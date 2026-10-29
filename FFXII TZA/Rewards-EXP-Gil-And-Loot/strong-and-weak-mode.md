---
title: "New Game+ and New Game- (Strong Mode and Weak Mode): how each is offered, what it changes, and how the save keeps it"
kind: "system"
category: "Rewards: EXP, LP, gil and loot"
addresses: "0x0050F460, 0x0050F490, 0x00238A20, 0x00238A50, 0x02089344, 0x00239960, 0x02EBF190, 0x00236740, 0x00236780, 0x0023A2C0, 0x00316DF0, 0x0030C470, 0x00312280, 0x00583D60, 0x0057FB00, 0x0023FBE0, 0x01E0B720, 0x00394130, 0x0023A110, 0x00233C10, 0x00229B40, 0x00394460"
---

## What the player sees

The game names the two modes **New Game+** and **New Game-** in English. The Japanese text calls them
強くてニューゲーム and 弱くてニューゲーム ("strong new game", "weak new game"); that is where the names Strong Mode
and Weak Mode come from. Neither of those two names appears in the English text.

### Where they are offered

- On the title screen, New Game opens a list. Its first three rows are "Start a new game", "Begin New Game+" and
  "Begin New Game-". The help lines read: *Start a new game in "New Game+." In this mode the character's levels are
  higher when the game begins.* and *Start a new game in "New Game-." In this mode there is no use of experience
  points.* Both rows are always there, whether or not the game or Trial Mode has been finished.
- After the staff roll the game asks: *You can now begin your adventure anew in New Game+ mode.* The choices are
  Begin New Game+ and Return to title.
- After the last Trial Mode stage the game shows: *Congratulations on completing Trial Mode! Time to complete:
  h:mm:ss. Your triumph has gained you access to New Game-. In New Game-, your characters will gain no experience.*
  The choices are Begin New Game- and Return to title.

### What New Game+ changes

Every party member is level 90 the first time they join the party. That includes Reks
in the prologue, Vaan at the start of the main story, and every member who joins later. EXP is still earned as
usual, and LP, gil, licences and equipment work as in a normal game.

### What New Game- changes

Kills give no EXP at all, and the reward line shows 0 EXP. LP and gil are still paid.
The party starts at the levels a normal game gives. A member who joins later still gets the usual join catch-up
level: the average of the two highest-level main characters plus the member's own bonus (for example Basch +2;
see [Party members](../Party/party-members.md)).

In the save list, a New Game- file's row shows a red "New Game−" badge at its top left, above the slot number. A
New Game+ file gets no badge: the file records the mode, but nothing in the game reads it back for display.

### Keeping the mode

The mode is stored in the save file, and loading the file brings it back. Going back to the
title clears it from the running game until a save is loaded or a new game is started.

## How it works

### The request bits

Both script verbs only leave a request in the battle flags `0x02089344`:

| Verb | Id | Native | Body | Writes |
|---|---|---|---|---|
| `btlAtelResetNgPlus` | `0x308A` | `0x0050F460` | `jmp 0x00238A20`: `or dword ptr [0x02089344], 2` | bit `0x2` |
| `btlAtelResetNgMinus` | `0x308B` | `0x0050F490` | `jmp 0x00238A50`: `or dword ptr [0x02089344], 4` | bit `0x4` |

The title's New Game list sets the same bits. The list is Config in mode 1 (row list `0x01E0BF60[1]` = `0x01E0B720`,
opened by `fsttl_openconfig`, `0x005120B0` → `0x003945E0` → `0x002406F0`). Its rows `0x18`, `0x1A` and `0x19` carry the
labels 2034, 2191 and 2190 and the help lines 3117, 3396 and 3397. The text lookup `0x002F9860` splits an id into
bank `id / 1000` and index `id mod 1000` (`0x002F9866`-`0x002F98BD`), so these are `menu_message.bin` 34, 191 and 190
and `help_menu.bin` 117, 396 and 397. The row builder `0x0023ED80` adds every row without a condition
(`0x0023EE10`-`0x0023EF27`).

On a confirm, Config's switch (`0x00240065`-`0x00240080`) sends all three commands to `0x00240173`. That code plays sound
`0x2B`, runs `0x00238A50` for `0x19` (`0x00240182`) or `0x00238A20` for `0x1A` (`0x0024018C`), sets the leaving bit
(`0x00240191`) and closes. Leaving the title list stores that bit (1 after a confirm, else the 0 set at
`0x0023FC58`) as the list's status (`0x0024022F`-`0x0024023E`, `0x00394620`), `fsttl_getconfigstatus` (`0x005120E0`, `0x00394430`) returns it, and the title script calls
`fsttl_newgamestart` (`ttl_c01` `configcommand.doconfig`; `ttl_a01` `コンフィグ起動`).

