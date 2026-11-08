---
title: "Game settings: the GameSetting.ini object and its options, the ini file's load and save, the quality presets, FrameLimit, DecideButton, the Config screen's commands, Active and Wait battle mode and the FF12CONFIG file"
kind: "system"
category: "Saving, loading and settings"
addresses: "0x001DE050, 0x001DED50, 0x001DE5D0, 0x001DF350, 0x001DEE90, 0x001DFD40, 0x001DE4F0, 0x0022BDF0, 0x001EDDC0, 0x0017E6E0, 0x0022A4F0, 0x002407F0, 0x002403F0, 0x002DDE60, 0x002DE060, 0x00255290, 0x00408C30, 0x001DF2C0, 0x00628690"
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

`0x007980A0`, the program's main routine, allocates `0x65C` bytes, builds the object with
`0x001DE050(object, path)` (`0x00798257`) and keeps it at `0x01F82D20` (`0x00798261`). The path is the
save directory (see the [saving and loading page](saving-and-loading.md)) joined with
`GameSetting.ini` (`0x01CB35F8`, `0x00798218`) and stored at `+0x450` as a wide string.

`0x001DE050` fills the object in three steps:

1. column 0 of the defaults table `0x00900CE0` (31 rows of 16 bytes) into the 31 dwords at `+0x00`;
2. Resolution and WindowSize from the desktop size (`GetSystemMetrics(0) << 16 |
   GetSystemMetrics(1)`);
3. Language from the Windows LANGID (see the [languages page](languages.md)).

Before step 1 `0x001DE050` stores `0x0101` at `+0x658` and 1 at `+0x44C` and `+0x65A` (`0x001DE069`-`0x001DE07B`);
step 2 writes the one value to Resolution (`+0x04`) and WindowSize (`+0x2C`) (`0x001DE0BA`, `0x001DE0BD`). After step
3 it zeroes the 972 bytes of value tables from `+0x7C` to `+0x447` (`0x001DE130`-`0x001DE13E`) and copies the path to
`+0x450` with `wcscpy_s` (260 characters) only when the path is not null (`0x001DE143`-`0x001DE157`). It returns the
object (`0x001DE162`).

`0x001DED50` then opens the file: when it is missing, the value tables are initialised (`0x001DF240`)
and the file is written from the defaults (`0x001DFD40`); otherwise the text is parsed (`0x001DE5D0`).

`0x001DED50` opens the path at `+0x450` with `_wfopen_s` mode `"rb"` (`0x001DED8A`). With no file it runs those two and
returns the result of `0x001DFD40` (`0x001DEE38`-`0x001DEE43`). With a file it clears `+0x658` and `+0x65A` (`0x001DED9F`,
`0x001DEDA8`), measures the file with `fseek` and `ftell`, and reads it whole with `fread` into a zeroed stack buffer
of `size + 0x20` bytes (`0x001DEDB3`-`0x001DEE19`). It closes the file (`fclose`, `0x001DEE23`), parses the buffer with
`0x001DE5D0` and returns 0 (`0x001DEE2F`-`0x001DEE34`); `0x001DF240` does not run on this path.

### The 31 settings

The defaults table has four columns, one per quality level (Low, Medium, High, Custom); column 0 is
the start-up default. The reset flag at `0x00900CC0 + index` marks the ten settings the quality
presets control.

| # | Key (`0x01DFD050`) | Defaults Low, Medium, High, Custom | Preset | Value names (`0x01DFD150`) |
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
(`0x01DFD148`); the value-name rows hold up to nine pointers and the strings sit at `0x008C5904`
onward. The value-name rows of the numeric settings hold only a pointer to the string `none`.

### Parsing the file

`0x001DE5D0(object, text)` reads the file line by line:

1. A line without `=` is logged as `[ConfigFile] invalid line`.
2. The key is matched case-insensitively against the 31 keys; a key outside the table is logged
   as `[ConfigFile] invalid key`.
