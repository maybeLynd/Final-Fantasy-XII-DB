[Home](../../README.md) / [Story, events and hunts](README.md) / Language-tree script differences

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Language-tree script differences: what each code change outside the English scripts does in the game | reference | Story, events and hunts | Scripts across all areas | Every place where the code of a zone or scene script in one of the other eight language trees (in, kr, cn, ch, fr, de, it, es) differs from the us script: the seven kinds of change, what each verb does, what the changed values move or switch on screen, and why the tree needs it. | 0x00343610, 0x003E9570, 0x003405C0, 0x003E9320, 0x002A7950, 0x00347830, 0x002EBBB0, 0x0034A090, 0x00349800, 0x00348DF0, 0x0034D920, 0x00355570, 0x002650B0, 0x002642C0, 0x00355A00, 0x00355930, 0x0026B4E0, 0x0016D6A0, 0x00354EF0, 0x003603E0, 0x0034E340, 0x00473E80, 0x003458D0, 0x00379430, 0x0033FED0, 0x00229E40 |

## What it lists

The game ships its zone and scene scripts once per language, in nine trees under `plan_master`: `us` (English),
`in` (Japanese: the Japanese language loads the `in` tables, see [languages](../Saving-Loading-And-Settings/languages.md)),
`kr`, `cn`, `ch`, `fr`, `de`, `it` and `es`. Almost every script is the same code in every tree, with its own text.

The table [script-language-differences.tsv](script-language-differences.tsv) has one row for each place where a
tree's code differs from the `us` script: 2,328 rows in 181 scripts. Each row says which trees carry the change, what
the code was in `us` and what it is in those trees, which kind of change it is, and what it does in the game.

| Kind | Rows | Trees | Scripts | What changes in the game |
|---|---:|---|---:|---|
| `picture-position` | 1,806 | `it` 1,130, `es` 648, `de` 17, `fr` 11 | 154 | the screen position of a part of an on-screen picture, so that the tree's own wording fits |
| `distance-culling` | 392 | `kr, cn, ch` | 12 | character distance culling is switched back on when control returns to the player |
| `message-window` | 71 | `in` 29, `cn, ch` 29, all eight 13 | 16 | where an icon window opens: its height, or its message slot |
| `demo-build` | 46 | `kr, cn, ch` | 8 | code for a build that ends early (closed passages, a thank-you page); none of it runs |
| `capture-reference` | 11 | `in, kr, cn, ch` 10, `it` 1 | 5 | nothing: the same actor name sits at a different offset |
| `sign-record` | 1 | `in` | 1 | nothing: an extra field-sign record that no code reads |
| `script-only` | 1 | `kr, cn` | 1 | nothing: a second title-screen script that no build loads |

Changes in text, and changes that only move code without changing it, are not rows.

## Columns

| Column | Holds |
|---|---|
| `group` | the script's group, the first three letters of its name (`rbl`, `tri`, `evt` and so on) |
| `script` | the script, by the name of its `.ebp` file without the extension |
| `function` | `actor.function` of the changed code; `file scope` for a table outside every function |
| `us_lines` | the lines of the `us` listing that change, or `before N` for code the tree inserts before `us` line N |
| `change` | `changed` (the tree has other code), `added` (the tree has extra code), or `script only in these trees` |
| `trees` | the trees that carry exactly this change, in the order `in, kr, cn, ch, fr, de, it, es` |
| `tree_lines` | the matching lines of the first listed tree's listing |
| `us_text` | the `us` code, `-` for added code |
| `tree_text` | the code in those trees |
| `calls` | the verbs and script functions the changed code calls |
| `kind` | the kind of change, one of the seven of the table above |
| `meaning` | what the change does in the game, in that tree |
| `area_page` | the area pages of this folder that cover the script's group, `-` when no area page does |

The listings name a verb without a name of its own `verb_0x<id>`, its call id; the `Data` sections below say what each
such verb does from its native body. The table of `frs_b02` is named `signRecords`, after the verb that reads it. A
listing's bitwise OR is written `bitor`.

## Data

### Picture positions (`picture-position`)

