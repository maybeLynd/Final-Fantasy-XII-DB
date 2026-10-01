---
system: UI layout parameters and the editor schema
category: 16-UI
status: AUDITED
owner_layer: PrimaryOwner:UI
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation delta - every function this document cites whose record differs between the stamped snapshot and GN161's gained a plate comment and tags ONLY (empty comment before, tag set a subset, checked field by field), and this document makes no uncorrected absence claim about any of them; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 12 cited address(es) among the 128 records changed across GN158..GN161; each differs only in comment and tags; 0 live absence claims (check_stranded_absence.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-DELTA-RELIANCE-BASIS; re-measured and applied for this document 2026-09-14 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708, on SNAPSHOT-IDENTITY - replaced rather than re-targeted because that basis is FALSE for this document, which cites a record that changed
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  vbf: FFXII_TZA.vbf (31,196,932,183 bytes)
last_reviewed: 2026-09-13
audit:
  passes: 1
  last_pass: 2026-09-02
  last_pass_state: falsification-pass
  crossref_clean: false
  reopened_count: 0
---

# UI layout parameters and the editor schema

> **Every measurement in FFXII's menus is a number in a data file — 231 of them.** And the
> developers shipped the definition of their own tuning tool alongside it, complete with slider
> ranges.

## 1. What the player sees

The position of the Gambit column. How tall a row in the command list is. Where the cursor sits
relative to the thing it points at. The height of the boss gauge. The offset of the pause menu.

None of it is baked into the code. All 231 measurements live in a file that ships with the game,
and there is a second file describing how each one was meant to be adjusted — minimum, maximum,
and how many decimal places — because someone at Square Enix had a tool with sliders for exactly
these values.

There are even **two complete layouts**: a normal one and a standard-definition one, so the menus
reflow for low resolutions.

## 2. Native mechanism

### The files

All inside `FFXII_TZA.vbf`:

| Path | Size | Content |
|---|---:|---|
| `jsondata/uisize/uisize.json` | 7,478 B | **231 layout parameters** |
| `jsondata/uisize/uisize_sd.json` | 4,609 B | standard-definition variant |
| `jsondata/parametersmanageruisizestruct.csv` | 10,350 B | **the editor schema, 266 rows** |
| `jsondata/parametersmanagermonstergallerystruct.txt` | 1,781 B | schema for the monster gallery |
| `jsondata/monstergallery.json` | 337,640 B | monster gallery data |
| `jsondata/monstertoweapon.json` | 50,445 B | monster-to-weapon mapping |

The loader is `001CA600` (8,186 bytes), the function that references `mGambitPositionOffsetX`.
`JsonBox` is the linked parser.

### The parameters

231 keys — 151 floats and 80 integers. Real values:

```json
{
  "mScrollListHeight": 46.0,
  "mCommandTitleFontHeight": 46.0,
  "mGeneralFrameFrontOffset": 28.0,
  "mGeneralFrameBackOffset": 10.0,
  "mBtlCommandScrollTableOffsetX": 18,
  "mBtlCommandScrollTableOffsetY": 0,
  "mGambitPositionOffsetX": -82.0,
  "mGambitPositionOffsetY": 28.0
}
```

### The editor schema — the developers' own tuning tool, shipped

`parametersmanageruisizestruct.csv` has this header:

```
#title name,toolbox,DecimalPlaces,"	min","	max",disable
```

266 rows: **229 `trackbar` widgets and 36 `label` section headers.**

```
BattleCommandNormal,label,,,,
mScrollListHeight,trackbar,0,0,100,
mCommandTitleFontHeight,trackbar,0,0,100,
mGeneralFrameFrontOffset,trackbar,0,-100,100,
BattleCommandScrollTableOffsetX,trackbar,0,-100,100,
```

Each row gives a parameter its **widget type, decimal precision, and slider min/max**. This is a
GUI definition — an internal parameter-manager application drove FFXII's menu layout with sliders,
and its configuration shipped in the retail archive.

The 36 section labels name the UI surfaces:

```
BattleCommandNormal   MessageWindow   BattleCommandNumber   BattleCommandMist
BattleInfo            PartyCommand    Gambit                BattleNum
Cursor                TriangleMenu(This Count change to Set Pixel)
TriangleMenuStatus    PauseMenu       BlackBand             WorldMap
NgSignal              BossGauge       ... (36 total)
```

`TriangleMenu(This Count change to Set Pixel)` is a developer note left in the label text.
`NgSignal` and `BlackBand` are internal names for UI elements.

### Schema and data do not line up exactly

The schema names **229** trackbars; the data file holds **231** keys. They are also not
name-identical — the schema contains `BattleCommandScrollTableOffsetX` and
`BattleCommandScrollBarWidth` (no `m` prefix) while the data uses `mBtlCommandScrollTableOffsetX`.

So the CSV is **not** a strict schema for the JSON; it is a tool definition that has drifted from
the data it edits. Recorded as **Y-2** rather than smoothed over.

### Which code reads each key — 2026-09-13 (FABLE)

**Every key lands in a fixed global, so the readers of that global are the code the key positions.** `001CA600` reads
a key by name (`lea rdx, key` … `call 00200B80`). It stores the value through the pointer at UI object `+0x3B00 + slot`:
`rbx = 001B1C00() + 0x3B00` (`001CA63F`), then `mov rcx, [rbx + slot]` and `mov [rcx], eax`. `001AF470` fills those
pointers with the addresses of fixed globals (`lea rax, global` / `mov [rcx + 0x3B00 + slot], rax`; e.g. `001AF710`–`001AF717`
for `WorldMapWidth` → `01F2CAA4`). Joining the two gives **key → global for ~~222~~ 226 keys**, with none unresolved
([`members/layout-key-slots.tsv`](members/layout-key-slots.tsv), from [`members/layout_key_slots.py`](members/layout_key_slots.py)).
*Corrected 2026-09-27 (FABLE, Claude Opus 5.5) — the 09-13 join lost four keys and misbound one.* Two defects in my
script: capstone prints a small displacement in decimal, so `mov rcx, [rbx + 8]` (`001CA673`) did not match and
`mCommandTitleFontHeight` (→ `01E0C374`) was dropped; and at `001CC572` `rbx` becomes a **second** object, `001B5FB0()`'s
singleton at `01F81200`, for the three `Variant_ReadFloat` keys. Their slots are filled by `001B44A0` (tail-jumped from
`0017F9E0`, `001B4551`–`001B4574`): `FontItalicVal` → `01E0CF90`, `FontItalicScale` → `01E0CF94`, `FontShadowAlphaMuti` →
`01DF6DE0`. The script keyed slots by offset alone, so `FontItalicVal`'s `[rbx + 0x2f8]` overwrote `MessageWinMaskBottom`'s
slot `+0x2F8` (`001CB2CD`): **`01E0CDA8` is `MessageWinMaskBottom`, not `FontItalicVal`**, and the other two float keys were
lost. The corrected join binds all **226** distinct keys the loader reads (223 int through `+0x3B00`, 3 float through the
second object), so the **Y-6** gap below is the join's own. `001AF470` installs **227** pointers: the 223 int keys' slots,
plus four (`+0x1A0`–`+0x1B8` → `01F2CA94`–`01F2CAA0`) that no loader key uses and that have no reader of any kind (their
only rip references are `001AF470`'s own `lea`s; none image-base-relative). Four is the count of the `NA_HintMessage`
trackbars dead in code (Y-2); that they are those four is an inference. Consumers: [consumer check](../../_index/candidates/y1-layout-key-uses/consumer-check.md).
One pass over every listed function then collects the rip-relative operands that hit those globals
([`members/layout-key-readers.tsv`](members/layout-key-readers.tsv), from [`members/layout_key_readers.py`](members/layout_key_readers.py)):

| | count |
|---|---:|
| keys bound by the pattern | ~~**222**~~ **226** (corrected 2026-09-27) |
| keys whose global has a rip-relative reader | ~~**210**~~ **213** |
| distinct reader functions | ~~**124**~~ **125** (adds `003EED60`) |
| … of them on the frontier | **117** (as of 2026-09-13; not recounted) |
| … of them widget procedures in the [handler census](../Widget-Object-Model/widget-message-handlers.tsv) | **41** |

**Control.** The map keys reproduce the readers found independently for the map screens: `TrackMap*` → `002B7B80` /
`002B8EE0`, `LocaMap*` → `002BA700` / `002BCB00`, `WorldMap*` → `00552250` / `005528C0` / `00550A00`
([map screens](../Map-Screens/the-map-screens-and-their-shared-map-data.md) §2.1).

**No rip-relative reader: ~~12~~ 13 keys.** They are `BattleLogBlackBandH`, `LicenseBlackBandH`, and the ten `mCursor{Up,Down,Left,Right,Open}{X,Y}`;
*2026-09-27:* and `FontShadowAlphaMuti` (`01DF6DE0`), found by the corrected join.
A reader through a base pointer plus offset would not show here, so these are not claimed unused. *2026-09-27:* Y-1 checks
those routes too (image-base-relative operands and loads of the slot pointers) and finds none for all 13.

**What a row means, and what it does not.** A reader of `LicenseBoard…` keys positions part of the license board. That
names its screen, not its role. The families come from the key names' leading words (`m` prefix dropped). Rows
like `PartyBlack…` / `BlackBand…` are fade bands shared by many screens, and `FontBase…` is shared text metrics.

| key family | keys read | reader functions (`P` = a widget procedure in the handler census) |
|---|---:|---|
| `HpGauge…` | 24 | `002C5F90` |
| `MsgWin…` | 13 | `002A4170`, `002A4430`, `002A6190` P, `002A7F70`, `002A8100`, `002A8220`, `002A86A0` P |
| `BattleCommand…` | 10 | `00273E30`, `0027CE70`, `0027DED0`, `00298250` P |
| `GambitTutorial…` | 10 | `00568460`, `005685B0` |
| `WorldMap…` | 9 | `0027EF50`, `002804E0`, `00550A00`, `00552250` P, `005528C0` P, `00553CB0`, `005552A0`, `00555A70`, `00555F80`, `00563430` |
| `LicenseBoard…` | 6 | `005565E0` P, `005569F0` P, `005588C0`, `0055A340` P |
| `MenuList…` | 6 | `002C9BF0`, `002CD170` P |
| `TrackMap…` | 6 | `002B7B80` P, `002B8EE0` |
| `BattleMist…` | 5 | `0027CE70` |
| `NumEffect…` | 5 | `0028AAA0`, `0028B140` |
| `BossGauge…` | 4 | `0029E840` |
| `NobuMsg…` | 4 | `002A70B0` |
| `OverHead…` | 4 | `002C7F90`, `002C84E0` |
| `StatusAlone…` | 4 | `002C1CC0`, `002C1D30`, `002C1E20` P |
| `ActionList…` | 3 | `002C4720` |
| `ActiveLog…` | 3 | `002BDCE0`, `002BE4F0` P, `002BF230` |
| `NobuMessage…` | 3 | `002A4170`, `002A5590`, `002AC5F0`, `002AE610`, `002AF340`, `002B2DF0` |
| `PauseMenu…` | 3 | `00228A70` |
| `AutoWindow…` | 2 | `002D66D0` P |
| `CommandMenu…` | 2 | `00281AE0`, `002C2320` P, `00565E00`, `0056F5F0`, `0057B400` |
| `ConfirmCaption…` | 2 | `00241D40` P, `0057C480` P |
| `ConfirmCursor…` | 2 | `00241D40` P |
| `ConfirmWindow…` | 2 | `00241D40` P, `0057C140`, `0057C480` P |
| `ExpLp…` | 2 | `0028B140` |
| `ExtraLoca…` | 2 | `002BCB00` |
| `ExtraTrack…` | 2 | `002B8EE0` |
| `FontBase…` | 2 | `00241D40` P, `002A2C00`, `002A4430`, `002A70B0`, `002A86A0` P, `002AC5F0`, `002AF960`, `002B24B0`, `002B2C50`, `002B2DF0`, `002BDCE0`, `002BE4F0` P, `002D4930`, `0035E070` P, `0039BB60`, `0039BF50`, `0057C140`, `0057C480` P |
| `GambitIcon…` | 2 | `00566C10` P |
| `GambitPosition…` | 2 | `00276BE0` |
| `General…` | 2 | `00247590`, `00247680` |
| `GeneralFrame…` | 2 | `002475D0` |
| `HelpMessage…` | 2 | `0028FCB0`, `002BF690` P |
| `ItemSort…` | 2 | `00566680` P |
| `ListItem…` | 2 | `00292390` P |
| `MapName…` | 2 | `00553AE0` P |
| `MessageLine…` | 2 | `002A2C00`, `002A4430`, `002A70B0`, `002AC5F0`, `002AF340`, `002B0280` |
| `Na…` | 2 | `002BA700` P, `002D5EB0` P, `0055E9E0`, `005789D0` P |
| `NgSignal…` | 2 | `0029E110` |
| `PartyBlack…` | 2 | `0027EE80`, `0027EF00`, `0027F540`, `002804E0`, `00280D20`, `002814E0`, `00281ED0`, `002BA700` P, `002C2320` P, `002D7070`, `003F3E40`, `00565E00`, `005679D0`, `0056DD50`, `00572E10` P, `00574E80` P, `0057B800` |
| `RegionText…` | 2 | `00553AE0` P |
| `ScrollMark…` | 2 | `002CEB40`, `002D1750` |
| `SilhouettePos…` | 2 | `002CF440` P |
| `SystemWindow…` | 2 | `002A4170` |
| `TalkingMessage…` | 2 | `002A2C00` |
| `2DSideCursorCenterX…` | 1 | `0028D460` |
| `2DSideCursorCenterY…` | 1 | `0028D460` |
| `BaseMap…` | 1 | `002BCB00` |
| `BattleMenu…` | 1 | `00276D30` P |
| `BlackBand…` | 1 | `0027EE80`, `0027EED0`, `0027EF00`, `0027EF50`, `002804E0`, `002814E0`, `00281ED0`, `002BA700` P, `002C2320` P, `003F3E40`, `00558FB0` P, `00561390` P, `00565E00`, `005679D0`, `005691E0` P, `0056DD50` |
| `BtlCommand…` | 1 | `0027DED0` |
| `CPCWindowHeight…` | 1 | `00298250` P |
| `ConfigBlack…` | 1 | `00281ED0` |
| `DefUnder…` | 1 | `0027EE80`, `002C9570` P, `005679D0`, `0057A4E0` P |
| `DeftopBlack…` | 1 | `0027EE80`, `002C9120` P, `005679D0`, `0057A4E0` P |
| `EXPLPNumOffsetX…` | 1 | `0028B140` |
| `EXPLPNumOffsetY…` | 1 | `0028B140` |
| `ExpEffect…` | 1 | `0028B140` |
| `ExpNum…` | 1 | `0028B140` |
| `FontItalic…` | ~~1~~ 2 | ~~`002A6190` P, `002A6C40`, `002A70B0`~~ `00273E30`, `00298250` P, `003EED60`, `005569F0` P, `0057C480` P (corrected 2026-09-27: the three struck readers read `MessageWinMaskBottom`) |
| `GambitAction…` | 1 | `0056B350` |
| `GambitTarget…` | 1 | `0056B350` |
| `LevelupBlink…` | 1 | `00299D10` P |
| `ListHelp…` | 1 | `002C2320` P, `00565E00`, `0056DD50`, `0057A4E0` P |
| `LocaMap…` | 1 | `0027EF00`, `002804E0`, `002BA700` P |
| `LpNum…` | 1 | `0028B140` |
| `MaskBottom…` | 1 | `0029CF30`, `0029CF90` P, `002A2C00` |
| `MaskGradation…` | 1 | `0029CF90` P |
| `MaskTop…` | 1 | `0029CF30`, `0029CF90` P |
| `MessageWin…` | ~~1~~ 2 | `002A3960` P, `002A6190` P, `002A6C40`, `002A70B0` (2026-09-27: adds `MessageWinMaskBottom`) |
| `CommandTitle…` | 1 | `0027DED0` (2026-09-27: `mCommandTitleFontHeight`, lost by the 09-13 join) |
| `NAOverHeadTextOffsetY…` | 1 | `002C64C0`, `002C8BC0` |
| `PauseBlack…` | 1 | `002C9120` P, `002C9570` P |
| `ScrollBar…` | 1 | `002D2DB0` P |
| `ScrollDown…` | 1 | `002D1750` |
| `ScrollList…` | 1 | `0027AD70` P |
| `ScrollTable…` | 1 | `002D2DB0` P |
| `ScrollUp…` | 1 | `002D1750` |
| `ShopItem…` | 1 | `0056C490`, `0056D940` |
| `SilhouetteWidth…` | 1 | `002CF440` P |
| `TargetInfo…` | 1 | `002C0870` P |
| `TriangleHelp…` | 1 | `00291D80` |

### The shared band/font/signal layer — 2026-09-14 (FRONTIER, LAYOUT-KEY-READERS)

Sixteen frontier readers belong to no single screen: they are the generic band, font, mask, signal
and pause helpers that many procs share. Their convention, covered once here:

- **The band cascade** passes `height → ecx`, `gradient → edx`, `anim-ms → r8d` into `002C9060` /
  `002C9490` (band build) or `002C99A0` / `002CD7F0` (band animation), each helper binding one
  screen's `*BlackBandH` triple:
  - `0027EE80` (`Deftop`/`DefUnder`/`PartyGrad`/`AnimTime` → `002C9060`+`002C9490`, `0027EE8E`–`0027EEBD`),
    `0027EED0` (`AnimTime` alone, `0027EED4`) and `002814E0` (`AnimTime`/`PartyBlackBandTime`,
    `00281621`/`00281652`) — all reached inside **`002C2320` P**, the id-8 geometry-pass proc that
    itself reads `BlackBandAnimTime`/`PartyBlackBandGradH`/`ListHelpBlackBandH`/`mCommandMenuStrHeight`
    (`002C2409`, `002C24F0`–`002C24FD`). `002C2320` also owns the menu-list helper `002C9BF0` and,
    through `002C1A80`, the action-list mist reader `002C4720`.
  - `0027F540`, `00280D20`, `002D7070` (`PartyBlackBandTime`→`ecx`, `PartyBlackBandGradH`→`edx`,
    `r8d`=1 → `002C99A0`; e.g. `0027F57C`/`0027F59B`, `002D70C2`/`002D70CE`) — all reached inside
    `0027FB70`, the shared party-band animation helper; the shop installer's `0057B800` reads the
    same pair (`0057B82D`/`0057B839`, shop page).
  - `002C9120` / `002C9570` P — the pause-band pair, both installed by `002C99E0` (ids 1,2,4,18):
    `cmovne` selects `PauseBlackBandH` over `Deftop`/`DefUnderBlackBandH` when the pause variant is
    active (`002C9344`/`002C934B`, `002C97CB`/`002C97D2`).
- **Generic font metrics:** `002B24B0` (`FontBaseWidth`→`eax`, `002B26CD`, inside the
  `002B3120`→`002B3050`→`00474100` text-layout path), `002D4930` (`FontBaseHeight`→`r9d`,
  `sub r9d, edx`, `002D4961` — shared by the action list, battle command, nobu-message and
  `002C59D0`-family callers), `002D5EB0` P (the `NaSPArt` signal widget, installed by `002D5030`:
  `OffsetY` `sub`ed, `OffsetX`→`ecx` → `0029E770`, `002D6117`/`002D611D` — the same call the map and
  item screens use), `00291D80` P (tail-jump installed; `mTriangleHelpMessageFontCount`→`r8d` then
  `jmp 0028FD00`, `00291D80` — the triangle-help char count, reached from the menu list, save/load
  and others).
- **The screen mask:** `0029CF90` P (atlas "screen mask", installed by `0029D290`, ids 1,4,18) reads
  `MaskTop`/`MaskBottomBlackBandH`/`MaskGradationHeight` — the letterbox band heights `sub`ed from
  the frame extent (`0029D008`, `0029D011`, `0029D023`); its helper `0029CF30` does the same two
  subs on the way to `00229DA0` (`0029CF5D`, `0029CF63`).
- **The pause menu:** `00228A70` (←`00228C70` P, atlas "pause menu") reads `PauseMenuLineOffset`
  (`sub r14d` from the `+0x9E` row word, `00228BD6`), `mPauseMenuOffsetX` (`edx`, `00228BB9`) and
  `mPauseMenuOffsetY` (`sub r14d`, `00228A82`) — the pause text's line pitch and origin feeding
  `002D8910`.

*Interior reads 2026-09-17 (SWE2-FRONTIER) — the six largest `P`-marked bodies above, each
consistent with the parameter-reader role:* `002D2DB0` (ScrollBar/ScrollTable, 2,882 B —
`[rbx+0x144]`/`[rbx+0x106]` field gates, `002D8D10` ×4 per-item helper, `0x80000000` sentinel
checks on scroll bounds, [`002D2F5E`](../../_index/ADDRESS-INDEX.md)); `00273E30` (BattleCommand
family, 2,382 B — `0029CD00` ×15 + `002B58B0` ×12 + `0035D330` ×11 widget calls, first at
`00273FBB`); `0057C480`
(ConfirmCaption/ConfirmWindow/FontBase, 2,088 B — `00247510` ×5, `002D4650`/`002B1E20` ×3 each,
entry call `0057C501`);
`00228C70` (pause-menu reader's parent, 2,097 B — `00244F00` ×8, `002F9860` ×7, `00249CA0` ×4
sound calls, first at `00228CC9`); `002BA700` (LocaMap/Na/PartyBlack/BlackBand, 2,077 B —
`00273A20` ×8, first call `002BA7AB`);
`00292390` (ListItem, 1,920 B — `0029F580`/`0024A1D0`/`00181610` ×3 each, first call
`002923DF`; `00181610`'s one outward edge is a call on Platform's `001B1960` — a shared
leaf helper, mechanical). Three further bodies on the same rows: `00574E80` (`P`, PartyBlack, 1,708 B —
`00244F00` ×9 + `00246AD0` ×5, first call `00574F50`); `00281ED0` (PartyBlack/BlackBand/
ConfigBlack, 1,697 B — `00244DD0` ×6 + `00280CF0` ×5, first call `00281F9F`); `002A70B0`
(`P`, NobuMsg/FontBase/MessageLine/MessageWinMaskBottom, 1,639 B — `0024ABC0` ×4 + `0029CB70` ×3,
first call `002A712C`); `00552250` (`P`, WorldMap, 1,543 B — `00246AD0`/`00244F00` ×3 each,
factory `00244F50` at `00552316`, and the `+0x100`/`+0x102` word counters the name dictionary
records — `add word [rax+0x100]`/`+0x102` at `005526B9`/`005526C7`); `0028B140`
(NumEffect/ExpLp/EXPLPNumOffset, 1,462 B — `003F0040`/`003F1290` ×2 each, `002DD7E0` ×2,
first call `0028B186`); `002C4720` (the `ActionList…` mist reader, 3,406 B — `00808F10`
prologue at [`002C4731`](../../_index/ADDRESS-INDEX.md), then `00861EC0`/`0031EB20`/
`002DD9A0` reads over the action-list params); `005691E0` (`P`, the BlackBand family's
largest reader, 3,386 B — `002922F0`/`003282C0`/`002814E0`/`002432B0`, first call
`00569236`); `005528C0` (`P`, WorldMap, 4,521 B — `00552250`'s sibling: `00247930`/`00247570`
head at `00552949`, `002C9430` ×16, factory `00244F50` ×4, and the same `+0x100`/`+0x102`
word counters the name dictionary records — ×5 here); `00572E10` (`P`, PartyBlack,
1,422 B — `00861EC0`/`00249580`/`00247870`/`00249C60`/`005704A0`, first call
[`00572EBB`](../../_index/ADDRESS-INDEX.md)); `002A86A0` (`P`, MsgWin/FontBase, 1,364 B —
`01F44830` record base at `002A86BE`, `002F9860`/`002B4090`/`002B3400`/`002D8BB0` solver band,
first call `002A86F0`); `0055E9E0` (`Na…`, 1,314 B — `01F2CACC` constant at [`0055EA60`](../../_index/ADDRESS-INDEX.md), `002CE280`/`00252D10` ×3 + `0055B960`/`002CE2F0` ×2); `0055A340` (`P`, LicenseBoard, 1,220 B — `002472A0` first call at [`0055A39A`](../../_index/ADDRESS-INDEX.md), `002DB080`/`002D0410`/`00861F08`/`00861F0E`); `00565E00` (CommandMenu/PartyBlack, 1,914 B — `002CD510` first at [`00565E57`](../../_index/ADDRESS-INDEX.md), `002CD3C0`/`00252D10` ×8 + `002DD7E0` ×5 + `002CD440` ×3); `0028AAA0` (NumEffect, 1,692 B — `00272DE0` first at `0028AB15`, `003F1290`/`003F0040`/`00271140` ×2); `0035E070` (`P`, FontBase, 1,159 B — `005C5230` first at `0035E0B2`, `002F9860`/`002B4090`/`00254F30`/`00254A10` ×2); `002A2C00` (FontBase/MessageLine, 1,113 B — `00244F50` factory first at [`002A2C2E`](../../_index/ADDRESS-INDEX.md), `0024ABC0` ×2 + `003678F0`/`002DDD70`); `002A3960` (`P`, MessageWin, 1,159 B — `005C5230` first at `002A399B`, `002DD7E0`/`002DC290`/`002D8BB0` ×2); `002C59D0` (1,187 B — `002432B0` first call at [`002C5A23`](../../_index/ADDRESS-INDEX.md), `002D45C0`/`002C5EC0` ×4 + `002D02A0` ×3 + `002D47C0` ×2); `00558FB0` (`P`, BlackBand, 1,332 B — `01F44830` at
[`00558FBB`](../../_index/ADDRESS-INDEX.md), `0024A5A0` ×14 + `002493D0` ×4 dense reader);
`005565E0` (`P`, LicenseBoard, 1,031 B — `002472A0` first at [`00556631`](../../_index/ADDRESS-INDEX.md),
`002DB080` + `00861F08`/`00861F0E` — the same license-board reader shape as `0055A340`);
`0028D460` (`2DSideCursorCenter…`, 1,080 B — `0028CD10` first at [`0028D59F`](../../_index/ADDRESS-INDEX.md),
`003F1430`/`003F1290`/`003F1230` — a small cursor-metric reader).

### 2a. The `0027FB70` exclusive subtree — all 10 members bound (SWE2-FRONTIER, followup queue)

The exclusive-callee census assigns the party-band animation driver **10 frontier functions** —
its private machinery beneath the `*BlackBand*` reads §2 listed. `0027FB70` itself is a dispatch:
mode helpers `002549F0`/`00254A60`/`00254A80`, then per-screen apply calls that all converge on
`002C99A0(time, gradH, 1)`. Interior cites are one instruction inside each declared extent
(`interior_cite.py`; no boundary crossings).

| cluster | members | role | interior |
|---|---|---|---|
| band-state flag | `0024AC00` (7 B), `0024AC10` (21 B), `00251F20` (32 B) | `0024AC00`/`0024AC10` — get / conditional-set on the `02091094` flag dword (`ecx==1` stores, else tail `0024AC30`); `00251F20` — bit-3 set/clear of `+0xE8` on the `020927F0` object (the driver's "band active" write, called twice in the tail) | `0024AC06` / `0024AC15` / `00251F2C` |
| apply arms | `0027F540` (142 B), `00280D20` (189 B), `002D7070` (123 B), `0057B800` (138 B) | §2's four arms: each loads `PartyBlackBandTime`/`PartyBlackBandGradH` from the `01E0C3B8`/`01E0C3BC` cells directly and calls `002C99A0`, then builds a sized widget through the `00244F50` factory (`0027F540` → `0xF0`/proc `0027F5D0` with the `{request, parameter, flag}` packet; `00280D20` and `002D7070` → `0x288`/procs `00280DE0`/`002D70F0` (interior read 2026-09-17, SWE2-FRONTIER: 1,115 B — `002D6F90` first at [`002D7130`](../../_index/ADDRESS-INDEX.md), `0024A5A0` ×3 + `0056C380`/`00568B30`/`00568230`) with `{0, ecx, edx}`; `00561390` (1,091 B) — the license-board-side world-map widget, `005C5230` first at [`005613D6`](../../_index/ADDRESS-INDEX.md), `002493D0` ×5 (of the two
procs, `00280DE0` is read 2026-09-17, SWE2-FRONTIER — opens with `00281E00`/`00281AE0` at
`00280E22`/`00280E4E`, then `0024A5A0` ×5 + `002DD7E0` ×4 over the widget); `0057B800` → `0x268`/proc `0057B890` and also `or`s `0x80` into `0024A5A0(01E0C1F8)+0x38`); `00280D20` additionally lazy-builds `*(0209C318)` (`0xC0`/proc `0029D340` → `00247570` → `00246AC0`). **Corrected 2026-09-14 (SWE2-FRONTIER):** `00244F50` is the widget factory — `00244F64`–`00244FAE` scans the `0x70`-entry pool of `0x120`-stride slots at `0208EA58` and `00244FB0`–`00244FCD` allocates `ecx` bytes via `002497B0` + constructs via `002465F0` — not a param getter | `0027F5A1` / `00280D84` / `002D70D4` / `0057B83F` |
| band-object rebuild | `002909F0` (146 B), `0028C560` (36 B) | `002909F0` — the `0209BE80` object's `+0x10F00` rebuild: `0028C4F0` teardown, clear `+0x10F68` bit 3, null `+0x10EF0`, `0028C940` on `+0x7EA0`, `0028C560` retag, `0028C4B0` re-alloc → `+0x10F00`; `0028C560` — walks the `+0xD70`-linked sublist writing `5` to each `+0xD54` | `00290A18` / `0028C570` |
| param cell | `002CC9F0` (14 B) | dword setter: `arg` → `+0xDF0` of the `0209AC30` object the apply arms share | `002CC9F7` |

