---
system: The Config screen, its 24 rows, and what a setting change actually runs
category: 16-UI
status: AUDITED — the screen, its 24 rows and what each setting change runs are read; DI-2 answered 2026-09-14 (section 6: 02F9736A is newly pressed) and the row table read as text 2026-09-18 (section 4: the Graphics Settings rows and their help lines; the six kind-0 rows are text-less headings)
owner_layer: PrimaryOwner:UI
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 132 addresses cited - 13 data, 38 entry, 69 interior, 4 literal, 8 text-data, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-13
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-config-screen-pass-1 - all four instruments reproduce with their controls, including the 2,527 raw-qword count exactly and the three single code-operand references at their published addresses; the 24-row table reproduces with sequential ordinals and the published widget classes, and yields the kind split 0x6 / 2x13 / 3x1 / 5x4 so 18 of 24 rows build a child; CORRECTED: row 1's textA is 0x056E, above the published 0x050C..0x0539, and the scan denominator is 38,161 function bodies rather than 34,270 - the instrument's result is unaffected
  crossref_clean: true
  reopened_count: 0
---

# The Config screen, its 24 rows, and what a setting change actually runs

## 1. What the player sees

Open **Config** and you get a list: screen mode, image quality, brightness, vertical sync,
anti-aliasing, shadows, depth of field, frame rate, two sound rows, and a handful of headings you
cannot land on. Push **left** or **right** on a row and its value steps to the next option.

**That press is the only thing in the whole game that applies a graphics quality preset.** Nothing at
startup does it, nothing on a timer does it: the 31 settings are written once with defaults before the
title screen and then left alone until the player moves the **Image Quality** row.

This document establishes that, names every row, and says which stored setting each one edits.

## 2. Why this was hard to find, and what made it findable

`0023B330` and `0023B6F0` — the two functions that receive the button press — have **zero callers in
the call graph**. So does the function that builds them. They are reached the way the whole menu system
is reached: an address is materialised into a register with `lea` and handed to an object constructor,
which stores it at the object's `+0x00`. This is the mechanism recorded as **AR-4**, and the object
header is the one documented in
[the widget constructor and object sizes](../Widget-Object-Model/the-widget-constructor-and-object-sizes.md).

**Four instruments, each with a control positive for that instrument:**

| instrument | control | control result | `0023B330` | `0023B6F0` | `0023BD40` |
|---|---|---|---|---|---|
| `E8` call rel32 | `001DE4F0` | **1 site** (`001D5139`) | 0 | 0 | 0 |
| `E9` jmp rel32 | `001D1660` | **1 site** (`001CD049`) | 0 | 0 | 0 |
| code memory operand | `0023B6F0` | **1 ref** (`0023BFE2`) | 1 (`0023C0CD`) | 1 (`0023BFE2`) | 1 (`0023BCF8`) |
| raw `.rdata` / `.data` qword | `005C5230` | **2,527 occurrences** | 0 | 0 | 0 |

> **The `E9` instrument earns its place here.** `001CD040` reaches `001D1660` by a **tail jump**, not a
> call. An `E8`-only reading finds `001D1660` unreachable — it has zero call sites in the image.