`setshapepos_183` (`0x183`, `0x00343610`) places one part of a picture window. It pops five values and calls
`0x003E9570(window, part, x, y, centre)`, which writes x and y as words to `+0x10` and `+0x12` of the part's record,
`part × 0x60` into the part array that the window object's `+0x3F8` points to, and bit `0x2` of `+0x08` from bit
`0x1` of `centre` (`0x003E959D`-`0x003E95C0`).

`0x003E9570` changes nothing when the message slot (`0x002E1040`, 0 to 7) holds no window object or the part is not
below the slot's word `+0x54` (`0x003E9588`-`0x003E959B`). Every row of this kind passes `centre` 0, so x and y are
the top-left corner of the part, in the 1920 × 1080 window that `shapewin(3, 0, 0, 0x0780, 0x0438, 0)` opens.

`setshape` (`0x17E`, `0x003405C0` → `0x003E9320`) chooses the frame a part shows. The frames are cut from the picture
block in the script's own reference area, so each tree draws its own wording: the block's frame table gives each
frame's corner and size in a TIM2 image that follows it.
`0x003405C0` calls `0x002640C0` before it pops anything and passes the answer as the first
argument of `0x003E9320`; the four ints follow in the reverse of the order popped
(`0x003405DD`-`0x0034061A`).

`0x002A7950`, which `registshape` runs while the context's `+0xB8` is empty (`0x003E92F6`-`0x003E930D`), takes the
block's address, not the image's: it keeps `block + 0x10` and `block + 0x10 + [block + 4]` in the first free of
the eight picture slots at `0x0209C510` (-1 when all eight are taken) and loads from `block + 0x10 + [block + 4] +
[block + 8]` through `0x0024A440`, the last two sums made in 32 bits (`0x002A7970`-`0x002A79CE`).

The image is registered with `0x0024A440(address, [0x01E0C270], 2)` and the answer is
kept at the slot's `+0x08` (`0x002A7996`-`0x002A79B7`).

`0x003E9320` changes nothing but the slot's `+0x4C` when the slot holds no window, no picture is registered (the
context's `+0xB8`) or the part is not below the slot's word `+0x54` (`0x003E934F`-`0x003E9371`, `0x003E941D`). After it
sets the frame it puts the part at x 0, y 0 with bit `0x2` of `+0x08` set, through `0x003E9570(window, part, 0, 0,
1)`, and sets bit `0x1` of `+0x08` (`0x003E93D5`-`0x003E9412`), so a part's position is the one a later
`setshapepos_183` gives it. The script moves a part because the tree's frame has a different width or reads in
another order:

| Picture | Trees | Rows | Scripts | What moves | Why |
|---|---|---:|---:|---|---|
| Pharos floor number (`rbl`) | `es` | 648 | 27 | tens digit x 1628 → 1688, ones digit 1658 → 1718, floor word 1694 → 1624 | the `es` word `Nv.` goes before the number: `Nv. 23` where `us` shows `23F` |
| Pharos floor number (`rbl`) | `it` | 216 | 27 | floor word x 1694 → 1686, y 358 → 360 | the `it` word `° PIANO` follows the number: `23° PIANO` |
| Trial Mode stage number (`tri`) | `it` | 900 | 100 | label x 1614 → 1554; hundreds, tens and ones digits 1717, 1741, 1765 → 1641, 1663, 1685 | the label `Prova` and digits 22 pixels apart instead of 24 |
| Round counter of `BOSS_魔神竜`, Hall of the Wroth God (`rui_e01`) | `it` | 7 | 1 | label x 1594 → 1564; digits as in Trial Mode | the `it` label `° round` follows the number: `12° round` |
| Round counter of `BOSS_神竜`, Colosseum (`rwf_d01`) | `it` | 7 | 1 | the same as the Hall of the Wroth God | the same |
| Bhujerba notoriety gauge (`byu`) | `de` | 17 | 14 | title x 1528 → 1488, y 346 → 350 | the `de` title `Gerücht in Umlauf` is wider than `NOTORIETY` |
| Barheim Passage charge gauge (`mic`) | `fr` | 11 | 11 | title x 1529 → 1519, the 8 × 8 piece beside it 1525 → 1515 | the `fr` title `PUISSANCE` is wider than `CHARGE` |