3. `0x001DF350(object, index, value)` stores the value:
   - Resolution and WindowSize take `width*height` (split at the `*` that `0x00900B10` holds; a value without
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
   `0x01DFDA58`, `0x01DFDBA8` and `0x01DFDCF8` are set to `{12, 13}`: entries 18 and 19 of the three id tables, 12 into
   those words and 13 into `0x01DFDA5C`, `0x01DFDBAC` and `0x01DFDCFC` (`0x001DECBA`, `0x001DECCE`, `0x001DECE2`).

The parser reads the text through a string stream: `0x001DF7D0` copies the text into the stream's
buffer and sets its pointers, `0x001A9E10` builds the key and value strings, `0x001DFA00` returns a
string's characters (the heap copy once its capacity is above 15) and `0x001DF760` frees a buffer.

### Writing the file

`0x001DEE90` serialises all 31 settings as `Key=Value`: Resolution and WindowSize as
`width*height`, a setting with one value name as its number, and any other setting as the name of
its current value (`DecideButton=Circle`). It builds the text in a string stream, takes it out with
`0x001E00D0` (which calls `0x001E0100` on the stream's buffer at `+8`), and releases the buffer with
`0x001DF8C0`. `0x001DFD40` writes that text to the ini path with `_wfopen_s("wb")`.

When the open fails `0x001DFD40` writes nothing (`0x001DFD85`). Otherwise it calls `0x001DEE90` with a null buffer and
takes its result as the length `n` (`0x001DFD87`-`0x001DFD91`), calls it again into a zeroed stack buffer of `n + 1`
bytes (`0x001DFDB9`-`0x001DFDCE`), writes `n` bytes with `fwrite` and closes the file (`0x001DFDE2`, `0x001DFDEC`). On both
paths it returns `GetLastError()` (`0x001DFDF2`).

### The three writers

| Writer | Site | What it writes |
|---|---|---|
| `0x001DE050` | `0x001DE099` | the defaults copy at start-up |
| `0x001DF350` | `0x001DF6AE` | the parsed file value |
| `0x001DF340(object, index, value)` | `0x001DF343` | the runtime setter the Config screen uses |

### The quality presets

`0x001DE4F0(object, quality)` returns at once when Quality already equals the argument; otherwise it
stores it at `+0x0C` and, for every setting whose reset flag is set, copies the defaults table's
column `quality` unless the quality is 3. Its one caller is `0x001D5120` (`0x001D5139`), the
graphics-settings apply. Of the ten settings the preset stores, it then pushes six to their consumers, in this
order:

1. Anisotropic (`+0x18`) to the samplers: `0x0018AC50([0x01F7E340])` and `0x001BD940(0x001BDAB0())`
   (`0x001D513E`-`0x001D5152`), which take the anisotropy from `0x001DE540`
   ([config screen](../Menus-And-HUD/config-screen.md)).
2. WaterQuality (`+0x40`) to `0x001A5B00(0x001A9930(), value)`.
3. Shadow (`+0x1C`) as the pair `0x00900F00[Shadow % 3]` (`0x001DE5A0`), the shadow map size for Low,
   Medium and High: 512, 1024 and 2048 on each axis, to `0x001EF520(0x001F0850(), high, low)`.
4. MSAA (`+0x20`) as a non-zero flag to byte `+0xDBA` of `0x00189120()`, and as the sample count
   `0x00900EE8[MSAA % 5]` = 1, 2, 4, 8 or 9 (`0x001DE570`) to `0x00189520`.
5. PostAA (`+0x24`) == 1 to byte `+0x4A3` of `0x00193D50()`.
6. SoftParticle (`+0x38`) == 1 to the virtual slot `+0x60` of the object at the caller's `+0xA80`.

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
sets it to 1 (bit `0x1`, Off), and `0x0017D9C0(bit)` adds one more bit through `0x001DF2B0(object, bit)`.

The device setup `0x00628690` asks the device at its `+0x108` for the quality level count of format
`0x1C` (`R8G8B8A8_UNORM`) at sample counts 2 to 32 (virtual slot `+0xF0`, `CheckMultisampleQualityLevels`
in the `ID3D11Device` layout). For every count with a non-zero level count it sets:

| Sample count | Bit, MSAA value |
|---|---|
| 2 | `0x2`, 1 MSAA2X |
| 4 | `0x4`, 2 MSAA4X |
| 8 | `0x8`, 3 MSAA8X; also `0x10`, 4 CSAA16x, when the level count is above 16 |
| 16 | `0x20`, 5 CSAA16XQ |

`0x001DF2C0(object, value, forward)` steps from `value` to the next value (or, with `forward` 0, the
previous one) in 0-4 whose bit is set, wrapping around, and stores it as MSAA (`+0x20`) of the
object at `0x01F82D20`. Its one caller is the Graphics Settings dispatcher `0x001D1660` (`0x001D4A53`), which the
Config screen's Anti-Aliasing row reaches through `0x0017DB90` and `0x001CD040` ([Config screen](../Menus-And-HUD/config-screen.md));
it then sets byte `+0xDBA` of `0x00189120()` to whether the result is non-zero.

### FrameLimit

`0x0017D8F0` returns FrameLimit (`+0x48`). `0x0022BDF0`, the first call of the boot frame mode
`0x0022A0B0`, reads it, scans the command line for `-nologo` (which calls `0x00314DE0(1)`), and calls
`0x001EDDC0(FrameLimit == 1)`:

| FrameLimit | `0x01DFE0B4` | `0x01DFE0B8` | `0x01DFE0BC` | `0x01F82E38` |
|---|---|---|---|---|
| 0 (30) | left at the image value 1 | left at 1.0 | left at 1.0 | untouched |
| 1 (60) | 2 | 2.0 (`0x01CEBC08`) | 0.5 (`0x01CEBB70`) | 1 |

The 30 fps arm leaves all three cells of the triple at their image values; it begins a multimedia timer period instead
(`timeGetDevCaps(&caps, 8)`, and only when that returns 0 (`0x001EDE31`) `timeBeginPeriod(wPeriodMin)`, keeping the
period at `0x01F82E40` and setting `0x01F82E3C` = 1; a failed `timeGetDevCaps` begins no period). The 60 fps arm also
calls `0x0033F020` and ends that period when one was begun (`timeEndPeriod([0x01F82E40])` and `0x01F82E3C` = 0,
`0x001EDE01`-`0x001EDE17`). Both arms then call `0x0032AE70`, `0x003333D0`, `0x00337A00` and `0x002BDA90` (the last as a tail
jump, `0x001EDE60`).

The triple is the game's time base: authored frame counts are multiplied by `0x01DFE0B8` (for
example the loot pickup lifetime, see the [loot pickups page](../Rewards-EXP-Gil-And-Loot/loot-pickups.md)),
and per-frame fades by `0x01DFE0BC`, so durations keep their wall-clock length at 60 fps.

### DecideButton

The Config screen's command `0x26` calls `0x0017E6E0(value)`: `0x001DF340(object, 25, value)`, which stores the value as
DecideButton (`+0x64`), then `0x00198960(0x00198790(), value == 0)` for the input manager, then `0x0022A4F0`, which reads
DecideButton back through `0x0017E210` (`0x0022A4F4`) and sets the confirm mask `0x01E0C2A0` and the cancel mask `0x01E0C2A4`
to `0x2000` and `0x4000` for value 0 and the reverse otherwise, as 16-bit stores (`0x0022A526`, `0x0022A51F`), and
`0x01FD4A64` to whether the value is non-zero (`0x0022A510`). The same masks are set at boot (see the
[languages page](languages.md)).

The Controls screen's Default calls `0x0017E520`, which runs `0x001DEE70` on the object: CameraRevise
(`+0x58`) = 1, MouseSensityX (`+0x5C`) = 4, and one 8-byte store that sets MouseSensityY (`+0x60`) to
4 and DecideButton (`+0x64`) to 0. Its caller `0x0023E020` then applies the masks with `0x0022A4F0`.

### The Config screen's commands

Two dispatchers switch on command ids 4-38 through 35-slot tables: the setter `0x002407F0` (table
`0x00240968`; each arm loads the row's value, calls the setter and jumps to the empty stub
`0x0016D6A0`) and the getter `0x002403F0` (table `0x00240518`). Two wrappers normalise values around
them: `0x00240750` (set: normalise, then `0x002407F0`) and `0x00240330` (get: `0x002403F0`, then
normalise), switching on the id through their index tables at `0x002407C0` and `0x002403CC`:

| Selector | Ids | Normalisation |
|---|---|---|
| 0 | 4, 12, 13 | `v != 0` |
| 1 | 5, 29, 30 | `v + 1` on set, `v - 1` on get |
| 2 | 6, 8, 9, 10, 11, 16, 28 | `v == 0` |
| 4 | 38 | `v != 1` |
| 3, 5 | 17; every other id | unchanged |

In `0x002407F0` the ids 7, 15, 18, 22-27 and 31-37, and any id outside 4-38, go straight to `0x0016D6A0` and set
nothing (`0x002407F6`-`0x002407FF`, `0x0024095E`). Id 8 passes the same value to both of its setters
(`0x0024084B`-`0x00240854`), id 14 calls `0x0023B2E0` after its setter (`0x002408B8`-`0x002408BF`), and id 17 loads its value
as a `u16` (`0x002408DF`).

`0x002403F0(id, out)` first stores 0 at `out` (`0x002403F9`). An id outside 4-38 (`0x00240405`) and the ids the table
sends to the exit, 7, 15, 18, 22-27 and 31-37 (`0x00240512`), leave that 0. Every other id stores its getter's
result from the table below, the music version's `u16` zero-extended (`0x002404B2`).

The in-game options are an `0x28`-byte record inside the save image: `0x002DDE60` sets `0x0215E6E0`
to `0x002536A0() + 8`, writes the template `{0x00000035, 0x00620400}` and patches it (bit `0x20000` of
dword 0 from `0x005C5230() == 2`; bit `0x1000` of dword 0 set for locale ids 1 and 6; bit `0x400` of dword 1
set for locale ids 0, 7, 8, 10 and 11), clears the camera-axis bits and pushes them to `0x001E1020`
and `0x001E0FF0`, sets the music version to 1 (`0x002DF530(1, 1)`), clears the speed-mode field, sets
the three volumes to 100 (`0x001DBA60(1.0, channel)`), and runs the platform applier `0x002DDA30(1)`.

| Command | Option | Setter | Field | Getter |
|---|---|---|---|---|
| 4 | Battle Mode (Wait, Active) | `0x002DE060` | dword 0 bit `0x8` | `0x002DDC30` |
| 5 | Battle Speed | `0x002DE0F0` | dword 0 bits `0xFF0`, signed | `0x002DDC90` |
| 6 | Target Lines | `0x002DE2D0` | dword 1 bit `0x400000` | `0x002DDE00` |
| 8 | Cursor Position | `0x002DE1E0`, `0x002DE1C0` | dword 0 bits `0x8000` and `0x10000` | `0x002DDD50` |
| 9 | Vibration | `0x002DE080` | dword 0 bit `0x2000`, pushed to `0x0035FF30` | `0x002DDC40` |
| 10 | Screen Shake | `0x002DE200` | dword 0 bit `0x4000`, pushed to `0x0037DDC0` | `0x002DDD60` |
| 11 | Subtitles | `0x002DE230` | dword 0 bit `0x1000` | `0x002DDD70` |
| 12 | Camera Y-Axis | `0x002DE190` | dword 1 bit `0x100`, pushed to `0x001E1020` | `0x002DDD20` |
| 13 | Camera X-Axis | `0x002DE160` | dword 1 bit `0x200`, pushed to `0x001E0FF0` | `0x002DDD00` |
| 14 | Speed Mode Multiplier | `0x002DE250`, `0x0023B2E0` | dword 1 bits `0x7800000`: the getter returns `(dword1 >> 23) & 0xF` (`0x002DDDAA`-`0x002DDDAD`); the setter clears the bits with `dword1 & 0xF87FFFFF` and sets `(v & 0xF) << 23` (`0x002DE257`-`0x002DE264`) | `0x002DDDA0` |
| 16 | Voice language | `0x002DE2F0` | dword 1 bit `0x400` | `0x002DDE20` |
| 17 | Music version | `0x002DE110` | `+0x0E` u16, pushed to `0x002DF530` | `0x002DDCA0` |
| 19, 20, 21 | Music, Sound Effects, Voice volume | `0x002DE0B0`, `0x002DE290`, `0x002DE310` | `+0x08`, `+0x0A`, `+0x0C` u16, at most 100, pushed to `0x002DF2B0` on channels 1-3 | `0x002DDC70`, `0x002DDDE0`, `0x002DDE40` |
| 28 | Camera Auto-Rotation | `0x0017E740` | `0x001DF340(object, 22)` CameraRevise | `0x0017E260` |
| 29, 30 | Mouse Sensitivity | `0x0032E020`, `0x0032E030` | `0x001DF340(object, 24)`, `0x001DF340(object, 23)`, values 1-6 | `0x0017E420`, `0x0017E430` |
| 38 | Confirm Button | `0x0017E6E0` | `0x001DF340(object, 25)` DecideButton | `0x0017E210` |

Because the record lives in the save image, loading a save also loads these options.

### Active and Wait

`0x002DE060(value)` writes bit `0x8` of the options dword (`0x0215E6E0`) and `0x002DDC30` reads it (1 =
Active). `0x00255290(mode)` maps a UI mode to a halt class, -1 meaning no halt:

| UI mode | Halt class |
|---|---|
| 1 | -1 when the bit is set, 0 when clear |
| 4 | 0 when the bit is set, -1 when clear |
| 2, 6, `0xF`, `0x11`, `0x12`, `0x13`, `0x16` | `0xD` |
| 3, `0x18` | 2 |
| `0x14` | 0 |
| other | -1 |

`0x00254740(mode)` applies a class other than -1 through `0x00226BE0`, which sets that halt bit on every
actor, so in Wait mode entering UI mode 1 halts the field and in Active mode it does not. The bit's
readers are the Config getter, `0x00254740`, `0x00255290`, `0x00225CD0`, `0x00225EB0` and `0x00227680`.

Before the halt, `0x00254740` sets bit `0x1` of `0x02EBDBBC` (`0x003B3B40`) when the class is not -1 and the UI mode is 3,
`0x14` or `0x18` (in both battle modes), 1 (Wait mode only: `0x002DDC30` answers 0 at `0x00254775`) or 4 (Active mode
only: its class from `0x00255290` is -1 with the bit clear, `0x002552C7`-`0x002552D2`, and `0x0025475D` returns).
While that bit is set the effect step `0x0024B9B0` sets bit `0x4` of the effect group mask it tests
(`0x0024B9F1`-`0x0024B9F9`); `0x0024D540`, `0x0024D9C0` and `0x0024E910` clear it (`0x0024D75B`, `0x0024DA05`, `0x0024E99D`).

In Wait mode the time stop of id 0 also sets bit `0x2` of the input manager's movement-key mode byte (`0x00182D10`,
reached from `0x00227680` at `0x002277FD`), and its cancel clears it (`0x00182DA0`, from `0x00225CD0` at `0x00225E81` and from
`0x00225EB0` at `0x00226052`); in Active mode neither call runs ([Time stop and freeze](../Engine-Core/time-stop-and-freeze.md)).
The Config painter `0x002403F0` shows the bit's value (`0x0024041E`).

