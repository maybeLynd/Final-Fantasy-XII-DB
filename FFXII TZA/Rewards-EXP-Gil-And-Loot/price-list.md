---
title: "Price list: every script price id with its gil amount and the scripts that ask for it"
kind: "reference"
category: "Rewards: EXP, LP, gil and loot"
addresses: "02EBF060, 0031C5D0, 0031D7B0, 0034B000, 0032A880, 0030A0F0"
---

## What it lists

`price-list.tsv` holds one line for each of the 128 rows of the price table that registry slot `02EBF060` reaches
(`battle_pack.bin` directory entry `+74`<sub>h</sub>). Row *n* is price id `B000`<sub>h</sub> + *n*, inventory class 16
([Item and ability ids](../Engine-Core/item-and-ability-ids.md)): a gil amount with no item behind it,
which an event script reads with `getprice`. The aerodrome counters of
[Chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md) read `B005`<sub>h</sub>-`B007`<sub>h</sub> this way and then
take the amount with `subgill`.

- 41 ids are named in a `getprice` call of the us scripts (90 calls); the most asked for is `B075`<sub>h</sub>, 20,000 gil,
  20 calls in `alc_b05`, `alc_b06`, `alc_f03`, `alc_f04` and `alc_f05`.
- Eight calls, all in `fon_b01`, pass the id in a script variable (variables 199 and 200), so the TSV does not tie
  them to an id.
- The other 87 ids are named by no us script.

### How it is built

`Database/Tools/catalogues/price_list.py` reads the `st2e` table at entry `+74`<sub>h</sub> (128 rows of 4 bytes from the
section's `+20`<sub>h</sub>). The script columns come from `price-script-calls.tsv`, which
`Database/Tools/catalogues/getprice_calls.py` writes: it reads every us event script from the game's archive,
decodes each script function's bytecode, and resolves each call's argument, reading a `PUSHI` operand through the
script section's int pool (`+20`<sub>h</sub>, [EBP script image](../EBP-Script-Files/ebp-script-image.md)).

| Offset | Type | Field | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | price | gil; `0031C5D0`'s class-16 arm copies it to the query record's price `+28`<sub>h</sub> (`0031D7B0`-`0031D7F4`) |

`getprice(id)` (verb `2F0`<sub>h</sub>, `0034B000`) pops the id and returns `0032A880(id)`: `0030A0F0` fills a class-1 query
record for the id and returns its `+28`<sub>h</sub>, and `0032A880` turns a failed fill (-1) into 0. The table is read only
by that arm, the validator `00322C50` and the loader `00236C30`.

### Checks

- The table's header gives 128 rows of 4 bytes, and the TSV has 128 data lines.
- Two runs of each tool give byte-identical output.
- Rows compared with their readers: `B005`<sub>h</sub>-`B007`<sub>h</sub> are 210 gil each and named by `nac_b01`, one of the
  five aerodrome scripts; `B000`<sub>h</sub> is 500 gil, named by `rbn_a17`, `rbn_a18` and `rbn_a19`.
- `price-script-calls.tsv` has 90 rows, the `us_calls` count the [Verb table](../Scripts-And-Script-Commands/verb-table.md)
  gives for `getprice`.

## Columns

| Column | Meaning |
|---|---|
| `id` | the price id |
| `price` | `+00`<sub>h</sub>, in gil |
| `script_calls`, `scripts` | the number of us `getprice` calls that name the id, and their scripts |
| `explanation` | the amount and who asks for it |

`price-script-calls.tsv` has one line per call: `price_id` (or the variable it passes), `script`, `function` and
`pc`, the call's offset in the script section.

## Related

- [Gil: storage, the gil cap, every way gil changes, and the Plunderer and Spendthrift counters](gil.md)
- [Chocobos and airships: riding a chocobo, the ride timer and its dismount, and aerodrome travel](../World-Areas-And-Travel/chocobos-and-airships.md)
- [Item and ability ids: the sixteen-bit id space, the fifteen inventory classes, the thirty-two-class validator and the query record](../Engine-Core/item-and-ability-ids.md)
