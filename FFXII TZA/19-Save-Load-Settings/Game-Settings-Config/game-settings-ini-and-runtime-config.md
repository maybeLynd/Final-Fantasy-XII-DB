---
system: GameSetting.ini configuration object
category: 19-Save-Load-Settings
status: AUDITED
owner_layer: Save_Load_Settings
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN158 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN158 this document cites none of batch R109's 109; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: three parallel tables dumped from the image and cross-checked against each
    other; writer analysis by a peer analysis session, names and tables re-verified here
last_reviewed: 2026-09-12
audit:
  passes: 5
  last_pass: 2026-09-08
  last_pass_state: framelimit-consumer-chain-read-DH1-DH2-answered
  last_pass_kind: authored
  note: sections 12-13 were derived against the GN160 export (work/graph) and the
    shipping EXE; sections 1-11 retain the earlier parent recorded above
  crossref_clean: false        # 2026-09-30 (SWE2-DATA): false until the pass-22 UNACCOUNTED NEIGHBOUR findings are accounted (FRONTIER-REQ-SWE2-DATA-PASS22-DEBT; OPUS-REQ-DATA-PASS30-CROSSREF-CLEAN-0930)
  reopened_count: 0
container_format: game-settings-ini
---

# GameSetting.ini configuration object

> **Every option the player can set lives in one 0x65C-byte object with 31 slots**, one dword each,
> described by three parallel tables in the image and persisted as plain text to
> ~~`%DOCUMENTS%\My Games\FINAL FANTASY XII THE ZODIAC AGE\GameSetting.ini`~~ `%DOCUMENTS%\My Games\FINAL FANTASY XII THE ZODIAC AGE\<Steam id>\\GameSetting.ini` *(corrected 2026-10-02, OPUS: checked at `0079817E`–`00798234` — `L"%s%s\"` with the Steam-id folder from `001F3ED0`, then `L"%s\%s"` + `L"GameSetting.ini"`; CONTRACT-game-setting-config.md, the per-account path)*.
> **Slot index × 4 is the field offset**, which is why the singleton's fields land where they do.

**For a player.** This is the options menu, and the file behind it. Language, resolution, shadow
quality, mouse sensitivity — and **`DecideButton`, the setting that decides whether Circle or Cross
confirms**. Changing it in the menu writes the object, notifies the input manager and re-applies the
button masks immediately; quitting writes the line `DecideButton=Circle` (or `Cross`) to the ini.

---

## 1. The object

| | |
|---|---|
| pointer | **`0x01F82D20`** — written exactly once, at `00798261` |
| size | **`0x65C`** bytes, allocated at `00798239` (`mov ecx,0x65C`) |
| settings array | **31 dwords** at `+0x00` .. `+0x7B` — **offset = index × 4** |
| ini path buffer | `+0x450`, **`wchar_t[0x104]` = 520 bytes**, `+0x450`..`+0x657` |

## 2. The three parallel tables

```
keys          0x01DFD050    31 x qword char*
value names   0x01DFD150    31 x 9 qword char*, NULL-terminated per row   <- corrected 2026-10-02, OPUS: not terminated - row 0 (Language) fills all nine slots, read at 01DFD150; CONTRACT-game-setting-config.md
defaults      0x00900CE0    31 x 16 bytes, column 0 read at init
```

**The value-name table ends exactly where the next table begins**, which fixes the count at 31
independently of the key table — two derivations agreeing.

| # | offset | key | # | offset | key |
|---:|---|---|---:|---|---|
| 0 | `+0x00` | **`Language`** | 16 | `+0x40` | `WaterQuality` |
| 1 | `+0x04` | `Resolution` | 17 | `+0x44` | `BackBufferCount` |
| 2 | `+0x08` | `ScreenMode` | 18 | `+0x48` | `FrameLimit` |
| 3 | `+0x0C` | `Quality` | 19 | `+0x4C` | `DeviceID` |
| 4 | `+0x10` | `Brightness` | 20 | `+0x50` | `LUIDLow` |
| 5 | `+0x14` | `VSync` | 21 | `+0x54` | `LUIDHigh` |
| 6 | `+0x18` | `Anisotropic` | 22 | **`+0x58`** | **`CameraRevise`** (Off/On) |
| 7 | `+0x1C` | `Shadow` | 23 | `+0x5C` | `MouseSensityX` |
| 8 | `+0x20` | `MSAA` | 24 | `+0x60` | `MouseSensityY` |
| 9 | `+0x24` | `PostAA` | 25 | **`+0x64`** | **`DecideButton`** (Circle/Cross) |
| 10 | `+0x28` | `HDAO` | 26 | `+0x68` | `Monitor` |
| 11 | `+0x2C` | `WindowSize` | 27 | `+0x6C` | `WindowPosX` |
| 12 | `+0x30` | `DepthofField` | 28 | `+0x70` | `WindowPosY` |
| 13 | `+0x34` | `Glare` | 29 | `+0x74` | `LastX` |
| 14 | `+0x38` | `SoftParticle` | 30 | `+0x78` | `LastY` |
| 15 | `+0x3C` | `CharacterSelfShadow` | | | |

Defaults (column 0 of `0x00900CE0`): `Language` = **1** (`en`), `CameraRevise` = **1** (On),
`DecideButton` = **0** (**`Circle`**).

**`Language`'s default is overwritten immediately after the defaults copy** by a region query at
`001DE0C0`, mapping a primary-language id into this index space. So the compiled-in default is
English and the shipped behaviour is "whatever the OS says".

## 3. `DecideButton` — and the removal of an external premise

Row 25 of the value-name table is exactly two strings: **`Circle`** (0) and **`Cross`** (1).

[The button convention](../Language-And-Locale/language-selection-and-locale-ids.md) established that
`0022A4F0` writes **`0x2000` to the confirm mask when the field is 0**. The field's value-0 name is
literally `Circle`.

> **`0x2000` = Circle and `0x4000` = Cross, derived from the game's own strings.**

That was previously carried as **EXTERNAL** knowledge — the PlayStation button-mask convention — and
flagged as an assumption nothing depended on. **It is now measured, and the external premise is
withdrawn.** The identification of *which mask is confirm* never rested on it (that came from which
branch can fail); what is new is that the *button names* are now internal evidence too.

## 4. The three writers

| # | site | in | what |
|---|---|---|---|
| 1 | `001DE099` | `GameSettingConfig_InitDefaultsAndPath` (`001DE050`) | the 31-iteration defaults copy (`lea r9,[00900CE0]`, stride `0x10`, count `0x1F`) |
| 2 | `001DF6AE` | `GameSettingConfig_ParseOneSettingValue` (`001DF350`) | the ini-driven write; enum path, value = ordinal of the matched name |
| 3 | `001DF343` | the generic indexed setter `FUN_001DF340` | the runtime write, `[rcx + rax*4] = r8d` |

The runtime path is the interesting one. `FUN_0017E6E0` loads the singleton, sets `edx = 0x19` (25),
calls the generic setter, **notifies the InputManager** (`00198960`), then **tail-jumps to
`0022A4F0`** — the mask applier. One caller: the settings-command dispatcher `FUN_002407F0`,
**command id `0x26`**.

**This answers whether a player can change it: yes.** It is a persisted user setting with a runtime
setter that re-applies the masks immediately — not a per-release constant.

## 5. Persistence

`GameSettingConfig_SerializeText` (`001DEE90`) walks all 31 settings using the same two tables and
writes `Key=Value`. **For a setting with more than one value name it writes the name, not the
number**, so the file contains `DecideButton=Circle`. If no file exists, the loader creates one from
the defaults.

## 6. Why a base-taint scan could never find the writer

An earlier pass looked for a write to `[reg+0x64]` on this object and found none — correctly.
**No literal `[reg+0x64]` write to this object exists anywhere in the image.** All three writers reach
the field through a **computed index** (`[base + index*4]`), never a literal displacement.

A full access-role scan of the image finds **~~157~~ 159 instructions referencing `0x01F82D20`: ~~156~~ 158 reads and
exactly one write** *(corrected 2026-10-02, OPUS: `retool.py refs 01F82D20`, in 63 functions)* — the singleton store itself.

**This is a new blind-spot shape and it is now on record:** a scan keyed on a *displacement* cannot
see a field written through an index, and an array-of-settings object is written that way by
construction. Finding it required enumerating all ~~36~~ 38 *(corrected 2026-10-02, OPUS: `retool.py callers 001DF340`, 38 call sites in 15 functions)* call sites of the generic setter and recovering
the constant index at each — **exactly one passes 25**.

## 7. Provenance of this document

Sections 4 and 6 were measured by a **peer analysis session** working read-only from a brief; the
three named functions and all three tables were **re-verified here against `functions.tsv` and the
image** before publication. The key list, value names, defaults and offset arithmetic in sections 1–3
and 5 are re-derived measurements, not transcription.

## Open questions

- [x] ~~What columns 1–3 of the defaults table hold.~~ **ANSWERED** — it is a **quality preset
      matrix**: column *j* is the value for quality level *j* (`VQ_LOW`/`MEDIUM`/`HIGH`/`CUSTOM`),
      applied by `FUN_001DE4F0` through a **31-byte mask at `0x00900CC0`** that selects **10**
      graphics settings. `VQ_CUSTOM` changes nothing, so column 3 is never read. Section 10. **AX-1.**
- [x] ~~Whether anything applies a quality preset **at startup**.~~ **ANSWERED — NO.** `FUN_001D5120`
      applies it, but nothing runs `001D5120` at startup; see `AX-6a`. The column-0 / `Quality = 1`
      mismatch therefore stands in the shipped game. Section 11 and [the Config screen](../../16-UI/Config-Screen/the-config-screen-and-what-a-setting-change-runs.md). **AX-6.**
- [x] ~~*When* the graphics-apply callback runs.~~ **ANSWERED** — when the player pushes left or right
      on a row of the in-game Config screen, and nowhere else in the image. `0023B330` / `0023B6F0` are
      the **procs of two row objects**, not registered callbacks; `FUN_0023BD40` is the screen's own proc.
      [the Config screen](../../16-UI/Config-Screen/the-config-screen-and-what-a-setting-change-runs.md). **AX-6a.**
- [x] ~~Which of the 31 settings the options UI actually exposes, versus ini-only.~~ **ANSWERED — ~~16 of~~
      ~~31.~~** 22 of 31 *(corrected 2026-10-02, OPUS: the correction this list records under AX-3, the Config screen page §11)*. Full split in [the Config screen](../../16-UI/Config-Screen/the-config-screen-and-what-a-setting-change-runs.md) section 5. **AX-2.**
- [x] `LUIDLow` / `LUIDHigh` / `DeviceID` / `Monitor` — the adapter-selection group. **AX-3.**
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (AX-3): they record the selected display
      adapter and output, and the in-game Config screen's row 4 edits them.* The display object `[01F82D18]` enumerates
      adapters in `001DD170` into a 0x140-stride table: a 0x130-byte description (the size of `DXGI_ADAPTER_DESC`),
      then an output count at `+0x130` and outputs at `+0x138`.
      - **Row 4 commit.** `001DC650` moves the index to a usable adapter (mask `+0x58`) and writes `DeviceID` = desc
        `+0x104` and `LUIDLow`/`LUIDHigh` = `+0x128`/`+0x12C`, the `DeviceId` and `AdapterLuid` offsets.
      - **Monitor.** `001DC7A0` replaces an output index above the adapter's output count with 1. It writes `Monitor`
        (and the file) only when the selected adapter is the current one.
      - Details, and the correction that AX-2's "16 of 31" is 22, are in
        [the Config screen](../../16-UI/Config-Screen/the-config-screen-and-what-a-setting-change-runs.md) §11.
- [x] ~~Which language index each arm of the LANGID mapping selects.~~ **ANSWERED** — full table in
      section 9. **`ch` = Traditional, `cn` = Simplified**; default `en`; `0x1C04` explicitly excluded
      from the Traditional group and treated as Simplified. **AX-4.**
- [x] ~~Object fields `+0x44C`, `+0x658` (`0x0101`) and `+0x65A`, all set before the defaults copy.~~
      **AX-5 ANSWERED 2026-09-12 (FABLE):** `+0x44C` is the **MSAA availability mask** — bit 0 the
      constructor's "off", bits 1 / 2 / 3 / 5 set for 2× / 4× / 8× / 16× by the device set-up's
      `ID3D11Device::CheckMultisampleQualityLevels` probe `00628690` (bit 4 for 8× with more than 16
      quality levels) through the thunk `0017D9C0` and the bit setter `001DF2B0`, and read only by the
      debug menu's five-option cycler `001DF2C0` into setting 8; `+0x658` / `+0x65A` are fresh-defaults
      markers zeroed on a successful load and never read on this object. Detail in
      [the contract](CONTRACT-game-setting-config.md) §14. **AX-5.**

## 8. Falsification pass 2026-09-02 — the count and the stride, from the loop itself

**Attack chosen.** Everything in this document rests on **31**. If the count is wrong every offset
after the first wrong slot is wrong, and `DecideButton` at index 25 is exactly the sort of claim that
would survive a reader's eye while being off by one. The count arrived from a peer session's
table-adjacency argument — good evidence, but indirect.

**The initialisation loop settles it in six instructions:**

```asm
001DE064  mov  edi, 1
001DE08F  lea  ecx, [rdi + 0x1E]        ; ecx = 0x1F = 31          <- THE COUNT
001DE082  lea  r9,  [rip + 0x722C57]    ; -> 0x00900CE0, defaults
001DE089  mov  r8,  rcx                 ; -> the settings array at +0x00
001DE092  mov  eax, dword ptr [r9]      ; defaults column 0
001DE095  lea  r9,  [r9 + 0x10]         ; defaults stride 0x10     <- THE ROW SIZE
001DE099  mov  dword ptr [r8], eax
001DE09C  lea  r8,  [r8 + 4]            ; settings stride 4        <- OFFSET = INDEX x 4
001DE0A0  sub  rcx, rdi
001DE0A3  jne  0x1DE092
```

**All three load-bearing numbers are stated by the code**, not inferred: the loop runs **31** times,
the defaults table has a **`0x10`** row, and the settings array advances **4 bytes per setting**.
Section 1's "offset = index × 4" was a pattern fitted to three known fields; it is now the increment
in the loop.

**A third confirmation, unlooked for:** the key table at `0x01DFD050` has a **NULL at index 31** —
it is null-terminated. Index 32 onwards is unrelated data (the `jp`/`en`/`fr` string pointers of the
runtime language table, which merely follows it).

So **31** is now established three independent ways: the loop bound, the key table's terminator, and
the value-name table ending exactly where the next begins. The document survives.

### What the same read added

**Resolution and WindowSize come from the desktop.** `008C29B0` is called twice, with `ecx = 0` then
`ecx = 1`, and the results packed `first << 16 | second` into **both** `+0x04` (`Resolution`) and
`+0x2C` (`WindowSize`) — a screen-metrics query shape. So a fresh install adopts the desktop
resolution rather than a hardcoded default.

**Which half is which, and how wide (OPUS-REQ-FABLE-PACKEDSIZE, 2026-09-11).** The two calls are
`GetSystemMetrics(0)` then `GetSystemMetrics(1)` — `SM_CXSCREEN`, the width, then `SM_CYSCREEN`,
the height (the same import pair feeds the diagnostic line `"Screen Resolution :%dx%d"` in that
order, `001CD530`–`001CD561`) — so `first << 16 | second` puts **the width in the high half**
(`+0x06`, `+0x2E`) **and the height in the low half** (`+0x04`, `+0x2C`); the row names'
`width<<16|height` is right, and a reader who expects width first in memory will be wrong. Every
arithmetic consumer treats **both halves as signed 16-bit**: the six functions that read a pair
(`001DC830`, `001DCD30`, `001DD8E0`, `00795DC0`, `00798FF0`, `0079F750`) `movsx` the high half and,
after a `movzx` load, `movsx` the low half too before multiplying or comparing (`001DC88A`–
`001DC8B3`, `0079F77C`–`0079F79E`), and the mode-picker in `001DC830` multiplies them into an area
it compares against each display mode's `width × height` to choose `+0x24`. Which pair a reader
uses is decided by `+0x08` (`ScreenMode`): zero selects the `WindowSize` pair, anything else the
`Resolution` pair — read in three of the six (`001DC883`–`001DC89E`, `00795DF8`–`00795E13`,
`0079F775`–`0079F790`), the same shape OPUS's census reports for the other three. Nothing
observed exceeds `0x7FFF`, so the signedness is the declared type, not a behaviour a player can
reach.