### The FF12CONFIG file

`0x003692D0` resets the block at `0x02B62DA8` with `0x00408BA0` (`0x00369323`) and then runs `0x00408C30`
(`0x0036943F`), which reads `PS2Data/SQUARE_FF12/FF12CONFIG` from the archive (`0x001D6F20`, `0x800`
bytes) and copies its bytes into the globals listed in the layout below.

- The u16 at file `+0x0A` goes to `0x02B62DB4` unless the dword `0x01E02804` is not negative, in which
  case its low word is stored instead.
- `0x02B62DAB` is always set to 1, and `0x02B62DB4` is zeroed when the second command-line argument is
  `debug`. The arguments come from `0x0017D240(&vector, &count)`, which returns the pointer and count
  the application object keeps at `0x01F7F480` and `0x01F7F488` (its `+0x1130` and `+0x1138`, stored by
  `0x0017CEB0`).
- When the file loads, `0x02B62DAD` is first set to `0x01E02804 >= 0`.
- The `0x01E02810` branch (a `FFXII_%03d` or `PS2Data//oldsave//new%03d` probe that sets `0x02B62DAD`
  = 2) runs only when that dword is not negative.
- Both dwords are -1 in the image, so `0x02B62DAD` stays 0 and neither branch runs in the shipped
  game.

