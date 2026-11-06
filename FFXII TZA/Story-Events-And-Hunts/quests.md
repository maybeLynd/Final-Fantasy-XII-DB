---
title: "Quests: the ordered and cleared state each quest keeps in the save, its progress byte and word, the verbs that change them, and the bug that clears the wrong ordered bit"
kind: "system"
category: "Story, events and hunts"
addresses: "0x0046B3F0, 0x0046B290, 0x0046B490, 0x0046B350, 0x0046B380, 0x0046B240, 0x0046B1A0"
---

## What the player sees

- Taking on a quest marks it as ordered; finishing it marks it as cleared and adds one to the total of
  quests cleared.
- Each quest also keeps a small progress value and a word the scripts use for its contract.
- Finishing a quest numbered above 7 leaves it marked as ordered and unmarks one of the first eight quests instead
  (finishing quest 13 unmarks quest 5), through a slip in how the game finds the bit.

## How it works

### Where quest state lives

Every quest field is in the save payload, the bytes from `SaveImage_GetPersistentPayloadBase` (`0x002EF2B0`,
[Save data](../Saving-Loading-And-Settings/save-data-fields.md)). A quest is a number *q* from 0 to 255:

| Payload offset | Field | Size |
|---|---|---|
| `+0x1000` | ordered bits, bit *q* | 32 bytes |
| `+0x1020` | cleared bits, bit *q* | 32 bytes |
| `+0x1040` | quests cleared in total, at most `0xFFFF` | `u32` |
| `+0x1064 + q` | scenario byte | 256 bytes |
| `+0x1164 + 2q` | contract word; set to the field id when the quest is first ordered | 256 words |
| `+0x1364` | OK bits, bit *q* | 32 bytes |

The quest fields occupy `+0x1000`-`+0x1043` and `+0x1064`-`+0x1383`; the 32 bytes between them hold other save data,
and the story flag banks begin at `+0x1384`.

### The verbs

| Verb | Handler | Body | Effect |
|---|---|---|---|
| `0x1D1` `setquestorder(q, v)` | `0x0033FF80` | `0x0046B3F0` | with *v*, sets ordered bit *q* and writes the current field id to the contract word (`0x0046B436`-`0x0046B44E`); an already ordered quest is left as it is (`0x0046B42D`-`0x0046B434`); without *v*, clears the bit (`0x0046B466`-`0x0046B470`) |
| `0x1CF` `isquestorder(q)` | `0x0033F6E0` | `0x0046B240` | ordered bit *q* |
| `0x1D3` `getquestorder` | `0x00340690` | `0x0046B0F0` | the number of ordered bits set, over the 32 bytes (`0x0046B105`-`0x0046B163`) |
| `0x1D2` `setquestclear(q, v)` | `0x00340300` | `0x0046B290` | with *v*: total + 1 below `0xFFFF`, cleared bit *q* set, and an ordered bit cleared, below (`0x0046B2C4`-`0x0046B316`); without, cleared bit *q* cleared (`0x0046B32D`-`0x0046B33C`) |
| `0x1D0` `isquestclear(q)` | `0x0033FAA0` | `0x0046B1A0` | cleared bit *q* |
| `0x1D4` `getquestclear` | `0x00340C50` | `0x0046B020` | the number of cleared bits set |
| `0x1D5` `getquestcleartotal` | `0x00341050` | `0x0046B0B0` | the total |
| `0x2B3` `setquestscenarioflag(q, v)` | `0x00351140` | `0x0046B490` | the scenario byte = *v*; the handler keeps *q* and *v* between 0 and 255 (`0x00351155`-`0x0035117B`) |
| `0x2B4` `getquestscenarioflag(q)` | `0x00351F90` | `0x0046B180` | the scenario byte |
| `0x2B5` `setquestcontract(q, v)` | `0x00351560` | `0x0046B350` | the contract word = *v* (`0x0046B364`) |
| `0x2B6` `getquestcontract(q)` | `0x00351C40` | `0x0046B0D0` | the contract word |
| `0x2BC` `setquestok(q, v)` | `0x00353B20` | `0x0046B380` | OK bit *q* set or cleared (`0x0046B3B5`, `0x0046B3D1`) |
| `0x2BD` `isquestok(q)` | `0x00353E80` | `0x0046B1F0` | OK bit *q* |