**The language default is replaced by an OS query with a Traditional-Chinese special case.**
After the defaults copy, `008C2110` returns a LANGID, and:

```asm
001DE0CB  and  ecx, 0x3F                ; keep the low bits
001DE0CE  lea  eax, [rdx - 0x404]
001DE0D4  test eax, 0xFFFFE7FF          ; true only if langid is 0x0404 | 0x0C04 | 0x1404 | 0x1C04
001DE0DB  cmp  edx, 0x1C04
```

`0xFFFFE7FF` clears exactly bits `0x0800` and `0x1000`, so that test passes for **four** LANGIDs —
`0x0404`, `0x0C04`, `0x1404`, `0x1C04` — which are the **Traditional Chinese** sublanguage group,
with `0x1C04` then singled out. **The mapping from Windows locale to the game's language index is not
a plain table lookup; it has a Chinese-variant branch.** ~~Which index each arm selects is not read~~
~~here.~~ *(answered: see §9, "AX-4 answered — the whole locale mapping"; 2026-10-02, OPUS)* **AX-4.**

Three more object fields, measured in passing: `+0x44C` = 1, `+0x658` = `0x0101` (two bytes),
`+0x65A` = 1 — all set before the defaults copy~~, all unidentified~~ *(answered: see the AX-5 box above — `+0x44C` is the MSAA availability mask, `+0x658` / `+0x65A` fresh-defaults markers; 2026-10-02, OPUS)*. **AX-5.**

## 9. AX-4 answered — the whole locale mapping, and `ch` versus `cn` settled

The OS query at `001DE0C0` returns a LANGID; the code keeps the low bits as the **primary language
id** (`and ecx, 0x3F`) and maps it to a language index. Read in full:

| test | index | code | Windows primary id |
|---|---:|---|---|
| LANGID ∈ {`0x0404`, `0x0C04`, `0x1404`} | **7** | `ch` | **Chinese, Traditional** |
| `ecx == 0x11` | **0** | `jp` | Japanese |
| `ecx == 0x0C` | 2 | `fr` | French |
| `ecx == 0x07` | 3 | `de` | German |
| `ecx == 0x10` | 4 | `it` | Italian |
| `ecx == 0x0A` | 5 | `es` | Spanish |
| `ecx == 0x12` | 6 | `kr` | Korean |
| `ecx == 0x04` | 8 | `cn` | **Chinese, Simplified** |
| **anything else** | **1** | `en` | English |

**`ch` is Traditional Chinese and `cn` is Simplified.** The
[locale document](../Language-And-Locale/language-selection-and-locale-ids.md) listed them only as
"two Chinese variants"; the mapping settles which is which, from the LANGIDs each arm accepts.

**Why Traditional needs its own test.** All Chinese LANGIDs share primary id `0x04`, so the primary-id
chain alone cannot separate Traditional from Simplified. The full-LANGID test runs **first**:
`lea eax,[rdx-0x404]` then `test eax, 0xFFFFE7FF` — which clears exactly bits `0x0800` and `0x1000`,
so it passes for precisely `0x0404`, `0x0C04`, `0x1404` and `0x1C04`. **`0x1C04` is then explicitly
excluded** (`cmp edx,0x1C04 / je`), so it falls through to the primary-id chain and lands on
**`cn` (Simplified)**.

**The default is `1` = `en`, and it is elegant.** `edi` is set to `1` at the top of the function for
the defaults loop (`lea ecx,[rdi+0x1E]`), and **never reset**. Every arm that matches overwrites it;
anything unmatched keeps `1`. The same register serves as the loop constant and the fallback language.

### A fourth independent confirmation of 31

Immediately after the mapping:

```asm
001DE130  lea  rcx, [rsi + 0x7C]
001DE138  mov  r8d, 0x3CC
001DE13E  call memset
```

**`0x7C` = 124 = 31 × 4** — the clear starts at exactly the byte after the last setting. The count is
now established four ways: the loop bound, the key table's null terminator, the value-name table's
end, and this `memset` origin.

It also fixes the object's shape: settings `+0x00`..`+0x7B`, then `0x3CC` zeroed bytes to `+0x448`,
then the ini path at **`+0x450`** — copied by `008C3008` with a length of **`0x104`**, and only
when the caller passes a non-null path.

> The unit of that `0x104` is corrected in §16 — it counts `wchar_t`, not bytes.

## 10. AX-1 answered — the four columns are the graphics quality presets

`0x00900CE0` is not a defaults table with spare columns. It is a **preset matrix**: 31 rows, one per
setting, **four columns, one per quality level**. `Quality`'s own value names name them —
`VQ_LOW`, `VQ_MEDIUM`, `VQ_HIGH`, `VQ_CUSTOM`.

`FUN_001DE4F0` applies it, and the indexing proves the reading:

```c
void ApplyQualityPreset(Config *cfg, int quality)          /* 001DE4F0, 71 B */
{
    if (cfg->setting[3] == quality) return;                /* index 3 = Quality, at +0x0C */
    cfg->setting[3] = quality;
    for (i = 0; i < 0x1F; i++)                             /* 31 settings */
        if (mask[i] && quality != 3)                       /* 3 = VQ_CUSTOM: change nothing */
            cfg->setting[i] = table[i*16 + quality*4];     /* row i, COLUMN = quality */
}
```

The address computed is `[r11 + (quality + i*4)*4]` = `table + i*16 + quality*4` — **row `i`, column
`quality`**. That is the whole claim, in one instruction.

### A second table, previously unseen: the preset mask

`0x00900CC0` is a **31-byte mask** — one byte per setting, `01` if the quality preset controls it —
sitting **immediately before** the matrix and ending at `0x00900CDF`. **Exactly 10 settings are
preset-controlled:**

| | preset-controlled |
|---|---|
| **yes** (10) | `Anisotropic`, `Shadow`, `MSAA`, `PostAA`, `HDAO`, `DepthofField`, `Glare`, `SoftParticle`, `CharacterSelfShadow`, `WaterQuality` |
| **no** (21) | everything else — including `Quality` itself, `Resolution`, `VSync`, `FrameLimit`, `BackBufferCount`, and every non-graphics setting |

**This is why changing the quality preset cannot change your language, your resolution or your
confirm button** — the mask excludes them. It is also why the matrix carries values for settings the
preset never touches (`Quality` `1,1,2,3`; `BackBufferCount` `0,1,1,0`): **that data is inert**,
because the mask gates the write.

**`VQ_CUSTOM` changes nothing.** `quality != 3` guards the assignment, so selecting Custom keeps
whatever the player already had — which is exactly what Custom should do, and it means **column 3 is
never read**. Its mostly-zero contents are dead.

### The preset values

| setting | LOW | MEDIUM | HIGH |
|---|---:|---:|---:|
| `Anisotropic` (1/2/4/8/16) | 2 (=4x) | 2 | 4 (=16x) |
| `Shadow` (Low/Medium/High) | 0 | 1 | 2 |
| `MSAA` | 1 | 2 | 3 |
| `HDAO` (Off/Half/Full) | 1 | 1 | 2 |
| `CharacterSelfShadow` (Off/On) | **0** | 1 | 1 |
| `PostAA`, `DepthofField`, `Glare`, `SoftParticle`, `WaterQuality` | 1 | 1 | 1 |

**Only `CharacterSelfShadow` is off at Low**, and only `Anisotropic`, `Shadow`, `MSAA` and `HDAO`
differ between Medium and High. The Low→Medium step is almost entirely shadow quality.

### A fifth confirmation of 31

The mask is **exactly 31 bytes** and ends at `0x00900CDF`, one byte before the matrix. Count now
established five ways: the init loop bound, the key table's null terminator, the value-name table's
end, the `memset` origin at `0x7C`, and this mask's length.

### One thing not established

`FUN_001DE4F0` has a single caller, `FUN_001D5120`. **~~Whether anything applies a preset at startup is~~
~~not shown here~~** *(answered: nothing does — `AX-6` answered NO, "Resolved 2026-09-08" below; 2026-10-02, OPUS)* — and it matters, because init copies **column 0 (`VQ_LOW`)** into every setting
while `Quality`'s own column-0 value is **1 (`VQ_MEDIUM`)**. Immediately after init the config
therefore says "Medium" while holding Low values, until something reconciles them. **AX-6.**

## 11. AX-6 — the preset *is* applied; when it runs is not statically provable

**The applier is not orphaned.** `FUN_001DE4F0` is called by **`FUN_001D5120`** (257 B, owner
`Presentation`), which is the **graphics-apply routine**: it applies the quality preset and then
pushes the resulting settings into the renderer.

```asm
001D5132  mov  rcx, [0x01F82D20]     ; the config
001D5139  call 0x1DE4F0              ; APPLY THE QUALITY PRESET   (quality arrives in edx, passed through)
          ... then, one setting at a time:
001D515E  mov  ebx, [cfg + 0x40]     ; index 16  WaterQuality
001D51A8  cmp  dword [cfg + 0x20], 0 ; index  8  MSAA        -> byte at renderer +0xDBA
001D51DE  cmp  dword [cfg + 0x24], 1 ; index  9  PostAA      -> byte at renderer +0x4A3
001D5206  cmp  dword [cfg + 0x38], 1 ; index 14  SoftParticle-> virtual call [r8+0x60]
```

**Every field it reads is one the preset mask marks as preset-controlled** — WaterQuality, MSAA,
PostAA, SoftParticle are all in the mask's set of ten. That is independent corroboration of section
10's mask, from a consumer rather than from the table.

~~It also resolves the resolution path:~~ *(corrected 2026-10-02, OPUS: `001DE5A0` is the shadow-map size from `Shadow`, not the resolution — `setting[7]` mod 3 indexes `00900F00` = {512,512}, {1024,1024}, {2048,2048}, checked at `001DE5A0`–`001DE5CD`; the SWE2-EC7-32 note)* `FUN_001DE5A0` is called twice on the config and the second
result is `sar`-ed by 16, splitting the packed `width << 16 | height` into two arguments.

### The chain, and where it stops

```
001DE4F0  preset applier               71 B
  <- 001D5120  graphics apply         257 B   Presentation
    <- 001D1660  renderer setup    13,753 B   Presentation
      <- 001CD040  adapter             14 B
        <- 0017DB90  dispatch         458 B
          <- 0023B330 (502 B) and 0023B6F0 (1,031 B)   -- ZERO callers each
```

**A single path, five levels, ending at two functions with no callers at all** — and neither is a CRT
initializer, so this is not part of the pre-`main` sequence.

**Both roots are `lea`-registered callbacks**, and from the *same* function: `FUN_0023BD40` takes both
addresses (`0023BFE2` → `0023B6F0`, `0023C0CD` → `0023B330`) and registers them together. **This is
exactly the mechanism [AR-4](../../99-Unresolved-Residual/Unowned-Code-Census/why-the-unowned-code-has-no-owner.md)
established** — an address materialised in code and handed to a registrar, invisible to the call
graph.

### The honest boundary

**Established:** the quality preset is applied by the graphics-apply routine, which then pushes the
preset-controlled settings into the renderer.

**~~Not established, and not establishable from the call graph:~~** ~~*when* that runs.~~ *(answered: a left/right press on a Config row — "Resolved 2026-09-08" below; `AX-6a` answered; 2026-10-02, OPUS)* The chain terminates
in callbacks whose invocation is dynamic. Answering it needs the registrar's dispatch semantics —
what `FUN_0023BD40` registers them *as* — not more call-graph walking. **AX-6a.**

So section 10's observation stands unresolved rather than explained: init copies **column 0
(`VQ_LOW`)** into all 31 settings while `Quality`'s own column-0 value is **1 (`VQ_MEDIUM`)**. If the
graphics-apply callback fires before the first frame, the mismatch is transient and invisible. **This
document does not claim it does.**

> ### Resolved 2026-09-08 — and the mismatch is **not** transient
>
> **The chain terminates in the procs of two row objects in the in-game Config screen**, and the only
> thing that runs them is the player pushing left or right on a row. Row 1 is `Quality`. See
> [the Config screen](../../16-UI/Config-Screen/the-config-screen-and-what-a-setting-change-runs.md).
>
> So the paragraph above resolves the *pessimistic* way: **no callback fires before the first frame**,
> nothing at startup applies a preset, and the column-0 / `Quality = 1` mismatch **stands in the shipped
> game** until the player opens Config and moves that row. `AX-6` is answered **NO**, `AX-6a` answered.
>
> **What made it findable was an instrument, not more call-graph walking** — as this section predicted.
> `001CD040` reaches `001D1660` by a **tail jump**, so an `E8`-only reading finds `001D1660` unreachable;
> and `0023B330` / `0023B6F0` are `lea`-materialised, so no call-based instrument can see them at all.

## 12. `FrameLimit` — the one setting that changes how long everything takes

> **`DH-1` and `DH-2` answered.** The frame-rate mode this database has been tracking from the other
> end — the `{1, 1.0, 1.0}` → `{2, 2.0, 0.5}` time-base triple at `0x01DFE0B4` — is decided by
> **`FrameLimit`, setting 18, the line `FrameLimit=30` or `FrameLimit=60` in `GameSetting.ini`.**

### What a player sees

You pick 30 or 60 in the options. What you do **not** see is that this is not a frame cap bolted onto
a fixed simulation. FFXII's timings were authored for the PlayStation 2, in **frames at 30 fps** — a
"wait half a second" is written in the data as the number **15**. Choosing 60 does not make those
waits happen twice as fast; the engine **multiplies every one of them by two**, so that half a second
stays half a second.

**Everything with a duration goes through this**: how long a status lasts, how long a chest takes to
reappear, how often a gambit is re-evaluated, how long a dropped item lies on the ground before it
vanishes. At 60 fps every one of those authored numbers is doubled on the way in.

And there is a second, quieter difference. **At 30 the game asks Windows for a high-resolution
timer; at 60 it does not.**

### The chain, end to end

```
GameSetting.ini
  FrameLimit=30 | FrameLimit=60
      |  parsed to value index 0 or 1 by GameSettingConfig_ParseText (001DE5D0)
      v
  config->setting[18]                       ; the object at 0x01F82D20, field +0x48
      |
      v
  0017D8F0   11 bytes:  mov rax,[01F82D20] / mov eax,[rax+0x48] / ret
      |
      v
  0022BDF0(argc, argv)                      ; the FIRST call in 0022A0B0
      |   ebp = (FrameLimit == 1)           ; xor ebp,ebp / cmp eax,1 / cmove ebp,1
      |   ...then scans argv for "-nologo"
      v
  001EDDC0(ebp)                             ; E9 tail call at 0022BE7D
```

**`0022BDF0` is the first call in `0022A0B0`**, and the getter dereferences `0x01F82D20` with **no
null check** — so the config object must already exist. It does: `007980A0` builds it, reached from
`007A3770`, which is reached from `00808D78`, tagged `MSVCCRT.ExecutableStartup`. **The settings
object is constructed during C-runtime static initialisation, before `main` runs.** The absence of a
null check is not an oversight; it is guaranteed by the startup order.

### The two modes are mutually exclusive

