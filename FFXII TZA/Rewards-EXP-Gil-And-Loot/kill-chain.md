[Home](../../README.md) / [Rewards: EXP, LP, gil and loot](README.md) / Kill chain

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Kill chain: chain count, chain level, the chain coin and resets | system | Rewards: EXP, LP, gil and loot | EXP, loot and progression | How kills build the chain count and chain level, the 5 %/60 % coin rolled on every link, breaks in a row, everything that resets the chain (save crystals, towns, presets), the HUD counter and the chain's globals. | 0x00317ED0, 0x003183D0, 0x0028EF00, 0x0028EF70, 0x003F9E50 |

## What the player sees

Kill the same kind of enemy twice in a row and the **chain** counter goes up; kill a different kind
and the chain breaks. "The same kind" means the same enemy class: one byte on the enemy, compared with
the class of the previous kill, so the whole chain state is "what did I kill last".

Breaking a chain is not simply a reset. The game counts **breaks in a row** - kills of different kinds
one after another, which modding tools call the **reverse chain** - and while that count is above zero
it picks the drop-chance table by a weighted roll instead of by chain level. Any kill that continues a
chain sets the count back to zero.

On every kill that continues a chain the game also flips a **coin**, and the odds depend on how the
previous flip landed: 5 % after a failure, 60 % after a success. A long run of failures stays at 5 %;
one success moves it to 60 % until the next failure. The coin is independent of chain length. While it
is up, the chain number on screen pulses grey.

The chain number shown stops at 999 in every language: the stored length stops at 998 and the display
adds 1.

The chain also has a **level**, 0 to 3, and the level is what improves drops. It rises when enough
kills have been added since the last rise; picking up loot in the meantime makes the next rise less
likely, unless the coin is up.

Everything resets when you touch a save crystal, when you enter an area flagged as a town (towns,
villages, shops, aerodromes and similar safe areas), and when a script applies a preset party and
inventory state. Moving between ordinary areas keeps the chain.

Whether an area counts as a town is a flag in the field record file `navimapdata.bin`, and a save crystal's talk
script asks for the reset. The chain's level, its run of kills of one quantity group and its breaks in a row are what the loot
roll reads to choose drop chances and quantities.

## How it works

`EnemyChain_UpdateOnDefeat` (`0x00317ED0`, 529 bytes) has one caller, the defeat-reward routine
`0x00312280`, which calls it (`0x003122CD`) only when the defeated unit's stats record (`[unit+0x698]`) has
byte `+0x05` equal to 1 (an enemy) and the credited unit's record has byte `+0x05` equal to 0 (the
party side) (`0x003122B9`-`0x003122C8`). The function checks the enemy side again: it does nothing for a
null actor, for a missing stats record or one whose byte `+0x05` is not 1 (`0x00317EF8`), or when bit `0x2`
of byte `+0x28` of the actor's `[actor+0xE68]` record is set (`0x00317F09`).

It compares the enemy's class byte `actor+0x56` with the previous kill's class at `0x022C3168`
(`0x00317F21`). The class byte is the class row's byte `+0x05`, not its type byte `+0x04`
([Bestiary](../Enemy-Spawning/bestiary.md)). Word bank 14 names 64 classes; the 954 class rows of
the shipped areas use 55 of those values (0 to 63 apart from 9, 21, 47 to 52 and 60), a count of the shipped
data and not a limit of the engine.

### First kill

When `0x022C3168` is negative (`0x00317F1B`) there is no chain yet. The update clears the coin bit and
stores the class (`0x003180BB`-`0x003180D0`).

### Same class - the chain continues

When the class matches, the chain continues (`0x00317F2D`-`0x00318065`):

1. Chain length `0x022C315C` += 1, capped at 999 (`0x3E7`), or at 998 (`0x3E6`) when `0x00229E40()` is
   non-zero (`0x00317F2D`-`0x00317F64`). `0x00229E40` returns the locale id at `0x01E02814`, which is never 0
   in the shipped game: `0x0017E270` maps every language code, Japanese included, to an id of 1 or
   more (see the [languages page](../Saving-Loading-And-Settings/languages.md)), so the cap is 998 and the
   999 arm never runs.