The Pharos floor number is part 1 (tens, `regI0 = n / 10`), part 2 (ones, `regI1 = n % 10`) and part 3 (the floor
word) of window 3, for the number `n`. Its y is 358, or 42 when the script's register `I2` holds 1:
`y = 0x0166 - 0x013c * regI2` (`floor_disp_ctrl.init`, all 27 `us` `rbl` scripts). The floor word is `F` in `us`,
`in`, `kr`, `cn` and `ch`, `E` in `fr` and `de`, `° PIANO` in `it` and `Nv.` in `es`; only `it` and `es` move a part.

The script sets `I2` to 1 only under `if ((mp_rbl_flg6 & 4))` (108 stores in the 27 `rbl` scripts), and back to
0 when the story counter is above 6,000. Bit `0x4` of `mp_rbl_flg6` (global `0x0933`) is set by the Knowledge
statue's `statusgmk_se_技.talk` in The Reach (`rbl_a03`) and The Bounds of Truth (`rbl_j02`)
([Pharos first ascent scripts](pharos-first-ascent-scripts.md)), so the floor number moves to y 42 after that
offering.

The Trial Mode stage number is drawn at y 58 to 60 and at y 124 to 126, label first. The same scripts also place part
0 (x 1594 → 1564 at y 368), whose frame says `Stage` in `us`, `Round` in `in`, `kr`, `cn`, `ch` and `fr`, `RUNDE` in
`de`, `° round` in `it` and `Etapa` in `es`; no `tri` script shows part 0 (`setshapeshowstatus(3, 0, 1)` occurs in
none of them).

The two boss counters use the same picture. `rui_e01`'s `BOSS_魔神竜.parameter` raises its counter (`short` at script
global `0x095C`) by 1, to at most 999, each time it sets up the fight while `g_btl_魔神竜` is 1, and shows part 0 and
the digits once the counter is above 1. `rwf_d01`'s `BOSS_神竜.parameter` does the same for its own counter.

### Distance culling (`distance-culling`)

In 12 scripts, `kr`, `cn` and `ch` insert 392 calls `setcharclipall(1)` (`0x156`, `0x00347830`): 387 in ten `evt_t`
scripts, four in `gol_c01` (Dell of the Dreamer) and one in `nal_d01`. Most of them sit in the block that hands
control back to the player, straight after `ucon(); sethpmenu(1);` and before `clear_force_char_nearfade();`.

`setcharclipall` reaches `0x002EBBB0`: a non-zero value clears bit `0x1` of the byte `0x0215FD56`, and 0 sets it. It
then writes bit `0x1` of the render system tail `+0x18` (`[0x022C6F28] + 0x48818`) from the whole byte: set when the
byte is 0, clear otherwise (`0x002EBBC7`-`0x002EBBDA`). While that bit is on, characters past the distance fade (start
34.0, range 4.0 by default) fade out and are culled
([character fades](../Graphics/character-fades.md),
[character render records](../Graphics/character-render-records.md)).

| Scripts | Rows |
|---|---:|
| `evt_t0086` | 148 |
| `evt_t0083` | 115 |
| `evt_t0081` | 43 |
| `evt_t0085` | 39 |
| `evt_t0082` | 28 |
| `evt_t0084` | 7 |
| `gol_c01` | 4 |
| `evt_t0505` | 3 |
| `evt_t0090` | 2 |
| `evt_t0015`, `evt_t0094`, `nal_d01` | 1 each |

The `us` scripts leave the setting as it stands at these points: none of the 12 calls `setcharclipall`. Over all `us`
scripts, `ucon(); sethpmenu(1);` is followed by `clear_force_char_nearfade();` 7,996 times, by `setcharclipall(1);` 3
times and by other code 35 times; in `kr` the counts are 7,624, 375 and 35. `setcharclipall(1)` occurs 479 times in
`us` and 871 times in `kr`; `setcharclipall(0)` 714 times in both.

