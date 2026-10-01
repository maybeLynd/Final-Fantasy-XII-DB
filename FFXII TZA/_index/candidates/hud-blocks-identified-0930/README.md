# `_types`: five battle-HUD blocks identified, and GR-3 answered (SWE2-ORACLE for OPUS, 2026-09-30)

The battle HUD singleton `ManagerSingleton0209BE80` (pointer slot `0209BE80`, constructor `00291750`) embeds five blocks
whose type rows said only what code touches them. This record says what each one is. The same was done for
`_7FB0` and `_8FA0` in [the OPUS record](../opus-types-hud-panes-0930/README.md). GR-3, the combo popup, turned out to be
the same code as `_5380`, so it is answered here too.

The method: a block is identified by a layout key, a string or text id, or a named requester. How the block works is
not enough on its own. Everything is static, from the certified image. The text ids were resolved from the shipped
files by the size-match method of GE-1.

The checker is `hud_blocks_check.py` (output `hud_blocks_check.out`, **`FAILS 0`**, about a minute).

## Answers

| block | identification | basis | proposed confidence |
|---|---|---|---|
| `ManagerSub0209BE80_5380` (0x460) | **the battle number popups**. Pool A holds the EXP / LP gain numbers, pool B the combo count, and pool C is not identified | layout keys, named requesters | PROVEN for A and B |
| `ManagerSub0209BE80_57E0` (0x26C0) | **the enemy chain counter** | named requesters (every writer of its request word) | PROVEN |
| `ManagerSub0209BE80_A0D0` (0x990) | **the key-signal strip (a button legend)** | text ids: `key_signal.bin` labels and `menu_command_template.bin` button templates; named requesters | PROVEN for identity, open for reachability (K7) |
| `ManagerSub0209BE80_7EA0` (0x110) | **the 2D side cursor**: two cross-fading lanes that follow an actor | layout keys `m2DSideCursorCenterX/Y`; requester in the target-info pane | PROVEN |
| `ManagerSub0209BE80_00A0` (0x52E0) | **the area-name markers** around the focus character: up to 64 `partytop_8_c` sprites plus area-name labels | strings: texture `partytop_8_c`, `MapName_GetAreaNameById`, `"???"` | PROVEN for what it draws; which map records it draws from is not read |
| `ManagerSub00A0Entry` (64 × 0x100) | one sprite quad of the area-name markers | its initialiser `003F9390` and the `partytop_8_c` handle | PROVEN |
| `ManagerSub7EA0Entry` (2 × 0x20) | one lane of the side cursor | the arming code `0028CA40` | PROVEN |

### `_5380`: the battle number popups

**In player terms:** these are the numbers that pop up over characters in battle: the EXP and LP gained from a kill,
and the hit count of a multi-hit Attack.

- **A1–A2.** Gate group `0x0001` runs `00289970(hud + 0x5380)`, one tick pass per list:
  - `0028A550` on `+0x420`;
  - `0028A350` on `+0x428`;
  - `0028A620` on `+0x430`.

  The draw pass `00289A10` is called only from `0028EE10`, with `rcx = hud + 0x5380`. It draws:
  - `+0x420` with `0028B140`, twice per entry;
  - `+0x428` with `0028AAA0`;
  - `+0x430` with `0028A790`.
- **A3.** The layout-key reader table binds these keys:
  - `0028B140` reads `ExpNumOffsetX`, `LpNumOffsetX`, `ExpLpPositionOffsetX/Y`, `EXPLPNumOffsetX/Y`,
    `NumEffectLPOffsetY` and `mExpEffectOffsetY`;
  - `0028AAA0` reads `mNumEffectOffsetX1/X2` and `NumEffectOffsetY1/Y2`;
  - `0028A790` reads no key.
- **A4.** Pool A has one producer, `00312280` (`BattleUnit_ProcessDefeatRewardsAndLoot`). It calls `0028FB80`
  (`Reward_PublishExpLpPresentation`), which calls `00289D00` twice, flag 0 then 1: one EXP entry and one LP entry.