2. Breaks in a row `0x022C3164` = 0 (`0x00317F6A`).
3. The quantity-group run `0x022C3160`: if the `u16` at `[actor+0xE68]+0x40` (the class row's quantity
   group, `model_family` in the [bestiary](../Enemy-Spawning/bestiary.md)) equals the previous
   one at `0x022C316C`, `run = min(run + 1, 999)`; otherwise it resets to 0 and stores the new group
   (`0x00317F70`-`0x00317FB6`). This run chooses the loot quantity table.
   - The group is not the model: the bound model id is the class row's `+0x00`. Coeurl and Grimalkin
     are both model `m1014` (`0x006D0014`) and class 5, with groups `0x0226` and `0x139A`, so after a run
     of Coeurl kills a party kill of a Grimalkin continues the chain but resets this run to 0.
   - Only this step stores a group: `0x00317FB6` is the one RIP-relative write to `0x022C316C`, beside
     the reset's -1 through `0x022C3168` (`0x003183BE`). The first-kill path (`0x003180BB`-`0x003180D0`) and the
     break path (`0x0031806C`-`0x003180B5`) leave it.
   - After a reset (`0x022C316C` = -1, `0x003183BE`) the first kill stores only the class, the second
     stores the group and leaves the run at 0, and each further kill of the same class and group
     adds 1, so kill *n* of such a run leaves it at *n* - 2, up to the cap of 999.
4. `EnemyChain_TryAdvanceRank` (`0x003183D0`, 315 bytes) tries to raise the chain level (`0x00317FBC`); see
   below.
5. The coin: three LCG steps on the shared gameplay generator `0x022C256C` (multiplier `0x41C64E6D`,
   increment `0x3039`) give `r` in 0-99 (`0x00317FC1`-`0x00318032`). If coin bit `0x1` of `0x022C3178` is set,
   success is `r >= 40` (60 %); otherwise success is `r < 5` (5 %) (`0x00318034`-`0x00318048`).
6. `0x0028EF70(length, coin, level)` posts the update to the chain display, adding 1 to the length passed
   when `0x00229E40()` is non-zero (`0x0031804B`-`0x00318065`), which it always is, so the display shows
   the stored length plus one.
7. The coin result becomes the new bit `0x1` of `0x022C3178` (`0x003180BB`-`0x003180C6`), and the class is stored.

### Different class - the chain breaks

When the class differs, the chain breaks (`0x0031806C`-`0x003180B5`):

1. `0x0028EF00(length, level)` posts the break to the display (again the stored length plus one).
2. Breaks in a row `0x022C3164` += 1, capped at 999.
3. Zeroed together: `0x022C3170`/`0x022C3174` (one qword store, `0x00318091`), chain level `0x022C3158` and
   length `0x022C315C` (one qword store, `0x00318098`), and the quantity-group run `0x022C3160`.
4. The coin bit is cleared and the class stored (`0x003180BB`-`0x003180D0`). The break path draws nothing.

### The level rise

`0x003183D0` decides whether the level rises. Nothing happens at level 3 (`0x003183ED`). Otherwise,
with `d = length - 0x022C3170`, the kills added since the last rise:

1. If `d` is above the level's threshold at `0x00D107D4` (30, 50, 80 for levels 0, 1, 2) the level
   rises outright (`0x00318403`-`0x00318417`).
2. If not, and the coin is down, `d` is reduced by `(level + 1) * 0x022C3174`, the loot pickups since
   the last rise (`0x0031841D`-`0x00318431`).
3. `d` is clamped to 0-10, a fresh three-step LCG roll `r` in 0-99 is taken, and the level rises
   when `r` is below the byte at `0x00D106F8 + level*11 + d` (`0x0031844A`-`0x003184D7`):

| `d` | 0-5 | 6 | 7 | 8 | 9 | 10 |
|---|---:|---:|---:|---:|---:|---:|
| level 0 | 0 % | 40 % | 60 % | 80 % | 90 % | 100 % |
| level 1 | 0 % | 20 % | 30 % | 50 % | 60 % | 100 % |
| level 2 | 0 % | 10 % | 20 % | 30 % | 40 % | 100 % |

On a rise: level += 1, `0x022C3170` = the current length, `0x022C3174` = 0, and `0x0028EF50(level)` tells the
display (`0x003184D9`-`0x003184F6`). The pickup count `0x022C3174` is incremented by every loot pickup
(`0x00319974`).

### Reset

`0x003183A0` (42 bytes) clears the coin bit and zeroes `0x022C3158`-`0x022C3167` and `0x022C3170`-`0x022C3177` with qword stores
(`0x003183A9`-`0x003183BE`), and sets `0x022C3168` and `0x022C316C` to -1 (`0x003183A0`-`0x003183BE`). It is reached
four ways:

1. **Save crystals.** The script verb `btladjustsystem` (`0x517`, handler `0x0034AAB0`) passes its
   argument to `0x002FEAC0`, which jumps to `0x003183A0` when bit `0x1` is set (`0x002FEAC3`). The save crystal's
   talk function calls `btladjustsystem(1)` (see [teleport and save crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md)).
2. **Entering a town.** The area initialisation `0x002342F0` resets the chain (`0x0023444F`) when the town flag is
   set (see the town reset below).
3. **A preset party state.** `0x002342F0` calls `0x00239960` (`0x00234349`), which consumes the pending
   preset byte `0x0208D455` and sets it back to -1 (`0x00239966`-`0x0023997B`). For a preset index in range
   it applies that preset and calls `0x003183A0` (`0x00239A85`); for -2 it jumps to `0x00237DF0` instead
   (`0x0023998E`), which resets the chain at `0x00237E3C`; for -1 it does nothing.
4. **The battle-state reset** `0x00237DF0`, which also runs from `0x00233C10` (three calls), `0x00238A80`
   and `0x00394460`.

The pending preset byte `0x0208D455` is written by the script verb `btlAtelSetNextSetSaveData`
(`0x0050F810`), by `0x0023A110` (called from `0x003942F9`), from the save image's `+0x4E660` when a save is
restored (`0x00584482`), and to -1 by `0x002368D0`.

### The town reset

When the new area's actor manager 0 finishes loading, `0x00332130(0)` calls `0x0032F1B0(0)`, which calls
`0x0026CE60(0)`; that runs once per load (manager byte `+0x10` bit `0x1` clear and byte `+0x13` set) and
calls the area initialisation `0x002342F0` (`0x0026CEC6`). `0x002342F0` is also called by `0x00266D10`
(`0x00267136`). It does nothing unless `0x02089300` is non-zero (`0x002342F4`; set to 1 at `0x00236A44`,
cleared by the battle-work setup `0x002368D0`).

Near its end `0x002342F0` calls `0x00377C20` and resets the chain only when that returns non-zero
(`0x00234446`-`0x0023444F`). `0x00377C20` returns bit `0x8000` of the 16-bit word at `+8 + id*3` in the map-info
table `0x02ADD100` (`navimapdata.bin`), where `id` is the current field id from the save payload's
`+0x1044` (`0x003148F0`, negative ids read as 0). It returns 0 for an id at or past the table's count
at `+4`, or when the table is absent. Bit `0x8000` is the town flag (see
[the field record table](../World-Areas-And-Travel/area-flags-navimapdata.md)).

### Script access

