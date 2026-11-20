[Home](../../README.md) / [Menus and HUD](README.md) / NPC name strings

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| NPC name strings: every name of the npcdic.bin dictionaries in all nine languages | reference | Menus and HUD | Game text tables | Every string of the npcdic.bin name dictionaries side by side in the nine language trees: the first and second name of each of the 1,141 name pairs that field characters and named enemies carry, which code loads the dictionary and shows a name, how the row index gives the pair and the name, and the empty names in each language. | 0x00379D20, 0x003EAC40, 0x02B5E0D8, 0x003EAC10, 0x00263990, 0x002639E0, 0x0026DEA0, 0x00272CB0, 0x00268D10, 0x00536280 |

## What it lists

[text-npc-names.tsv](text-npc-names.tsv) has one row per entry of `bin/npcdic.bin`, with the name in each of the nine
language trees: 2,282 rows, the same count in every language. Every shipped dictionary holds 2,282 entries, so the
name ids mean the same character in every language.

`0x00379D20` loads the dictionary at boot through `0x003EAC40` and keeps it at `0x02B5E0D8`. Entry `2 x id` is the first
name of pair `id` and entry `2 x id + 1` its second¹. A field character shows the first name until the
story flag with the same number as its pair is set, and the second after it². `0x0026DEA0`
takes the choice from its caller: the map screens test the flag themselves³ and the battle
log asks for the second name⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003EAC10` |
| ² | `0x00263990`, `0x002639E0` |
| ³ | `0x002B9C70`, `0x002BA530` |
| ⁴ | `0x00536280` |

</details>

The entries are read through `0x003EAC10` and `0x003EABE0`: besides the load¹ and the relocation callback
`0x003EAC70`, they are the only instructions that name `0x02B5E0D8`², and no image word points at
it.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003EAC58` |
| ² | `0x003EAC1A`, `0x003EABE7` |

</details>

The getters `0x00263990`, `0x002639E0` and `0x0026DEA0` reach `0x003EAC10` from 17 call sites: the name tag `0x00272CB0` and
`0x00272CE0`, which copies the name into a buffer, the field interaction pass `0x00268D10`, the battle log `0x00536280`
(always the second name), the text interpreter `0x002AC5F0`¹, the string copy `0x002B5240`², `0x002B0280`³, the map screen's `0x002B9C70`⁴ and
`0x002BA530`⁵, and `0x0025C230` and `0x0025C830` (two sites each).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002ADDAA`, `0x002ADEA3` |
| ² | `0x002B52EF` |
| ³ | `0x002B16D4`, `0x002B1730` |
| ⁴ | `0x002B9CFE`, `0x002B9D17` |
| ⁵ | `0x002BA5DA`, `0x002BA5F0` |

</details>

`0x003EABE0`, the second name, is called by the verbs `setnpcname`¹ and `setshopname`² and
by the shop screens³. [NPC names](../Characters-And-Objects/npc-names.md) describes the file,
the flag and the script verbs that give an actor its name id.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0034B9BD` |
| ² | `0x0034C1A9` |
| ³ | `0x0057B9B7`, `0x0057C029` |

</details>

### Reading the rows

| `index` | Pair | `us` | `de` | `in` |
|---:|---:|---|---|---|
| 0 | 0, first | `Rabanastran` | `Rabanastre-Bürger` | `ラバナスタ市民` |
| 1 | 0, second | `Rabanastran` | `Rabanastre-Bürger` | `ラバナスタ市民` |
| 32 | 16, first | `Imperial` | `Imperialer Soldat` | `帝国兵` |
| 33 | 16, second | `Sherral` | `Scharmal` | `シャルアール` |

Pair 0 repeats one name, so its flag changes nothing on screen; pair 16 shows `Imperial` until its flag is set
and `Sherral` after. The only text code in the names is the space `0x04`, in every tree but `in`, `cn` and `ch`.

## Columns

| Column | Meaning |
|---|---|
| `index` | the entry: pair `index / 2`, its first name when `index` is even and its second when odd |
| `us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn`, `ch` | the name in that language tree (English, German, Spanish, French, Italian, Japanese, Korean, Simplified Chinese, Traditional Chinese), decoded with the tree's font |
| `missing` | the languages whose dictionary has no entry `index`; empty in every row |
| `same_bytes` | the groups of languages whose name bytes are identical, each group's languages joined by `=` and the groups by `;`; only groups of two or more |