`002C99A0`, `00244F50`, `002CC9C0`, `00251D90` and `0024AC30` are shared callees with other
callers — deliberately not census members.

## 3. Key addresses

| Address | Role | Verified |
|---|---|---|
| `001CA600` | UI parameter loader (8,186 B) — references `mGambitPositionOffsetX` | ✅ key-binding pattern read (§2, "Which code reads each key") |
| `001AF470` | installs the ~~222~~ 227 slot pointers to the value globals (corrected 2026-09-27: 223 keyed, 4 unkeyed) | ✅ read (same section) |
| `001B44A0` | fills the second object's three float-key slots (`+0x2F8`/`+0x300`/`+0x308`) | ✅ read 2026-09-27 (same section) |
| `001CA6DA` | the referencing instruction | ✅ located |
| `008FB700` | the string `mGambitPositionOffsetX` in `.rdata` | ✅ located |

## 4. Data structures and formulas

```
jsondata/uisize/uisize.json          231 keys: 151 float, 80 int
jsondata/uisize/uisize_sd.json       standard-definition variant

parametersmanageruisizestruct.csv
  column 0   name        parameter name, or a section title when toolbox == "label"
  column 1   toolbox     "trackbar" | "label"
  column 2   DecimalPlaces
  column 3   min         (tab-prefixed in the header)
  column 4   max
  column 5   disable
```

**Resolution selection** (inferred from the file pair, not read from code — see **Y-3**):

```
layout = (standard definition) ? uisize_sd.json : uisize.json
```

> **Y-3 read from the code 2026-09-12 (FABLE) — the inference was right in shape and wrong in
> spirit: the choice is a compiled constant.** The loader `001C6C00` calls `001B1620` — an 8-byte
> getter of the byte at **`01F811E0`** — and builds `JsonData/UISize/UISize.json` when it is non-zero
> (`001C6C4A`–`001C6C8A`) or `JsonData/UISize/UISize_sd.json` when it is zero (`001C6D33`–`001C6D5B`).
> The byte has **one setter**, `001B24B0`, reached through `00184660` (which also re-runs
> `0024B120`, `00248410` and `0024B100` after the store — the re-layout hooks), and `00184660` has
> two callers: the boot function `0022A0B0` at `0022A120`, which passes **the dword at `01E0280C`**,
> and the debug menu `001D1660` at `001D1F46`–`001D1F50`, which passes the *inverse* of the current
> byte (a toggle). `01E0280C` is a `.data` constant **1** with **no writer anywhere in the image**
> (rip scan: three reads, no store), so the shipped game always selects **`UISize.json`**; the SD
> file is reachable only by the debug-menu toggle. The same byte selects the 512 × 448 PS2 reference
> frame in [what happens between two frames](../../22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md) and the font painters' raw-versus-divided metrics, so "standard definition"
> is one build-wide switch, off in the shipping executable. `002465D0` picks one of two static
> records by the same constant.

## 5. Call chain

```
startup / UI init
  -> 001CA600
     -> JsonBox parse of jsondata/uisize/uisize(_sd).json
     -> 231 named layout values
        -> battle command list, Gambit column, cursor, pause menu,
           world map, boss gauge, message window, black bands
```

**Upstream:** the resource pipeline reading from `FFXII_TZA.vbf`.
**Downstream:** every menu surface.

**Do not confuse with:** the render tuning parameters in `jsondata/init.json` and
`jsondata/maps/*.json`. Same mechanism and same `m`-prefix convention, different files and a
different owner.

## 6. Modding notes

- **UI layout is fully data-driven.** 231 numbers reposition every menu element; no code patch
  needed.
- **`uisize.json` is NOT strict-JSON valid** — it has a trailing comma (line 232). `JsonBox`
  tolerates it; `json.load` in Python does not. Any tool must parse leniently or it will fail on
  the shipped file.
- **The CSV gives you safe ranges.** Most offsets are `-100..100`, sizes `0..100`. Those are the
  bounds the developers' own tool enforced.
- **Two layouts ship.** Editing only `uisize.json` leaves the SD path untouched.
- **The schema has drifted from the data** — 229 vs 231, with name mismatches. Trust the JSON keys,
  not the CSV names.
- **XIIOnline:** UI layout is purely local presentation. Nothing here needs to cross the wire, and
  clients with different layouts are harmless.

## 7. What is not known

- [x] ~~The remaining ~220 parameter names and what each positions.~~ **Y-1 ANSWERED 2026-09-27 (FABLE, Claude Opus
      5.5) — every read of every key is read.** [`y1-layout-key-uses.tsv`](../../_index/candidates/y1-layout-key-uses/y1-layout-key-uses.tsv) gives, for each
      of the 335 (key, reader) pairs, every read site, what the value is added to, compared with or stored into, and what
      it positions; all 335 rows are `read`. 213 keys are read, in 125 functions. The other **13** are read by nothing,
      by any route: the ten `mCursor…`, `BattleLogBlackBandH`, `LicenseBlackBandH` and `FontShadowAlphaMuti`. Control
      [`y1_key_uses.py`](../../_index/candidates/y1-layout-key-uses/y1_key_uses.py) (5 checks, FAILS 0); [README](../../_index/candidates/y1-layout-key-uses/README.md).
      Among the findings:
      - `FontItalicVal` is a real slant: the glyph drawer shifts each glyph quad's top edge right by advance × value
        (`002B0AE3`).
      - `EXPLPNumOffsetX`'s authored value never reaches the digits: `0028B24A` overwrites its global first.
      - `mHelpMessageFontCount` is a width, not a count.
      - Several reader-page readings are wrong, and are routed to their author.
      *Narrowed 2026-09-13 (FABLE):* **which code each key positions** is now a table. ~~210 of the 222 keys have readers, in
      124 functions~~ *(corrected 2026-09-27: 213 of 226, in 125 — §2)* grouped by screen family (§2, "Which code reads each key"). What each reader does with its value is not read.
