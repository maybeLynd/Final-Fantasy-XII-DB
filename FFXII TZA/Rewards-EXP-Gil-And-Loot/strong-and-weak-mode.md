[Home](../../README.md) / [Rewards: EXP, LP, gil and loot](README.md) / New Game+ and New Game- (Strong Mode and Weak Mode)

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| New Game+ and New Game- (Strong Mode and Weak Mode): how each is offered, what it changes, and how the save keeps it | system | Rewards: EXP, LP, gil and loot | EXP, loot and progression | The two alternative new games: where the game offers New Game+ and New Game- (the title's New Game list, the question after the staff roll, the Trial Mode completion screen), the request bits the two script verbs set, how the first area start moves them into the party block's flag word, the level-90 rule of New Game+, the EXP and EXP-display block of New Game-, the save header bits and how a loaded save keeps its mode. | 0x0050F460, 0x0050F490, 0x00238A20, 0x00238A50, 0x02089344, 0x00239960, 0x02EBF190, 0x00236740, 0x00236780, 0x0023A2C0, 0x00316DF0, 0x0030C470, 0x00312280, 0x00583D60, 0x0057FB00, 0x0023FBE0, 0x01E0B720, 0x00394130, 0x0023A110, 0x00233C10, 0x00229B40, 0x00394460 |

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
level: the average of the two highest-level main characters (`sum / n`) plus the member's own bonus
(`level = max(sum / n, 1) + row[+0x2E]`, through `0x0030C470`), for the `n` (at most 2) other active main characters
found and `sum` their levels `+0x1C2`, with `sum / n` taken as 0 when `n == 0` (`0x003175C5`-`0x0031760F` in `0x00317480`;
for example Basch +2; see [Party members](../Party/party-members.md)).

In the save list, a New Game- file's row shows a red "New Game−" badge at its top left, above the slot number. A
New Game+ file gets no badge: the file records the mode, but nothing in the game reads it back for display.

### Keeping the mode

The mode is stored in the save file, and loading the file brings it back. Going back to the
title clears it from the running game until a save is loaded or a new game is started.

Choosing either mode, from the title list or from the question a script asks after the staff roll or Trial Mode, only
leaves a request. The request becomes the game's mode when the new game's first area starts, and from then on it
travels in the save file.

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
bank `id / 1000` and index `id mod 1000`¹, so these are `menu_message.bin` 34, 191 and 190
and `help_menu.bin` 117, 396 and 397.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002F9866`-`0x002F98BD` |

</details>

The row builder `0x0023ED80` records every row's id and kind without a condition¹, but builds a widget only for kinds 1, 2, 3, 6, 8 and 10²; these three rows are
kind 13 and get none.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0023EE10`-`0x0023EF27`, `0x0023EE47`, `0x0023EE69` |
| ² | `0x0023EE6F`-`0x0023EE83` |

</details>

`0x002406F0(a, b)` builds the screen with `0x00244F50(0x4D8, 0x0023FBE0, arguments)` only
while `0x0208E6D8` is 0, the three construct arguments being the dword 0, its own byte
`a` and its own word `b`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00240703`-`0x00240736` |

</details>

On a confirm, Config's switch¹ sends all three commands to `0x00240173`. That code plays sound
`0x2B`, runs `0x00238A50` for `0x19`² or `0x00238A20` for `0x1A`³, sets the leaving bit⁴ and closes. Leaving the title list stores that bit (1 after a confirm, else the 0 set at
`0x0023FC58`) as the list's status⁵, `fsttl_getconfigstatus`⁶ returns it, and the title script calls
`fsttl_newgamestart` (`ttl_c01` `configcommand.doconfig`; `ttl_a01` `コンフィグ起動`).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00240065`-`0x00240080` |
| ² | `0x00240182` |
| ³ | `0x0024018C` |
| ⁴ | `0x00240191` |
| ⁵ | `0x0024022F`-`0x0024023E`, `0x00394620` |
| ⁶ | `0x005120E0`, `0x00394430` |

</details>

The status is the byte `0x01EFAC11`, 3 in the image: `0x00394620(value)` stores its low byte there and
`0x00394430()` returns it zero-extended¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00394620`-`0x00394626`, `0x00394430`-`0x00394437` |

</details>

`0x02089344` lies outside the save image, so a request survives the new game's image reset.

### The first area start moves the request into the party block

`fsttl_newgamestart`¹ creates the widget `0x00394130`². When it is built, the widget clears
the active image³, marks scenario preset 0 as pending (`0x0023A110(0)`, `0x003942F9`, which
stores it at `0x0208D455`) and sets the first field `0x112`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00512130` |
| ² | `0x00394640` |
| ³ | `0x002EF650`, `0x003942F2` |
| ⁴ | `0x003942FE`-`0x00394303` |

</details>

At the next area start, `0x002342F0` calls `0x00239960`¹, which applies the pending preset
([Scenario presets](../Party/scenario-presets.md)). Around its reset of the party block `[0x02EBF190]` it handles
the flag dword `+0x04`:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00234349` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | It keeps bits `0x1000`, `0x2000` and `0x4000` of the old dword (`0x002399D7`, then `0x002399F5`-`0x00239A3E` after the reset `0x002370C0`, `0x002399E9`). |   |
| 2 | A request bit `0x2` becomes bit `0x2000` and is cleared from `0x02089344`. | `0x00239A45`-`0x00239A66` |
| 3 | A request bit `0x4` becomes bit `0x4000` and is cleared. | `0x00239A6C`-`0x00239A7E` |

Of the stores that name `0x02089344`, only these two clear bits `0x2` and `0x4`: `0x00233C7C` and `0x00238A30` change only
bit `0x1` (`0x00238A43` for `0x00238A30`), and `0x00238A20` and `0x00238A50` set the requests. An area start that applies no
preset (an area init that returns at once because `0x02089300` is 0, `0x002342F4`-`0x002342FB`; none pending, the value -2,
which runs `0x00237DF0` instead, any other negative value, or a number at or past the preset count,
`0x00239966`-`0x002399BB`) leaves a request set, and so does a return to the title.

The prologue's end asks for preset 1 (`naf_b04`, `btlAtelSetNextSetSaveData(1)`). That second pass keeps the bits
the same way.

| Bit of `[0x02EBF190] + 4` | Meaning | Getter | Setter |
|---|---|---|---|
| `0x2000` | New Game+ | `0x00236740` | `0x00239960`; `0x0023A2C0(v)`, from the Reserve verbs `0x3086`/`0x3088` |
| `0x4000` | New Game- | `0x00236780` | `0x00239960` only |
| `0x1000` | Trial Mode stash (kept alongside; see [Saving and loading](../Saving-Loading-And-Settings/saving-and-loading.md)) | `0x00236760` | `0x00239960`, `0x00233C10`, `0x0023A390` |

### New Game+: level 90 on a member's first activation

`0x00316DF0(record, arg)` activates a member. New Game+ is checked twice¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00316E14`, `0x00316E25` |

</details>

- with arg bit `0x2` set outside New Game+, it skips the join catch-up `0x00317480`¹;
- in New Game+, after the catch-up, a record whose flags byte has bit `0x8` clear (never activated) is grown to
  level 90 by the level grower: `0x0030C470(record, 0x5A, 0)`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00316E0F`-`0x00316E1B` |
| ² | `0x00316E2E`-`0x00316E3D` |

</details>

The level grower also sets the member's EXP to that level's total ([Battle unit construction](../Characters-And-Objects/battle-unit-construction.md)).
Activation runs from the seat fill `0x00329080` (`0x0032916A`, used by the preset at `0x00239DCB`), from
`addpartymember`¹, from the staging commit `0x00326110`² and from
`0x00329CC0`³. `0x00239960` rebuilds all forty member records⁴, which clears their
flags, so the members a preset seats get level 90 at the new game's start and again after the prologue.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003172E0`, `0x003173A5` and `0x003173D2` |
| ² | `0x003261A6` |
| ³ | `0x00329D92` |
| ⁴ | `0x0023AC80`, `0x00239AC4` |

</details>

### New Game-: no EXP from kills

In the kill reward `0x00312280` ([EXP, LP and level-ups](exp-lp-and-level-ups.md)):

- `0x00312429`-`0x00312444`: while `0x00236780()` is set, the EXP add to `+0x18C` is skipped; the level loop, LP and the
  gil conversion still run;
- `0x00312505`-`0x00312518`: the EXP passed to the reward display `0x0028FB80` becomes 0.

The join catch-up `0x00317480` reads no mode bit, so a joiner's level is set as in a normal game (`0x0031762C`,
[Party members](../Party/party-members.md)).