Of the file's 2,048 bytes, only `+0x06` and `+0x10` can change what the player sees, and both are 0 in the shipped
file. They override the Vibration Function and Screen Shake options whenever the options are reset to their
defaults: 1 turns the option on, 2 turns it off, and any other value keeps the default. A loaded save keeps its own
options. [`game-settings-ff12config-values.tsv`](game-settings-ff12config-values.tsv) gives every byte: its shipped
value, the global it is copied to, its readers, and what another value does.

[The FF12CONFIG inputs](game-settings-inputs.tsv) table gives each of the 22 entries as a setting: its values, what
else sets the same state and which wins, when it takes effect, what reads it, what the player sees, and when it
changes nothing.

- `0x002DDA30` reads `+0x06` and `+0x10` through the getters `0x00408B80` and `0x00408B40` (`0x002DDA3B`, `0x002DDA66`) only
  when it is entered with 1. The options-defaults installer `0x002DDE60` enters it with 1 (`0x002DE035`) at start-up,
  on the title screen, on the return to the title and for Restore Defaults; the save-load applier `0x002DE050` enters
  it with 0.
- Value 1 ORs `0x2000` (Vibration Function) or `0x4000` (Screen Shake) into dword 0 of the options record, and value
  2 clears that bit (`0x002DDA51`-`0x002DDA8B`). The bits then go to `0x0035FF30`, which lets the pad's motors run
  ([Vibration](../Controls-And-Input/vibration.md)), and to `0x0037DDC0`, which gates the camera-shake row
  ([Scripted camera](../Graphics/scripted-camera.md)).