- [x] ~~Why the schema (229) and the data (231) disagree, and the name mismatches.~~ **Y-2
      ANSWERED 2026-09-20 (SWE2-DATA) — the three-way join decomposes the gap with zero remainder.**
      `members/uisize-y2-join.tsv` (`gen_uisize_y2_join.py`) joins the shipped CSV, the shipped
      JSON, and the bound set re-derived from `001CA600`'s `lea rdx` sites (227 sites / 226
      distinct — reproduces OPUS's count exactly):
      - **All 229 schema names are in the JSON** (schema-only set is empty); the file's two extra
        keys are `BattleMistCount0Offset` and `mBtlCommandScrollTableOffsetX`, so
        **231 = 229 + 1 schema-less addition + 1 stale duplicate**.
      - **4 schema names are dead in code** — the `NA_HintMessage{,Icon}_PosX/Y` trackbars:
        slider rows kept for an element whose binding was removed; keys still in the file,
        never bound.
      - **1 bound key has no schema row** — `BattleMistCount0Offset`: data-keyed and code-bound
        (`001CAF50`, beside its three siblings `Count1`–`Count3`, which do have schema rows)
        but the tool config never gained a trackbar for it.
      - **1 JSON key is a stale duplicate** — `mBtlCommandScrollTableOffsetX`, the pre-rename
        `m`-form of `BattleCommandScrollTableOffsetX`. Both sit in the file; only the renamed
        one is bound. *This settles the ADVANCED note's caution:* the bound X/Y pair is
        mixed-convention — `BattleCommandScrollTableOffsetX` (X, schema style) plus
        `mBtlCommandScrollTableOffsetY` (Y, member style) — and `mBtlCommandScrollTableOffsetX`
        is not the missing X of that pair; it is the orphaned duplicate of the renamed X.
      - **Name mismatches: none.** Every bound name matches a JSON key and (except the one
        schema-less key) a schema row verbatim; the apparent `Battle`↔`mBtl` mismatch was the
        stale duplicate's shadow, not a live rename discrepancy. **226 bound = 229 − 4 dead + 1.**
      *Narrowed 2026-09-15 (OPUS) — the data-vs-code half:* **`231 = 226 + 5`.** The
      loader `001CA600` binds **226 distinct keys** and **every one of them is present in the file**
      (set difference in that direction is **empty**), so the file holds exactly **five keys no code
      reads**: **`NA_HintMessage_PosX`**, **`NA_HintMessage_PosY`**,
      **`NA_HintMessageIcon_PosX`**, **`NA_HintMessageIcon_PosY`** and
      **`mBtlCommandScrollTableOffsetX`**. The last is the sharp one: the loader reads
      `mBtlCommandScrollTableOffsetY` (`001CA6B9`) **and** `BattleCommandScrollTableOffsetX`
      (`001CAEE4`), but never `mBtlCommandScrollTableOffsetX` — so an `m`-prefixed X was left in
      the data when its partner was renamed, which is a concrete instance of this row's *name
      mismatches*. *Measured against the shipped `uisize.json`; the four `NA_*` keys suggest a
      North-American hint-message element the shipped code does not position.*
      ⚠ **The shipped `uisize.json` is not strict JSON** — it ends with a trailing comma before
      the closing brace, which a strict parser rejects and JsonBox accepts.
- [x] ~~How the game chooses between `uisize.json` and `uisize_sd.json`.~~ **Y-3 ANSWERED 2026-09-12 (FABLE):** by the byte at `01F811E0`, set at boot from the `.data` constant `01E0280C` = 1 (no writer in the image) and flippable only by the debug menu — the shipped game always loads `uisize.json`; the note under the selection formula. **Y-3.**
- [x] What `NgSignal` and `BlackBand` are. **Y-4.**
      *Narrowed 2026-09-12 (FABLE):* the parameter reader `001CA600` binds the keys to slots of one
      record — `PartyBlackBandGradH` / `PartyBlackBandTime` / `WorldMapBlackBandGradH` /
      `WorldMapBlackBandH` / `PauseBlackBandH` / `DeftopBlackBandH` / `DefUnderBlackBandH` /
      `BattleLogBlackBandH` / `ConfigBlackBandH` / `ListHelpBlackBandH` / `LocaMapBlackBandH` /
      `LicenseBlackBandH` / `BlackBandAnimTime` / `MaskTopBlackBandH` / `MaskBottomBlackBandH`
      (`001CAA64`–`001CAC5C`) and `NgSignalOffsetBaseX` / `Y` (`001CAF08`–`001CAF2C`) — so
      `BlackBand` is a per-screen family of heights, gradient heights and one animation time, and
      `NgSignal` a single base offset. ~~What draws them is not followed.~~

      **`BlackBand` - answered 2026-09-16 (FABLE) in the register row, restated here so the box carries it:** a
      masking band the UI lays over the field behind a menu, one at the top (`MaskTopBlackBandH`) and one at the
      bottom (`MaskBottomBlackBandH`). It has a height authored per screen, a gradient height on two screens and an
      animation time; the fifteen keys are one contiguous run, record `+0x100`–`+0x170`.

      **`NgSignal` - ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): it is the on-screen button legend (the
      key-signal strip), and `NgSignalOffsetBase` is that strip's screen anchor.**
      - **Where the two values go.** The key-slot installer `001AF470` points `NgSignalOffsetBaseX` at `0209C494`
        and `…Y` at `01E0C584` (`001AF844`–`001AF859`). Record `+0x228` / `+0x230` is installer `+0x3D28` / `+0x3D30`,
        the same `0x3B00` step that maps `LocaMapBlackBandH` (`+0x150`) to `01E0C3E0`. That control is the global the
        map-screens page reads independently. The shipped `jsondata/uisize/uisize.json` authors 86.0 and 18.0.
      - **The one reader is the legend's host.** Each global has exactly one reader, `0029E110` (`0029E251`,
        `0029E271`). That is the procedure of the `0x3F8`-byte HUD widget which `0029E0E0` builds on demand and which
        publishes itself at `0209C498`. Its `+0x158` child holds the button legend that
        [five-small-bin-tables.md](../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/five-small-bin-tables.md)
        decodes (its section 185). The construct arm stores `+0xC0 = X` and `+0xC2` = screen height (`01E0C1DC`, 448)
        − `Y`.
      - **How the strip is placed.** `0029DCE0` sets the legend's x to `+0xC0` + `+0xC4` minus a term `0029DFB0`
        measures over the entries' strings. It sets y to `+0xC2` + `+0xC6` minus the strip height: twice the pad
        (8) plus 20 per shown entry (`0029DD2A`–`0029DD89`). `+0xC4` / `+0xC6` are a per-screen nudge set by
        `0029E730(dx, dy)` from three call sites, `00295D42`, `00295D60` and `002BAB48`.

      *So with the shipped values the strip's base line sits 18 lines above the bottom of the 448-line layout,
      from x 86, and the strip grows upward by its own height.* **Not established:** what `Ng` abbreviates, and any
      live observation. The evidence is static plus the shipped layout file.
- [x] ~~Whether the parameter-manager tool itself is recoverable.~~ **Y-5 ANSWERED 2026-09-22
      (FABLE): no — only its CONFIGURATION shipped, and the game itself ignores that.** Two
      measurements, each with its own control.
      - **No binary ships.** Every file in the extract was opened and tested for `MZ` magic:
        **0 of them are a Windows image**. *Controls:* the same test reads `MZ` off the game's own
        executable, so it can see a PE; and the walk counts **35,984** `.phyre` files, this
        corpus's published figure. The archive ships no executable of any kind — the extension
        census runs `.phyre`, `.ebp`, `.sab`, `.webm`, `.csv` (17) and the rest, with nothing
        executable among them.
      - **The tool's logic is not in the game either.** The image names its own layout files —
        `JsonData/UISize/UISize.json` and `JsonData/UISize/UISize_sd.json` literally, with
        `uisize` occurring 4 times and `jsondata` 9 — but searched **case-insensitively** it
        contains **zero** occurrences of `parametersmanageruisizestruct`, `parametersmanager`,
        `uisizestruct`, `toolbox`, `trackbar` or `DecimalPlaces`. **The game never opens the CSV
        and does not know a single word of its schema.**

      > **So the tool is a separate developer application and nothing of it survives here.** What
      > shipped is the file it was configured by, left in `jsondata/` as an artifact the runtime
      > has no use for. **The recoverable part is its behaviour contract, and §3 already states
      > it**: per parameter, the widget kind (`trackbar` or a `label` section title), the decimal
      > places, and the `min`/`max` the tool enforced — 266 rows of it. *A reimplementation can
      > rebuild a tool that behaves identically; it cannot recover the original.*

      > **A case-sensitivity note worth keeping, because it nearly inverted this answer.** The
      > archive index is entirely lower case (`0 of 89,414` entries carries an upper-case letter),
      > so the extract's path is `jsondata/...`. **The image's literals are mixed case**
      > (`JsonData/UISize/UISize.json`). A lower-case search of the image returns 0 for `uisize`
      > and `jsondata` and looks like a finding; it is an artifact of searching the image with the
      > archive's casing. The zeros above are case-insensitive, and the non-zero `uisize`/
      > `jsondata` counts are the control that says so. **Y-5.**
- [x] ~~The body of `001CA600`.~~ **Y-6 ANSWERED 2026-09-15 (OPUS) - read in full, 8,186 B /
      1,600 instructions. There is no loop and no table: the key list is unrolled in code as
      227 read sites over 226 distinct keys.**
      - **It opens with an all-or-nothing guard.** `001CA604` looks up `mScrollListHeight` and
        calls `Variant_IsAbsent`; if the key is absent, `001CA621` jumps straight to the
        return at `001CC5FA` and **not one parameter is bound**. A single missing key silently
        leaves all 226 at their static defaults - the whole layout system has one point of failure.
      - **Then two base pointers, for two different destination objects.** `001B1C00` returns
        `[01F811E8]` and `rbx = that + 0x3B00` is the slot-pointer array `001AF470` installs;
        later, `001CC566` calls `001B5FB0` - a lazy singleton on `[01F81200]` - for a second object.
      - **Each site is the same three steps:** `001FF740` (`EASTL_LookupByCString`) against the one
        parsed document at `01F81318`, a typed read, then a store through a slot pointer:
        `mov rcx,[rbx+disp]` / `mov [rcx],eax`. The slot displacements are 8 apart but **not
        contiguous** - `+0x00`, `+0x08`, `+0x10`, `+0x18`, then `+0x28` - so the array has gaps.
      - **The typed split is 223 int to 3 float.** `Variant_ReadInt` (`00200B80`) for 223 keys;
        `Variant_ReadFloat` (`00200B50`) for exactly three - `FontItalicVal`, `FontItalicScale`,
        `FontShadowAlphaMuti` - which store `movss` into the **second** object at `+0x2F8`,
        `+0x300`, `+0x308` (`001CC589`-`001CC5E3`), never through the slot array.
      - **`mScrollListHeight` is the only key read twice** - once at `001CA604` as the guard probe,
        once at `001CA631` as a real `Variant_ReadInt`. So 227 sites, 226 distinct keys.
      - **It releases the document on the way out:** `001CC5F0` tail-jumps to `00202880`, which
        frees the payload and stamps the tag back to 6 (absent).
      - **The accessor ABI is not restated here** - `001FF740`, `00200B50`, `00200B80` and
        `00200BE0` are already decoded from their bytes in
        [what-the-console-tunes.md](../../00-Engine-Core-Runtime/Developer-Tuning-Console/what-the-console-tunes.md).
      - ⚠ **Two figures on this page do not match the body, reported rather than rewritten.**
        (1) This page's join gives **222** keys bound; the body binds **226 distinct**. *Resolved 2026-09-27 (FABLE): the join
        had two defects of its own, and corrected it binds all 226 (§2, "Which code reads each key").* The three
        float keys land on `[01F81200]`, not on `001AF470`'s slot table, so a join built only on
        that table cannot see them - that plausibly explains part of the gap, but it is an
        explanation offered, not a measurement, and the remaining difference is unexplained.
        (2) *“151 floats and 80 integers”* describes the **JSON literal syntax**, not the engine's
        type: 223 of the 226 are read with `Variant_ReadInt`, which `cvttsd2si`-truncates a JSON
        double, into genuinely integer globals - `WorldMapWidth`'s `01F2CAA4` has **7 references in
        5 functions and every read is an integer GPR load** (`mov ecx/edx/eax`, `add r14d`; control
        `01F81318` returned 234, so absence would have been meaningful). **The truncation is real as a mechanism but never
        exercised, which I should have measured before implying otherwise.** The shipped file
        holds **231 keys, 80 written as integer literals and 151 with a decimal point** — but
        **149 of those 151 are whole-numbered**, and the **only two fractional values in the
        entire file are `FontItalicScale` `0.88` and `FontItalicVal` `0.27`, both of which are
        read with `Variant_ReadFloat`.** **No value read through `Variant_ReadInt` has a
        fractional part**, so `cvttsd2si` discards nothing in the shipped data and the three
        float keys are exactly the ones that need the precision. The guard key
        `mScrollListHeight` is `46.0`, so the all-or-nothing probe passes. Both figures
        belong to `Y-1`/`Y-2` and are their owner's to correct. **Y-6.**