- **A5.** Pool B's producer is `00307300` (`Battle_ProcessActionTarget`), at `00307676`. It runs on action `0x96`, when
  the tally `+0x6B8` grows, and reaches `0028E920`, then `00289D70`. Pool C's producer is `0030AF30`, reaching
  `00290540`, then `00289F50`.
- **GR-3 confirmation.** OPUS asked whether GR-3's `+0x428` object is `_5380`. It is: `0028E920` does
  `add rcx, 0x5380` on `[0209BE80]`. GR-3's list is `_5380`'s `ptr0428`, and its six 40-byte slots are
  `ManagerSub5380PoolBEntry` (flag `+0x16`, base `+0x240`).

**Readiness text:** *SEMANTICALLY IDENTIFIED / PROVEN - the battle number-popup layer: pool A (`+0x000`, list `+0x420`)
the EXP / LP gain numbers (keys `ExpNum…`/`LpNum…`/`ExpLp…`, producer `00312280` via `0028FB80`), pool B (`+0x240`, list
`+0x428`) the combo count (keys `NumEffectOffset…`, producer `00307300` via `0028E920`), pool C (`+0x330`, list `+0x430`)
unidentified (producer `0030AF30` via `00290540`, drawn keyless by `0028A790`).*

### `_57E0`: the enemy chain counter

**In player terms:** this is the Chain counter that appears when you keep defeating the same kind of enemy. The
number's colour changes with the chain level, a level-up plays an effect, and the counter disappears when the chain
breaks.

- **C1.** An image-wide scan finds four functions that touch the request word `hud + 0x7C7C` (`_57E0 +0x249C`) and
  `+0x7C82` (`+0x24A2`): `0028EF00`, `0028EF50`, `0028EF70` and `0028F0C0`. Only `003F9F40` reads them relative to the
  block.
- **C2.** Their callers are the chain functions:
  - `EnemyChain_UpdateOnDefeat` `00317ED0` calls `0028EF00` and `0028EF70`;
  - `EnemyChain_TryAdvanceRank` `003183D0` calls `0028EF50`.

  The values they pass are the chain count `022C315C` and the chain rank `022C3158`, which
  [the chain page](../../../13-Rewards-Progression-Economy/loot-drops-and-enemy-chain.md) names.
- **C3.** `0028F0C0(count)` stores a live count at `+0x2498`. Count 0 releases all three of the block's widgets
  (`+0x000`, `+0xD0`, `+0x1A0`).
- **C4.** `003F9F40` builds the `003FACF0` widget at `+0xD0` on bit 2, which the rank advance `0028EF50` sets. The
  number's colour is `fontcolor.bin` colour `0xBF`–`0xC2`, chosen by the rank at `+0x24A2` through `002DD7E0`.

**Readiness text:** *SEMANTICALLY IDENTIFIED / PROVEN - the enemy chain counter: every writer of its request word
`+0x249C` / count `+0x2498` / rank `+0x24A2` is the chain's HUD writer (`0028EF00`/`0028EF50`/`0028EF70`/`0028F0C0`),
called from `EnemyChain_UpdateOnDefeat` / `EnemyChain_TryAdvanceRank` with the chain count `022C315C` and rank `022C3158`;
colour by rank from `fontcolor.bin` `0xBF`–`0xC2`; the rank-up effect is `003FACF0` at `+0xD0`.*

### `_A0D0`: the key-signal strip

**In player terms:** this is a small button guide at the lower left, each row a button icon and what the button does.
The party-down prompt and the leader-selection route ask for it. In this release its row labels ship empty, and it is
not established that the box is ever built (K7).

- **K1.** When `+0x984` bit 0 is set, gate group `0x0040` has `003F7E80` build a 0x110-byte strip widget (procedure
  `003F8250`), bound to the block's `+0x220`.