- `+0x0D` is the start value of the HDD-use flag `0x02B62DB1`, which the script verb `getusehdd` (`0x376`, `0x00341DD0`)
  returns unchanged. `setusehdd` (`0x375`, `0x00341980`) stores its argument != 0 and the `hddinstall` and
  `networkhddinstall` result `0x003447F0` stores 1, both through `0x00408EC0`. None of the 1,114 decompiled US scripts
  calls these verbs ([Verb table](../Scripts-And-Script-Commands/verb-table.md)).
- `+0x0A` (236, Throne Road) never picks a field. The start-up `0x003318C0` and the return to the title `0x00331920` use
  `0x02B62DB4` only while `0x02B62DAD` is 1, which needs `0x01E02804` not negative, and then that dword's low word has
  replaced the file's value. With the shipped -1 both request field 12, `ttl_a01` (`0x00331903`, `0x0033196D`).
- `+0x02` is compared with 3 at 15 sites in five functions (getter `0x00408B10`), each behind a test of `0x02B62DAB`
  that skips the comparison on 1. The loader stores the file's value and sets `0x02B62DAB` to 1 in the same run
  (`0x00408CCB`, `0x00408D89`), and only the reset `0x00408BA0` also writes that byte, with 1, so the file's value is
  never compared.
- `+0x04` is read once, at start-up (`0x003694E2`): 1 passes 1 and any other value 0 to `0x0016D6A0`, which is a bare
  `ret`.
- `+0x03`, `+0x08`, `+0x09`, `+0x0C`, `+0x0E`, `+0x0F`, `+0x11`, `+0x12`, `+0x15` and `+0x16` are copied and never
  read. The reset `0x00408BA0` and the loader's stores are the only instructions that reach their globals: no other
  rip-relative operand, image-base-relative displacement, immediate, data qword or RVA in the image reaches the
  block.
- `+0x00`, `+0x01`, `+0x05`, `+0x07`, `+0x13`, `+0x14` and every byte from `+0x17` on are not copied: the loader
  reads only the offsets in the layout from its stack copy (`0x00408CBB`-`0x00408D79`).