- [x] ~~What `monstergallery.json` (337 KB) and `monstertoweapon.json` (50 KB) contain.~~ **Y-7
      answered 2026-09-12 (FABLE) — read from `FFXII_TZA.vbf`; ~~the readers are not found~~ **corrected 2026-09-19
      (FABLE): the gallery keys' reader is `001C6320`, which formats `MonsterId%d` and reads every key below by
      name - [the handbook's monster viewer](../Handbook/the-handbooks-monster-viewer.md); the reader of
      `monstertoweapon.json` is still not found** (neither
      file name is a literal string in the image).** `monstergallery.json` is **the Clan Primer's
      monster-viewer presentation table**: a `Common` default plus **384 entries `MonsterId0`–`MonsterId383`**
      (no gaps), each with the same 38 keys — `monsterModelId` (a letter in the high word, `m` ×295 /
      `n` ×76 / `s` ×13, over a **model index 0–249**, 303 distinct), `motionIndex` (0–80), `motionRepeatFrame`,
      `motionRate`, `modelScale`, `xOffset` / `yOffset`, `cameraPitch` / `cameraYaw` / `cameraFov`, ambient
      and two directional lights (direction, colour, intensity), `bgColorR/G/B` / `drawBgColor`,
      `eyeVfxZBias`, `variation`, `clut`, and **`monsterWeaponIndex` / `monsterWeaponIndex2` in 4096–4634 —
      the `0x1000`-based weapon ids** ([the encoded-id space](../../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md)). `parametersmanagermonstergallerystruct.txt` is the
      editor schema for exactly those keys (name, type, setter group, min, max, default — e.g.
      `motionIndex 0..80`, `cameraPitch −30..80`, `cameraFov 0.5..4`). `monstertoweapon.json` maps **349 monster
      model ids** (the same letter-over-index keys, plus the file name `ModelName` `m1231` …) to **one to
      seven weapon models** (`w1003` … with a `WeaponIndex`, 82 distinct ids in the same 4096–4634 space; 311
      monsters carry one) — the weapon models a monster is drawn holding. Neither file holds stats: the
      bestiary's numbers come from the battle tables, these two only tell the viewer how to pose and
      light a monster and which weapon meshes to attach. The letter-over-index key is the scheme the
      motion-override tables use too ([section 019](../../25-EBP-Script-Container/Sections/section-019.md), CC-10).

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| 231 UI parameters, 151 float / 80 int | `uisize.json` extracted from the retail VBF and parsed | 1 |
| Schema is 266 rows: 229 trackbars, 36 labels | `parametersmanageruisizestruct.csv` extracted and parsed | 1 |
| Slider ranges and decimal precision per parameter | the CSV's own columns | 1 |
| 36 named UI sections | the CSV's `label` rows | 1 |
| `uisize.json` is not strict-JSON valid | `json.load` raises `Illegal trailing comma ... line 232 column 35`; a lenient re-parse succeeds | 1 |
| An SD layout variant exists | `jsondata/uisize/uisize_sd.json`, 4,609 B, present in the archive | 1 |
| `001CA600` loads these | RIP-relative reference from `001CA6DA` to the `mGambitPositionOffsetX` string | 1 |
| Key → global (~~222~~ 226) and global → reader (~~210 keys, 124 functions~~ 213 keys, 125 functions; corrected 2026-09-27) | `members/layout_key_slots.py` joins `001CA600` with `001AF470`; `members/layout_key_readers.py` scans every listed function; the map screens' readers as the control | 1 |

**Everything here came from the shipping data**, extracted from the authorized 31 GB
`FFXII_TZA.vbf` with `vbfextract.py`. It is tier 1 in the strongest sense available for data: not a
decompilation of code that reads the file, but the file itself.

**The one thing not from data** is the resolution-selection rule in §4, which is inferred from the
existence of a `_sd` file. No code was read to confirm when it is chosen, and it is marked as
inferred there and tracked as **Y-3**.

## 9. Related

- [`../../17-Presentation-Rendering/Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md`](../../17-Presentation-Rendering/Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md) — the same mechanism for rendering, where these names were first found
- [`../../23-Third-Party-Libraries/third-party-middleware-inventory.md`](../../23-Third-Party-Libraries/third-party-middleware-inventory.md) — JsonBox, the parser
- [`../../02-Resource-And-Asset-Pipeline/resource-section-addressing.md`](../../02-Resource-And-Asset-Pipeline/resource-section-addressing.md) — how VBF content is reached

## 9. Falsification pass 2026-09-02

**Attack chosen.** This document rests on two kinds of claim: **counts inside data files** (231
parameters, 266 schema rows, 229 trackbars) and **references inside the executable**. Only the
second can be checked from the authorized binary, so that is what was checked — and the first is
recorded as **not re-derived**, not as verified.

### SURVIVED exactly: the binary-side evidence

| Claim | Result |
|---|---|
| the string `mGambitPositionOffsetX` lives at `008FB700` | ✅ `.rdata`, exact |
| `001CA6DA` is the referencing instruction | ✅ `48 8D 15 1F 10 73 00` = `LEA RDX, [rip+0x73101F]` → **`008FB700`** |

That is the whole tier-1 chain in §3, and it holds byte for byte.

### NOT re-derived: the file counts

`jsondata/parametersmanageruisizestruct.csv` and the parameter JSON are **inside the VBF archive**
and are not extracted on this machine, so **231 / 266 / 229 could not be recounted**. They stand as
originally recorded, unconfirmed by this pass. Anyone extracting the VBF should recount them first —
every other count this database has re-derived has been checked, and these three have not.

### Y-2 ADVANCED: part of the schema/data mismatch is a naming convention, not a missing parameter

§2 records that the schema names `BattleCommandScrollTableOffsetX` while the data does not, and
**Y-2** asks why schema and data disagree. The executable carries **both naming conventions side by
side**:

```
BattleCommandScrollTableOffsetX     no `m` prefix, full word "Battle"    <- schema style
mBtlCommandScrollTableOffsetY       `m` prefix, abbreviated "Btl"        <- data/member style
```

Across the whole image the split is visible in the `BattleCommand` family: **eight** names carry no
`m` prefix and spell "Battle" in full, while the member-style names take the `m` prefix — and the one
scroll-table name that does so also **abbreviates to `Btl`**.

So at least one of the reported mismatches is **two names for one concept under two conventions**,
not a parameter present in the tool and absent from the game. Two cautions, both material:

- The axis differs too — the schema name ends `X`, the member name ends `Y` — so this is **not a
  pure rename**, and the pair cannot simply be equated.
- This explains *a* mismatch, not the **229 vs 231** count gap, which remains open until the files
  can be recounted.

**Y-2 stays open**, with the convention split recorded as a lead: when comparing schema names to data
keys, normalise `Battle`↔`Btl` and the leading `m` before concluding a name is missing.

### Note for §6

The modding guidance *"Trust the JSON keys"* is unaffected and, if anything, reinforced: the JSON
uses the member-style names the engine actually looks up, which is the `m`-prefixed form referenced
from `001CA600`.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — SERVICE and CLIENT, 21 edges.** Cited layout functions call small core helpers (40 bytes 9 times, 7 bytes 4 times, 8 bytes twice, 37 bytes) and the 146-byte core start-up helper. They are called by the 978-byte core start-up root and a 387-byte core start-up body (2).
- **CombatAI - SERVICE (2 edges).** `00283270`, BattleMenu_BuildCommandEntryList (`0031EB20`) reach bodies filed to CombatAI: GambitConfig_ClassifyActionTargetPairCompatibility (`00327A10`), GambitConfig_CopyBasePairSetForStatsIndex (`00327BE0`) - shared machinery across the layer boundary, no shared ownership.
- **Developer - CLIENT (4 edges).** `00200B50`, `00200B80`, `00200BE0` are called by bodies filed to Developer: `001C2F50`, `001C6320` - shared machinery across the layer boundary, no shared ownership.
- **Party - CLIENT and SERVICE (4 edges).** `00283270` is called by bodies filed to Party: `00328BD0`; `002C64C0`, BattleMenu_BuildCommandEntryList (`0031EB20`), `00326BB0` reach bodies filed to Party: BattleUnit_ResolveByFocusHandle (`0031B7E0`), PartyFocus_GetCurrentPackedActorHandle (`003590D0`) - shared machinery across the layer boundary, no shared ownership.
- **RNG_Random_Selection - SERVICE (1 edge).** `0022A0B0` reaches bodies filed to RNG_Random_Selection: RNG_MT19937_Seed (`00379CF0`) - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (25 edges).** `00229EA0`, `00249CA0`, `00264150`, `002DEE50` (+10 more) are called by bodies filed to Script_VM_Native_Bridge: `0033F310`, `0033FD40`, `00340260`, `00345B60` (+21 more) - shared machinery across the layer boundary, no shared ownership.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Movement — SERVICE.** `00281AE0` on this page calls `FUN_00326bb0`, owned by that layer. What it reaches is a one-time reset guarded by bit 0 of `[022C25A0]`: it stamps a table of `0x30`-byte slots from `022C25B0` with `0xFFFF` sentinels and zeroed counters; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Story_Event_Quest_Hunt — SERVICE.** `00281AE0` on this page calls `PersistentFlag_QueryPrimaryOrAuthoredTable`, owned by that layer. What it reaches is the flag query whose id is masked to `0x3FFF` while **bit 14 selects between the primary and the authored table**; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Audio — MECHANICAL (SWE2-CONTRACT 2026-09-15, 20 edges).** 17 of the 20 edges are the single
shared helper `00249C60` (Audio-tagged) called by fourteen of this page's layout bodies
(`00241D40`, `00281ED0`, `002A3960`, `002A6190`, `002A70B0`, `002C2320`, …); the rest are
`00249CA0` via `00241D40`, `001DBB00`/`002DEBA0` via `001D1660`, `002DEE50` via `002814E0` and
`00271500`/`002716F0` via `002D5EB0`. `00249C60` is a generic query helper the census attributes to
Audio — the same fan-in appears on the menu-screen-atlas row — not an audio relationship the layout
schema owns.

**ActorEntity — MECHANICAL (SWE2-CONTRACT 2026-09-15, 6 edges).** ActorEntity bodies share the page's cited generic
accessors — same fan-in shape as the Audio row above.

**Input — MECHANICAL (SWE2-CONTRACT 2026-09-15, 5 edges).** Same shape — input bodies neighbour the shared helpers.

**Rewards_Progression_Economy — MECHANICAL (SWE2-EC7 batch 27, 1 edge).** `002F90C0`
(`Reward_ComputeLicensePointsForRecipient`) calls `00264150`, the condition guard this page's
`002CDAE0` dispatcher variant arms run. Shared-callee fan-in, not a rewards relationship the layout
schema owns.

**Gameplay — SERVICE (SWE2-CONTRACT 2026-09-15, 2 edges).** Layout bodies `00273E30`/`0035E070` call the Gameplay definition-validation helper `0031C5D0`. Small, real.

**Items_Equipment_Shops_License — SERVICE (SWE2-EC7-158, 14 edges).** Batch-123's `002CA5D0` names `002CBA50`/`002CA7C0`/`00282DF0`, and the layout helpers `002826F0`/`00283E40` are called from the items layer (`00317B70`/`00323630`/`00323670`) — shared-helper exchange, not a shared responsibility.

**Presentation — MECHANICAL (SWE2-EC7-159, 525 edges).** The dominant fan-in is `0017FFD0`, called by Presentation bodies `003745C0`/`00449AB0`/`00455DB0`/`0045B8xx` et al.; batch-124's `002847C0` names the text-metric helpers `002DDC50`/`00254A00`, whose own neighbours are Presentation-tagged. Shared presentation fan-in, not a layout responsibility.

**Resource — MECHANICAL (SWE2-EC7-160, 83 edges).** `00181610` is called by `0024A680`, `001B1960` calls `001B1440`, `001D1660` calls `002EEEE0`, `0022A0B0` calls `00259DF0` — batch-125's `0037F860`/`0028CB90` name layout teardown/lookup helpers whose neighbours are Resource-tagged. Shared-helper exchange, not a layout responsibility.

**WorldAreaField — MECHANICAL (SWE2-EC7-172, 21 edges).** The batch-137 `003C1DF0` section newly names the
allocator `003BD950`, which calls `00265270`; the standing edges are `0057FB00` calling this page's
`00264150`/`002DC290` and the shared helpers `0020E620`/`002F9860`/`00808C40`, the `00314440`/`00314530`/
`003145E0` cluster calling `002EFA70`/`002EFD20`/`005C5230`/`00808C40`/`00861EC0`, and this page's `002B7B80`
calling `WorldTransition_GetActiveOrPendingFieldId` (`003148F0`). Shared-helper exchange, not a world/field
relationship the layout schema owns.

**Save/Load — SERVICE.** `00225580`, the scaled-row emit this page's `002D53F0` entry names, and `00244960` share a caller set in the Save/Load layer (`005812B0`/`005817D0`/`00581930` and siblings) - the layout page borrows a shared row-emit helper; it owns no save-state machinery.
**PlatformOnlineAchievements — CLIENT (SWE2-EC7, batch 168, 7 edges).** The batch-168 `003BD950` resolved-row probe names `00265270` and `0032A8A0`, whose callers `003154B0`/`003162E0`/`00316760`/`00254E80` sit on that layer - achievements-side bodies consult the same resolve helpers the layout block's probe uses; shared-helper consultation, not ownership.



## Interior citation — frontier hubs `002D8BB0` / `002D45C0` / `0024A5A0` (2026-09-17, SWE2-EC7)

Three helpers this page's arms call, all read against the shipping image:

- `002D8BB0` (79 B, 12 A-callers) — the `+0x5C`/`+0x5D` repeat-bitmask gate. Interior verified:
  `edx == 1` increments `byte [+0x5D]` and, only when it wrapped from 0, tails
  `00249FD0(0)`; otherwise it decrements the `0xFF00` field of `[+0x5C]` and, when that byte
  reaches 0, selects `rcx+0x48` iff bit `0x11` of `[+0x5C]` is set before the same tail
  ([`002D8BCA`](../../_index/ADDRESS-INDEX.md)–`002D8BF9`). A saturating up/down counter whose
  zero crossing fires the shared `00249FD0` notify with an optional payload.
- `002D45C0` (134 B, 11 A-callers) — flag-write + conditional notify: `+0xE0` bit 16 is
  rewritten from `arg & 1` ([`002D45CA`](../../_index/ADDRESS-INDEX.md)), then the `[rbx+0x10]`
  chain is walked for a node whose `[+0x40]` bits 0 and 3 are set and whose `[+0x7C]` low nibble
  is 5-or-negative; reaching `00244820`'s result node fires `003689E0(arg)`.
- `0024A5A0` (75 B, 11 A-callers) — the dense reader's lookup: a 64-entry name table at
  `0208F580`, stride 0x48, gated on `[entry+0x38] & 0x20`; entries that pass get a byte-string
  compare against the arg ([`0024A5C0`](../../_index/ADDRESS-INDEX.md) loop), returning the
  entry pointer or 0. The name side of the resource registry the readers resolve through.

NOT claimed: the `0x48`-stride record's other fields, or what `+0x38` bit 5 gates semantically.

## Interior citation — frontier hubs `00244DD0`, `003678F0`, `0029CD00` (2026-09-18, SWE2-EC7)

`00244DD0` — 301 B, 9 A-measured callers; a widget state-initialise called ×6 by the
ConfigBlack ctor listed above. Interior verified: `[rcx+0xB8]` is preset to `1.0f`
(`00244DE1`); when `00229EA0()` returns 2 the field becomes `K/00229E70()` via the `divss` at
`00244E0B`. The mode switch reads `[rcx+0x7C]` low nibble (`shl/sar 0x1C` at `00244E2F`): modes
0/3 set bit 9 of `[+0x40]`, pick a record pointer for `[+0x68]` (bit 16 selects `009151AC` vs
`[+0x48]+0x14`), seed `[+0x74]` from the `0208F570`-band global and `[+0x78] = 1.0f`, ~~run
`00181C90` on `word[record+2]`, and fold the result into `[+0x70]` through the divide-by-60
magic `0x10624DD3` at [`00244ED1`](../../_index/ADDRESS-INDEX.md)~~ and set `[+0x70]` from `word[record+2]`. The
delay is zeroed when the getter `00181C90` returns 1, and then replaced by `[+0x7C]`'s top 10 bits when its bit 11 is
armed. The result is converted from milliseconds to 60 Hz ticks, `floor(x·60/1000)`, through the `0x10624DD3` magic at
[`00244ED1`](../../_index/ADDRESS-INDEX.md). Mode 2 instead writes `[+0x74] = 2*global -
[+0x70] - [+0x74]` and clears `[+0x70]` when bit 16 is set. ~~The tail always ORs `0x34` into
`[+0x7C]`~~ Other nibbles return before the tail. With `[+0x40]` bit 0 clear the nibble becomes 1 before the tail's
`or 0x30`, and on the schedule and rebase paths it becomes 4. When `[rbx]` is non-null, the tail vcalls it with
argument `01E0C0F8` (`00244EF5`) — the completion notify. *(Corrected 2026-09-28, FABLE, Claude Opus 5.5, on ASTRA's
widget-deferred-dispatch-domain; re-read from the listing. The bit-16 wording above was already right. See
[the widget contract](../Widget-Object-Model/CONTRACT-widget-object.md) for the full order.)*

`003678F0` — 79 B, 9 callers; the sentinel reset the MessageLine/FontBase constructors run
(`002A2C00` above). Interior verified: a cluster of globals at `022CBE38`/`022CBE3E`/
`022CBE4C`/`022CBE50`/`022CBE70`/`022CBE76`/`022CBE7A`/`022CBE7E`/`022CBE82` is written with the `0x8000`
/`0x80008000`/`0` "unset" pattern ([`00367901`](../../_index/ADDRESS-INDEX.md)–`0036793E`) — the same -32768
sentinel the layout parameter records use.

`0029CD00` — 134 B, 8 callers ×15 in the family pass above; the float-scaled variant of
`002B3050`. Interior verified: it forwards `(rcx=ctx, rdx=arg, r8=&[rsp+0x60],
r9=&[rsp+0x20])` to `002B3050` at `0029CD24`; when `xmm2 > 0` both word outputs are scaled —
`[rbx] = word[rsp+0x60] * f` and `*qword[rsp+0x70] = word[rsp+0x20] * f` via `cvtdq2ps`/
`mulss`/`cvttss2si` at [`0029CD3D`](../../_index/ADDRESS-INDEX.md)–`0029CD60`; when `f <= 0` the raw words pass
through unscaled.


## Interior citation — frontier hubs `002CE2F0`, `002D8910` (2026-09-18, SWE2-EC7)

`002CE2F0` — 120 B, 7 A-measured callers; a gated `0xE0`-record submit. Interior verified:
`[0209AC30]`'s dword `+0x2E8` must be zero or it returns 0 (`002CE30A`–`002CE312`); otherwise it
packs the caller's `ecx`/`edx` into a stack pair, passes `ecx = 0xE0` and `rdx` = the literal
block at `002CE370` (the bytes immediately after the body, `002CE33D` `lea rdx,[rip+0x2C]`) to
`00244F50` — the fixed-pool widget allocator this contract already measures — at
[`002CE351`](../../_index/ADDRESS-INDEX.md). GS-cookie checked (`00808C40`).

`002D8910` — 198 B, 6 A-measured callers; a two-arm record materialiser. Interior verified:
`00364980` is the predicate (`002D8946`); on true it builds a 16-byte arg block
`{edi, esi, [rbx+0x70]}` and runs `003659F0` ([`002D8982`](../../_index/ADDRESS-INDEX.md)) then
`002DD5D0` (`002D8994`); on false it runs `002B3400` — the persistent-record init measured on
the widget-object contract — at [`002D89A1`](../../_index/ADDRESS-INDEX.md) then `002DD680`.
Same `(rbx, edi, esi, rbp)` argument shape on both arms; only the constructor differs.


## Interior citation — frontier hubs `002C9430`, `0024ABA0` (2026-09-18, SWE2-EC7)

`002C9430` — 87 B, 13 callers; the `0209AC30` command record's bounded stat read the
layout rows share. Interior verified: `ecx & 0x7F` selects `[+0x2B8]` vs `[+0x2C8]`
(`002C943E`–`002C9449`); the sign bit of `cl` with `[rdx+0xD0] & 1` takes the summed arm —
`word[+0xDA] + word[+0xD6]`, optionally rebased by `[01E0C1DC]` when the low 7 bits are set
([`002C9454`–`002C947A`](../../_index/ADDRESS-INDEX.md)) — else `word[+0xCE]` at
`002C947F`. Bit 7 of the selector picks "computed" over "stored".

`0024ABA0` — 20 B, 11 callers; the dword-ratio leaf. Interior verified:
`cvtdq2ps [01E0C1DC]` divided by the `008C5B44` constant at
[`0024ABAB`](../../_index/ADDRESS-INDEX.md) — a scalar published as a float for the layout
rows' consumers.

## Interior citation — frontier hub `002D4650` (2026-09-18, SWE2-EC7)

`002D4650` — 160 B, 11 callers; a layout-record update arm. It snapshots `[rcx+0xED]` (sbyte)
and `[rcx+0xF2]` (sword), calls `002D4B70`, and when that returns 1 replays the delta pair —
`[+0xED]`−old, `[+0xF2]`−old plus `eax+6` — into `002D4A40` (`002D467A`–`002D4696`). Then, if
the `[+0xC8]` sub-record exists, it composes the linear index
`([+0xF4]+[+0xF2]) * byte[+0xEC] + byte[+0xEE] + byte[+0xED]` and calls
`00247510(record, idx, 0x8000)` ([`002D46DB`](../../_index/ADDRESS-INDEX.md)) — the
`0x8000`-flagged write the layout schema's grid cells receive when a parameter row moves.

## Interior citation — frontier hub `003FFAB0` (2026-09-18, SWE2-EC7)

`003FFAB0` — 78 B, 9 callers; the three-byte escape-field decode the `002AC5F0`
control-code interpreter (`UI.Text.ControlCodeInterpreter`, §174/184/193 class rows)
consumes. When `[rcx+1] & 7` is zero it ORs `([+1] & 0xC0) << 1` into `[+2] & 0x7F` and
writes the composite byte to `[rdx]`; otherwise it treats `[+2] & 0x7F` as a table index,
reads `byte [0039BA00(cl)]`'s result (`0039BA00` at [`003FFAD8`](../../_index/ADDRESS-INDEX.md))
and stores that instead. Returns 3 — the consumed byte count, which is how the interpreter's
stream cursor advances past a two-parameter escape.

## Interior citation — frontier hub `00200B50` (2026-09-18, SWE2-EC7)

`00200B50` — 41 B, 8 callers; the variant-to-float reader shared by the parameter rows.
Tag `[rcx]` selects the payload at `[rcx+8]`: `2` dereferences a `double` and `cvtpd2ps`s it
([`00200B5F`](../../_index/ADDRESS-INDEX.md)), `1` dereferences an `int32` and `cvtdq2ps`s
it, any other tag returns `0.0f`. The schema's numeric cells are stored as this tagged pair;
this is the single point where their declared type becomes the float the UI draws.


### Interior citation — frontier hub `002D47C0` (2026-09-18, SWE2-EC7)

`002D47C0` — 128 B, 16 callers: the size-compute `002C59D0` runs twice. First
`002D4D60(rcx)` — when it returns 1, `002D4A40(rcx, 0, 0, stack_arg)` re-inits
the record. Then when `r9d` holds and `[rbx+0xC8]` exists, the body computes
`edx = (word[+0xF4] + word[+0xF2]) * byte[+0xEC] + sbyte[+0xEE] + sbyte[+0xED]`
([`002D4813`](../../_index/ADDRESS-INDEX.md)) — width-times-height plus two
signed margins — and calls `00247510([rbx+0xC8], 0x8000, edx)`. The
element-size query feeding the layout allocator.

### Interior citation — frontier hubs `002C9EB0`, `0029E330`, `002CC630`, `00200B80`, `0029DBE0` (2026-09-18, SWE2-EC7)

`002C9EB0` — 101 B, 7 callers (`00565E00`, `002C2320`, `00280DE0` above): the
`0x11F`-kind callback invoke — packs `{0x11F, movsxd edx, movsxd r8d}` and
calls `[rcx]` when non-null at
[`002C9EED`](../../_index/ADDRESS-INDEX.md), cookie-guarded.

`0029E330` — 116 B, 6 callers (`002D5EB0`, `005789D0` above): the
`0209C498`/`0209C4A0`-gated init pass — `0029DA70` builds the block,
`0029DDF0` runs it, `[rax+0xC4]` is zeroed, `0029DCE0` finishes at
[`0029E364`](../../_index/ADDRESS-INDEX.md), cookie-guarded.

`002CC630` — 35 B, 6 callers (`002C59D0`, `0057A620` above): a two-hop
adapter — `00282DF0(movsx word[*(0209AC30)+0xDE0])` then tail `002CC660` at
[`002CC642`](../../_index/ADDRESS-INDEX.md).

`00200B80` — 31 B, 6 callers, `Variant_ReadInt`: the typed reader the key
stores run — tag `1` reads `dword[[+8]]`, tag `2` `cvttsd2si` the qword at
[`00200B97`](../../_index/ADDRESS-INDEX.md), anything else 0.

`0029DBE0` — 174 B, 6 callers (`002D5EB0` above): the `0209C4A0` TLV decode —
`ecx >= 0x100` resolves `word[+0xA]`-offset header + `ecx-0x100` index, clamps
against `dword[hdr]`, reads `byte[hdr + idx*4 + 7]` at
[`0029DC17`](../../_index/ADDRESS-INDEX.md), and switches 0x16/0x17/0x1A to either
`word 01E0C2A4`, or the `word[+8]`-offset second table's
`dword[hdr2 + code*8 + 8]`. The tagged-payload decoder the UI reads
through.

### Interior citation — frontier hubs `0029DA70`, `002C99A0`, `002CC960`, `002CBC20`, `003BDB30`, `003BDCD0` (2026-09-18, SWE2-EC7)

`0029DA70` — 361 B, 7 callers: the record builder behind `0029DBE0`'s TLV
decode. Walks the `word[+0xC]`-offset u16 index list looking up a byte ==
`edx`, copies the 3-byte record header, then loops the secondary
`word[+0xA]`/`word[+8]` tables with the same clamped `byte[hdr + idx*4 + 7]`
code read at [`0029DB1A`](../../_index/ADDRESS-INDEX.md), masks the payload
`& 0xFFFFFF`, calls `002F9920` twice and writes 0x18-stride output records
(two pointers + flags + byte) until the count at `byte[r14+2]` is reached.

> **Falsification note (FABLE, 2026-09-18) — the two readings above are mechanically right and semantically wrong.** `0209C4A0` is not a pane-state block and `0029DBE0` / `0029DA70` are not a TLV decoder. The pointer is written by `0029DCD0`, the completion handler `0029DC90` attaches to its request `(7, 0x24)` = `key_signal_data.bin` (`0029DCBF`, through `00249180` → `00249210`); the `word[+8]` / `word[+0xA]` / `word[+0xC]` the two bodies index are that file's **three section offsets** (`0x10`, `0xEC`, `0x150`), the `dword[hdr]` is each section's record count, and the records are `{u32 nameTextId, u32 buttonMask}` (section 0), `{u24 labelTextId, u8 buttonIndex}` (section 1) and the scene table (section 2). So `0029DBE0(key)` returns the **pad-button mask** of a key (tested by every caller against a word of the gameplay input snapshot `02F97360`), and `0029DA70(out, scene)` builds the **button legend** for a scene. The switch codes `0x16 / 0x17 / 0x1A` above are right. Separately, `0029E770` writes its word pair on `[0209C498]`, the key-signal HUD object, not `[0209C4A0]` (`0029E770`–`0029E783`). Full reading on [the five small bin tables](../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/five-small-bin-tables.md), UQ-69.

`002C99A0` — 53 B, 5 callers: dual-call adapter — `002C99E0(ecx, 0)` first,
then when `r8 == 1` also `002CD800(ecx)` over the `[0208EA10]` record at
[`002C99B2`](../../_index/ADDRESS-INDEX.md).

`002CC960` — 68 B, 5 callers (`002814E0`, `00574E80` above): indexed fan-out
— `ecx > 1` gate, `002EFD20(3)` mode check, then loops `002EFA70` with
`r9+3`/`r9+1` and an index scaled `ebx*0x3C` through the `0x10624DD3` magic
divide at [`002CC980`](../../_index/ADDRESS-INDEX.md).

`002CBC20` — 35 B, 5 callers (`002C59D0` above): sibling of `002CC630`'s
two-hop — `movsx word[*(0209AC30)+0xDE0]` → `00282DF0` at
[`002CBC32`](../../_index/ADDRESS-INDEX.md) → tail `002CBC50`.

`003BDB30` — 408 B, 4 callers (`002BCB00` above): gated slot scan —
`003BF920()` id (0xFFFF out), requires bits 8+9 of `[ctx+0xD0]`, loops
`00473BB0(0, i, count, &out)` per slot at
[`003BDBEC`](../../_index/ADDRESS-INDEX.md) collecting a matching
`{id, payload}` pair; when found and bit `0x400` is set, `00473CC0` fetches
the pointer and the body writes `word[r13]` + `[r13+8]` then returns 1.

`003BDCD0` — 260 B, 4 callers (`002BCB00` above): the counting twin of
`003BDB30` — same `003BF920` gate, same bits 8+9 requirement, same
`00473BB0` loop at [`003BDD6C`](../../_index/ADDRESS-INDEX.md), but returns
the match count in `esi`/`edi` instead of the record.
### Interior citation — frontier hubs 002CE280, 0029E770, 00249210, 0035BB20 (2026-09-18, SWE2-EC7)

Four hubs the layout schema's per-pane machinery calls:

- **002CE280** (26 B, 4 A-measured callers) — chained `00247730` calls: `[rcx]` then `[rcx+0xC0]` then `[[rcx+0xC0]+0xD8]` — the three-level property walk behind a pane's layout read. First interior anchor [`002CE292`](../../_index/ADDRESS-INDEX.md).
- **0029E770** (27 B, 4 A-measured callers) — writes a word pair `+0xC0/+0xC2` on the `[0209C4A0]` pane-state block — the inline mutation every pane updater performs. Anchor [`0029E77C`](../../_index/ADDRESS-INDEX.md).
- **00249210** (`FFXII.ResourceDataLoading` helper, 265 B, 4 A-measured callers) — the resource-load wrapper the schema's callers reach through `00561390`: nested loops resolve a resource, then `0032E620` commits it and `inc word[rbp+0x18]` bumps the load counter. Anchor [`002492F3`](../../_index/ADDRESS-INDEX.md).
- **0035BB20** (36 B, 4 A-measured callers) — bounded indexed getter: `ecx < word[022D8060]` → `table + ecx*0xC0`, else 0 — the pane-record lookup the schema's accessor callers (`002D5EB0` chain) use. Anchor [`0035BB3D`](../../_index/ADDRESS-INDEX.md).

## SWE2-EC7-18 update (2026-05-15) — `002CC9C0` getter stub trio + `002CD7B0` 9-argument arm

`002CC9C0` (41 B) is the count-scaled forward this page's kind tables use: `ecx <= 1` returns unchanged (`002CC9C3`); larger counts multiply by `0x3C` and run the `0x10624DD3`/`sar 7` reciprocal divide (`002CC9C5`..`002CC9E1`), then `ecx=3` and `jmp 002EFA70` (`002CC9E3`) — the scaled-count arg the shared `002EFA70` continuation consumes.

`002CD7B0` (24 B) is the `0209AC30`-record gate the `00572E10`/`00574E80` menu callers and `002804E0` reach: `rax = [0209AC30]`, `rcx = [rax+0x280]` (`002CD7B0`..`002CD7BE`) — a non-null `+0x280` field forwards into `00244F00` (`002CD7C1`), a null returns. The readiness test the menu arms consult before the `00244F00` dispatch.

## SWE2-EC7-26 update (2026-09-18) — `0024ABC0` / `002B1E20` / `002475D0` / `004051D0` / `002BEFB0` / `002B39A0` layout helpers

`0024ABC0` (20 B) reads `dword[01E0C1D8]` into `xmm0`, `cvtdq2ps`-converts
it, and multiplies by `float[008C5B30]` (0x3B000000 = 1/512) — the
master-scale to normalized-float read the `NobuMsg`/`FontBase`/
`MessageLine`/`MessageWinMaskBottom` builders call four times
(corrected 2026-09-28 per FABLE Y-1: the bytes at `008C5B30` are
`00 00 00 3B`; 1/128 is `008C5B34`, and the `002A70B0` reader's
`FontItalic`-labelled global is `MessageWinMaskBottom`). Interior anchor
`0024ABC8` (the convert).

`002B1E20` (171 B) is the layout duration setter with three arms:
`dl == 0` calls `002B43C0(word[+0x8A] + [rcx+0x28], 3)` and commits the
count to `+0x8C`/`+0x90`, `ax-1` to `+0x8E`, zeroing `+0x9B`/`+0x9D`;
`dl > 0x1E` clamps `+0x9C = 0x1E`, derives `+0xA0 = dl/30` by the
`0x88888889` reciprocal, and when `00248F20()` returns 1 halves `+0xA0`
with a floor of 1; `dl <= 0x1E` stores `+0x9C = dl`, `+0xA0 = 1`.
Interior anchor `002B1E3B` (the `002B43C0` call).

`002475D0` (170 B) is the frame-key field initializer the
`GeneralFrame` reader and `002D66D0` widget entry run: `+0xA3` takes
`dl` with a `0xFF`-to-1 `cmove`, `+0x40` gets `btr 0x1B` + `or 0x180`,
then `+0xA4..+0xAB` are filled from two global bytes —
`byte[01E0C110]` negated twice then doubled twice, `byte[01E0C114]`
the same — an eight-byte signed margin/direction block. Interior
anchor `002475F5` (the `+0x40` flag compose).

`004051D0` (152 B) — reached through its `002BDCE0`/`002BE4F0`/
`002BF690`/`002C0870` layout-reader callers — zeroes the caller's out
mask, then walks the two-slot pointer array at `[02B62D88] + 0xC0`
(slots `+0xC8`/`+0xD0`): each live record whose `byte[+0x130]` carries
`0x10` and whose sign-extended low nibble of `dword[+0x7C]` is `<= 1`
contributes a `byte[+0x135]`-indexed `bts` into the mask; `r10d = 1`
flags a slot that failed the test. Interior anchor `0040521A` (the
`+0x130` bit test).

`002BEFB0` (94 B) — same caller set — hands `[0209AC30] + 8` plus
`rbx + 0x50` and `r9 = rbx` to `002432B0`, then copies four words
`[rax+4]`/`[+6]`/`[+8]`/`[+0xA]` into `[rbx+0x98..0x9E]` when the out
record is non-null. Interior anchor `002BEFCE` (the `002432B0` call).

`002B39A0` (34 B) — reached through `002A5590`/`002A6C40`/`002A70B0` —
is the null-terminated byte find: scans `rcx` for `dl`, returns the
match pointer or 0. The primitive the layout name/string walkers share.
Interior anchor `002B39AC` (the byte compare).

## SWE2-EC7-27 update (2026-09-18) — `002CDAE0` `0x400`-range dispatcher + `002CD800` `+0x280` provider init

`002CDAE0` (549 B) — reached through `00280DE0`/`002C2320`/`00565E00` —
is the MSVC two-table jump dispatcher for ids `0x400..0x4BE`: bounds
`ecx - 0x400 <= 0xBE`, case byte at `[00120000 + i + 0x1ADD60]`, offset
dword at `[00120000 + i*4 + 0x1ADD08]` — twenty arms, most calling
`00254DD0(N)` with N from the case byte (`0x02`/`0x08`/`0x01`/`0x1D`/
`0x03..0x06`/`0x0A..0x11`), several `00264150`-guarded variants, one
`0032A8A0(0x4067)` flag arm, and a `[0209AC30] + 0xB2C` bound check on
the default path. Interior anchor `002CDB16` (the `jmp rcx`).

`002CD800` (126 B) is the `+0x280` lazy provider the `0208EA10` path
runs when `r8 == 1`: cookie-checked, if `[0209AC30] + 0x280` is null it
`00244F50`-creates a `0xC0`-kind object with the `002CE7E0` handler and
the index/flag stack outs, stores it, then `00246AD0(rbx, obj)`.
Interior anchor `002CD84D` (the create call).

## SWE2-EC7-28 update (2026-09-18) — `002CD3C0`/`002C1A80`/`002CA0C0`/`002CA010`/`002969E0` record-table helpers

`002CD3C0` (85 B) is the `002CD3C0`/`00565E00` queue push the
CommandMenu/PartyBlack row names: `[[rip]+0x330]` object's `word[+0]`
count increments, the old count `* 0x20` indexes `[+8]`, `ecx` stamps
`[+0]`, and `002F9860(edi)` twice fills `+0x10`/`+0x18` — a 32-byte
record push returning the record. Interior anchor `002CD3E1` (the count
increment).

`002C1A80` (571 B) is the `002C1A80` -> `002C4720` mist path: a
`00264150` guard first, then `byte[+0xDE7]` selects the arm — 0 checks
`+0x118`/`+0x290`, 1 runs `002C2F90` -> `bts 0xF` key test ->
`00249C60(0x38)` -> `+0x120` flag-`0x20`-gated `00244DD0` ->
`002C5480` -> `+0xDE7 = 2` -> ret 1; 2 runs `002C4220` -> same key
test -> `00249C60(3)` -> triple `+0x120`/`+0x128`/`+0x118` flag-gated
`00244DD0` -> `002CCBA0` -> `+0xDE7 = 0` -> ret 2. Interior anchor
`002C1AC2` (the `+0xDE7` load).

`002CA0C0` (29 B) and `002CA010` (166 B) — reached through
`00280DE0`/`002C2320`/`00565E00` — are the record table's `+0xF0` flag
writers: `002CA0C0` folds `(edx & 1) << 2` into `[[rcx+8]+0xF0]` bit 2;
`002CA010` does the same for bit 1, broadcast across all `word[rcx]`
records (`edx == -1`) or the single record whose `dword[+0] == edx`.
Interior anchors `002CA0C9`/`002CA03E` (the `& ~bit` clears).

`002969E0` (13 B) — reached through `00276D30` — null-guards `rcx` and
stores `rdx` at `+0xB28` — the `+0xB2x` field setter sibling of
`002969F0`. Interior anchor `002969E5` (the store).

## SWE2-EC7-29 update (2026-09-18) — `002922F0` flag sweep + `00292FA0`/`00292B10` `+0x2F8` pair + `0017FFD0` ratio

`002922F0` (151 B) is the flag-id enable sweep `002814E0` runs: two
master gates — `02CA8F94 == 0` unlocks id `0x11`, `02CA96D4 == 0`
unlocks `0xA`/`0x14`/`0xE` — then `0x10` unconditionally; each id is
`002F8040(id)`-tested and `002F83E0(id)`-enabled only when the test
reports it needs enabling (the last `002F83E0` is a tail `jmp`).
Interior anchor `00292302` (the first `call 002F8040`).

`00292FA0` and `00292B10` (92/93 B) — reached through `002C2320` — are
the `*(0209AC30)+0x2F8` lazy pair: `00292FA0` allocates
`00244F50(0xD8, 00293010)` when the slot is empty (the `00293010` init
arm seeds `+0xC0 = 0`, `+0xC8 = 0xFF`, `+0xCC = 0`, `+0xD0` in
{1,4,5,6,7} by sub-kind, `+0x40 &= ~0x800`, `+0x98..+0x9E` from
`01E0C1D8`/`01E0C1DC`, then `00247930(rbx, 0x50)` +
`00246AD0(0208EA28, rbx)` publishes it); `00292B10` tears it down —
`00247570(child, 00916058)` + `00244F00` on the `+0xC0` child,
`00244F00` on the object itself, slot nulled. Interior anchors
`00292FE8`/`00292B50` (the `00244F50` alloc / the `00244F00` self-free).

`0017FFD0` (105 B) — reached through `0029D340` — is the singleton
ratio read the layout readers share: `001DDAB0()` twice — the first
non-null runs `001DD110(obj)` for the numerator else defaults to
`[008C5B38]`; the second non-null runs `001DD120(obj)` for the
denominator else `xorps`+`divss` yields +inf. `divss xmm6, xmm0`
returns the quotient — a numerator/denominator read whose
missing-denominator case returns IEEE infinity rather than failing.
Interior anchor `00180028` (the `xorps`/`divss` divide-by-zero arm).

## SWE2-EC7-30 update (2026-09-18) — `00473BB0` bit-packed record reader + `0027EF50` paired `0x5F` pass

`00473BB0` (213 B) is the reader the `00473BB0(0, i, count, &out)` loop
above names: `ecx` selects a row of the `02CA6C68` bank (`+8` is the
row's record pointer), `edx` an 18-byte record in it, `r8` a bit
position, and `r9` a 0x1C-byte out record. The row's `byte[+1]` kind
lands in `out[+0]`; kind 0 copies `byte[rec+2]` to `out[+4]`, kind 1
unpacks `{byte[+2], word[+4], byte[+3]}` to `out+8`/`+0xC`/`+0x10`.
Then the requested bit — `min(r8/5, 0x32)` by the `0x66666667`
magic-divide, clamped to 50 — is extracted as `1 << (idx & 7)` from
`byte[rec+6+(idx>>3)]` into `out[+0x14]` and from `byte[rec+0xD+(idx>>3)]`
into `out[+0x18]`: two packed bitfields per record, one read each.
Interior anchor `00473C6C` (the `+6` bitfield byte read).

`0027EF50` (76 B) is the paired `0x5F` pass the WorldMap/BlackBand rows
list: `002C9400(0x5F)` opens, `002C9060` runs with the `01E0C3C4`/
`01E0C3C0`/`01E0C3E8` global triplet as its three arguments,
`002C9890(0x5F)` marks, and a tail `jmp 002C9490` replays the same
triplet — a begin/work/mark/work sequence on kind `0x5F` records.
Interior anchor `0027EF97` (the `jmp 002C9490` tail).
## SWE2-EC7-31 update (2026-09-18) — `002C9890` `+0x2C8` kind gate

`002C9890` (34 B) is the guard shim the `0027EF50` paired pass calls
as its mark step: on the `0209AC30` bank it loads `qword[+0x2C8]`;
a null record returns immediately, and only when the record's
`word[+0x44]` differs from the argument does it tail-dispatch
`jmp 00247930` — a kind-mismatch filter in front of the bank
walker. Interior anchor `002C98AB` (the `jne 00247930` tail).

## SWE2-EC7-34 update (2026-09-19) - `002CE370`

`002CE370` (950 B) is a layout command handler - `[rdx]` switch `{1, 0xB, 3}`, 0x468 frame, `0057C340` then a `call rax` indirect dispatch, `002F9860`/`002B4090`/`005C5230`. Interior anchor `002CE3F0` (the `0057C340` call).

## SWE2-EC7-38 update (2026-09-19) - `002C4220`

`002C4220` (473 B) is a layout-parameter body - `0209E65C`/`0209AC30`/`01E0CF88`, `002C54B0` quadruple plus `002C3D70` pair and `001E0A10`/`00249C60`/`002C53B0`. Interior anchor `002C4277` (an `001E0A10` call).

## SWE2-EC7-39 update (2026-09-19) - `002CE7E0`

`002CE7E0` (415 B) is a layout-parameter body - `01E0C1D8`/`01E0C1DC`/`01E0C238`/`0209AC30`/`0209E630`/`02CA972C`, `0024A5A0` triple plus `00577BD0`/`002D8C80`/`00247570`/`00247930`. Interior anchor `002CE827` (a `0024A5A0` call).

## SWE2-EC7-42 update (2026-09-19) - `002C99E0`

`002C99E0` (321 B) is a layout-parameter body - `00917070`/`01F44830`/`0208EA28`/`0208EA38`, `00244F50` triple/`00246AD0` pair/`00247570`/`00246AC0`/`00808C40`. Interior anchor `002C9A44` (a `00244F50` call).

## SWE2-EC7-43 update (2026-09-19) - `0029DDF0`

`0029DDF0` (292 B) is a layout-parameter body - `0209C498`, `0029DF20`/`0029E3B0`. Interior anchor `0029DF04` (a `0029DF20` call).

## SWE2-EC7-44 update (2026-09-19) - `0029DCE0`

`0029DCE0` (258 B) is a body - `002468A0`/`0029DFB0` pair. Interior anchor `0029DD25` (a `002468A0` call).

## SWE2-EC7-44 update (2026-09-19) - `002CC660`

`002CC660` (253 B) is a body - `00282DF0`/`00282FA0` pair. Interior anchor `002CC6E9` (a `00282DF0` call).

## SWE2-EC7-45 update (2026-09-19) - `002CBC50`

`002CBC50` (242 B) is a body - `00282DF0`/`00282FA0` pair. Interior anchor `002CBCC9` (a `00282DF0` call).

## SWE2-EC7-46 update (2026-09-19) - `00293010`

`00293010` (232 B) is a body - `00246AD0`/`00247930`. Interior anchor `002930DC` (a `00246AD0` call).

## SWE2-EC7-46 update (2026-09-19) - `00248410`

`00248410` (230 B) is a call-free resolution publisher - reads `01E0C1D8`/`01E0C1DC` (512x448), scales by `0090030C` into `0208ECC0`/`0208ECC4`, then writes `+0x98`/`+0x9C`/`+0x9E` into each `0208EA20`..`0208EA38` record. Interior anchor `00248426` (the `cvtdq2ps`).

## SWE2-EC7-47 update (2026-09-19) - `002D0410`

`002D0410` (213 B) is a body - `00248F40` single call. Interior anchor `002D0446` (the `00248F40` call).

## SWE2-EC7-48 update (2026-09-19) - `002C5EC0`

`002C5EC0` (202 B) is a body - `002D02A0` single call. Interior anchor `002C5F6D` (the `002D02A0` call).

## SWE2-EC7-51 update (2026-09-19) - `002DD5D0`

`002DD5D0` (172 B) is the persistent-record init `002D8994` runs - `003649A0`/`00365B20`. Interior anchor `002DD5E7` (a `003649A0` call).

## SWE2-EC7-51 update (2026-09-19) - `0024AC30`

`0024AC30` (173 B) is a body - `0016D6A0`/`0032E400`/`0032E520`/`0032E620`/`0037B330`/`0037B450`. Interior anchor `0024AC4C` (an `0016D6A0` call).

## SWE2-EC7-51 update (2026-09-19) - `0029D290`

`0029D290` (172 B) is a body - `00244F50`/`00246AC0`/`00247570`. Interior anchor `0029D2BB` (a `00244F50` call).

## SWE2-EC7-52 update (2026-09-19) - `0029E3B0`

`0029E3B0` (759 B) is a layout-parameter body - `0209C498` fields, `0029DF20`/`00246AD0`/`0029CD90`/`0029DCE0` calls. Interior anchor `0029E40F` (a `0029DF20` call).

## SWE2-EC7-53 update (2026-09-19) - `002C54B0`

`002C54B0` (425 B) is a call-free `[rcx+0x7A4]`-indexed backward pointer-table scan - `[rcx+rax*8+0xC0]` chain walked down for `[rax+0x40]`-bit-0 entries. Interior anchor `002C5508` (the flag read).

## SWE2-EC7-55 update (2026-09-19) - `0029DFB0`

`0029DFB0` (244 B) is a `002468A0`-pair body - `002B3050`/`003FFAB0` plus `0209C498`. Interior anchor `0029E018` (a `003FFAB0` call).

## SWE2-EC7-56 update (2026-09-19) - `002C53B0`

`002C53B0` (196 B) is a layout-parameter body - `002D4840` single call plus `00916D30`/`0209AC30`. Interior anchor `002C5411` (a `002D4840` call).

## SWE2-EC7-59 update (2026-09-19) - `0029CD90`

`0029CD90` (164 B) is a layout-parameter body - `002B3050`/`002B4540`. Interior anchor `0029CDBB` (a `002B3050` call).

## SWE2-EC7-61 update (2026-09-19) - `003F1430`

`003F1430` (153 B) is a cursor-metric reader - `003F12E0` single call. Interior anchor `003F1440` (a `003F12E0` call).


## SWE2-EC7-70 update (2026-09-19) - `002D4840` two-phase layout body measured

`002D4840` (127 B) is the body `002C53B0` calls singly: `002D4D60(rcx) ==
1` first runs `002D4A40(rcx, 4, 0, 0)`; then when `r9d` is set it resolves
`[+0xC8]` and computes `(word[+0xF4] + word[+0xF2]) * byte[+0xEC] +
byte[+0xEE] + byte[+0xED]` into `r8`, calling `00247510(record, 0x8000,
r8)` - the fixed-point push the force-fight page names.
Interior anchor `002D4892` (the `imul edx, eax` product).

## SWE2-EC7-72 update (2026-09-19) - `002D4A40` scroll-delta commit measured

`002D4A40` (291 B) is the scroll/clamp body the layout callers run:
`r15 = -(word[+0xEA] * movsx byte[+0xED])` and
`r14 = -(word[+0xF2] * word[+0x100])` are the two deltas; when the
`+0xC0` record's `[+0x98]`/`[+0x9A]` already equal them and `edx == 1`
they are committed back with `byte[+0x80] & ~1`; otherwise
`002D1870(rcx)` runs, `ebx & 0xFFFF0FFF` selects an op - `3` or `9`/`10`
pass `r9 = 0`, `7` sets `+0xE0` bit `0x18` and passes `5` - then
`(result * 0x3E8)` is magic-divided by 55 (`0x88888889`/`>>5`+sign) into
`rsp+0x20`, `002468A0(rec, r15, r14, r9)` runs, `[rec+0x94]` decrements,
and the `002D1870` result returns.
Interior anchor `002D4B05` (the `imul ecx, ebp, 0x3e8` scale).

## SWE2-EC7-73 update (2026-09-19) - `003DFBB0` + `003DFB50` bounded record readers measured

`003DFBB0` (43 B) is the bounded word read the layout callers share:
record non-NULL with `byte[+7] >= 0x32`, `edx` nonzero and below
`word[+8]`, and `edx - 1 <= 8` returns `word[rcx + edx*4 + 0xC]`; every
guard failing returns 0 - the `+0xC`-strided element fetch.
Interior anchor `003DFBD2` (the `+0xC` indexed read).

`003DFB50` (90 B) is the nested element getter: same `+7 >= 0x32`
guard, then `r8d < word[+0xC + rdx*4]` resolves
`rbx = rcx + word[+0xA + rdx*4] + r8d*16`; a non-NULL hit is validated
through `0032A8A0(movsx word[rbx+0xA])` and NULL-substituted on zero -
the two-level record element fetch the config/layout bodies run.
Interior anchor `003DFB91` (the `0032A8A0` validator call).

## SWE2-EC7-74 update (2026-09-19) - `003938B0` + `0037B450` + `0037B330` release sweep and flag pair measured

`003938B0` (74 B) is the release-and-clear sweep: for `rdi = edx`
elements at `rbx`, each non-NULL pointer goes through `003697F0` then
the slot is zeroed - the layout family's bounded teardown.
Interior anchor `003938D8` (the `003697F0` release call).

`0037B450` (31 B) writes `bl` to `02ADD930`, runs `0037B3D0()`, then
writes `bl` to `02ADD931` - the flag-run-flag triple the config/layout
bodies drive.
Interior anchor `0037B45E` (the `0037B3D0` call).

`0037B330` (22 B) is the paired reader: `02ADD931` set returns 4,
otherwise the `02ADD930` byte - the mode the writer commits.
Interior anchor `0037B337` (the `02ADD930` read).

## SWE2-EC7-75 update (2026-09-19) - `002C2240` gated two-call pair measured

`002C2240` (52 B) is the gated pair the layout bodies call:
`ebx = 0027F360(edi)`; only when it returns 1 does `00249C60(0x51)`
then `002C2C50(edi)` run - the success-only follow-up.
Interior anchor `002C225B` (the `00249C60` call).

## SWE2-EC7-76 update (2026-09-19) - `002C2200` + `0027F2E0` + `002732E0` layout helpers measured

`002C2200` (52 B) is the `002C2240` sibling gate: `ebx =
0027ED10(edi)`; only on return 1 do `00249C60(0x51)` then
`002C2C50(edi)` run - the same success-only follow-up shape.
Interior anchor `002C221B` (the `00249C60` call).

`0027F2E0` (121 B) is the `0209AC30` `+0x400` state commit: `ebx` is
1 when bit 11 stands, else `0xC8`; `002C98C0(ebx)`, `00250F30()`,
`002CC960(ebx)` run in order; then `+0x400` bit 9 clear stores byte
2, set stores `bit10 ? 2 : 1`, and bit 11 is cleared - the
flag-state advance the layout callers drive.
Interior anchor `0027F306` (the `002C98C0` call).

`002732E0` (53 B) is the four-slot find: `ebx` 0..3 calls
`0035BB20(ebx)` and returns the record whose `+4` equals `edi`, else
0.
Interior anchor `002732F2` (the `0035BB20` call).

## SWE2-EC7-77 update (2026-09-20) - `002C2C50` + `0024AB60` layout follow-ups measured

`002C2C50` (125 B) is the follow-up the `002C2200`/`002C2240`/
`002C2320` gates call on success: `rbx = [0209AC30]+0x110`; if the
block exists `002C56F0(rbx)` runs, then `[rbx+0x148]` nonzero CLEARS
bit 0 of `[[rbx+0x60]+0x20]+8` and zero SETS it - a parity toggle -
before `002C1FF0()`, `002C2CD0(edi)` and `002CC2A0()` run in order.
It tails `002527B0(6, 4, movsx word[*(0209AC30)+0xDE0])` - the same
`+0xDE0` selector the `0027F210` fill writes.
Interior anchor `002C2C72` (the `002C56F0` call).

`0024AB60` (35 B) is the `02091094` consume-once notify: if the flag
stands it runs `0037B450(0)` (the measured flag-clear writer), then
stores 0 into `02091094` - a one-shot edge, not a level.
Interior anchor `0024AB6F` (the `0037B450` call).

## SWE2-EC7-78 update (2026-09-20) - `002CC2A0` nine-slot layout pass measured

`002CC2A0` (584 B) is the third and largest call in the
`002C2C50`-family sequence: it works on `[0209AC30]+0x2E0` (rbx).
`[rbx+0x168] & 0xF0000` picks the dimension pair (`+0x160`/`+0x162`
vs `+0x164`/`+0x166`); `r8d` is `byte[*(0209AC30)+0xB2A]-1 +
byte[+0xB2B]`, or `byte[+0xB2C]-1` when `+0xD3C:0x10` stands; `esi =
dim - r8d*slotsize`. The body then runs a 9-iteration loop over the
8-byte-strided `[rbx+0x118]` slot list: per slot `rbp = [r15-0x48]`,
`rdi = [r15]`; `00282DF0([rbp+0xD4])` fetches the record; flags
`0xC00000`/bit8/`0x300000` gate the populated arm, where
`+0xD3C:0x10` adds a `00282FA0` veto, `word[r14+0x60] >= 0` runs
`00247870(rbp,1)` + re-fetch + a `0..0xF` clamp of `[rax+0x60]`,
copies `byte[[rax]+0x20][idx*8+7]` into `+0x39`, writes `+0xA` and
`+0x98`; the empty arm runs `00247870(*,0)`. `esi += r12d` and
`byte[+0x168]` counts passes. Tail: `002CAFE0([rbx+0xC0], ...)`,
then `[rbx+0xC8]` gets `+0x98`/`+0x9A` written from the hi/lo words
of its `[+0x98]`, and `002CBA50` runs.
Interior anchor `002CC35F` (the `00282DF0` call).

## SWE2-EC7-85 update (2026-09-20) - `004043B0` + `00403180` list passes measured

`004043B0` (279 B) is the per-element oscillation pass the layout
callers run: for each `[rbx+0x98]`-linked record with `+0xA8` bit 0,
`cvtsi2ss(global_dword) * c1 / c2` feeds `00861F0E`, the result
scales into a stack vector by `c3`/`c4` + `c5`, and
`00274CA0(rec, &vec, [rec+0x90])` applies it - stack-cookie framed.
Interior anchor `0040444C` (the `00861F0E` call).

`00403180` (419 B) is the `[rbx+0x60]`-linked per-element animator:
`word[+0x4E]` bits 0/1/2 drive the `+0x4C` counter (+-0x10, clamped
against `0x80`/`0x40`/`edx<<5`), `00254A10()` selects which pair of
float steps moves `+0x38` toward `0.75`/`0.9`/`1.0`, and `+0x50`
counts +-0x10 toward `0x100` or 0 by whether the element is the
`rdi` anchor.
Interior anchor `0040324D` (the `00254A10` call).

## SWE2-EC7-86 update (2026-09-20) - `003FE410` lazy registry record measured

`003FE410` (123 B) is the one-time record install the layout
callers run: when `[0209AC30]+0x138` is null it packs `ecx` into
a stack descriptor, calls `00244F50(0x118, 003FE5D0, &desc)` so
the `003FE5D0` callback builds the 0x118 record, stores it into
`[0209AC30]+0x138`, and registers it via
`00246AD0([0208EA28], record)` - all under a stack cookie.
Interior anchor `003FE457` (the `00244F50` builder call).

## SWE2-EC7-88 update (2026-09-20) - `003CA140` + `003BF8E0` + `003BBFB0` measured

`003CA140` (100 B) is the mode-code registration the layout
callers run once (`[02B47750]` gates the init): `ecx` selects
the `0x1B5`/`0x1B6`/`0x1B7`/`0x1B8` code written to
`[02B4774C]` with `[02B47748]` armed - a four-way table write.
Interior anchor `003CA166` (the `0x1B7` arm).

`003BF8E0` (51 B) is the byte-field fetch over the
`[02B457E0+0xE8]` table: the `word[+8]`-relative index list's
`dword` bound gates `ecx`, and `byte[table + ecx*8 + 4]` is
returned - the same index geometry `003C02B0` writes through.
Interior anchor `003BF90C` (the byte read).

`003BBFB0` (425 B) is the `02B457E0` table teardown the layout
callers run: `byte[+0xC8]` is set to 2, then the `+0xD8`/
`+0xE0`/`+0xE8`/`+0xF8`(+`0x108`) slots are released through
`003697F0` under their `+0xD0` flag bits (8 / 0x10 / 0x20 /
4+0x40), each flag cleared and slot zeroed; the `+0xD0` bit-7
arm runs `0037F050`/`0037F160`/`0037E4F0` liveness checks, and
the accumulated flag gates a final `00245020(table)` destroy.
Interior anchor `003BC004` (the first `003697F0` release).

## SWE2-EC7-92 update (2026-09-20) - `0037E5B0` + `0037E4F0` measured

`0037E5B0` (426 B) is the layout-record builder the `005789D0`
caller runs: index `ecx` bounds against the `+0xA` word count of the
~~`02A8D480`-rooted~~ `02AED490`-rooted *(corrected 2026-09-26 (FABLE, Claude Opus 5.5): the instruction reads `02AED490`, the hunt list's
table owner; see the save payload page, `FG-1`)* `+0xC8` table, `002F9920` resolves the entry's `+0xC`
id into `out+0`, `+0x10` decodes to `out+8` (`>>8 & 0x3FF`), `out+0xA`
and `out+0xB` (both `>>0x14`), prior entries with a matching low byte
increment `out+0xC`, and the `+0xD0` word-table name lookup resolves
`0xFFFF` to the `02CB128` fallback string before returning 1.
Interior anchor `0037E5FE` (the `002F9920` call).

`0037E4F0` (190 B) is the mode setter `003BBFB0` calls: when the
`02A8D470` global's `+0xE0` bit 7 is clear it runs `0037F860`, stores
the argument at `+0xC0`, writes state byte `+0xE5` = 4 on success
(3 on failure) and calls `00244F00`; a non-null argument then takes a
vtable call through `[rbx]` with a 0x10-sized stack record.
Interior anchor `0037E531` (the `0037F860` call).

## SWE2-EC7-99 update (2026-09-20) - `002D9B00` + `002D04F0` + `002D02A0` + `002CDE50` measured

`002D9B00` (317 B) is the display-list close `0029E840`
calls: `(write - read - 0x20) >> 4` counts the queued
entries, `0x11000000` plus `count << 16 | 0x6C008000` seal
the header, and the count-8 fast path republishes through
`0016D6A0`/`003A1DB0`; otherwise the entry at `[rax-0xF4]`
gains bit 0, `0x6C0380F0` and the
`0x1000000000000002`/`0xE` record go out, `rdx+0x80` and
`rdx+0x78` copy as `0x47`- and `0x42`-tagged records,
`002DD350` runs the shrunk-argument publish, and
`00181910`/`001816B0`/`00181330` close out - the
submit-and-link tail of the layout command stream.
Interior anchor `002D9C14` (the `002DD350` call).

`002D04F0` (122 B) is the flag-word write `002C1CC0` and
`002C1D30` call: `[+0xC0]` loses its low byte
(`& 0xFFFFFF01`) then gains `(((r8 & 3) << 4 | (r9 & 0xF))
<< 2 | 1)`, `byte[+0xA0]` or `byte[+0xA1]` (chosen by
`r8 >= 1`) lands at `+0xC4` with `dx - ax` at `+0xC8`,
`0208F570` stamps `+0xD0`, and `arg * 0x3C` scaled by the
`0x10624DD3`/`sar 6` ~1/1000 fixup lands at `+0xCC` - the
packed mode/duration record the layout arms set.
Interior anchor `002D0513` (the `or` into `+0xC0`).

`002D02A0` (30 B) is the class-bitmap probe `002C59D0` and
`002C5EC0` call: `byte[rcx]` must sign-read non-negative
(`<= 0x7F`) and `byte[rcx+1]` must differ from `0xFF`,
then `bt edx, eax` tests the class bit - the
two-byte-gated bitmap membership test the layout scan
applies.
Interior anchor `002D02B0` (the `bt`).

`002CDE50` (39 B) is the resolve-and-forward `00281ED0`
and `00565E00` call: `002CD920` maps `edx` to an index, a
negative result returns quietly, otherwise
`(zx(ax), zx(bl))` tail into `00252D40` - the
lookup-then-dispatch trampoline the layout verbs share.
Interior anchor `002CDE6C` (the `00252D40` tail jmp).

## SWE2-EC7-100 update (2026-09-20) - `002CB7F0` + `002C9BF0` + `002C9400` + `002C56F0` measured

`002CB7F0` (89 B) is the bit-0 toggle `002C59D0` and
`005691E0` call on the `0209AC30` `+0x2E0` object:
`dword[obj+0xC0 + 0xF0]` flips its low bit toward `ecx`,
then `002CAFE0` runs with `byte[+0x168]` and a stacked 1 -
the flag-mirror-and-notify pair the layout arms drive.
Interior anchor `002CB82B` (the `xor` fold into `+0xF0`).

`002C9BF0` (617 B) is the record spawn `00281AE0`,
`002C2320`, `00565E00`, `0056F5F0` and `0057B400` call:
`002432B0(rcx+0x50, [0209AC30]+0x30, rdi, 3)` builds the
row set, a stack record carries the scaled extents
(`dword[0209F624] + arg` and `word[r13+0x10]` through
`mulss` chains), `002D14E0` allocates the child record
(`+0xE4` bit 1 set, `+0x98`..`+0x9E` seeded from `r13`'s
`+0xC`/`+0xE`/`+0x10` words plus the computed `r14w`),
`00244960` links it, and when `rsi == 0` a `rbx`-count
loop posts `0xF8` commands through `00244F50` to fill the
`0x20`-stride rows and `00244960`s each product onto `r15`
- then the summed `+0x98`..`+0x9E` extent lands on `rdi`
and `00247570` publishes `02317098` - the
build-link-fill-finalize sequence the layout spawns run.
Interior anchor `002C9DAB` (the `00244F50` post inside
the fill loop).

`002C9400` (34 B) is the conditional dispatch `0027EE80`,
`0027EF00`, `0027EF50`, `002804E0` and `005679D0` call on
the `0209AC30` `+0x2B8` object: a null object returns;
`movsx word[+0x44] != edx` jumps to `00247930` - the
word-gated forward the layout arms share.
Interior anchor `002C9415` (the `+0x44` compare).

`002C56F0` (278 B) is the subrecord fill `002C2C50` and
`002C59D0` call: under the `00254A10`/`00264150` gates,
three `00282DF0` resolutions of `word[*(0209AC30) + 0xDE0]`
feed `002D0280`/`002D02C0`/`002D03B0` passes on the
`+0xC8` subrecord, the last resolution's `[+0x44]` lands
at `+0x148` and `bl` at `+0x14C`, and a quiet
`00254A10` afterwards runs `002D4930([rsi+0xC0], 1 or
movsx bl)` - the orchestrated populate the layout
records receive.
Interior anchor `002C5768` (the first `002D02C0` call).

## SWE2-EC7-101 update (2026-09-20) - `002D0280` + `002CAFE0` + `002A0180` measured

`002D0280` (27 B) is the `0xFEFE` fill `00283E40` and
`002C56F0` call: `rep stosd` of `edx` dwords at `rcx` -
the poison pass the `+0xC8` subrecord refresh runs
before repopulating.
Interior anchor `002D028E` (the `0xFEFE` constant).

`002CAFE0` (361 B) is the four-link flag pass `002CB7F0`,
`002CB8D0`, `002CB9C0` and `002CC2A0` call: bit 0 of
`[+8]` is cleared on the `[rbx+0x60]` node's four links
(`+0`/`+8`/`+0x10`/`+0x18`), and when `dword[+0x40]` bit 0
is set, `edi > 1` and `dword[+0xF0]` lacks bit 1, two of
the four re-arm bit 0 (which pair follows `+0xF0` bit 0),
`002DD7E0` computes a value broadcast into `+0x24`..`+0x34`
on the `+0`/`+8`/`+0x10` links, and a null stack flag
derives `word[+0xEE] = -(di-1)*si` plus `+0xC`/`+0xE`
fields on the `+0x10` link - the clear-enable-broadcast
sequence the notify arms drive.
Interior anchor `002CB0B2` (the `002DD7E0` call).

`002A0180` (692 B) is the three-segment layout composer
`0029E840` and `0029ED50` call: `r14d` units split across
head/middle/tail `002D8D40` emits - when the stack flag
is set, `word[rbx+4]` and `word[rbx+0x14]` bound fixed
margins around an `r14d`-wide middle; when clear and
`r14d - word[+0x14] - word[+4]` is nonnegative the
segments take fixed margins; negative input instead runs
two `idiv` proportional shares
(`margin * r14d / (head + tail)`) and merges the pieces
through the `rsp+0x50` record with adjusted `+0x50`/`+0x54`
words - the fixed-versus-proportional splitter the
layout walks run.
Interior anchor `002A03BC` (the proportional-path
`002D8D40` call).

## SWE2-EC7-106 update (2026-09-20) - `00251D90` measured

`00251D90` (105 B) is the conditional
one-shot register `002289D0`,
`0027FB70` and `003EEEC0` call: only
when `020927F0` is null does it build
a stack descriptor - `word = cx`,
`dword = edx`, `dword = r8d`, a count
out-slot and a `0x10`-byte buffer
pointer - and runs `00244F50(0x140,
002509D0, &desc)`; a live record
skips straight to the `00808C40`
cookie check - the deferred install
the layout callers rely on.
Interior anchor `00251DDD` (the
`00244F50` call).

## SWE2-EC7-107 update (2026-09-20) - `002472A0` + `00244070` measured

`002472A0` (95 B) is the conditional
float publish `005565E0` and
`0055A340` call: null `rcx` or
`byte[+0x80] & 7` armed answers 0;
when `float[+0x84]` already equals
`xmm1` it answers 0 too. Otherwise
`+0x80` gains bit 3, bits `0x3C00`
are rewritten from `r8d & 3`,
`float[+0x84] = xmm1`, and
`002418F0(rcx)` fires - the
change-only update the layout arms
share.
Interior anchor `002472D3` (the
`0xFFFFC3FF` mask).

`00244070` (254 B) is the tree-entry
decode `002A4430`, `002A86A0` and
`002D1750` run against `0208EA90`:
the `[+0x20]` node's `word[+0x44]`
selects a `+0x20` word-table offset,
`r9d` picks an 8-byte entry whose
words land at `[rsp + 0x40..0x46]`
(low `0xFFF` and `>> 0xC & 0xFFF`),
`byte[+7]`'s high nibble indexes a
`word[+0x12]` byte table and its low
nibble is added into
`byte[rbp + 0x5C]`; then
`002D8BB0(rbp, 1)`, a
`002D8CB0(rbp, 0208EA90, &rect,
esi - ((dword[+4] >> 1) & 0x7FF))`
with `edi - ((dword[+4] >> 0xD) &
0x7FF)` folded in, and
`002D8BB0(rbp, 0)` - the
bracketed rect emit the layout arms
share.
Interior anchor `0024409C` (the
`word[+0x44]` select).

## SWE2-EC7-108 update (2026-09-20) - `00229DA0` measured

`00229DA0` (51 B) is the
mode-keyed constant select
`00247AE0` and `0029CF30` call:
`ecx` 2, 3 or 4 answers
`float[00908D50]` (1.1547),
`float[00908D54]` (1.3333) or
`float[00908D48]` (1.0972);
anything else answers `1.0` - the
three-way scale lookup the layout
arms share.
Interior anchor `00229DAF` (the
`1.0` default load).

`0057E210` (212 B) is the `005528C0`-family widget message sender: under the stack cookie it first calls `00368250` into a 4-byte out record and, when that returns nonzero, `[rcx+0x18]` bit 0 is set, and `[rcx+0x10]`'s first two words match the reply, clears that bit; it then packs a `{w,w,w|0x100,si,w,arg-w,0}` 0x18-byte message and calls `00368360` then `00245510` on `rdi` — a conditional flag-clear followed by an unconditional send pair.

Interior anchor `0057E240` (function `0057E210`).

`0057E190` (122 B) is the flag-driven pointer walker `005528C0` uses: if `[rcx+0x10]` is null it is set to `[rcx+8]` and the function returns; otherwise each of `r8b` bits `0x80`/`0x20`/`0x10`/`0x40` chases `[cur+0x18]`/`[+0x20]`/`[+0x28]`/`[+0x30]` respectively, and every non-null hop both stores the new pointer into `+0x10` and sets `[rcx+0x18] |= 3` — a multi-link reseater with a dirty flag.

Interior anchor `0057E1B0` (function `0057E190`).

`0057E090` (249 B) is the rect-edge clamp `005528C0` applies: when `[rcx+0x18]` bit 1 is clear or `[rcx+0x10]` is null it just writes `*rdx = 0`; otherwise it reads the `+0`/`+4` dwords of that record, adds the `r8`/`r9` window offsets, measures the `rdi` rect's `movsx` word edges, and writes the per-axis overshoot into `r10`; each nonzero overshoot is then divided by 8 with a minimum magnitude of 1 (sign preserved via `cdq`/`idiv`) — a screen-edge overflow-to-step converter.

Interior anchor `0057E157` (function `0057E090`).

`0057CD00` (61 B) is the `+0x5B8` word-table lookup `00566680` (`ItemSort…`) runs: `movzx`'s the count at `[rcx+0x636]`, walks 0x10-stride records comparing each `+0` word against `dx`, and returns the index of the first match, 0 otherwise — a keyed slot find over the widget's word array.

Interior anchor `0057CD23` (function `0057CD00`).

`0057C320` (26 B) is the global-object forwarder `002CDF20` and `00566680` share: loads `[[0209AC30] + 0x328]`, `movzx`s both word args, and tail-jumps to `0057C140` — a three-line re-dispatch onto the shared UI object's method.

Interior anchor `0057C335` (function `0057C320`).

`0057C140` (475 B) is the append-and-relayout `0057C320` forwards onto the shared UI object: returns unless `rcx` non-null and byte `[+0x636]` < 8 (an eight-slot cap); `002F9860(dx)` resolves the text into slot `+0x5B0 + count*0x10` (16-stride records: `+0` text ptr, `+8` = `r8w` tag word, `+0xC` dword `|= 1`), then `count` is incremented; `002B3280` measures into a stack record and the geometry pass rewrites `[+0xC0]`'s `+0x98`/`+0x9A`/`+0x9C`/`+0x9E`/`+0xEA` words (clamping against its own `+0x9C` and the parent's) before `002D48C0` and a final centering pass halves `0x200`/`0x1C0` minus extents into `+0x98`..`+0x9E` of `rsi` — append, measure, re-center.

Interior anchor `0057C1C3` (function `0057C140`).

`00577BD0` (81 B) is the `02CA9730` thunk `002CE7E0` invokes: when the global and its first qword are both non-null it calls `[02CA9730]`'s stored fnptr with a `{0x10, 0,0,0,0}` stack record — a fixed-shape event poke through an installed callback, silent when nothing is installed.

Interior anchor `00577C0D` (function `00577BD0`).

`00274CB0` (1577 B) is the apply body `00274CA0` calls as `00274CB0(rec, &vec, [rec+0x90])`: `xmm7 = 1.0 / (r9 - 1)` normalizes the step, `00276320` consults the mode, `[02EBEFF0]` indexes the `02EBEFC0` triple-width records, and `00202C90` x7, `00202B70` x2, `00203080` x2, `00202FE0` x2 plus the `00181560`/`00181910`/`001816B0`/`00181870`/`00181890`/`00181930`/`00181350`/`00181330` emit battery with `002724A0` produce the interpolated record set.

Interior anchor `00274D20` (function `00274CB0`).

`002C2F90` (1110 B) is the record-table walk `002C1A80` runs: `0209AC30 + 0x120` supplies the list head (null early-out), `0209E65C` ticks the sequence, and `001E0A10`, `002C3C80` x4, `002C2DA0` x2, `00249C60`, `002C3B90` walk the entries into `r15d` - the layout family's counted list pass.

Interior anchor `002C3071` (function `002C2F90`).

`00405C20` (1162 B) is the flag-gated gauge draw `00405310` runs: `[rcx+0x130]` bit 8 and `test 0x40` gate the modes, `[rcx+0xD0]`/`[rcx+0xE4]` feed the state, `0029E840` x2 binds the shader material, `0035D460`, `002DAF30`, `002D9DB0`, `002DAC70` x2 and `002D8D10` x2 run the textured-quad and item helpers - the boss-gauge draw chain's gated body.

Interior anchor `00405C7C` (function `00405C20`).

`002CEFD0` (1005 B) is the `ScrollMark` arm's worker `002CEB40` runs: `00250E90` x2, `00248F40`, `00248A90`, `00249810` x2, `0024AA00` x2, `0024A440` x2, `0024A1D0` x2 with `00181610` x2 and `002CEF10`, cookie-checked - ~~the scroll-mark layout's per-row emit~~. **Corrected 2026-09-30 (SWE2-EC7, SWE2-DATA's `.as7` decode):** it is the character-silhouette group decode: it decodes two runs of `0x102` `char_silhouette` pages through `0024AA00` (pages `[g·0x204, g·0x204 + 0x102)` into its `+0xE0` buffer, the next `0x102` into `+0xE8`), with `g` picked by the signed byte `+0x10D` through the table `{0, 1, 3, 2, 4, 5}` ([rc22-34-resource-readers-0930](../../_index/candidates/rc22-34-resource-readers-0930/README.md) §2; consumer check [ec7-as7-roles-0930](../../_index/candidates/ec7-as7-roles-0930/README.md)).

Interior anchor `002CF2CE` (function `002CEFD0`).

`0024AA00` (293 B) is the ~~scroll-mark emit~~ `.as7` page walker `002CEFD0` calls twice and `00292390` once: ~~`byte[rcx+2]` and `byte[rdi+3]` key the row fields and `00248500` performs the layout step - the per-row emit's single-callee helper~~. **Corrected 2026-09-30 (SWE2-EC7, SWE2-DATA's `.as7` decode):** `0024AA00(as7, out, first, n)` reads the page count as the big-endian u16 at `+2`/`+3`, takes the tail block at `as7 + be32[+4]`, and calls `00248500` once per page on `as7 + be32 offsets[i]`; a 0 return fails the walk ([rc22-34-resource-readers-0930](../../_index/candidates/rc22-34-resource-readers-0930/README.md) §1).

Interior anchor `0024AAF4` (function `0024AA00`).

`002CEF10` (143 B) is the `ScrollMark` worker `002CEB40` and ~~the emit~~ `002CEFD0`/`002CF440` call (*Corrected 2026-09-30, SWE2-EC7: `002CEFD0` is the silhouette group decode, not an emit*): the `rip+0x1DCBD13` global's `+0x308` qword supplies the object whose `+0xE0`, `+0xF0`, `+0xF8` fields are walked, `003697F0` x2 and `0024A680` x2 running the steps - the scroll-mark layout's record accessor.

Interior anchor `002CEF3C` (function `002CEF10`).

`00281AE0` (797 B) is the `0x288` widget proc `00280DE0` opens with beside `00281E00`: `00326BB0`, `00283690`, `002CD4D0`, `0032A8A0` x6, `002CD3C0` x9, `00254A50` x2, `00861EC0`, `00283270`, `002826F0`, `002CD510`, `00254E80`, `00252610`, `002C9BF0`, `002CD440` x2, `002CA0E0` x2, `00249580`, `002920C0`, `002CEFA0`, `002CEAE0`, `00249410` and `0024A5A0` under the cookie check - the proc's dense emit stage.

Interior anchor `00281B52` (function `00281AE0`).

`002CD510` (317 B) is the emit stage `00281AE0` and `00565E00` call: `002CD650` prepares, then `00252D40` x14 and `00252D10` x8 with `00264150` run the row's field writes - the `0x288` proc's `00252D40`-dense helper.

Interior anchor `002CD514` (function `002CD510`).

`002CD440` (42 B) is the index-search `00281AE0` and `00565E00` call: `word[rdx]` bounds the `[rcx+8]` array, the loop scans `dword[rax]` for `r8d` and returns the matching ecx or falls out - a call-free slot finder.

Interior anchor `002CD451` (function `002CD440`).

`002CA0E0` (40 B) is the accumulator `00281AE0` and `00565E00` call: `[rcx+8]` supplies the object, `word[+0x98] += dx`, `word[+0x9A] += r8w`, then `word[+0xEC] = dx`, `word[+0xEE] = r8w` - a two-field add-and-store, call-free.

Interior anchor `002CA0E9` (function `002CA0E0`).

`002826F0` (842 B) is the emit stage `00281AE0` calls: `0031C4C0`, `00252F40` x2, `0020E600` x2, `00252FA0` x4, `0031C5D0`, `0016D6A0`, `002CCA00`, `00317B70` and `00306340` under the cookie check - the same call family as the license-board cell builder, here driving the `0x288` proc's grid emit.

Interior anchor `002827A4` (function `002826F0`).

`002C1FF0` (513 B) is the teardown-rebuild `002C2C50` calls: `0209AC30`'s `+0x130` object gives `rbx`, its `+0xC0`/`+0xC8` chains are freed through `00244F00` and cleared, then a `0x100`-byte request on the `0028xxxx` data runs `00246AD0`/`00247570`/`00282DF0`/`00283E40`/`002847C0`/`00244F50`/`00808C40` - the layout's widget reset.

Interior anchor `002C2053` (function `002C1FF0`).

`00309C40` (504 B) is the indexed-record build `002D5EB0` calls: `0030D600` looks up `rdi`'s entry, `002F88B0` runs on it with `022C217C` incremented, `00861EC0` zeroes `rdi*24` bytes of record, and `0020E600`/`00808C40` finish - the schema's per-index record fill.

Interior anchor `00309C6B` (function `00309C40`).

`002CBA50` (457 B) is the cursor walk `002CC2A0` calls: `0209AC30`'s `+0x2E0` object `r14` gates, its `+0xD0` array loops calling `00282DF0([rax+0xD4])`, `dword[r14+0x168] & 0x300000` picks `002CA5D0` directly or `bt 0x11` into the `[rdi+0x48]`-keyed `002DD7E0` arm - the layout's per-cursor rebuild pass.

Interior anchor `002CBA99` (function `002CBA50`).

`002C2DA0` (445 B) is the call-free cyclic stepper `002C2F90` uses: `byte[[rcx+0xC0]+0xEC]` bounds a four-case `esi` dispatch; `word[rcx+0xAE8]` is the cursor, `+0xAEE`/`+0xAEC`/`r8d` wrap it forward or back inside the count - the layout's index-wrap arithmetic.

Interior anchor `002C2E01` (function `002C2DA0`).

`002CA5D0` (232 B) is the record flag-setter `002CBA50`/`002CA7C0` call: `00282DF0` resolves `dword[rcx+0xD4]`, `word[0209AC30 + 0xDE0]`'s slot resolves the same way and `word[+0x60]` must match `word[rbp+0x60]`, `esi != 1` gates, then `dword[rdi+0xC0]` is rewritten `& 0xFFFFFF45 | 0x45` and `byte[[[rdi+0x60]] + 0x3B]` lands in `+0xC6` - the layout record's flag commit.

Interior anchor `002CA5F2` (function `002CA5D0`).

`00248500` (430 B) is the call-free ~~byte-stream walker~~ `.as7` page codec `0024AA00` calls (**Corrected 2026-09-30 (SWE2-EC7, SWE2-DATA's `.as7` decode):** a static-dictionary LZ: `mode = tail[0]` - only 0 and 3 decode, and `<= 2` takes the output length from `be16 tail[2..3]` - and `k = tail[1]` splits a copy token's length and dictionary offset; literal runs copy `n + 1` payload bytes and copy tokens read the tail's dictionary, never the output; [rc22-34-resource-readers-0930](../../_index/candidates/rc22-34-resource-readers-0930/README.md) §1): `byte[rdi]` is ~~the opcode~~ the tail's mode byte (`<= 2` folds a `* 0x100 + byte` pair into `si`: the be16 output length), `r9 = byte[rdi+1]` ~~sizes each step~~ is `k`, ~~`r13 = 0x100`/`r12 = 0xFFFF` bound the accumulation, and the `r9 + 1` loop walks the blob - the packed layout-parameter decoder~~ `r13 = 0x100` joins the big-endian halves, and `0xFFFF` shifted right by `r9 + 1` (`00248555`) is the dictionary-offset mask - the page decode, not a layout-parameter decoder.

Interior anchor `00248533` (function `00248500`).

`002847C0` (422 B) is the metrics setter `002C1FF0` calls: `[[rcx+0x60]+0x18]` is `rbx`, five rounds of `002DDC50` predicate then `00254A00` float scaled by `word[[rbx]+8]` through `cvtdq2ps`/`mulss`/`cvttss2si` into `word[rbx+0x10]`.. - the layout record's text-metrics writes.

Interior anchor `002847E8` (function `002847C0`).

`0037F860` (401 B) is the teardown `0037E4F0`/`0037F4D0` call: frees `[r14 + 0xC8]` via `003697F0` and zeroes the slot, `dword[r14 + 0xE0] & 0x40` runs `002F83E0(0x15)` then clears the bit, frees `+0xD0` (`003697F0`) and `+0xD8` (`0039BB60`), then `0017FA70` and `00473B50`/`00473B60` - the layout record's release sweep.

Interior anchor `0037F87D` (function `0037F860`).

`0028CB90` (381 B) is the interval lookup `0028D260`/`0028D460` call: an `r8d`-bounded bisect over word pairs at `rbx` - `word[rbx + 6] > r9d` descends left, `word[rbx + 0xE] <= r9d` ascends right - then `00861F0E` twice and `002752E0` - the layout's range search.

Interior anchor `0028CC49` (function `0028CB90`).

`002D5280` (354 B) is the index finder `002D5EB0` calls: loops `r8d` entries of the `rdx` array at 0x18 stride, `movsx word[rdi + 0x140]` through `0035BB20` resolves each and `[rax + 4]` is compared against `[rbp]` - the schema's linear key match.

Interior anchor `002D52C7` (function `002D5280`).

`002D5170` (270 B) is the label compose `002D5EB0` runs on the signal widget: `word[rdi+0x140]` resolves through `0035BB20` and `sword[rax+0x60]` through `00296600` for the suffix string; `byte[rdi+0x142] & 4` or a nonzero `esi` selects `002F9860(0x46B4)`, otherwise `ebp` picks one of `0x4669`/`0x466A`/`0x466C`; the chosen string lands at `rdi+0xC0` with `rbx` appended, then `[rdi+0x60]`'s head takes `r8` into `+0x18` and `0020E620`'s index into `+0x20` - the widget's text install.

Interior anchor `002D51D5` (function `002D5170`).

`003C1DF0` (268 B) is the lazy block install `002BA700` runs on the `02B457E0` layout object: gated on `dword[+0xD0]` bit `0x20` set with either bit `4` clear or bit `0x40` set, it computes the element span `word[[+0xE8]+0xA] + [+0xE8] + 2 + word[[+0xE8]] x 2` aligned up to 4, `003BD950` allocates it into `+0xF0`, `003BC970` validates, `00249580` opens the context, `00249210` runs with `edx = 7`, `r8d = byte[alloc+4] + 0x496`, `r9d = 3`, and `[result+8]` lands in `+0xF8`; `dword[+0xD0]` is then masked `& ~0x40` and given bit `4`, and `00249410` closes - the deferred sub-record build the layout object performs on first eligible call.

Interior anchor `003C1E48` (function `003C1DF0`).

`00242F30` (254 B) is the packed-record read `00276D30` runs straight on `0208EA90`: `[+0x20] + 0x30` heads the block, `word[+0x44]` counts the `word[+0x18]`-based index table that `r10 = word[.. + rax*2] + r9` selects into, and the `x 8` row at `[r9 + r10*8]` yields three u16 fields plus the `+4` dword's `& 0xFFF`/`>> 0xC` split - `002D8BB0` frames and `002D8CB0` consumes the pair, `002D8BB0` closes.

Interior anchor `00242FD6` (function `00242F30`).

`00242600` (236 B) is the packed scroll-list row read `0027AD70` runs: `0035D460` resolves `rcx` to the context, `[rax+0x20] + 0x30` heads the blob, `word[+0x30]` indexes `word[r11 + r9*2 + 0x18]` into the `word[+0x10]`-based `x8` rows; the row's three u16s and `+4` dword split `& 0xFFF`/`>> 0xC` stage `rsp+0x50`, `byte[r11+7]`'s nibbles pick a `word[+0x12]`-based byte for `[r14+0x5C]`, `esi` loses `(+4 >> 0xD) & 0x7FF`, and `002D8CB0(rdi, &pair, ebp, ...)` consumes before `+0x5C` restores - the scroll-list's per-entry field fetch.

Interior anchor `0024261A` (function `00242600`).

`00247570` (24 B) is the `+0x48` field setter the layout readers run: null-guards `rcx`, then `[rcx+0x48] = rdx` or the `00915198` sentinel `0x100000000` when `rdx` is null - the optional-pair write every UI record builder shares.

Interior anchor `00247583` (function `00247570`).

`002CDE20` (39 B) is the two-stage index query the emit family shares: `002CD920` maps the arg to a signed index, a negative result returns 1 (absent/closed), otherwise `movzx ecx, ax` feeds `00252D10` and its byte is the answer - the index-then-flag probe three layout callers run.

Interior anchor `002CDE37` (function `002CDE20`).

`002CD920` (181 B) is the dense id remap: `ecx - 0x405` bounds to `0xB9`, the byte table at `0012DA1C` picks a case index and `0012D9D8` its target - each case returns a small code `0x29..0x3A` and the default is -1 - the layout-id classifier the two `002CDExx` callers share.

Interior anchor `002CD953` (function `002CD920`).

`002B9D30` (648 B) is the lazy double-buffered page-state allocator behind `002BA700`: on first use it builds the 0x179E0-byte `0209E5F0` singleton through `00244F50` (ctor `002BA700`) and stamps the mode word `bp` at `+0x179DA`; thereafter it selects the front/back page by bit 2 of `+0x179D2` into `+0x1B0 + sel*0xBC10`, probes it with `00273A20`, formats the 0xBC08-byte region through `00245000`, runs the object's first vtable entry with code 0x29, and sizes its rows from `002C9430(0x80)`/`(0x81)` and the `+0x179D9` override byte into `+0xBBEE` - the surface flip the layout-parameter editor drives.

Interior anchor `002B9E59` (function `002B9D30`).

`00564430` (497 B) is the text-metric scanner `00565E00` drives: `ecx-0x405` indexes the ten-way jump table at `00564624` to pick a `{start, count}` pair (defaults `{1,1}`), then for each index `ebx` it counts strings via `00252FA0`, resolves the category record's `+4` offset through `00252F40`/`0020E600` into a u16 id array, and per id looks the string up with `00292B70` and measures it with `002B3050`, keeping the signed maximum of the result's `+0x30` word in `esi` - the widest glyph run the selected categories produce.

Interior anchor `0056456C` (function `00564430`).

`0028E690` (248 B) is the event post `002814E0` runs on a u16 kind: kind 1 goes straight to `002B9D30(5, [+2])` + `002BA040`; other kinds except 0/3 mark `0209BE80+0x10FA2`, run `00550400` on `+0x10FA2`/`+0x10FA6` and `00550510` on `+0x10F68>>12&1`, then repack `[rbx+2]` (strip bit15, fold bit14 into the low pair) with `movsx [rbx+4]` into a local posted through `00550540`/`00550610` - kind 0 and 3 return untouched

Interior anchor `0028E72F` (function `0028E690`).

`002BA040` (364 B) is the `0209E5F0` object refresh `0028E690` invokes: flag `+0x179D2 & 0x400` set copies the cached 0x20-byte pair `+0x190`/`+0x1A0` off the `02B47760` object (refreshing `02B47760` via `003CB410` first when the flag was clear), clear rebuilds through `00249580` + `00404060` + `00249410`; with `0x400` set it then does `+0x179D2 |= 3` and fires the object's two vtable entries with `0x10`/`0x20` codes, clear it substitutes `003BC450(0, 1, obj)` - the return is `obj + 0x1B0`, selecting the `+0xBC10` second array when `+0x179D2` bit 2 is set

Interior anchor `002BA12D` (function `002BA040`).

`002724A0` (230 B) is the packed-command emitter `00274CB0` runs: it ORs `0x3000000000008000` into the sign-extended `[rcx+0x40]` and stores it with a `0x412` tag into `[rcx+0x38]`'s record, writes `((+0x10 - +0x20 - 0x10) >> 4 << 16) | 0x6C008000` plus a `0x10000000` triple into `[rcx+0x20]`'s stream, a `0x10000000`/`0x13000000`/`0x17000000`/`0x10000000` quad into `[rcx+0x10]`'s stream (advancing it `0x10`), calls `0016D6A0` on the stack pair `{+0x18, (+0x10 - +0x18 - 0x10) >> 4}`, and when `[rbx+0x10]` has passed `[rbx+8]` it aligns `[rbx]+8` up 16 and tails `003A1DB0`

Interior anchor `00272539` (function `002724A0`).

`003BC450` (137 B) is the deferred-register shim `002BA040` substitutes for the vtable arm and `003CB440` also invokes: while `02B457E0` is empty it registers `003BC4E0` through `00244F50` (code `0x278`) with a stack record carrying `{0}` plus a `{ecx, edx}` pair and a `r8` pointer indirection, stores the handle into `02B457E0`, and returns `1`; an already-taken slot returns `0`

Interior anchor `003BC493` (function `003BC450`).

`00404060` (187 B) is the named-parameter binder `002BA040`'s `0x400`-clear rebuild runs after `00249580`: three `002493D0` lookups bind "LocaBack_c" to `rdi`, "Loca_8_c" to `rdi+8` and "w_line01" to `rdi+0x10` (each with its `7`-/`2`-shaped kind and line tags `0xB9`/`0xBA`/`0xB0`), then `00249320` fills `rdi+0x18` - the local-layout shader slots of the refreshed object

Interior anchor `004040CF` (function `00404060`).

`002C5810` (228 B) is the modulo-`0x20` cursor walk `002C59D0` runs: from the signed `+0x14D` position it steps by mode `dl` (`0`/`1` decrement/increment, `2`/`3` subtract/add the `byte[[rcx+0xC0]+0xEC]` stride), wrapping into `0`..`0x1F`, then scans up to `0x20` candidates probing `002D02A0` on the `+0x32`-indexed `r14` slot table with `[r14+0x148]` until one accepts; it writes `+0x14D` and returns whether the position changed

Interior anchor `002C589C` (function `002C5810`).

`00250F30` (212 B) is the `020927F0` transition dispatcher `0027F2E0` runs: `+0xE4` s16 state `0` arms the fade-in (`+0x114` = `+0x110`, `+0x118` = `-+0x110`, copies `0208F570` into `+0x11C`/`+0x13C`, `+0x122` into `+0x13A`, `+0x130` = 0, `+0x134` = `1.0f`, `+0x138` = 0) and states `2`/`3`/`4` run `00250E50(0.0f)` - all landing `+0xE6 = 5`, with any other state setting `+0xE6 = 6`

Interior anchor `00250FB1` (function `00250F30`).

`00250E50` (53 B) is the transition-arm `00250F30`'s states 2-4 call and `00251010` also reaches: on the `020927F0` record it sets `+0x114 = +0x110` (prior value), `+0x118 = xmm0 - +0x110` (signed delta of the caller's target), and `+0x11C = [0208F570]` (frame tick) - the shared 'begin a fade toward xmm0' primitive behind both callers

Interior anchor `00250E64` (function `00250E50`).

`002C3C80` (205 B) is the slot probe `002C2F90` runs: `r9d = [[+0xC0]+0xEC]` bounds the search and `edx` mode-dispatches the candidate index - `0` wraps `r8 mod r9`, `1` accepts only the last slot when `r8 % r9 == r9-1` else `r8+1`, `2` requires `r8 - r9 < [+0xAEC]`, `3` requires `r8 + r9 > [+0xAEE]` - then scans up to `r9` `0x20`-stride slots for `+0xD0 word != 0` or `+0xC8 != 0`, returning 1 when one hits

Interior anchor `002C3CB0` (function `002C3C80`).

`002D50B0` (188 B) is the row emit `002D5EB0` runs over the widget's `+0x748`-counted `0x158`-stride table: every row except index `r14d` is `00244DD0`-submitted via its `rsi + i*0x158 + 0x180` node, while the selected row is stamped in place - `+0x2C2` byte OR'd with `3`, `+1 = 0x10`, `+2` taking the row's own `+0x218` word, and `+4` summing `[rsi+0x15A] + [rbp+0xE]` where `rbp` is the `[[rcx+0x120]]` list head - before a tail `00244DD0` submits the `+0xC0` node

Interior anchor `002D5117` (function `002D50B0`).

`002A5460` (188 B) is the message-record emit `002A70B0` builds on the stack: `002AC1E0` initialises the `rsp+0x30` envelope, `[rbx+0x20]` resolves `0020E600` -> `0039BAD0` into byte `rsp+0xD6`, `[rbx+0x18]` lands at `+0x58`, the `[rbx+0x28]` float at `+0x64`, the `[rbx+0x2F]` signed byte converted to float at `+0x7C`, `rsp+0xE0` gains arm bit `0x2000000` and `rsp+0xD3` clears; `002B3120` then hands the record to the sink and the function returns the emitted `word[rsp+0x20] + 4` - the record's own size word plus its header

Interior anchor `002A54A4` (function `002A5460`).

`002D53F0` (177 B) is the two-phase scale emit `002D5EB0` (the `NaSPArt` signal widget) calls: `xmm1` maxed against zero times the `[008F3134]` constant yields a tick count handed to `0029F6E0` as row `(3, 0x15, 0x80808080)`, then a nonzero `xmm7` divides `xmm6` into the second count and `00225580` runs on `[[rcx+0x60]]` - the widget's scaled-row publish

Interior anchor `002D544E` (function `002D53F0`).

`002CBED0` (165 B) is the lazy `+0x2E0` sub-record `002C2320` runs on `0209AC30`: absent, it `00244F50(0x170, sub-002CBF80, args)`-builds one seeded with `[+0x38]` and the `ecx`-bit-0 pick of `8` or `0`, then stores it; present with `+0x7C` bit `0x20` set, it instead feeds `eax` to `00246AD0` on `0208EA28`

Interior anchor `002CBF39` (function `002CBED0`).

`002418F0` (69 B) is the rate setter `002472A0` and `00247300` share: it presets `[rcx+0xB8]` to `1.0f`, calls `00229DF0`, and when that returns nonzero asks `00229EA0` - on `2` it calls `00229E70` and writes `1.0f / xmm0` back into `[+0xB8]`, the reciprocal of whatever the scheduling lane measured

Interior anchor `00241903` (function `002418F0`).

`00250E90` (157 B) is the `020927F0` record's slot wire: on the `rcx == 0` lane it refuses `[rdx+0xE4]` words `2`/`3`, points `[rdx+0xF8]` at `[0209AC30]+0x390+0x40` and tail-jumps `002553C0`; on the live-`rcx` lane it stores `rcx+0x40` there, then lazily allocates `0209AC48` through `00183760(0x100, 1)` or extends it through `00183310`

Interior anchor `00250EFC` (function `00250E90`).

`002553C0` (72 B) is the `0209AC48` array's grow-or-create `002509D0` and `00250E90` call: a null global lazily allocates `00183760(rcx, 0x100, 1)` and stores it; a live one tail-jumps `00183310(rcx=[0209AC48], rdx=arg, 0x100, 1)` - the same `0x100`-element block machinery `00250E90` uses for the `020927F0` slots.

Interior anchor `002553DF` (function `002553C0`).

`00283690` (156 B) is the flag-count scorer the UI reader `00281AE0` runs: `0032A8A0` is polled over `0x4008`, `0x4006`, `0x4004`, `0x4010`, `0x4009`, `0x400A` and `0x4007`, counting set bits into `ebx` (with an extra +1 when `0x4006` is set AND `00254A50()` returns 0, and the same for `0x4010`); the return is `ebx+2` when `0x4007` is set else `ebx+1` - a bounded tally of enabled options in the `0x4004`..`0x4010` flag lane.

Interior anchor `0028369D` (function `00283690`).

`00299FC0` (221 B) is the per-row fade driver `00299D10` ticks: `003588B0` resolves `dword[rcx+0xC4]` - a null record clears bit 0 of `+0xE8`, a live one gets `002E9A90` applied to `+0xD0`; under `+0xE8` bit 2 the `+0xCC` progress float ramps by 1/6 up (bit 0 set) or down, clamped 0..1; and when `+0xE8` bit 1 is clear with `+0x7C & 0xF == 3` the `+0xC0` counter decrements to 0, sets bit 1 and tail-calls `00244F00`.

Interior anchor `00299FCF` (function `00299FC0`).

`003BD950` (145 B) is the deepest-entry find `003C1DF0` installs from (both this page and the map-screens page name it inside the block install): `dword[rcx]` is the pair count, and the body walks `rcx+4 + count*8` backwards testing each `{u16, u16}` row - rows whose threshold `row[0]` does not exceed `00265270()`'s current value are skipped; a row is returned when `row[1] != 0xFFFF` and `0032A8A0(row[1])` resolves non-null - the layout block's resolved-row probe, not an allocator.

Interior anchor `003BD986` (function `003BD950`).
