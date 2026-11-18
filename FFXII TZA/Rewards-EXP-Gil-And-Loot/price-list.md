[Home](../../README.md) / [Rewards: EXP, LP, gil and loot](README.md) / Price list

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Price list: every script price id with its gil amount or sale count and the scripts that ask for it | reference | Rewards: EXP, LP, gil and loot | Gil, prices and reward packages | All 128 price ids (price_data, ids 0xB000-0xB07F) of the shipped battle_pack.bin: the gil amount of each, or for the 31 trophy trade limits the number of times a package sells, the number of getprice calls in the us event scripts that name it and the scripts they are in, and a one-line explanation; 41 ids are named by a script, and eight more calls pass the id in a script variable. | 0x02EBF060, 0x0031C5D0, 0x0031D7B0, 0x0034B000, 0x0032A880, 0x0030A0F0 |

## What it lists

[`price-list.tsv`](price-list.tsv) holds one line for each of the 128 rows of the price table that registry slot `0x02EBF060` reaches
(`battle_pack.bin` directory entry `+0x74`). Row *n* is price id `0xB000` + *n*, inventory class 16
([Item and ability ids](../Engine-Core/item-and-ability-ids.md)): a gil amount or a sale count
(below), with no item behind it,
which an event script reads with `getprice`. The aerodrome counters of
[Chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md) read `0xB002`-`0xB00F` this way and then
take the amount with `subgill`.

- 41 ids are named in a `getprice` call of the us scripts (82 of the 90 calls); the most asked for is `0xB075`, 20,000 gil,
  20 calls in `alc_b05`, `alc_b06`, `alc_f03`, `alc_f04` and `alc_f05`.
- Eight calls, all in `fon_b01`, pass the id in a script variable (variables 199 and 200). They are the Hunters'
  Camp trophy trade: the seller's `talk` stores 62 more ids, `0xB035` to `0xB072`, in two arrays beside the 31
  packages he sells. For package *k* he takes the first array's price and checks the second array's value as the
  number of times it sells, 1 for every package.
- The other 25 ids appear in no `getprice` call and no stored id of the us scripts.

### What each price buys

[`price-list-buys.tsv`](price-list-buys.tsv) gives, for the 103 ids a script uses, what the player pays for, read
from the steps of the function that asks for the price, and where the seller stands. Its 119 rows:

- 22 are maps a moogle sells: the price and the map's key item sit at the same index of two arrays.
- 14 are airship tickets: each aerodrome counter prices the route it keeps, and the same route's greeting names the
  destination ([Chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md)).
- 8 are chocobo hire at the stables.
- 5 are the pinewood chop the Archades shops sell for 20,000 gil, 3 the cab fare to Tsenoble without a chop and 3
  the 1,500 gil asked to get into the city in Old Archades.
- 1 is a rest at the Outpost on the Dalmasca Estersand that restores the party, and 1 a paid talk on the history
  of Rabanastre.
- 62 are the trophy trade: 31 package prices and 31 sale limits.

### Columns of price-list-buys.tsv

| Column | Holds |
|---|---|
| `gil` | the price `+0x00`: gil, except on the 31 `trophy trade limit` rows, where it is the number of times the package sells, 1 on each |
| `detail` | what the price buys, by the kind in `buys`: a map's key item id and name (`0x8002 Bhujerba`); an airship route with its destination and route code (`to Archades (route 1)`); a trophy trade package id and its contents, or for a sale limit `how many times package 0x90FF sells`; for the other kinds, the purchase in words with the line that asks for the price in single quotes, `[value]` standing for the price |
| `map_name`, `region` | where the seller stands: the map name and region of the script's zone in [`zone-asset-list.tsv`](../World-Areas-And-Travel/zone-asset-list.tsv), as the location line shows them (117 rows); the two scene scripts `ald_a0180` and `alc_a0280`, which have no row there, read Alley of Muted Sighs (Old Archades) and Nilbasse (Archades) |
| `seller` | the actor whose talk asks for the price: on the 62 trophy trade rows the name the game shows for it, Shifty-Eyed Man (name pair `0x3D4`), which becomes Outfitters (`0x418`) once quest scenario flag 71 is at least `0x46` and bit `0x1` of global byte `0x31F` is set, as his talk sets it (`setnpcname(0x03d4)` and `setnpcname(0x0418)` of `fon_b01`); on the other rows the actor's script name |

### Where the values come from

The price table is the `st2e` table at entry `+0x74` (128 rows of 4 bytes from the section's `+0x20`). The script
columns come from [`price-script-calls.tsv`](price-script-calls.tsv): every `getprice` call of the us event scripts,
with a `PUSHI` argument read through the script section's int pool (`+0x20`,
[EBP script image](../EBP-Script-Files/ebp-script-image.md)).

| Offset | Type | Field | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | price | gil, or a number of sales for `0xB054`-`0xB072` (What it lists); `0x0031C5D0`'s class-16 arm copies it to the query record's price `+0x28` (`0x0031D7B0`-`0x0031D7F4`) |

`getprice(id)` (verb `0x2F0`, `0x0034B000`) pops the id and returns `0x0032A880(id)`: `0x0030A0F0` fills a class-1 query
record for the id and returns its `+0x28`, and `0x0032A880` turns a failed fill (-1) into 0. The table is read only
by that arm, the validator `0x00322C50` and the loader `0x00236C30`.

The query record lives on `0x0030A0F0`'s stack: it writes the class 1 at `+0x00` and the id word at `+0x06`
(`0x0030A0F7`-`0x0030A101`), and the class-1 arm of `0x0031C5D0` replaces the class with the id's own class from
`0x00309440` and dispatches again (`0x0031C61F`-`0x0031C639`). `0x0030A0F0` returns -1 whenever `0x0031C5D0` returns a
negative value (`0x0030A115`-`0x0030A117`), for example the -2 it returns when `0x00309440` finds no class for the id
(`0x0031C62A`, `0x0031C650`).

## Columns

| Column | Meaning |
|---|---|
| `id` | the price id |
| `price` | `+0x00`: gil, except the 31 trophy trade limits `0xB054`-`0xB072`, where it is the number of times a package sells |
| `script_calls`, `scripts` | the number of us `getprice` calls that name the id, and their scripts |
| `explanation` | the amount and who asks for it |

[`price-script-calls.tsv`](price-script-calls.tsv) has one line per call: `price_id` (or the variable it passes), `script`, `function` and
`pc`, the call's offset in the script section.

## Related

- [Gil: storage, the gil cap, every way gil changes, and the Plunderer and Spendthrift counters](gil.md)
- [Chocobos and airships: riding a chocobo, the ride timer and its dismount, and aerodrome travel](../World-Areas-And-Travel/chocobos-and-airships.md)
- [Item and ability ids: the sixteen-bit id space, the fifteen inventory classes, the thirty-two-class validator and the query record](../Engine-Core/item-and-ability-ids.md)