## Data

| Fact | Value |
|---|---|
| entries | 2,282 in each of the nine languages, 1,141 pairs |
| empty names | entries 1924 and 1925 in all nine languages; 1873, 1875, 1881 and 1883 also in `cn` and `ch`; 1996 and 2065 also in `cn` |

## Related

- [NPC names](../Characters-And-Objects/npc-names.md) - the dictionary file, the name flag, the pairs whose names differ
  and the verbs that assign a name id.
- [Text codes](text-codes.md) - the escape `0F 38` that inserts a name into message text.
- [String tables](text-string-tables.md) - the battle messages whose unit names come from here.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 43 calls with 13 other topics</summary>

**Characters and objects** (explained on [identifier spaces](../Engine-Core/identifier-spaces.md), [script requests](../Scripts-And-Script-Commands/script-requests.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [ps2 cpu emulation](../Engine-Core/ps2-cpu-emulation.md), [frame update order](../Engine-Core/frame-update-order.md), [npc names](../Characters-And-Objects/npc-names.md), [battle unit construction](../Characters-And-Objects/battle-unit-construction.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0025C230`](../Scripts-And-Script-Commands/script-requests.md) (on script requests) | calls | [`0x003589B0`](../Graphics/effect-anchors-and-targets.md) Actor handle: encode registry entry (on effect anchors and targets)<br>[`0x003DBB60`](../Scripts-And-Script-Commands/script-requests.md) (on script requests) |
| [`0x0025C230`](../Scripts-And-Script-Commands/script-requests.md) (on script requests) | is called by | [`0x0025C170`](../Engine-Core/time-stop-and-freeze.md) (on time stop and freeze) |
| [`0x0025C830`](text-npc-names.md) | calls | [`0x00233D70`](../Scripts-And-Script-Commands/battle-verbs.md) (on battle verbs)<br>[`0x003589B0`](../Graphics/effect-anchors-and-targets.md) Actor handle: encode registry entry (on effect anchors and targets)<br>[`0x003DBB60`](../Scripts-And-Script-Commands/script-requests.md) (on script requests) |
| [`0x0025C830`](text-npc-names.md) | is called by | [`0x0025C170`](../Engine-Core/time-stop-and-freeze.md) (on time stop and freeze) |
| [`0x00263990`](enemy-names-on-screen.md) (on enemy names on screen) | is called by | [`0x0025C230`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x0025C830`](text-npc-names.md)<br>[`0x00268D10`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x00272CB0`](enemy-names-on-screen.md) (on enemy names on screen)<br>[`0x00272CE0`](../Characters-And-Objects/npc-names.md) (on npc names) |
| [`0x00268D10`](../Scripts-And-Script-Commands/script-requests.md) (on script requests) | calls | [`0x00268EA0`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x0026DFB0`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x00358940`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor manager: get record by ordinal (on party during scenes)<br>[`0x003589B0`](../Graphics/effect-anchors-and-targets.md) Actor handle: encode registry entry (on effect anchors and targets)<br>[`0x003DB6E0`](../Scripts-And-Script-Commands/script-requests.md) Actor resource: select pending entry for execution (on script requests) |
| [`0x00272CB0`](enemy-names-on-screen.md) (on enemy names on screen) | calls | [`0x003588B0`](../Characters-And-Objects/actor-record.md) Actor handle: resolve registry entry by packed id (on actor record) |
| [`0x00272CE0`](../Characters-And-Objects/npc-names.md) (on npc names) | calls | [`0x003588B0`](../Characters-And-Objects/actor-record.md) Actor handle: resolve registry entry by packed id (on actor record) |

**Battle actions** (explained on [jump thunks](../Engine-Core/jump-thunks.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00268D10`](../Scripts-And-Script-Commands/script-requests.md) (on script requests) | calls | [`0x00317E60`](../Movement-And-Pathfinding/player-movement.md) (on player movement) |

**Engine core** (explained on [startup constants](../Engine-Core/startup-constants.md), [game application](../Engine-Core/game-application.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002AC5F0`](text-drawing.md) (on text drawing) | calls | [`0x00229E40`](../Story-Events-And-Hunts/script-language-differences.md) (on script language differences) |
| [`0x002B0280`](text-drawing.md) (on text drawing) | calls | [`0x00229E40`](../Story-Events-And-Hunts/script-language-differences.md) (on script language differences) |
| [`0x00379D20`](text-npc-names.md) | is called by | [`0x0022A0B0`](../Saving-Loading-And-Settings/languages.md) (on languages) |

**Party** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0025C830`](text-npc-names.md) | calls | [`0x00358BB0`](../Engine-Core/frame-update-order.md) (on frame update order) |

**Graphics** (explained on [handbook files](../Game-Files-And-Data-Tables/handbook-files.md), [tim2 images](../Game-Files-And-Data-Tables/tim2-images.md), [message windows](message-windows.md), [battle numbers](battle-numbers.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00263990`](enemy-names-on-screen.md) (on enemy names on screen) | is called by | [`0x002B0280`](text-drawing.md) (on text drawing) |
| [`0x002639E0`](text-npc-names.md) | is called by | [`0x002B0280`](text-drawing.md) (on text drawing) |
| [`0x002AC5F0`](text-drawing.md) (on text drawing) | calls | [`0x003A1DB0`](../PhyreEngine/the-frame.md) Render command: submit current buffer and swap (on the frame) |
| [`0x002AC5F0`](text-drawing.md) (on text drawing) | is called by | [`0x002AAE40`](text-drawing.md) (on text drawing) |
| [`0x002B0280`](text-drawing.md) (on text drawing) | calls | [`0x003A1DB0`](../PhyreEngine/the-frame.md) Render command: submit current buffer and swap (on the frame) |
| [`0x002B0280`](text-drawing.md) (on text drawing) | is called by | [`0x003F1530`](hud.md) (on hud) |

**Game files and data tables** (explained on [music table](../Sound-And-Music/music-table.md), [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md), [small bin tables](../Game-Files-And-Data-Tables/small-bin-tables.md), [startup constants](../Engine-Core/startup-constants.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00379D20`](text-npc-names.md) | calls | [`0x003EAB60`](../Sound-And-Music/music-table.md) (on music table)<br>[`0x003EAC40`](text-npc-names.md)<br>[`0x00473D20`](../Game-Files-And-Data-Tables/small-bin-tables.md) (on small bin tables) |
| [`0x003EAC40`](text-npc-names.md) | calls | [`0x0051ED10`](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md) (on file requests and the read queue) |
| [`0x003EAC40`](text-npc-names.md) | is called by | [`0x00379D20`](text-npc-names.md) |

**Scripts and script commands** (explained on [npc names](../Characters-And-Objects/npc-names.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x003EABE0`](../Characters-And-Objects/npc-names.md) (on npc names) | is called by | [`0x0034B9A0`](../Story-Events-And-Hunts/archades-scripts.md) (on archades scripts)<br>[`0x0034C170`](../Characters-And-Objects/npc-names.md) (on npc names) |

**Story, events and hunts** (explained on [identifier spaces](../Engine-Core/identifier-spaces.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00263990`](enemy-names-on-screen.md) (on enemy names on screen) | calls | [`0x0032A930`](../Engine-Core/identifier-spaces.md) Persistent flag: query bank2048 (on identifier spaces) |
| [`0x002639E0`](text-npc-names.md) | calls | [`0x0032A930`](../Engine-Core/identifier-spaces.md) Persistent flag: query bank2048 (on identifier spaces) |
| [`0x002B9C70`](text-npc-names.md) | calls | [`0x0032A930`](../Engine-Core/identifier-spaces.md) Persistent flag: query bank2048 (on identifier spaces) |
| [`0x002BA530`](text-npc-names.md) | calls | [`0x0032A930`](../Engine-Core/identifier-spaces.md) Persistent flag: query bank2048 (on identifier spaces) |

**World, areas and travel** (explained on [force fight mode](../Engine-Core/force-fight-mode.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0025C830`](text-npc-names.md) | calls | [`0x00377C20`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes) |
| [`0x00268D10`](../Scripts-And-Script-Commands/script-requests.md) (on script requests) | calls | [`0x00377700`](../World-Areas-And-Travel/area-flags-navimapdata.md) (on area flags navimapdata) |

</details>
