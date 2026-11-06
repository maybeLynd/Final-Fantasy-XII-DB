---
title: "Settings launcher: FFXII_TZA_GameSetting.exe, the options it writes to GameSetting.ini, the display list it builds, its reset button, and every other file the game ships beside the executable"
kind: "system"
category: "Saving, loading and settings"
addresses: "0x001DE050, 0x001F3ED0, 0x0079813C, 0x0078AD20, 0x007911D0, 0x00862C70"
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
([Game settings](game-settings.md), `0x001DE050`). The method names below are those of its own metadata.

### Where the files live

`Program.InitGlobalConfig` reads the file names from the embedded resource `PathConfig`: `IniFile` is
`GameSetting.ini` and `ResetFile` is `keymap.ini`. It places both in `Documents\My Games\FINAL FANTASY XII THE
ZODIAC AGE\`, followed by the Steam account id when `SteamAPI.Init` succeeds, and creates the folder with
`SHCreateDirectory`. That is the folder the game uses for the same files (`0x001F3ED0`;
[Keymap file](../Controls-And-Input/keymap-file.md)).

Before it goes on, `SteamAPI.RestartAppIfNecessary(595520)` decides whether the program must be restarted
through Steam; on true the launcher exits at once. The game makes the same check with the same app id
(`0x0079813C`; [Steam integration](../Steam-And-Achievements/steam-integration.md)).

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

Each of the nine `Lang` elements of the shipped file (`jp`, `en`, `cn`, `ch`, `fr`, `de`, `it`, `es` and `kr`) has
the same 32 entries; [`settings-launcher-settingsloc-strings.tsv`](settings-launcher-settingsloc-strings.tsv) lists
all 288 with their text and what each one sets. Only the launcher reads the file: the game's executable does not
contain its name.

- `ConfigTitle` is the window title, and `Font` is the font of every control, of the adapter list's width measure
  and of the message boxes. Each `Text[@Control]` sets the text of the control it names, matched without regard to
  case, so `button_reset` labels `button_Reset`. Each `Text[@Key]` sets the text of one box item; the item still
  writes its own key to `GameSetting.ini`.
- `msg_Caption` and `msg_Content` are the box a second copy of the launcher shows before it exits;
  `msg_WarningCaption` and `msg_WarningContent` are the Reset question; `msg_ErrorDiskFull` is the disk-full text,
  under the `msg_Caption` title. The boxes' OK and Cancel buttons take the `button_ok` and `button_cancel` texts
  (`MsgForm.OnPaint`).
- `LanguageName` is never read: the name does not occur in the launcher's binary, and
  `SetLanguageComboBox(XmlDocument)` has an empty body and no caller.
- The shipped file marks no `Lang` element `small`, so a screen under 720 pixels high gets the same texts.
- The launcher opens the file by its bare name, in its working folder. A missing file, or a language code with no
  `Lang`, leaves the texts built into the window: English labels, the title FINAL FANTASY X/X-2 Launcher, and
  message boxes without text.
- `LoadXmlFile` drops everything before the first CRLF, so the XML declaration must stay on its own line, and a
  file with no CRLF stops the launcher with an exception before its window opens.
- A `Text[@Control]` naming no control, a `Key` given twice in one language, or a `Lang` without `ConfigTitle` or
  `Font` raises an exception while the window loads. A `Key` the launcher does not use is ignored, and a font that
  Windows lacks is replaced by Microsoft Sans Serif.

### Columns of settings-launcher-settingsloc-strings.tsv

| Column | Holds |
|---|---|
| `selector` | the attribute of a `Text` element that says what it labels: `Control=` and a control name on 12 elements per language (108 rows), `Key=` and a box item key on 12 per language (108 rows); empty on the 8 other elements of each language (72 rows) |
| `read_by` | the launcher method that reads the entry and how it uses it: `ConfigForm_Load (Controls[name].Text)` for control texts, `ConfigForm_Load (ComboboxItem.Value)` for item texts, `MsgForm.OnPaint` for the message boxes, both where one text serves both; `nothing` on the 9 `LanguageName` rows |
| `what_it_sets` | what the text sets in the launcher: the window title, the font, a control's text, a box item's text with the item's design-time text, or a message box's title or text; on the `LanguageName` rows, that it has no effect |

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

That holds when the read succeeds. A key given twice makes the read throw (`Dictionary.Add`); the launcher then
starts with no keys, every box takes its default, and a save writes only its own keys and `Language`. Lines
without `=` are skipped.

- Values it cannot use: a `ScreenMode` outside the three selects full-screen, a `FrameLimit` other than `60`
  selects 30 FPS, and a `VSync` other than `Off` and `Adaptive` selects on. A `Quality` outside the four keys
  becomes an extra item with the text Custom, which writes the same value back.
- A missing `WindowSize` selects the first size and a missing `Resolution` the last. A `WindowSize` not in the list
  is raised to at least 640 x 360 and added to it in size order; a `Resolution` not in the list selects the listed
  size nearest in pixel count.
- These raise an exception the launcher does not catch: a `MasterVolume` that is not a number (`int.Parse` while
  the window loads), a `WindowSize` without `*` in windowed mode, a `LastX` or `LastY` that is not a number in
  borderless mode, an adapter field or `FrameLimit` outside the 32-bit range, and a `Monitor` of 0 or less on the
  stored adapter.
- [`settings-launcher-instances-rows.tsv`](settings-launcher-instances-rows.tsv) lists every key the launcher
  reads or writes, its 24 controls, 12 box items, eight gamepad bits, the files it opens, the 12 `PathConfig`
  elements and the 22 members it never uses or never assigns, each with the method that uses it and where its text
  sits in the binary.
- [The launcher inputs](settings-launcher-program-inputs.tsv) table gives each of those 103 rows as an input: its
  values, what wins when two sources set it, when it takes effect in the launcher and in the game, what reads it, what
  the player sees and when it changes nothing.

In borderless mode the resolution box shows the size of the screen that holds the point
`LastX`, `LastY` from the file. When no screen holds it, it takes the screen whose bottom-right corner is nearest,
measured with `LastX` for both coordinates, and with no screen at all it falls back to `Resolution` or the primary
screen's size (`ConfigForm.UpdateResolutionComboBoxItems`).

A full disk (HRESULT `0x80070027` or `0x80070070`) shows the `msg_ErrorDiskFull` text; any other write error
shows the exception's message.

### Columns of settings-launcher-instances-rows.tsv and settings-launcher-program-inputs.tsv

Both tables have the same 103 rows in the same order (the `kind` column of the first): 2 shipped files, 16
`GameSetting.ini` keys, 24 controls, 12 box items, 8 gamepad inputs, 7 files and mutexes, 12 `PathConfig` elements
and 22 unused members.

| Column | Holds |
|---|---|
| `detail` | in settings-launcher-instances-rows.tsv, by kind: the file's size; the default the launcher's code gives the key (`""`, `"us"` ...; `-` on `Mute` and `Volume`); the control's type; the item's built-in text; the gamepad mask bit; the .NET calls that open the file; the element's text; what the unused member is |
| `value_or_text` | by kind: the file's SHA-256; the values the launcher writes to the key, or that it never writes it; the control's built-in text, `-` on the 11 controls without one; the setting the item writes (`ScreenMode=SM_WINDOW`); `-` for gamepad inputs and unused members; what is done with the file (`read`, `read and written`, `deleted`, `read, result discarded`, `named mutex`); `embedded resource PathConfig`, where the element comes from |
| `read_or_created_by` | the methods that read the key, input, file or element, or the form that creates the control (`ConfigForm`, `MsgForm`, `ConfigWindow`); for an unused member, the source file and line of its declaration in the decompiled launcher (`Program` alone for the two static fields); `-` for the shipped files; on 10 `PathConfig` elements and `Mute` the cell says no code reads it |
| `written_or_handled_by` | the methods that write the key, or the control's event and handler (`Click: button_OK_Click`); `ConfigForm.SaveConfiguration` for the items and `ConfigForm.timer1_Tick` for the gamepad inputs; `-` for the shipped files, files and `PathConfig` elements; on the 22 unused members, 15 controls and the keys `LastX`, `LastY` and `Volume` the cell says no code writes or handles it |
| `string_in_binary` | `yes` on the 71 rows whose name's text is in the launcher's binary, with the text in parentheses where the row names a variable (`Program.ConfigPath`, `Program.ResetFilePath`, the mutex name); `-` on the 2 shipped files, 8 gamepad inputs and 22 unused members |
| `domain` | in settings-launcher-program-inputs.tsv, by kind: the file's size and SHA-256; the key's values (the text of `value_or_text`); the control's type, the file's .NET calls and what the member is (the text of `detail`); `the item text` and the item's built-in text; `pressed or not` with the mask bit; `text; shipped` and the element's text |
| `precedence` | what wins when two sources set the input: for 11 keys the launcher's box at OK or Apply; for `LastX`, `LastY` and `Volume` the file's value, which the launcher never writes; for `MasterVolume` the file's value, written back; for `Mute` the `Off` the launcher writes at every save; for the 12 items a `SettingsLoc.xml` `Text[@Key]` over the built-in text; for the 8 gamepad inputs the OR of every attached controller; `-` on the other 67 rows |
| `consumers` | what reads the input: for the 16 keys, `the launcher:` and its methods, then `the game:` and the game's setting or the note that the game's 31-key table lacks the key; for the shipped files, the launcher or the player; for controls, their event handler or the message box; for items, `ConfigForm.ConfigForm_Load` and `ConfigForm.SaveConfiguration`; for gamepad inputs, `Joy.handleInput` and `ConfigForm.timer1_Tick`; for files, the .NET calls; on the 22 unused members, 11 controls and 10 `PathConfig` elements the cell says nothing reads it |
| `visible_effect` | what the player sees in the launcher or the game, with the fallback for a value the launcher cannot use; `read by nothing` on the 10 `PathConfig` elements whose text is `Hello.exe` or empty, and nothing on the 22 unused members |
| `inert_when` | when the input changes nothing: `always` and the reason on 48 rows (20 members declared and never used, 2 fields never assigned, 10 labels and a panel, 10 `PathConfig` elements read by nothing, 3 gamepad bits nothing reads, `Mute` and `Volume`); `MasterVolume` in the game only; `code_steam.txt` and `data.txt` while the file is absent; the `VQ_CUSTOM` item, listed only when `GameSetting.ini` says `VQ_CUSTOM` or another `Quality` value; `-` on the other 51 rows |

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
- The mask holds the hat as left `0x1`, right `0x2`, up `0x4` and down `0x8` (angles 27000, 9000, 0 and 18000) and
  the first four buttons as `0x10`, `0x20`, `0x40` and `0x80` (`Joy.handleInput`). Button one is `0x20`, the
  controller's second button; nothing reads `0x10`, `0x40` or `0x80`.

### Leftovers in the program

- `PathConfig` also names `Hello.exe` for `FFX`, `FFX2` and `SideStory`, which nothing in this program reads, and
  the window's design-time title is "FINAL FANTASY X/X-2 Launcher", replaced by `ConfigTitle` when it loads.
- `ConfigForm.SetVersionInfo` reads `./code_steam.txt` and `./data.txt` and then sets the version label to the
  constant "Ver  1.0.4.0", the assembly version.
- The Custom quality item is removed from its box unless the file already says `VQ_CUSTOM` (`ConfigForm_Load`), and
  the frame-limit and VSync boxes write their key on every change, not only on save.
- `PathConfig` has twelve elements: besides `IniFile` and `ResetFile`, `FFX`, `FFX2`, `SideStory`, `LastMission`
  and `Credit` each name `Hello.exe`, and their five `Param` elements are empty. Only `IniFile` and `ResetFile` are
  read.
- The VSync box's designer name is `comboBox_FrameLimit`, the frame-limit box's name. A `Text[@Control]` naming
  `comboBox_FrameLimit` labels the frame-limit box, which is added first, and one naming `comboBox_Vsync` names no
  control.
- The resolution box's 26 design-time sizes (2560 x 1440 twice) and the version label's design text
  `Ver  1.0.0.1` never show: the screen-mode selection refills the box, and `SetVersionInfo` sets the label.
- `SetVersionInfo` cuts the first line of `code_steam.txt` and of `data.txt` between its first space and its first
  `on`, discards the result, and throws in the window's constructor when the cut's length is negative, as for a
  line without `on`; neither file ships.
- Declared and never used: the methods `LoadVBFImage`, `RetriveMonitorResolutions`, `Pause`, `ToSBC`, `ToDBC`,
  `GetXmlSelectorNodeByLanguage` and `stopTimer`, the import `AllocConsole`, and the properties `LanguagePath`,
  `LangAndSizePath`, `MainFormHandle`, `FocusMessage`, `MaxScreenWidth`, `MaxScreenHeight`, `ResetButton`,
  `DefaultButton`, `ApplyButton` and `VersionNumber`.
- `OnVolumeChanged` and `mSharedMemoryObject` are never assigned, so the `Volume` key test in `SetIniString` calls
  nothing and `MainFormHandle` never maps its shared memory.

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
| `d3dcompiler_47.dll` | the Direct3D shader compiler library | the game, for one import, `D3DReflect` (`0x007911D0`) |
| `xinput1_3.dll` | the XInput 1.3 controller library | the game's XInput controller, which loads `.\xinput1_3.dll` from the working folder when an XInput pad is built and keeps only its ordinal-100 export (`0x00862C70`; [Controllers](../Controls-And-Input/controllers.md)); the game's own `XInputGetState` and `XInputSetState` come from the system's `XINPUT9_1_0.dll` |

The game imports nothing else from `d3dcompiler_47.dll`: its one caller, `0x0078AD20` in the post-effect library's
`TinyEffect` code, reflects already compiled shader bytecode to list its constant buffers and resources
([Yebis post effects](../Third-Party-Libraries/yebis-ppfx-post-effects.md)). No shader is compiled at run
time. The shipped install has no `steam_appid.txt`.

The `keymap.ini` in `ConfigData` is not the control file, and changing or deleting it changes nothing: no shipped
program opens it. The controls the game uses are in the `keymap.ini` of the Documents folder, in another format
([Keymap file](../Controls-And-Input/keymap-file.md)). The shipped file is 38 lines of text in five sections;
[`settings-launcher-keymap-rows.tsv`](settings-launcher-keymap-rows.tsv) lists every line.

- Read in the game's control codes ([Control names](../Controls-And-Input/control-names.md)), `[Button]` key1-key16,
  `[Analog]` key1-key8 and `[KeyFunction]` key1-key3 are the game's built-in profile 1, slots 0-26 in order, with one
  difference: `[Button]` key10, R2, is 118 (Left Shift) where the game's default is 117 (Left Control). No line holds
  WalkMode, slot 27.
- `[Setting]` gives the length of each of those lists (16, 8 and 3). `[Mouse]` gives Left 14, Middle 3 and Right
  15, which in the game's numbering are Triangle, the third mouse-button code and L1.
- The text `ConfigData` occurs in no file of `x64`, the game, the launcher and the DLLs alike, and the archive has
  no keymap entry. The game builds its one `keymap.ini` path from the Documents folder (`0x00197EE0`), and
  the launcher's Reset deletes the file of that name in the same folder (`Program.InitGlobalConfig`).
- Put in the Documents folder in place of the game's file, it is not used: its first line, `[Setting]`, is neither
  a `[KeyboardN]` header nor a binding, so the read stops there with profile 1 empty. The game then installs its
  default controls and writes them over the file when it shuts down.

`ConfigData\GaussianFilter\GaussianFilterSetting.ini` (619 bytes, CRLF) holds a `[Setting]` section with `Count=5`
and the sections `[Custom1]` to `[Custom5]`. Each gives a band of screen sizes by `StartWidth`, `EndWidth`,
`StartHeight` and `EndHeight`, and a `BigKernel`, `Factor` and `BlendAmount` for it: 15x15 up to 800 x 600, 7x7 up
to 1280 x 720, 5x5 up to 1600 x 900, 3x3 up to 1920 x 1080 and 3x3 from there to 32767 x 2160. `Factor` is 0.91
and `BlendAmount` 0.5 in all five.

- No shipped program opens it: no `.exe` or `.dll` in `x64` holds the text `GaussianFilterSetting`, `ConfigData`,
  `[Setting`, `BigKernel=`, `StartWidth=` or any other of its keys with its `=`, ASCII or UTF-16, in any case.
- The game sets the three values itself. The developer console labels render-parameter fields `+0x19C` "Gaussian
  Filter big kernel" (0 3x3, 1 5x5, 2 7x7, 3 15x15), `+0x1A0` "Gaussian Filter factor" and `+0x1A4` "Gaussian
  Filter blend amount" (`0x001CDFF0`, `0x001D0787`).
- In play they are 3x3, the screen height divided by 1080.0 and 0.5, `+0x0C = h > 0 ? h / 1080.0 : 1.0` with h
  the screen height (`0x002256A0`, `0x001DC3EB`-`0x001DC415`): the constructor `0x0018CD90` stores 0 and 0.5,
  and the copiers take `+0x08`, `+0x0C` and `+0x10` of the object `0x001DC510` returns, which `0x001DC3D0` sets to 0,
  height / 1080.0 and 0.5 ([YEBIS and PPFX](../Third-Party-Libraries/yebis-ppfx-post-effects.md)).
- Editing the file therefore changes nothing. At 1920 x 1080 the game's factor is 1.0, where the file says 0.91.
- [`settings-launcher-gaussianfiltersetting-rows.tsv`](settings-launcher-gaussianfiltersetting-rows.tsv) lists its
  42 lines with their offsets, the game's value for each key and where the key's text occurs in the shipped
  programs.

[The settings inputs](settings-launcher-inputs.tsv) table gives every key line of the two `ConfigData` files as a
setting: 33 in `keymap.ini` and 36 in `GaussianFilterSetting.ini`. Each one's values, when it takes effect, what reads
it and what the player sees are given there, and no setting takes effect, because no shipped program opens either file.

### Columns of the keymap, Gaussian filter and settings inputs tables

| Column | Holds |
|---|---|
| `value_in_game_code_numbering` | in settings-launcher-keymap-rows.tsv, the line's value read as the game's control code, with its name and device ([Control names](../Controls-And-Input/control-names.md)), for example `40, Key_M (keyboard)`, on the 30 key lines; on the 3 `[Setting]` lines the count and the section it counts; `section header` on the 5 header lines |
| `game_profile1_counterpart` | the slot of the game's built-in profile 1 the line stands for, as `slot N name (group g entry e)`, on the 27 lines of `[Button]`, `[Analog]` and `[KeyFunction]`; `no counterpart` and the reason on the 3 `[Mouse]` lines; empty on the 5 headers and the 3 `[Setting]` lines |
| `comparison` | the value against the game's default for that slot: `same as the game default` on 26 lines and `differs: the game default is 117 Left Control` on `[Button]` key10; on the `[Setting]` lines, that the count matches its section; empty on the 5 headers and the 3 `[Mouse]` lines |
| `read_by` | the same on all 38 lines: neither the game nor the launcher opens the file |
| `offset` | in settings-launcher-gaussianfiltersetting-rows.tsv, where the line starts in the file, in hex bytes (`0x000` to `0x25A`): each line starts at the previous one plus its length and CR LF, and the last ends at byte 619, the file's size; `-` on the `file` row |
| `game_side` | on the 15 `BigKernel`, `Factor` and `BlendAmount` lines, the render parameter the game uses for that key and its value in play; `-` on the other 28 rows |
| `text_in_x64_programs` | which `.exe` or `.dll` in `x64` holds the key's text: on all 42 lines the cell says that no program does, and on the `file` row it says the same for the file name and for `ConfigData` |
| `domain` | in settings-launcher-inputs.tsv, `any text; shipped` and the shipped value, on all 69 rows |
| `precedence` | `-` on all 69 rows |
| `consumers` | what reads the line: on the 33 `keymap.ini` lines, the note that neither `FFXII_TZA.exe` nor `FFXII_TZA_GameSetting.exe` opens the file; on the 36 Gaussian filter lines, the note that no `.exe` or `.dll` in `x64` holds the text `GaussianFilterSetting` or `ConfigData` |
| `visible_effect` | what the player sees, nothing on all 69 rows: on the 33 `keymap.ini` lines the cell names the Documents folder's `keymap.ini` as the file the game uses, and on the 15 `BigKernel`, `Factor` and `BlendAmount` lines it gives the value the game uses instead |
| `inert_when` | `always` on all 69 rows, with the file that no shipped program opens |

## Modding notes

- The launcher only edits `GameSetting.ini`; editing the file by hand does the same, and the game reads it on the
  next start.
- `Quality` Low, Medium and High overwrite the ten preset settings on every game start whatever the file says
  for them ([Game settings](game-settings.md)); the launcher has no box for those ten.
- Deleting `keymap.ini` by hand has the same effect as the Reset button.
- Neither the game nor the launcher opens `ConfigData\keymap.ini`; the controls are in the Documents folder's
  `keymap.ini`.

## Related

- [Game settings: the GameSetting.ini object and its options, the ini file's load and save, the quality presets, FrameLimit, DecideButton, the Config screen's commands, Active and Wait battle mode and the FF12CONFIG file](game-settings.md)
- [Languages: the Language setting, the nine language codes, the locale id each maps to, the data folder it selects, the Windows-locale default, and the confirm and cancel buttons](languages.md)
- [Keymap file: keymap.ini, the control config file, when it is read and written, its names in slot order, and the shipped defaults](../Controls-And-Input/keymap-file.md)
- [Steam integration: how the game starts and pumps Steam, the interfaces and callbacks it uses, and what it does without Steam](../Steam-And-Achievements/steam-integration.md)
- [Controllers: how a gamepad is found, the three kinds of controller the game builds, plugging one in during play, and the Steam Input action names](../Controls-And-Input/controllers.md)
- [YEBIS and PPFX: the post-effect library, how the game starts and drives it, its licence check and the EnableYebis switch](../Third-Party-Libraries/yebis-ppfx-post-effects.md)

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Audio: `0x001DC3D0` calls `0x002256A0`; `0x001DC510` calls `0x001DC3D0`; `0x002256A0` is called by `0x00182E80`, `0x001DC3D0`,
  `0x00221940`, `0x00221C70`, `0x00221E60`, `0x002238F0`, `0x00223F40`, `0x00223FA0`, `0x002240B0`, `0x00224180`, `0x00224290`,
  `0x00224360`; `0x002256A0` is also called by `0x00224470`, `0x00224A30`.
- Audio: those functions are documented on
  [screen mode and aspect](../Graphics/screen-mode-and-aspect.md),
  [yebis ppfx post effects](../Third-Party-Libraries/yebis-ppfx-post-effects.md),
  [game application](../Engine-Core/game-application.md), [spatial sound](../Sound-And-Music/spatial-sound.md);
  and on [audio manager](../Sound-And-Music/audio-manager.md).
- Presentation: `0x001DC510` is called by `0x00193AD0`.
- UI: `0x0018CD90` is called by `0x0018EEE0`; those functions are documented on
  [graphics settings](../Engine-Core/graphics-settings.md).
