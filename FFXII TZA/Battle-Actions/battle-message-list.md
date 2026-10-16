---
title: "Battle message list: every battle_message.bin row with its argument slots, flags and English text"
kind: "reference"
category: "Battle actions"
addresses: "02EBF018, 00236C7B, 005369C0, 00469570, 0046AB10"
---

## What it lists

Every line the battle log can show is a row of the battle message table, indexed by event id
([Battle log](battle-log.md)). The table is `battle_message.bin`
(`ps2data/image/ff12/test_battle/<language>/binaryfile/`), which the game loads as entry 2 of
`battle_pack.bin`. The shipped `battle_pack.bin` entry 2 begins with the exact bytes of the US
`battle_message.bin`.

`00236C30` binds it: `00236C7B`-`00236C86` pass the pack's directory entry 2 (`[pack+Ch]`) and the
descriptor slot `02EBF018` to `003845F0`. The readers then take a row as `table + id * stride` from
that slot (`0046AB10`, `00469570`, `005369C0`).

The US file is an `st2e` table: 102 rows of 8 bytes from `+20`<sub>h</sub>, and a text heap at `+350`<sub>h</sub>. In the
heap the row count is at `+0C`<sub>h</sub>, the offsets from `+10`<sub>h</sub>, and each text at `heap + 0Ch + offset`.
The German, Spanish, French and Italian files also have 102 rows; the `in`, `ch`, `cn` and `kr` files
have 100. The event ids and texts below are the US table's.

## Columns

`battle-message-list.tsv`, one row per event id:

| Column | Meaning |
|---|---|
| `event_id` | the row index, as the posting code passes it |
| `slot0`-`slot3` | the argument kind in row bytes `+0`, `+1`, `+2` and `+5`: user name (1), target name (2), status name (5), item or number (7), action name (8), or a context number (3, 4, 6, 9); blank for none |
| `always_shown` | `yes` when bit 7 of row byte `+3` is set, so the 24-unit visibility rule does not apply (`00469570`) |
| `category` | bits 2-6 of row byte `+3`, passed with the line (`005369C0`) |
| `rate_limited` | `yes` when bit 0 of row byte `+4` is set, so a repeat for the same unit is dropped for 450 clock ticks (`0046AB10`) |
| `text_readable` | the text with every code written as a named placeholder. A string or number insert of slot n becomes the slot's kind, `[user]`, `[target]`, `[action]`, `[status]`, `[item]` or `[number]` (`{0F}{31}{8n}{80}{80}`, `{0F}{2D}{8n}{80}`). `[article of X]` is the article string of X's word row (`{0F}{6E}{80}{8n}`, word-row string 2, for example "a "). `[count of N, or the article of X for one]` is `{0F}{6C}`, and `[X, plural when N is above 1]` is `{0F}{6D}`, which takes the row's plural template ([Text codes](../Menus-And-HUD/text-codes.md)). A line break with its baseline code is `[newline]`; the colour and baseline codes `{0F}{29}..` and `{0F}{3C}..` are removed, and the one-byte characters `{99}` and `{9A}` are `!` and `?`. Rows `0B`<sub>h</sub> and `0C`<sub>h</sub> hold only the byte `C7`<sub>h</sub>, kept as `{C7}` |
| `text_us` | the US text as stored: letters and `. , ' - :` decoded, the byte after each `{0F}` and all other bytes as `{hh}`, line breaks as `\n` |

## Data

The rows fall into these groups (full rows in the `.tsv`):

| Event ids | Lines |
|---|---|
| `00`<sub>h</sub>-`03`<sub>h</sub> | traps triggered |
| `04`<sub>h</sub> | level up |
| `05`<sub>h</sub>-`0C`<sub>h</sub> | actions cancelled, out of range or too far (repeat-limited) |
| `0D`<sub>h</sub>-`0F`<sub>h</sub> | begins casting, readies, uses |
| `10`<sub>h</sub>-`12`<sub>h</sub> | has fallen, cast into the void, turns to stone |
| `13`<sub>h</sub>-`23`<sub>h</sub> | HP and MP restored, regains consciousness, cured or fading statuses, no effect, reserve members |
| `24`<sub>h</sub>-`26`<sub>h</sub> | items and gil obtained |
| `27`<sub>h</sub>-`3D`<sub>h</sub> | technick results and failures, steals, poach, Libra |
| `3E`<sub>h</sub>-`43`<sub>h</sub> | Paling, Magick Shield and White Wind rising and falling |
| `44`<sub>h</sub>-`4D`<sub>h</sub> | results of enemy abilities |
| `4E`<sub>h</sub> | loot stolen |
| `4F`<sub>h</sub>-`5C`<sub>h</sub> | magick fields falling and lifting (repeat-limited) |
| `5D`<sub>h</sub>-`62`<sub>h</sub> | the Magick Pot, Zalera and back-attack lines (repeat-limited) |
| `63`<sub>h</sub> | empty |
| `64`<sub>h</sub>, `65`<sub>h</sub> | items added to inventory |

Rows `0D`<sub>h</sub>-`0F`<sub>h</sub>, `27`<sub>h</sub>-`2C`<sub>h</sub>, `33`<sub>h</sub>-`35`<sub>h</sub>, `39`<sub>h</sub>, `3A`<sub>h</sub>, `3C`<sub>h</sub>-`4C`<sub>h</sub> and `63`<sub>h</sub> are not
always shown. Rows `05`<sub>h</sub>-`0C`<sub>h</sub> and `4F`<sub>h</sub>-`62`<sub>h</sub> are repeat-limited. Bytes `+6` and `+7` are 0 in
every row.

## Related

- [Battle log](battle-log.md) - which result posts which event, and how a row becomes a line.
- [Action results](action-results.md) - the result fields the lines describe.