- **K2.** On creation, `003F8250` places a strip 180 × 80 px, 92 px above the bottom of the screen, under UI root 6.
  `003F8790` keeps one row for each non-zero entry of the four-entry queue at `+0x960`.
- **K3.** Each row is a 0xE8-byte widget (`003F8510`), 180 × 18 px. It holds two texts from the pair table
  `00D11D50`:
  - a label id, 5001–5012;
  - a button template, `0x4662 +` index, which is 18023–18035.
- **K4.** The label id's group 5 maps to kind-2 loader id 1 (the group table `01E09F68`). Loader id 1's size matches
  `key_signal.bin` in the file-size tables of all nine locales. `listhelp_gambit.bin` has the same size in US but not in
  the other locales.

  Group 18 maps to loader id 55, `menu_command_template.bin` (button-glyph control codes). Row 11 of `key_signal.bin`
  is `" Shuffle"`. The rows the modes actually queue (1–4 and 6) are empty in US and read `"(Unused"` in German.
- **K5–K6.** `00290450(mode)` calls `003F80E0`, which copies the mode's four row values from `00D11D80` into `+0x960`.
  The modes are `{1,1,1,1}`, `{4,3,2,1}`, `{4}`, `{4}`, `{4}` and `{5}`. The requesters:
  - mode 2: the widget procedure `0035D6B0` of request 24 (party incapacitated), and request 3's route `0035D980`
    (leader selection);
  - mode 1: `0035C630`, `0035D8D0` and `0035DA80`;
  - mode 5: `002D5EB0`, through the thunk `0035D060`. The `003C8990` / `003C8A50` / `003C8B70` family calls the same
    thunk.

**Readiness text:** *SEMANTICALLY IDENTIFIED / PROVEN (identity) - the key-signal strip (button legend): up to four rows of
{button template from `menu_command_template.bin`, label from `key_signal.bin`}, a mode from `00D11D80` selected through
`00290450` by the request-24 / request-3 prompts and `0035C630`/`0035D8D0`/`0035DA80`; the modes' labels ship empty; the
first setter of the build flag `+0x984` bit 0 is not a displacement write (K7), so whether the strip is ever built is open.*

### `_7EA0`: the 2D side cursor

**In player terms:** this is the on-screen cursor beside the unit being looked at from the target-info window. It fades
over to a new unit instead of jumping, and its angle rotates each frame.

- **S1.** The HUD constructor clears the block (`0028CA30`, 0x80 bytes). Gate group `0x0800` tail-jumps to `0028C870`
  on it.
- **S2.** The draw path is `0028EAB0`, then `0028C970(hud + 0x7EA0)`, then `0028D8A0` once per lane (`+0x30`, `+0x50`),
  then `0028D460`. `0028D460` is the reader of the layout keys **`m2DSideCursorCenterX` / `m2DSideCursorCenterY`**.
- **S3.** The block's only arming path is `00290370`, with `edx` non-zero, into `0028CA40`. Its one caller is
  `002BF0E0`, which is reached from the target-info pane's open path `002BE300` and the thunk `002BE080`. `00290990`
  clears the cursor, and the pane router `002BE1A0` (`_8FA0`) calls it.
- **S4.** `ManagerSub7EA0Entry` is one lane, and the two lanes are armed in turn (`+0x74` bit 1). A lane holds:
  - live flag `+0x14` bit 0 (bit 1 means it is fading out);
  - actor id `+0x18`;
  - level `+0x12`, set to 0x80;
  - position `+0x00`, taken from the actor (`002E7F70`).

**Readiness text:** *SEMANTICALLY IDENTIFIED / PROVEN - the 2D side cursor: two cross-fading lanes (ManagerSub7EA0Entry)
that follow an actor, drawn by `0028D8A0` → `0028D460` (keys `m2DSideCursorCenterX/Y`), armed by the target-info pane
(`002BF0E0` → `00290370` → `0028CA40`) and cleared by `00290990`; fade `+0x76`, angle `+0x70`.*