Two dispatchers reach the same bodies outside the verbs. `0x00329E60(kind, unit, q, v)` sets an ordered bit for kind
4 and a cleared bit for kind 5 (`0x00329EC9`, `0x00329EE0`); the action effect applier `0x00312170` (`0x0031225E`) and
`0x002FE660` (`0x002FE74E`) call it. Its reader twin `0x00321190(kind, unit, q, out)` answers ordered, cleared, scenario
byte and contract word for kinds 4-7 (`0x003211FC`-`0x00321232`); `0x00301AD0`, `0x002FAD40`, `0x002FE660` and `0x00312170` call
it. The developer verb `0x206C` `debug_clearquestall` does nothing: its handler `0x0017E7D0` returns at once.

### The wrong ordered bit

When `setquestclear` sets a cleared bit it also means to clear the quest's ordered bit, but it computes the byte
and bit again from the bit position, `q & 7`, instead of from *q* (`0x0046B2EF`-`0x0046B316`). The byte is therefore
always the first, and the bit value `1 << (q & 7)`: clearing quest 13 clears the ordered bit of quest 5, and the
quest itself stays ordered. Only quests 0-7 have their own ordered bit cleared. The same happens when a clear
arrives through `0x00329E60` kind 5.

### Who else reads it

The quest list of the `menuhandbook` object, bound at `0x022C2550`, gives a minimum scenario byte per quest:

- The clan rank counts the list's quests that are ordered or cleared and whose scenario byte reaches the minimum
  (`0x00316480`, `0x00316520`-`0x0031654D`; [Shops](../Items-Equipment-Shops-And-Licenses/shops.md) has the rank table).
- `0x00315DC0(q)` answers false for q = -1 (`0x00315DC8`-`0x00315DCD`) and true for a cleared quest (`0x00315DD5`), else, for a quest in the list, whether its scenario
  byte reaches the minimum (`0x00315DE9`-`0x00315E6D`). A quest the list does not hold, or an empty list, answers
  false (`0x00315E27`-`0x00315E45`); only a missing list answers true (`0x00315DF5`-`0x00315E10`, `0x00315E75`).

Besides these, the menu's quest readers (`0x0037E780`, `0x0037EAA0`, `0x0037EB90`, `0x0037EC70`, `0x0037EE10`, `0x0037EF70`,
`0x0037F060`, `0x00380170`, `0x003BC260`, `0x003C0A00`, `0x003F4C30`) and the Clan Primer's hunt panes (`0x00577C30`, `0x005781A0`,
`0x00578310`, `0x00578450`, `0x005789D0`; [Clan Primer](../Menus-And-HUD/clan-primer.md),
[Quest menu files](../Game-Files-And-Data-Tables/quest-menu-files.md)) read the bits.

### The quests

[quest-list.tsv](quest-list.tsv) has 30 rows: one for each of the 18 quest ids outside the hunts that a shipping
script sets, 0, 3, 4, 5, 6, 8, 10, 11, 12, 13, 15, 18, 52, 53, 57, 58, 59 and 71, and one for each of 12 side quests
with no quest id of their own. The 45 hunts, quests 128 to 172, are in
[hunts.tsv](hunts.tsv).

These counts cover the 1,114 us listings that decode, 769 zone and 345 event scripts;
`evt_t0020.ebp` has no `EBP2` header and no listing. The developer scripts `evt_t0090` (`デバッグ監督`, the debug
director), `evt_t0500` (`イベントデバッグメニュー`, the event debug menu) and `evt_t0505` are left out of the rows, cells and counts.

