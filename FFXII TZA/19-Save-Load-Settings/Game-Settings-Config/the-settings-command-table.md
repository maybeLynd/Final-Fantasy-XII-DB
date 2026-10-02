---
system: in-game settings command table (Config screen -> save-backed options record)
category: 19-Save-Load-Settings
status: AUDITED
owner_layer: Save_Load_Settings
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: both 35-slot dispatch jump tables dumped from the image; every setter and
    getter body disassembled; descriptor table 0x01E0BF60 dumped and walked through
    the pane repeater 0023ED80; row labels decoded from the shipped text pools
    (menu_command.bin / menu_message.bin / help_menu.bin) with a cstring-at-offset
    read - the st2e offset array is NOT monotonic, slicing between adjacent offsets
    returns empty for five of the labels
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-settings-falsification-pass-1
  crossref_clean: true
  reopened_count: 0
  note: written for FABLE-REQ-SWE2-DATA-SETTINGS-COMMAND-TABLE; pending
    SWE2-AUDIT-SPEC first review
  promoted: 2026-10-01 DOCUMENTED -> AUDITED by SWE2-AUDIT-SPEC (FRONTIER eligibility census sweep): falsification record opus-settings-falsification-pass-1; audit_crossrefs at HEAD reports 0 unresolved findings; cross-subsystem neighbours dispositioned in their section; killer observations recorded in the pass; promoter is not the last substantive author (last substantive commit: SWE2-DATA)
container_format: options-record + ui-descriptor
---

# The in-game settings command table

> **The Config screen talks to the saved options through a 35-slot command dispatch.**
> Nineteen command ids have handlers (21 handler functions: commands 8 and 14 each
> call two); commands 4-21 write the save-backed options record `*(0x0215E6E0)` and
> commands 28-30, 38 write `GameSetting.ini` fields through `001DF340`.
> **Command 4 is the Battle Mode option (options word bit 3, Wait=0 / Active=1)** —
> the ASTRA AQ-13 row is readable and named.

**For a player.** This is everything the in-game Config screen can change: Battle
Mode and Battle Speed, Target Lines, cursor memory, vibration, screen shake,
subtitles, both camera axes, the 2x/4x speed-mode multiplier, voice language,
soundtrack, three volumes — plus the four entries on the Controls screen
(camera auto-rotation, both mouse sensitivities, confirm-button layout).

---

## 1. The command dispatch

Two symmetric switch dispatchers, each over command ids **4..38** (`cmd-4` indexes
a 35-slot table of image-base-relative offsets; unhandled ids jump to the shared
epilogue):

| | address | table | default arm | arm shape |
|---|---|---|---|---|
| SET | `002407F0` | `0x00240968` | `0x0024095E` | `mov ecx,[rbx]; call SETTER; jmp 0016D6A0` |
| GET | `002403F0` | `0x00240518` | `0x00240512` | `call GETTER; mov [rbx],eax; ret` |

`0016D6A0` is the shared ~~post-set notifier~~ tail every handled arm jumps to
(~~generic UI-dirty broadcast,~~ a bare `ret 0` that notifies nothing *(corrected 2026-10-02, OPUS: `0016D6A0` is `ret 0`; CONTRACT-save-image-buffers.md — a port must not add a notification)*; ~2.4k callers — not options-specific).

Row-side wrappers: **`00240750`** normalises the widget's value through a 35-byte
selector table before calling the SET dispatcher; **`00240330`** calls the GET
dispatcher then applies the *same* selector table to convert stored->display.
The selector tables at `0x2407C0` (set) and `0x2403CC` (get) are **identical byte
arrays**; the two functions implement inverse semantics per selector:

| sel | 00240750 (choice->store) | 00240330 (store->choice) |
|---:|---|---|
| 0 | `v = (v != 0)` | `v = (v != 0)` |
| 1 | `v = v + 1` | `v = v - 1` |
| 2 | `v = (v == 0)` | `v = (v == 0)` |
| 3 | passthrough | passthrough (default arm) |
| 4 | `v = (v != 1)` | `v = (v != 1)` |
| 5 | passthrough | passthrough (default arm) |

Per-command selector (`00240750`/`00240330`, indexed by `cmd-4`):

```
sel bytes: 00 01 02 05 02 02 02 02 00 00 05 05 02 03 05 05 05 05 05 05
           05 05 05 05 02 01 01 05 05 05 05 05 05 05 04
cmd  4    -> sel 0    cmd 12,13 -> sel 0    cmd 17 -> sel 3
cmd  5    -> sel 1    cmd 6,8-11,16,28 -> sel 2
cmd 29,30 -> sel 1    cmd 38    -> sel 4    all others -> sel 5
```

## 2. The options record

`*(0x0215E6E0)` is a pointer installed by **`002DDE60`** (defaults installer) to
`002536A0()+8` — i.e. the options record is a field inside the active save-data
buffer (`*(0x020927C0)+8`). `002DE040` is the `*(0x0215E6E0) != 0` predicate.
The record is 0x28 bytes (the shadow copy at `0x0215E6E8` is filled with a 0x28
template before being pushed into the record):

| field | meaning |
|---|---|
| `+0x00` bits 0-1 | 2-bit field — `002DDCF0`/`002DE150` accessor pair, no command (internal) |
| `+0x00` bit 2 | `002DDCE0` reader — no callers found |
| `+0x00` bit 3 | **cmd 4 — Battle Mode** |
| `+0x00` bits 4-11 | **cmd 5 — Battle Speed**, signed byte (`shl 0x14; sar 0x18` on read) |
| `+0x00` bit 12 | **cmd 11 — Subtitles** (stored bit = display value; see §5) |
| `+0x00` bit 13 | **cmd 9 — Vibration** (stored inverted) |
| `+0x00` bit 14 | **cmd 10 — Screen Shake** (stored inverted) |
| `+0x00` bit 15 | **cmd 8 — Cursor Position** (stored inverted) |
| `+0x00` bit 16 | written with bit 15 by cmd 8's compound arm; own reader `002DDD40` (callers `002778C0`, `00290CF0`) |
| `+0x00` bits 17-24 | byte field; bit 17 = `005C5230()==2` patched in by `002DDE60` |
| `+0x04` bit 8 | **cmd 12 — Camera Y-Axis** (0=Normal, 1=Inverted) |
| `+0x04` bit 9 | **cmd 13 — Camera X-Axis** |
| `+0x04` bit 10 | **cmd 16 — voice Language** (stored inverted: 1=Japanese, 0=English) |
| `+0x04` bit 21 | `002DE270`/`002DDDC0` accessor pair — no command (callers `0034D440`/`00251F40`) |
| `+0x04` bit 22 | **cmd 6 — Target Lines** (stored inverted) |
| `+0x04` bits 23-26 | **cmd 14 — Speed Mode Multiplier**, 4-bit field |
| `+0x08` u16 | **cmd 19 — Music volume** (clamped <= 100) |
| `+0x0A` u16 | **cmd 20 — Sound-Effects volume** (clamped <= 100) |
| `+0x0C` u16 | **cmd 21 — Voice volume** (clamped <= 100) |
| `+0x0E` u16 | **cmd 17 — soundtrack** (0=Original, 1=Reorchestrated, 2=OST) |
| `+0x18` dword | `& 3` -> `002DF360` — applied by `002DDA30`/`0050DA00`, no command |
| `+0x1C` dword | read by `002DDA30`, no command |

**Defaults** (`002DDE60` writes `.rdata 0x00917268` template, then patches):
`dword0 = 0x00000035`, `dword1 = ~~0x62000400~~ 0x00620400` — i.e. bits0-1=1, bit2=1, Battle
Mode=Wait, Battle Speed=3; dword1 bits ~~10/25/29/30~~ **10, 17, 21 and 22** set (corrected 2026-09-29, OPUS, CON-193: the
template bytes are `00 04 62 00`). Then: bit 17 of dword0
`= (005C5230()==2)`; bit 12 of dword0 set iff `00229E40()` is ~~6~~ **1 or 6** (CON-193, `002DDEF9` / `002DDF03`); bit 10 of dword1
set iff `00229E40() in {0,7,8,0xA,0xB}`; bits 8,9 of dword1 cleared and pushed to
`001E1020`/`001E0FF0`. **Then (added 2026-09-29, OPUS, CON-193):** the speed-mode field (dword1 bits 23-26) is
cleared, the soundtrack word `+0xE` is set to 1 and applied (`002DF530(1, 1)`), all three volumes are set to 100 and
pushed through `002DF2B0` on channels 1-3, and the installer tail-jumps the platform applier `002DDA30` with `ecx = 1`.