Six of the ten `evt_t` scripts (`evt_t0081`-`evt_t0085`, `evt_t0505`) and `evt_t0090` are the developer menus named
on [story counter values](story-counter-values.md); `evt_t0086` (`Map_Debug_menu_mtanaka`) and `evt_t0094`
(`トライアルデバッグメニュー`, a Trial Mode debug menu) are debug menus by their actor names.

### Message windows (`message-window`)

`amest` (`0x082`, `0x0034A090`) pushes 0 and runs `0x00349800`, which places two zeros beneath the last two values and
runs `mes` (`0x00348DF0`). The result is `amest(slot, text, x, y, style)`: `0x002E1EA0` sets the window style, `0x002E1F80`
the window corner with an automatic size, and `0x002E1F40` the window kind
([message windows](../Menus-And-HUD/message-windows.md)). `mesclose` (`0x012`, `0x0034D920`) closes the window of a slot.

`mes` opens the window through `0x002E16B0` only when the text's section 2 flag, which `0x002673A0` reads, is clear
(`0x00348E85`, `0x00348EE0`-`0x00348EFF`) ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

Each row of this kind opens a small window whose text is the escape `0F ;` and one inline icon, letter `H`
([text codes](../Menus-And-HUD/text-codes.md)): icon 8, the Square button in the button order of
[controls](../Controls-And-Input/controls.md), drawn as sprite `0x2D` of the icon tables `0x01E0CE10` and `0x01E0CE30`, or as
the key cap of Square's key, which `0x002B5B60` writes to `0x01E0CE30`:

| Where | Trees | Rows | Scripts | Change |
|---|---|---:|---:|---|
| Bhujerba notoriety gauge (`byu`) | `in` | 29 | 14 | `amest(6, text, 1687, y, 4)`: y 445 → 450 |
| Bhujerba notoriety gauge (`byu`) | `cn, ch` | 29 | 14 | the same window: y 445 → 444 |
| Royal Palace, Cellars and Lower Halls (`rrp_a02`, `rrp_a03`) | all eight | 7 | 2 | the window opens in slot 6 instead of slot 0 |
| Royal Palace (`rrp_a02`, `rrp_a03`) | all eight | 6 | 2 | `mesclose(0)` → `mesclose(6)`, closing it there |

In the Bhujerba rows the tree's text also starts with a letter-spacing escape (`0F $`), and the window sits 5 pixels
lower in `in` and 1 pixel higher in `cn` and `ch`.

In `us` the Royal Palace icon window shares slot 0 with the spoken lines (`amese(0, …)`), and its `mesclose(0)`
closes whatever window slot 0 holds. Every other tree opens and closes it in slot 6, the slot the `us` scripts
already clear when they set up the picture (`mesclose(6)` at `rrp_a02` line 452 and `rrp_a03` line 95).

### Demo-build code (`demo-build`)

Verb `0x5B4` runs `0x00355930` (`xor edx, edx; jmp 0x0026B4E0`), which stores 0 as the verb's result, so it is always
false; `0x5B1` runs the same body ([standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md)).
`kr`, `cn` and `ch` carry four blocks that only a build where it is true would run:

| Where | Rows | Code | In the game |
|---|---:|---|---|
| `gol_a01` group 1, `gol_b01` group 2, `pla_a02` group 1, `pla_a03` group 5, `pla_b02` groups 2 and 3 | 5 | `if (verb_0x5B4())`: `setmapidmj(group, 0, 0)`, `setmapidmj(group, 7, 0)`, `verb_0x5C7()` | never runs |
| `gol_c01`, `nal_d01` | 4 | the thank-you return to the title, under `verb_0x5B4()` | never runs |
| `gol_c01` | 32 | the same variables under new numbers | no change |
| `rui_a04` (Doubt Abandoned) | 5 | the save offer wrapped in `if (!verb_0x5B4())` | runs as in `us` |

`setmapidmj` (`0x100`, `0x003458D0`) pushes -1 and pops it straight back (`0x003458DF`-`0x003458F0`), then pops the
value, the kind and the group and jumps to `0x00379430(group, kind, value)` (`0x003458F5`-`0x00345927`).