### The save file and loading

- The block is part of the save image (`0x02EBF190` = `0x002EF640() + 0x4E68C`, `0x00238A84`-`0x00238A92`). Its flag dword
  is image `+0x4E690`. The save capture `0x00229B40` also copies the block head to image `+0x2200`¹.
- The save finaliser `0x00583D60` sets the bits in the header byte `+0x57` with `or`: `0x1` from `0x00236760`, `0x4`
  from `0x00236780`, `0x2` from `0x00236740`². It never clears one of them, so a bit already
  set in the destination's `+0x57` is left set.
- The save list's row filler `0x0057FB00` hides the row's part `+0xD8`³ and shows it again
  when header bit `0x4` is set⁴.
- The row is record 8 of `save_load.mrp`, and part `+0xD8` is its item 27: a 198 × 30 sprite at row x 36, y 0, cut
  from the `dataface_c` atlas (`DataFace_c.tm2`, sub-image 0, frame 18: x 641, y 129), the "New Game−" badge
  (弱くてニューゲーム in the Japanese files).
- No instruction in the executable tests header bit `0x2`: every test of byte `+0x57` reads bit `0x1`⁵ or bit `0x4`⁶.
- On load, the load-complete call `0x00285E60` runs `0x00233C10`⁷. Its prelude `0x00235AF0`⁸ first
  copies the image's `0x6000`-byte copy at `+0x2200` over the block, flag dword included, when the block's first two
  dwords, byte `+0x5B42` or word `+0x5B12` differ from the copy's⁹.
- With the block bound and its magic in place, `0x00233C10` itself writes only bit `0x1000` of the flag dword
 ¹⁰, so bits `0x2000` and `0x4000` keep the saved block's value or, after that copy, the copy's.
- With a wrong magic `0x00233C10` runs the battle reset `0x00237DF0` instead¹¹, and with an empty pointer
  it binds the block and runs that reset twice¹². The reset's block clear `0x002370C0`
  (through `0x0023AF50`, `0x00237DF6`, `0x0023AF56`) zeroes the whole flag dword, these bits included.
- The title's `fsttl_initialize`¹³ runs `0x00394460`, whose battle reset `0x00237DF0`¹⁴ reaches
  the block clear `0x002370C0` through `0x0023AF50`. On the title the running game has no mode until a save is loaded
  or a new game starts.
- Before that reset `0x00394460` runs `0x00229AD0`, clears byte `+0xDE6` of `[0x0209AC30]` and runs `0x002B9FD0`,
  `0x002501E0` and `0x002DDE60`¹⁵. After it, it creates the widget `0x00394070` with
  `0x00244F50(0xD8, 0x00394070, 0)` when `0x02AEE4C0` is empty¹⁶ and ends with a jump to
  `0x001D6C60`¹⁷.
- The widget's procedure `0x00394070` takes three messages. Message 1 stores the widget
  in `0x02AEE4C0`, zeroes `+0xC0`, runs `0x00393FF0` and `0x002E1C20(0, 0x15)` and attaches the
  widget under `[0x0208EA28]` with `0x00244960`¹⁸. Message 16 sets bit
  `0x1` of `+0xC0`¹⁹.