**Platform applier `002DDA30`** (called with `ecx=1`; `002DE050` tail-jumps it
with `ecx=0`): `00408B80()==1 -> opt+0 |= 0x2000`, `==2 -> &= ~0x2000` (forces
cmd 9's bit from ~~a pad/vibration capability query~~ *(corrected 2026-09-26 (FABLE, Claude Opus 5.5): `00408B80` is a plain getter of `FF12CONFIG` byte `+0x06`; see [the FF12CONFIG page](ff12config-and-debglobal.md) `PC-1`)*); `00408B40()==1 -> opt+0 |=
0x4000`, `==2 -> &= ~0x4000` (cmd 10's bit). Then propagates bit 13 -> `0035FF30`,
bit 14 -> `0037DDC0`, `+0x18 & 3 -> 002DF360`, reads `+0x1C` and `u16[0x0215E6D8]`.

## 3. The full table

Setter/getter addresses are the arm's callee(s); `extra_call` is a second call in
the same arm. `sel` = the §1 normaliser applied on both paths. Field notation
`opt+N` = `*(0x0215E6E0)+N`; `cfg` = the `GameSetting.ini` object `0x01F82D20`
(see `game-settings-ini-and-runtime-config.md`).

| cmd | Config row (label tid -> text) | choices | setter | stores | getter | reads | sel | row style |
|---:|---|---|---|---|---|---|---|---:|
| 4 | `0x42D` "Battle Mode" | Wait `0x431` / Active `0x432` | `002DE060` | opt+0 bit 3 | `002DDC30` | opt+0 bit 3 | 0 | 2 |
| 5 | `0x42E` "Battle Speed" | six-position selector (no text ids) | `002DE0F0` | opt+0 bits 4-11 (s8) | `002DDC90` | same, sign-extended | 1 | 3 |
| 6 | `0x447` "Target Lines" | toggle | `002DE2D0` | opt+4 bit 22 | `002DDE00` | opt+4 bit 22 | 2 | 1 |
| 8 | `0x438` "Cursor Position" | Last Selection `0x43D` / Default `0x43E` | `002DE1E0`+`002DE1C0` | opt+0 bit 15 **and bit 16** | `002DDD50` | opt+0 bit 15 | 2 | 2 |
| 9 | `0x433` "Vibration Function" | toggle | `002DE080` | opt+0 bit 13 -> `0035FF30` | `002DDC40` | opt+0 bit 13 | 2 | 1 |
| 10 | `0x434` "Screen Shake" | toggle | `002DE200` | opt+0 bit 14 -> `0037DDC0` | `002DDD60` | opt+0 bit 14 | 2 | 1 |
| 11 | `0x429` "Subtitles" | toggle | `002DE230` | opt+0 bit 12 (stores `!normalised`) | `002DDD70` | `u16[0x0215E6DC]` bit 0 when that word is non-zero, else NOT opt+0 bit 12 (CON-194) | 2 | 1 |
| 12 | `0x4EB` "Camera Y-Axis" | Normal `0x4EC` / Inverted `0x4ED` | `002DE190` | opt+4 bit 8 -> `001E1020` | `002DDD20` | opt+4 bit 8 | 0 | 2 |
| 13 | `0x4EE` "Camera X-Axis" | Normal `0x4F9` / Inverted `0x4FA` | `002DE160` | opt+4 bit 9 -> `001E0FF0` | `002DDD00` | opt+4 bit 9 | 0 | 2 |
| 14 | `0x4EF` "Speed Mode Multiplier" | `0x4F0` "x2" / `0x4F2` "x4" (glyph-coded) | `002DE250`+`0023B2E0` | opt+4 bits 23-26 | `002DDDA0` | opt+4 bits 23-26 | 5 | 2 |
| 16 | `0x4F3` "Language" | Japanese `0x4F4` / English `0x4F5` | `002DE2F0` | opt+4 bit 10 | `002DDE20` | opt+4 bit 10 | 2 | 2 |
| 17 | `0x4F6` "Music" | Original `0x4F7` / Reorchestrated `0x4F8` / OST `0x502` | `002DE110` | opt+0xE u16 -> `002DF530` | `002DDCA0` | opt+0xE u16 | 3 | 2 |
| 19 | `0x4FC` "(icon) Music" | 0-100 bar | `002DE0B0` | opt+8 u16 <=100 -> `002DF2B0(f,1)` | `002DDC70` | opt+8 u16 | 5 | 6 |
| 20 | `0x4FD` "(icon) Sound Effects" | 0-100 bar | `002DE290` | opt+0xA u16 <=100 -> `002DF2B0(f,2)` | `002DDDE0` | opt+0xA u16 | 5 | 6 |
| 21 | `0x4FE` "(icon) Voice" | 0-100 bar | `002DE310` | opt+0xC u16 <=100 -> `002DF2B0(f,3)` | `002DDE40` | opt+0xC u16 | 5 | 6 |
| 28 | `0x564` "Camera Auto-Rotation" | On `0x421` / (empty `0x422`) | `0017E740` | `001DF340(cfg,22)` CameraRevise | `0017E260` | `cfg+0x58` | 2 | 8 |
| 29 | `0x562` "Mouse Sensitivity L-R" | 1-6 slider | `0032E020` | `001DF340(cfg,24)` MouseSensityY if `v-1<=5` | `0017E420` | `cfg+0x60` | 1 | 7 |
| 30 | `0x563` "Mouse Sensitivity U-D" | 1-6 slider | `0032E030` | `001DF340(cfg,23)` MouseSensityX if `v-1<=5` | `0017E430` | `cfg+0x5C` | 1 | 7 |
| 38 | `0x565` "Confirm Button" | Type A `0x566` / Type B `0x567` | `0017E6E0` | `001DF340(cfg,25)` DecideButton + `00198960` | `0017E210` | `cfg+0x64` | 4 | 8 |

Commands **4, 5, 6, 8 exist only on the in-game panes** (descriptors 0 and 2);
commands 9-21 exist on all three Config variants; commands 28-30, 38 exist only on
the Controls screen (the runtime-built BSS pane).

## 4. How a row reaches its command

**Static descriptor table** `0x01E0BF60`: 45 pointers to descriptors at
`0x01E0B670+` (stride `0xB0`). Descriptor = `{u8 style, u8 id, u16 count,
items[count*6]}`; item = `{u8 child_id, 0, u16 text_id, u16 req_id}`. The child id
of a leaf row **is** the settings command id — it travels `item[0]` -> create msg
`+8` -> child object `+0xC0` -> the row proc's `00240330`/`00240750` call.
*(Scope, 2026-09-30, SWE2-AUDIT-SPEC [`auditspec-review-sd22-0930`](../../_index/candidates/auditspec-review-sd22-0930/REVIEW.md), restated by SWE2-DATA with register row SD-22: the descriptor's `u8 id` equals its own table index for 37 of the 45 descriptors only. Roots `0x00` / `0x01` carry 2, and the unreferenced copies `0x27`-`0x2C` of descriptor `0x17` carry `0x17`. A row's id comes from its parent's child entry, as the sentence above says.)*

**Pane repeater `0023ED80`** (installed into the Config-screen pane proc): reads
`byte[obj+0xC0]` = pane id -> `0x01E0BF60[pane]` -> walks items; per item resolves
`desc[child].style` and creates a leaf widget via `00244F50` for styles that own
one:

| desc style | row proc | kind | rows |
|---:|---|---:|---|
| 1, 2, 8 | `0023E770` | `0xF0` | toggles + choice rows (cmds 4,6,8-14,16,17,18,28,38) |
| 3 | `0023D6B0` | `0xD8` | six-position selector (cmd 5) |
| 6 | `0023EBE0` | `0xD8` | volume bars (cmds 19-21) |
| 0xA | `0023E400` | `0xF0` | Max LP / Max Gil display rows (children 36,37) |
| 4,5,7,9,0xB+ | *(none)* | — | pane-drawn rows: headers, separators, nav entries, action buttons |

**Three Config pane descriptors** (the pane id selects the variant):

- **desc 0** (27 items) — full in-game Config: nav rows 32/33 ("Graphics
  Settings" `0x503`, "Controls" `0x504`), then cmds 4,5,6,8,9,10,11,12,13,14,
  16,17, the "Volume" header (child 18, `0x4FB`), volume sliders 19-21, child 23
  "Restore Defaults" (`0x42B`, style 5 — pane-drawn action row), and children
  36/37 "Max LP"/"Max Gil" (`0x53B`/`0x53C`, style 0xA display rows).
- **desc 1** (23 items) — title-screen variant: three style-0xD menu rows
  (children 24,26,25 -> "Start a new game" `0x7F2`, "Begin New Game[A5]" `0x88E`,
  "Begin New Game[A4]" `0x88F`, bank-2/menu_message labels), then the options
  block **without the battle rows** (no cmds 4,5,6,8) and without Max LP/Gil.
- **desc 2** (24 items) — in-game variant identical to desc 0 minus the
  Restore-Defaults/Max-LP/Max-Gil tail.

**Controls pane** (runtime-built, 41 x 0x14 records at `0x0208E6E4`, filled by the
static initialiser at `002414B0` copying `.rdata` templates `0x914D10..0x914FF0`):
record = `{+0 kind, +4 text_id, +8 req_id, +0xC arg, +0x10 index}`; `0023CE41`
walks it — kind 3 -> `0023DB40`, kind 4 -> `0023E710` (-> `0023E770`), kinds 1-2
-> `0023C5C0` (key-bind rows). Only four records carry settings commands:

| rec | kind | text | req | cmd |
|---:|---:|---|---|---:|
| 34 | 3 | `0x562` Mouse Sensitivity Left-Right | `0xD3A` | 29 |
| 35 | 3 | `0x563` Mouse Sensitivity Up-Down | `0xD3B` | 30 |
| 36 | 4 | `0x564` Camera Auto-Rotation | `0xD3C` | 28 |
| 38 | 4 | `0x565` Confirm Button | `0xD3F` | 38 |

## 5. Command semantics and side effects

| cmd | semantic notes |
|---:|---|
| 4 | **Battle Mode** — bit 3. Consumers `00225CD0`, `00225EB0`, `00227680`, `00254740`, `00255290` (battle wait/active logic). Closes **ASTRA AQ-13**: the row is "Battle Mode"; bit set = Active, clear = Wait. |
| 5 | **Battle Speed** — signed byte at bits 4-11. Selector sel1 makes the stored value `choice+1`; consumer `002F9C00`. |
| 6 | **Target Lines** — bit 22 of dword1, stored inverted. Consumer `0028EAB0` gates target-line drawing on `002DE040()` && bit && state flags. |
| 8 | **Cursor Position** — compound arm writes the same value to **bit 15 and bit 16**; `002DE1E0` tails to `002526D0` which `memset`s the remembered-position table at `savebuf+0x30` (0x1F4 bytes). Bit 15 read by `002526F0` (menu cursor code); bit 16 by `002DDD40` -> `002778C0`/`00290CF0`. Choices: "Last Selection" (remember) / "Default" (reset each time). |
| 9 | **Vibration** — bit 13, stored inverted; propagated by `0035FF30(device<2, on)` to bit 2 of `device[0x294]+9`. `002DDA30` can force it from `00408B80()` ~~(pad capability)~~ *(corrected 2026-09-26 (FABLE, Claude Opus 5.5): `00408B80` is a plain getter of `FF12CONFIG` byte `+0x06`; see [the FF12CONFIG page](ff12config-and-debglobal.md) `PC-1`)*. |
| 10 | **Screen Shake** — bit 14, stored inverted; propagated by `0037DDC0` to `dword[0x02EBF3C4]`. `002DDA30` forces from `00408B40()`. **What reads it (2026-09-21, FABLE):** `0037D9FF`, one of two flags gating the 28-byte accumulator-row copy in `0037D970` — which runs its calculation `003D83A0` **first**, so the option suppresses the *output*, not the work, and an OFF setting is not evidence that the camera-shake sampler stopped ([the camera page](../../17-Presentation-Rendering/Scripted-Camera/how-a-camera-reaches-the-renderer.md)). |
| 11 | **Subtitles** — ~~the only command whose setter and getter touch *different* storage~~ the command whose getter reads other storage only while `0215E6DC` is non-zero *(answered: see the falsification table, C4, CON-194; 2026-10-02, OPUS)*: setter stores opt+0 bit 12 as `!normalised` (net effect: bit = display value, because the sel-2 row normaliser inverts first); getter reads the live flag `u16[0x0215E6DC]` bit 0 (a state word beside the options pointer) ~~.~~ **only while that
word is non-zero; when it is zero the getter returns the inverse of opt+0 bit 12, the setter's own storage
(corrected 2026-09-29, OPUS, CON-194, `002DDD7A`..`002DDD8D`).** Extra caller `002A2C00`. |
| 12 | **Camera Y-Axis** — bit 8 of dword1; propagated by `001E1020`. Help `0xCFB` "Adjust vertical camera controls". |
| 13 | **Camera X-Axis** — bit 9; propagated by `001E0FF0`. Help `0xCFC` "horizontal camera controls". |
| 14 | **Speed Mode Multiplier** — 4-bit field at dword1 bits 23-26 (choices x2/x4 -> stored 0/1). Second call `0023B2E0` re-applies live speed mode: stored 0 -> `00229ED0(1)`+`00182FB0(1)`, stored 1 -> `00229ED0(2)`+`00182FB0(2)`, gated on `00229E20()!=0` (speed mode active). `00229E20`/`00229ED0` are get/set of the live speed-mode dword `0x01FD4A98`. |
| 16 | **Language (voice)** — bit 10, stored inverted (1=Japanese, 0=English); help `0xCFE` "Select language for voices". Consumers `002DEBB0`, `002DF460`, `002DF4D0`. Default set by region id (`00229E40` in {0,7,8,0xA,0xB}). |
| 17 | **Soundtrack** — u16 at +0xE; `002DE110` writes `cx` then, if `cx==2` and `0017E490()` returns 0, forces it to 1 (OST gated behind a flag; `0017E490` is also queried by row procs `0023D890`/`0023DD10`/`0023E770` to offer/hide the OST choice). Applies via `002DF530(stored,1)`; consumer `003EFAA0`. |
| 19-21 | **Volumes** — u16 clamped <=100, converted to `v/100` float and pushed to `002DF2B0` with channel ids 1/2/3. |
| 28 | **Camera Auto-Rotation** — `cfg` setting 22 (`CameraRevise`). sel-2 inversion maps choice "On"->1. Help `0xD3C` "how the camera rotates around the character when they are moving". |
| 29 | **Mouse Sensitivity Left-Right** — slider 1-6 (sel1 +1); writes `cfg` setting 24 (`MouseSensityY`). Help `0xD3A` "horizontal mouse movement" — the ini key names the **rotation axis** (horizontal look = yaw = rotation about Y), consistent with `MouseSensityY`; not a swap. |
| 30 | **Mouse Sensitivity Up-Down** — slider 1-6; `cfg` setting 23 (`MouseSensityX`), "vertical mouse movement" = pitch = rotation about X. |
| 38 | **Confirm Button** — sel4 `v=(v!=1)` maps Type A->1 / Type B->0 into `cfg` setting 25 (`DecideButton`); `0017E6E0` also re-maps the pad buttons via `00198790`/`00198960` and tails `0022A4F0`. |

**Unhandled ids** (default arm, no setter/getter): 7, 15, 18, 22, 23, 24, 25, 26,
27, 31-37. On the panes these are structural rows, not settings: children 7/15/16/22
are `0xFFFF`-text separators; child 18 is the "Volume" section header; child 23 is
the "Restore Defaults" action row; children 24-26 are title-menu entries; children
31-35 are spacers/nav; children 36-37 are the Max LP/Gil display rows. The ids
simply have no get/set semantics — they are not "missing" settings.

## 6. Text-id resolution

The pane proc resolves text group `0x4BE` (`002F9860` call at `0023FD76`). The
shipped text pools index by **`textid = bank*1000 + pool_index`**:

| bank | file (test_battle/us/binaryfile/) | used for |
|---:|---|---|
| 1 | `menu_command.bin` (428 entries) | row labels + choice labels (`0x4xx`, `0x5xx`) |
| 2 | `menu_message.bin` | title-menu labels (`0x7F2`, `0x88x`) |
| 3 | `help_menu.bin` (398 entries) | row help text (`0xCxx`, `0xDxx`) |

`st2e` heap caveat: the string-offset array is **not monotonic** — read each
record as a cstring at `heap+base+offs[i]`; slicing to `offs[i+1]` silently yields
empty for backward offsets (five Config labels looked "empty" under the slice
method). Glyphs: byte+0x20 maps linearly onto `A-Za-z`; `0x04` is a space;
`[A2]`=bullet, `[A5]`=dash, `[A8]`=period, `[AA]`=colon, `Q 0x87/0x88/0x89` = the
x2/x3/x4 multiplier glyphs, `0x0F 0x6F 0x82 0x80 0xE4` = the music-note icon on
the volume rows.

Every row's help text (req id -> bank 3) decodes and matches its command:
`0xC37` "In Active Mode, time flows during battle command selection." (cmd 4),
`0xC38` "Set battle speed." (cmd 5), `0xC4B` "Toggle target lines ON/OFF." (cmd 6),
`0xC3E` "Configure battle menu cursor behavior." (cmd 8), `0xC3B` vibration (cmd 9),
`0xC3C` screen shake (cmd 10), `0xC33` subtitle display (cmd 11), `0xCFB`/`0xCFC`
vertical/horizontal camera (cmds 12/13), `0xCFD` speed-mode multiplier (cmd 14),
`0xCFE` "Select language for voices." (cmd 16), `0xCFF` soundtrack (cmd 17),
`0xD00`-`0xD02` volumes (cmds 19-21), `0xD3A`/`0xD3B` horizontal/vertical mouse
sensitivity (cmds 29/30), `0xD3C` camera auto-rotation (cmd 28), `0xD3F` confirm
button (cmd 38), `0xC35` "Restore default settings." (child 23), `0xD1C`/`0xD1D`
"Max out your LP/Gil." (children 36/37), `0xD03`/`0xD04` nav rows.

## 7. Reachability summary

- **Player-facing, in-game Config (descs 0/2):** commands 4-6, 8-14, 16-21.
- **Player-facing, title-screen variant (desc 1):** commands 9-21 only — the
  four battle rows (4,5,6,8) are absent there.
- **Player-facing, Controls screen (BSS pane):** commands 28, 29, 30, 38.
- **Not reachable as commands:** ids 7,15,18,22-27,31-37 (structural rows; §5).
- **Saved options fields with no command:** opt+0 bits 0-1 (accessor pair
  `002DE150`/`002DDCF0`, reader `004742A0`), opt+0 bit 2 (`002DDCE0`, dead),
  opt+0 bit 16 (cmd-8 mirror, `002DDD40`/`002778C0`/`00290CF0`), opt+0 bits 17-24
  (`005C5230`-derived byte), opt+4 bit 21 (`002DE270`/`002DDDC0`, callers
  `0034D440`/`00251F40`), opt+0x18 (`&3` -> `002DF360`), opt+0x1C.
- **ini-backed:** commands 28-30 and 38 land in `GameSetting.ini` slots 22-25
  via `001DF340`; all other ini slots (0-21, 26-30) are the graphics/display
  config documented in `game-settings-ini-and-runtime-config.md` — a different
  screen (`00914710` row table) that does not go through this dispatcher.

## 8. Artifacts and open questions

- `members/settings_command_table.tsv` — the full per-command table, regenerated
  by `members/gen_settings_commands.py` (re-derives every cell from the image and
  the three text pools).
- The pane-id -> screen binding (which screen instantiates desc 0 vs desc 1 vs
  desc 2) is inferred from item content, not from a traced creator table: desc 1
  carries title-menu labels, so it is the title-screen variant; descs 0/2 are the
  two in-game variants. The screen-creator path (message-dispatched procs
  `0023FCD4`/`0023CE41`) has no direct-code callers to cite.
- `00229E40` language-id domain: ids {0,7,8,0xA,0xB} select the ~~non-Japanese~~
  ~~voice default~~ Japanese voice default *(corrected 2026-10-02, OPUS: `002DDF24`–`002DDF6E` set bit 10 of dword1, stored 1 = Japanese, for those ids; §2)*; the full id->region map is owned by the language-selection page.
- Choice item ids (`0x2D`, `0x36`, ...) are second-level descriptor references;
  their second u16 (`0xC34` shared by several rows) is carried but its consumer
  is unverified - it is *not* the per-choice help (rows' help comes from the item
  req id).
- `u16[0x0215E6DC]` (cmd 11's live flag) is written through a non-direct path
  (no direct store found); presumed maintained by the options-load/propagation
  path alongside `u16[0x0215E6D8]`.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2.
Edges from `edges.tsv` (tier 2: ledger names, sizes and edges.tsv; the setter/propagation bodies
themselves were disassembled for this page). Registry rows in
`_index/candidates/neighbour-dispositions.tsv`. Which layers this page claims about: the command
table IS the contract between UI rows and the option fields, so a layer the handlers deliberately
call (Input propagation, Audio application, the speed-mode get/set) is a claimed crossing; a layer
that merely surrounds a cited consumer or helper is ruled out of scope.*

- **Input — SERVICE and CLIENT.** SERVICE: the setters push changes into the input layer live —
  cmd 38 `0017E6E0` calls `InputManager_GetSingleton`/`00198960`/`0022A4F0` to rebind the confirm
  button; cmd 9 `002DE080` propagates via `0035FF30`; cmds 12/13 `002DE160`/`002DE190` propagate
  camera inversion via `001E0FF0`/`001E1020`; defaults `002DDE60` and the platform applier
  `002DDA30` run the same three propagators. SERVICE: the Battle-Mode consumers `00225CD0`,
  `00225EB0`, `00227680` call the pad-request bodies `00182CD0`/`00182CF0`/`00182D10`/`00182D40`/
  `00182D60`/`00182DA0` — the request family bit 3 selects among. SERVICE: Controls-pane row proc
  `0023C5C0` calls input helpers `001E0920`/`001E0AA0`/`001E0C50`/`001E1050`, and the propagators
  themselves reach `InputManager_GetSingleton`/`001989E0`/`001989F0`. CLIENT: `0022A4F0` calls
  getter `0017E210` and setter `0017E6E0`; the input-manager singleton `00198790` is driven by 45
  input bodies. The layer is where half these commands take effect; the crossing is the claim.
- **Audio — SERVICE and CLIENT.** SERVICE: soundtrack setter `002DE110` — itself Audio-filed —
  applies through `002DF530`; the voice-language appliers `002DF460`/`002DF4D0` reach
  `001DC190`/`001DC1E0`/`002DE800`; `002DF530` reaches `001DBAC0` and is also run by `002DDA30`/
  `002DDE60`. SERVICE: the four row procs `0023D6B0`/`0023DB40`/`0023E770`/`002778C0` call
  `00249C60`, the UI tick sound. CLIENT: voice-language consumer `002DEBB0` is read by
  `003E9B10`/`003E9C10`/`003EA430`/`003EA540`; options reader `002DE050` by `00360D30`/`00361080`;
  `002DF460`/`002DF4D0` by `003A0E50`/`003A0E20`; `003EFAA0` calls `002DECE0`. Volume and voice
  language are audio claims by definition.
- **CombatAction — CLIENT.** `BattleAction_ComputeChargeProgressStep` (`002F9C00`) calls
  `002DDC90`, the cmd-5 battle-speed getter — the stored speed feeds charge-progress stepping,
  inside `BattleUnit_AdvanceStandardActionState` (`00304850`). The remaining edges are the cited
  consumers' own combat plumbing: `00313DB0` calls Battle-Mode consumer `00225CD0`, and
  `002778C0` calls `BattleUnit_IssueCommandByFocusHandles{,WithOptionalPartyFanout}`
  (`00311B20`/`00311CD0`).
- **CoreRuntimeScheduling — SERVICE.** Defaults init `002DDE60` calls `00229E40` (the cached
  language id) to pick the voice default; cmd 14's live notifier `0023B2E0` calls `00229E20`/
  `00229ED0`, the get/set of the live speed-mode dword. `0022A0B0`→`0017E210` and
  `0017D670`→`00198790` are core init/frame calls into cited subjects — mechanical fan-out, named.
- **Gameplay — OUT-OF-SCOPE.** `BattleSystem_ResetRuntimeState` (`00237DF0`) calls `00229ED0` —
  the runtime reset reuses the same speed-mode setter the cmd-14 notifier uses. The page claims
  the settings path, not every caller of the shared setter.
- **Party — CLIENT.** `004742A0` reads `002DDCF0`, the no-command opt+0 bits 0-1 accessor (§7);
  its caller `PartyControl_ApplyAnalogLocomotionToActor` (`00358CB0`) places the field inside
  analog-locomotion handling — consistent with a movement-mode option that has no menu row.
- **Presentation — SERVICE and CLIENT.** SERVICE: Target-Lines consumer `0028EAB0` calls seven
  presentation bodies `003F0170`/`003F1530`/`003F2CF0`/`003F3260`/`003F5100`/`003F5390`/`003F7200`
  — the draw path the bit-22 setting gates. CLIENT: `00434CD0`/`00435050`/`002B0280` call
  `00229E40` (the vertex-prep language gate); `001D1660` — the 13,753-byte graphics-config
  applier — calls `0017E260`/`001DF340`/`0032E020`/`0032E030`, the same cfg getter/key-map the
  Controls commands use; `0032B1C0`→`0017E260`, `00579420`→`002526F0`,
  `003B2310`/`003E9780`→`002DEBB0`.
- **Resource — SERVICE.** `0028EAB0` also calls `0024A5A0` inside the same target-line path —
  the resource leg of the Presentation crossing above.
- **Rewards_Progression_Economy — OUT-OF-SCOPE.** `EnemyChain_UpdateOnDefeat` (`00317ED0`) calls
  `00229E40`; chain bookkeeping consulting the language id is not a settings claim.
- **Script_VM_Native_Bridge — CLIENT.** `0034D440` calls `002DE270`, the no-command opt+4 bit-21
  setter — the script bridge is why that field exists without a menu row. `0033FED0`/`0034BA00`
  call `00229E40`; `0034B650` calls `002DEBB0`; `0050DA00` calls `002DF360` (the opt+0x18 apply,
  §2). `0034D440`/`0050DA00` reach `VMValueStack_PopInt32CoerceFloat32` (`00267E10`) — the script
  argument pop, a hop inside the same natives.
- **ActorEntity — OUT-OF-SCOPE.** `00225CD0`/`00225EB0` are cited for their Input-service calls
  under the bit-3 gate. Their ActorEntity edges — callees `ActorManager_GetRecordByOrdinal`
  (`00358940`), `00263FF0`, `00359B80`, callers `00263050`, `002628B0` — are the consumers' own
  iteration machinery; the page claims nothing about that layer.
- **World — OUT-OF-SCOPE.** `00266D10` calls `00225CD0` — the Battle-Mode consumer's own caller
  in the world-area layer; same reasoning as ActorEntity.
- **Story_Event_Quest_Hunt — OUT-OF-SCOPE.** `0035CA70` — cited below as a caller of `002DECE0`,
  the persisted 0x7F-clamped setter — calls `0032AB60`. That callee is the shared caller's own
  Story-layer plumbing; the page claims the settings path, not its callers' callees.
  (SWE2-EC7, 2026-09-20.)

## SWE2-EC7-30 update (2026-09-18) — `00271450` current-record getter (via `003F2CF0` family)

`00271450` (37 B) — reached through `003F2CF0`, `003F3260`,
`003F0170`, `0028EAB0` and the rest of its 28 callers — is the
current-record getter of the `02EBEFC0` cursor table: `dword[02EBEFF0]`
indexes 24-byte rows (`idx*3*8`), and the out triple is
`{row, row+8, row+8}` — the record pointer plus both cursors
initialized to the row's `+8` field. Interior anchor `00271461` (the
`rax + rdx*8` row select).

## SWE2-EC7-33 update (2026-09-19) - `003F0170`

`003F0170` (**1,183 B** — *corrected 2026-09-19 (SWE2-EC7); this line printed 962 B, a wrong literal in the batch-33 append — the body is 1,183 B per the function list*) is the chain-item presentation body - `"chain_item"`/`"targetline_p"`/`"chainflash"` strings, `00202B70`/`0024ABC0`/`0024ABA0`/`002DD8B0`/`00202FE0`/`00202C90`/`00271100`. Interior anchor `003F035C` (a `00271100` call).

## SWE2-EC7-34 update (2026-09-19) - `002414B0`

`002414B0` (903 B) is the settings-table image writer - ~90 `movdqa` copies of `{id, value}` rows from `00914D10`-`00915030` into `0208E6E0`-`0208EA00`, `1`/`0x27` sentinel stores. Interior anchor `00241738` (a sentinel store).

## SWE2-EC7-36 update (2026-09-19) - `003F3260`

`003F3260` (622 B) is a settings-command body - `008C5F70`/`00915614`/`00915620`/`00915624` rdata run, `003F3710` quadruple plus `003F35C0`/`00271450`/`00270FF0`/`002715A0`. Interior anchor `003F32FA` (an `003F3710` call).

## SWE2-EC7-37 update (2026-09-19) - `003EFAA0`

`003EFAA0` (555 B) is the soundtrack settings consumer - `01F44830`/`003EF4A0`, `00808C40` quintuple plus `00244F00` pair and `00285EC0`/`003EF290`/`002EFA70`/`00244F50`/`002DECE0`. Interior anchor `003EFB2D` (a `00244F00` call).

## SWE2-EC7-37 update (2026-09-19) - `003F2CF0`

`003F2CF0` (550 B) is a settings-command body - `02AEDDB0`/`02AED5F0`/`02B5F1F4`, `002714A0`/`00271080` quadruples plus `002713B0`/`00202C70`/`00202C90`/`003F5390`/`00272390` pairs. Interior anchor `003F2D22` (a `00271450` call).

## SWE2-EC7-38 update (2026-09-19) - `0023ED80`

`0023ED80` (466 B) is the pane repeater the page names - `01F44830`, `0023E770`/`0023D6B0` row procs, `00243260`/`00244F50`/`00244960`/`00808C40`. Interior anchor `0023EDE5` (a `00243260` call).

## SWE2-EC7-38 update (2026-09-19) - `0032B1C0`

`0032B1C0` (461 B) is a settings-command body - `0032DF40`/`0026E500`/`0032CE40`/`0032C910`/`0032B4D0`/`0032B390`. Interior anchor `0032B1FB` (a `0032DF40` call).

## SWE2-EC7-38 update (2026-09-19) - `0023DB40`

`0023DB40` (455 B) is the kind-3 row proc the page names - `02F9736A`/`02F9736C`/`01E0C2A0`, `00240330` triple plus `005C5230`/`00249C60`/`00240750`/`002405F0`/`00392FC0`. Interior anchor `0023DB73` (a `005C5230` call).

## SWE2-EC7-40 update (2026-09-19) - `003F7200`

`003F7200` (381 B) is a settings-command body - `01F44830`/`02AED5F0`, `00203080`/`002703F0`/`003F70F0`/`00808C40`. Interior anchor `003F724D` (a `00203080` call).

## SWE2-EC7-41 update (2026-09-19) - `003F5100`

`003F5100` (350 B) is a settings-command body - `01CEBB70`/`01F44830`/`02AED5F0`, `00202C90`/`00275490`/`00203080`/`002703F0`/`003F6960`/`00808C40`. Interior anchor `003F5135` (a `00202C90` call).

## SWE2-EC7-41 update (2026-09-19) - `0023E400`

`0023E400` (339 B) is the row `0xA` body the table names (Max LP / Max Gil display rows, children 36/37) - `01E0BF60`/`01F44830`, `005C5230`/`0023D4F0`/`00244F50`/`00244960`/`00808C40` pair. Interior anchor `0023E41D` (a `005C5230` call).

## SWE2-EC7-42 update (2026-09-19) - `0023EBE0`

`0023EBE0` (301 B) is the row-6 body the table names (volume bars, cmds 19-21) - `02F97368`, `00240330` triple/`00240750`/`0023D4F0`. Interior anchor `0023EC2B` (a `00240330` call).

## SWE2-EC7-45 update (2026-09-19) - `00251F40`

`00251F40` (236 B) is the deferred-flush body - `0028FF20`/`00290030`/`00290060`/`00290190`/`00290280`/`00290C00`/`002B6140`. Interior anchor `00251F5F` (a `0028FF20` call).

## SWE2-EC7-46 update (2026-09-19) - `00361080`

`00361080` (233 B) is a body - `002DEC20`/`002DEDE0` pair. Interior anchor `003610FA` (a `002DEC20` call).

## SWE2-EC7-53 update (2026-09-19) - `003EF4A0`

`003EF4A0` (389 B) is a settings command-table body - `002432B0`/`00244960`/`00246AD0`/`00247510`/`00247570`/`00247870`/`00247930`/`001EDEC0` plus `00D11CA8`/`02B5F1C8`. Interior anchor `003EF4E2` (a `002432B0` call).

## SWE2-EC7-54 update (2026-09-19) - `0032C910`

`0032C910` (339 B) is a settings-command body - `00229E70`/`0032D3D0`/`0032D620`/`0032D820`/`0032DB10`/`0032DC00`/`0046DB10`/`0046DB20`/`0046DB40` plus `00D108DC` rdata. Interior anchor `0032C927` (a `0046DB20` call).


## SWE2-EC7-54 update (2026-09-19) - `0032B390`

`0032B390` (313 B) is the settings-command caller the input-stack page names - `0032B9C0`/`0032BCC0`/`0032C180`/`0032C2B0`/`0032C650`/`0032CF50`/`0032D2E0`/`0032DF40` plus `00D108A0`/`01CEBB70`/`01CEBD80`. Interior anchor `0032B39D` (a `0032C650` call).


## SWE2-EC7-54 update (2026-09-19) - `0032B4D0`

`0032B4D0` (290 B) is a settings-command body - `0017E260`/`0032BA70`/`0032BEB0`/`0032DF40`/`003CC130`. Interior anchor `0032B536` (a `003CC130` call).

## SWE2-EC7-55 update (2026-09-19) - `0032D820`

`0032D820` (737 B) is a settings-command body - `0032DC00` angle-wrap calls plus `008F3A2C`/`008F8D80`/`009153EC`/`00915620` rdata. Interior anchor `0032DAB9` (a `0032DC00` call).


## SWE2-EC7-55 update (2026-09-19) - `0032BEB0`

`0032BEB0` (719 B) is a settings-command body - `00230C00`/`0032BB00`/`0032CD20`/`003CC130`/`00808C40`/`00861F14` plus `00D108B4`/`01CEBBA8` rdata. Interior anchor `0032BF0B` (a `0032CD20` call).


## SWE2-EC7-55 update (2026-09-19) - `0032C650`

`0032C650` (692 B) is the input-record lookup the settings table names - `0017E260` single call plus `008C5F70`/`008F30F8`/`008F311C`/`008F6D54`. Interior anchor `0032C88C` (a `0017E260` call).


## SWE2-EC7-55 update (2026-09-19) - `0032D3D0`

`0032D3D0` (581 B) is a settings-command body - `0017E260`/`0017E420`/`001E0CE0`/`001EDE70` plus `008F30F8`/`008F311C`/`008F3A2C`. Interior anchor `0032D405` (a `001E0CE0` call).


## SWE2-EC7-55 update (2026-09-19) - `0032D620`

`0032D620` (505 B) is a settings-command body - `0017E260`/`0017E430`/`001E0D30` plus `008F30F8`/`008F3108`/`008F311C`. Interior anchor `0032D655` (a `001E0D30` call).


## SWE2-EC7-55 update (2026-09-19) - `0032BCC0`

`0032BCC0` (492 B) is a settings-command body - `00230C00`/`00231690`/`00232490`/`0032BB00`/`0032CD20`/`00808C40` plus `00D108B4`/`01CEBBA8`/`01EED3E0`. Interior anchor `0032BD08` (a `0032CD20` call).


## SWE2-EC7-55 update (2026-09-19) - `0032DC00`

`0032DC00` (469 B) is a call-free angle/phase wrap - xmm1/xmm2 wrapped by `0xC90FDB`/`40C90FDB` constants into range, `[rcx+0x36C]` write, `+0xC0` |= `0x200000`, `+0x118`. Interior anchor `0032DC50` (the wrap `addss` loop).


## SWE2-EC7-55 update (2026-09-19) - `0032C180`

`0032C180` (304 B) is a settings-command body - `0017E260` single call plus `008F8D80`/`008FCC8C`/`009146E4`/`00D108A0`. Interior anchor `0032C1B5` (a `0017E260` call).


## SWE2-EC7-55 update (2026-09-19) - `0032C2B0`

`0032C2B0` (290 B) is a settings-command body - `0017E260` single call plus `008F8D80`/`008FCC90`/`009146E4`/`00D108A0`. Interior anchor `0032C2D7` (a `0017E260` call).


## SWE2-EC7-55 update (2026-09-19) - `0032CE40`

`0032CE40` (270 B) is a settings-command body - `00861F02`/`00861F14` plus `008C5F6C`/`01DFE0BC`. Interior anchor `0032CE89` (a `00861F02` call).


## SWE2-EC7-55 update (2026-09-19) - `003F70F0`

`003F70F0` (267 B) is a shared-dialog body - `00181310`/`00181560`/`001816B0`/`00181740`/`00181870`/`00181890`/`00181910`/`00181930`/`00271450`, `009152A0`/`01E0C1E0` and the `"targetline_p"` literal. Interior anchor `003F710C` (a `00271450` call).


## SWE2-EC7-55 update (2026-09-19) - `0032DB10`

`0032DB10` (237 B) is a settings-command body - `00861F08` single call plus `008F6D54`/`008F8D80`/`00D108BC`/`01CEBB70`. Interior anchor `0032DB67` (a `00861F08` call).

## SWE2-EC7-56 update (2026-09-19) - `0032BB00`

`0032BB00` (447 B) is a settings-command body - `00231890`/`002321D0`/`0046DB50`/`00808C40`/`00861F14` plus `008F6D54`/`008FCC90`/`00901988`/`00D108B4`. Interior anchor `0032BB7B` (a `0046DB50` call).


## SWE2-EC7-56 update (2026-09-19) - `00231690`

`00231690` (393 B) is a settings-command body - `0022E340`/`0022F830`/`00233050`/`00808C40` plus `01CEBC08`/`01CEBC9C`/`01CEBD80`/`01F44830`. Interior anchor `002316D2` (a `00233050` call).


## SWE2-EC7-56 update (2026-09-19) - `0032CD20`

`0032CD20` (278 B) is a settings-command body - `003CC2F0`/`00808C40` plus `00D108E8`/`01EED450`-`01EED458`. Interior anchor `0032CD74` (a `003CC2F0` call).


## SWE2-EC7-56 update (2026-09-19) - `0032D2E0`

`0032D2E0` (227 B) is a settings-command body - `00202C70`/`0032C3E0`/`0032CD20`/`00808C40` plus `00D108B0`-`00D108D4`. Interior anchor `0032D318` (a `00202C70` call).

## SWE2-EC7-57 update (2026-09-19) - `0022E340`

`0022E340` (875 B) is a settings-command body - `0022E340` self-recursive call plus `0022F830`/`00231E40`/`00808C40`, `01CEBB70`/`02088FE0`/`020891E0`. Interior anchor `0022E567` (a `00231E40` call).


## SWE2-EC7-57 update (2026-09-19) - `0032C3E0`

`0032C3E0` (509 B) is a settings-command body - `00202B70`/`00808C40` plus `0090030C`/`0091523C`/`01CEBB70`/`01CEBBA8`. Interior anchor `0032C4AC` (a `00202B70` call).


## SWE2-EC7-57 update (2026-09-19) - `0046DB50`

`0046DB50` (503 B) is a settings-command body - `00202B70`/`00202D70`/`00202F00`/`00203170`/`00382020`/`003DAE20`/`00808C40`/`00861F02` plus `01CEBB70`-band rdata. Interior anchor `0046DB7A` (a `003DAE20` call).


## SWE2-EC7-57 update (2026-09-19) - `002321D0`

`002321D0` (427 B) is a settings-command body - `002324F0`/`00233050`/`00808C40` plus `01F44830`/`0209A2D0`. Interior anchor `002321F5` (a `00233050` call).


## SWE2-EC7-57 update (2026-09-19) - `0032DF40`

`0032DF40` (186 B) is a settings-command body - `00861F02`/`00861F14` plus `00D108B0`-`00D108D4`. Interior anchor `0032DFBD` (a `00861F02` call).


## SWE2-EC7-57 update (2026-09-19) - `002715A0`

`002715A0` (176 B) is a settings-command body - `0016D6A0` single call. Interior anchor `0027163C` (a `0016D6A0` call).


## SWE2-EC7-57 update (2026-09-19) - `0032B9C0`

`0032B9C0` (174 B) is a call-free float wrap-and-clamp - `0xC90FDB` wrap loop into range, `[rcx+0x70]` store, `+0xFC`/`+0x100` ratio + `+0x7C`/`+0x108` offsets, min/max into `+0x7C`, `0xA00` gate writes `+0x114`. Interior anchor `0032BA33` (the `divss` ratio).

## SWE2-EC7-58 update (2026-09-19) - `00231E40`

`00231E40` (215 B) is a call-free UV normalizer - `[r11+0x10]`·edx - `[rcx+0x38]` -> `cvtdq2ps` into `[r10]`/`+0x8`, `+0xC`=1.0f, odd-row `+0x14` center-half offset. Interior anchor `00231E69` (the `cvtdq2ps` normalizer).


## SWE2-EC7-58 update (2026-09-19) - `0032CF50`

`0032CF50` (167 B) is a settings-command body - `003D97E0` single call plus `01EED488`. Interior anchor `0032CFB7` (a `003D97E0` call).


## SWE2-EC7-58 update (2026-09-19) - `003F6960`

`003F6960` (167 B) is a settings-command body - `003F5430` single call. Interior anchor `003F69C2` (a `003F5430` call).

## SWE2-EC7-59 update (2026-09-19) - `003F5430`

`003F5430` (1967 B) is a settings-command body - `00181310`/`00181350`/`00181560`/`001816B0`/`00181870`/`00181890`/`00181910` family plus `009152A0`/`01F44830` and the `"targetline_p"` literal. Interior anchor `003F5462` (a `00202C70` call).


## SWE2-EC7-59 update (2026-09-19) - `003D97E0`

`003D97E0` (326 B) is a settings-command body - `00230B60`/`00232160`/`00861F14` plus `008C5F6C`/`01CEBBA8`. Interior anchor `003D9829` (a `00230B60` call).

## SWE2-EC7-60 update (2026-09-19) - `003F5390`

`003F5390` (156 B) is a settings-command body - `002712E0`/`00271360` plus `02064AB0`. Interior anchor `003F53A1` (a `00271360` call).



## SWE2-EC7-63 update (2026-09-19) - `003F35C0`

`003F35C0` (145 B) is a settings-command body - `00202D20`/`00202DE0`/`00203080`/`00808C40` plus `01CEBBA8`/`01EF93F0`/`01EF93F8`/`01F44830`. Interior anchor `003F3614` (a `00203080` call).



## SWE2-EC7-66 update (2026-09-19) - `0032BA70`

`0032BA70` (130 B) is a call-free float wrap - `addss xmm0,xmm2` while `> xmm1`, `+ xmm1` while `< 0` -> `[rcx+0x70]` (`00915624`/`01CEBBA8`/`01CEBC78`). Interior anchor `0032BAA0` (the `addss` wrap loop).


## SWE2-EC7-71 update (2026-09-19) - `002710C0` packet-header writer measured

`002710C0` (58 B) is the draw-list packet-header sibling of `00271080`:
`([+0x10] - [+0x28] - 0x10) >> 4` derives the pending element count, ORs
`(edx << 15)` and constant `0x200000000000` into the qword at `[+0x28]`,
then writes `0xE` at `[+0x28]+8` - the same cursor layout the tag writer
`00271080` and consume `00270FF0` operate on.
Interior anchor `002710E7` (the `or r8, rax` header fold).

## SWE2-EC7-76 update (2026-09-19) - `00271010` + `00254DD0` settings helpers measured

`00271010` (56 B) is the aligned-advance: when `[rcx+0x10]` differs
from `[rcx+8]`, `[rcx][+8]` advances by `diff & ~0xF`; `edx` nonzero
adds `0016D6A0(0)`; `003A1DB0` tails either way - the
consume-16-and-notify the settings bodies share.
Interior anchor `0027102B` (the aligned add).

`00254DD0` (42 B) is the `020927C0` bitmap test: byte `(cx >> 3) +
0x32C4` bits `1 << (cx & 7)` - the flag read.
Interior anchor `00254DEE` (the indexed `test`).

## SWE2-EC7-88 update (2026-09-20) - `003C58B0` flag-reset forward measured

`003C58B0` (87 B) is the flag pass the settings callers run:
`dword[02B45A00] &= ~6`; when `[02B476B0]` is live its `+0x40`
loses `0x10000`, `002544B0()` runs, and `eax == 1` or a nonzero
`[02B476E4]` re-arms `0x10000` and clears `02B476E4`; the body
then tails `00244F00(record)`.
Interior anchor `003C58FC` (the `00244F00` tail).

## SWE2-EC7-92 update (2026-09-20) - `00392F30` six-arm dispatch measured

`00392F30` (87 B) is the settings-command dispatch `00392FC0` calls:
`ecx <= 5` indexes the `014102F8` offset table, arms set `ecx` to
0, 2, 3, 4, 5, 6 respectively and tail `002DD7E0`; `ecx > 5` returns 0
without dispatching.
Interior anchor `00392F49` (the `jmp rcx` dispatch).

## SWE2-EC7-94 update (2026-09-20) - `0032E020` + `0032E030` measured

`0032E020` (33 B) and `0032E030` (33 B) are the twin range-gated
trampolines `001D1660` and `002407F0` call: both take a 1-based
command id, admit `id-1 <= 5`, and tail `0017E760` / `0017E780`
respectively - adjacent arms of the same six-entry dispatch the
settings table splits across the pair.
Interior anchors `0032E026` and `0032E036` (the two conditional
`jbe` entries).

## SWE2-EC7-98 update (2026-09-20) - `002DECE0` + `002DDE20` measured

`002DECE0` (69 B) is the persisted setter `00342F80`,
`0035CA70`, `003EFAA0` and `0050E8E0` call: `ecx < 0` reloads
`dword[0215EF44]` (the last value), a resolved non-negative
value arms `byte[0215EF4D] = 0x7F` and runs
`001DBC70(ecx, 0x7F)`, `001DBC10` always gets the original
`ecx`, `001DBBD0` runs only when it was non-negative, and
the original is stored back to `0215EF44` - the
clamped-at-0x7F setter with memory the settings table
drives.
Interior anchor `002DED02` (the `001DBC70` call).

`002DDE20` (23 B) is the bit-10 probe `002403F0`, `002DEBB0`,
`002DF460` and `002DF4D0` call: a null `[0215E6E0]` object
yields 0, else `eax = (dword[obj+4] >> 0xA) & 1` - the
single-flag read the settings arms share.
Interior anchor `002DDE2C` (the `dword[+4]` load).

## SWE2-EC7-99 update (2026-09-20) - `002DDD70` measured

`002DDD70` (35 B) is the two-source boolean `002403F0` and
`002A2C00` call: a nonzero `word[0215E6DC]` yields its bit 0
(`cwde` + `and 1`); otherwise the same `0215E6E0` object
`002DDE20` probes supplies `~(dword[obj+0] >> 0xC) & 1` -
the negated bit 12 of the object's first dword standing in
when the word gate is clear.
Interior anchor `002DDD8A` (the `shr eax, 0xC`).

## SWE2-EC7-103 update (2026-09-20) - `0027DED0` + `002713B0` + `00271360` measured

`0027DED0` (379 B) is the `+0x1510`-widget extent
composer `002778C0` and `0027E050` call: `[+0xD8]`
takes the owner, `0027BDE0` resolves `r14d` into a
stack word, `edi`/`esi` clamp to `>= 1`, and when
`r14d - 0xA <= 4` with `dword[+0x50C] == 4` the
height gains `01E0C364 - 01E0C354`; `byte[+0x1528]`
and `word[+0xEA]` publish, `002D48C0` and
`002D4930` run, the `[+0xC0]` node's
`+0x98`/`+0x9A`/`+0x9C`/`+0x9E` words take the
`01E0C360`/`0209ABFC + bp`-adjusted extents, and
`r14d == 0x11` or `+0x1528` bit 15 forces
`+0x9E = 01E0C374` before `00247870` - returning
`edi`, the line-count the settings rows compute.
Interior anchor `0027DF67` (the `002D48C0`
call).

`002713B0` (41 B) is the four-entry map
`002911D0`, `003F2CF0` and `003F5430` call:
`ecx = 1` returns 1, `2` returns 5, `3` returns 0,
`4` returns 3, anything else 0 - the small
index-to-code translate the command arms share.
Interior anchor `002713CD` (the `eax = 5`
arm).

`00271360` (23 B) is the three-word slice copy
`003F5390`, `003F5430`, `003F67C0` and `003F6B30`
call: `[rcx] = [rdx]`, `[rcx + 8] = [rdx + 0x10]`,
`[rcx + 0x10] = [rdx + 0x10] + 0x10` - the
{head, base, end} record pack the settings walks
publish.
Interior anchor `00271366` (the `+0x10`
load).

## SWE2-EC7-104 update (2026-09-20) - `002712E0` + `002703F0` measured

`002712E0` (116 B) is the packed-record close
the settings-table arms `003F5390`, `003F5430`,
`003F67C0` and `003F6B30` run: it saves
`[rdx + 8]` (the record head), and when
`r8d == 1` first emits a `0x8000` / `0xE`
qword pair into the `[rdx + 0x10]` cursor and
advances it by `0x10`. It then computes the
entry count `(cursor - head - 0x10) >> 4`, ORs
`0x50000000` into the tag, stores it at
`[head + 0xC]`, clears `[head + 8]`, calls
`0016D6A0(&head)`, and publishes the cursor to
`[rbx + 0x10]` - the `0x50000000`-tagged list
seal the command arms share.
Interior anchor `002712F8` (the `0x8000` record
write).

`002703F0` (35 B) is the squared-length reader
`003F5100`, `003F7200` and the other table arms
call: `x*x + y*y + z*z` over the float3 at
`rcx`, returned in `xmm0` - the
no-square-root magnitude test used where only
a comparison is needed.
Interior anchor `002703FE` (the first
`mulss`).

## SWE2-EC7-106 update (2026-09-20) - `0024E410` measured

`0024E410` (73 B) is the
context-gated range probe
`00434CD0`, `00435050` and
`004355D0` call: `00862C40` fills a
stack pair, and only when
`dword[rsp + 0x30] == 0`, the
`02F97340` pointer is live, and its
`byte[rcx] == 7` does the answer
become `word[rcx + 4] - 0x200 <=
0x3F` - the tagged-record window
test the settings arms share.
Interior anchor `0024E437` (the
`byte[rcx]` tag compare).

## SWE2-EC7-108 update (2026-09-20) - `0022F830` + `00232490` + `00230C00` measured

`0022F830` (120 B) is the
bit-walk dispatcher `0022E340`,
`00230C10`, `00231400`, `00231690`
and `00232490` drive: bits 0..3 of
`byte[rdi + 0x16]` each arm one
invoke - the index lands at
`(word[[+8] + 0x40] + 1) * bit +
word[+0x10]` inside the `[+8]`
record's `[+0x20]` word table,
`word[+0x12]` gets the start entry,
`word[+0x14]` the next-minus-start
length, then `call [rdi]` runs the
descriptor's own callback - the
four-channel command walk the
settings arms share.
Interior anchor `0022F894` (the
`call [rdi]` invoke).

`00232490` (90 B) is the
descriptor-post wrapper `0026E3C0`,
`0032BCC0` and `0032CA70` call: it
builds the descriptor
`{0022F8B0, rcx, ...}` -
`00233050()` fills `word[+0x10]`,
`byte[+0x16] = 6` arms bits 1-2,
`rdx` and `r8d` land at
`+0x18`/`+0x24` - runs
`0022F830(&desc)` and returns the
`dword[+0x20]` out field the
callback writes.
Interior anchor `002324D6` (the
`0022F830` call).

`00230C00` (15 B) is the
stack-arg forward thunk
`0032BCC0`, `0032BEB0` and
`0032CA70` call: it re-stages
`word[rsp + 0x28]` and tails
`00230C10` - the 5th-argument
handoff into the same family.
Interior anchor `00230C0A` (the
`jmp 00230C10`).

## SWE2-EC7-115 update (2026-09-21) - `0079AEE0` / `0079AE40` measured

`0079AEE0` (60 B) is the
test-and-clear `001E0920`
and `001E0C50` run: when
`qword[+0x150]` is live and
`edx - 1` is under 3, the
byte at `[+0x150] + edx +
0x1E0` answers whether it
was nonzero and is cleared
- a one-shot flag consume
on the three-slot `+0x1E0`
bank.
Interior anchor `0079AEF3`
(the `+0x1E0` byte test).

`0079AE40` (78 B) is the
same consume on the
`+0xDF8` object's `+0x118`
bank: `r8 < 7` selects the
bank, `edx - 0x1C < 0x100`
selects the row, and
`byte[bank + row + 0x30]`
answers set-then-cleared -
the read half of the
`+0x30` bytes `007A0B50`
refreshes from `+0x130` and
`0079A120`'s INPUT command
writes.
Interior anchor `0079AE68`
(the `+0x30` byte test).

`00230C10` (2018 B) is the settings body `00230C00` wraps: `[r9]`'s 16-byte record copies into `[rdx]`, float deltas form against `[r8]`, and the `0022F430` x2/`00233050`/`0022F830` x2 command calls interleave with `00861F14` x4, `00202E10` x2, `00380190`, `00380650` and `00202B90` - the command table's vector-parameter arm.

Interior anchor `00230D45` (function `00230C10`).

`003F1A60` (1065 B) is the presentation body `003F0170` runs: `byte[rcx+0xEA] & 1` gates the arm, `02AED5F0` stages through `00203080`/`003CBFA0`/`00202D20`/`002703F0`/`003590D0`/`002E9D10`, and the `00271100`/`00271080`/`00271010`/`00271450`/`002714A0`/`002714E0`/`002714C0`/`002710C0`/`00271290` battery with `003F0610` and `00181310` drives the item emission - the settings-table presentation's gated worker.

Interior anchor `003F1AAE` (function `003F1A60`).

`003F9390` (902 B) is the presentation body `003F9720` calls: a full xmm spill frame, then `003F00F0`, `003F1230`, `00270260`, `00203080`, `00270550`, `00861F0E` and `00202C90` run the emit passes under the cookie check - the `003Fxxxx` presentation family's vectorized worker.

Interior anchor `003F953E` (function `003F9390`).

`003F8FE0` (641 B) is the transform-compose stage the settings arm `003F9720` calls (a sibling of `003F9390`): xmm-spill frame under the cookie, three `00202C90` copies seed the stack vectors, `00270590`/`00203080` x4/`00270550` x2/`00202DE0` x2/`00202D20` compose the matrices, `00270260`/`002703F0`/`00808C40` finish - the `003Fxxxx` presentation family's compose step.

Interior anchor `003F9021` (function `003F8FE0`).

`00270590` (389 B) is the per-element compose `003F8FE0` and `003F9720` call under the cookie frame: `00203080` builds stack vectors from `rdx`/`r8`/`r9`, `00202E10` composes and the negated dot lands in `[rbp-0x44]`, `00202B10` then `00203080`/`00202C90`/`00202DE0`/`002708E0`/`00808C40` finish the pair - the settings family's matrix-compose helper.

Interior anchor `002705E5` (function `00270590`).

`0023EFC0` (449 B) is the three-table dispatch `0023FBE0` calls: `byte[rcx+0xC2]` picks `01E0BF60`/`01E0BF68`/`01E0BF70`, `[rcx+0x60] -> [rcx] -> +0x18` resolves `rbx`, `byte[rax+2]` gives the selector, and `002D48C0`/`002445C0`/`002526F0`/`002D45C0`/`002D46F0` run the arm - the settings command's per-kind table.

Interior anchor `0023F020` (function `0023EFC0`).

`003F6690` (291 B) is the six-entry table emit `003F5430` runs: the header writes `0x10000000` x3, `0x6C138000`, `0x3000000000008006` and `0x412` before six iterations copy `01EFF3E0`-based vec4 triples at 0x30 stride through `00202C90` x3 (an optional `dword[r15]` lands at `+0x1C` per row), then the `+0x140` trailer takes `0x13000000`/`0x17000000`/`0x10000000` x2 and returns `+0x150` - the settings command's fixed-block publish.

Interior anchor `003F6718` (function `003F6690`).

`003F6850` (261 B) is the scaled-plate draw `003F5430` runs per settings row: `xmm6 = (1.0f - [rdx+0x824]) x 0.5f + 0.5f` computes the fade-derived scale, `00203170`/`00202D70`/`00202C90` build the transform stack (scale vec into `+0x20`, the `rbp+0x20` matrix through `rsp+0x90` with `w = 1.0f`), `003F67C0` runs on `rsi`, `00271760` draws from `[rbp+0x30]` through the staged matrix, `002715A0` issues with `rdx = [rbp+0x7E8]` and `r9d = edi`, and `[rbp+0x10C]` doubles on exit - the highlight/fade plate the settings screen renders per entry.

Interior anchor `003F68A7` (function `003F6850`).

`003F0610` (3084 B) is the chain/target-line plate builder behind the settings command table's emitter: it constructs a four-column transform for the plate - either the uniform-scale arm that divides each basis column by the reciprocal of the weighted extent sum (`[rdi+0x50..0x6C]` products through `0024ABC0`/`0024ABA0` divides) or the general arm that combines the per-axis products against the constant basis table `02B5F1D0..02B5F1EC` - normalizes every column with `00202FE0`, folds in the `[rdi+0x70]/[+0x74]` offset pair divided by the same aspect helpers, copies the record's two 16-byte integer blocks forward, then dispatches on `[rsi+0xF0]`: -1 lays out `chain_item` at the scaled extent, -2 sizes `targetline_p` from the `ebx`x`r14d` pair, -3 fixes `chainflash` at 0x400x0x200, and the default arm emits the target line through `002DD8B0`/`00181390`/`001813F0`, halving the `+0xEC` offset when the `[rsi+0xE0]+0x38` mask test `& 0x3F00 == 0x1300` fails.

Interior anchor `003F0C48` (function `003F0610`).

`0035D1B0` (208 B) is the enable-toggle `00251F40` issues: after `00408AA0`/`004052D0` guards, `ecx & 0x80` selects `0035E5A0` or `0035E5C0` on the `0208EA28` object, `00246AC0` notifies on success and `0035D2D0` sweeps `[+0x18]` list nodes; on the set path `[+0x44] & 0x180000 == 0x180000` triggers a second `00246AC0` and a `0035E580` list pass - the settings write that propagates to live objects

Interior anchor `0035D1C1` (function `0035D1B0`).

`0035D0E0` (205 B) is the conditional sweep `00251F40` issues after `004082D0`/`00405150`: `ecx & 0x80` selects `0035E5C0` over `0035E5A0` on the `0208EA28` object, `002A2720` runs on success, then `0035D280` walks the `[+0x18]` list with the selected hook; on the set path `[+0x44] & 0x180000 == 0x180000` earns a second `002A2720` plus a `0035E580` pass, and the body tail-jumps `002E2010(6)` - the sibling shape of `0035D1B0` one settings row over

Interior anchor `0035D102` (function `0035D0E0`).

`0035E5C0` (45 B) is the strict predicate `0035D0E0` and `0035D1B0` share: record null or `([rcx+0x44] & 0x180000) != 0x100000` returns 0, and a set `0x100000` bit in `[rcx+0x40]` also fails it - only a record of that kind with the flag clear passes

Interior anchor `0035E5CF` (function `0035E5C0`).

`0035E5A0` (26 B) is the weaker sibling predicate the same two sweepers call: null-safe, returns exactly `([rcx+0x44] & 0x180000) == 0x100000` - the kind test without the `+0x40` flag check `0035E5C0` adds

Interior anchor `0035E5AA` (function `0035E5A0`).

`002E2010` (57 B) is the bounded enable setter `0035D0E0`/`0035D1B0` invoke: `ecx` is clamped to [0,7], indexes the 8-slot 0x68-stride table at `0215F200`, and when the row pointer is live rewrites bit 0 of `[row+0x40]` from `edx & 1` (clear then set)

Interior anchor `002E202A` (function `002E2010`).

`003F6200` (196 B) is the vec3 compose `003F5430` calls per emit row: `00203080` unpacks `[rdx+0x10]` and `r8` into two stack vectors, `00202E10` combines them, `00202DE0` and `00202FE0` normalise/scale the result by `xmm3` (with `1.0f` in `rsp+0x2C`), and `00202B10` delivers it back against `rsi` - one arm of the paired transform

Interior anchor `003F6255` (function `003F6200`).

`003F6130` (196 B) is the twin arm of the same compose: identical unpack-combine-normalise pipeline and `rsp` layout, differing only in the final call - `00203080` instead of `00202B10` - the second write path `003F5430` selects between

Interior anchor `003F6185` (function `003F6130`).

`0027BDE0` (167 B) is the code-to-pair map `0027DED0` runs: `ecx - 2` in `0`..`0x11` selects `edx` `0xE` down to `1` through the `0027BE88` jump table (out-of-range gets `edx = 0`), `0035C3F0(&local, edx)` fills a 4-byte scratch, and its two words land at `[rdx]`/`[rdx+2]`

Interior anchor `0027BE70` (function `0027BDE0`).

`003F67C0` (140 B) is the command-record builder this page's setter family uses: a fixed field block carrying `0x53001`, `0x47`, `0x1A` and `0x5D` is assembled, then `00271360` and `002712E0` stage and post it - the construction half of the settings command path the config screen invokes.

Interior anchor `003F67FD` (function `003F67C0`).

## Falsification pass 1 — 2026-09-29 (OPUS): the defaults (CON-193) and command 11's getter (CON-194) corrected; the dispatch and table survive

**Attack.** The dispatch, the selector tables, a sample of setters, the defaults installer and command 11's split storage
were turned into checks at their instructions, independently of the page's own regenerator. Script:
`Tools/analysis-kit/gfz-scripts/falsify_settings_commands.py`, output `falsify_settings_commands.out`, image `73461d08…`,
0 BROKEN after the corrections, exit 0.

| # | Clause attacked | Result |
|---|---|---|
| C0 | section 1: the selector tables | **survives**: identical, with the page's bytes |
| C1 | sections 1 and 3: the dispatch | **survives**. All 19 SET and GET arms go to the page's setters and getters, including the second calls of commands 8 and 14. The 16 unhandled ids call nothing |
| C2 | section 3: setters for 4, 5, 11, 14, 17, 19 and 29 | **survives** |
| C3 | section 2: the defaults | **REFUTED (CON-193).** The template's second dword is `0x00620400` (bytes `00 04 62 00`), bits 10, 17, 21 and 22, not `0x62000400`. Dword0 bit 12 is set for language ids **1 and 6**, not 6 alone. The installer also clears the speed-mode field, sets the soundtrack word to 1 and all three volumes to 100 |
| C4 | sections 3 and 5: command 11's getter | **REFUTED in part (CON-194).** `002DDD70` returns the live word `0215E6DC`'s bit 0 only when that word is non-zero. When it is zero, it returns the inverse of `opt+0` bit 12, the setter's own storage. So setter and getter do not always touch different storage |

**In player terms.** A new save starts with:
- Battle Mode Wait, Battle Speed 3;
- the Reorchestrated soundtrack;
- all three volumes at 100;
- the ×2 speed multiplier;
- subtitles on for language ids 1 and 6;
- the Japanese-voice bit ~~clear~~ set for ids 0, 7, 8, 10 and 11 *(corrected 2026-10-02, OPUS: `002DDF24`–`002DDF6E`, `ebx = 0x400` for those ids, `or` into dword1)*.

## Interior citations for the entry-cited functions (OPUS, 2026-10-01)

*Functions this page named only at their entry. Each was read from the certified image; the sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Verified by [`settings_interior.py`](../../_index/candidates/opus-settings-interior-1001/settings_interior.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00181390` | 96 B | forwards its six arguments to `001B0A20`, with `001B1C00()` inserted as the first | `001813AF`, `001813D6` |
| `00198960` | 109 B | swaps the two dwords of each pair `01DF176C`/`01DF1770`, `01DF18C8`/`01DF18CC` and `01DF1A24`/`01DF1A28`, and also writes each swapped pair to `01F80164`/`01F80168`, `01F802C0`/`01F802C4` and `01F8041C`/`01F80420` | `0019896C`, `00198972`, `00198978`, `00198990`, `001989B4` |
| `001DC190` | 76 B | forwards its four arguments to `00211200`, with `00210B30()` inserted as the first | `001DC1AE`, `001DC1C2` |
| `001DC1E0` | 84 B | forwards its five arguments to `00211210`, with `00210B30()` inserted as the first | `001DC1FE`, `001DC21A` |
| `001E0920` | 82 B | on the object at qword `+0xDF8` of the framework-singleton getter, calls `0079AEE0(it, i)` for i = 1 to 3; then calls `0079AE40(g, i, 0)` (g = what the framework-singleton getter returns) for i = `0x1C` to `0x98` | `001E093E`, `001E0945`, `001E095D`, `001E0964` |
| `001E0AA0` | 90 B | when `00198790()` is non-null, tail-calls `00197710(it, dl, byte 2 of 001E0650(), byte 0 of 001E0650())` | `001E0AAC`, `001E0AC4`, `001E0AEA` |
| `001E0CE0` | 67 B | returns dword `+0x184` of the object at qword `+0xDF8` of the framework-singleton getter, negated when `00198790()` is non-null and `001976E0` on it returns non-zero | `001E0CFA`, `001E0D0E`, `001E0D1A` |
| `001E0D30` | 67 B | returns dword `+0x188` of the object at qword `+0xDF8` of the framework-singleton getter, negated when `00198790()` is non-null and `001976F0` on it returns non-zero | `001E0D4A`, `001E0D5E`, `001E0D6A` |
| `00231400` | 474 B | returns 0 or 1. After `00233050` and `00233110(rcx, stack block, 00233050(), rdx)`, the word at stack `+0xA2` indexes a 32-byte record of `[rcx+0x10]` (a negative word returns 0); when the record's float `+4` exceeds 0.001 (`008C5B2C`) it takes the height of the record's plane (floats `+0`/`+4`/`+8` through the point at `[rcx+8] + 16*word +0x10`) at the x and z of the point `rdx`; with `r9d` 0 that height replaces the y of a stack copy of the point, otherwise a height above the y returns 0. It then turns x and z plus the integers `+0x38`/`+0x3C` into a cell of the grid at `[rcx]` (cell sizes `+0x10`/`+0x14`, odd columns shifted by half a cell, bounds `+8`/`+0xC`, -1 outside) and calls `0022F830` on a stack query {callback `0022F8B0`, `rcx`, that cell, byte 6, the point}; it returns 1 when the query's dword `+0x20` stays 0 | `00231482`, `002314AA`, `00231548`, `002315A9`, `002315B2` |
| `00232160` | 99 B | for a word `r8w` below `0x5000`: from `0x4000` up, tail-calls `00381D90([rcx+0x18] + 0x90*(r8w-0x4000), rdx, r9)`; below `0x4000`, copies the first 16 bytes of the 32-byte record `[rcx+0x10] + 32*r8w` to `rdx`; from `0x5000` up it does nothing | `0023216B`, `0023218B`, `00232193`, `002321A0`, `002321BE` |
| `0023B2E0` | 78 B | when `00229E20()` is non-zero: when `002DDDA0()` is 0, calls `00229ED0(1)` and tail-calls `00182FB0(1)`; when it is 1, calls `00229ED0(2)` and tail-calls `00182FB0(2)`; any other value does nothing | `0023B2E4`, `0023B2ED`, `0023B2FE`, `0023B30C`, `0023B324` |
| `0023E710` | 82 B | calls `00244F50(0xF0, 0023E770, record)` with a stack record {dword 0, qword `ecx`, qword `dl`} | `0023E72F`, `0023E737`, `0023E743`, `0023E74B` |
| `00290030` | 33 B | stores `xmm0` at float `+0x1D7C` of the object at qword `+0x10F80` of `[0209BE80]`, when both are non-null | `00290037`, `0029003C`, `00290048` |
| `00290060` | 85 B | with `[0209BE80]` and its qword `+0x10F80` non-null: calls `002C63D0` on that object, and when `002544B0()` returns 1 sets word `+0x1D78` of that object to `0x80` and bit 2 of its word `+0x1D7A` | `0029007E`, `00290083`, `00290099`, `002900A7` |
| `00290190` | 21 B | tail-calls `0016D6A0([0209BE80] + 0x8FA0, ecx)` | `00290192`, `00290199`, `002901A0` |
| `00290280` | 74 B | with qword `+0x10F80` of `[0209BE80]` non-null, sets bit 1 (when `ecx` is non-zero) or bit 0 (otherwise) of that object's word `+0x1D7A` to bit 0 of `dx` | `00290293`, `002902A3`, `002902AB`, `002902B9` |
| `00290C00` | 66 B | with `[0209BE80]` non-null: calls `003F5070` on its qword `+0x10F10` when that is non-null, then tail-calls `003F7490` on its qword `+0x10F30` when that is non-null | `00290C1C`, `00290C28`, `00290C38` |
| `002911D0` | 324 B | looks up `edx` in the list at qword `+0x10F40` (`003F3580`); a found node gets float `+0x64` = `xmm2` and dword `+0x48` = `002713B0(r9d)`. Otherwise it allocates a `0x80`-byte node (`00273A30(0, [[0209BE80]+0x10FC0], 0x80)`), loads qword `+0x10F50` once through `0024A5A0([01E0C1E0])`, fills a stack record from an entry of the table at `[[+0x10F50]+0x20] + 0x30` (word +0 plus 2, word +2, dword +4 minus 4 in the low 12 bits and unchanged in bits 12-23), initialises the node with `003F3510` and stores `003F34D0(list, node)` back in `+0x10F40`; returns the node | `00291204`, `00291211`, `00291234`, `002912AF`, `002912F0` |
| `002DE080` | 36 B | sets bit 13 of the dword at `[0215E6E0]` to bit 0 of `ecx`, then tail-calls `0035FF30(0, that bit)` | `002DE08A`, `002DE08D`, `002DE093`, `002DE09F` |
| `002DE160` | 37 B | sets bit 9 of dword `+4` of `[0215E6E0]` to bit 0 of `ecx`, then tail-calls `001E0FF0(that bit)` | `002DE16A`, `002DE16D`, `002DE174`, `002DE180` |
| `002DE190` | 37 B | sets bit 8 of dword `+4` of `[0215E6E0]` to bit 0 of `ecx`, then tail-calls `001E1020(that bit)` | `002DE19A`, `002DE19D`, `002DE1A4`, `002DE1B0` |
| `002DF4D0` | 85 B | calls `001DC1E0(ecx, edx, r8d, r9d, 1 when 002DDE20() is 0 else 0)` | `002DF4EE`, `002DF502`, `002DF50B` |
| `0032CA70` | 538 B | calls `003CC130(rcx + 0x350, rcx + 0x60, ...)` with three output floats and returns 0 when the one written through `r9` is above 1.3962634 (`00D108C4`). Otherwise it calls `003CC480(0, the one written through r8 plus 0.25 01CEBB68, 0)` into a stack vector, applies `00202B70` to the stack vector (0, 0, 3.0 `008F311C`, 1.0 `01CEBBA8`) and that result and stores it as the 16 bytes at `+0x300`; runs `00232490` and `00231690` (with `0x13` and `01EED410`) on qword `+0x2C8`, then `00230C00` with 4 (when `00232490` returned 0 and `00231690`'s float is not strictly between 0 and 0.27 `00D108B4`) or -1 and the float 0.27, copying its 16-byte result to `+0x300` when it returns non-zero; finally copies the 16 bytes at `+0x350` to `+0x310` and returns 1 | `0032CAAD`, `0032CAB7`, `0032CB5F`, `0032CBB4`, `0032CC10` |
| `00342F80` | 132 B | when `00267310(byte +0x15 of rdx)` is non-zero, tail-calls `00360960` with word `[r8]`, dword `[r8+0xC]` and the signed low nibble of byte `[r8+2]`; otherwise, when `00360C20()` is 5 and `002DEC00()` differs from word `[r8]`, tail-calls `002DED70` (the nibble non-zero, or dword `+0xC` positive with the word `0x5A` or `0x5B`), `002DECE0` (the nibble 0 and dword `+0xC` not positive) or `002DEC80` (the rest) | `00342F8D`, `00342F9E`, `00342FAB`, `00342FC6`, `00342FF9` |
| `0035D280` | 79 B | calls the function `rdx` on the node `rcx`, and `002A2720` on the node when that returns non-zero; then recurses over the children from qword `+0x18`, each call returning the next sibling; returns qword `+0x20` | `0035D290`, `0035D299`, `0035D2B6`, `0035D2C0` |
| `0035D2D0` | 79 B | calls the function `rdx` on the node `rcx`, and `00246AC0` on the node when that returns non-zero; then recurses over the children from qword `+0x18`, each call returning the next sibling; returns qword `+0x20` | `0035D2E0`, `0035D2E9`, `0035D306`, `0035D310` |
| `0035E580` | 26 B | returns 1 when `rcx` is non-null and bits 19 and 20 of its dword `+0x44` are both set, else 0 | `0035E587`, `0035E58A`, `0035E596` |
| `0035FF30` | 41 B | for `ecx` below 2, sets bit 2 of byte `+9` of the `0x294`-byte record `022CAE90 + 0x294*ecx` to `edx != 0` | `0035FF38`, `0035FF3F`, `0035FF49`, `0035FF55` |
| `00382020` | 94 B | returns 1 when the float at `+4` lies strictly between -1.0 (`01CEBC9C`) and 1.0 (`01CEBBA8`) and `00861F14(x*x + z*z)` of the floats at `+0` and `+8` is below 1.0, else 0 | `00382036`, `0038203B`, `00382059`, `0038205E` |
| `003EF290` | 79 B | calls `002DEE50(002DEC00(), edx, 0)`; then, with `2*edx`, calls `003611F0(it, 1)` and `003634B0(it, 0)` and stores it in dword `+0xC8`; stores 6 in byte `+0xC0` | `003EF2AB`, `003EF2B0`, `003EF2B9`, `003EF2C7`, `003EF2D2` |
| `003F6B30` | 124 B | fills a stack block with `00271360(block, rcx)`, writes six qwords (`0x1000000000000002`, `0xE`, `0x53001`, `0x47`, `0x44`, `0x42`) at the block's write pointer (qword `+0x10`) and advances it by `0x30` (the 16 bytes first copied there from `02064AB0` are overwritten), then calls `002712E0(rcx, block, 1)` | `003F6B41`, `003F6B6A`, `003F6B98`, `003F6BA1` |
| `00405150` | 82 B | with `[02B62D88]` and its qword `+0xC0` non-null: calls `00244DD0` on the latter when bit 20 of its dword `+0x40` is clear, and in either case sets bit 2 of dword `+0xC8` of `[02B62D88]`; when `+0xC0` is null, sets that bit only when bit 0 of `+0xC8` is set | `0040516C`, `00405175`, `00405181`, `0040518D` |
| `004052D0` | 61 B | with `[02B62D88]` and its qword `+0xC0` non-null and bit 2 of its dword `+0xC8` set, calls `00246AD0([02B62D88], [+0xC0])` and clears that bit | `004052EC`, `004052F5`, `00405301` |
| `004082D0` | 38 B | with `[02B62D80]` and its qword `+0xC0` non-null, tail-jumps to `00244DD0` on the latter when bit 20 of its dword `+0x40` is clear | `004082DC`, `004082E8`, `004082EF` |
| `00408AA0` | 43 B | with `[02B62D80]` and its qword `+0xC0` non-null, tail-jumps to `00246AD0` when the latter's dword `+0xD8` has bit 2 set and bit 3 clear | `00408AB8`, `00408ABE`, `00408AC2`, `00408AC4` |
| `0046DB10` | 12 B | tail-calls `0035EEB0(0, ecx, 0)` | `0046DB12`, `0046DB15`, `0046DB17` |