The script verb `btlAtelGetChainCount` (`0x00510100`) returns the breaks in a row for
argument 0 (`0x00318380`), the chain length for 1 (`0x00318390`), and -1 otherwise. The script verb
`btladjustsystem` clears the chain when bit `0x1` of its argument is set ([Reset](#reset)).

### The display

The chain counter is a widget in the HUD sub-object at `+0x57E0`. The HUD keeps chain flags at
`+0x7C7C`, the pending count at `+0x7C78` and the level at `+0x7C82`.

- `0x0028EF00` (79 B), the break or continue notice, resets the flags to bits `0x8` and `0x1` and stores the
  pending count and level.
  - It writes the flags through the HUD pointer `0x0209BE80` (`0x0028EF07`-`0x0028EF26`) before its null test
    (`0x0028EF34`), which guards only the count and level.
  - The pointer is written only by `0x0028F8B0`, with the `0x10FD0`-byte block `0x00271420` returns
    (`0x0028F8CA`-`0x0028F8D4`), and cleared only by the teardown `0x0028F2F0` that `0x0028F8B0` runs first (`0x0028F8B4`,
    `0x0028F554`). `0x0028F8B0` runs once, at startup: its one call chain is `0x0022A0B0` (`0x0022A415`), `0x00253970`
    (`0x002539C5`), `0x0035C560` (`0x0035C57F`).
- `0x0028EF70` (70 B) calls `0x0028F0C0(length)`, keeps the other flags, sets bit `0x2` to the coin's bit `0x1` and
  stores the level at `+0x7C82` (`0x0028EF7F`-`0x0028EFA9`).
- `0x0028F0C0(count)` does nothing while the manager `[0x0209BE80]` is null (`0x0028F0C6`-`0x0028F0D2`). For a
  count other than 0 it reports achievement index 18 with the count, stores the count's low word at
  `+0x7C78`, sets bit `0x1` of the dword `+0x7C7C` and clears its bit `0x8` (`0x0028F0DC`-`0x0028F10B`).

  For 0 it stores 0 at `+0x7C78` and clears bits `0x8` and `0x1` (`0x0028F118`-`0x0028F136`), then releases
  with `0x00244F00` each of three parts that `0x00273A20` answers non-zero for: `+0x57E0` when bit `0x1`
  of the byte `+0x58A4` is clear, `+0x58B0` when the word `+0x5972` is 0 and `+0x5980` when the word
  `+0x5A42` is 0 (`0x0028F13D`-`0x0028F1D8`).
- `0x0028EF50(level)` (29 B), called on a level rise, sets flag bit `0x4` and stores the new level at `+0x7C82`
  (`0x0028EF50`-`0x0028EF65`).

The widget update `0x003F9F40` reads those flags each frame:

- Flag bit `0x2` is copied into the widget's `+0xC4` bit `0x2` (`0x003FA069`-`0x003FA07E`), which makes the
  number redraw every frame in a pulsing grey.
- `0x003F9E50(widget, count, playSound)` (229 B) returns 1 at once for a count of 0, drawing nothing and
  leaving the widget as it is (`0x003F9E67`-`0x003F9E69`), does not show a
  count of 1 (the test is on `0x00229E40()` being non-zero, which it always is), and otherwise draws
  `min(count, 999)` in three digits (unsigned compare), playing sound `0x30` when asked.
- Before drawing, `0x003F9E50` builds the widget in place with `0x00245000(widget, 0xD0, 0x003FAF10, 0)` and opens it
  (`0x00246AC0`) when its first qword is 0 (`0x00273A20`); for a built widget whose `+0xC4` has bit `0x1` or `0x4` set
  it returns 0 and draws nothing (`0x003F9E81`-`0x003F9EC8`). The sound comes with the descriptor `0x00D11FA0`
  (`0x00247570`), and the count is kept at `+0xC8` with `+0xC0` = 0 (`0x003F9ECD`-`0x003F9F1B`). It returns 1
  (`0x003F9F25`).
- With flag bit `0x4` set, it counts frames at widget `+0x24A0` and, once the count passes 15 times the
  frame base `0x01DFE0B4`, starts a second element at widget `+0xD0` with the handler `0x003FACF0` and
  clears the bit (`0x003F9F51`-`0x003F9FB5`).
- The second element is started only while its slot at `+0xD0` is empty (`0x00273A20`);
  the frame count goes back to 0 and the bit is cleared either way (`0x003F9F76`-`0x003F9FB5`).
- Flag bit `0x10` starts a third element at widget `+0x1A0` with the handler `0x003FC3F0`
  in the same way and is cleared only when it does (`0x003F9FBC`-`0x003F9FFD`).
- The count is redrawn when it differs from the drawn count `+0x249A` and is not 0, or
  when flag bit `0x1` is set; `playSound` is flag bit `0x8` (`0x003FA004`-`0x003FA040`). A
  redraw that answers 0 sets flag bit `0x1` for the next frame (`0x003FA146`).
- A redraw that answers 1 clears flag bits `0x1`, `0x2` and `0x8`, puts flag bit `0x8`
  into the widget's `+0xC4` bit `0x4` beside bit `0x2`, and copies the count to `+0x249A`
  (`0x003FA04D`-`0x003FA08B`).
- In the same frame, with `+0xC4` bit `0x2` set, it draws the kept count `+0xC8` with
  `0x0029F6E0`, in a colour whose three colour bytes are what `0x00296F50(0x40, 0x80, 0)`
  answers and whose fourth byte is `0x80` (`0x003FA0EC`-`0x003FA136`).

That second element is a one-shot sprite: on creation it takes element `0x59` of the layout at
`0x00D11FC8` and sits at the counter's x position; it plays sound `0x6C` (`0x00249C60`) and removes
itself after 30 times the frame base (`0x003FACF0`).

The handler takes messages 1 (creation), 2 (the frame count), 3 (the draw), 14 (the
sound) and 15, and passes any other to `0x005C5230` (`0x003FACFB`-`0x003FAD28`). Message 15
stores 1 in the word `+0xC2`, and the frame count `+0xC0` stops while that word is not 0
(`0x003FAD2D`-`0x003FAD35`, `0x003FAE41`-`0x003FAE49`).

The draw reads the picture entry of the element, stores at the draw record's `+0x5C`
the layout's palette-table byte for the high four bits of the entry's byte `+0x07` plus
that byte's low four bits (`0x003FADE1`-`0x003FAE0C`), and makes the record's alpha word
`+0x58` `(alpha * 100) >> 7` for the
call of `0x002D8C80`, putting the old value back after it (`0x003FAD59`-`0x003FAE35`).

When the count is redrawn and is non-zero (unless widget `+0xC4` bit `0x4` was set before the redraw and
still is, `0x003FA092`-`0x003FA0AB`), the digits take their colour from the colour table
`0x0215E6C8` (`0x002DD7E0`, grey `0x80808080` when the table is absent): entry `0xC0`, `0xC1` or `0xC2`
for levels 1-3 and `0xBF` for level 0 (`0x003FA0AD`-`0x003FA0DD`), applied to the three digits by
`0x003FAAF0`, so the number's colour shows
the chain level.

### The coin and loot share one generator

The coin's three LCG steps advance the same state
`0x022C256C` the loot rolls use, so the two are correlated through that state. The clock-based seed
computed when a save loads (`0x00584210`, see [boot fixups](../Engine-Core/startup-constants.md))
goes to a different generator, the Mersenne Twister whose state starts at `0x02EB3870` (624 words, index
`0x02EB4230`), seeded through `0x00863D30` (reached by the thunk `0x00379CF0`): its first use seeds 5489 and
then the clock value (`0x00863D4D`-`0x00863D6A`). It does not touch `0x022C256C`.

## State

| Global | Width | Meaning | Written by |
|---|---|---|---|
| `0x022C3158` | `u32` | chain level 0-3 | `0x003183D0` (rise); zeroed on a break (`0x00318098`) and by the chain reset (`0x003183B7`) |
| `0x022C315C` | `u32` | chain length, cap 999 or 998 | `0x00317F64`; zeroed on a break (`0x00318098`) and by the chain reset (`0x003183B7`) |
| `0x022C3160` | `u32` | quantity-group run, cap 999 | `0x00317F70`-`0x00317FB6`; zeroed on a break (`0x0031809F`) and by the chain reset (`0x003183B0`) |
| `0x022C3164` | `u32` | breaks in a row, cap 999 | `0x003180B5`; zeroed by a continuing kill (`0x00317F6A`) and by the chain reset `0x003183A0` (`0x003183B0`, a qword store from `0x022C3160`) |
| `0x022C3168` | `i32` | previous kill's class byte; negative before the first kill | `0x003180D0`; `0x003183BE` (-1) |
| `0x022C316C` | `u32` | quantity group (class row `+0x40`) stored by the last continuing kill whose group differed from it; -1 after a reset | `0x00317FB6`; `0x003183BE` (-1) |
| `0x022C3170` | `u32` | chain length at the last level rise | `0x003184DC`; zeroed on a break (`0x00318091`) and by the chain reset (`0x003183A9`) |
| `0x022C3174` | `u32` | loot pickups since the last level rise | `0x00319974` (+1); `0x003184EC` (0); zeroed on a break (`0x00318091`) and by the chain reset (`0x003183A9`) |
| `0x022C3178` | `u32` | bit `0x1`: the coin | `0x003180C6`; bit `0x1` cleared by the chain reset (`0x003183A0`) |

Of the instructions that address `0x022C3158`-`0x022C317B`, every write is in `0x00317ED0`, the chain reset `0x003183A0`, the
level rise `0x003183D0` or `0x00319920`, whose write is the pickup count (`0x00319974`).

## Modding notes

- The coin's odds are the two immediates at `0x0031803D` (`cmp ecx, 0x28`: success on 40-99) and
  `0x00318045` (`cmp ecx, 5`: success on 0-4).
- The coin's effect: while bit `0x1` of `0x022C3178` is set, loot pickups do not slow the level rise
  (`0x0031841D`).
- The level thresholds (`0x00D107D4`) and the rise chances (`0x00D106F8`) are tables in the executable, not
  in game data.
- The 999 / 998 cap is chosen by locale, not by data.
- To change what the chain does to drops, see [Loot drops](loot-drops.md):
  level, the quantity-group run and breaks in a row each select a row of the drop table.

## Related

- [Loot drops](loot-drops.md) - how chain level, the quantity-group
  run and breaks in a row choose drop chances and quantities.
- [Teleport and save crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md) - the
  crystal script that resets the chain.
- [The field record table](../World-Areas-And-Travel/area-flags-navimapdata.md) -
  the town flag that resets the chain on entry.
- [Language selection and locale ids](../Saving-Loading-And-Settings/languages.md)
- [Who gets EXP, LP and gil from a kill](exp-lp-and-level-ups.md) - the
  defeat-reward routine that calls the chain update.

---

[← EXP, LP and level-ups from kills](exp-lp-and-level-ups.md) | [Loot drops →](loot-drops.md)
