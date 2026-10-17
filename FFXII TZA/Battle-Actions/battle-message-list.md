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

`00236C30` binds it: `00236C7B`-`00236C86` pass the pack's directory entry 2 (`[pack+0xC]`) and the
descriptor slot `02EBF018` to `003845F0`. The readers then take a row as `table + id * stride` from
that slot (`0046AB10`, `00469570`, `005369C0`).

The US file is an `st2e` table: 102 rows of 8 bytes from `+0x20`, and a text heap at `+0x350`. In the
heap the row count is at `+0x0C`, the offsets from `+0x10`, and each text at `heap + 0x0C + offset`.
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
| `text_readable` | the text with every code written as a named placeholder. A string or number insert of slot n becomes the slot's kind, `[user]`, `[target]`, `[action]`, `[status]`, `[item]` or `[number]` (`{0F}{31}{8n}{80}{80}`, `{0F}{2D}{8n}{80}`). `[article of X]` is the article string of X's word row (`{0F}{6E}{80}{8n}`, word-row string 2, for example "a "). `[count of N, or the article of X for one]` is `{0F}{6C}`, and `[X, plural when N is above 1]` is `{0F}{6D}`, which takes the row's plural template ([Text codes](../Menus-And-HUD/text-codes.md)). A line break with its baseline code is `[newline]`; the colour and baseline codes `{0F}{29}..` and `{0F}{3C}..` are removed, and the one-byte characters `{99}` and `{9A}` are `!` and `?`. Rows `0x0B` and `0x0C` hold only the byte `0xC7`, kept as `{C7}` |
| `text_us` | the US text as stored: letters and `. , ' - :` decoded, the byte after each `{0F}` and all other bytes as `{hh}`, line breaks as `\n` |

## Data

The rows fall into these groups (full rows in the `.tsv`):

| Event ids | Lines |
|---|---|
| `0x00`-`0x03` | traps triggered |
| `0x04` | level up |
| `0x05`-`0x0C` | actions cancelled, out of range or too far (repeat-limited) |
| `0x0D`-`0x0F` | begins casting, readies, uses |
| `0x10`-`0x12` | has fallen, cast into the void, turns to stone |
| `0x13`-`0x23` | HP and MP restored, regains consciousness, cured or fading statuses, no effect, reserve members |
| `0x24`-`0x26` | items and gil obtained |
| `0x27`-`0x3D` | technick results and failures, steals, poach, Libra |
| `0x3E`-`0x43` | Paling, Magick Shield and White Wind rising and falling |
| `0x44`-`0x4D` | results of enemy abilities |
| `0x4E` | loot stolen |
| `0x4F`-`0x5C` | magick fields falling and lifting (repeat-limited) |
| `0x5D`-`0x62` | the Magick Pot, Zalera and back-attack lines (repeat-limited) |
| `0x63` | empty |
| `0x64`, `0x65` | items added to inventory |

Rows `0x0D`-`0x0F`, `0x27`-`0x2C`, `0x33`-`0x35`, `0x39`, `0x3A`, `0x3C`-`0x4C` and `0x63` are not
always shown. Rows `0x05`-`0x0C` and `0x4F`-`0x62` are repeat-limited. Bytes `+6` and `+7` are 0 in
every row.

## Related

- [Battle log](battle-log.md) - which result posts which event, and how a row becomes a line.
- [Action results](action-results.md) - the result fields the lines describe.