`setmapidmj` (`0x100`, `0x003458D0` → `0x00379430`) with kinds 0 and 7 and value 0 would turn the floor of the map-jump
group into a wall for movement kinds 0 and 5 ([doors, gates and map changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md)),
closing those exits of Golmore Jungle and the Tchita Uplands. Verb `0x5C7` is `0x0016D6A0`, a bare `ret 0`.

The thank-you return adds the actors `RETURNTOTITLE` and `thankyoupage_IN_PLAYING`. It stops the music and sounds,
shows `thankyou.tga` through the title-image verbs (`0x5A2`, `0x0034E340` → `0x00473E80`, index 3) and ends with verb
`0x5B8` (`0x00354EF0`), whose last call `0x003603E0` sets the return-to-title byte `0x022CB72B` to 1
([game over](../World-Areas-And-Travel/game-over.md)). `thankyou.tga` ships in no tree.

The title-image verbs it uses work on the screen picture object at `[0x01F82CE0]`
([screen fades](../Graphics/screen-fades.md) has `0x5A3` and `0x5A6`):

- `0x5B9` (`0x0034D360` → `0x00474030` → `0x00183150` → `0x001D8D40`): sets the fade-in length `+0x14` and the fade-out
  length `+0x18`, each its count times `[0x01DFE0B4]`;
- `0x5A2` (`0x0034E340` → `0x00473E80`): loads title image `i`: 0 `warning.tga`, 1 the SQUARE ENIX logo, 2
  `rating_01.tga`, 3 `thankyou.tga`;
- `0x5A3` (`0x0034EA10` → `0x00473E60`): shows the loaded image for `n` steps plus both fades;
- `0x5A5` (`0x0034F140` → `0x00473E10` → `0x0017FF50` → `0x001D8C70`): returns the picture's `+0x04` while it plays (`+0x00`
  non-zero), else -1. `+0x04` counts the passes since the image started: the start `0x001D8F50` sets it to 0
  (`0x001D8F76`), and the picture's update `0x001D9080`, which the frame pump `0x0017D6E0` runs once a pass (`0x0017D819`),
  adds 1 (`0x001D90AB`). The scripts let the confirm button end the image once it passes a value they set;
- `0x5A4` (`0x0034ED70` → `0x00474020` → `0x00182F30` → `0x001D8FF0`): starts the fade-out, or ends the image at once when the fade-out
  length is 0;
- `0x5A6` (`0x0034F570`): holds the script while the image still plays.

The two added actors shift the numbering of `gol_c01`'s variables in the listing: each of the 32 rows differs from
`us` only in the `file_var_s<N>` or `local_var_s<N>` number, with the same offsets.

In `rui_a04` the save offer ("You will now have the option of saving your game." and
`openfullscreenmenu_48d(0x8005, 0)`) sits under `if (!verb_0x5B4())`, which is always true.

### Capture references (`capture-reference`)

`captureactor_367` (`0x367`, `0x00355570`) takes a reference of class three: the reference decoder `0x002650B0` resolves
class 3 through its jump table at `0x00265180` to the image plus the image's `+0x40` (the reference area) plus the
offset (`0x00265155`) ([party during scenes](../Scripts-And-Script-Commands/party-during-scenes.md)). The area
holds the actor names and the scripts' pictures. In every row the same name sits at the new offset:

| Scripts | Trees | Actors captured | Why the offset moves |
|---|---|---|---|
| `mic_d0100`, `mic_d0101` | `in, kr, cn, ch` | `BOSS_ザルエラ` | the picture at the start of the area has 4,096 palette colours instead of 2,304: 0x1C00 bytes more |
| `rsn_a0101`, `rsn_a0102` | `in, kr, cn, ch` | `BOSS_Jギース`, `BOSS_剣士兵隊長`, `BOSS_雑魚剣士兵01`, `BOSS_雑魚剣士兵02` | the same |
| `rui_e0101` | `it` | `BOSS_魔神竜` | the first picture is 256 × 256 instead of 256 × 128: 0x8000 bytes more |

With the resolved name, `0x00355570` takes manager 0's actor of that name (`0x00358800(0, name)`, `0x003555AB`) and,
when one is found and it is not the issuer, binds them with `0x00262F50(issuer, found)` (`0x003555C5`-`0x003555D7`), as
`captureactor` does; the gate `0x0053DD10(name)` it calls twice always returns 1.