`0x02089344` lies outside the save image, so a request survives the new game's image reset.

### The first area start moves the request into the party block

`fsttl_newgamestart` (`0x00512130`) creates the widget `0x00394130` (`0x00394640`). When it is built, the widget clears
the active image (`0x002EF650`, `0x003942F2`), marks scenario preset 0 as pending (`0x0023A110(0)`, `0x003942F9`, which
stores it at `0x0208D455`) and sets the first field `0x112` (`0x003942FE`-`0x00394303`).

At the next area start, `0x002342F0` calls `0x00239960` (`0x00234349`), which applies the pending preset
([Scenario presets](../Party/scenario-presets.md)). Around its reset of the party block `[0x02EBF190]` it handles
the flag dword `+0x04`:

1. It keeps bits `0x1000`, `0x2000` and `0x4000` of the old dword (`0x002399D7`, then `0x002399F5`-`0x00239A3E` after
   the reset `0x002370C0`, `0x002399E9`).
2. A request bit `0x2` becomes bit `0x2000` and is cleared from `0x02089344` (`0x00239A45`-`0x00239A66`).
3. A request bit `0x4` becomes bit `0x4000` and is cleared (`0x00239A6C`-`0x00239A7E`).

The prologue's end asks for preset 1 (`naf_b04`, `btlAtelSetNextSetSaveData(1)`). That second pass keeps the bits
the same way.

| Bit of `[0x02EBF190] + 4` | Meaning | Getter | Setter |
|---|---|---|---|
| `0x2000` | New Game+ | `0x00236740` | `0x00239960`; `0x0023A2C0(v)`, from the unused verbs `0x3086`/`0x3088` |
| `0x4000` | New Game- | `0x00236780` | `0x00239960` only |
| `0x1000` | Trial Mode stash (kept alongside; see [Saving and loading](../Saving-Loading-And-Settings/saving-and-loading.md)) | `0x00236760` | `0x00239960`, `0x00233C10`, `0x0023A390` |

### New Game+: level 90 on a member's first activation

`0x00316DF0(record, arg)` activates a member. New Game+ is checked twice (`0x00316E14`, `0x00316E25`):

- with arg bit `0x2` set outside New Game+, it skips the join catch-up `0x00317480` (`0x00316E0F`-`0x00316E1B`);
- in New Game+, after the catch-up, a record whose flags byte has bit `0x8` clear (never activated) is grown to
  level 90 by the level grower: `0x0030C470(record, 0x5A, 0)` (`0x00316E2E`-`0x00316E3D`).

The level grower also sets the member's EXP to that level's total ([Battle unit construction](../Characters-And-Objects/battle-unit-construction.md)).
Activation runs from the seat fill `0x00329080` (`0x0032916A`, used by the preset at `0x00239DCB`), from
`addpartymember` (`0x003172E0`, `0x003173A5` and `0x003173D2`), from the staging commit `0x00326110` (`0x003261A6`) and from
`0x00329CC0` (`0x00329D92`). `0x00239960` rebuilds all forty member records (`0x0023AC80`, `0x00239AC4`), which clears their
flags, so the members a preset seats get level 90 at the new game's start and again after the prologue.

### New Game-: no EXP from kills

In the kill reward `0x00312280` ([EXP, LP and level-ups](exp-lp-and-level-ups.md)):

- `0x00312429`-`0x00312444`: while `0x00236780()` is set, the EXP add to `+0x18C` is skipped; the level loop, LP and the
  gil conversion still run;
- `0x00312505`-`0x00312518`: the EXP passed to the reward display `0x0028FB80` becomes 0.

The join catch-up `0x00317480` reads no mode bit, so a joiner's level is set as in a normal game (`0x0031762C`,
[Party members](../Party/party-members.md)).

### The save file and loading

- The block is part of the save image (`0x02EBF190` = `0x002EF640() + 0x4E68C`, `0x00238A84`-`0x00238A92`). Its flag dword
  is image `+0x4E690`. The save capture `0x00229B40` also copies the block head to image `+0x2200` (`0x00229B7B`-`0x00229BE2`).
- The save finaliser `0x00583D60` copies the bits into the header byte `+0x57`: `0x1` from `0x00236760`, `0x4` from
  `0x00236780`, `0x2` from `0x00236740` (`0x00583F5A`-`0x00583F7D`).