Twelve are story chapters, the ids `menuquest.dat` puts in group 0 (records 0 to 18; no `us` listing sets the seven ids
14, 16, 17 and 19 to 22). Their scenario byte steps along the story beside the story counter, and their
`questtitle.bin` rows are empty in `us`. Six are quests that `menuquest.dat` does not list: July's soldier at Nalbina
(52), Rimzat's windvane (53), the Nabudis medallions of Ma'kleou (57), Roh'kenmou (58) and Roh'kenmu (59), and the
Hunt Club (71).

The twelve side quests have `-` for a quest id: the Craftsmoogles' windmills of the Cerobi Steppe, the Dragon Scale,
the bottles and their messages, the Feather of the Flock and the escaped cockatrices, the Cactoid Compact, the Ring of
the Toad, the Errmonea Leaf, the sick traveler and the Barheim Key, the cactoids of the Nebra, the Soul Ward Key,
Pilika's diary and Ann's letter.

They keep their state in key items and in bytes of the script globals; the cockatrices and the Ring of the Toad also
step along the scenario byte of hunt quests 160 and 138 after those hunts. The sick traveler and Pilika's diary begin
once hunt quests 130 and 161 are cleared, and the cactoids of the Nebra once Dantro's wife has the cactus flower.

Few quests use the ordered and cleared bits. `setquestorder(q, 1)` with a literal id runs for 6, 18 and 53, and
`setquestclear(q, 1)` for 0, 4, 12, 18, 53, 57 and 58, each one line after `setquestorder(q, 0)`, which clears the
quest's own ordered bit; for 12, 18, 53, 57 and 58 the clear itself misses it (The wrong ordered bit, above). The
clears of 4, 12 and 18 and the order of 18 sit in the quest-clear and quest-accept screen functions
(`クエストクリア画面`, `クエスト受諾画面`) that no `us` listing requests by name.

The `quest_director` actor of `rbn_a18`, `rbn_a19`, `bhm_a04` and the scene `slm_a0380` orders, accepts and clears
the quest whose id a script variable holds; the variable is set to 53 in `rbn_a19` (line 5299) and 3 in `slm_a0380`
(line 90). No `us` listing requests a `quest_director` function: the name occurs only at the four actor headers.
The variable id of `rbn_a14`'s hunt clear is 167 or 170 (lines 2614, 2634), both hunts.

| Column | Meaning |
|---|---|
| `quest` | the quest id, or `-` for a side quest without one |
| `kind` | story chapter, with its `menuquest.dat` record, quest, or side quest (script bytes) |
| `what_it_is` | the quest in game terms, from its dialogue and scenes |
| `giver` | the character who asks, by the name the game shows |
| `place` | the fields where its steps are written, by zone name |
| `ordered_by`, `cleared_by` | the script, actor, function and line of the order and clear calls, or where the first and last steps are written |
| `condition` | what the scripts test before the order or the first step |
| `steps` | each scenario-byte value, what it marks, and where it is written; for a side quest, each step and the bytes it writes |
| `reward` | the items the clearing code gives or takes, with [scene-rewards.tsv](scene-rewards.tsv) |
| `menu_title` | the `questtitle.bin` row of its `menuquest.dat` text id |

## Modding notes

- Clearing a quest from a script also unmarks quest `q & 7` as ordered; a mod that relies on ordered bits above 7
  should not expect `setquestclear` to clear them.
- The field id written on the first order and the contract word are the same word, so a script that sets the
  contract replaces the recorded field.

## Related

- [Save data](../Saving-Loading-And-Settings/save-data-fields.md) - the payload the quest fields sit in.
- [Shops](../Items-Equipment-Shops-And-Licenses/shops.md) - the clan rank that counts quests.
- [Hunts](hunts.md) - the 45 hunts, quests 128 to 172.
