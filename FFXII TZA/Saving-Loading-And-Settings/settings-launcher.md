---
title: "Settings launcher: FFXII_TZA_GameSetting.exe, the options it writes to GameSetting.ini, the display list it builds, its reset button, and every other file the game ships beside the executable"
kind: "system"
category: "Saving, loading and settings"
addresses: "001DE050, 001F3ED0, 0079813C, 0078AD20, 007911D0, 00862C70"
---

## What the player sees

- Before the game starts, a small window offers the display adapter and monitor, screen mode, resolution,
  graphics quality, frame limit and VSync. OK and Apply save them; Cancel discards them.
- A Reset button, after a warning, deletes the keyboard control file, so the game rebuilds its default
  controls on the next start.
- The window follows the Steam language, or the Windows language when Steam does not answer, and it can be
  driven with a gamepad.

## How it works

The launcher is `FFXII_TZA_GameSetting.exe`, a 32-bit .NET Windows Forms program with the namespace
`GameSettings`; it never starts the game itself. The game reads what it writes when it starts
([Game settings](game-settings.md), `001DE050`). The method names below are those of its own metadata.

### Where the files live

`Program.InitGlobalConfig` reads the file names from the embedded resource `PathConfig`: `IniFile` is
`GameSetting.ini` and `ResetFile` is `keymap.ini`. It places both in `Documents\My Games\FINAL FANTASY XII THE
ZODIAC AGE\`, followed by the Steam account id when `SteamAPI.Init` succeeds, and creates the folder with
`SHCreateDirectory`. That is the folder the game uses for the same files (`001F3ED0`;
[Keymap file](../Controls-And-Input/keymap-file.md)).

Before it goes on, `SteamAPI.RestartAppIfNecessary(595520)` decides whether the program must be restarted
through Steam; on true the launcher exits at once. The game makes the same check with the same app id
(`0079813C`; [Steam integration](../Steam-And-Achievements/steam-integration.md)).

### The language

`Program.InitGlobalConfig` first takes a default from `GetUserDefaultLangID`: the Chinese locales 1028, 3076 and
5124 give `ch`, and otherwise the primary language picks `fr` (12), `de` (7), `it` (16), `es` (10), `jp` (17),
`kr` (18), `cn` (4) or `en`.

`Program.LoadIniFile` then keeps the file's `Language` value when there is one, and
`SetLanguageAccordingToSteam` overrides both with `SteamApps.GetCurrentGameLanguage`: `english`, `german`,
`french`, `italian`, `koreana`, `spanish`, `schinese`, `tchinese` and `japanese` become `en`, `de`, `fr`, `it`,
`kr`, `es`, `cn`, `ch` and `jp`, and the result is written back as `Language`.

The window's text comes from `SettingsLoc.xml`: one `Lang` element per language with its title, font, language
name, five message texts (`msg_Caption`, `msg_Content`, `msg_WarningCaption`, `msg_WarningContent`,
`msg_ErrorDiskFull`) and 24 `Text` elements, which `ConfigForm_Load` reads: `Text[@Control]` labels a control by
its name and `Text[@Key]` names a box item (`SM_WINDOW`, `VQ_LOW`, `FL_SIXTYFRAME`, `VSYNC_AUTO` and the rest). When the primary screen is under 720 pixels high, elements marked `small` are used
as well (`Program.XmlNodeSelectorCondition`).

### The display list

`Program.GetDisplayAdapter` keeps every DXGI adapter that has at least one output (SharpDX `Factory1`). The
adapter box lists their outputs in order. `ConfigForm.SaveGameSettingDisplayAdapter` stores the chosen one as
`DeviceID`, `LUIDLow` and `LUIDHigh` (the adapter's id, the low half of its LUID, and 0: the high half is computed
as `(int)(luid >> 32 << 32)`, which is always 0, and the readers compare with the same expression, so the match
still works) and `Monitor` (the output's
1-based index on that adapter).

`Program.UpdateResolutionAcorrdingMonitor` fills the resolution box from that output's display modes in format
R8G8B8A8, keeping each width x height once and only those at least 1280 x 720. With `FrameLimit` 60 it keeps only
modes of 59 Hz or more. When the stored adapter fields are missing or are not numbers, it uses the first output of
the adapter with the most dedicated video memory instead.

### The keys it writes

`ConfigForm.SaveConfiguration` writes:

| Key | Values | From |
|---|---|---|
| `ScreenMode` | `SM_WINDOW`, `SM_FULLSCREEN`, `SM_BORDERLESS` | the screen mode box (default `SM_FULLSCREEN`) |
| `WindowSize` | `width*height` | the resolution box, in windowed mode only |
| `Resolution` | `width*height` | the resolution box, in full-screen mode only |
| `Quality` | `VQ_LOW`, `VQ_MEDIUM`, `VQ_HIGH`, `VQ_CUSTOM` | the quality box (default `VQ_MEDIUM`) |
| `FrameLimit` | `30`, `60` | the frame limit box |
| `VSync` | `On`, `Off`, `Adaptive` | the VSync box (default `On`) |
| `DeviceID`, `LUIDLow`, `LUIDHigh`, `Monitor` | numbers | the adapter box |
| `Mute` | `Off` | a flag no control changes: its handler `ConfigForm.pictureBox2_Click` is attached to no control |
| `MasterVolume` | the number read from the file (default 100) | written back unchanged; the window has no volume control |

The game's settings table has neither `Mute` nor `MasterVolume`, so it ignores and logs both
([Game settings](game-settings.md)).

The file is plain `key=value` lines. On reading, `Program.LoadIniFile` matches each line with
`^[ \t]*(.+?)[\t ]*=[\t ]*(.+?)[\t ]*$` and turns the `*` in `Resolution` and `WindowSize` into `x` for display;
`Program.SaveIniFile` turns it back. It rewrites the whole file from what it read plus its changes, so keys it
does not know are kept.

In borderless mode the resolution box shows the size of the screen that holds the point
`LastX`, `LastY` from the file. When no screen holds it, it takes the screen whose bottom-right corner is nearest,
measured with `LastX` for both coordinates, and with no screen at all it falls back to `Resolution` or the primary
screen's size (`ConfigForm.UpdateResolutionComboBoxItems`).

A full disk (HRESULT `0x80070027` or `0x80070070`) shows the `msg_ErrorDiskFull` text; any other write error
shows the exception's message.

### Reset, OK, Apply and Cancel

- Reset shows the warning texts and, on OK, deletes `keymap.ini` (`ConfigForm.button_Reset_Click`).
- OK saves and exits; Apply saves and reloads the window; Cancel exits without saving.

### The rest of the program

- A named mutex, `A8825348-F5CE-4E67-8735-D4AF7E7E58F1`, keeps a second copy from opening; a second start shows
  the error message instead (`Program.IsSingleInstance`).
- A 100 ms timer reads every attached DirectInput game controller at once (SharpDX `DirectInput`;
  `Joy.FindJoysticks`, `Joy.AcquireJoystick`), ORs their hats and first four buttons into one mask with a
  three-tick repeat gate, and types keys for it (`ConfigForm.timer1_Tick`): up is Shift+Tab, down is Tab, left and right are the arrow keys, and button one clicks
  the focused button or the open message box's button.

### Leftovers in the program

- `PathConfig` also names `Hello.exe` for `FFX`, `FFX2` and `SideStory`, which nothing in this program reads, and
  the window's design-time title is "FINAL FANTASY X/X-2 Launcher", replaced by `ConfigTitle` when it loads.
- `ConfigForm.SetVersionInfo` reads `./code_steam.txt` and `./data.txt` and then sets the version label to the
  constant "Ver  1.0.4.0", the assembly version.
- The Custom quality item is removed from its box unless the file already says `VQ_CUSTOM` (`ConfigForm_Load`), and
  the frame-limit and VSync boxes write their key on every change, not only on save.

## Shipped data

The game's folder holds the archive `FFXII_TZA.vbf`, the `FileSizeTables` folder and `ConfigData` (with
`keymap.ini` and the Gaussian filter settings) one level above `x64`. The `x64` folder holds these files:

| File | What it is | Loaded by |
|---|---|---|
| `FFXII_TZA.exe` | the game, 64-bit | Steam |
| `FFXII_TZA_GameSetting.exe` | the settings launcher, 32-bit .NET | the player or Steam |
| `SettingsLoc.xml` | the launcher's texts in nine languages | the launcher |
| `SharpDX.dll`, `SharpDX.DXGI.dll`, `SharpDX.DirectInput.dll` | .NET wrappers of DXGI and DirectInput, 32-bit | the launcher (display list, gamepad) |
| `Steamworks.NET.dll` | a .NET wrapper of the Steam API, 32-bit; it calls `CSteamworks` | the launcher |
| `CSteamworks.dll` | a 32-bit native bridge that imports `steam_api.dll` | `Steamworks.NET.dll` |
| `steam_api.dll` | the 32-bit Steam API | `CSteamworks.dll` |
| `steam_api64.dll` | the 64-bit Steam API, nine imports | the game |
| `d3dcompiler_47.dll` | the Direct3D shader compiler library | the game, for one import, `D3DReflect` (`007911D0`) |
| `xinput1_3.dll` | the XInput 1.3 controller library | the game's XInput controller, which loads `.\xinput1_3.dll` from the working folder when an XInput pad is built and keeps only its ordinal-100 export (`00862C70`; [Controllers](../Controls-And-Input/controllers.md)); the game's own `XInputGetState` and `XInputSetState` come from the system's `XINPUT9_1_0.dll` |

The game imports nothing else from `d3dcompiler_47.dll`: its one caller, `0078AD20` in the post-effect library's
`TinyEffect` code, reflects already compiled shader bytecode to list its constant buffers and resources
([Yebis post effects](../Third-Party-Libraries/yebis-ppfx-post-effects.md)). No shader is compiled at run
time. The shipped install has no `steam_appid.txt`.

## Modding notes

- The launcher only edits `GameSetting.ini`; editing the file by hand does the same, and the game reads it on the
  next start.
- `Quality` Low, Medium and High overwrite the ten preset settings on every game start whatever the file says
  for them ([Game settings](game-settings.md)); the launcher has no box for those ten.
- Deleting `keymap.ini` by hand has the same effect as the Reset button.

## Related

- [Game settings: the GameSetting.ini object and its options, the ini file's load and save, the quality presets, FrameLimit, DecideButton, the Config screen's commands, Active and Wait battle mode and the FF12CONFIG file](game-settings.md)
- [Languages: the Language setting, the nine language codes, the locale id each maps to, the data folder it selects, the Windows-locale default, and the confirm and cancel buttons](languages.md)
- [Keymap file: keymap.ini, the control config file, when it is read and written, its names in slot order, and the shipped defaults](../Controls-And-Input/keymap-file.md)
- [Steam integration: how the game starts and pumps Steam, the interfaces and callbacks it uses, and what it does without Steam](../Steam-And-Achievements/steam-integration.md)
- [Controllers: how a gamepad is found, the three kinds of controller the game builds, plugging one in during play, and the Steam Input action names](../Controls-And-Input/controllers.md)
- [YEBIS and PPFX: the post-effect library, how the game starts and drives it, its licence check and the EnableYebis switch](../Third-Party-Libraries/yebis-ppfx-post-effects.md)
