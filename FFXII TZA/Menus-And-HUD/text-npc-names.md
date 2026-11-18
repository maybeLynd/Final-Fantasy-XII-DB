[Home](../../README.md) / [Menus and HUD](README.md) / NPC name strings

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| NPC name strings: every name of the npcdic.bin dictionaries in all nine languages | reference | Menus and HUD | Game text tables | Every string of the npcdic.bin name dictionaries side by side in the nine language trees: the first and second name of each of the 1,141 name pairs that field characters and named enemies carry, which code loads the dictionary and shows a name, how the row index gives the pair and the name, and the empty names in each language. | 0x00379D20, 0x003EAC40, 0x02B5E0D8, 0x003EAC10, 0x00263990, 0x002639E0, 0x0026DEA0, 0x00272CB0, 0x00268D10, 0x00536280 |

## What it lists

[text-npc-names.tsv](text-npc-names.tsv) has one row per entry of `bin/npcdic.bin`, with the name in each of the nine
language trees: 2,282 rows, the same count in every language. Every shipped dictionary holds 2,282 entries, so the
name ids mean the same character in every language.

`0x00379D20` loads the dictionary at boot through `0x003EAC40` and keeps it at `0x02B5E0D8`. Entry `2 x id` is the first
name of pair `id` and entry `2 x id + 1` its second (`0x003EAC10`). A field character shows the first name until the
story flag with the same number as its pair is set, and the second after it (`0x00263990`, `0x002639E0`). `0x0026DEA0`
takes the choice from its caller: the map screens test the flag themselves (`0x002B9C70`, `0x002BA530`) and the battle
log asks for the second name (`0x00536280`).

The entries are read through `0x003EAC10` and `0x003EABE0`: besides the load (`0x003EAC58`) and the relocation callback
`0x003EAC70`, they are the only instructions that name `0x02B5E0D8` (`0x003EAC1A`, `0x003EABE7`), and no image word points at
it.

The getters `0x00263990`, `0x002639E0` and `0x0026DEA0` reach `0x003EAC10` from 17 call sites: the name tag `0x00272CB0` and
`0x00272CE0`, which copies the name into a buffer, the field interaction pass `0x00268D10`, the battle log `0x00536280`
(always the second name), the text interpreter `0x002AC5F0` (`0x002ADDAA`, `0x002ADEA3`), the string copy `0x002B5240`
(`0x002B52EF`), `0x002B0280` (`0x002B16D4`, `0x002B1730`), the map screen's `0x002B9C70` (`0x002B9CFE`, `0x002B9D17`) and
`0x002BA530` (`0x002BA5DA`, `0x002BA5F0`), and `0x0025C230` and `0x0025C830` (two sites each).

`0x003EABE0`, the second name, is called by the verbs `setnpcname` (`0x0034B9BD`) and `setshopname` (`0x0034C1A9`) and
by the shop screens (`0x0057B9B7`, `0x0057C029`). [NPC names](../Characters-And-Objects/npc-names.md) describes the file,
the flag and the script verbs that give an actor its name id.

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

**Characters and objects**

| Function | | Functions |
|---|---|---|
| `0x0025C230` | calls | `0x003589B0`, `0x003DBB60` |
| `0x0025C230` | is called by | `0x0025C170` |
| `0x0025C830` | calls | `0x00233D70`, `0x003589B0`, `0x003DBB60` |
| `0x0025C830` | is called by | `0x0025C170` |
| `0x00263990` | is called by | `0x0025C230`, `0x0025C830`, `0x00268D10`, `0x00272CB0`, `0x00272CE0` |
| `0x00268D10` | calls | `0x00268EA0`, `0x0026DFB0`, `0x00358940`, `0x003589B0`, `0x003DB6E0` |
| `0x00272CB0` | calls | `0x003588B0` |
| `0x00272CE0` | calls | `0x003588B0` |

**Characters and objects** (explained on [identifier spaces](../Engine-Core/identifier-spaces.md), [script requests](../Scripts-And-Script-Commands/script-requests.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [ps2 cpu emulation](../Engine-Core/ps2-cpu-emulation.md))

**Characters and objects** (explained on [frame update order](../Engine-Core/frame-update-order.md), [npc names](../Characters-And-Objects/npc-names.md), [battle unit construction](../Characters-And-Objects/battle-unit-construction.md))

**Battle actions** (explained on [jump thunks](../Engine-Core/jump-thunks.md))

| Function | | Functions |
|---|---|---|
| `0x00268D10` | calls | `0x00317E60` |

**Engine core** (explained on [startup constants](../Engine-Core/startup-constants.md), [game application](../Engine-Core/game-application.md))

| Function | | Functions |
|---|---|---|
| `0x002AC5F0` | calls | `0x00229E40` |
| `0x002B0280` | calls | `0x00229E40` |
| `0x00379D20` | is called by | `0x0022A0B0` |

**Party** (explained on [frame update order](../Engine-Core/frame-update-order.md))

| Function | | Functions |
|---|---|---|
| `0x0025C830` | calls | `0x00358BB0` |

**Graphics**

| Function | | Functions |
|---|---|---|
| `0x00263990` | is called by | `0x002B0280` |
| `0x002639E0` | is called by | `0x002B0280` |
| `0x002AC5F0` | calls | `0x003A1DB0` |
| `0x002AC5F0` | is called by | `0x002AAE40` |
| `0x002B0280` | calls | `0x003A1DB0` |
| `0x002B0280` | is called by | `0x003F1530` |

**Graphics** (explained on [handbook files](../Game-Files-And-Data-Tables/handbook-files.md), [tim2 images](../Game-Files-And-Data-Tables/tim2-images.md), [message windows](message-windows.md), [battle numbers](battle-numbers.md))

**Game files and data tables** (explained on [music table](../Sound-And-Music/music-table.md), [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md), [small bin tables](../Game-Files-And-Data-Tables/small-bin-tables.md))

| Function | | Functions |
|---|---|---|
| `0x00379D20` | calls | `0x003EAB60`, `0x003EAC40`, `0x00473D20` |
| `0x003EAC40` | calls | `0x0051ED10` |
| `0x003EAC40` | is called by | `0x00379D20` |

**Game files and data tables** (explained on [startup constants](../Engine-Core/startup-constants.md))

**Scripts and script commands** (explained on [npc names](../Characters-And-Objects/npc-names.md))

| Function | | Functions |
|---|---|---|
| `0x003EABE0` | is called by | `0x0034B9A0`, `0x0034C170` |

**Story, events and hunts** (explained on [identifier spaces](../Engine-Core/identifier-spaces.md))

| Function | | Functions |
|---|---|---|
| `0x00263990` | calls | `0x0032A930` |
| `0x002639E0` | calls | `0x0032A930` |
| `0x002B9C70` | calls | `0x0032A930` |
| `0x002BA530` | calls | `0x0032A930` |

**World, areas and travel** (explained on [force fight mode](../Engine-Core/force-fight-mode.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md))

| Function | | Functions |
|---|---|---|
| `0x0025C830` | calls | `0x00377C20` |
| `0x00268D10` | calls | `0x00377700` |

</details>