- Message 18 calls `0x0024A680([+0xC8], 1)`, frees the pointer `+0xD0` through `0x003697F0`
  when it is not null and nulls it, calls `0x002E1CA0(0, 0x15)` and zeroes `0x02AEE4C0`
 ²⁰. Every other message goes on to `0x005C5230`²¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00229B7B`-`0x00229BE2` |
| ² | `0x00583F5A`-`0x00583F7D` |
| ³ | `0x0057FBA1`-`0x0057FBB3` |
| ⁴ | `0x0057FBFC`-`0x0057FC0E` |
| ⁵ | `0x0057FB2A`, `0x0057FC12`, `0x00580C9E`, `0x00584241`, `0x00584410` |
| ⁶ | `0x0057FBFC` |
| ⁷ | `0x00285E86` |
| ⁸ | `0x00233C14` |
| ⁹ | `0x00235B19`-`0x00235B48`, `0x00235B76`, `0x002EF4A0` |
| ¹⁰ | `0x00233C65`-`0x00233CA6` |
| ¹¹ | `0x00233C59` |
| ¹² | `0x00233C3F`, `0x00233C48` |
| ¹³ | `0x00511EA0` |
| ¹⁴ | `0x00394486` |
| ¹⁵ | `0x00394464`-`0x00394481` |
| ¹⁶ | `0x0039448B`-`0x003944A4` |
| ¹⁷ | `0x003944AD` |
| ¹⁸ | `0x003940F2`-`0x00394121` |
| ¹⁹ | `0x003940E3` |
| ²⁰ | `0x00394097`-`0x003940D2` |
| ²¹ | `0x00394092` |

</details>

### Where the scripts offer the two questions

| Script | Field | Reached from | Function | Choice 0 | Other choice |
|---|---|---|---|---|---|
| `ttl_b01` | 13 | `bhm_d01`, after event 399: `mapjump(13, 0, 1)` | `監督.main`: event 429 (staff roll), then `aask_1ff` | `btlAtelResetNgPlus(); fsttl_newgamestart();` | `softwarereset()` |
| `ttl_d01` | 1147 | the Trial Mode stage scripts `tri_a01`-`tri_t05`, on the stage whose field is `0x051F`, after achievement 40 (`unkCall_5ad(40)`) and event `0x1AB`: `mapjump(0x047b, 0, 1)` | `監督.main`: play time into the message, then `aask_1ff` | `btlAtelResetNgMinus(); fsttl_newgamestart();` | `softwarereset()` |

## State

<details>
<summary>Show the state it keeps</summary>

| Address | Type | Meaning | Written by | Read by |
|---|---|---|---|---|
| `0x02089344` bit `0x2` | request | New Game+ requested | `0x00238A20` (verb `0x308A`; Config `0x0024018C`) | `0x00239960` (`0x00239A4B`), which clears it |
| `0x02089344` bit `0x4` | request | New Game- requested | `0x00238A50` (verb `0x308B`; Config `0x00240182`) | `0x00239960` (`0x00239A6C`), which clears it |
| `[0x02EBF190] + 4` bit `0x2000` | flag | New Game+ | `0x00239960`, `0x0023A2C0` | `0x00236740`: `0x00316DF0`, `0x00583D60`, `0x0050F3F0` |
| `[0x02EBF190] + 4` bit `0x4000` | flag | New Game- | `0x00239960` | `0x00236780`: `0x00312280`, `0x00583D60` |
| header `+0x57` bit `0x2` / `0x4` | save header | the file's mode | `0x00583D60` | bit `0x4`: `0x0057FB00` (`0x0057FBFC`); bit `0x2`: no reader |
| `0x0208D455` | `i8` | pending scenario preset | `0x0023A110` (new game: 0), `0x0050F810` (verb `0x302B`) | `0x00239960` |

</details>

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

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 181 calls with 46 other topics</summary>

**Characters and objects** (explained on [frame update order](../Engine-Core/frame-update-order.md), [force fight mode](../Engine-Core/force-fight-mode.md), [party data](../Party/party-data.md), [party control modes](../Engine-Core/party-control-modes.md), [debug menu](../Engine-Core/debug-menu.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002342F0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) | is called by | [`0x0026CE60`](../Characters-And-Objects/actor-managers.md) Actor system: initialize manager runtime (on actor managers) |
| [`0x00236760`](strong-and-weak-mode.md) | is called by | [`0x00300E40`](../Items-Equipment-Shops-And-Licenses/equipping-an-item.md) Battle unit: teardown and despawn (on equipping an item) |
| [`0x00237DF0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) | calls | [`0x00329CC0`](strong-and-weak-mode.md) Battle slot map: initialize mapping classes |
| [`0x0023AC80`](../Items-Equipment-Shops-And-Licenses/equipment.md) Battle stats: initialize definition record (on equipment) | is called by | [`0x0023A570`](../Characters-And-Objects/battle-unit-construction.md) Battle unit: apply unit definition (on battle unit construction) |
| [`0x00312280`](strong-and-weak-mode.md) Battle unit: process defeat rewards and loot | calls | [`0x00265020`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor: get world position (on party during scenes) |
| [`0x00316DF0`](strong-and-weak-mode.md) Definition runtime: activate and apply configured side effects | is called by | [`0x00329CC0`](strong-and-weak-mode.md) Battle slot map: initialize mapping classes |

**Sound and music** (explained on [config screen](../Menus-And-HUD/config-screen.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002DDE60`](../Saving-Loading-And-Settings/game-settings.md) (on game settings) | calls | [`0x002DF530`](../Saving-Loading-And-Settings/game-settings.md) (on game settings) |

**Enemy AI and gambits** (explained on [unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md), [item and ability ids](../Engine-Core/item-and-ability-ids.md), [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00233C10`](strong-and-weak-mode.md) | calls | [`0x00327F80`](../Party/party-data.md) Gambit runtime: rebuild all order sets (on party data) |
| [`0x00239960`](../Party/scenario-presets.md) (on scenario presets) | calls | [`0x00327CB0`](../Enemy-AI-And-Gambits/gambits.md) Gambit config: load authored preset and rebuild runtime orders (on gambits) |
| [`0x0023AC80`](../Items-Equipment-Shops-And-Licenses/equipment.md) Battle stats: initialize definition record (on equipment) | calls | [`0x00326030`](../Enemy-AI-And-Gambits/gambits.md) Gambit config: initialize three banks from base pairs (on gambits)<br>[`0x00327CB0`](../Enemy-AI-And-Gambits/gambits.md) Gambit config: load authored preset and rebuild runtime orders (on gambits)<br>[`0x00327DE0`](../Enemy-AI-And-Gambits/gambits.md) Gambit runtime: rebuild order set for stats record (on gambits) |

**Battle actions** (explained on [frame update order](../Engine-Core/frame-update-order.md), [battle unit fields](../Characters-And-Objects/battle-unit-fields.md), [call signatures](../Engine-Core/call-signatures.md), [party control modes](../Engine-Core/party-control-modes.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002342F0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) | calls | [`0x00306570`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning)<br>[`0x0030E010`](../Characters-And-Objects/battle-unit-fields.md) (on battle unit fields)<br>[`0x0030FE60`](../Enemy-AI-And-Gambits/gambit-conditions.md) (on gambit conditions) |
| [`0x0030C470`](stat-growth-per-level.md) (on stat growth per level) | is called by | [`0x00306760`](../Party/party-table.md) Battle action: update special presentation sequence (on party table) |

**Damage and battle formulas** (explained on [battle unit construction](../Characters-And-Objects/battle-unit-construction.md), [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md), [subsystem update flags](../Engine-Core/subsystem-update-flags.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00237DF0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) | calls | [`0x0023AC80`](../Items-Equipment-Shops-And-Licenses/equipment.md) Battle stats: initialize definition record (on equipment) |
| [`0x00239960`](../Party/scenario-presets.md) (on scenario presets) | calls | [`0x0023AC80`](../Items-Equipment-Shops-And-Licenses/equipment.md) Battle stats: initialize definition record (on equipment)<br>[`0x00320A40`](../Menus-And-HUD/gambit-screen.md) (on gambit screen) |
| [`0x0030C470`](stat-growth-per-level.md) (on stat growth per level) | calls | [`0x0030F340`](../Damage-And-Battle-Formulas/hp-and-ko.md) Battle stats: reconcile current hp to effective maximum (on hp and ko)<br>[`0x0030F5A0`](../World-Areas-And-Travel/save-and-teleport-crystals.md) Battle stats: reconcile resources to effective capacity (on save and teleport crystals) |
| [`0x0030C470`](stat-growth-per-level.md) (on stat growth per level) | is called by | [`0x0023AC80`](../Items-Equipment-Shops-And-Licenses/equipment.md) Battle stats: initialize definition record (on equipment) |
| [`0x00312280`](strong-and-weak-mode.md) Battle unit: process defeat rewards and loot | calls | [`0x00320AB0`](../Engine-Core/subsystem-update-flags.md) (on subsystem update flags) |

**Engine core** (explained on [frame update order](../Engine-Core/frame-update-order.md), [enemy respawning](../Enemy-Spawning/enemy-respawning.md), [startup constants](../Engine-Core/startup-constants.md), [global state accessors](../Engine-Core/global-state-accessors.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00233C10`](strong-and-weak-mode.md) | calls | [`0x00229ED0`](../Saving-Loading-And-Settings/game-settings.md) (on game settings) |
| [`0x00237DF0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) | calls | [`0x00229ED0`](../Saving-Loading-And-Settings/game-settings.md) (on game settings)<br>[`0x0032A160`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) |
| [`0x002DDE60`](../Saving-Loading-And-Settings/game-settings.md) (on game settings) | calls | [`0x00229E40`](../Story-Events-And-Hunts/script-language-differences.md) (on script language differences) |
| [`0x002EF650`](../Saving-Loading-And-Settings/loading-a-save.md) (on loading a save) | is called by | [`0x0022B6E0`](../Items-Equipment-Shops-And-Licenses/bazaar.md) (on bazaar) |
| [`0x00394130`](../Saving-Loading-And-Settings/loading-a-save.md) (on loading a save) | calls | [`0x001EDEC0`](../Saving-Loading-And-Settings/loading-a-save.md) (on loading a save) |

**Gameplay** (explained on [frame update order](../Engine-Core/frame-update-order.md), [party verbs](../Scripts-And-Script-Commands/party-verbs.md), [identifier spaces](../Engine-Core/identifier-spaces.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00233C10`](strong-and-weak-mode.md) | calls | [`0x00237DF0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) |
| [`0x00236740`](strong-and-weak-mode.md) | is called by | [`0x00316DF0`](strong-and-weak-mode.md) Definition runtime: activate and apply configured side effects |
| [`0x00239960`](../Party/scenario-presets.md) (on scenario presets) | calls | [`0x00237DF0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) |
| [`0x0023AC80`](../Items-Equipment-Shops-And-Licenses/equipment.md) Battle stats: initialize definition record (on equipment) | is called by | [`0x00237DF0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) |
| [`0x0023AF50`](../Party/starting-inventory.md) Inventory: initialize primary state from authored table (on starting inventory) | is called by | [`0x00237DF0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) |
| [`0x0030C470`](stat-growth-per-level.md) (on stat growth per level) | is called by | [`0x00316DF0`](strong-and-weak-mode.md) Definition runtime: activate and apply configured side effects |
| [`0x003172E0`](../Party/party-members.md) Party configuration: add selector00 to06 to available index4 to8 (on party members) | calls | [`0x00316DF0`](strong-and-weak-mode.md) Definition runtime: activate and apply configured side effects |
| [`0x00317480`](../Party/party-members.md) (on party members) | is called by | [`0x00316DF0`](strong-and-weak-mode.md) Definition runtime: activate and apply configured side effects |
| [`0x00326110`](../Party/party-members.md) Party configuration: set empty index selector (on party members) | calls | [`0x00316DF0`](strong-and-weak-mode.md) Definition runtime: activate and apply configured side effects |
| [`0x00329080`](../Scripts-And-Script-Commands/party-verbs.md) Party configuration: set definition selector for index (on party verbs) | calls | [`0x00316DF0`](strong-and-weak-mode.md) Definition runtime: activate and apply configured side effects<br>[`0x00322C50`](../Engine-Core/item-and-ability-ids.md) Battle encoded id: is valid for class (on item and ability ids)<br>[`0x00323540`](../Party/party-members.md) Definition runtime: deactivate and remove configured items (on party members) |
| [`0x00329CC0`](strong-and-weak-mode.md) Battle slot map: initialize mapping classes | calls | [`0x00316DF0`](strong-and-weak-mode.md) Definition runtime: activate and apply configured side effects<br>[`0x00322C50`](../Engine-Core/item-and-ability-ids.md) Battle encoded id: is valid for class (on item and ability ids)<br>[`0x00323540`](../Party/party-members.md) Definition runtime: deactivate and remove configured items (on party members) |
| [`0x00329CC0`](strong-and-weak-mode.md) Battle slot map: initialize mapping classes | is called by | [`0x00237DF0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) |
| [`0x00394460`](strong-and-weak-mode.md) | calls | [`0x00237DF0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) |

**Controls and input** (explained on [force fight mode](../Engine-Core/force-fight-mode.md), [config screen](../Menus-And-HUD/config-screen.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00236760`](strong-and-weak-mode.md) | is called by | [`0x00253C70`](../Controls-And-Input/controls.md) (on controls) |
| [`0x002DDE60`](../Saving-Loading-And-Settings/game-settings.md) (on game settings) | calls | [`0x001E0FF0`](../Saving-Loading-And-Settings/game-settings.md) (on game settings)<br>[`0x001E1020`](../Saving-Loading-And-Settings/game-settings.md) (on game settings) |
| [`0x00394460`](strong-and-weak-mode.md) | calls | [`0x002501E0`](strong-and-weak-mode.md) |

**Items, equipment, shops and licenses** (explained on [item and ability ids](../Engine-Core/item-and-ability-ids.md), [party data](../Party/party-data.md), [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [battle unit construction](../Characters-And-Objects/battle-unit-construction.md), [party verbs](../Scripts-And-Script-Commands/party-verbs.md), [party members](../Party/party-members.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00233C10`](strong-and-weak-mode.md) | calls | [`0x0030B6A0`](../Items-Equipment-Shops-And-Licenses/inventory.md) Inventory runtime: rebase class descriptors and clear derived state (on inventory) |
| [`0x002370C0`](../Party/party-data.md) (on party data) | is called by | [`0x0023AF50`](../Party/starting-inventory.md) Inventory: initialize primary state from authored table (on starting inventory) |
| [`0x00237DF0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) | calls | [`0x0023AF50`](../Party/starting-inventory.md) Inventory: initialize primary state from authored table (on starting inventory) |
| [`0x00239960`](../Party/scenario-presets.md) (on scenario presets) | calls | [`0x00300BA0`](../Items-Equipment-Shops-And-Licenses/inventory.md) (on inventory)<br>[`0x0031A630`](../Items-Equipment-Shops-And-Licenses/equipment.md) Battle stats: set equipment slot direct (on equipment)<br>[`0x00323910`](../Items-Equipment-Shops-And-Licenses/buying-a-license.md) Battle stats: set license node state and apply side effects (on buying a license) |
| [`0x0023AC80`](../Items-Equipment-Shops-And-Licenses/equipment.md) Battle stats: initialize definition record (on equipment) | calls | [`0x0031A630`](../Items-Equipment-Shops-And-Licenses/equipment.md) Battle stats: set equipment slot direct (on equipment)<br>[`0x00323910`](../Items-Equipment-Shops-And-Licenses/buying-a-license.md) Battle stats: set license node state and apply side effects (on buying a license) |
| [`0x0023AF50`](../Party/starting-inventory.md) Inventory: initialize primary state from authored table (on starting inventory) | calls | [`0x00300BA0`](../Items-Equipment-Shops-And-Licenses/inventory.md) (on inventory) |
| [`0x0030C470`](stat-growth-per-level.md) (on stat growth per level) | calls | [`0x00324100`](../Characters-And-Objects/battle-unit-construction.md) Battle stats: compute license derived rank (on battle unit construction) |
| [`0x00316DF0`](strong-and-weak-mode.md) Definition runtime: activate and apply configured side effects | calls | [`0x00300B80`](../Story-Events-And-Hunts/shared-zone-script-actors.md) (on shared zone script actors)<br>[`0x0030C410`](../Items-Equipment-Shops-And-Licenses/inventory.md) (on inventory) |
| [`0x00317480`](../Party/party-members.md) (on party members) | calls | [`0x003237C0`](../Party/party-members.md) Battle stats: compute lp including owned license costs (on party members) |

**Movement and pathfinding** (explained on [frame update order](../Engine-Core/frame-update-order.md), [mpk map pack](../World-Areas-And-Travel/mpk-map-pack.md), [party slots](../Party/party-slots.md), [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md), [navigation mesh and pathfinding](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md), [battle units](../Characters-And-Objects/battle-units.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002342F0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) | calls | [`0x0031BD60`](../Party/party-slots.md) (on party slots)<br>[`0x00322220`](../World-Areas-And-Travel/mpk-map-pack.md) (on mpk map pack)<br>[`0x00327360`](../Party/party-slots.md) (on party slots)<br>[`0x0033A380`](../Movement-And-Pathfinding/battle-locomotion.md) (on battle locomotion)<br>[`0x00383740`](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md) Navigation: get world bounds xz (on navigation mesh and pathfinding)<br>[`0x003924B0`](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md) (on navigation mesh and pathfinding) |
| [`0x00312280`](strong-and-weak-mode.md) Battle unit: process defeat rewards and loot | calls | [`0x00319490`](loot-pickups.md) (on loot pickups) |

**Party** (explained on [party verbs](../Scripts-And-Script-Commands/party-verbs.md), [party control modes](../Engine-Core/party-control-modes.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00239960`](../Party/scenario-presets.md) (on scenario presets) | calls | [`0x00329080`](../Scripts-And-Script-Commands/party-verbs.md) Party configuration: set definition selector for index (on party verbs) |
| [`0x00316DF0`](strong-and-weak-mode.md) Definition runtime: activate and apply configured side effects | is called by | [`0x003172E0`](../Party/party-members.md) Party configuration: add selector00 to06 to available index4 to8 (on party members)<br>[`0x00326110`](../Party/party-members.md) Party configuration: set empty index selector (on party members)<br>[`0x00329080`](../Scripts-And-Script-Commands/party-verbs.md) Party configuration: set definition selector for index (on party verbs) |
| [`0x003172E0`](../Party/party-members.md) Party configuration: add selector00 to06 to available index4 to8 (on party members) | calls | [`0x00321100`](../Party/party-members.md) (on party members)<br>[`0x003261D0`](../Party/party-members.md) Party configuration: reconcile roster from current selectors (on party members) |
| [`0x00326110`](../Party/party-members.md) Party configuration: set empty index selector (on party members) | calls | [`0x003261D0`](../Party/party-members.md) Party configuration: reconcile roster from current selectors (on party members) |
| [`0x00326110`](../Party/party-members.md) Party configuration: set empty index selector (on party members) | is called by | [`0x003170E0`](../Party/party-members.md) Party configuration: add selector07 to25 to available primary index (on party members) |
| [`0x00329080`](../Scripts-And-Script-Commands/party-verbs.md) Party configuration: set definition selector for index (on party verbs) | is called by | [`0x003261D0`](../Party/party-members.md) Party configuration: reconcile roster from current selectors (on party members)<br>[`0x003273D0`](../Party/party-members.md) Party configuration: set selectors and reconcile roster (on party members) |
| [`0x00329CC0`](strong-and-weak-mode.md) Battle slot map: initialize mapping classes | calls | [`0x00326500`](../Party/party-leader.md) Party focus: select and request default actor (on party leader) |
| [`0x00583D60`](../Saving-Loading-And-Settings/save-file-format.md) Save image: finalize header and checksum (on save file format) | calls | [`0x003271D0`](../Scripts-And-Script-Commands/party-verbs.md) Party focus: get preferred definition selector (on party verbs) |

**Steam and achievements** (explained on [debug menu](../Engine-Core/debug-menu.md), [shops](../Items-Equipment-Shops-And-Licenses/shops.md), [gil](gil.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00312280`](strong-and-weak-mode.md) Battle unit: process defeat rewards and loot | calls | [`0x00316A50`](../Steam-And-Achievements/achievements.md) (on achievements) |
| [`0x00583D60`](../Saving-Loading-And-Settings/save-file-format.md) Save image: finalize header and checksum (on save file format) | calls | [`0x00315390`](../Items-Equipment-Shops-And-Licenses/shops.md) (on shops)<br>[`0x003166F0`](../Steam-And-Achievements/achievements.md) (on achievements) |

**Graphics** (explained on [exp lp and level ups](exp-lp-and-level-ups.md), [ps2 cpu emulation](../Engine-Core/ps2-cpu-emulation.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00312280`](strong-and-weak-mode.md) Battle unit: process defeat rewards and loot | calls | [`0x0028FB80`](../Menus-And-HUD/hud.md) (on hud) |
| [`0x0057FB00`](strong-and-weak-mode.md) | calls | [`0x002DC290`](../Engine-Core/ps2-cpu-emulation.md) (on ps2 cpu emulation) |

**Random numbers** (explained on [loot drops](loot-drops.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002342F0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) | calls | [`0x00328D80`](../Random-Numbers/random-number-generators.md) (on random number generators) |

**Game files and data tables** (explained on [prefetch manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md), [file path resolution](../Game-Files-And-Data-Tables/file-path-resolution.md), [verb table](../Scripts-And-Script-Commands/verb-table.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x001D6C60`](strong-and-weak-mode.md) | calls | [`0x001DA220`](../Game-Files-And-Data-Tables/prefetch-manifests.md) (on prefetch manifests)<br>[`0x001DADA0`](../Game-Files-And-Data-Tables/file-path-resolution.md) (on file path resolution) |
| [`0x00394070`](strong-and-weak-mode.md) | calls | [`0x0024A680`](../Game-Files-And-Data-Tables/handbook-files.md) (on handbook files) |
| [`0x00394460`](strong-and-weak-mode.md) | calls | [`0x001D6C60`](strong-and-weak-mode.md) |

**Saving, loading and settings** (explained on [resource arena and relocation](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md), [party data](../Party/party-data.md), [global state accessors](../Engine-Core/global-state-accessors.md), [save data fields](../Saving-Loading-And-Settings/save-data-fields.md), [saving and loading](../Saving-Loading-And-Settings/saving-and-loading.md), [item and ability ids](../Engine-Core/item-and-ability-ids.md), [party control modes](../Engine-Core/party-control-modes.md), [frame update order](../Engine-Core/frame-update-order.md), [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md), [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md), [standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md), [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [loading a save](../Saving-Loading-And-Settings/loading-a-save.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00233C10`](strong-and-weak-mode.md) | is called by | [`0x00280140`](../Items-Equipment-Shops-And-Licenses/bazaar.md) (on bazaar) |
| [`0x002EF640`](strong-and-weak-mode.md) | is called by | [`0x00280140`](../Items-Equipment-Shops-And-Licenses/bazaar.md) (on bazaar) |
| [`0x002EF650`](../Saving-Loading-And-Settings/loading-a-save.md) (on loading a save) | is called by | [`0x00280140`](../Items-Equipment-Shops-And-Licenses/bazaar.md) (on bazaar) |
| [`0x00229B40`](../Saving-Loading-And-Settings/save-data-fields.md) World transition snapshot: capture runtime state (on save data fields) | calls | [`0x002EF620`](../Saving-Loading-And-Settings/save-data-fields.md) (on save data fields)<br>[`0x002EF640`](strong-and-weak-mode.md) |
| [`0x00233C10`](strong-and-weak-mode.md) | calls | [`0x002EF640`](strong-and-weak-mode.md) |
| [`0x00236740`](strong-and-weak-mode.md) | is called by | [`0x00583D60`](../Saving-Loading-And-Settings/save-file-format.md) Save image: finalize header and checksum (on save file format) |
| [`0x00236760`](strong-and-weak-mode.md) | is called by | [`0x001C1720`](../Saving-Loading-And-Settings/saving-and-loading-autosave.md) (on saving and loading autosave)<br>[`0x002EF690`](../Party/party-data.md) Save image: copy capture to write submission buffer (on party data)<br>[`0x00583D60`](../Saving-Loading-And-Settings/save-file-format.md) Save image: finalize header and checksum (on save file format) |
| [`0x00236780`](strong-and-weak-mode.md) | is called by | [`0x00583D60`](../Saving-Loading-And-Settings/save-file-format.md) Save image: finalize header and checksum (on save file format) |
| [`0x00237DF0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) | is called by | [`0x00238A80`](../Items-Equipment-Shops-And-Licenses/bazaar.md) (on bazaar) |
| [`0x0023A390`](strong-and-weak-mode.md) | is called by | [`0x00584210`](../Saving-Loading-And-Settings/save-data-fields.md) Save load: normalize loaded runtime state and reseed rng (on save data fields) |
| [`0x002DDE60`](../Saving-Loading-And-Settings/game-settings.md) (on game settings) | is called by | [`0x00253A80`](../Saving-Loading-And-Settings/save-data-fields.md) Save runtime: initialize header and image backed state (on save data fields) |
| [`0x002EF640`](strong-and-weak-mode.md) | is called by | [`0x00238A80`](../Items-Equipment-Shops-And-Licenses/bazaar.md) (on bazaar)<br>[`0x00253A80`](../Saving-Loading-And-Settings/save-data-fields.md) Save runtime: initialize header and image backed state (on save data fields)<br>[`0x002EF2B0`](../Saving-Loading-And-Settings/save-data-fields.md) (on save data fields)<br>[`0x002EF2D0`](../Story-Events-And-Hunts/story-flags.md) (on story flags)<br>[`0x002EF300`](../Saving-Loading-And-Settings/save-file-format.md) (on save file format)<br>[`0x002EF370`](../Saving-Loading-And-Settings/save-data-fields.md) (on save data fields)<br>[`0x002EF390`](../Saving-Loading-And-Settings/save-data-fields.md) (on save data fields)<br>[`0x0057E310`](../Saving-Loading-And-Settings/saving-and-loading-autosave.md) Save write: prepare and submit full image (on saving and loading autosave)<br>[`0x00580CD0`](../Saving-Loading-And-Settings/saving-and-loading-screen.md) (on saving and loading screen)<br>[`0x00580EB0`](../Saving-Loading-And-Settings/saving-and-loading-screen.md) (on saving and loading screen)<br>[`0x005819F0`](../Saving-Loading-And-Settings/saving-and-loading-transaction.md) Save slot scan: controller callback (on saving and loading transaction)<br>[`0x00581B70`](../Saving-Loading-And-Settings/saving-and-loading-transaction.md) Save slot probe: storage completion callback (on saving and loading transaction) |
| [`0x002EF640`](strong-and-weak-mode.md) | is also called by | [`0x00581DA0`](../Saving-Loading-And-Settings/saving-and-loading-transaction.md) Save slot transaction: state machine (on saving and loading transaction)<br>[`0x00583C00`](gil.md) Save ui: restore active header from controller backup (on gil)<br>[`0x00583CB0`](../Saving-Loading-And-Settings/saving-and-loading-screen.md) Save ui: backup active header to controller cache (on saving and loading screen)<br>[`0x00583D60`](../Saving-Loading-And-Settings/save-file-format.md) Save image: finalize header and checksum (on save file format)<br>[`0x00584210`](../Saving-Loading-And-Settings/save-data-fields.md) Save load: normalize loaded runtime state and reseed rng (on save data fields)<br>[`0x005844A0`](../Saving-Loading-And-Settings/save-data-fields.md) Save transition: prepare runtime image for capture (on save data fields) |
| [`0x002EF650`](../Saving-Loading-And-Settings/loading-a-save.md) (on loading a save) | calls | [`0x00238A80`](../Items-Equipment-Shops-And-Licenses/bazaar.md) (on bazaar)<br>[`0x00253A80`](../Saving-Loading-And-Settings/save-data-fields.md) Save runtime: initialize header and image backed state (on save data fields)<br>[`0x002EF2D0`](../Story-Events-And-Hunts/story-flags.md) (on story flags) |
| [`0x00394130`](../Saving-Loading-And-Settings/loading-a-save.md) (on loading a save) | calls | [`0x00255260`](../Saving-Loading-And-Settings/loading-a-save.md) Save image: validate runtime format header (on loading a save)<br>[`0x002EF640`](strong-and-weak-mode.md)<br>[`0x002EF650`](../Saving-Loading-And-Settings/loading-a-save.md) (on loading a save) |
| [`0x00583D60`](../Saving-Loading-And-Settings/save-file-format.md) Save image: finalize header and checksum (on save file format) | calls | [`0x002EF620`](../Saving-Loading-And-Settings/save-data-fields.md) (on save data fields)<br>[`0x002EF640`](strong-and-weak-mode.md)<br>[`0x003BB220`](../Saving-Loading-And-Settings/save-file-format.md) Crc32: compute (on save file format) |
| [`0x00583D60`](../Saving-Loading-And-Settings/save-file-format.md) Save image: finalize header and checksum (on save file format) | is called by | [`0x00581DA0`](../Saving-Loading-And-Settings/saving-and-loading-transaction.md) Save slot transaction: state machine (on saving and loading transaction)<br>[`0x005844A0`](../Saving-Loading-And-Settings/save-data-fields.md) Save transition: prepare runtime image for capture (on save data fields) |

**Scripts and script commands** (explained on [party verbs](../Scripts-And-Script-Commands/party-verbs.md), [starting inventory](../Party/starting-inventory.md), [native commands](../Scripts-And-Script-Commands/native-commands.md), [force fight mode](../Engine-Core/force-fight-mode.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00236740`](strong-and-weak-mode.md) | is called by | [`0x0050F3F0`](strong-and-weak-mode.md) |
| [`0x00236760`](strong-and-weak-mode.md) | is called by | [`0x0050F540`](strong-and-weak-mode.md) |
| [`0x0023A2C0`](strong-and-weak-mode.md) | is called by | [`0x0050F3C0`](strong-and-weak-mode.md) |
| [`0x0023A390`](strong-and-weak-mode.md) | is called by | [`0x0050F500`](strong-and-weak-mode.md) |
| [`0x003172E0`](../Party/party-members.md) Party configuration: add selector00 to06 to available index4 to8 (on party members) | is called by | [`0x0034C370`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs) |
| [`0x00394430`](strong-and-weak-mode.md) | is called by | [`0x005120E0`](strong-and-weak-mode.md) |
| [`0x00394460`](strong-and-weak-mode.md) | is called by | [`0x00511EA0`](strong-and-weak-mode.md) |
| [`0x0050F3F0`](strong-and-weak-mode.md) | calls | [`0x0026B4E0`](../Scripts-And-Script-Commands/verb-dispatch.md) (on verb dispatch) |
| [`0x0050F810`](strong-and-weak-mode.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x005120E0`](strong-and-weak-mode.md) | calls | [`0x0026B4E0`](../Scripts-And-Script-Commands/verb-dispatch.md) (on verb dispatch) |

**Enemy spawning** (explained on [enemy respawning](../Enemy-Spawning/enemy-respawning.md), [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00229B40`](../Saving-Loading-And-Settings/save-data-fields.md) World transition snapshot: capture runtime state (on save data fields) | calls | [`0x00233440`](../Saving-Loading-And-Settings/save-data-fields.md) Spawn keep: serialize persistence banks (on save data fields) |
| [`0x002342F0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) | calls | [`0x00233780`](../Enemy-Spawning/enemy-respawning.md) Spawn: swap or push banks (on enemy respawning)<br>[`0x00307090`](../Enemy-Spawning/enemy-respawning.md) Spawn group: reset lifecycle ledger (on enemy respawning) |
| [`0x0030C470`](stat-growth-per-level.md) (on stat growth per level) | is called by | [`0x002398F0`](../Scripts-And-Script-Commands/reward-verbs.md) (on reward verbs) |

**Status effects and KO** (explained on [battle units](../Characters-And-Objects/battle-units.md), [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [force fight mode](../Engine-Core/force-fight-mode.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002342F0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) | calls | [`0x0030E990`](../Status-Effects-And-KO/status-changes.md) (on status changes) |
| [`0x0030C470`](stat-growth-per-level.md) (on stat growth per level) | calls | [`0x0030F690`](../Damage-And-Battle-Formulas/augments.md) Battle stats: remove statuses from mask and recompute (on augments)<br>[`0x0030FED0`](../Items-Equipment-Shops-And-Licenses/equipping-an-item.md) Battle stats: recompute derived state and auto statuses (on equipping an item) |
| [`0x00312280`](strong-and-weak-mode.md) Battle unit: process defeat rewards and loot | is called by | [`0x0030E360`](../Engine-Core/identifier-spaces.md) Battle stats: change status and process side effects (on identifier spaces) |

**Story, events and hunts** (explained on [identifier spaces](../Engine-Core/identifier-spaces.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00583D60`](../Saving-Loading-And-Settings/save-file-format.md) Save image: finalize header and checksum (on save file format) | calls | [`0x0032A8A0`](../World-Areas-And-Travel/zone-asset-list.md) Persistent flag: query primary or authored threshold gate (on zone asset list) |

**Menus and HUD** (explained on [party control modes](../Engine-Core/party-control-modes.md), [config screen](../Menus-And-HUD/config-screen.md), [stats](../Damage-And-Battle-Formulas/stats.md), [resource arena and relocation](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md), [inventory](../Items-Equipment-Shops-And-Licenses/inventory.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00237DF0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) | calls | [`0x00313840`](../Engine-Core/party-control-modes.md) (on party control modes) |
| [`0x0023FBE0`](strong-and-weak-mode.md) | calls | [`0x0023ED80`](../Menus-And-HUD/config-screen.md) (on config screen)<br>[`0x00291D80`](../Menus-And-HUD/dialogs.md) (on dialogs) |
| [`0x002B9FD0`](strong-and-weak-mode.md) | is called by | [`0x0027FB70`](../Story-Events-And-Hunts/tutorials-scenes.md) (on tutorials scenes)<br>[`0x0028F8B0`](../Menus-And-HUD/hud.md) (on hud) |

**World, areas and travel** (explained on [force fight mode](../Engine-Core/force-fight-mode.md), [script variables](../Scripts-And-Script-Commands/script-variables.md), [changing areas](../World-Areas-And-Travel/changing-areas.md), [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md), [party control modes](../Engine-Core/party-control-modes.md), [loading a save](../Saving-Loading-And-Settings/loading-a-save.md), [debug menu](../Engine-Core/debug-menu.md), [game over](../World-Areas-And-Travel/game-over.md), [menu map files](../Game-Files-And-Data-Tables/menu-map-files.md), [area flags navimapdata](../World-Areas-And-Travel/area-flags-navimapdata.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002342F0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) | is called by | [`0x00266D10`](../Engine-Core/frame-update-order.md) (on frame update order) |
| [`0x00229B40`](../Saving-Loading-And-Settings/save-data-fields.md) World transition snapshot: capture runtime state (on save data fields) | calls | [`0x0025D8E0`](../Saving-Loading-And-Settings/save-data-fields.md) World persistence: export group persistent bank (on save data fields) |
| [`0x00229B40`](../Saving-Loading-And-Settings/save-data-fields.md) World transition snapshot: capture runtime state (on save data fields) | is called by | [`0x003145E0`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) World transition: stage field transition (on zone changes and mapjump) |
| [`0x002342F0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) | calls | [`0x002FA520`](../Scripts-And-Script-Commands/reward-verbs.md) (on reward verbs)<br>[`0x00377C20`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes) |
| [`0x00236760`](strong-and-weak-mode.md) | is called by | [`0x003145E0`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) World transition: stage field transition (on zone changes and mapjump)<br>[`0x005843E0`](../World-Areas-And-Travel/chocobos-and-airships.md) World transition snapshot: restore persistence pair for active slot (on chocobos and airships)<br>[`0x00584580`](../Saving-Loading-And-Settings/save-data-fields.md) World transition snapshot: capture persistence pair for active slot (on save data fields) |
| [`0x00239960`](../Party/scenario-presets.md) (on scenario presets) | is called by | [`0x002342F0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) |
| [`0x002EF640`](strong-and-weak-mode.md) | is called by | [`0x00229B40`](../Saving-Loading-And-Settings/save-data-fields.md) World transition snapshot: capture runtime state (on save data fields)<br>[`0x003145E0`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) World transition: stage field transition (on zone changes and mapjump)<br>[`0x005843E0`](../World-Areas-And-Travel/chocobos-and-airships.md) World transition snapshot: restore persistence pair for active slot (on chocobos and airships) |
| [`0x00312280`](strong-and-weak-mode.md) Battle unit: process defeat rewards and loot | calls | [`0x00377C20`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes) |
| [`0x00329CC0`](strong-and-weak-mode.md) Battle slot map: initialize mapping classes | calls | [`0x003148F0`](../World-Areas-And-Travel/treasure-chests.md) World transition: get active or pending field id (on treasure chests) |
| [`0x00394130`](../Saving-Loading-And-Settings/loading-a-save.md) (on loading a save) | calls | [`0x00267C90`](../Saving-Loading-And-Settings/loading-a-save.md) (on loading a save)<br>[`0x00268320`](../World-Areas-And-Travel/weather.md) World persistence: reset banks and mark initialization state (on weather)<br>[`0x00314440`](../World-Areas-And-Travel/changing-areas.md) (on changing areas)<br>[`0x00314DC0`](../Saving-Loading-And-Settings/loading-a-save.md) World transition: set active or pending field id (on loading a save) |
| [`0x0057FB00`](strong-and-weak-mode.md) | calls | [`0x00264F90`](../World-Areas-And-Travel/zone-asset-list.md) Map ref: get persistence group id (on zone asset list)<br>[`0x003778B0`](../World-Areas-And-Travel/zone-asset-list.md) (on zone asset list) |
| [`0x00583D60`](../Saving-Loading-And-Settings/save-file-format.md) Save image: finalize header and checksum (on save file format) | calls | [`0x00264F90`](../World-Areas-And-Travel/zone-asset-list.md) Map ref: get persistence group id (on zone asset list)<br>[`0x003148F0`](../World-Areas-And-Travel/treasure-chests.md) World transition: get active or pending field id (on treasure chests) |

</details>