### `_00A0`: the area-name markers

**In player terms:** these are place-name labels drawn in the field around the character you control. Each one names an
area, or shows `???` when the name is withheld.

- **N1.** `003F8D20` runs from `00253780` through `0028FB40`. It loads the texture named by `[01E0C208]`,
  **`partytop_8_c`**, into `+0x52B8`.
- **N2.** `003F8EC0` follows the focus actor `022C806C` (through `0035BAD0`) and runs `003F9720` twice.
  `003F9720` fills up to 64 sprites at `parent + 0x20 + (i << 8)` on that texture, through `003F9390`.
- **N3.** `003F9720` labels each group of link records with **`MapName_GetAreaNameById`** `00377870` (the
  `planmapname.bin` area names). It uses the name when the field's bit 14 (`00377A40`) or the record's own flag allows
  it. Otherwise it uses text 1004, which is **`"???"`** (`menu_command.bin` row 4).
- **N4.** The draw `003F8C70`, from `0028EAB0`, queues the sprites through `003F1290` and the labels through
  `003F14D0`.

**Readiness text:** *SEMANTICALLY IDENTIFIED / PROVEN (what it draws) - the area-name markers around the focus actor: up
to 64 `partytop_8_c` sprites (ManagerSub00A0Entry, `003F9390`) and area-name labels from `MapName_GetAreaNameById` or
`"???"` (text 1004) over the link records `00264AC0`/`002649B0` return; the records' identity is not read.*

## GR-3: what the combo popup draws

**In player terms:** from the second hit of an Attack combo, a hit counter pops up over the unit. The number slams in
from double size while it fades in. A fading copy then swells outward. The number follows the unit for two seconds,
fades out over the last half second, and restarts from the midpoint if another hit lands. At 12 it stops counting and
grows 20 %. It also pulses and switches to its other digit style, and each further hit replaces the old popup with a
new one.

Inputs are the entry fields: `+0x00..+0x08` position, `+0x0C` unit id, `+0x10` animation clock, `+0x12` age,
`+0x14` count as one decimal digit per nibble, `+0x16` live flag. The time base `[01DFE0B4]` is 1 at 30 fps and 2 at
60 fps.

| step | answer |
|---|---|
| G1 recording (`00289D70`) | A count below 2 is dropped. The count is formatted `"%2.2d"` (`00915FA4`) and packed one digit per nibble, capped at `0x12`, so the popup never shows more than 12. A repeat below the cap pulls the clock back to `0x80`, if it was past that, and zeroes the age. At the cap the old entry is detached (`+0xC = 0`) and a new one is recorded. |
| G2 lifetime (`0028A350`) | The clock climbs `0x10 / [01DFE0B4]` per frame to `0x100`, 16 steps of the 30 Hz base (about 0.53 s). Then the age counts to `60 × [01DFE0B4]` frames (2 s). The entry follows its unit (`002718E0`, eased by `00275490`), and is freed when the unit cannot be resolved or the age runs out. |
| G3 animation tracks | Two keyframe tracks of 12-byte keys `{x, y, t, alpha, bright, curve, scale}`, run by `00271AB0`. `00915F28` is the slam: t `0`→`0x80`, scale 2.0 → 1.0, alpha 0 → 0x80, brightness 0xFF → 0x80, ease-out. `00915F50` is the echo: t `0x80`→`0x100`, scale 1.0 → 2.0, alpha 0x80 → 0, brightness back to 0xFF. Once the clock passes `0x80`, both are drawn. |
| G4 the draw (`0028AAA0`) | Alpha is the unit's display factor (`00272DE0`) × the caller's alpha. It fades linearly over the last quarter of the age. Each track draws one **label sprite**, from the sprite set `[0209AC30]+0x338` (`0035D460`), and the **digits** right to left, from the sprite set `[0209AC30]+0x360` (`0035D470`). The tens digit is skipped when it is 0. Two cases: **below the cap**, digit group 2, placement keys `mNumEffectOffsetX2` / `NumEffectOffsetY2`, label at 100 % and digits at 110 %, spacing −2. **At the cap**, digit group 1, keys `mNumEffectOffsetX1` / `NumEffectOffsetY1`, both at 120 % plus a sine pulse on the frame counter, spacing −4. Each quad is a 0x100 slot from `003F0040`, queued by `003F1290`. |