### Sign record (`sign-record`)

In `in`, the image header's `+0x60` table of `frs_b02` (the Grand Bower, The Salikawood) holds one 16-byte record,
words 1, 2, 3, 1, 1, 0, 0, 0; in `us` it holds no record ([EBP script
image](../EBP-Script-Files/ebp-script-image.md)). The table's reader is `0x002642C0`, whose one direct caller
is `fieldsign` (`0x176`, `0x00355A00`, at `0x00355A23`), the verb that sets up a field object's touch and talk area.
`frs_b02` calls `fieldsign` in no tree, so the record has no effect.

### The title script `ttl_a01_e3` (`script-only`)

`kr` and `cn` ship a second title script, `plan_map/ttl_a/ttl_a01/global/ttl_a01_e3.ebp`, beside `ttl_a01.ebp`. The
two files are byte-identical and their image names `ttl_a01.src` as its source. Against `us` `ttl_a01` it:

- adds the actor `SERIES_PAGES`, whose `Play` and `Sync` function pairs show each title image with 30-step fades
  (`0x5B9(30, 30)`), and `WARNINGPAGE_IN_PLAYING`;
- requests `Warning_page` when verb `0x5C6` and `isFirstStartDone()` both return 0, in place of the rating request.
  `0x5C6` (`0x0033FED0`) returns the locale id from `0x00229E40` with 10 read as 0, so the page would show for Japanese.

No build loads it. Every language arm of the executable's zone script path table names `ttl_a01.ebp` for zone 12
([asset paths](../Game-Files-And-Data-Tables/asset-paths.md)), and neither the executable nor any shipped data
file names `ttl_a01_e3`. It is an unused copy, because that path table has no entry for it; the
[title scripts](titles-scripts.md) are those of `ttl_a01`.

## Related