Denominators: **38,161** function bodies scanned for the code-operand instrument (`functions.tsv`'s
row count — the 34,270 first published here is `progress.py`'s `engine_explained` denominator,
corrected §10; the instrument's results are unchanged, since a wider scan found the same three);
every section's raw bytes for the qword instrument.

## 3. The screen object

```
0023BCC0  open the screen, once      128 B   guarded by [0208E6C0] != 0
   +- 00244F50(size = 0x730, proc = 0023BD40, initMsg = {0, arg, 0})
        +- 002465F0 stores the proc at object +0x00      (widget constructor, prior art)
   [0208E6C0] = the screen object
```

`0023BCC0` is itself `lea`-materialised, at `0023C537` inside `0023BD40`, and additionally has **three
`E8` call sites** (`002401FD`, `0024027D`, `00282186`) in two functions — `0023FBE0` and `00281ED0`.
**`00281ED0` is owned by UI and tagged `V112-UI-Menu-HUD`**, and its own caller `00280DE0` carries the
same ownership and `00280DE0` has **zero callers of its own** — the same `lea` mechanism, one level further up.

`0023BD40` (2,091 B) is the screen's proc, not a registrar. On construction it walks a descriptor table
and builds one child object per interactive row.

## 4. The row table — 24 records of 20 bytes at `00914710`

```
+0x00  dword  ordinal        0 .. 23, sequential, matches the array index
+0x04  dword  kind           2, 3 or 5 -> build a child; 0 -> build nothing
+0x08  dword  widget class   7,8,9,0A,0B,0C for the kind-0 rows; 0x0F for row 1; 0x10 for the rest
+0x0C  dword  text id A      0x050C .. 0x0539 in rows 4-23, 0x056E in row 1, 0 in the six
                             kind-0 rows   (UNRESOLVED - not read as text by this document)
+0x10  dword  text id B      0x0D07 .. 0x0D1B   (UNRESOLVED)
```

**Read as text 2026-09-18 (FABLE), through the string pool (bank = id ÷ 1000, position = id mod 1000; `0x05xx` is `menu_command.bin`, `0x0Dxx` is `help_menu.bin`).** The screen is the Graphics Settings screen. Text id A names the row and text id B is its help line: row 1 (class `0F`) has an empty A and the help *Set to the preset image quality* (the preset selector); rows 4..10 are *Display Adapter*, *Resolution*, *Screen Mode*, *Brightness*, *Vsync*, *Display Buffer*, *Frame Rate Limit*; rows 12..13 *Anisotropic Filtering* and a row whose A is empty and whose help is *Adjust water shader quality*; rows 15..16 *Shadows*, *Character Self-Shadowing*; rows 18..23 *Anti-Aliasing*, *Post-Process Anti-Aliasing*, *Ambient Occlusion*, *Depth of Field*, *Glare*, *Soft Particles*. The four ids after the table (`0x0D08`..`0x0D0A`, `0x0D42`) are the preset descriptions: *Use graphical presets designed to maximize performance*, *Use standard graphical presets*, *... maximize quality*, *Adjust graphics settings individually*. The six kind-0 rows (0, 2, 3, 11, 14, 17; classes `07`..`0C`) carry text id 0 in both columns, and the 27-entry command list the settings dispatcher's descriptor table holds for this screen (`01E0B670`, kind 0, entries of `{command, label id, help id}`) has exactly six label-less entries at the same positions, so the headings have no text anywhere: what they draw is the widget class alone.

The construction loop bound is `esi < 0x18` = **24**, and the table's own ordinals run `0 .. 0x17`.
**The bound and the content agree; neither was assumed from the other.**

```asm
0023BFC0  mov  edx, [r12]      ; r12 = 00914714 = record + 4, stride 0x14
0023BFC4  mov  ecx, edx
0023BFC6  sub  ecx, 2   ; je  -> kind 2
0023BFCB  sub  ecx, 1   ; je  -> kind 3
0023BFD4  cmp  ecx, 2   ; jne -> skip     ; falls through only for kind 5
0023BFE2  lea  rdx, [rip - 0x8f9]         ; = 0023B6F0   (kinds 2 and 5)
0023C0CD  lea  rdx, [rip - 0xda4]         ; = 0023B330   (kind 3)
0023BFFA  mov  ecx, 0x1d8                 ; every child is 0x1D8 = 472 bytes
0023BFFF  call 0x244f50
0023C03F  mov  [r14], r15                 ; r14 = screen + 0x4E0, stride 0x18
0023C042  mov  [r14 - 8], esi             ; the ordinal, 8 bytes earlier in the same record
```

**Kind counts, of 24:** kind 0 → 6 rows, kind 2 → 13, kind 3 → **1**, kind 5 → 4.
**Exactly one row in the screen uses `0023B330`.** It is row 7, and section 5 names it Brightness.

## 5. Every row, and the setting it edits

Two independent 23-entry jump tables were read — `0017DD5C` (change) and `0017E1AC` (read back) — and
the setting names come from the game's own `GameSetting.ini` key table at `01DFD050`.

| row | kind | proc | reads | setting | **`GameSetting.ini` key** | change id |
|---:|---:|---|---|---:|---|---|
| 0 | 0 | — | — | — | *no child built* | — |
| **1** | 2 | `0023B6F0` | `cfg+0x0C` | 3 | **Quality** | `0x11B` |
| 2 | 0 | — | `-1` | — | *no child built* | — |
| 3 | 0 | — | `-1` | — | *no child built* | — |
| 4 | 5 | `0023B6F0` | `001DDAB0()+0x48` | 19–21 (26) | *display object: adapter index* → **`DeviceID` `LUIDLow` `LUIDHigh`** (§11) | `0x10A` |
| 5 | 5 | `0023B6F0` | `001DD050(001DDAB0())` | 11 or 1 | *display object: size index* → **`WindowSize`** or **`Resolution`** (§11) | special |
| 6 | 5 | `0023B6F0` | `cfg+0x08` | 2 | **ScreenMode** | *cycles 0 to 1 to 2; committed only after a confirm dialog* (§11) |
| **7** | **3** | **`0023B330`** | `cfg+0x10` | 4 | **Brightness** | `0x110` |
| 8 | 2 | `0023B6F0` | `cfg+0x14` | 5 | **VSync** | `0x111` |
| 9 | 2 | `0023B6F0` | `cfg+0x44` | 17 | **BackBufferCount** | `0x11C` |
| 10 | 5 | `0023B6F0` | `cfg+0x48` | 18 | **FrameLimit** | `0x11D` |
| 11 | 0 | — | `-1` | — | *no child built* | — |
| 12 | 2 | `0023B6F0` | `cfg+0x18` | 6 | **Anisotropic** | `0x112` |
| 13 | 2 | `0023B6F0` | `cfg+0x40` | 16 | **WaterQuality** | `0x86` |
| 14 | 0 | — | `-1` | — | *no child built* | — |
| 15 | 2 | `0023B6F0` | `cfg+0x1C` | 7 | **Shadow** | `0x113` |
| 16 | 2 | `0023B6F0` | `cfg+0x3C` | 15 | **CharacterSelfShadow** | `0x114` |
| 17 | 0 | — | `-1` | — | *no child built* | — |
| 18 | 2 | `0023B6F0` | `cfg+0x20` | 8 | **MSAA** | `0x115` |
| 19 | 2 | `0023B6F0` | `cfg+0x24` | 9 | **PostAA** | `0x116` |
| 20 | 2 | `0023B6F0` | `cfg+0x28` | 10 | **HDAO** | `0x117` |
| 21 | 2 | `0023B6F0` | `cfg+0x30` | 12 | **DepthofField** | `0x118` |
| 22 | 2 | `0023B6F0` | `cfg+0x34` | 13 | **Glare** | `0x119` |
| 23 | 2 | `0023B6F0` | `cfg+0x38` | 14 | **SoftParticle** | `0xA6` |

`cfg` is the singleton at `01F82D20`; `setting[i]` is at `i * 4`, per
[the contract](../../19-Save-Load-Settings/Game-Settings-Config/CONTRACT-game-setting-config.md).

> ### The control that makes this table trustworthy
>
> **The set of rows that do nothing is `{2, 3, 11, 14, 17}` in both tables at once.** The descriptor
> table says so by carrying kind `0`; the two jump tables say so by pointing at their default arm.
> They were read by different means from different constructs. **They agree exactly.** Row 0 is absent
> from the jump tables only because the index is `row - 1`.
>
> A second, independent check: row 10 reads `cfg + 0x48` = `setting[18]`, and `0017D8F0` — read in a
> different block, for a different reason — returns `cfg->setting[18]` and is named `GetFrameLimit`.

**16 distinct settings are reachable from this screen.** The other 15 are not: `Language`
(locale-derived), `Resolution`, `WindowSize`, `DeviceID`, `LUIDLow`, `LUIDHigh`, `CameraRevise`,
`MouseSensityX`, `MouseSensityY`, `DecideButton`, `Monitor`, `WindowPosX`, `WindowPosY`, `LastX`,
`LastY`. **Whatever edits those is not this screen** — mouse sensitivity and the confirm button in
particular are player-facing and must be edited somewhere. **Open question `DI-1`.** *Answered 2026-09-14 (FABLE) in §11.*

> **Corrected 2026-09-14 (FABLE): the count is 22, not 16.** Rows 4 and 5 were read above as an audio
> object. `001DDAB0` returns the **display object** at `[01F82D18]`, and those two rows edit six more of
> the "unreachable" settings through it: row 4 commits `DeviceID`, `LUIDLow` and `LUIDHigh` (and can
> rewrite `Monitor`), and row 5 commits `WindowSize` or `Resolution`. §11 has the bodies. The settings
> this screen does not reach are nine: `Language`, `CameraRevise`, `MouseSensityX`, `MouseSensityY`,
> `DecideButton`, `WindowPosX`, `WindowPosY`, `LastX` and `LastY`.

## 6. What a left/right press runs — and this is the answer to `AX-6a`

```asm
; 0023B330, message 10 - the Brightness row
0023B399  cmp   [rsi + 0x1d0], 0          ; the row's "disabled" flag
0023B3A0  jne   default
0023B3A6  movzx eax, word [02F9736C]      ; input word
0023B3AD  test  al, al
0023B3AF  jns   0x23b3b9                  ; bit 7 clear?
0023B3B1  mov   r8d, 1                    ;   bit 7 set   -> direction 1
0023B3B9  test  al, 0x20
0023B3BB  je    default                   ;   neither bit -> nothing happened
0023B3C1  xor   r8d, r8d                  ;   bit 5 set   -> direction 0
0023B3C4  mov   edx, [rsi + 0xc4]         ; the row's current value
0023B3CA  mov   ecx, [rsi + 0xc0]         ; the row ordinal
0023B3D0  call  0x17db90
0023B3D5  mov   [rsi + 0xc4], eax         ; store what the change returned
```

`0023B6F0` does the same with **one difference that matters**: it reads the input word at
**`02F9736A`**, two bytes earlier. Both then test bit 7 and bit 5 of the low byte. `02F97360` is
already recorded in this database as an input snapshot; **which of `+0x0A` and `+0x0C` is "held" and
which is "newly pressed" is UNRESOLVED — open question `DI-2`.**

> **`DI-2` answered 2026-09-14 (FABLE): neither is "held".** `02F9736A` is **newly pressed** and `02F9736C` is
> **pressed with auto-repeat**; held is `02F97368`.
>
> **The snapshot copies the input channel's history.** `InputGameplay_RebuildFrameSnapshotFromChannelHistory`
> (`002498B0`) zeroes `02F97360`–`02F9739B`, then for each of the two channels (a 0x14-byte record) ORs eight
> history mask fields over the lookback frames (`00249940`–`002499AC`). The field-to-slot mapping, for
> channel 0:
>
> | snapshot | ← history frame field (accessor) | contents |
> |---|---|---|
> | `02F97368` | `+0x04` (`GetHistoryMaskOffset04`) | held |
> | **`02F9736A`** | **`+0x0C`** (`…Offset0C`) | **`cur & (cur ^ prev)`: newly pressed** |
> | **`02F9736C`** | **`+0x08`** (`…Offset08`) | **the repeat filter's "fires this frame" word** |
> | `02F9736E` | `+0x10` (`…Offset10`) | `prev & (cur ^ prev)`: released |
>
> - **The contents come from the builders.** `InputControl_ConvertButtonMaskToTransitions` (`0035FAC0`) stores
>   held at frame `+0x04`, `(prev ^ cur) & cur` at `+0x0C` and `(prev ^ cur) & prev` at `+0x10`
>   (`0035FB92`–`0035FBB4`), then calls `0035FBD0`. That writes `+0x08` with a bit set on the press and again
>   each time the per-button countdown expires while held (initial delay: channel byte `+4`; repeat delay:
>   `+5`) — `AP-8` on [the input stack](../../15-Input/Input-Stack/input-stack-device-channel-and-bindings.md).
> - **`02F9736A` is also consumed.** `InputGameplay_ArbitrateDigitalInputAndModalState` clears it after acting
>   on a press (`00253F70`, `00253FE9`, `002540C5`, …), which fits an edge word, not a level.
>
> **So the Brightness row (`0023B330`, `02F9736C`) keeps stepping while left or right is held, and every other
> row (`0023B6F0`, `02F9736A`) steps once per press.** That is the difference the question expected on a held
> stick, now read from the code. How it looks on screen was not observed.

```
0017DB90(row, currentValue, direction)
   23-entry jump table at 0017DD5C, index = row - 1, bound "> 0x16" -> default
   each live arm: r8d = a property id, then
0017DD2E   call 001CD040(manager, direction, propertyId)
0017DD39   call 0016D6A0()                 ; unread   <- corrected 2026-10-02, OPUS - 0016D6A0 is ret 0, the stub /OPT:ICF folded empty functions onto
0017DD40   return 0017E070(row)            ; read the value back out of the config
```

```
001CD040  test dl,dl / mov r9d,r8d / sete r8b / jmp 001D1660   ; 14 B, direction in both polarities
   001D1660   282-id dispatcher, 226 arms
      001D5120   graphics apply
         001DE4F0   GameSettingConfig_ApplyQualityPreset
```

> ### `AX-6a` is answered
>
> **The graphics-apply chain runs when the player pushes left or right on a Config-screen row.** It is
> not a startup callback, not a frame callback and not registered against a timer. `AX-6a` asked *when*
> it fires; the answer is *on player input, in one screen, and nowhere else in the image*.
>
> Every function on the chain has **exactly one caller** once EH-funclet sources are excluded, and the
> chain's two roots have **no callers at all** by any of the four instruments — they are the procs of
> two row objects in this screen.
>
> **The consequence is behavioural and checkable.** Construction copies preset **column 0** into all 31
> settings, while `Quality`'s own column-0 value is `1`. Nothing reconciles that at startup, because the
> only thing that could is behind a button press. **`AX-6` — "does anything apply a quality preset at
> startup" — is therefore answered NO.**

## 7. The message ids these two handlers implement

Both procs have the shape `proc(self, msg)` with `msg + 0x00` a small id and `msg + 0x08` a qword
parameter, which is the same 24-byte record shape as the draw-pass messages `3`, `4`, `5` recorded in
[the widget tree draw pass](../../99-Unresolved-Residual/the-widget-tree-draw-pass.md).

| id | `0023B330` | `0023B6F0` | what it does here |
|---:|---|---|---|
| 1 | yes | yes | early branch, not read |
| 4 | yes | yes | the draw-pass message already recorded; not re-derived here |
| **10** | yes | yes | **sample left/right and change the row's value** |
| **12** | yes | yes | `self->disabledFlag = (msg[+8] == 1)` — `+0x1D0` in `0023B330`, `+0x1CC` in `0023B6F0` |
| **13** | — | yes | notify, carrying a command id at `msg[+8]` |
| 14 | yes | — | tail-calls `002470D0` |

**Message 13 travels both ways.** The screen sends `{13, 0x2CA2}` / `{13, 0x2CA3}` (payloads at
`00914CB0` / `00914CC0`) down to a child; a child sends `{13, 0x2CA6, 5}` / `{13, 0x2CA7, 1}` (payloads
at `00914D50` / `00914D40`) back up, by loading `[0208E6C0]`, reading the screen's proc from its `+0x00`,
and calling it. **That is an independent confirmation that `+0x00` holds the proc** — a child recovers
its parent's entry point from that slot without any other help.

### 7.1 The screen proc `00280DE0` and the `00281ED0` state machine (SWE2-FRONTIER, switch-families package)

`00280DE0` (1566 B) is the screen's root procedure: `msg+0x00` ids `1`–`0x13` go through RVA
table `00281400` (site `00280E16`), with id `0x11F` peeled by an explicit `je` to `00281243`
and anything `> 0x11F` falling out at `002813ED`. **Nine** of the nineteen ids share the
`002813ED` tail — ids **3–9, 11 and 17** (cases `{2..8,10,16}`) — which restores `rbx` and
tail-jumps to `005C5230`; the distinct arms are:

| id | arm | what it does |
|---|---|---|
| 1 | `00280E45` | `msg+8 → self+0x278`, then `00281AE0` |
| 2 | `002811DC` | short arm — not read in detail |
| 10 | `00280FD4` | not read in detail |
| **12** | `00281015` | **row activation** — see below |
| 13 | `002811A5` | not read in detail |
| 14 | `00280EC3` | `[+0x280]` bit-1 test: set → `002D1AC0([+0x260], 0x8001)`, clear → `002C9EB0(0x8000)`; then `and [+0x280], ~2`, `002CFCF0`, and `[0209AC30]+0xF8` → `00246AD0` |
| 15 | `002811F0` | not read in detail |
| 16 | `00280E62` | a 12-call reset battery — `002CE980`, `00291D50`, `00295D10`, `00284E90`, `002CF8B0(0)`, `002CE7A0(0)`, `002CF710`, `002C1390`, `002C2F60`, `002C41F0`, `00567770`, then ~~`00246AD0(0209EA28-obj, self)`~~ `00246AD0(0208EA28-obj, self)` *(corrected 2026-10-02, OPUS: `00280DE0+0xBD` loads `[0208EA28]`; nothing references `0209EA28`)* and `002470D0(self)` — ends with its own `ret` |
| 18 | `00280E22` | `00281E00`, then clears `[0209AC30]+0xDF8` |
| 19 | `00280F2A` | not read in detail |
| `0x11F` | `00281243` | apply-to-all-rows — see below |

**Id 12 is "the highlighted row was activated."** `msg+0x10` selects the row —
`[msg+0x10]×0x20 + [self+0xD8]` — and `msg+8` is the command: `0x8002` arms state 5 and clears
`[+0x260]+0xE0` bit `0x200000` (`00281044`–`0028106D`); `0x8000` goes to `00281184`; `0x8001`
is the apply path — `002526F0(6, 4, 1)`, `002C9E60(row)`, a `002DD7E0(0)` compare
(`0028107C`–`002810A4`), then publishes the row into `+0x268`, its `[+0]` id into `+0x274`,
`+0x274`'s word into `+0x270` via `00282650`, and `[rsi]` into `[0209AC30]+0xDF8`
(`002810B8`–`002810FC`). Finally the row's `[+0]` — a request id in `0x4B3`–`0x53A` — is
dispatched through a second byte-mapped table (`00281111`–`00281125`, map `00281458`, RVA
table `0028144C`) that ends by writing `+0xC0 = 3` (`002CDE20`/`002CD8A0`/`002CE2F0` path,
`00281127`–`0028114B`) or `+0xC0 = 1` (`0028114D`).

**`+0xC0` is the state dword of `00281ED0`** (1697 B — all accesses are 32-bit: `mov eax,
dword[rcx+0xC0]` at `00281ED7`, `mov dword[…+0xC0], 3/1` on the arms), the machine `00280DE0` id-12 arms:
its outer RVA table `00282574` (site `00281F03`) has seven states on `[self+0xC0]`, and state
1 (`00281F0F`) re-reads `[[+0x268]]` and dispatches the same `0x4B3`–`0x53A` request band
through its own byte map `002825C0` / RVA table `00282590` — the row's request id chooses
which apply body runs per tick (`00281F3F` writes `+0x11C`/`+0x11E`/`+0x120` on the
`[0209AC30]+0xF8` object; `002820BC`/`002820D6`/`00282127`/`00282131`/`0028217D` and the
`0x503`–`0x505`, `0x53A` arms are not individually read). Id `0x11F` is the batch twin: on
`msg+8 == 0x8001` it loops `i < [self+0xD0]` calling `002C9F20(row_i)` over the `0x20`-stride
table at `+0xD8` (`00281280`–`002812A0`) — apply the same change to every row.

The row record at `[self+0xD8] + i×0x20` ~~uses the same `0x20` stride as §4's static~~ uses a `0x20` stride, not the `0x14` stride of §4's static *(corrected 2026-10-02, OPUS: `0023BD40+0x308` `add r12, 0x14` steps that table, whose first dwords read 0, 1, 2 at 20-byte spacing)*
`00914710` table (24 rows); whether `+0xD8` points at that table or a per-screen copy is not
established — `+0` is a `0x4B3`-band request id, the rest not yet field-mapped.

## 8. Two existing documents are corrected

### `0017E070` is not "16 settings in one pass"

[`CONTRACT-game-setting-config.md`](../../19-Save-Load-Settings/Game-Settings-Config/CONTRACT-game-setting-config.md)
section 6 says *"`0017E070` reads 16 settings in one pass"*. **The count 16 is right; the mechanism is
not.** `0017E070(row)` is a 23-arm jump table that returns **one** value — the value for that row — and
returns `-1` for the five dead rows. The 16 is the number of *distinct settings across all arms*, not a
pass.

### `001D1660` is not developer-only

[`the-282-command-parameter-console.md`](../../00-Engine-Core-Runtime/Developer-Tuning-Console/the-282-command-parameter-console.md)
names `001D1660` `DevConsole_DispatchCommand` and says the console *"has exactly one entry point"*.
**Its facts stand and its entry point is now named: the retail Config screen.** 16 of its 282 ids
(`0x86`, `0xA6`, `0x110`–`0x119`, `0x11B`–`0x11D`) are driven by shipped menu rows a player can reach.
Whatever else lives in the other 266 ~~arms~~ ids *(corrected 2026-10-02, OPUS: the 282-entry table holds 226 distinct arms and a default, `001D1660+0x359A`, that 56 ids share)*, **the dispatcher itself is live retail code, and calling the
whole of it a developer console overstates what was shown.**

## 9. What this document does not claim

- **What the two text-id columns resolve to.** `0x050C`–`0x0539` and `0x0D07`–`0x0D1B` are treated as
  opaque ids. The row names in section 5 come from the `GameSetting.ini` key each row reads, **not** from
  the label the player sees, and the two could in principle differ.
- ~~**Which input word means what.** Section 6, `DI-2`.~~ *Answered 2026-09-14 (FABLE) in section 6.*
- ~~**What rows 4 and 5 are.** They read an audio object (`001DDAB0`), not the config.~~ *Corrected
  2026-09-14 (FABLE):* they are the display adapter and the screen size rows (§11).
- **Where `ScreenMode` is written.** Row 6 cycles a value `0 → 1 → 2` and returns it to the row object
  **without calling `001CD040` and without writing the config**. Something else must commit it.
  **Open question `DI-3`.** *Answered 2026-09-14 (FABLE): a confirm dialog commits it (§11).*
- ~~**That the six kind-0 rows are headings.** They build no child and no jump-table arm answers for them;
  what they draw is not established.~~ *Answered 2026-09-18 (FABLE) in section 4: they carry no text in the row table nor in the command list, so what they draw is the widget class (`07`..`0C`) and nothing else; the eighteen rows' labels and help lines are read there too.*
- **Anything observed in a live process.** Every statement here is static. The screen has never been
  opened under a probe.

## 10. Falsification pass 1 — 2026-09-13 (OPUS)

*(Static only. The four instruments and the row table were re-run from the shipped image. Nothing
executed.)*

### ✔ All four instruments reproduce, controls included

| | page | measured |
|---|---|---|
| `E8` control `001DE4F0` | 1 site | **1** |
| `E9` control `001D1660` | 1 site | **1** |
| `E8` / `E9` against the three functions | 0 / 0 | **0 / 0, all three** |
| code memory operand | 1 ref each, at `0023C0CD` / `0023BFE2` / `0023BCF8` | **1 each, at exactly those three addresses** |
| raw qword control `005C5230` | **2,527** occurrences | **2,527** |
| raw qword against the three | 0 | **0, all three** |

**The 2,527 is the one worth calling out**: a five-significant-figure count over every section's raw
bytes, reproduced exactly by an independent implementation. That is what a control is for.

### ✔ The row table reproduces, and it yields three numbers the page does not give

24 records of 20 bytes at `00914710`: **ordinals sequential `0`–`23`**, and the widget classes exactly
as published — `07`, `08`, `09`, `0A`, `0B`, `0C` on the six kind-0 rows, `0F` on row 1, and `0x10`
on the other **seventeen**.

* **Kind distribution: 0 ×6, 2 ×13, 3 ×1, 5 ×4.** So **18 of the 24 rows build a child** and six are
  the headings the player cannot land on — which is the count §1 describes in words.
* The record after the table is `00000D08 00000D09 00000D0A 00000D42 00000000` — **text ids, not a
  25th row**, which is what a `0x18` bound is protecting against.

### ✖ Corrected: row 1's text id is outside the published range

`+0x0C` is given as `0x050C .. 0x0539`. Seventeen rows fall in it; **row 1 holds `0x056E`**, above the
stated maximum, and the six kind-0 rows hold `0`. Row 1 is also the one row with widget class `0F`, so
it is the odd row on two counts and the range hides one of them. `+0x10`'s `0x0D07 .. 0x0D1B` is
right — row 1 is its **low** end.

### ✖ Corrected: the denominator

*"34,270 function bodies scanned"* — `functions.tsv` holds **38,161**. 34,270 is `progress.py`'s
`engine_explained` denominator, not a body count. **The instrument's result is unaffected**: scanning
the larger set found the same one reference each, so the finding is robust to the denominator and only
the stated denominator was wrong.

**Not claimed.** What the text ids resolve to — **not read as text here either**. Anything about the
proc bodies `0023B330` / `0023B6F0` beyond their reference counts. `AR-4` and the `lea`-materialisation
mechanism are cited, not re-derived. Nothing was executed.

## 11. Rows 4, 5 and 6: the display object and the confirm dialog — 2026-09-14 (FABLE)

*(Static reading of the shipped image. Nothing executed. Answers `DI-3`, `AX-3`; corrects the row
table's rows 4 and 5 and §5's count.)*

### Kind-5 rows change a pending value; a dialog commits it

A row child keeps two values: **`+0xC4`, the value shown**, and **`+0xC8`, the value last committed**.
A left/right press only changes `+0xC4` (§6). A kind-5 row (rows 4, 5, 6 and 10) commits through a
second path that the other rows also have, driven by message 13 in `0023B6F0`:

| `msg+8` | effect in `0023B6F0` |
|---|---|
| `0x2CA2` / `0x2CA3` | set / clear the row's lock `+0x1CC` (`0023B74A`, `0023B75D`) |
| `0x2CA4` **revert** | `+0xC4 = +0xC8`, then `0017E540(row, +0xC8)` (`0023B771`–`0023B783`) |
| `0x2CA5` **accept** | `+0xC8 = +0xC4`, then `0017E540(row, +0xC4)`; for row 5 also `0017DB40` (`0023B792`–`0023B7B2`) |
| `0x2CA6` / `0x2CA7` | re-read both values from `0017E070(row)` (`0023B7C5`–`0023B7E1`) |

**`0017E540(row, value)` is the row-indexed setter**, a 23-entry jump table at `0017E684`. For most rows it
stores `cfg->setting[k]` through `001DF340` (`mov [rcx+rdx*4], r8d`). Rows 4, 5 and 6 go to the display
object instead (below).

**Who sends accept or revert.** In the screen proc `0023BD40`, message 12 with command `0x8002` checks the
highlighted row (`[screen+0x718]`). If that row is kind 5 and its `+0xC8 != +0xC4`, the proc posts
`0x8003` to itself (`0023C344`–`0023C39B`); otherwise it plays sound 3 and closes the screen
(`0023C3A2`–`0023C3B8`). On `0x8003` it opens a dialog, `0023DFC0` with proc `0023E020`, parented to that
row child. The dialog kind comes from the row ordinal (`0023C3E5`–`0023C414`):

| row | dialog kind | text id (group `0x4BE`) |
|---:|---|---|
| 4 | `0x27` | `0x896` |
| 5 | `0x2B` | `0x89A` |
| **6** | **`0x2C`** | **`0x89B`** |
| 10 | `0x28` | `0x897` |

The dialog answers on message 12 (`0023E0AF`):
- **Command `0x8101`** on kinds `0x27`, `0x28`, `0x2B` and `0x2C` posts **`0x2CA4` (revert)** to the row
  (`0023E0C5`–`0023E127`).
- **Command `0x8100`** on kind `0x2B` posts **`0x2CA5` (accept)**. On kind `0x2C` it posts `0x2CA5`, then
  posts `{0x2CA6, 5}` to the screen (`0023E1F4`–`0023E24E`). The screen forwards that to child 5, so the
  size row re-reads its value (`0023C4A2`–`0023C4C7`).
- Kinds `0x27` and `0x28` on `0x8100` write the settings file (`0017E530`) and call `0017E050`; they post
  nothing to the row.

While a kind-5 row has a pending change, message 10 also passes a pending flag of 1 to the cursor routine
`00240DE0` (`0023C243`–`0023C27F`). What that flag does to cursor movement is not read here.

### `DI-3`: where `ScreenMode` is committed

**Row 6 is committed by the accept of dialog `0x2C`.** `0017E540(6, v)` takes arm `0017E5D4`. That arm
logs `"Change Screen Mode By Config Menu!!!!\n"` (`008C5A70`) and tail-jumps to **`001DC830(display, v)`**,
which:
1. returns if `v` equals `display+0x18`, the live screen mode (`001DC83F`);
2. stores `display+0x18 = v` and logs it (`001DC848`–`001DC85A`);
3. **stores `cfg->setting[2] = v` through `001DF340(cfg, 2, v)`** (`001DC85F`–`001DC86E`);
4. when `v == 1`, picks the display-mode index `+0x24` whose `width × height` is closest to the area of the
   `Resolution` pair (`001DC873`–`001DC909`, the mode-picker [the settings page](../../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md) describes).

`display+0x18` is the same field the display object's constructor `001DC5C0` copies from `cfg+0x08`. The
same `001DC830` is reached from the developer console's arm (`001D45E9`, logging `"Screen Mode Change by
Debug Menu !!!"`) through `00182DE0`, and from `0079C140` through `00182DE0`.

- **Not written to disk at commit.** `001DC830` writes memory only. The file is written when the screen is
  destroyed: message 18 of `0023BD40` calls `0017E530` → `GameSettingConfig_WriteFile` (`0023C501`).
- **A revert commits the old value**, and step 1 turns that into a no-op.
- **Resync.** On message 4, row 6 re-reads the config. If the value differs from `+0xC8`, both values are
  overwritten (`0023B8EA`–`0023B910`), so a mode change made elsewhere shows up on the row.
- **Not established:** what the window side does with the new `+0x18` / `setting[2]` after the commit.
  The readers `007980A0`, `00798FF0`, `0079C140` and others compare `cfg+0x08` against 0, 1 and 2, but
  they were not traced from this commit.

### Rows 4 and 5 edit six "unreachable" settings

`001DDAB0` returns `[01F82D18]`, the **display object** (0x180 bytes, built by `001DDA70`, constructed by
`001DC5C0`). **Its adapter list is built by `001DD170`:**
- `00623C10` fills the adapter count `+0x50`, the current adapter `+0x4C` (copied to `+0x48`) and a
  usable-adapter mask `+0x58`.
- For each adapter it copies a **0x130-byte description** from `00623CB0` into a 0x140-stride table
  `+0x78`, with the output count at `+0x130` and an output array (0x60 per output) at `+0x138`.
- The description's size and the offsets read below (`+0x104`, `+0x128`, `+0x12C`) are exactly
  `DXGI_ADAPTER_DESC`'s size and its `DeviceId` / `AdapterLuid` offsets. That is a layout match, not an
  import-confirmed type.

**Row 4 is the adapter.** It reads `display+0x48`.
- **Change.** `0017DB90` arm `0017DBF0` sends property id `0x10A` through `001CD040`.
- **Commit.** `0017E540` arm `0017E573` calls `001DC650(display, v, 1)`. That moves `v` (mod the count) to an
  adapter whose bit is set in `+0x58`, stores `+0x48`, and writes **`setting[19]` (`DeviceID`) = desc `+0x104`**,
  **`setting[20]` (`LUIDLow`) = `+0x128`** and **`setting[21]` (`LUIDHigh`) = `+0x12C`**
  (`001DC69F`–`001DC714`).
- **Monitor.** It then calls `001DC7A0(display, [display+0x64], 1)`. That stores the monitor `+0x60`,
  replacing an index above the adapter's output count with 1. **Only when the selected adapter is the current one** (`+0x48 ==
  +0x4C`) and the monitor changed does it write **`setting[26]` (`Monitor`)** and the settings file
  (`001DC7E6`–`001DC81E`).

**Row 5 is the screen size.** It reads `001DD050(display)`: `+0x38` when the live mode `+0x18` is 0,
otherwise `+0x24`.
- **Change.** `0017DC00` cycles the index through `001DC940`: the window-size list `+0x40` in mode 0,
  otherwise the display-mode list `+0x28`. Only in mode 0 does it apply at once through `001DC730`.
- **Commit.** `0017E540` arm `0017E5B2` stores the index (`001DC920`), and accept adds `0017DB40` →
  `001DC730`. That takes the chosen 0x1C-stride entry's `+0x00`/`+0x04` into `001DDBA0`, which writes
  **`setting[11]` (`WindowSize`)** when `cfg+0x08 == 0` and **`setting[1]` (`Resolution`)** otherwise,
  as `+0x00 << 16 | +0x04`, and then **writes the settings file** (`001DDBC8`–`001DDBF8`).

**So of the 15 settings §5 called unreachable, six are reached here:** `DeviceID`, `LUIDLow`, `LUIDHigh`,
`Monitor` (conditionally), `WindowSize` and `Resolution`. **Nine remain:** `Language`, `CameraRevise`,
`MouseSensityX`, `MouseSensityY`, `DecideButton`, `WindowPosX`, `WindowPosY`, `LastX` and `LastY`.

### `DI-1`: what writes the nine — 2026-09-14 (FABLE)

**Every runtime write of a setting goes through the generic setter `001DF340`.** Its 38 direct call sites
(`tools/rawcalls.json`) were read for the index in `edx`, and they split the nine this way:

| setting | writer | how |
|---|---|---|
| `CameraRevise` (22) | settings command **`0x1C`** | `002407F0` arm `00240924` → `0017E740` (`setting[0x16]`). `00240750` first transforms the value (arm `00240776`: `v = (v == 0)`). |
| `DecideButton` (25) | settings command **`0x26`** | `002407F0` arm `00240957` → `0017E6E0`, already on [the settings page](../../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md) §4; `00240750` arm `00240799` sets `v = (v != 1)` |
| `MouseSensityY` (24), `MouseSensityX` (23) | **no reachable writer** | setters `0017E760` (`edx = 0x18`) and `0017E780` (`0x17`) exist, but nothing references them (below) |
| `WindowPosX` (27), `WindowPosY` (28), `LastX` (29), `LastY` (30) | the window layer, not a menu | `0079EBA0` calls `GetWindowRect` on the game window (`0079EBBF`). When flag `02EA5247` is set it stores the rectangle's left/top as 27/28; it always stores the centre as 29/30; then it writes the settings file (`0079EC5E`). It runs from `0079C140` when that object's `+0x24` flag is set (`0079C2FE`–`0079C309`). `0079B300` resets 27/28 to 0 when the saved position lies outside the virtual screen (`GetSystemMetrics` 0x4C–0x4F, `0079B594`–`0079B645`). |
| `Language` (0) | the platform layer, not a menu row | besides the OS LANGID default (settings page §9), `007A0C60` (called from `007980A0`) gets a name from the Steam context (`SteamInternal_ContextInit`, interface `+0x30`, vtable slot 4 — the `ISteamApps::GetCurrentGameLanguage` slot). It matches the name against `japanese` … `schinese` (`01CB3510`–`01CB3560`) and stores `setting[0]` (`007A0F17`). It runs after the defaults, the OS query and the ini load, so Steam's language wins (`AV-3` on [the language page](../../19-Save-Load-Settings/Language-And-Locale/language-selection-and-locale-ids.md)). |

- **The settings commands come from a sibling screen's rows.** `00240750(id, &v)` has four callers, the row
  procs `0023D6B0`, `0023DB40`, `0023E770` and `0023EBE0`. `0023D6B0` passes its row byte `+0xC0` as the
  command id (`0023D77E`–`0023D78A`) after stepping `v` on the same input words as §6. `0023CE10` installs
  `0023DB40` (`0023D04C`). So `CameraRevise` and `DecideButton` are player-editable, from a screen other
  than this one.
- **Why the mouse sensitivities have no writer.** `0017E760` and `0017E780` are 20-byte bodies after
  `0017E740`, listed as unlisted code (`99-Unresolved-Residual/Unlisted-Code`). A full-`.text` search found
  no `E8`/`E9`/`EB` branch to either, no rip-relative operand into them (`tools/ripscan.py`), and no
  absolute or image-relative pointer to them anywhere in the file. The settings are only read, through the
  getters `0017E430` (`+0x5C`) and `0017E420` (`+0x60`). **In the shipped image a player can change mouse
  sensitivity only by editing `GameSetting.ini`.** A computed or data-driven call that none of these
  searches sees is not excluded.

## Residual placements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)

| function | size | role (call-signature read) |
|---|---:|---|
| `0023EFC0` | 449 | config-screen widget body (caller `0023FBE0`): `[rcx+0x60]`/`+0xC2`, `[rbx+0xE0..0x120]` fields; `002D48C0`, `002D45C0`, `002445C0`, inventory `002526F0`, `002D46F0` |

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — CLIENT and SERVICE.** Cited functions are called by `MainLoop_UpdateAndRenderFrame`, the 146-byte core start-up helper and two core frame bodies (463 and 2,001 bytes). They call a 40-byte core helper (2) and a 27-byte one.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**ActorEntity — SERVICE.** `00506700` on this page calls `ActorHandle_EncodeRegistryEntry`, owned by that layer. What it reaches is the 38-byte packer for an actor handle, and it states the layout: `word[+0]` occupies the low 16 bits, `byte[+0x15] & 0xF` bits 16-19, and `word[+0x16] & 0x7FF` bits 20-30; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Application — CLIENT.** `FUN_0017d6b0`, owned by that layer, calls `001DDA70` on this page. That caller is a 45-byte startup sequencer: six calls in fixed order and a tail-jump into a final one, with no work of its own; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Presentation — CLIENT and SERVICE (SWE2-CONTRACT 2026-09-15, 29 edges).** The config screen is
drawn by the render layer's widget machinery: `00579420`
(`Presentation.UI.Quest.ListScreenSelectionStateMachine`, 5 edges) and `002BAF80`
(`Presentation.UI.InputConsumerStateMachine`) drive `002470D0`/`002526F0`/`002D45C0`/`002D46F0`/
`002D48C0`; `002DD7E0` is reached by the nine-patch backgrounds `002455A0`/`00245170`, icon draws
`002BCB00`/`002B8EE0`, post-process binding `0029A930`, ScreenCapture `002D0650` and
`00506700`/`003FB3E0`/`003FBA80`/`004048E0`. `001D1660` both calls and is called by the
`Presentation.Rendering.NativeSupport` family (`001C7520`/`001C7360`/`001CD040`/`001DC650`/
`001DC7A0`/`001DDAB0`, 7 edges) — the settings-change path runs through native-support helpers the
render layer owns. The crossing is the screen's place inside the draw pass.

**Resource — MECHANICAL (SWE2-CONTRACT 2026-09-15, 8 edges).** `0024A5A0` (5 edges, via `00280DE0`/`00281AE0`/
`00281E00`/`002CE980`/`00506700`), `00249580` (2, via `00281AE0`/`002BAF80`) and `002EEEE0` (via
`001D1660`) — the Resource-owned generic helpers the config screen's bodies call. Same
helper-sharing shape as the other screen rows; no resource-semantics crossing.

**Rewards_Progression_Economy — CLIENT.** `002CE7A0`, named in the `00280DE0` id-16 arm's reset
battery, is 59 bytes that call `00253690`, owned by that layer, take ~~`[[0209EC30]+0x30]`~~ `[[0209AC30]+0x30]` *(corrected 2026-10-02, OPUS: `002CE7A0+0xD` loads `[0209AC30]`; nothing references `0209EC30`)*, and post
the result through `002A1F20` with event kind `9` — the progression/economy read the reset performs,
not a shared responsibility. Read from the shipping bytes 2026-09-15 (SWE2-FRONTIER).

**CombatAction / CombatFormula / Items_Equipment_Shops_License — MECHANICAL (SWE2-EC7 batch 27, 9
edges).** `00253690`, the resolved-object getter this page's `002CE7A0` consumes, is also called by
four CombatAction bodies (`00300280`, `00303BD0`, `00305640`, `0030EF20`), one CombatFormula body
(`003112F0`) and four Items/Equipment/Shops/License bodies (`002FD530`, `002FD880`, `002FEEB0`,
`00310870`) — shared-callee fan-in, not a relationship this page owns in those layers.

## The `0023BD40` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`0023BD40` ~~(~350 B)~~ (2,091 B *(corrected 2026-10-02, OPUS: its last instruction is `0023BD40+0x82A` `ret`)*) — a config-screen row handler under a stack cookie.

| member | role | interior |
| --- | --- | --- |
| `0023D610` | row setter + dispatch — `byte[+0xC2] = r8b`, `byte[+0xC0] = dl`, then a `00120000`-based jump-table dispatch (`0023D61A`/`0023D62E`) | [`0023D61A`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: the jump-table targets.

## SWE2-EC7-19 update (2026-05-15) — `0023D4F0` config-path shared tail

`0023D4F0` (275 B) is the row-commit the eight `0023xxxx` config-screen callers (`0023D6B0`, `0023DB40`, `0023E020`, `0023E400`, `0023E560`, `0023E770`, `0023EBE0`, `0023FBE0`) funnel through — the largest shared-callee cluster this batch: `[rcx+0xC0]=dl` and `[rcx+0xC2]=r8b` store the (kind, param) pair (`0023D504`/`0023D4FD`); `dl < 0x2D` resolves through the `01CEBF60` descriptor table — its entry's lead byte lands at `+0xC1` (default `0xFF` when out of range or null) and the entry itself at `+0xC8` (`0023D519`..`0023D549`). The `01CEB638` byte-table row for `dl` then drives the geometry half: a non-`0xFF` first byte calls `002432B0([0209AC30]+0x60, &rcx+0x50, kind, rcx)` (`0023D571`..`0023D57D`) and publishes the result's `word[+4]`/`+6`/`+8`/`+0xA` to `+0x98`..`+0x9E`, while `0xFF` writes the `01E0C1D8`/`01E0C1DC` defaults (`0023D5B2`..`0023D5CC`). A non-`0xFF` second row byte runs `00394700(rcx, dl)` (`0023D5E1`); `+0x40` bit-7 clears (`0023D5E6`), and the body tails `00247930` with `edx = movsx word[rdi+2]` (`0023D5F0`..`0023D5FE`) — the per-setting apply the config rows share.

## SWE2-EC7-23 update (2026-09-18) — `003C21C0`/`003BE2D0` slot matchers + `003BF6C0` record builder

`003C21C0` (58 B) is the two-slot matcher over `[02B457E0]+0x120`: two
`0xA8`-stride slots scanned for `byte[+0x10] == ecx` -> `jmp 003C22B0` hit arm
— the bounded lookup the `002Bxxxx` config/UI callers run. Interior anchor
`003C21D9` (the kind-byte load).

`003BE2D0` (202 B) is the companion arm: `003C0380` kind fetch into `r14d`,
the same `+0x120`/`0xA8` two-slot walk matching `byte[+0x10] == r14d`, then
`word[rdx+8]` accumulate — the kind-keyed slot find with the word-field read.
Interior anchor `003BE30E`.

`003BF6C0` (255 B) is the record builder the same caller cluster drives:
`cx >= 0x3B` reject, `[rdx] = cl` byte write, `00254380` resolve ->
`[rsi+1] = al`, then a `[02B457E0]`-banked `0xFF`-sentinel loop building the
out-record — the table-driven writer the config arms call. Interior anchor
`003BF6DC` (the first byte store).

## SWE2-EC7-24 update (2026-09-18) — `003948B0` + `00392FC0` settings-record arms

`003948B0` (255 B) is the `003949B0` record builder's flag-extended sibling — same
`[0208EA28]` capture, same `movups` block pair, but `r10d &= 0xFF0` and a five-bit
flag ladder off `[r9+0x48]`: `&1 -> ecx|8`, `&2 -> bts 9` plus `byte[r9+0x44]`,
`&4 -> ecx|0x10`, `&8 -> bts 0xB`, `&0x10 -> bts 0xA`, with `r8d` bit `0xC`
vetoing the `+0x18` dword. The config-screen `0023xxxx` cluster reaches it
through `0023E020`/`0023E560`. Interior anchor `00394907` (the `test r9` gate).

`00392FC0` (360 B) walks the `[rcx+0x10]` pointer bank while `[rcx] & 0x3FFFC`
holds: per entry `([rbx+8] >> 2) & 0xF` selects a kind — kind 2 runs a four-slot
write loop over `rbx+0x28..0x37` dispatched by an `esi`-indexed jump table at
`0x273148` (one arm calls `002DD7E0` with `ecx=2`), kind 5 calls `00392F30` and
stores at `rbx+0x24`. The settings-command callers (`0023D6B0`, `0023DB40`,
`0023DD10`...) share it. Interior anchor `00393000` (the bank fetch).

## SWE2-EC7-27 update (2026-09-18) — `002CE7A0` resolved-object dispatch

`002CE7A0` (59 B) calls `00253690()`, loads `[0209AC30] + 0x30`, and
dispatches `002A1F20(obj, 9, eax, 1, {ebx, 0})` — the resolved-object
call the setting-change paths run. Interior anchor `002CE7D0` (the
`002A1F20` call).

## SWE2-EC7-28 update (2026-09-18) — `002C9F20`/`002C9E60` the `+0xE4` field pair

`002C9F20` (16 B) null-guards `[rcx+8]` and stores `edx` at `+0xE4`;
`002C9E60` (22 B) is its getter — `0x80808080` when the object is
absent, else `dword[+0xE4]`. The queued-record field the config rows
write and read back. Interior anchors `002C9F29` (the store) /
`002C9E69` (the sentinel).

## SWE2-EC7-29 update (2026-09-18) — `00394700` kind<4 table forward

`00394700` (28 B) is the `edx < 4` table forward `0023D4F0` runs for a
non-`0xFF` second `01CEB638` row byte: `rdx = edx*40`
(`lea rdx,[rax+rax*4]` then `[00D112E0 + rdx*8]` — 0x28-byte descriptor
records) and tail-jumps `00247570(record)`; `edx >= 4` returns without
dispatch. Interior anchor `00394712` (the scaled `lea` add). The
`00394720`/`00394790` siblings repeat the same table lookup and add the
`+0x7C` bit-pack write (`(v&0x3FF) | (v<<0x16) | (v<<0xC&0x3FF000) |
0xC00` merged over the record's low 10 bits).

## SWE2-EC7-30 update (2026-09-18) — `00282650` `+0xAC8` slot repair

`00282650` (160 B) is the copy `+0x274`'s word into `+0x270` rides
on: `*rcx` indexes the `0209AC30` bank's nine-entry `+0xAC8` pointer
table. For opcodes `0x4B5`/`0x4B6` (`edx - 0x4B5 <= 1`, else return)
it keeps the indexed record when that record is live and kind > 5;
otherwise it scans all nine slots for the first `word[+0x60] >= 0`,
`byte[+0] & 2` clear, kind <= 5 entry — writes that index (or 0
when none qualifies, or when `*rcx` was negative) back to `*rcx`,
and tails `002527B0(6, 4)`. Interior anchor `002826E0` (the match
arm's `002527B0` tail).
## SWE2-EC7-31 update (2026-09-18) — `00241C90` `0x3D0` record ensure (via `003948B0`/`003949B0`)

`00241C90` (101 B) — reached through `003948B0`, `003949B0`,
`00394A90`, `003CA310`, `00228C70` and `002A1FB0` — is the shared
0x3D0-byte record ensure the settings/dialog builders call: a null
`rcx` allocates one through `002497B0(0x3D0)` (the `rsp+0x20` flag
records borrowed-vs-owned), then `002465F0(rec, 0x3D0, 00241D40,
&out)` ~~runs the table-driven init with the `00241D40` descriptor~~ constructs a `0x3D0`-byte widget whose handler is `00241D40` *(corrected 2026-10-02, OPUS: `002465F0` takes the handler in `r8` — `00241BF0+0x7C` `lea r8, [00241D40]`)*
and returns the record. Interior anchor `00241CE7` (the `call
002465F0` init).

## SWE2-EC7-33 update (2026-09-19) - `002A1FB0`

`002A1FB0` (**1,640 B** — *corrected 2026-09-19 (SWE2-EC7); this line printed 1,810 B, a wrong literal in the batch-33 append — the body is 1,640 B per the function list*) is a config-screen driver - `002F9860`/`0039C480`/`002C9430`/`002A3730`/`0029F6E0`/`0024ABC0` plus a `00861EC0` libfn call. Interior anchor `002A216E` (a `002F9860` call).

## SWE2-EC7-33 update (2026-09-19) - `00240DE0`

`00240DE0` (**1,520 B** — *corrected 2026-09-19 (SWE2-EC7); this line printed 1,650 B, a wrong literal in the batch-33 append — the body is 1,520 B per the function list*) is a config-screen driver - `002D47C0`/`002413E0`/`002D3BA0`/`002F9860`/`002DC290`/`002D8BB0`/`002D4650`, reaching `001E0A10` at entry+0xA2. Interior anchor `0024106F` (a `002D47C0` call).

## SWE2-EC7-33 update (2026-09-19) - `0029A930`

`0029A930` (**1,304 B** — *corrected 2026-09-19 (SWE2-EC7); this line printed 1,325 B, a wrong literal in the batch-33 append — the body is 1,304 B per the function list*) is the gambit-adjacent screen driver - `0035BB60`/`002DD7E0`/`00247930`/`0035BB00`/`0029B790`/`002973E0` plus the `00861F0E` trig call. Interior anchor `0029AA96` (a `002DD7E0` call).

## SWE2-EC7-33 update (2026-09-19) - `003FB3E0`

`003FB3E0` (**1,292 B** — *corrected 2026-09-19 (SWE2-EC7); this line printed 1,134 B, a wrong literal in the batch-33 append — the body is 1,292 B per the function list*) is the screen's text-record builder - 9 `00202C90` calls plus `003F1290`/`003F1230`/`003F0040`/`002DD7E0`/`00202B10`. Interior anchor `003FB448` (a `00202C90` call).

## SWE2-EC7-33 update (2026-09-19) - `004048E0`

`004048E0` (**1,118 B** — *corrected 2026-09-19 (SWE2-EC7); this line printed 1,218 B, a wrong literal in the batch-33 append — the body is 1,118 B per the function list*) is a config-screen driver - `00394690`/`00244F00`/`004060B0`/`00405770`/`0031B690`/`002DD7E0`/`005C5230`. Interior anchor `00404BA6` (a `002DD7E0` call).

## SWE2-EC7-33 update (2026-09-19) - `003FBA80`

`003FBA80` (**1,031 B** — *corrected 2026-09-19 (SWE2-EC7); this line printed 995 B, a wrong literal in the batch-33 append — the body is 1,031 B per the function list*) is the screen's builder - `00202C90`/`00202B10`/`002DD7E0`/`002714A0`/`00271290`/`00271080`/`0020E600`. Interior anchor `003FBAFC` (a `00202C90` call).

## SWE2-EC7-38 update (2026-09-19) - `001C7360`

`001C7360` (446 B) is a `Presentation.Rendering.NativeSupport` sibling - `01F813C8`/`008FA338`/`008FA350`, `"TrackingMapScreenRateX"`, `001FF740` quadruple plus `00200BE0`/`001FEE10`/`001EDF00` pairs and `00202930`. Interior anchor `001C7394` (a `001FF740` call).

## SWE2-EC7-38 update (2026-09-19) - `001C7520`

`001C7520` (446 B) is the `TrackingMapScreenSuperWideMul` sibling - `01F813C8`/`008FA368`/`008FA388`, same `001FF740`/`00200BE0`/`001FEE10`/`001EDF00`/`00202930` shape. Interior anchor `001C7554` (a `001FF740` call).

## SWE2-EC7-39 update (2026-09-19) - `0023E560`

`0023E560` (425 B) is a config-screen body - `0208EA28`, `00247510`/`002F9860` pairs plus `002DDE60`/`001EDEC0`/`00244F00`/`0023D4F0`/`00244960`. Interior anchor `0023E5AD` (a `00247510` call).

## SWE2-EC7-41 update (2026-09-19) - `002CE980`

`002CE980` (339 B) is a config-screen body - `01E0C208`/`0209AC30`, `0024A5A0`/`00861EBA`/`00181580`/`003697F0`. Interior anchor `002CE9C9` (a `0024A5A0` call).

## SWE2-EC7-47 update (2026-09-19) - `00394A90`

`00394A90` (218 B) is a body - `00241C90` single call. Interior anchor `00394B5C` (the `00241C90` call).

## SWE2-EC7-49 update (2026-09-19) - `00281E00`

`00281E00` (196 B) is the setting-change runner - `0024A5A0`/`0024AB60`/`00292140`/`00295D80`/`002CEEF0`/`00326D60`. Interior anchor `00281E04` (a `0024A5A0` call).

## SWE2-EC7-54 update (2026-09-19) - `00405770`

`00405770` (354 B) is a config-screen driver body - `00225580`/`00394690`/`00404F50`/`004073B0`/`00407450`/`00407720` plus `00D12190` rdata. Interior anchor `004057BD` (a `00394690` call).


## SWE2-EC7-54 update (2026-09-19) - `004060B0`

`004060B0` (312 B) is a config-screen driver body - `00246AD0` single call plus `02B62D88`. Interior anchor `004060E5` (a `00246AD0` call).

## SWE2-EC7-55 update (2026-09-19) - `002973E0`

`002973E0` (247 B) is a config-screen body - `00271960`/`002726C0`/`00272730`/`002727C0`. Interior anchor `00297414` (a `00271960` call).

## SWE2-EC7-56 update (2026-09-19) - `002413E0`

`002413E0` (197 B) is a config-screen body - `002D3BA0`/`002D45C0` plus one vcall. Interior anchor `00241408` (a `002D45C0` call).

## SWE2-EC7-58 update (2026-09-19) - `00623CB0`

`00623CB0` (169 B) is an indirect-only vtable sequence - `call [rax+0x38]`/`call [rax+0x40]` walking the `[rsp+0x40]` interface (five vcall sites). Interior anchor `00623CDD` (the `call [rax+0x38]` vcall).

## SWE2-EC7-60 update (2026-09-19) - `00623C10`

`00623C10` (159 B) is an indirect-only adapter-count filler - `call [rax+0x38]`/`call [rax+0x10]` on the `[rcx+0x1878]` interface, `+0x18B0` copy (three vcall sites). Interior anchor `00623C56` (the `call [rax+0x38]` vcall).


## SWE2-EC7-60 update (2026-09-19) - `004073B0`

`004073B0` (155 B) is a config-screen driver body - `0029F4B0` single call. Interior anchor `004073E2` (a `0029F4B0` call).



## SWE2-EC7-64 update (2026-09-19) - `00272730`

`00272730` (142 B) is a config-screen body - `00271960` single call. Interior anchor `00272754` (a `00271960` call).



## SWE2-EC7-66 update (2026-09-19) - `002A1F20`

`002A1F20` (131 B) is the event-kind-9 progression body - `00244F50`/`00808C40` plus `01F44830`/`0209C4C8`. Interior anchor `002A1F8C` (a `00244F50` call).


## SWE2-EC7-73 update (2026-09-19) - `003FFF40` record state decoder measured

`003FFF40` (39 B) is the record decoder the config-screen and layout
callers share: `word[+0xA] == 1` or `word[+8] == 0` returns 0; `ax == 0`
returns 1; otherwise `movsx ecx, ax` tails `0032A8A0` - the
validity-gated value dispatch for the `+8`/`+0xA` record shape the UI
bodies read.
Interior anchor `003FFF62` (the `jmp 0032A8A0` tail).

## SWE2-EC7-74 update (2026-09-19) - `00377870` table string lookup measured

`00377870` (49 B) is the `02ADD0F8` string-table lookup: `ecx` under
`[rdx+8]` reads `word[rdx + ([rdx+4] + ecx)*2 + 0x10]`; a nonzero word
returns `rdx + word` (the offset into the table), anything failing
returns `01CEB638` - the empty-string default the config screen shows.
Interior anchor `00377888` (the `+0x10` indexed word read).

## SWE2-EC7-75 update (2026-09-19) - `002D2D40` verb-class dispatch measured

`002D2D40` (98 B) is the class dispatch the config screen reaches:
`edx` 1..3 reads `byte[+0xFF]` (sign-extended, `-1` aborts), requires
`[+0xE0] & 0x400000` clear, then `movsx ecx, ax` and `+0xE4` bit
`0x20000000` picks `00249CA0` vs `00249C60`; `edx` 4..6 skips the byte
read and uses `ecx = 0x17` on the same bit test - the two-class tail
selector.
Interior anchor `002D2D5F` (the `jmp 00249CA0` arm).

## SWE2-EC7-80 update (2026-09-20) - `00567770` + `00568B30` + `005678A0` measured

`00567770` (48 B) is the `02CA96D8` lazy init `00280DE0`/`002D70F0`
rely on: a NULL global runs `00244F50(0xD0, 005677A0, 0)` - a 0xD0-byte
object with the `005677A0` callback - and stores it back.
Interior anchor `0056778F` (the `00244F50` create call).

`00568B30` (121 B) is the triple-issue on `[0209AC30]+0x160`: while
that slot is NULL it runs `00244F50(0x368, 005691E0, &args)` three
times with the caller's `ecx`/`edx` packed into the stack block -
stack-cookie guarded.
Interior anchor `00568B80` (the `00244F50` call).

`005678A0` (25 B) is the gated forwarder: a live `[02CA96D8]` tails
`00246AD0([0208EA28], rdx)`; a NULL one returns.
Interior anchor `005678AC` (the `0208EA28` load).

## SWE2-EC7-81 update (2026-09-20) - `005601B0` lazy-create measured

`005601B0` (95 B, stack-cookie) is the `*(0209AC30) + 0x158` lazy
init `00281ED0`/`002D70F0` rely on: a NULL slot runs
`00244F50(0x190, 00560910, &args)` with the caller's `ecx` packed
into the stack block - the same gate `00568B30` uses on `+0x160`.
Interior anchor `005601F3` (the `00244F50` call).

## SWE2-EC7-85 update (2026-09-20) - `00407720` centisecond time formatter measured

`00407720` (626 B) is the elapsed-time formatter the screen callers
run: `00407D10(rcx)` then `+0x50` bit 0 gates `00394690([+0xC8], 2)`
into `rbp`; the `+0x130` bit-0 arm folds `+0xE4` centiseconds through
`0x88888889` magic division into M:SS:cc (clamped 999:99), picks the
`002F9860` string by `+0xD8` bit 1 (`0x4B3E`/`0x4B3D`), and formats
into `rdi+0x134` via `00364980` + `00365B30`/`002B4090` before
`0020E620(0)` registers into `[rbp+0x18]`/`+0x20`; the else arm does
the full h:m:s:cc decomposition (`0x9B583739`/`0x91A2B3C5` magics),
uses `0x4B3C`, and also copies `[rdi+0xF4]` into `[rbp+0x24]`.
Interior anchor `00407774` (the `0x88888889` `imul`).

## SWE2-EC7-86 update (2026-09-20) - `00400190` counted-list append cited

`00400190` (54 B) is the intrusive push_back the config-screen
change path shares with the icon drawers: head/tail at `[rcx]`/
`[rcx+8]`, link fields `+0x28`/`+0x30`, count at
`word[+0x1412]` - empty-head seeds both ends; otherwise splice
after tail and bump the count. Body measured on
`the-second-icon-drawer-and-what-it-adds.md`.

## SWE2-EC7-92 update (2026-09-20) - `00393220` flag predicate measured

`00393220` (26 B) is the two-gate flag test the config-screen
walkers run: `rcx == 0` or `[rcx+8] bit 0` clear answers 0, otherwise
the answer is bit 28 of the first dword of `[rcx]`'s record.
Interior anchor `00393231` (the record dword load before `shr 0x1C`).

## SWE2-EC7-94 update (2026-09-20) - `0035F130` + `0035EEB0` measured

`0035F130` (22 B) is the plain row-header read `002498B0` and
`0036FDF0` use: `ecx*0x294` into the same `02CDB457` table and the
byte at `+0` comes straight back.
Interior anchor `0035F141` (the row byte fetch).

`0035EEB0` (94 B) is the second `+0x44`-family accessor `002498B0`,
`003594E0` and `0046DB10` call: `ecx >= 2` returns 0x80, otherwise
the `0x294` record at `02CDB588` has byte `+1` advanced by `r8d`
with the same dual wrap (negative `+0x10 & ~0xF`, overflow mod 16),
and the wrapped index fetches the unsigned byte at `+0x58 + edx`
inside the `9*4` index row.
Interior anchor `0035EF08` (the `+0x58` byte fetch).

## SWE2-EC7-99 update (2026-09-20) - `002D9DB0` + `002D4B70` measured

`002D9DB0` (1,312 B) is the textured-quad emitter
`002D0650` calls: the four shorts of the source rect expand
to `x+w`/`y+h`, a `0xA`-tagged packed header goes out first
(three `shl 0xA` field packs plus the tag `or`), then a
repeating pattern writes colour dwords (from `r13+0x90`
through `+0x93`) and coordinate dwords into the `+0x10`
cursor of the draw record at `r11`, two `00202B70`
transform applications normalize UVs by `divss` against
the w lanes, `00181890` submits the first vertex block,
and four `0x30`-stride vertex records at `rbp-0x80`
(position pair, RGBA lanes, UV pair, `0x3F800000` w) feed
`00181460` - the full single-quad submission the config
preview runs.
Interior anchor `002D9E57` (the packed header store).

`002D4B70` (492 B) is the sibling paged-cursor step
`002D4650` and `002D46F0` call: the same `+0x100`/`+0xEA`
page pitches and `+0x9E`/`+0x9C` index arithmetic as
`002D4D60`, but the clamp writes the second axis pair
`+0xF4`/`+0xF6` and `+0xED`/`+0xEE` record the opposite
edge - the other-direction advance the same grid cursor
takes.
Interior anchor `002D4C39` (the `+0xF4` write).

## SWE2-EC7-101 update (2026-09-20) - `002B3280` measured

`002B3280` (64 B) is the forwarding trampoline `00227EE0`,
`00241D40`, `0057C140` and `0057C480` call: three stack
arguments are repacked (`rsp+0x20`/`+0x28`/`+0x30` from
`+0x80`/`+0x88`/`+0x90`, `+0x38`/`+0x40` zeroed) into a
single `002B32D0` call - the argument-adapter the
setting-change arms reach through.
Interior anchor `002B32B6` (the forwarded call).

## SWE2-EC7-103 update (2026-09-20) - `00280CF0` measured

`00280CF0` (47 B) is the shorter teardown prefix
`00281ED0` and `002D70F0` call: `00244DD0` on
`[0209AC30]+0xD8` when nonnull, then `002CF870`
and `005112A0`, tailing `002CF6F0` - the
three-call close the config-change arms share.
Interior anchor `00280D07` (the `00244DD0`
call).

## SWE2-EC7-105 update (2026-09-20) - `00255150` measured

`00255150` (82 B) is the bounds-checked
bitfield read `003C1180`, `003C4810`,
`003C6420`, `00402000` and `004048E0`
call: `edx` and `r8d` must sit inside
`[0, r9d)` and `[0, [rsp + 0x28])`
respectively, the byte fetched is
`[rcx + (edx >> 3) + r8d * [rsp + 0x30]]`,
and the answer is the bit at position
`edx mod 8` - the row-strided bit probe
the config arms share.
Interior anchor `00255178` (the byte
fetch).

## SWE2-EC7-107 update (2026-09-20) - `00241A50` measured

`00241A50` (20 B) is the
slot-present probe `00228C70`,
`00279E20` and `0027C3D0` call:
answers `0208EA60[movsxd(ecx)] != 0`
- the single indexed occupancy test
the config arms share.
Interior anchor `00241A5C` (the
table compare).

## SWE2-EC7-113 update (2026-09-21) - `00865510` measured

`00865510` (34 B) is the
three-field predicate
`00798FF0` runs: it returns
1 only when
`dword[+0x88] <= 1` AND
`dword[+0x84] == 0` AND
`dword[+0x80] == 1` - the
`cmove` folds the last test
into the return, so any
counter above 1 or a set
`+0x84` vetoes the whole
answer.
Interior anchor `0086552E`
(the `cmove`).

## SWE2-EC7-114 update (2026-09-21) - `007A03D0` measured

`007A03D0` (57 B) is the
window-procedure step
`001DC7A0` runs:
`byte[02EA5360]` clears,
IAT `008C2880` on the
`02EA5248` object with
`edx = -0x15` (-21) swaps a
window field, and
`007A3BD0(rax + 0x48)`
forwards the result's
`+0x48` object into the
`+0x30`-mode vtable call -
the subclass swap feeding
the shared forwarder.
Interior anchor `007A03FF`
(the `007A3BD0` call).

## SWE2-EC7-122 update (2026-09-21) - `00624490` measured

`00624490` (231 B) is the
`+0x1878` enumerator
`001DD170` calls:
`vtable[+0x38]` fetches the
enumerator object,
`vtable[+0x40]` reads its
info, then for each of the
`esi` indices a
`vtable[+0x38]` produces
the item and the item's own
`vtable[+0x38]` fills the
caller's `rbp`-based
0x60-stride record
(`r9 + index * 0x60`); both
levels end in
`vtable[+0x10]` releases.
Interior anchor `0062452F`
(the item `vtable[+0x38]`
call).

`00326D60` (1005 B) is the config worker `00281E00` runs: `022C25A0 & 1` and `02089340 & 0x10` flag-gate the arms, `byte[rax+4]` seeds the step, `0030A880`, `003590D0`, `003588B0`, `00263E30`, `0031B770` x2, `00313F60` x4, `003003F0` x2, `00311F70`, `00236850` x2, `00236820` and `0024C600` drive the rebuild - the setting-change path's flagged worker; its `00263E30`, `00236820`/`00236850`, `00313F60` and `00311F70` helpers are shared with Combat-, Spawn_Encounter_Lifecycle- and Status_Periodic_Terminal-side callers.

Interior anchor `00326F86` (function `00326D60`).

`003FAB60` (395 B) is the record fill `003FB3E0` calls: `003F0040` resolves the target, `00202C90` string-copies into `rbx` and `rbx + 0x10` (four calls total), stack args `[rsp + 0x88]`/`[+0x80]`/`[+0x98]` bound `<= 4`, `003F1230`/`003F1290` commit - the config screen's entry writer.

Interior anchor `003FAB81` (function `003FAB60`).

`002B32D0` (299 B) is the record init `002B3280` calls: `002AC1E0` base-fills `rdi`, stack args land at `+0x70`/`+0x78`/`+0x84`, `0039BAD0(rdx)` writes `byte[+0xA6]`; `00254A10` false + `+0xA6==7` sets `+0x44 |= 0x800` and stores `0039C4A0((+0x44>>0xB)&1)` into `+0x60`; `ebp` nonzero runs `002B3C30`, and the out-params take `word[+0x94]+8` - the measure trampoline's record constructor.

Interior anchor `002B3301` (function `002B32D0`).

`002B3C30` (287 B) is the font-metrics init `002B32D0` runs when `ebp` is nonzero: `rdx` stores at `[rcx+0x28]` and `byte[+0xA3]` clears (null exits); `002B24B0` returns the metric pair, `cvttss2si` converts them into `word[+0x96]`/`word[+0x94]` and the floats into `[rbx+0x80]`/`[rbx+0x48]`, `word[+0x90]` takes `-byte[+0x9E]`, `byte[+0xAF]` and `dword[+0xB0] bit 23` take the out-flag (`&1<<0x17`) with bit `0x800000` first cleared; `002B2150` measures the text, then a zero `[rbx+4]` defaults to `23.0f` and `[rbx+0xC]` sets `1.0f` - the record constructor's text-size leg.

Interior anchor `002B3D21` (function `002B3C30`).

`002B3D50` (220 B) is the control-record init plus escape scan: clears `byte[+0xB0]/+0xA3/+0x9D/+0xAB/+0x44` and `dword[+0x8A]`, stores `rdx` at `+0x28`, writes `word[+0x90]` = `-sbyte[+0x9E]`, clears bit 20 of `dword[+0xB0]`, sets `byte[+0xAE] = 0xFF`, runs `002B2150(rcx)`, defaults `float[+4]` to 23.0f when zero and `float[+0xC]` to 1.0f, then walks `rdx` for a `0x0F`+`=` pair routed through `003FFAB0(rbx, rdi+0xAE)` - the option-control constructor the input and config callers share.

Interior anchor `002B3DC2` (function `002B3D50`).

`003F5290` (216 B) is the packed panel-record initializer `003FBA80` runs: writes `+0x70..+0x78` = `0.15f` (0x3E19999A), `+0x7C` = `1.0f`, `+0x80..+0x8C` = `2044.0f` (0x44FFF000), copies the caller's `+0xC` field, sets `+0x60..+0x68` position floats, stamps `0x10000000` command words at `+0`/`+4`/`+8`/`+0x98`/`+0x9C`, `0x6C088000` at `+0xC`, `0x13000000` at `+0x90`, and `+0x94` = `eax | 0xA0000007` from `02EBB798`

Interior anchor `003F5319` (function `003F5290`).

`003F5BE0` (180 B) is the packed-block builder `003FBA80` appends per settings row: the fixed header `0x10000000` is written at `+0`/`+4`/`+8`, field `[rcx+0x5C]` folds into two constants - `+0xC = ((n + 5) << 16) | 0x6C008000` and `+0x40 = (n*4 + 2) | 0x3000000000008000` - `+0x10`/`+0x18`/`+0x20`/`+0x30`/`+0x48` take `0x1000000000000002`/`0xE`/`0x5B`/`0x5C`/`0x412`, a 16-byte `0x13000000`/`0x17000000`/`0x10000000`/`0x10000000` tail record lands at `r8 + ((n + 6) << 4)`, and the return is the block's `+0x10`-biased length

Interior anchor `003F5C72` (function `003F5BE0`).

`00407150` (233 B) is the bit-1 flag setter `00408190`/`004088A0`/`004088B0` call on the row object: `dword[rcx+0xC8]` bit 1 is compared against `edx` and xor-replaced only when it differs; the child `rbx = [rcx+0xC0]` then either (a) when `byte[+0xC0]` is clear, commits `+0x118` into `+0x114`, adds `+0x11C` into `+0x124` and `+0xE4`, forces `+0x128` to 1.0f and runs `00407450`, or (b) picks `+0xE0`/0 into `+0xE4` by `byte[+0xDC]` and runs `00407720` - both paths end `or dword[+0xD8], 0x20`, the dirty flag this page's rows honour.

Interior anchor `004071E3` (function `00407150`).

`0056C3A0` (239 B) is the child-visibility combinator `005677A0` runs on a settings change: manager `0209AC30`'s `+0xDE0` word resolves through `00282DF0`, the record's `+0x60` word indexes `02EBF190+0x7370` into `+0xC0`/`+0xC4`, and the mode then sets or clears bit 0 of `+8` across the `+0x60` chain's five children (alternate arms for modes 1 and 2) - the panel-visibility propagation a settings change triggers..

Interior anchor `0056C3C7` (function `0056C3A0`).

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-the-config-screen-and-what-a-setting-cha-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0017E050` | 25 B | loads `rcx` from qword `02EA5248`, sets `edx` = 0x10, `r8d` = 4 and `r9d` = 0, and tail-jumps through the pointer at `008C2820` | `0017E057`, `0017E05A`, `0017E05E`, `0017E062` |
| `0024C600` | 56 B | returns at once when `ecx` is zero or `edx` is zero; otherwise calls `002FBFA0` (with `ecx` and `edx` still as passed), then `003B0190(ecx, edx)` and `003B14F0(ecx, edx)`, and returns | `0024C602`, `0024C614`, `0024C616`, `0024C61F`, `0024C628` |
| `002726C0` | 79 B | stores `edx << 4` at dword `+0x0` and `r8d << 4` at dword `+0x4` of the record at `rcx`; with `d` = dword `+0x4` minus dword `+0x0` (a 32-bit difference, then sign-extended), stores `(r9d * d >> 8) + (edx << 4)` at `+0x8`, `(fifth stack argument * d >> 8) + dword +0x0` at `+0xC` and `(sixth stack argument * d >> 8) + dword +0x0` at `+0x10` (64-bit products, arithmetic shifts, 32-bit sums), and 0x400 at dword `+0x14` | `002726C3`, `002726CD`, `002726E0`, `00272704`, `00272707` |
| `002727C0` | 39 B | divides 0x400 (signed) by `edx` when `edx` is greater than 0 (signed), else by 1, stores the quotient's low word at word `+0x16` of `rcx`, and overwrites that word with 1 when it is zero; returns the quotient in `eax` | `002727D0`, `002727D5`, `002727D8`, `002727DC`, `002727E1` |
| `0029B790` | 57 B | returns 1 when qword `+0xB20` of `rcx` is null; otherwise calls that pointer with `rcx` = qword `+0xB30`, `r9d` = the sign-extended byte `+0xB48` (`rdx` and `r8` as passed) and returns 1 when the call returns non-zero, else 0 | `0029B79B`, `0029B7A0`, `0029B7AA`, `0029B7B9`, `0029B7BF` |
| `002CD8A0` | 81 B | subtracts 0x4B3 from `ecx` and returns 0x10 when the result is above 9 (unsigned); otherwise jumps through a 10-entry table of image-base-relative dword offsets indexed by the result, which sends `ecx` = 0x4B4 to the arm returning 0x11, 0x4B6 to 0x12, 0x4B5 to 0x13, 0x4B9 to 0x14, 0x4B7 to 0x15, 0x4B8 to 0x16, 0x4BC to 0x17, and 0x4B3, 0x4BA and 0x4BB to the 0x10 arm | `002CD8A6`, `002CD8A9`, `002CD8B5`, `002CD8BF`, `002CD8EB` |
| `00408190` | 100 B | reads qword `02B62D80` and takes `rbx` = its qword `+0xC0` (0 when the global is null); calls `00407150(qword 02B62D80, 0)`; then, when `rbx` is non-null, calls `00244DD0` with qword `+0xC0` of a fresh read of `02B62D80` (0 when that is null) and in dword `+0xD8` of `rbx` clears bit 2 (AND 0xFFFFFFFB) and sets bit 3 (OR 8) | `004081A8`, `004081B6`, `004081D6`, `004081DB`, `004081E2` |