```c
void ApplyFrameLimit(int isSixty)                    /* 001EDDC0 */
{
    if (isSixty) {
        *(float*)0x01DFE0B8 = 2.0f;                  /* from 01CEBC08 */
        *(float*)0x01DFE0BC = 0.5f;                  /* from 01CEBB70 */
        *(int  *)0x01F82E38 = 1;                     /* the "60 Hz" gate - see below */
        *(int  *)0x01DFE0B4 = 2;                     /* the time base */
        FUN_0033F020();                              /* seven initialisers, 60 Hz only */
        if (*(u8*)0x01F82E3C) {                      /* a timer period was raised earlier */
            timeEndPeriod(*(u32*)0x01F82E40);
            *(u8*)0x01F82E3C = 0;
        }
    } else {
        TIMECAPS caps;                               /* 8 bytes */
        if (timeGetDevCaps(&caps, 8) == 0) {
            *(u32*)0x01F82E40 = caps.wPeriodMin;
            timeBeginPeriod(caps.wPeriodMin);
            *(u8 *)0x01F82E3C = 1;
        }
    }
}
```

| | `FrameLimit=30` (value 0) | `FrameLimit=60` (value 1) |
|---|---|---|
| `01DFE0B4` time base | **`1`** — the image value stands; **the 60 fps arm is the only writer** | **`2`** |
| `01DFE0B8` / `01DFE0BC` | **`1.0f` / `1.0f`** — image values | **`2.0f` / `0.5f`** |
| `01F82E38` gate | **`0`** — BSS zero stands; **`001EDDE8` is its one writer, on the 60 fps arm** | **`1`** |
| `FUN_0033F020` | **not called** | called |
| Windows timer | **`timeBeginPeriod(wPeriodMin)`** | released, if previously raised |

> **At 30 fps the engine writes nothing at all.** The triple keeps the values the linker put in
> `.data`, and the whole 30 fps configuration *is* the image's initialised state. This is worth
> saying plainly, because it makes the 30 fps path invisible to a scan for writers — which is exactly
> how it stayed unexplained.

**The three imports were resolved through the PE import directory, not inferred:** `008C2A90` =
`WINMM.dll!timeGetDevCaps`, `008C2A98` = `timeBeginPeriod`, `008C2AA0` = `timeEndPeriod`. The
`edx = 8` argument is `sizeof(TIMECAPS)`, and `caps.wPeriodMin` is its first `UINT`.

### The formula, with real constants

Every authored duration in the game is a **30 fps frame count**, converted at the point of use:

```
frames_to_wait = authored_constant * (*(int*)0x01DFE0B4)
```

The multipliers actually present in the image — ten distinct `imul <reg>, [01DFE0B4], N` sites — are
**30, 60, 90, 150, 240, 900, 1200, 1500, 9000, 30000**. Divide each by 30 and every one is a whole
number of seconds: **1, 2, 3, 5, 8, 30, 40, 50, 300 and 1000 seconds.** That is the confirmation that
`N` is a 30 fps frame count and `01DFE0B4` is the conversion factor, not a speed control.

Worked through: a fifteen-second timer is authored as `450`.

```
FrameLimit=30 :  450 * 1 =  450 frames  /  30 fps  = 15.0 s
FrameLimit=60 :  450 * 2 =  900 frames  /  60 fps  = 15.0 s
```

**The wall-clock duration is identical. That is the point of the multiplier.**

### `01F82E38` — a process-wide "running at 60" gate

The flag written alongside the time base has, across the whole image, **exactly one write — the one
above — and thirteen reads, ~~every one of them `cmp dword ptr [...], 0`~~ not all of them `cmp` — `001EDE70` reads it with `mov eax, [01F82E38]`** *(corrected 2026-10-02, OPUS: `retool.py refs 01F82E38`, 13 reads and 1 write; the list below omits `001EDE70`)*, in thirteen different
functions clustered in `001EC6B0`–`001EDEC0`:

```
001EC6B6  001EC776  001ED026  001ED0DA  001ED1E4  001ED270  001EDAE9
001EDBD0  001EDCD6  001EDDA9  001EDE84  001EDEC0      (+ the write at 001EDDE8)   <- corrected 2026-10-02, OPUS: the read in 001EDE70 (mov eax, [01F82E38]) is missing from this list
```

> **Thirteen functions branch on whether the game is running at 60**, and at 30 the flag is BSS and
> stays zero forever, so all thirteen take their other branch permanently. **~~What those thirteen do~~
> ~~is not read here~~** *(answered: see §17.3, `DH-3` — four accessors and nine content exceptions; 2026-10-02, OPUS)* — but the shape is worth recording: this is not a value, it is a mode switch
> with thirteen consumers.

### The seven initialisers that only run at 60

`FUN_0033F020` (43 B) is **six calls and a tail jump** — seven targets, not six:

```
0046FBF0   00471100   00471330   004715F0   004718F0   00472580   00473210
```

It has **exactly one caller, `001EDDC0`, inside the `isSixty` branch**, so all seven run only at 60.
The ledger assigns six of the seven to `Presentation` — **that is a tag, a prior session's claim, not
a reading**~~; none of the seven has been disassembled here~~ *(answered: see §17.2, `DH-4` — they convert authored presentation timing tables at boot; 2026-10-02, OPUS)*.

### `DH-2` answered — there is no 4x mode

The previous formulation asked whether some path writes a mode other than `2`, and could only say
"no 4x variant was found" — an absence from an unbounded search. **The source side closes it:**

- `FrameLimit`'s value-name row is **exactly two entries, `"30"` and `"60"`**, NULL-terminated. The
  parser can only ever store `0` or `1`.
- `0022BDF0` reduces even that to a boolean: `xor ebp,ebp` / `cmp eax,1` / `cmove ebp,1`. **Any value
  that is not exactly `1` produces `0`** — so a hand-edited `GameSetting.ini` cannot reach a third
  mode either.
- `001EDDC0` is reached by **one `E9` tail call and nothing else** — no `E8`, no address in data.

**So `01DFE0B4` is `1` or `2`, and the engine knows no other time base**, established from the setting
that feeds it rather than from failing to find a writer.

### Why the default is `30`, and what that does and does not mean

`FrameLimit`'s row in the preset matrix is `0,0,0,0`, and **its mask byte at `0x00900CC0` is `0`** —
so the quality preset never touches it, and the value copied at init is column 0 = **`0` = `"30"`**.

> **The compiled-in default is 30.** What a shipped installation actually contains is a different
> question: `GameSettingConfig_LoadOrCreateFile` writes the file from these defaults **only when no
> file exists**~~, and this document has not examined an installed `GameSetting.ini` or the launcher~~ *(answered: see "What a fresh install writes for `FrameLimit` — 30"; 2026-10-02, OPUS)*.
> **The claim here is about the image's default, not about what players find on disk.**

### `FrameLimit` also filters the display-mode list

The 11-byte getter `0017D8F0` has **two raw callers**, not one. Besides `0022BDF0`, the display
object's mode-list builder `001DD420` reads it — reached from the display constructor `001DC5C0`
and the monitor setter `001DC7A0`. The builder reads `FrameLimit` at `001DD581` (`sete dil` on
`== 1`) and then compacts its array of 28-byte `DXGI_MODE_DESC`-shaped records
(`001DD5A6`–`001DD654`), keeping a record only if all three hold:

1. it is at least **1280 × 720** (`cmp [r8], 0x500`, `cmp [r8+4], 0x2D0`);
2. its refresh denominator is non-zero;
3. its refresh rate `numerator / denominator`, truncated to an integer, is in the set that
   `FrameLimit` allows.

| `FrameLimit` | refresh rates kept |
|---|---|
| `60` (value 1) | 59 and 60 |
| `30` | 29, 30, 59 and 60 (constants `008F8D80`, `00900A10`, `00900A14`, `008F6D54`) |

Records that fail are swap-removed. So the setting that picks the time base also decides which
fullscreen modes are offered. Which list the options screen shows from this array is not read.
(Crossing recorded on `09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md`, FINAL-AUDIT
pass 22; ported here 2026-09-16.)

### An aside: `-nologo`

The other half of `0022BDF0` is unrelated to timing, and is recorded here only because the two share
a function. It walks `argv` comparing **eight bytes** of each entry against the literal at
`0x00908BD8`, which is `"-nologo\0"` — exactly eight — and on a match calls `00314DE0`, a 7-byte
`mov dword ptr [0x022C2528], ecx; ret` with `ecx = 1`.

**`FFXII_TZA.exe` accepts a `-nologo` command-line switch**, and it sets one global. The comparison is
a fixed 8-byte run with no length check on the argument; the first mismatching byte exits the loop,
so a shorter argument is not read past its terminator unless its bytes happen to match.

### Corrections this section makes

| where | was | is |
|---|---|---|
| `09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md`, "What the writer actually stores" | `cmp byte [01F82E35]`, `mov ecx,[01F82E30]` | **`01F82E3C`** and **`01F82E40`** — both were hand-computed RIP targets; recomputed with the tool |
| the same document, "What this does and does not license" | "`FUN_0033F020` (six sub-initialisers)" | **seven** — six `call` and one `jmp` tail call |
| `00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md`, falsification row | "`0022BDF0` … is the writer of that global. **The ordering is the guard.**" | `0022BDF0` writes it only through the tail call, and **only at 60**. At 30 nothing writes it, and the safety of `2 / DAT_01DFE0B4` rests on the **`.data` initialiser `1`**, not on ordering |

## 13. Evidence — section 12

| claim | evidence | tier |
|---|---|---|
| `+0x48` is `FrameLimit`, values `"30"` / `"60"` | key table `01DFD050[18]`, value-name row `01DFD150[18*9 + 0..1]`, read from the image | 1 |
| `0017D8F0` reads `*(int*)(*(void**)0x01F82D20 + 0x48)` | 11-byte body disassembled; RIP target computed with the tool | 1 |
| `0022BDF0` passes `(field == 1)` to `001EDDC0` | `xor ebp,ebp` / `cmp eax,r15d(=1)` / `cmove ebp,r15d` / `jmp 0x1EDDC0` | 1 |
| The three WINMM imports | walked the PE import directory to the named thunks | 1 |
| `01DFE0B4/B8/BC` ship as `{1, 1.0f, 1.0f}` | read from `.data` **inside `SizeOfRawData`** — checked, not assumed | 1 |
| `01F82E38`, `01F82E3C`, `01F82E40` are BSS and load as zero | their offsets in `.data` exceed `SizeOfRawData` `0x18E400`; a naive file read returns `.pdata` bytes instead | 1 |
| `01F82E38`: 1 write, 13 reads, all `cmp …,0` | `data_xref_scan.py` with a passing control | 1 |
| `0033F020` has one caller and seven targets | `edges.tsv` plus the disassembled 43-byte body | 1 |
| The config object is built before `main` | `007980A0` ← `007A3770` ← `00808D78` (`MSVCCRT.ExecutableStartup`); `0022BDF0` is the first call in `0022A0B0` | 1 |
| `"-nologo"` at `0x00908BD8` | RIP target computed with the tool; 8 bytes read | 1 |
| `001DD420` reads `FrameLimit` and keeps only modes ≥1280×720 with integer refresh 59/60 (limit 60) or 29/30/59/60 (limit 30) | `001DD581` `sete dil` on `==1`; `001DD5A6`–`001DD654` compact loop over 28-byte `DXGI_MODE_DESC` records; constants `008F8D80`, `00900A10`, `00900A14`, `008F6D54`; callers `001DC5C0`, `001DC7A0` | 1 |
| What the thirteen `01F82E38` readers do | ~~**not read**~~ read, §17.3 *(answered: `DH-3`; 2026-10-02, OPUS)* | — |
| What `0033F020`'s seven targets do | ~~**not read**~~ read, §17.2 *(answered: `DH-4`; 2026-10-02, OPUS)* | — |
| What a shipped `GameSetting.ini` contains | ~~**not examined**~~ none ships; both writers default `FrameLimit` to 30 *(answered: "What a fresh install writes for `FrameLimit`"; 2026-10-02, OPUS)* | — |

### An independent re-derivation, unplanned

Section 12 was reached from the timing side, without knowing this document existed. Getting there
required re-deriving the whole settings schema from scratch: the **31**-iteration defaults loop, the
key table at `01DFD050`, the 31×9 value-name table at `01DFD150`, the 16-byte descriptor rows at
`00900CE0`, `ApplyQualityPreset` at `001DE4F0`, and the 31-byte mask at `00900CC0`.

**Every one of those matched sections 1–11 exactly** — the same 31 keys in the same order, the same
ten preset-driven settings, the same column-indexed-by-quality reading of the matrix. **Two
independent derivations, no disagreement.** Recorded because a confirmation that cost nothing extra
is still evidence, and because a re-derivation that found a discrepancy would have mattered a great
deal.

## 14. Two things the answer changes about how the question was asked

### 14a. Part of this answer was already in the database, in another category

**`DH-1` should not have been filed.** After writing section 12 a
`check_already_answered.py` sweep found that
[`../../15-Input/Binding-Profiles/keymap-ini-file-format-and-default-controls.md`](../../15-Input/Binding-Profiles/keymap-ini-file-format-and-default-controls.md)
already carried, in its address table:

```
0017D8F0  GameSetting_GetFrameLimit                  11 B  return *(u32 *)(GameSetting + 0x48)
0022BDF0  Startup_ParseCommandLineAndSelectFrameBase 146 B  -nologo, then HostTiming_Select(FrameLimit == 1)
001EDDC0  HostTiming_SelectFrameBaseAndTimerPeriod   165 B  the sole writer of 01DFE0B4/B8/BC
```

**The identification of `+0x48` as `FrameLimit` was three months of work old and one category away**,
while `DH-1` was being filed in `09-Combat-AI-And-Gambits` as "whether the argument reflects a display
mode, a config value or a constant is **unread**".

> **The rule this earns:** `check_already_answered.py` must run **before a question is filed**, not
> only before one is assigned. The same rule was recorded once already this week after `CR-1`; this is
> the second instance, and the first at the scale of a whole thread rather than a single question.

**What section 12 adds over that row** is everything past the name: the two branches are *mutually
exclusive* and the 30 branch writes nothing at all; the value names are literally `"30"` and `"60"`;
the compiled-in default is **30**; `01F82E38` gates **thirteen** functions; `FUN_0033F020`'s **seven**
targets run only at 60; and `DH-2` is closed from the setting's value-name row. The input document
named the road; it did not say where it went.

### 14b. The 4x that `DH-2` was worried about exists — in a different system

`DH-2` asked whether any path writes a time base other than `2`, and the worry is well founded,
because **FFXII TZA does have a 4x**. It is not this global.

| | speed control | time base |
|---|---|---|
| global | **`0x01FD4A98`** (`g_speedMode`) | `0x01DFE0B4` |
| set by | `GameSpeed_SetModeRaw` `00229ED0` (7 B, `mov [01FD4A98], ecx`) | `001EDDC0` only |
| read as | `GameSpeed_GetMultiplier` `00229E00` (20 B): `movsxd rax,[01FD4A98]` / `movss xmm0,[00908BA8 + rax*4]` | `imul <reg>, [01DFE0B4], N` |
| values | table at `0x00908BA8` = **`{1.0f, 2.0f, 4.0f}`** | `1` or `2` |
| driven by | the player's speed keys, every frame | `FrameLimit`, once at startup |

> **These are opposite operations on the same-looking numbers.** The **speed multiplier** makes the
> same authored durations elapse *faster* — that is the fast-forward the player holds a key for. The
> **time base** multiplies the authored durations so that they elapse in *the same wall-clock time* at
> a higher frame rate. One compresses time, the other preserves it.