**Proposed GR-3 answer text:** *ANSWERED 2026-09-30 (SWE2-ORACLE for OPUS), static: `0028AAA0` draws, per popup, a label
sprite from `[0209AC30]+0x338` and the one- or two-digit count from `[0209AC30]+0x360`, placed by
`mNumEffectOffsetX2`/`NumEffectOffsetY2` (at the cap of 12: `…X1`/`…Y1`, 120 %, sine pulse, digit group 1); animated by
two keyframe tracks (`00915F28` slam 2.0→1.0 fade-in, `00915F50` echo 1.0→2.0 fade-out) over a clock of `0x100` at
`0x10/[01DFE0B4]` a frame, then held `60 × [01DFE0B4]` frames (2 s) following the unit and faded over the last quarter;
which glyph the label is (the sprite set's file) is not read.*

## Step table

| step | block | what the checker verifies |
|---|---|---|
| A1–A5 | `_5380` | gate call and tick passes, the draw pass and its three drawers, the key bindings, the producers of pools A / B / C |
| G1–G4 | GR-3 | the recorder's count and cap, the lifetime, the two tracks' bytes, the draw's sprite sets, keys and scales |
| C1–C4 | `_57E0` | image-wide writers of the request word, the chain requesters and globals, the teardown, the rank colour |
| K1–K7 | `_A0D0` | the strip and row widgets, the texts in nine locales, the mode table, the requesters, the build-flag setter census |
| S1–S4 | `_7EA0` | the constructor and gate, the draw path to the key reader, the arm / clear paths, the lane record |
| N1–N4 | `_00A0` | the texture name, the focus follow and the 64 sprites, the area-name / `???` labels, the draw |

## Limits

- **`_5380` pool C** (`+0x330`, list `+0x430`) is not identified. Its drawer `0028A790` reads no key and uses the track
  `00915F68`. Its producer `0030AF30` is named `BattleAction_CheckAndHandleExecutionTimeout` by the atlas only.
- **GR-3:** the files behind the two sprite sets `[0209AC30]+0x338` and `+0x360`, and so the glyph of the label, are
  not read. `00273880` (the value 3 or 1 stored as the quad's top byte) and `00272DE0`'s factor are not read either.
- **`_57E0`:** bit 4 of `+0x249C`, which builds the `003FC3F0` widget at `+0x1A0`, has no setter by displacement
  (C1's scan). What that widget shows is not read.
- **`_A0D0` (K7):** no integer instruction outside `003F7E80` / `003F80D0` addresses `+0x984` or `hud + 0xAA54`. The
  build flag's first setter is therefore a computed or bulk write, or the flag is never set in this build. A requester
  only fills the queue `+0x960`. The row widget's procedure `003F8510` (the text draw) is not read.
- **`_7EA0`:** what `002BF0E0`'s mode value means is not read; the arm fires only on the arms where `edx` is non-zero.
  The main record at `+0x00` (drawn by `0028D260`) is not separated from the lanes.
- **`_00A0`:** the link records come from the table at `[02098E10]+0x70`, which the map screen's reader `003C34E0` also
  walks. They are not identified, and "zone exits" is not claimed. The 8 label records at `+0x4020` (0x250 each) and
  `003F14D0` are not read.
- The function names quoted (`EnemyChain_*`, `Battle_ProcessActionTarget`, `Reward_PublishExpLpPresentation`,
  `MapName_GetAreaNameById`) are the atlas's. The identifications rest on the globals and pages cited, not on the names.