- [script-language-differences.tsv](script-language-differences.tsv) - the rows of this page.
- [Pharos first ascent scripts](pharos-first-ascent-scripts.md), [Pharos third ascent scripts](pharos-third-ascent-scripts.md) - the floor number.
- [Ridorana Cataract scripts](ridorana-cataract-scripts.md) - the Colosseum fight.
- [Golmore Jungle scripts](golmore-jungle-scripts.md), [Nalbina dungeons scripts](nalbina-dungeons-scripts.md) - the demo-build blocks.
- [Royal Palace scripts](royal-palace-scripts.md) - the message verbs of the palace scripts.
- [Title scripts](titles-scripts.md) - `ttl_a01`.
- [Message windows](../Menus-And-HUD/message-windows.md), [text codes](../Menus-And-HUD/text-codes.md) - slots, pictures and escapes.
- [Character fades](../Graphics/character-fades.md) - the distance fade and cull.
- [Standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md) - the title images and verb `0x5B4`.
- [Languages](../Saving-Loading-And-Settings/languages.md) - the locale id and the trees each language reads.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x00355A00` calls `0x0025D5E0`, `0x00269F20`, `0x0026B4A0`; `0x00358800` calls `0x00263A30`, `0x00263FF0`.
- Actor entity: those functions are documented on [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md),
  [battle unit construction](../Characters-And-Objects/battle-unit-construction.md),
  [script requests](../Scripts-And-Script-Commands/script-requests.md),
  [party during scenes](../Scripts-And-Script-Commands/party-during-scenes.md).
- Actor entity: and on [debug menu](../Engine-Core/debug-menu.md).
- Audio: `0x00354EF0` calls `0x00249CA0`, `0x002DEE70`, `0x00360D70`, `0x00363560`; those functions are documented on
  [menu lists](../Menus-And-HUD/menu-lists.md),
  [time stop and freeze](../Engine-Core/time-stop-and-freeze.md),
  [chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md),
  [game over](../World-Areas-And-Travel/game-over.md).
- Core runtime: `0x0017D6E0` calls `0x001A1460`, `0x001DB600`, `0x001E0550`, `0x001E0590`, `0x001E05E0`, `0x001E05F0`, `0x0022A490`;
  `0x0017D6E0` is called by `0x0017CCD0`; `0x001D9080` is called by `0x0017D6E0`; `0x0033FED0` calls `0x00229E40`; `0x00473E80`
  calls `0x00229E40`; `0x0053DD10` is called by `0x0022B6E0`.
- Core runtime: those functions are documented on
  [game application](../Engine-Core/game-application.md),
  [frame update order](../Engine-Core/frame-update-order.md),
  [debug menu](../Engine-Core/debug-menu.md),
  [startup constants](../Engine-Core/startup-constants.md).
- Developer: `0x0017D6E0` calls `0x001C2F50`; those functions are documented on
  [game application](../Engine-Core/game-application.md).
- Input: `0x0024A440` is called by `0x00291D90`; `0x002B5B60` calls `0x001E0B90`, `0x001E0BD0`, `0x001E0DA0`, `0x001E0DC0`;
  `0x0053DD10` is called by `0x002E09A0`, `0x0035FCA0`, `0x0035FDD0`, `0x0046DD50`.
- Input: those functions are documented on
  [as7 menu graphics](../Game-Files-And-Data-Tables/as7-menu-graphics.md),
  [control remapping](../Controls-And-Input/control-remapping.md), [controls](../Controls-And-Input/controls.md),
  [frame update order](../Engine-Core/frame-update-order.md).
- Input: and on
  [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md).
- Movement: `0x00355A00` calls `0x0026AB60`, `0x0026B0C0`, `0x0026B620`, `0x0026BB00`, `0x0026BC70`, `0x0026BD50`, `0x0026BDD0`,
  `0x0026BFF0`; `0x00379430` calls
  `0x0026E850`, `0x0026E880`.
- Movement: those functions are documented on
  [party control modes](../Engine-Core/party-control-modes.md),
  [movement bodies and separation](../Movement-And-Pathfinding/movement-bodies-and-separation.md),
  [doors gates and map changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md).
- Presentation: `0x0017D6E0` calls `0x00189CE0`, `0x001BC190`, `0x001BDAC0`, `0x001CC600`, `0x0022FFE0`; `0x00229E40` is called by
  `0x002B0280`, `0x00434CD0`, `0x00435050`; `0x0053DD10` is called by `0x004355D0`, `0x00462540`.
- Presentation: those functions are documented on [debug menu](../Engine-Core/debug-menu.md),
  [game application](../Engine-Core/game-application.md),
  [frame update order](../Engine-Core/frame-update-order.md),
  [handbook files](../Game-Files-And-Data-Tables/handbook-files.md).
- Presentation: and on [effect element types](../Graphics/effect-element-types.md).
- Resource: `0x0017D6E0` calls `0x001A1220`; `0x0024A440` calls `0x0024A1D0`, `0x0024A4E0`; `0x002A7950` calls `0x0024A440`;
  `0x00473E80` calls `0x002DF8E0`.
- Resource: those functions are documented on
  [async load manager](../Game-Files-And-Data-Tables/async-load-manager.md),
  [as7 menu graphics](../Game-Files-And-Data-Tables/as7-menu-graphics.md),
  [binmenu images](../Game-Files-And-Data-Tables/binmenu-images.md),
  [debug menu](../Engine-Core/debug-menu.md).
- Rewards progression economy: `0x00229E40` is called by `0x00317ED0`; those functions are documented on
  [bestiary](../Enemy-Spawning/bestiary.md).
- Save load settings: `0x003603E0` is called by `0x00280140`; those functions are documented on
  [resource arena and relocation](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md).
- Save load settings: `0x0017D6E0` calls `0x001C18E0`, `0x001C1910`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md),
  [game application](../Engine-Core/game-application.md).
- UI: `0x00229E40` is called by `0x0028AAA0`, `0x002AC5F0`; `0x0053DD10` is called by `0x003C80C0`; those functions are
  documented on [hud](../Menus-And-HUD/hud.md), [augments](../Damage-And-Battle-Formulas/augments.md),
  [map screens](../Menus-And-HUD/map-screens.md).
- World area: `0x0053DD10` is called by `0x003789A0`; those functions are documented on
  [mpk map pack](../World-Areas-And-Travel/mpk-map-pack.md).