**They cannot interact through `01DFE0B4`**, which has exactly one writer. So the answer to `DH-2`
stands as given in section 12 — the time base is `1` or `2` — and the `4x` the question was reaching
for is real but belongs to `g_speedMode`, whose 1x/2x/4x mapping is recorded by
[`../../15-Input/Binding-Profiles/keymap-ini-file-format-and-default-controls.md`](../../15-Input/Binding-Profiles/keymap-ini-file-format-and-default-controls.md).
**Verified here:** the multiplier table at `0x00908BA8` is three floats, `1.0 / 2.0 / 4.0`, indexed by
`0x01FD4A98`; index 3 onward is unrelated data (`"-nologo"` begins at `0x00908BD8`).

## 15. What section 12 leaves open

- [x] ~~**What the thirteen `0x01F82E38` readers do.**~~ **`DH-3` ANSWERED 2026-09-12 (FABLE):** four
  accessors (the flag, the HALFRATE test, the even-phase gate, the step count) and nine per-cutscene /
  per-asset exceptions, **all 60 fps-only branches** with neutral 30 fps defaults — §17.3.
- [x] ~~**What `FUN_0033F020`'s seven targets do**~~ **`DH-4` ANSWERED 2026-09-12 (FABLE):** they
  convert authored presentation timing tables in place at boot — frame counts doubled, per-frame rates
  halved, curves resampled — §17.2.
- [x] ~~**What the `-nologo` global `0x022C2528` gates.**~~ **`DH-5` ANSWERED 2026-09-12 (FABLE):** it
  is the "first start done" flag read by verb `isFirstStartDone`; the title script skips the ESRB,
  logo and autosave pages when set; a field restore also sets it — §17.4.
- [x] ~~**DH-7.** **What state decides HALFRATE.** *Narrowed 2026-09-12:* `mode` is the DXGI present sync
  interval (1 or 2, clamped to 3) and HALFRATE is 60 fps presenting at interval 2; open is what the
  `01F82E18` singleton's `+0x118` handle is and what `001DADA0()` `+0x88` is. `DH-7`, §17.3.~~
  **ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5).** Both predicate states are now named:
  - `01F82E18` is the handbook monster viewer, and `+0x118` is "the viewer has a model open". That half
    was answered 2026-09-19 on [the monster viewer page](../../16-UI/Handbook/the-handbooks-monster-viewer.md).
  - **`001DADA0()` is the FileCache singleton `[01F82CF0]`, and `+0x88` is its "map jump pending" byte.**
    It is set only by `001DA090`, which logs `"[FileCache] OnMapJumpBefore (%d)"` (`009006E8`), records
    the previous and next field ids at `+0x80` / `+0x7C`, and hands them to `0020C1A0`. `001DA090` is
    reached only through `001D6C40`, from `WorldTransition_RequestFieldTransition` (`00314508`) and
    `WorldTransition_RequeueCurrentFieldForRestore` (`003145CF`).
  - It is cleared only by the 7-byte `001DA080` (through `001D6C20`), the step that runs before a
    script `fadein` ([the fade page](../../17-Presentation-Rendering/Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md)).
    The constructor writes it once (`001D947B`).

  So `002507C0` presents at interval 2 unless a map jump is under way.
  Census: every write to `+0x88` in `001D9000`–`001DB200` plus the getter's call sites and the
  methods they pass it to.
- [x] ~~**UQ-268.** **Whether a shipped installation's `GameSetting.ini` says 30 or 60.** The image default is 30;
  what the installer, launcher or first run actually writes is not established from the binary alone.
  `DH-6`.~~ **ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): 30, whichever program writes it first.**
  - The install ships no `GameSetting.ini`.
  - Both programs that can create it default to `30`: the game's create path, and the shipped settings
    launcher `FFXII_TZA_GameSetting.exe`, whose IL maps a missing or unrecognised value to `FL_THIRTYFRAME`
    and saves `"30"`.
  - `60` appears only when the player chooses it.

  See [§ What a fresh install writes](#what-a-fresh-install-writes-for-framelimit--30-fable-claude-opus-55-2026-09-25).

## 16. Correction 2026-09-10 — `0x104` counts characters, and the `+0x554` span never existed

**What was believed.** `iniPath` at `+0x450` was a **260-byte** buffer, and a second, separate
**260-byte unresolved span** sat at `+0x554` that *"no config function writes"*. §1 and §8 both
recorded the length as `0x104` without a unit.

**What is now believed.** There is one field: `iniPath`, **`wchar_t[260]`, 520 bytes,
`+0x450`–`+0x657`**. `+0x554` is its midpoint.

**What proved it.** The copy at `001DE157` calls through IAT slot `008C3008`. Read straight out of
the PE import directory, that slot is `api-ms-win-crt-string-l1-1-0!wcscpy_s`, whose second
parameter is `rsize_t numberOfElements` — **wide characters**. `001DE152` loads `0x104` into it, so
the destination is declared `wchar_t[260]` = `0x208` bytes, and `0x450 + 0x208 = 0x658` is exactly
where the next PROVEN field starts. The register assignment is independently decisive: `rdx` holds
the immediate and `r8` the source pointer, the shape of `wcscpy_s(dest, count, src)` and not of
`wcsncpy(dest, src, count)`. It is the image's only `wcscpy_s` call site.

**Why the earlier reading was reachable.** `0x104` is a plausible byte count for a path, and
`260 = MAX_PATH` is a plausible *byte* length too if the buffer is assumed narrow. Read as narrow,
the field yields `"C"` — one character followed by a NUL high byte — which looks like a short
string in a 260-byte field. The validator then reported the remaining 260 bytes as an undeclared
span, and a displacement scan honestly found no writer for it, because a buffer's tail has no
writer. **The general shape of the mistake: a size taken from a CRT call without resolving which
CRT function it is.** Any other field whose width came from an import's length argument is subject
to the same error.

**Bounded negative control.** Every memory operand of `001DE050`, `001DED50`, `001DFD40`,
`001DF240` and `007980A0` was decoded over the full recorded body length. The only displacement in
`[0x440, 0x660)` besides `+0x448`, `+0x44C`, `+0x658` and `+0x65A` is `+0x450` itself. Positive
control: `+0x450` appears in three of those four config functions. **Search boundary: those five
functions only.**

**A second fact fell out of the same read.** The `0x65C` block is obtained at `00798239` through
`00210EC0` → `0085E730` → IAT `008C2B40` = `malloc`: **it is never zeroed.** The constructor's only
bulk clear is `memset(obj + 0x7C, 0, 0x3CC)` at `001DE138` (IAT `008C2A60` = `VCRUNTIME140!memset`),
covering `+0x07C`–`+0x447` and nothing else. So `+0x448` is **uninitialised heap** until `001DF240`
writes `0x51`, which is why a live read of a fresh process returned `0` where the contract claimed
*"always 81"* — a fresh OS page reads zero. The contract's §4a now carries the full initialisation
extent.

## 17. The 60 fps layer — the apply, the table conversions, the switches and the per-cutscene exceptions (2026-09-12, FABLE)

Section 12 established the time base. The rest of what `FrameLimit` changes is read here, because
it answers `DH-3`, `DH-4` and `DH-5` together and because it is the part of the game's timing a
reconstruction cannot infer from the time base alone.

### 17.1 The apply runs once, at boot

`001EDDC0(isSixty)` has one caller: `0022BDF0`, the command-line scan, tail-jumps to it
(`0022BE7D`) with `isSixty = (0017D8F0() == 1)` — the settings object's `+0x48`, the `FrameLimit`
index (`0022BE08`–`0022BE18`). So every conversion below happens exactly once per process and cannot
compound.

| arm | writes | calls |
|---|---|---|
| **60** (`isSixty != 0`) | time base `01DFE0B4 = 2`, scale `01DFE0B8 = 2.0`, inverse `01DFE0BC = 0.5`, **the 60 fps flag `01F82E38 = 1`** (`001EDDC8`–`001EDDF2`) | `0033F020` — the seven table conversions (§17.2); then, if the other arm had begun a timer period (`01F82E3C`), `timeEndPeriod(01F82E40)` (`001EDE01`–`001EDE17`) |
| **30** | `01F82E40 = wPeriodMin` from `timeGetDevCaps`, `01F82E3C = 1` (`001EDE1F`–`001EDE46`) | `timeBeginPeriod(wPeriodMin)` — the Windows timer resolution is raised only in this arm |
| both | — | `0032AE70`, `003333D0`, `00337A00`, then a tail jump to `002BDA90` (not read here) |

The three `WINMM.dll` imports are named from the PE import directory (`008C2A90` `timeGetDevCaps`,
`008C2A98` `timeBeginPeriod`, `008C2AA0` `timeEndPeriod`). What frame pacing the 60 arm relies on
instead of a raised timer period is not read.

### 17.2 `DH-4`: the seven 60-only functions convert authored timing tables in place

`0033F020` calls `0046FBF0`, `00471100`, `00471330`, `004715F0`, `004718F0`, `00472580` and
tail-jumps to `00473210`; its only caller is the 60 arm (`001EDDFC`). Each converts image-initialised
timing tables in `.data` (`01F20530`–`01F264AA`) from 30 fps to 60 fps and rebuilds their curves:

- **frame counts are doubled in place** — `mov eax, [tbl]; add eax, eax; mov [tbl], eax` over the
  count words (`0046FBFF`–`0046FC4D`: `01F20530`, `01F20534`, `01F20538`, `01F2053C`, `01F20A98`;
  `0047321B`–`004732A8`: `01F24100`–`01F24110`, also mirrored to the bytes at `01F264A8`…);
- **per-frame rates are halved** — `mulps` / `mulss` by `0.5` (`00D22600`) over the rate vectors
  (`00473228`–`0047329E`: `01F24118`, `01F24128`, `01F2414C`, …);
- **the sampled curves are resampled to the new density** by three resamplers with the same shape —
  copy the table, then interpolate between neighbours with `0.5` / `1.0` weights: `0033E310` (cyclic
  float table), `0033E5E0` (bounded float table), `0033E990` (byte kernel), plus `0033ECE0` —
  each called as `(table, samples, lanes)`, e.g. `0033E310(01F21F40, 60, 1)` (`00471104`–`0047112D`).

The owner tags of the seven and the resamplers are `Presentation` / `Presentation.ProceduralPose.
TableResampling`; the tables' consumers are not enumerated here beyond one (`0046FAA0` reads
`01F2053C`). **Consequence for a reconstruction:** at 60 fps these tables are not the image's values —
a 60 fps run that loads the image data without the conversion plays those presentation curves at double
speed.

### 17.3 `DH-3`: the thirteen readers of `01F82E38` are four accessors and nine content exceptions

**The accessors** (image-wide callers from the raw `E8` / `E9` index):

| function | returns | callers |
|---|---|---|
| `001EDE70` | the 60 fps flag itself | 22 — input arbitration, character render, UI |
| `001EDDA0` | `0` iff **HALFRATE** (`01F82E38 != 0 && 01DFE0C0 == 0`), else `1` | 40 — actor runtime, presentation, effects, the action timeline |
| `001EDEC0(x)` | `1` unless HALFRATE; under HALFRATE `(~x) & 1` — "run on even phases" | 40 — UI, widgets, presentation |
| `001EDE80` | under HALFRATE `[02064AD8] + [02064AA8]`, else `1` — the number of steps this frame | 7 — `WorldActor_UpdateRuntimeAndScriptExecutionState`, character render, … |

`02064AA8` is incremented and reset by the main loop `0022A770` (`0022AD60`, `0022AD77`) and
`02064AD8` toggled by `0022A580` (`0022A646`–`0022A64F`). **HALFRATE is a sub-mode of 60 fps, off by
default**: `01DFE0C0` is `1` in the image and its one writer `001EDEF0` is called only by `00184960(mode)`
(from boot `0022A0B0`, `0022B7E0`, `00250540`, `002507C0`), which sets it to `1` and then to `0` when the
60 flag is set and `mode != 1`, or `02092748` is set with `00229EA0() != mode`, or `001EBA40()` `+0x118` is set (`00184960`–`001849A7`). What `mode` denotes is `DH-7`.