The loader zeroes a `0x800`-byte buffer with `memset` and reads at most `0x800` bytes into it (`0x00408C80`,
`0x00408CAE`), so a shorter entry reads as if padded with zeros and anything past `0x800` is never read. Without the
entry no byte is copied and the reset values stay, which plays the same as the shipped file: neither override byte
is set in either. The entry is read once per start, in start-up step 8
([Startup constants](../Engine-Core/startup-constants.md)).

The block's other bytes are not taken from the file:

- `0x02B62DAB` is always 1, and the getter `0x00408B30` reads it only for the 15 tests above.
- `0x02B62DAD` selects the start-up field: 0 requests field 12, 1 the field in `0x02B62DB4`, and 2 passes the old-save
  number `0x02B62DC0` to the empty `0x0016D6A0` and requests no field (`0x003318C4`-`0x003318FE`). It is 0 in the shipped game.
- `0x02B62DB9` is the debug-status flag. It is reset to 0, and no other instruction in the image writes it. While it
  is 0, a jump to field 0 goes to field 12 (`0x00314463`-`0x0031446E`), the pad updates `0x0035FCA0` and `0x0035FF90`
  handle channel 0 only, and the verb `debug_getdebugstatus` (`0x20A6`, `0x0050DFC0`) returns 0.
- `0x02B62DBA` is reset to 0 and never read. `0x02B62DC0`, a u16, is written only in the old-save branch (`0x00408E87`)
  and read by `0x00408B20` at `0x003318EA` and `0x00331953`.

### Columns of game-settings-ff12config-values.tsv and game-settings-inputs.tsv

Both tables have one row per entry of the FF12CONFIG layout, 22 rows in the same order, from `+0x00` to the run
`+0x17-+0x7FF`.