- The save list's row filler `0x0057FB00` hides the row's part `+0xD8` (`0x0057FBA1`-`0x0057FBB3`) and shows it again
  when header bit `0x4` is set (`0x0057FBFC`-`0x0057FC0E`).
- The row is record 8 of `save_load.mrp`, and part `+0xD8` is its item 27: a 198 × 30 sprite at row x 36, y 0, cut
  from the `dataface_c` atlas (`DataFace_c.tm2`, sub-image 0, frame 18: x 641, y 129), the "New Game−" badge
  (弱くてニューゲーム in the Japanese files).
- No instruction in the executable tests header bit `0x2`: every test of byte `+0x57` reads bit `0x1` (`0x0057FB2A`,
  `0x0057FC12`, `0x00580C9E`, `0x00584241`, `0x00584410`) or bit `0x4` (`0x0057FBFC`).
- On load, `0x00394130` runs `0x00233C10` (`0x00394222`). That function touches only bit `0x1000` of the flag dword
  (`0x00233C65`-`0x00233CA6`), so bits `0x2000` and `0x4000` stay as saved.
- The title's `fsttl_initialize` (`0x00511EA0`) runs `0x00394460`, whose battle reset `0x00237DF0` (`0x00394486`) reaches
  the block clear `0x002370C0` through `0x0023AF50`. On the title the running game has no mode until a save is loaded
  or a new game starts.

### Where the scripts offer the two questions

| Script | Field | Reached from | Function | Choice 0 | Other choice |
|---|---|---|---|---|---|
| `ttl_b01` | 13 | `bhm_d01`, after event 399: `mapjump(13, 0, 1)` | `監督.main`: event 429 (staff roll), then `aask_1ff` | `btlAtelResetNgPlus(); fsttl_newgamestart();` | `softwarereset()` |
| `ttl_d01` | 1147 | the Trial Mode stage scripts `tri_a01`-`tri_t05`, on the stage whose field is `0x051F`, after achievement 40 (`unkCall_5ad(40)`) and event `0x1AB`: `mapjump(0x047b, 0, 1)` | `監督.main`: play time into the message, then `aask_1ff` | `btlAtelResetNgMinus(); fsttl_newgamestart();` | `softwarereset()` |

## State

| Address | Type | Meaning | Written by | Read by |
|---|---|---|---|---|
| `0x02089344` bit `0x2` | request | New Game+ requested | `0x00238A20` (verb `0x308A`; Config `0x0024018C`) | `0x00239960` (`0x00239A4B`), which clears it |
| `0x02089344` bit `0x4` | request | New Game- requested | `0x00238A50` (verb `0x308B`; Config `0x00240182`) | `0x00239960` (`0x00239A6C`), which clears it |
| `[0x02EBF190] + 4` bit `0x2000` | flag | New Game+ | `0x00239960`, `0x0023A2C0` | `0x00236740`: `0x00316DF0`, `0x00583D60`, `0x0050F3F0` |
| `[0x02EBF190] + 4` bit `0x4000` | flag | New Game- | `0x00239960` | `0x00236780`: `0x00312280`, `0x00583D60` |
| header `+0x57` bit `0x2` / `0x4` | save header | the file's mode | `0x00583D60` | bit `0x4`: `0x0057FB00` (`0x0057FBFC`); bit `0x2`: none |
| `0x0208D455` | `i8` | pending scenario preset | `0x0023A110` (new game: 0), `0x0050F810` (verb `0x302B`) | `0x00239960` |

## Modding notes

- The New Game+ starting level is the immediate `0x5A` at `0x00316E39` (`lea edx, [r8 + 0x5A]`).
- New Game- blocks only kill EXP, at `0x00312430` (`jne`) and its display at `0x00312513` (`cmovne`). Other ways a level
  changes, such as the join catch-up, are not blocked.
- Setting `[0x02EBF190] + 4` bit `0x2000` or `0x4000` in a running game switches the mode at once. Level 90 only
  applies to members not yet activated.

## Related

- [EXP, LP and level-ups](exp-lp-and-level-ups.md) - the kill reward that New Game- gates.
- [Scenario presets](../Party/scenario-presets.md) - the preset step that carries the mode bits.
- [Config screen](../Menus-And-HUD/config-screen.md) - the title's New Game list.
- [Save file format](../Saving-Loading-And-Settings/save-file-format.md) - the header byte `+0x57`.