**`DH-7` narrowed 2026-09-12 — `mode` is the DXGI present sync interval.** `00184960(mode)` stores
`clamp(mode, 1, 3)` in `01F3DA18` (`00798E90`; getter `00184950`, eight callers that add it to per-frame
accumulators such as `0208F570`) and posts it to the render thread through a command whose callback
`0017ECB0` copies it to `01DF08F8`. The render side `006234A0` reads it back (`0017ECE0`) and calls
**`IDXGISwapChain::Present(interval, flags)`** through the swap chain at `+0x118` of its device object
(vtable slot 8, `+0x40` — `Present`'s slot; `0062361D`–`0062362C` and `006237C6`–`006237D5`); it drops to interval 0 when the
average frame time over the last 30 frames (`02CF2548` / `02CF2550`) exceeds **0.0158 s** for interval 1
or **0.0327 s** for interval 2 (`00D56048` / `00D56050`), with `DwmIsCompositionEnabled` consulted
(`00623517`) and `0022A040()`, `001EBA40()` `+0x118` and `00193D50()` `+0x1E9` tested on the same path (`006235CF`–`006235E8`; how each combines with the threshold is not traced here). The callers choose
the interval: boot passes 1 (`0022A15E`); `00250540` passes 1 at 60 fps and, at 30 fps, `2` while
`001EBA40()` `+0x118` is set, else 1 (`00250546`–`00250568`); `002507C0` passes `2` when `001D6B70()`
(`001DADA0()` `+0x88`) is zero, else 1, with `02092748` raised around the call. **So HALFRATE means "the
60 fps build is presenting every second refresh"**: under it, the phase-gated work in §17.3's accessor
table runs on alternate frames and `001EDE80` reports the step count from the two frame counters. The residue is the state behind the two
predicates: `001EBA40()` is a `0x2E0`-byte singleton (`01F82E18`) whose `+0x118` byte is set by
`001EB9C0` when it opens a handle through `002EE9C0` (kept at `+0x130`, keyed by `001C6320()` at
`+0x120`) and cleared by `001EB940` / `001EB7B0`, which close it through `002EEB20`; what that handle
is, and what `001DADA0()` `+0x88` is, are not read. *Answered for the handle 2026-09-19 (FABLE): it is a slot of
the handbook monster viewer's staged model loader, and `+0x118` is "the viewer has a model open" -
[the handbook's monster viewer](../../16-UI/Handbook/the-handbooks-monster-viewer.md). `001DADA0()` `+0x88` stays unread.* *Answered 2026-09-25 (FABLE, Claude Opus 5.5): the FileCache's "map jump
pending" byte, set by `OnMapJumpBefore` `001DA090` on every field transition and cleared before the script
fade-in (`001DA080`); see the DH-7 box.*

**The nine exceptions** — each first tests the 60 fps flag and returns its 30 fps default otherwise; most
also consult `001EC560()` (a cutscene slot `01DFE40C` 0–4 whose flag at `01F832B0` is set, and the
field-frame hold `00265680`), and they key on **the story progress variable** (`FieldData_GetVariable0`,
[the flag banks](../../14-Story-Event-Quest-Hunt/persistent-flag-banks.md)), the cutscene slot's state word
and **asset names** matched with `strstr`:

| function | caller | keys | 60 fps result | 30 fps default |
|---|---|---|---|---|
| `001EC6B0(name)` | `00418880` | `m1009`, `m1266`, `m1222`, `m1223`, `m1151`, `m1267` | `1` | `0` |
| `001ED020(name)` | `00418880` | progress `0x15AE` + state 1 + `g0111`; progress `0x15E0` + state 15 + `c1006` | `0.5` / `−1.0` | `0.0` |
| `001ED0D0(name, id)` | `00416FB0` | outside a cutscene: `hc1006` with `id == 0x57` | `0.0` | `0.5` |
| `001ED1E0()` | `004717E0` | progress `0x14B7` + state 4 | `1` | `0` |
| `001ED240(…, f)` | `00418880` | progress `0xD70`, `0x15AE`, `0x15E0` … with `g0999`, `c1019`, `c1004`, `c1005`, `n1018`, `n1210`, `c1021`, `c1006`, `mrm_g0100`, `bds_f0100`, `n1150`, `sum_j0001`, `sum_a0001`, `sum_f0001`, `sum_i0001`, `n1120_32`, `n1129`, `m1072_10`; float thresholds `81.5`, `95.5`, `301.0` … | per-case frame adjustments | `0` |
| `001EDAD0()` | `003D9150` | `sum_j0001` loaded, state 7, odd slot counter `01F832C4` | `1` | `0` |
| `001EDBB0(…)` | `002F2530` (effect frame advance — **interior read 2026-09-17, SWE2-FRONTIER**: `001EDDA0` ×2 over `02EBEF88`, `003A8950`/`002F31C0` arms at [`002F25CD`](../../_index/ADDRESS-INDEX.md), then a π/2- and −0.5-scaled SSE stage writing the `022D92E0`/`022D92F0` vector pair — the same effect-parameter globals the `003A56F0` compute front fills) | in a cutscene: `spc_z0000` with `01EF9218 == 8` and the slot counter `01F832C4 == 0x39F`; outside one: arguments `(odd, 1, 0x14A)` | `1` | `0` |
| `001EDCD0(name)` | `0040ACF0` — interior verified 2026-09-17 (SWE2-FRONTIER): 1,153 B, `0020E600` ×7 first at [`0040AD13`](../../_index/ADDRESS-INDEX.md), `003D8E50` ×4 + `00415EE0`/`00413C80` ×3 | in a cutscene: progress ∈ {`0xDC`, `0xE1`, `0x190`, `0x294`, `0x37A`, `0x3E8`, `0x618`, `0x67C`, `0x6D1`, `0x6DC`, `0x712`, `0x76C`, `0x8F2`, `0xFD2`, `0x1086`}; otherwise `m1126` | `1` | `0` |
| `001EC760` (2,232 B) | `0022A770` (main loop) | `spc_z0000`, `sum_m0001`, `sum_l0001`, `sum_h0001`, `hne_e0100`, `wdl_b0101` and ~40 progress / id compares | calls `0024DE30` / `0024FCE0` | `1` |

**So `DH-3`'s "which side" is settled: every exception is a 60 fps-only branch**, and each returns its
neutral value at 30 fps (`0` / `0.0` / `1`, or `0.5` for `001ED0D0`). They are hand-written corrections
to specific cutscenes, summons (`sum_*` events) and character or monster assets (`c1006`, `m1126`, …)
whose authored timing was made for 30 fps. What each correction changes on screen — which pose, effect
or camera — is read only as far as its caller; the callers are Presentation functions (`00418880`,
`00416FB0`, `0040ACF0`, `003D9150`, `002F2530`) and the main loop. `00418880` itself — the 7,148-B
dispatcher that calls three of the rows above — is interior-read 2026-09-17 (SWE2-FRONTIER):
`0046D110`/`0046E8B0` head the body ([`004188F9`](../../_index/ADDRESS-INDEX.md), `00418922`), then the
`0041xxxx` case family (`0041A470` ×11, `0041A7F0` ×9, `00418650` ×7, `0041D180` ×6) over
`0046D730`/`0046D350`/`0046D380` progress reads and `0020E600` ×8 — consistent with the
progress-keyed scene-correction dispatcher the table describes. `00413C80` — the 7,253-B body
`0040ACF0` calls — is interior-read the same day (SWE2-FRONTIER): a per-row evaluator of the
`0040FF30` weather type (`0020E600` ×51 row lookups first at [`00413CF2`](../../_index/ADDRESS-INDEX.md),
`0036DD80` ×9, `00861F14` ×7) over the `01EC3E1F`/`01EC3FAB`/`01EC414E` constant bank.

### 17.4 `DH-5`: `-nologo` is "first start done"

`022C2528` has two writers — the argv scan's `-nologo` match (`0022BE54` → `00314DE0(1)`) and
`WorldTransition_RequeueCurrentFieldForRestore` (`003145C5`, `= 1`) — and one reader, `00314930`, whose
only caller is the handler of script verb **`isFirstStartDone`** (`0x05A7`, `0034FDA0` →
`VMResult_WriteInt32`). The one shipped script that calls it, the title script `ttl_a01`, shows the
**ESRB rating page**, the **logo page** and the **autosave notice page** only while it returns `0`. So
`-nologo` makes the first boot behave like a return to the title: no rating, logo or autosave pages;
and once a restore has requeued a field in this process, the title flow skips them too.

### 17.5 The `001EDDC0` exclusive subtree — all 10 members bound (SWE2-FRONTIER, followup queue)

The exclusive-callee census assigns the frame-base apply **10 frontier functions** — the whole
subtree is the 60/30 fps adaptation §17 described in passing. Interior cites are one instruction
inside each declared extent (`interior_cite.py`; no boundary crossings).

| cluster | members | role | interior |
|---|---|---|---|
| both-arms scaling | `0032AE70` (67 B), `003333D0` (30 B), `00337A00` (71 B) | `0032AE70` — reads the 60 flag via `001EDE70`: at 60 writes `float(pow-like CRT double)` to `022C3180`, at 30 a constant float (`01CEBBD8`); `003333D0` — `int(const × scale[01DFE0B8]) << 2` → `02EC0F90`; `00337A00` — `base[01DFE0B4] × 0xF0` → `02EC0F80` and a double-reciprocal rate `1/(x/(base×30))` → `02EC0F84` — all three scale authored frame counts by the chosen time base | `0032AE85` / `003333E0` / `00337A32` |
| tail interval table | `002BDA90` (78 B) | the apply's tail jump: reads `01DFE0B4` and writes five scaled byte intervals — ×2+base, ×15, ×4+base, ×25, ×30 per unit — into `0209E610`–`0209E614` (per-tick counts that double at 60) | `002BDAAA` |
| 60-only driver | `0033F020` (43 B) | six `call`s + tail `jmp 00473210` — the seven 60-arm conversions §17.2 enumerated | `0033F02E` |
| cyclic resamples | `00471330` (65 B), `004715F0` (65 B) | identical shape: double the count word (`01F22120` / `01F221B0`), then `0033E310(table, 2n, 1)` twice (call + tail) — two cyclic float-table resamples each | `00471350` / `00471610` |
| mixed resample | `004718F0` (165 B) | doubles three count words (`01F223A0`/`01F223A4`/`01F223A8`), then `0033E310`, `0033E5E0` ×2, `0033ECE0` ×2 — one table family needing all three resampler shapes | `00471974` |
| byte-kernel family | `00472580` (645 B), `0033ECE0` (819 B) | `00472580` — the largest converter: `mulps × 0.5` (`00D22600`) halves rate vectors at `01F227E0`+, doubles ~14 counts, then fifteen `0033E990(table, 2n, 3)` byte-kernel resamples; `0033ECE0` — the fourth resampler itself (per-lane interpolation over a `memcpy`'d table copy, `01F44830` staging) | `00472753` / `0033EDC7` |

The other three §17.2 targets — `0046FBF0`, `00471100`, `00473210` — are *not* exclusive to this
subtree (they have other callers) and so are not census members; the binding above is the census
set exactly.

## 18. The `007980A0` exclusive subtree — what constructing the config object runs

The exclusive-callee census assigns 54 frontier functions to `007980A0`, the config-object
constructor that `007A3770` calls during C-runtime static initialisation (§12). All 54 were
signature-swept 2026-09-15 (`bshape.py`); they decompose into six clusters:

| cluster | members | role |
|---|---|---|
| interface populate | `001DE5D0` (1,919 B — **`GameSettingConfig_ParseText`, corrected 2026-09-17:** a `key=value` line parser, not a table fill — see note below), `001DDC40` (430 B, 8 more indirect calls), `001DED50` (wires `001DE5D0` + `001DF240` + `001DFD40`), `001DF240` (`01DFDA10`/`01DFDB60`/`01DFDCB0` triples), `001DF760` (5 indirect calls) | `001DED50` installs the object's method/interface table; `001DE5D0` is one of the methods *being* installed |
| input-binding readers | `0020C730` (263 B, `0020CCC0` + `008C3180`/`00906360` consts), `0020CCC0` (105 B, `01DFE0D0`), `0020CD30` (`00210EC0` + `0020C730`, `01DFE410`), `0020CD80` (`00809950`, `01F83450`) | the `008C31xx` constant block + `01DFExxx` state the input-stack page's `+0x64` field sits beside |
| settings-block bodies | `00607FA0` (1,292 B — `01F7F5A0`/`02CF7480`/`02CF7A30` banks, 15 helper calls; interior verified 2026-09-17, SWE2-FRONTIER — `01F44830` base at [`00607FC8`](../../_index/ADDRESS-INDEX.md), `0016D6A0`/`0016D680` alloc pair ×3 + `0062C820`), `00607E20`, `00607F00`, `00609870`, `00609950`, `0060E9C0`, `0060EF70`, `00615790`, `0061CE30`, `006264F0` (1,173 B — interior verified 2026-09-17, SWE2-FRONTIER: `005CDAA0` first at [`0062658C`](../../_index/ADDRESS-INDEX.md), `005FCF20` ×4 + `005FD050` ×3 + `005CD7D0` ×2), `00626990`, `0062C570`, `0062C820`, `006343E0`, `0063C730` (`02CF8264`/`02CF94EC`), `0064A0E0` (1,050 B — `02D34718`/`19` flag bytes; interior verified 2026-09-17, SWE2-FRONTIER — `001B7170` first at [`0064A123`](../../_index/ADDRESS-INDEX.md), `00671B10` ×4 + `00674610`/`00674230` ×2), `00607D20` (245 B — `00D4A7B0` block + `0016D6A0` free), plus leaves `00599460`, `005DBFC0`/`005DBFE0`, `005F0590`, `005FE190`, `0061C540`, `006AA340` | the `005xxxxx`/`006xxxxx` band — per-setting block init over `01F7F5xx`/`02CF7xxx`/`02CBxxxx` banks |
| settings-load band | `0079F150` (1,515 B — the master populate; calls `00792760`, `0079D430`, `0079E4A0`, `0061CE30`, `0064A0E0`, `0063C730`, `00607D20`, `00797910`, `00607E20`, `006AA340`, `0060E9C0`, `0079E3D0` + 14 more; interior verified 2026-09-17, SWE2-FRONTIER — `01CB2xxx` key-name loads begin [`0079F1E5`](../../_index/ADDRESS-INDEX.md) (`"Trying to"`, `"INFO:Se"`, `"0:TimeSt"`, `"InputSou"`), `005CDAA0` ×6 + `00584730` ×3 register calls, double `01CB3CF0` loaded for a float default), `0079B300` (1,353 B — 35 indirect calls, `008C22xx` key strings; interior verified 2026-09-17, SWE2-FRONTIER — `01F44830` base at [`0079B31F`](../../_index/ADDRESS-INDEX.md), `001DF340` ×4 plus the `00808C40`/`00808F10`/`00861EBA` driver thunk triple), `00792F10` (key strings `008C2118`–`008C2410`), `00797910`, `007979B0`, `0079FA00` (`00408ED0` ×2 + `001F3ED0`), `007A0C60` (`00861ED2` ×9 — repeated float parse), `007A3810` (`01CB3EF8`–`01CB40B0` table), `00792690`/`00792760` (`01CB24xx` strings), `0079D430`, `0079E3D0`, `0079E4A0`, `0079E520`, `007A0FC0`, `007A3D70`, `007A4240`, `007A4250`, `00791A60` | the ini-table populate — `008C2xxx` `.rdata` strings are the key names, `01CBxxxx`/`01F4xxxx` the destination cells |
| tail helpers | `008655E0` (`00210EC0` + `01CCFCA0`), `00865660` (`00809950` + `01CCFBC0`/`02EB3860`) | late-bound pair behind the `008C3178`/`008C3180` consts |
| authored settings-block tail | `001DF240` also reads `01DFDA10`/`01DFDB60`/`01DFDCB0` — the three 81-dword source tables | **CORRECTED 2026-09-20 (OPUS), CON-122.** This row read *“the same `01DFDxxx` request-ring family the field frame’s mailbox uses — cross-system state the constructor snapshots”*. Both halves fail. The family was inferred from the shared address prefix, and the prefix is **this page’s own subsystem**: `01DFD050` is the 31 × `char *` key table (§ the parser’s `rdx=[r12+rdi*8+0x1CDD050]` at `001DE893` resolves there, `r12 = 0x120000`), `01DFD148` its NULL, and `01DFD150` begins **31 per-setting enum value-name arrays of 9 qwords each** (`jp…cn`, `SM_WINDOW…`, `VQ_LOW…`, `MSAA2X…`, `30`/`60`, `Circle`/`Cross` — 70 names) running `31 × 0x48 = 0x8B8` to `01DFDA08`; `valueTableA` starts at `01DFDA10`, 8 bytes of padding later. The tables are the **tail of one contiguous authored settings block**. Nor are they snapshotted for anyone: a fixpoint census over the config pointer (77 fns) finds **four** accesses in the whole `0x3CC` range and all four are `001DF240`’s writes — **no reader exists**. What stands: the copy itself, and that the tables’ **meaning is not yet established** *(reworded 2026-09-30, SWE2-DATA, for FINAL-AUDIT pass 4: the open point is the three tables’ content; `001DF240` itself is classified to Save_Load_Settings)* |

What this establishes: the constructor is not a small `memset`-and-defaults body — `001DED50`
wires the method table (`001DE5D0` + `001DF240` + `001DFD40`), then a settings populate (`0079F150` → the `0079xxxx`/`006xxxxx`
band) that reads authored key strings from `008C2xxx` and writes the `01CBxxxx`/`01F7F5xx`/
`02CF7xxx` cell blocks. Not established: which `.rdata` string each `0079B300`/`00792F10`
indirect call pairs with which destination cell (the pointer table ↔ key pairing is not walked).
The `001DE5D0` question is **answered 2026-09-17 (SWE2-FRONTIER):** neither a vtable nor a
handler registry — all 34 rip-indirect calls target `.rdata` **IAT slots** `008C25E0`/`008C2550`/
`008C2798`/`008C2A18`/`008C3000`/`008C2DA8` etc. (qwords into `01CCxxxx` CRT/std code). The body
is the `GameSettingConfig_ParseText` the key table already names: std::string locals at
`rbp+0x70`/`+0xb0` (SSO cap `0xF`, `001DE616`–`001DE628`), `byte[rdx]` null test + `or r8,-1`
length scan (`001DE62F`–`001DE639`), `strchr`-class `=` split via `edx=0x3d` at `001DE7EC`,
key lookup by indexed load `rdx=[r12+rdi*8+0x1CDD050]` (`001DE893`), two `0017D280` diagnostics
(`001DE8D0`/`001DEB3C`), CFG-guarded tail (`00808C40` at `001DED2E`).

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL.*

- **Movement — CLIENT.**
  - `WorldActor_UpdateRuntimeAndScriptExecutionState` reads the half-rate test `001EDDA0` and the per-frame gate body
    `001EDE80`.
  - The frame-base setup `001EDDC0` calls a 71-byte movement helper.
  - The world-tick entry gate `00265680` is read by a 475-byte movement body.
- **Party — CLIENT.**
  - The main loop `0022A770` commits a pending party focus handle (`PartyFocus_CommitPendingPackedActorHandle_Th…`).
  - The world-tick gate is also asked by `PartyFocus_ProcessActorControlPresentationSt…` and
    `PartyControl_ApplyAnalogLocomotionToActor`.
- **Developer — SERVICE and CLIENT.** `001EB9C0` calls a 2,261-byte Developer-filed body, and `001EBA40` (the object
  whose `+0x118` gates the path above) is also called by that body.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Spawn_Encounter_Lifecycle — CLIENT.** A 432-byte function this page cites is called by a 110-byte spawn body.
- **CombatAction — CLIENT.** The same 432-byte function is called by `BattleAction_UpdateSpecialPresentationSequence`.
- **CombatFormula — CLIENT and SERVICE.** The same 432-byte function is called by `BattleStats_InitializeDefinitionRecord`, and calls `BattleStats_ReconcileCurrentHpToEffectiveMaximum` and `BattleStats_ReconcileResourcesToEffectiveCapacity`.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Gameplay — CLIENT.** `BattleSystem_ResetRuntimeState`, owned by that layer, calls `00229ED0` on this page. That caller is the runtime reset: it walks **40 records of `0x1C8` bytes** from `[02EBF190] + 8` and resets each through `0023AC80`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Rewards_Progression_Economy — SERVICE.** `0023AC80` on this page calls `FUN_0030c470`, owned by that layer. What it reaches is a per-record step that reads the `byte[+4]` / `byte[+5]` kind-and-state pair and clears `byte[+0x1C2]`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Application — CLIENT.** `0071F970` on this page — a callee of the settings-load body `0079D430` — is also called by a body in that layer's census. The crossing is that the layer consults this page's function, not that this page owns anything in that layer. MECHANICAL accounting (SWE2-EC7, 2026-09-19).


**Presentation — CLIENT (SWE2-EC7-156, 506 edges).** `00183A00`/`00183C60`/`00183EE0`/`00194xxx` call this page's `0016D680`; batch-121's `00416270` helpers `0020E600`/`0020E620`/`00861EBA` join the same fan-in — the render layer consults the config helpers, not a shared responsibility.

## The `00184960` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`00184960(mode)` — the page's DH-7 present-sync setter — member calls
`001EDEF0` twice (`0018496D` with `ecx=1`, `001849A2` with the
checked mode), gates on `dword[02092748]` (`00184980`),
`00229EA0()` vs `mode` (`0018498E`), and `001EBA40()`'s
`byte[rax+0x118]` (`00184997`); then member `00798E90(1)`
(`001849AE`), `00189120` context → `[rax+8]` + `0017ECB0` → tail
`005FEA50` (`001849D0`), and a `001B31D0` ×2 arm (`00184A02`,
`00184A0C`).

| member | role | interior |
| --- | --- | --- |
| `001EDEF0` (7 B) | the `01DFE0C0` sync-interval writer — `dword[01DFE0C0] = ecx; ret` | [`001EDEF0`](../../_index/ADDRESS-INDEX.md) |
| `00798E90` (27 B) | clamped mode store — `eax=3`, `ecx` clamped to `1` when `≥3` (`00798E95`/`00798E9F`), `dword[01F3DA18] = eax` (`00798EA4`) | [`00798EA4`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `001EDE70`, `00229EA0`, `001EBA40`,
`00189120`, `005FEA50`, `001B31D0`, `0017ECB0` (callback arg).

## The `006234A0` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

`006234A0` (142 B) — a settings-object update: vtable call
`[[rcx+0x110]]+0x378` (`006234B3`), `qword[rbx+0x118]` null-gate →
early `al = 0` (`006234B9`/`006234C3`), `0017ECE0` (`006234EF`),
`dword[rbx+0x18A4]` vs `0x1F` (`006234F4`).

| member | role | interior |
| --- | --- | --- |
| `0017D880` (40 B) | safe double getter — `001D50D0` (`0017D884`); null → `xorps` else `movsd xmm0, [rax+0xD70]` (`0017D893`); the `00796E20`/`+0xD50` work is sibling `0017D8B0` | [`0017D893`](../../_index/ADDRESS-INDEX.md) |
| `00182780` (47 B) | byte-compare — `00193D50` ×2 (`00182784`/`0018278E`), `byte[rax+0x1E9]` vs `cl`, `eax = 1` on match (`00182795`/`001827A5`) | [`00182795`](../../_index/ADDRESS-INDEX.md) |
| `0022A040` (55 B) | mode check — `ebx` vs `3`/`7` (`0022A050`/`0022A06A`), `002EFD20` (`0022A057`), `eax == 1` (`0022A05E`) | [`0022A057`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0017ECE0`, `001D50D0`, `00796E20`,
`00193D50`, `002EFD20`.


### Interior citation — frontier hub `0033E310` (2026-09-18, SWE2-EC7)

`0033E310` — 718 B, 4 callers: the cyclic float resampler named above —
after copying the destination block it runs nested loops over `(samples,
lanes)` weighting each output `0.5`/`1.0` between neighbour rows with
`idiv r11d` (`r11 = samples/2`) — the `mulss`/`addss` stores at
[`0033E416`](../../_index/ADDRESS-INDEX.md). Cookie-guarded, pure float
math, no I/O.
## SWE2-EC7-19 update (2026-05-15) — `001DFD40`/`007A4190` settings-init helpers

`001DFD40` (214 B) is one of the settings-entry bodies the CONTRACT lists (`007980A0`, `001DE050`…`001DFD40`…): ~~an IAT-driven buffered read over the entry's `+0x450` source~~ the settings file writer *(corrected 2026-10-02, OPUS: `001DFD7A` opens `+0x450` with `_wfopen_s` mode `L"wb"` (`00901018`), `001DFDE2` is `fwrite` and `001DFDEC` `fclose`; CONTRACT-game-setting-config.md, `001DFD40` = write file)* — `call qword[008C2E00]` opens it into an `rbp`-frame record (`001DFD7A`, `00901018` descriptor arg); when `[rbp]` is non-null it measures the source with `001DEE90` (`001DFD8C`), stack-probes `size+0xF` via `00808F10`, `00861EC0`-clears the scratch buffer, reads a second `001DEE90` into it, posts through `call qword[008C2F40]` (`001DFDE2`), and releases via `call qword[008C2F00]`/`call qword[008C20A8]` (`001DFDEC`/`001DFDF2`) — the read-measure-fill-post shape of the config-entry initialisers.

`007A4190` (155 B) is the `02EACF68`-guarded lazy init the `00798xxx` config entries (`007980A0`/`00798FF0`/`0079B160`/`0079EDD0`/`0079F150`) call: the TLS-slot version check (`ecx=[02EAED3C]` slot in `gs:[0x58]`, `[rcx+4]` vs `[02EACF68]`, `007A419F`..`007A41C0`) skips when current; behind `008092FC`/`0080929C` init-once bracket it runs `005CC900` on both `02EACF10` and `02EACF40` records, clears the `02EACF28`/`02EACF58` flag bytes, and registers `008B8620` for teardown via `00808B90` (`007A41CE`..`007A4214`). Returns `&02EACF10` either way (`007A4219`/`007A421E`) — the MSVC-style once-init the config entries' shared record pair needs before first use.
## SWE2-EC7-32 update (2026-09-18) — `001DE5A0` mod-3 config lookup + `001DFA00` SSO selector (via `001DF350`)

`001DE5A0` (46 B) is the resolution-path reader the ini page names:
`[rcx+0x1C]` reduced mod 3 (the `0xAAAAAAAB` magic divide) indexes
8-byte rows of `00900F00`; the answer packs the row's two dwords as
`(hi << 16) | lo`. The config's `+0x1C` picks one of three packed
word pairs. Interior anchor `001DE5C6` (the `shl eax, 0x10` pack).

`001DFA00` (15 B) — reached through `001DF350`, `001A7F10` and
`0020DE30` — is the CRT string buffer selector every parse helper
shares: `qword[rcx+0x18] >= 0x10` returns `qword[rcx]` (the heap
buffer), anything smaller returns `rcx` itself (the inline
characters). Interior anchor `001DFA07` (the heap-pointer load).

## SWE2-EC7-34 update (2026-09-19) - `0033E5E0`

`0033E5E0` (940 B) is an ini field accessor - 0x9C8 cookie frame, a `movsxd` index pair `(edx, r8d)`, one `00861EBA` libfn call. Interior anchor `0033E96B` (the `00861EBA` call).

## SWE2-EC7-34 update (2026-09-19) - `0033E990`

`0033E990` (834 B) is the sibling accessor - 0x2E0 frame, `movsxd` index pair, `shr r8,1`, `00861EBA`. Interior anchor `0033E9CC` (the `00861EBA` call).

## SWE2-EC7-34 update (2026-09-19) - `00415EE0`

`00415EE0` (911 B) is a record-registration pass - `movaps` copy `[rdx]`->`[rcx]`, `02CA43C0` state, 14 `0020E600` + 7 `0020E620` id-record calls plus the `00416xxx` internal arms. Interior anchor `00415F5A` (an `0020E620` call).

## SWE2-EC7-34 update (2026-09-19) - `0041A470`

`0041A470` (896 B) is a settings record reader - `[rdx+0x34]==1` gate, `movzx` word id, `0041B920`/`0041BB00`/`0041BA10`/`0041BC40`/`0041A7xx`. Interior anchor `0041A4E8` (an `0041B920` call).

## SWE2-EC7-35 update (2026-09-19) - `0079EDD0`

`0079EDD0` (797 B) is the settings load log/fail path - `"INFO: Wr"` and `"App fail"` strings, an `008C2F28` import call, `005CDAA0`/`00584730` plus the `007A42E0`/`007A4190`/`007A1320`/`007A12B0` family. Interior anchor `0079EDFF` (an `008C2F28` import call).

## SWE2-EC7-36 update (2026-09-19) - `001DD170`

`001DD170` (677 B) is a settings/ini body - `01F44830`/`01F82D20`, `001DF340`/`00861EC0`/`00210EC0` plus `00808C40`/`00624670`. Interior anchor `001DD1B2` (an `001DF340` call).

## SWE2-EC7-36 update (2026-09-19) - `00626990`

`00626990` (669 B) is a settings record op - `00861EC0`/`0017D260` pair. Interior anchor `00626AEF` (an `00861EC0` call).

## SWE2-EC7-38 update (2026-09-19) - `0063C730`

`0063C730` (474 B) is the `02CF8264`/`02CF94EC` settings-block body the page names - `01F2E340`/`01F2E330` fields, `006343E0`/`00584730`/`008092FC`/`00808B90`/`0080929C`. Interior anchor `0063C76B` (a `006343E0` call).

## SWE2-EC7-39 update (2026-09-19) - `0046D730`

`0046D730` (419 B) is a settings body - `01CEBB70`/`01CEBBA8`/`01F20520`, `00861F14` pair. Interior anchor `0046D770` (an `00861F14` call).

## SWE2-EC7-39 update (2026-09-19) - `0060E9C0`

`0060E9C0` (411 B) is a settings sibling - `0017D260`/`00861EBA`/`0063C0C0` plus three vcalls. Interior anchor `0060EA1B` (a `0017D260` call).

## SWE2-EC7-41 update (2026-09-19) - `007A3810`

`007A3810` (357 B) is a call-free multi-sub-record ctor - installs `01CB3EF8`/`01CB3F50`/`01CB3FA8`/`01CB4000`/`01CB4058`/`01CB40B0`/`01CB4108` vtables across `+0x38`-stride sub-records (`+0x38`/`+0x58`/`+0x78`/`+0x90`/`+0xb0`/`+0xc8`), `0xffffffff` id fields, and copies `dword[01F82D20+4]` (~~the locale id~~ `Resolution`, setting 1 *(corrected 2026-10-02, OPUS: `007A3847`–`007A3859` `mov rax, [01F82D20]` / `mov edx, [rax + 4]`; the key table puts `Resolution` at `+0x04`, the language at `+0x00`)*) into each `+0x10`. Interior anchor `007A3847` (the `01F82D20` read).

## SWE2-EC7-41 update (2026-09-19) - `00416FB0`

`00416FB0` (347 B) is a settings body - `01CEBBA8`/`02EBB750`, `0020E600` quadruple plus `001ED0D0`. Interior anchor `00416FDD` (a `0020E600` call).

## SWE2-EC7-41 update (2026-09-19) - `002EE9C0`

`002EE9C0` (343 B) is a call-free settings slot-table writer - `02164208`/`02164210`/`02164238`/`02164268`/`01EEBAA8`/`01EEBAD8` globals, `0xa`-bounded index, writes `ebx` into the `01EDCAB0`-region dword table. Interior anchor `002EEA27` (the table write).

## SWE2-EC7-43 update (2026-09-19) - `0079D430`

`0079D430` (289 B) is a settings-load body the master populate `0079F150` calls - `"Error opening : %s"`/`"%d:"` strings, `01CB29B0`/`01CB29C4`, `00584730`/`00597970`/`00598100`/`0059BD80`/`0059D920`/`0059F200`/`005CDAA0`/`0071F970`. Interior anchor `0079D458` (a `00584730` call).

## SWE2-EC7-43 update (2026-09-19) - `0079E520`

`0079E520` (283 B) is the Input-family settings/teardown body - `008C21D0`/`008C21E0` import calls, `01CEB638`/`01F403A8`-`01F403BC`, `0079B300`/`0079EDD0`/`0079F150`/`007A3D70`. Interior anchor `0079E53F` (a `0079B300` call).

## SWE2-EC7-44 update (2026-09-19) - `0020C730`

`0020C730` (263 B) is a body - `008C3180` x3/`008C3190` import calls, `0020CCC0`. Interior anchor `0020C78C` (the first import call).

## SWE2-EC7-45 update (2026-09-19) - `004717E0`

`004717E0` (239 B) is a body - `001ED1E0`/`0020E600`/`003E4350`/`003E5AD0`. Interior anchor `004717E9` (an `001ED1E0` call).

## SWE2-EC7-46 update (2026-09-19) - `0061CE30`

`0061CE30` (233 B) is a body - `0017D260`/`005DBFC0`/`00618FD0`. Interior anchor `0061CE6A` (an `0017D260` call).

## SWE2-EC7-46 update (2026-09-19) - `0041A7F0`

`0041A7F0` (228 B) is a body - `00409150`/`00409170`/`0041B460`. Interior anchor `0041A82B` (a `00409150` call).

## SWE2-EC7-47 update (2026-09-19) - `001EDAD0`

`001EDAD0` (214 B) is the `001EDAD0()` settings-table body - `001C50C0`/`001EC560` plus `008C2A08` import and `call [rax+0x18]` vcalls. Interior anchor `001EDAFC` (an `001C50C0` call).

## SWE2-EC7-47 update (2026-09-19) - `00609950`

`00609950` (219 B) is a body - `005CCB80`/`0061E2E0`/`00625F20`/`00626990`. Interior anchor `0060997C` (a `005CCB80` call).

## SWE2-EC7-47 update (2026-09-19) - `00607E20`

`00607E20` (212 B) is a settings sibling - `005CD160`/`00607F00`/`00607FA0`/`00615BC0`/`00616700`/`00624670`/`00624960`. Interior anchor `00607E4D` (a `005CD160` call).

## SWE2-EC7-48 update (2026-09-19) - `00609870`

`00609870` (209 B) is a body - `005CCB80`/`0061E270`/`00625F10`/`006264F0`. Interior anchor `0060989C` (a `005CCB80` call).

## SWE2-EC7-48 update (2026-09-19) - `00792690`

`00792690` (202 B) is a text-service body - `00597970`/`00598100`/`0059BD80`/`0059D920`/`0059F200`/`005CDAA0`. Interior anchor `007926D7` (a `00597970` call).

## SWE2-EC7-49 update (2026-09-19) - `001DCD30`

`001DCD30` (190 B) is a `movsx`-high-half config reader - `001A1E40`/`00808C40` plus a `008C2810` import call. Interior anchor `001DCD62` (an `001A1E40` call).

## SWE2-EC7-52 update (2026-09-19) - `007A1320`

`007A1320` (637 B) is a call-free intrusive-list detach - `[rcx+0x150]` sentinel, unlinks and self-links nodes at `[r8+0x30]`/`[+0x48]`/`[+0x90]`, zeroes `+0x10`/`+0x38`/`+0x40`. Interior anchor `007A134E` (the first unlink).

## SWE2-EC7-53 update (2026-09-19) - `0059F200`

`0059F200` (590 B) is a settings-load populate body - `0017D260`, a `00584730`-driven vcall loop (`call [rax+0x28]`/`call [r9+0x28]`), `0067B100`/`00861EBA`. Interior anchor `0059F268` (a `0017D260` call).


## SWE2-EC7-53 update (2026-09-19) - `0041BC40`

`0041BC40` (375 B) is a call-free bounds-checked record walker - `r10 = r14 + rsi*3` byte index, `byte[rdi + r10*4 + 3] > rdx+1` bound, 4-wide elements. Interior anchor `0041BC7E` (the bound read).

## SWE2-EC7-54 update (2026-09-19) - `0041BB00`

`0041BB00` (309 B) is a settings record reader body - `0041B3A0` single call. Interior anchor `0041BBB3` (a `0041B3A0` call).

## SWE2-EC7-55 update (2026-09-19) - `0041B920`

`0041B920` (238 B) is a call-free settings record enumerator - `byte[3]` index, `word[4]` cursor against the `word[rax+r10*8+6]` count, wrap-reset returns 1. Interior anchor `0041B955` (the table count word read).


## SWE2-EC7-55 update (2026-09-19) - `0041BA10`

`0041BA10` (238 B) is a call-free settings record enumerator sibling - 4-stride records, emitted field `&0x1FFFF` + `[rdi+0x30]`. Interior anchor `0041BA97` (the `&0x1FFFF` field read).

## SWE2-EC7-57 update (2026-09-19) - `0041B3A0`

`0041B3A0` (177 B) is a call-free settings record walker - `byte[3]`/`word` cursor over `0x1C`-computed/`0x8`-stride rows, `0x40`-bit leaf byte test. Interior anchor `0041B3F8` (the leaf byte test load).

## SWE2-EC7-59 update (2026-09-19) - `001EC6B0`

`001EC6B0` (164 B) is an indirect-only name matcher - `008C2A08` import calls against `"m1266"`/`"m1222"`/`"m1223"`/`"m1151"`/`"m1009"` literals, first-hit return 1 (six call sites). Interior anchor `001EC6E3` (the `"m1266"` `lea`).

## SWE2-EC7-60 update (2026-09-19) - `0041D180`

`0041D180` (156 B) is a call-free `02CA43DC` constant-block copy - ~10 `movss` loads into `[rcx+0xC]`-`+0x2C`. Interior anchor `0041D1AE` (the `+0xC` float store).

## SWE2-EC7-62 update (2026-09-19) - `00618FD0`

`00618FD0` (147 B) is a settings-runtime body - `00584730` single call plus three vcalls. Interior anchor `00619049` (a `00584730` call).


## SWE2-EC7-62 update (2026-09-19) - `00797910`

`00797910` (147 B) is a settings-load band body - `008088FA` single call plus four vcalls, `008C2290`/`008C3190`/`01CC71A0`/`01DFE0D0`. Interior anchor `0079795D` (a `008088FA` call).


## SWE2-EC7-67 update - `0079E4A0`

`0079E4A0` (128 B) is a game-settings body - `005DBF80`/`006253D0`. Interior anchor `0079E4C5` (a `005DBF80` call).

## SWE2-EC7-70 update (2026-09-19) - `0059BD80` record close measured

`0059BD80` (64 B) is the close body the settings-load and text-service
paths share: frees `[+0x10]` through `002150D0` and NULLs it; when
`qword[+0x20] > 0` it runs `001D6AA0([+0x28])` - the handle release - and
writes `+0x20 = -1`. Always returns 1; idempotent on a re-close since the
freed pointer and the `-1` sentinel both gate their arms.
Interior anchor `0059BD92` (the `002150D0` free call).

## SWE2-EC7-72 update (2026-09-19) - `00409150` bounded table read measured

`00409150` (22 B) is the bounds-checked `+0x40` table read the config
bodies share: `edx < 0` or `edx >= [+0xC]` returns 0; otherwise
`[rcx + edx*4 + 0x40] + ecx` - index-plus-base addressing into the
record's dword table.
Interior anchor `0040915F` (the `[rcx + rax*4 + 0x40]` load).

## SWE2-EC7-79 update (2026-09-20) - `006253D0` NvAPI/display-adapter init measured

`006253D0` (1,106 B) is the display-adapter enumeration the
settings callers drive: the `01F44830` config flag gates the early
arm; `008C2A90`/`008C29A0` (CRT entries) and `0065E5D0`/`0065E580`/
`00159340` run the setup; `005CDAA0` formats against the `00D553A0`
`NvAPI_*`/`00D553C8`/`00D553F8` strings with `0080F2CE`/`0080F2C2`
environment reads; the record's `+0x38`/`+0x10` virtuals enumerate
adapters, `02CF2544`/`02CF2540`/`02CED884` carry the state, and
`00625830`/`00808C40` finish.
Interior anchor `00625493` (the `0065E5D0` call).

## SWE2-EC7-85 update (2026-09-20) - `00409170` bounds-checked getter measured

`00409170` (25 B) is the indexed getter the settings callers run:
`0 <= edx < [rcx+0xC]` returns `rcx + word[rcx + edx*2 + 0x40]` as
a pointer; anything else returns 0 - call-free.
Interior anchor `0040917F` (the `movzx` table read).

## SWE2-EC7-93 update (2026-09-20) - `003676B0` + `00367200` measured

`003676B0` (17 B) is the flag-armed entry: `or word [02CDBE6], 0x800`
then a tail into `00367200` - the bit the settings callers set before
the pump runs.
Interior anchor `003676B5` (the `or`).

`00367200` (1,196 B) is the periodic pump itself: gated on
`02334A93` and a nonzero `02CDBE54` mode word, mode 2 runs a
`bp`-counted `00367ED0` poll that shifts seven word globals per pass
and copies a byte table, while modes 1/2/3+ drive the `bp`-scaled
countdown, the `0x6020000`/`0x1E04` record stamps, and the reset arm
that writes `0x80008000` triples, `0xFFFF8000` sentinels and mode
byte 3 across `02CDBExx`.
Interior anchor `00367285` (the `00367ED0` call).

## SWE2-EC7-109 update (2026-09-20) - `001F3EA0` measured

`001F3EA0` (43 B) is the CRT
guard `00197EE0` and `007980A0`
call: `call qword [008C2B20]`
runs the wrapped primitive with
`edx = 0`; only a `-1` answer
tails into `qword [008C2B10]`
(~~the failure/handler IAT slot~~ `_wmkdir`; `008C2B20` is `_waccess` *(corrected 2026-10-02, OPUS: the import directory names both; `001F3EA0` creates the directory when `_waccess(path, 0)` fails, checked at `001F3EA0`–`001F3EBE`)*),
otherwise it returns inline -
the checked-wrapper shape the
config file I/O uses.
Interior anchor `001F3EAB` (the
`008C2B20` call).

## SWE2-EC7-111 update (2026-09-20) - `001A6E20` measured

`001A6E20` (226 B) is the
needle find `001A7F10` and
`001DF350` run: `r9` is the
needle length, `r8` the start
offset against `qword[+0x10]`
size - an empty needle inside
bounds answers `r8`
immediately. The scan
memchrs `*r15` through
`008C2A18` in the remaining
window (`+0x18 >= 0x10`
selects heap vs inline
buffer), then `00861ED2`
memcmps the full needle; a
match answers
`found - buffer`, a partial
restarts at `found + 1` with
the window shrunk
accordingly, and a miss
answers -1.
Interior anchor `001A6E9F`
(the `008C2A18` memchr call).

## SWE2-EC7-122 update (2026-09-21) - the `00625830` device-init callees measured

`00625210` (441 B) is the
device-caps apply
`00625830` runs after
creation: `006250C0` sets
up, then two 2-iteration
loops walk the `r13`/`r13+0x10`
device pairs - each entry's
`vtable[+0x50]` reads its
info block, then
`vtable[+0x40]` on `[r15]`
applies it into
`r13+0x38`/`+0x48` outs with
a feature record whose
`+8` divisor comes from the
flags (`0x20` -> `>> 2`,
`0x40` -> divide, else
`0x27`/`1`).
Interior anchor `006252F9`
(the first `vtable[+0x40]`
apply).

`00624F70` (332 B) is the
buffer-pair create: `r8`/`r9`
default to `0x400000` and
`0x100000` and store at
`+0x30`/`+0x34`; a
0x28-byte descriptor on the
stack feeds two
`vtable[+0x18]` creates
into `rsi`-indexed outs,
then `0017D260(size, 0x10)`
allocates the `+0x38`/`+0x48`
pairs that are still null.
Interior anchor `0062501E`
(the first `vtable[+0x18]`
create).

`00624980` (681 B) is the
debug-draw device init:
`vtable[+0x18]` buffer
create, `vtable[+0x60]`
then three `vtable[+0x78]`
GUID queries (`01F2EEC0`,
`01F2F308`, `01F2F65C`,
`01F2FA88`) into `+0x20`/
`+0x28`/`+0x30`/`+0x38`, a
`vtable[+0x58]` input-layout
create over the
`POSITION`/`TEXCOORD`
semantic pair (`00D383A0`/
`00D38420`), a
`vtable[+0x18]` create of
the 0x50 x 4 constant
buffer at `+0x18`, and
`0061C550` names it
`"DebugDrawConstantBuffer"`
(`00D55508`). Any null or
negative stage exits 9 or
5.
Interior anchor `00624B9F`
(the `vtable[+0x58]`
layout create).

## SWE2-EC7-123 update (2026-09-21) - `00623320`, `006250C0` and the `006242C0` monitor enum measured

`00623320` (382 B) is the
interface-chain matcher
`00625830` calls during
device bring-up:
`0080F2CE` creates the
`00D55390`-GUID object, then
three nested
`vtable[+0x38]` queries walk
factory -> adapter -> output,
`vtable[+0x40]` (`edx =
0x1C`) fetches the mode list,
`0017D260` allocates
`count*0x1C` records, a
second `vtable[+0x40]` fills
them, and the scan writes
`[r15] = record+0` on the
first entry matching the
caller's (`r14d`, `ebp`)
pair. All three COM-style
handles are released with
`vtable[+0x10]`; the temp
buffer is freed with
`00584730` unless the bit-31
flag kept it.
Interior anchor `00623413`
(the second `vtable[+0x40]`
fill).

`006250C0` (322 B) is the
shared buffer-pair allocator
`00625210` runs first - the
same shape `00624F70` has on
its own object: `r8`/`r9`
default `0x400000`/`0x100000`
into `+0x30`/`+0x34`, two
0x28-byte descriptors on the
stack (flags `r8d|1` and
`r8d|2`, sizes `r8` and
`r10+0x10`), then a
2-iteration loop of
`vtable[+0x18]` creates into
`r14+rbx*8` and
`r14+(rbx+2)*8` slots that
are still null. Any negative
create exits 9.
Interior anchor `006251A8`
(the first `vtable[+0x18]`
create).

`006242C0` (450 B) is the
monitor walk `001DD420`
calls: on the `edx=0` path
`[+0x1880]`'s
`vtable[+0x38]` enumerates
and the loop re-queries
`vtable[+0x40]` (`edx =
0x1C`) per index, logging
`"[Monitor ..."` lines
(`00D55600`/`00D55620`)
through `005CDAA0`; the loop
count lands in `[r14]` as
`ebx - 1`. The `edx != 0`
path decrements `+0x1894`,
re-queries once, copies the
16-byte record the caller
passed at `[rsp+0x98]` into
`[rbx]` when nonnull, then
writes `+0x1898` and
`+0x18A0` - the pair
`00625F30` compares against.
Interior anchor `00624392`
(the loop's `vtable[+0x40]`
query).

## SWE2-EC7-124 update (2026-09-21) - the `02CED8xx` staged-copy trio and `0061C1C0` measured

`0061C540` (15 B) sets the
two staging pointers the
copy machinery uses:
`rcx -> 02CEDA18`,
`rdx -> 02CEDA10`.
Interior anchor `0061C547`
(the second store).

`0061C8A0` (118 B) is the
cursor-bound staged copy
`006C8CA0`/`006CA8D0` call:
`vtable[+0x90]` moves `edx`
bytes, then if `edx` is
below the `02CED880` global
cursor a second
`vtable[+0x90]` moves the
`(cursor - edx)` remainder
through the `02CED990`/
`02CED890` tables, and the
cursor is updated to `edx`.
Interior anchor `0061C8FF`
(the second `vtable[+0x90]`
copy).

`006187A0` (66 B) is the
flush `0061E760` calls: if
`02CED880` is nonzero it
runs `vtable[+0x90]` once
over the `02CED990`/
`02CED890` tables and zeroes
the cursor.
Interior anchor `006187CD`
(the `vtable[+0x90]`
flush).

`0061C1C0` (111 B) is the
mode mapper the save-image
family calls: a 6-case jump
table returns `1`, `2`, `4`,
or - for one mode - logs
`"FAN_NOT_SUPPORTED"`
(`00D554E0`) once behind
the `02CF6C3C` guard and
returns 5; out of range
returns 0.
Interior anchor `0061C206`
(the `FAN_NOT_SUPPORTED`
load).

## SWE2-EC7-124 update (2026-09-21) - 00618740 measured

`00618740` (91 B) is the
once-guarded register its
caller runs: behind the
`01F2DE88` flag it picks
`8` vs `1` on whether
`[+0x168]` is below
`0xB000`, then calls
`vtable[+0x220]` on
`[+0x110]` with the
`02CED840` table and raises
the flag.
Interior anchor `00618789`
(the `vtable[+0x220]`
call).

## SWE2-EC7-125 update (2026-09-21) - the stream-window init, the checkerboard fill, the vector delete, and the callback install measured

`00607F00` (154 B) is the
stream-window init
`00607E20` runs: it stores
the `02CB7FD0` descriptor at
`+0x98`, records the base at
`+0x28`/`+0x38`, computes the
element index as
`(r9d & ~0xF) / stride`
with the count as
`(arg >> 7) / stride`, lays
out the window bounds
(`+0x30` element pointer,
`+0x40` = 0, `+0x48` count,
`+0x50`/`+0x60` base,
`+0x58` = `r8 + r11*128`
limit, `+0x70` =
`r9d * 128`), and finishes
with `0060FA10(this)`.
Interior anchor `00607F83`
(the `0060FA10` call).

`005F0590` (94 B) is the
checkerboard fill `00607FA0`
runs over a fresh buffer:
`r8` rows by `r11d` columns
on a `r9` byte stride,
writing `0xFF00FF00` where
`(row ^ col) & 1` is even
and `0xFFFF00FF` where odd -
the magenta/yellow debug
pattern. Null buffer or zero
height exits silently.
Interior anchor `005F05D7`
(the pattern dword store).

`005F0330` (107 B) is the
array teardown shared by
`0060EF70` and `007936A0`:
for each of `edx` records on
a 0x138 stride it calls
`vtable[+0]` (the element
destructor) then frees the
block itself through
`00584730`. Null pointer or
zero count skips the loop.
Interior anchor `005F0368`
(the element-dtor call).

`005FE190` (15 B) is the
callback install `007980A0`
runs at init: `02CB6348 =
rcx` (the callback) and
`02CB6340 = rdx` (its
context) - the pair
`00600C20`'s drain loop
calls each wait retry.
Interior anchor `005FE197`
(the `02CB6340` store).

## SWE2-EC7-126 update (2026-09-21) - the ring-window wrap and the word reset measured

`0060FA10` (197 B) is the
wrap fix-up `00607F00`'s
init ends on: a live `+0x78`
runs `005CD840` first; then
for each of the two cursors
(`+0x38`/`+0x40` against
limit `+0x30` over base
`+0x28`, and `+0x60`/`+0x68`
against `+0x58` over
`+0x50`) it pushes the
cursor `+count` bytes
forward, wrapping to the
base when it passes the
limit, and clears
`+0x88`/`+0x90`. Interior anchor `0060FA58` (the
wrap subtract).

`005DBFC0` (29 B) is the
word-reset wrapper
`0061CE30` calls:
`00615790(this)` runs the
base reset, then `+0x28`'s
word is zeroed and the
object returned. Interior anchor `005DBFC9` (the
`00615790` call).

## SWE2-EC7-127 update (2026-09-21) - the triple device create measured

`00615790` (124 B) is the
three-slot resource create
`005DBFC0` calls during its
reset: after `005DBFE0`
initializes the object it
fetches the device root
through `005FD050`, takes
`[rax+0x108]` as the device
object, and issues three
calls through its
`vtable[+0xC0]` slot with a
stack mode dword - first
3 (into `rdi+0x10`), then
2 twice (into `rdi+0x18` and
`rdi+0x20`). The returned
object is `rdi`.
Interior anchor `006157C6` (the first `vtable[+0xC0]` call).

`005DBFE0` (14 B) is the minimal two-field reset `00615790` and `00625F60` share: clears the qword at `+0` and the byte at `+8`, then returns the object pointer — leaves the record zeroed but addressable for the caller's own populate.

Interior anchor `005DBFEA` (function `005DBFE0`).

`00599460` (60 B) is the `0x50`-record factory `0079F150` calls inside its settings-populate loop: allocates `0x50` via `00584740`, null-checks, then hands the block to `00597A70` for field init before returning it — the failure path is the `xor eax,eax` return, so callers must tolerate null.

Interior anchor `0059948C` (function `00599460`).

`00597A70` (131 B) is the `0x50`-record constructor `00599460`'s factory wraps: zeroes `+0x20`/`+0x30`/`+0x48`, sets `+0x28` and `+0x40` to `-1`, clears the `+0x38` byte, and when `rdx` is non-null runs `0059EE90` (the union-source payload fill) on the record; then installs vtable `00D26C60`, stores `0x0B` at `+8` and `001C26B0(rdx)` at `+0x10`, and finally swaps the vtable to `00D26CD0` with `+0x18` zeroed — a two-vtable construction sequence (RTTI `01CF20D0` -> `01CF23A8`) marking the object fully formed.

Interior anchor `00597AB6` (function `00597A70`).

`0040B780` (8458 B) is the first of `0040ACF0`'s three row-walk callees: `0020E600([rdx+8])` resolves the base, `byte[r13]` counts the loop, and `0020E600` runs 27 times over the rows with `00861F14`, `0036DD80`, `00380260`, `00380410`, `00380650`, `00808C40` - the per-row record evaluator's main walk.

Interior anchor `0040BB28` (function `0040B780`).

`00411650` (7405 B) is the second `0040ACF0` row-walk (`0040D890`/`0040FEF0` also call it): `0020E600([rdx+0x10])`, `byte[r15+4]` gates the loop, `0020E600` x27 with `0036DD80` x10 and `00861F14` - the sibling resolver over the `+0x10` table.

Interior anchor `004123C8` (function `00411650`).

`00413340` (2355 B) is the third `0040ACF0` row-walk: `0020E600([rdx+8])`, `byte[r15]` count, `0020E600` x54 with `00861EC0` and `0036DD80` - the compact sibling over the same `+8` table as `0040B780`.

Interior anchor `004136C9` (function `00413340`).

`00380410` (575 B) is the matrix-vector multiply `0040B780` calls: `[rcx]`'s four rows against `[rdx]`'s vector as pure `mulss`/`addss` chains through xmm6-15 with the result republished to the stack - the config path's transform helper.

Interior anchor `00380549` (function `00380410`).

`00476F40` (491 B) is the vector helper `00418880` calls: `[rdx]` and `[r8]`'s components multiply into xmm1/xmm6/xmm8/xmm10 partials through xmm6-12 with `00861F56` finishing - the config path's dot-length primitive.

Interior anchor `00476FF9` (function `00476F40`).

`00416270` (471 B) is the record copier `00415EE0` calls: `r8d` gates, four `movaps` copy the 0x40-byte source into `rcx`, `byte[rsi+3] * 0x50` re-indexes the `02CA43C0` cursor, `0020E600`/`0020E620` resolve `[rsi+4]`/`[rsi+0x24]`-keyed entries, and `00861EBA` tail-fixes - the config's struct copy with cursor rebase.

Interior anchor `004162D1` (function `00416270`).

`00416910` (447 B) is the 0x60-record copier `00415EE0` calls (sibling of `00416270`): `r8d` gates, six `movaps` copy the record into `rcx`, `02CA43C0`'s cursor is re-indexed by `[rsi+0xC]`, then `0020E600`/`0020E620` resolve keyed entries - the config's larger struct copy with cursor rebase.

Interior anchor `00416974` (function `00416910`).

`00416600` (436 B) is the 0x50-record copier `00415EE0` calls (sibling of `00416270`/`00416910`): `r8d` gates, five `movaps` copy the record into `rcx`, `02CA43C0`'s cursor is re-indexed by `byte[rsi+3] << 4`, then `0020E600`/`0020E620` resolve keyed entries - the config's mid-size struct copy.

Interior anchor `0041665E` (function `00416600`).

`00380260` (420 B) is the matrix-to-quaternion arm `0040B780` calls: `xmm2 + xmm1 + xmm3` sums `[rdx]`/`[+0x14]`/`[+0x28]` (the trace), `>= 0` adds `1.0f` then `00861F14` square-roots it, `w = 0.5 * root` and `0.5 / root` seed the component division, and `xorps`-zeroed fallbacks cover the negative-trace branches - the rotation conversion stored through `rdi`.

Interior anchor `0038029E` (function `00380260`).

`00416450` (420 B) is the fourth `02CA43C0`-cursor copier `00415EE0` calls (sibling of `00416270`/`00416910`/`00416600`): `r8d` gates, `movaps` copies a `0x40`-byte record into `rcx`, `byte[rsi+3] << 4` re-indexes the cursor, then `0020E600`/`0020E620` resolve keyed entries - the config's `0x40`-record copy.

Interior anchor `004164A6` (function `00416450`).

`004167C0` (332 B) is the 0x50-record commit `00415EE0` calls: when `r8d` is set it bump-allocates two 0x50 slots off the `02CA43C0` arena cursor and `0020E620`-registers them into `[rbx]`/`[rbx+4]`; always copies the 80-byte source record (5 movaps quads) into the slot and `0020E600`-writes the mirror - the config record's clone-into-arena step.

Interior anchor `00416814` (function `004167C0`).


## What a fresh install writes for `FrameLimit` — 30 (FABLE, Claude Opus 5.5, 2026-09-25)

**Answers UQ-268 and the open half of DH-6.** Two programs can create `GameSetting.ini`, and both
default to `30`.

**1. The install ships no settings file.** The Steam installation on this machine holds exactly two
`.ini` files, both under `ConfigData/`: `keymap.ini` and the Gaussian-filter setting. `x64/`
holds the game, the launcher `FFXII_TZA_GameSetting.exe` (SHA-256 `E35CEC8A…ADF515B`), its
`SettingsLoc.xml`, and the SharpDX and Steamworks.NET assemblies. The installer's first run has no
file to read.

**2. When the game runs first**, `001DED50`'s `_wfopen_s` fails and the create path writes the file
from defaults (the contract §7, `DEFAULTED → CREATED`). `FrameLimit` is not driven by the preset
mask, so it gets the constructor's column-0 value, which is `"30"`.

**3. When the launcher runs first.** Its IL was read by reflection, without running it
([`members/launcher_framelimit_il_events.ps1`](members/launcher_framelimit_il_events.ps1) →
[`members/launcher-framelimit-il-events.txt`](members/launcher-framelimit-il-events.txt);
[`members/launcher_framelimit_il_bytes.ps1`](members/launcher_framelimit_il_bytes.ps1) →
[`members/launcher-framelimit-il-bytes.txt`](members/launcher-framelimit-il-bytes.txt)).
- `ConfigForm.LoadConfiguration` reads `GetIniString("FrameLimit", "30FPS")` into a local (IL
  `0x40`–`0x4F`).
- `0x50`–`0x5B`: if it equals `"30"`, it branches to `0x6A`.
- `0x5D`–`0x68`: if it equals `"60"`, it branches to `0x72`.
- **Any other value falls through to `0x6A`**, which selects `FL_THIRTYFRAME`. That includes a
  missing key, whose default `"30FPS"` matches neither. `0x72` selects `FL_SIXTYFRAME`.
- `ConfigForm.SaveConfiguration` writes `FrameLimit` = `"30"` when the selection is
  `FL_THIRTYFRAME` and `"60"` otherwise (IL `0x0F8`–`0x148`).
- **So accepting the launcher's defaults writes `30` too.**

**This is consistent with the three files DH-6 found live.** The unscoped file says `30`, the value
either writer produces untouched. The Steam-ID-scoped file the game reads says `60`, and DH-6 already
showed the game had rewritten it, so it reflects a player's choice rather than a default.

**Not established here.**
- Which path the launcher writes, Steam-ID-scoped or unscoped. Its path builder sits in a type the
  reflection load cannot resolve without the Steamworks.NET dependency.
- Whether other storefronts ship a different launcher.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (FABLE, Claude Opus 5.5, 2026-09-25)

**Resource — PROVIDER.** The DH-7 answer names the FileCache singleton (`001DADA0` → `[01F82CF0]`):
its constructor `001D9400`, its `OnMapJumpBefore` `001DA090` and the clear `001DA080`, with their
wrappers `001D6C40` / `001D6C20`. The present-interval choice in `002507C0` reads one byte the
FileCache owns, `+0x88`. This page claims nothing about the FileCache's prefetch work beyond when
that byte is raised and lowered.

**Script_VM_Native_Bridge — CLIENT, at one remove.** The clear `001DA080` is reached through
`001D6C20`, which the raw call index shows called from `003559B0` and `00355EB0`, and jumped to from
`00254A90`. [The fade page](../../17-Presentation-Rendering/Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md)
reads this step as the one that runs before a script `fadein`.
So authored script ends the interval-1 window. This page says nothing else about those verbs.

*These two paragraphs cover only the edges the DH-7 citations add.* The page's earlier Resource and
Script_VM_Native_Bridge edges, from its `0017D280` diagnostic citations, are not dispositioned here.

`00416AD0` (260 B) is the count-driven record merge `0040ACF0` runs between a source and a destination record: three counted loops - `[rsi]` `0x40`-stride element pairs resolved via `0020E600` and copied by `00416BE0`, `[rsi+7]` `0x60`-stride elements whose `+0x28` floats are halved (`*0.5` from `01CEBB70`) and summed into the destination's, and `[rsi+0x28]` elements resolved the same way - the additive merge behind the config record combine

Interior anchor `00416B33` (function `00416AD0`).

`00416BE0` (967 B) is the vec4 half-blend `00416AD0` runs over its record pair: both `+4` offsets resolve through `0020E600`, then per element of count `[rbx+3]` it writes `dst = 0.5*dst + 0.5*src` (`xmm6` = `01CEBB70` = 0.5f) across the four floats at `+0xC`/`+0x10`/`+0x14`/`+0x18` - the 50% merge applied to each lane

Interior anchor `00416E2D` (function `00416BE0`).

`00159340` (213 B) is the `CSingletonCriticalSection` guarded-static accessor `006253D0` (the display-adapter enumeration) uses: the `02EAEA98` bit-0 once-guard double-checks around `lock` refcount `02EAEA128`, installs vtable `01CC6B60` at `02EAEA68`/`02EAEA70` and registers `008B9040` teardown via `00808B90`, then `00158F60()` runs under the guard with counter `02EAEA138` - returns that call's result

Interior anchor `001593A6` (function `00159340`).

`001EDCD0` (203 B) is the gated whitelist test `0040ACF0` runs: `01F82E38` must be set and `001EC560` must accept, then `00265270`'s u16 id is compared against a 15-constant set (0xE1, 0xDC, 0x190, 0x294, 0x37A, 0x3E8, 0x618, 0x67C, 0x6D1, 0x6DC, 0x712, 0x76C, 0x8F2, 0xFD2, 0x1086); outside the set it falls back to an IAT string compare against "m1126"

Interior anchor `001EDD03` (function `001EDCD0`).

`00476E70` (199 B) is the vec4 normaliser `0046D730` calls: dot(v,v) > 0 takes `00861F14` (sqrtf) and scales all four lanes by `1.0f/len`; a zero-length input writes the normalised diagonal `0x3F13CD36` (1/sqrt(3)) into xyz and 0 into w

Interior anchor `00476EBF` (function `00476E70`).

`001ED020` (174 B) is the module-probe bias `00418880` consults: gated on `[01F82E38]` and `001EC560()`, `00265270` supplies a setting id `ax` and `01DFE40C` indexes the `01F832B0` dword table (clamped 0..4); id `0x15AE` with table value 1 ~~probes `GetModuleHandle`-family IAT `008C2A08`~~ matches an asset name with `strstr` (IAT `008C2A08`) *(corrected 2026-10-02, OPUS: the import directory names `008C2A08` `VCRUNTIME140!strstr`; §17.3, asset names matched with `strstr`)* for `"g0111"` and returns `0.5f` when present, id `0x15E0` with value `0xF` probes `"c1006"` and returns `-1.0f` when present, else `0.0f`

Interior anchor `001ED07C` (function `001ED020`).
- **ActorEntity - CLIENT and SERVICE (13 edges).** `00265680`, `002EFD20`, `0036DD80` are also called by bodies filed to actor entity: `0025B600`, `00263660`, `0026C5D0` (+3 more); `003A56F0`, `0022A0B0` reach bodies filed to actor entity: `002368D0`, `00263C30`, `00263FF0` (+4 more) - shared machinery across the layer boundary, no shared ownership.
- **Platform - CLIENT and SERVICE (64 edges).** `00615BC0`, `005CD7D0`, `005FCF20` are also called by bodies filed to platform: `001DD420`, `00625830`, `006253D0` (+10 more); `00625830`, `001DD170`, `0079F150` reach bodies filed to platform: `0019A510`, `001DD420`, `005CC930` (+17 more) - shared machinery across the layer boundary, no shared ownership.
- **PlatformOnlineAchievements - CLIENT and SERVICE (22 edges).** `001F3ED0`, `00408ED0`, `001DF340` are also called by bodies filed to platform/online achievements: `0079FA00`, `00862A40`, `007A0C60` (+3 more); `007980A0`, `00197EE0`, `0020C730` reach bodies filed to platform/online achievements: `001F3ED0`, `007A0810`, `0020CCC0` (+8 more) - shared machinery across the layer boundary, no shared ownership.
- **RNG_Random_Selection - SERVICE (2 edges).** `0022A0B0`, `0022B7E0` reach bodies filed to random selection: `00379CF0`, `00379CD0` - shared machinery across the layer boundary, no shared ownership.
- **Status_Periodic_Terminal - CLIENT (1 edge).** `00265680` is also called by bodies filed to status/periodic terminal: `00310DB0` - shared machinery across the layer boundary, no shared ownership.
- **StoryEvent - CLIENT and SERVICE (4 edges).** `001C50C0`, `001EC560` are also called by bodies filed to story event: `001ED240`; `00418880` reaches bodies filed to story event: `001EC6B0`, `001ED240` - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT and SERVICE (30 edges).** `001EDEC0`, `00229EA0`, `001EDDA0` are also called by bodies filed to UI: `0018EEE0`, `0024B9B0`, `003FA790` (+19 more); `002507C0`, `0022A770`, `0023BD40` reach bodies filed to UI: `00367200`, `00254E50`, `00291D80` (+2 more) - shared machinery across the layer boundary, no shared ownership.