| Column | Holds |
|---|---|
| `shipped_effect` | in game-settings-ff12config-values.tsv, what the shipped byte does: on all 22 rows it changes nothing the player sees; on 6 rows the cell gives the reason after a colon (a value never tested on `+0x02`, the empty function `0x0016D6A0` on `+0x04`, the option's default kept on `+0x06` and `+0x10`, the start field on `+0x0A`, no script asking on `+0x0D`) |
| `other_values` | in game-settings-ff12config-values.tsv, what any other value would do: on `+0x06` and `+0x10` the options bit that 1 sets and 2 clears; on `+0x0D` what `getusehdd` would answer; on `+0x02`, `+0x04` and `+0x0A` why no value changes anything; on the other 16 rows no value changes anything |
| `label` | in game-settings-inputs.tsv, `FF12CONFIG`, the entry's offset and its `name` in game-settings-ff12config-values.tsv, on all 22 rows |
| `domain` | the values the entry takes: `any value of its u8` on 14 rows, of its `u8[2]` on `+0x13` and of its `u8[2025]` on the run; `a u16 field id` on `+0x0A`; on `+0x02`, `+0x04`, `+0x06`, `+0x0D` and `+0x10`, which values are tested and what each does |
| `precedence` | what else sets the same state and which wins: `the file is its only source` on 11 rows; `-` on the 6 entries the loader does not copy; on `+0x02`, `+0x06`, `+0x0A`, `+0x0D` and `+0x10`, the other writer or gate and when the file's value applies |
| `visible_effect` | what the player sees: on `+0x06` and `+0x10`, the Vibration Function or Screen Shake option starting on or off for 1 or 2; on the other 20 rows nothing, with the reason on `+0x0A` and `+0x0D` |
| `inert_when` | when the entry changes nothing, with the reason: `always` on 19 rows (6 entries not copied, 10 copied but never read, `+0x02` whose test no site reaches, `+0x04` whose function is a bare `ret`, and `+0x0A` in the shipped game); on `+0x0D`, in every US script; on `+0x06` and `+0x10`, for any value other than 1 and 2 and while a loaded save's options are in force |

## Layouts

`GameSettingObject` (`0x65C` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u32[31]` | settings | the 31 settings, offset = index * 4; `0x001DE050`, `0x001DF350`, `0x001DF340` |
| `+0x07C` | `u8[972]` | tables | the value tables `0x001DF240` fills from `0x01DFDA10`, `0x01DFDB60` and `0x01DFDCB0` (81 dwords each at `+0x7C`, `+0x1C0` and `+0x304`) |
| `+0x448` | `u32` | count | 81 after `0x001DF240` |
| `+0x44C` | `u32` | msaa | bit set of the supported MSAA values: 1 from `0x001DE050`, more bits from `0x001DF2B0`; read by `0x001DF2C0` |
| `+0x450` | `u16[260]` | path | the ini path, wcscpy_s by `0x001DE050` |
| `+0x658` | `u16` | fresh | `0x0101` from `0x001DE050`, 0 after a file load (`0x001DED50`) |
| `+0x65A` | `u8` | fresh2 | 1 from `0x001DE050`, 0 after a file load |
| `+0x65B` | `u8` | pad | not written by `0x001DE050`, `0x001DED50` or `0x001DF240` |

`Ff12Config` (`0x17` bytes, offsets from the start of the file):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | unread00 | not copied by `0x00408C30` |
| `+0x01` | `u8` | unread01 | not copied |
| `+0x02` | `u8` | opt02 | to `0x02B62DA8` (reset value 3) |
| `+0x03` | `u8` | opt03 | to `0x02B62DA9` |
| `+0x04` | `u8` | opt04 | to `0x02B62DAA` |
| `+0x05` | `u8` | unread05 | not copied |
| `+0x06` | `u8` | opt06 | to `0x02B62DAC` |
| `+0x07` | `u8` | unread07 | not copied |
| `+0x08` | `u8` | opt08 | to `0x02B62DAE` |
| `+0x09` | `u8` | opt09 | to `0x02B62DAF` (reset value 1) |
| `+0x0A` | `u16` | fieldId | to `0x02B62DB4` unless `0x01E02804` is not negative |
| `+0x0C` | `u8` | opt0C | to `0x02B62DB0` |
| `+0x0D` | `u8` | opt0D | to `0x02B62DB1` |
| `+0x0E` | `u8` | opt0E | to `0x02B62DB2` |
| `+0x0F` | `u8` | opt0F | to `0x02B62DB3` |
| `+0x10` | `u8` | opt10 | to `0x02B62DB6` |
| `+0x11` | `u8` | opt11 | to `0x02B62DB7` |
| `+0x12` | `u8` | opt12 | to `0x02B62DB8` |
| `+0x13` | `u8[2]` | unread13 | not copied |
| `+0x15` | `u8` | opt15 | to `0x02B62DBB` (not reset by `0x00408BA0`) |
| `+0x16` | `u8` | opt16 | to `0x02B62DBC` |

## Operations

| Function | Role |
|---|---|
| `0x001DE050` | build the settings object: defaults, desktop size, the Windows Region Format language, path |
| `0x001DED50` | load the ini, or create it from the defaults |
| `0x001DE5D0`, `0x001DF350` | parse the text, parse one value |
| `0x001DEE90`, `0x001DFD40` | serialise, write the file |
| `0x001DE4F0` | apply a quality preset |
| `0x00628690`, `0x001DF2B0`, `0x001DF2C0` | record the supported MSAA values, step MSAA through them |
| `0x001DEE70` | reset the four control settings |
| `0x0022BDF0`, `0x001EDDC0` | read FrameLimit at boot, set the time base |
| `0x0017E6E0`, `0x0022A4F0` | DecideButton setter, mask applier |
| `0x002407F0`, `0x002403F0` | the Config screen's set and get dispatchers |
| `0x002DDE60` | install the in-game options record defaults |
| `0x00408BA0`, `0x00408C30` | reset and load the FF12CONFIG block |

## State

| Address | Width | Meaning | Written by |
|---|---|---|---|
| `0x01F82D20` | `void*` | the settings object | `0x007980A0` |
| `0x0215E6E0` | `void*` | the in-game options record, `0x002536A0() + 8` inside the save image | `0x002DDE60` |
| `0x01DFE0B4` / `0x01DFE0B8` / `0x01DFE0BC` | `i32` / `f32` / `f32` | the time base | `0x001EDDC0` |
| `0x01F82E38` | `i32` | the 60 fps gate | `0x001EDDC0` |
| `0x01E0C2A0` / `0x01E0C2A4` | `u16` | confirm and cancel masks | `0x0022A4F0`, boot mode 0 |
| `0x02B62DA8`-`0x02B62DC1` | bytes | the FF12CONFIG block | `0x00408BA0`, `0x00408C30`, `0x00408EC0` |

`0x002DDE60` builds the options template in a `0x28`-byte staging copy at `0x0215E6E8` and does not write it into the
record directly. It copies the `.rdata` template `0x00917268`-`0x0091728F` into the copy (`0x002DDE6F`-`0x002DDE9F`). It sets
bit `0x20000` of dword 0 to `0x005C5230() == 2` (`0x002DDEB2`-`0x002DDEC5`), which is always 0 because that stub returns 0. Then
it copies the staging copy into the record at `[0x0215E6E0]` (`0x002DDECB`-`0x002DDEEF`), and the patches after that go to
the record:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x0215E6E8` | `u32[4]` | 0 (zero-filled tail of `.data`) | dwords 0-3 of the staging copy: `0x35` with bit `0x20000` clear, `0x00620400`, 0 and `0x00010000` | `0x002DDE60` (`0x002DDE88`, 16 bytes; `0x002DDEC5`, dword 0) | `0x002DDE60` (`0x002DDEB2`, dword 0; `0x002DDECB`, 16 bytes) |
| `0x0215E6F8` | `u32[4]` | 0 (zero-filled tail of `.data`) | dwords 4-7 of the staging copy, all 0 in the template | `0x002DDE60` (`0x002DDE9F`) | `0x002DDE60` (`0x002DDEDC`) |
| `0x0215E708` | `u64` | 0 (zero-filled tail of `.data`) | the last 8 bytes of the staging copy, 0 in the template | `0x002DDE60` (`0x002DDE97`) | `0x002DDE60` (`0x002DDEE7`) |

## Modding notes

- Values in GameSetting.ini are matched by name, case-insensitively; a numeric value is accepted
  only for settings without value names. A key outside the table is ignored and logged.
- Quality Low, Medium and High overwrite the ten preset settings on every load; set Quality to
  Custom to keep edited values.
- FrameLimit is the only setting that rescales timed behaviour; everything that reads
  `0x01DFE0B8` follows it.
- The Config screen's options are stored in the save image, so editing a save edits them.
- Of FF12CONFIG only `+0x06` and `+0x10` change the game: 1 turns Vibration Function or Screen Shake on and 2 off
  whenever the options are reset to their defaults; a loaded save keeps its own options.

## Related

- [Languages: the Language setting, the nine language codes, the locale id each maps to, the data folder it selects, the Windows-locale default, and the confirm and cancel buttons](languages.md)
- [Saving and loading: the save slots and their files, the save screen's states, the six-step save transaction, the storage queue, the file layer's read and write rules, the area-change autosave and what a load runs](saving-and-loading.md)
- [Save file format: the SAFH container, its zlib and RC4 layers, the save image and its header fields, the four in-memory copies and the format stamps](save-file-format.md)
- [Loot pickups: the ten-slot pool, creation and eviction, the one-minute lifetime and blink, collection on contact, and the pickup object](../Rewards-EXP-Gil-And-Loot/loot-pickups.md)
- [`game-setting-config-accesses.tsv`](game-setting-config-accesses.tsv): every access to the settings
  object at `[0x01F82D20]`, by its offset in the object (163 rows).
- [`game-setting-key-name-accesses.tsv`](game-setting-key-name-accesses.tsv): the reads of the key table at
  `0x01DFD050` (31 entries of 8 bytes), all in the serialiser `0x001DEE90` (3 rows).
- [`game-setting-value-name-row-accesses.tsv`](game-setting-value-name-row-accesses.tsv): the read of the value-name
  rows at `0x01DFD150` (31 rows of `0x48` bytes) in `0x001DEE90` (1 row).
- [`game-settings-command-table.tsv`](game-settings-command-table.tsv): the Config commands that have a handler, one
  row per command id; the other 16 ids from 4 to 38 fall to the default arms `0x0024095E` and `0x00240512` (19 rows).

In the access tables, `function`, `name` and `site` give the function, its name and the instruction's address,
`disp` the offset in the object or the entry, `kind` a read (`r`), a write (`w`) or the address taken (`addr`),
`instruction` the instruction itself, and `route` how the object reached it:

- `ptr load S`: the pointer at `0x01F82D20`, loaded at S; `ctor`: inside `0x001DE050`, which receives the object in
  `rcx` and keeps it in `rsi`, as the `note` says;
- `route-seeded ARRAY` with the table's address, stride and count: an entry of the key table or of the value-name
  rows.

The command table's columns:

- `cmd` the command id; `label_tid` and `label` the text id and text of the row's label, and `choices` the choice
  texts with their text ids;
- `setter` the function the set arm calls, `extra_call` a further function the arm calls (`-` when it calls no
  other) and `stores` the option bits it writes; `getter` and `reads` the same for the get arm (`opt+0`: the options
  record at offset 0);
- `sel` the normalisation the two wrappers apply (the selector table above); `set_arm` and `get_arm` the command's
  arms in the two dispatchers;
- `row_style` the style byte of the command's entry in the descriptor table at `0x01E0BF60`; `pane_row` the row's item
  index in descriptors 0, 1 and 2 of that table (`desc1--` where descriptor 1 leaves it out) or, for a Controls
  screen row, its pane record; `reachability` the screens that show it.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Script VM: `0x00182D10` is called by `0x00341030`; `0x00182DA0` is called by `0x003413E0`; `0x00341980` calls `0x00267E10`;
  `0x00341DD0` calls `0x0026B4E0`; `0x00408EC0` is called by `0x00341980`, `0x003447F0`; `0x0050DFC0` calls `0x0026B4E0`.
- Script VM: those functions are documented on [controls](../Controls-And-Input/controls.md),
  [force fight mode](../Engine-Core/force-fight-mode.md),
  [native commands](../Scripts-And-Script-Commands/native-commands.md),
  [verb table](../Scripts-And-Script-Commands/verb-table.md).
- World area: `0x003318C0` calls `0x00314440`; `0x00331920` calls `0x00314440`; `0x00408B10` is called by `0x0032FC30`; `0x00408B20`
  is called by `0x003318C0`, `0x00331920`; `0x00408B30` is called by `0x0032FC30`.
- World area: those functions are documented on [debug menu](../Engine-Core/debug-menu.md),
  [frame update order](../Engine-Core/frame-update-order.md),
  [game over](../World-Areas-And-Travel/game-over.md).
