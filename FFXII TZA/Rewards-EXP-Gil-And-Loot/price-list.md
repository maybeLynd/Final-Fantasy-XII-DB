---
title: "Price list: every script price id with its gil amount and the scripts that ask for it"
kind: "reference"
category: "Rewards: EXP, LP, gil and loot"
addresses: "0x02EBF060, 0x0031C5D0, 0x0031D7B0, 0x0034B000, 0x0032A880, 0x0030A0F0"
---

## What it lists

`price-list.tsv` holds one line for each of the 128 rows of the price table that registry slot `0x02EBF060` reaches
(`battle_pack.bin` directory entry `+0x74`). Row *n* is price id `0xB000` + *n*, inventory class 16
([Item and ability ids](../Engine-Core/item-and-ability-ids.md)): a gil amount with no item behind it,
which an event script reads with `getprice`. The aerodrome counters of
[Chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md) read `0xB005`-`0xB007` this way and then
take the amount with `subgill`.

- 41 ids are named in a `getprice` call of the us scripts (82 of the 90 calls); the most asked for is `0xB075`, 20,000 gil,
  20 calls in `alc_b05`, `alc_b06`, `alc_f03`, `alc_f04` and `alc_f05`.
- Eight calls, all in `fon_b01`, pass the id in a script variable (variables 199 and 200), so the TSV does not tie
  them to an id.
- The other 87 ids are named by no us script.

### Where the values come from

The price table is the `st2e` table at entry `+0x74` (128 rows of 4 bytes from the section's `+0x20`). The script
columns come from [`price-script-calls.tsv`](price-script-calls.tsv): every `getprice` call of the us event scripts,
with a `PUSHI` argument read through the script section's int pool (`+0x20`,
[EBP script image](../EBP-Script-Files/ebp-script-image.md)).

| Offset | Type | Field | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | price | gil; `0x0031C5D0`'s class-16 arm copies it to the query record's price `+0x28` (`0x0031D7B0`-`0x0031D7F4`) |

`getprice(id)` (verb `0x2F0`, `0x0034B000`) pops the id and returns `0x0032A880(id)`: `0x0030A0F0` fills a class-1 query
record for the id and returns its `+0x28`, and `0x0032A880` turns a failed fill (-1) into 0. The table is read only
by that arm, the validator `0x00322C50` and the loader `0x00236C30`.

## Columns

| Column | Meaning |
|---|---|
| `id` | the price id |
| `price` | `+0x00`, in gil |
| `script_calls`, `scripts` | the number of us `getprice` calls that name the id, and their scripts |
| `explanation` | the amount and who asks for it |

`price-script-calls.tsv` has one line per call: `price_id` (or the variable it passes), `script`, `function` and
`pc`, the call's offset in the script section.

## Related

- [Gil: storage, the gil cap, every way gil changes, and the Plunderer and Spendthrift counters](gil.md)
- [Chocobos and airships: riding a chocobo, the ride timer and its dismount, and aerodrome travel](../World-Areas-And-Travel/chocobos-and-airships.md)
- [Item and ability ids: the sixteen-bit id space, the fifteen inventory classes, the thirty-two-class validator and the query record](../Engine-Core/item-and-ability-ids.md)
