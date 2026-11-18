[Home](../../README.md) / [Damage and battle formulas](README.md) / Unit stats fields

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Unit stats fields: every field of a unit's combat stats record, what it holds, and what writes and reads it | reference | Damage and battle formulas | Stats, HP and augments | Each field of the 0x1C8-byte combat stats record every battle unit carries (unit +0x698), from the kind byte and the party or enemy base values to the computed stats, status words, affinities, HP and MP, equipment, augment layers, timers, experience, license points, licenses and level, with its width, its meaning and the functions that write and read it. | 0x002FEF30, 0x0030FED0, 0x0030E360, 0x00300530, 0x0030C470 |

## What it lists

Every battle unit has a combat stats record at unit `+0x698`. The party's records, the forty member stats records, sit in the party block
at `[0x02EBF190] + 8 + k * 0x1C8`; an enemy's record is the stats page of its spawn record. Byte `+0x05` says
which kind a record is, and several fields mean different things for the two kinds:

- for a member stats record (kind 0), `+0x08`-`+0x20` hold the base values the stats are grown from;
- for an enemy record (kind 1), the same bytes hold signed adjustments added to the enemy's area table
  values ([Stats](stats.md)).

The computed stats `+0x24`-`+0x44` are rewritten from these by `0x002FEF30`, and the augment layer `+0x78`
by `0x0030FED0` ([Augments](augments.md)). Statuses are added and removed by `0x0030E360`
([Gaining and losing statuses](../Status-Effects-And-KO/status-changes.md)), the level is reset to 0 by the
grower `0x0030C470` (`0x0030C496`) and raised by the level change `0x0030C650`
([Stat growth per level](../Rewards-EXP-Gil-And-Loot/stat-growth-per-level.md)).

## Columns

[`unit-stats-fields.tsv`](unit-stats-fields.tsv), one row per field and owner. A field that means the same for both kinds has one row; a
field that means different things has a party row and an enemy row at the same offset:

| Column | Meaning |
|---|---|
| `offset` | the field's offset in the record |
| `owner` | `both`, `party` (kind 0) or `enemy` (kind 1) |
| `width_type` | its width and type for that owner |
| `field` | a short name |
| `meaning` | what the field holds, with the instruction that fixes it |
| `writers`, `readers` | every function that writes or reads the field, with one site each |

Rows named `pad` are bytes no field uses.

### How an access is counted

- A store or a read counts for every field its bytes cover, so the word store at `0x0023AD8E` writes both `+0x04`
  and `+0x05`. A clear or copy of a whole record or of the party block counts for every field.
- A function that only takes a field's address is listed as a reader.
- The block's member stats records are always kind 0: the initialiser `0x0023AC80` takes the kind from `edx >> 8`
  (`0x0023ACA1`), the block resets pass the member index, below `0x28` (`0x00237E26`, `0x00239AC4`), and no other
  instruction writes `+0x05` (the `kind` row).
- A party row lists the functions that reach a record through the block's member array
  ([Party data](../Party/party-data.md)), through the roster array `0x022C1740`, whose nine entries are member
  records from `0x00320AB0`, or through a battle unit's `+0x698`.
- An enemy row lists the functions that reach a record through a unit's `+0x698`, or before the record is bound:
  in the binder `0x0023A570` (record = spawn record `+0x80`, `0x0023A787`) and in what the initialiser `0x0023AC80` does
  for kind 1 (`0x0023AD9B`-`0x0023ADFF`).
- A test of the kind byte `+0x05` before an access limits it to the kinds that pass: a `cmp` or `test` of the byte,
  or of a register loaded from it, and the conditional jump on that result, in the function or in a caller that
  hands the record on.
- A function is in both the party row and the enemy row at an offset when it reads the record from a unit's
  `+0x698` and no test of `+0x05` lies between that load and the access. A `both` row lists every function.

The columns hold every access through a unit's `+0x698`, the block's member array, the roster array `0x022C1740`,
the record homes `0x02EBB560` and `0x022C1F50`, and the binder `0x0023A570`. No access reaches past the `0x1C8` bytes of
a record.

## Related

- [Stats](stats.md) - how `+0x24`-`+0x37` are computed.
- [Augments](augments.md) - the augment layer, the immunity word and the clamps.
- [Elements](elements.md) - the affinity bytes `+0x40`-`+0x44`.
- [HP and KO](hp-and-ko.md) - current HP `+0x48`.
- [Action results](../Battle-Actions/action-results.md) - the applier that writes the enemy adjustments.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Movement: `0x0046AB10` is called by `0x00469A50`; those functions are documented on
  [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md).
- RNG random selection: `0x00386C70` calls `0x00379CD0`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md).
- Save load settings: `0x00234ED0` is called by `0x005844A0`; `0x00235AF0` calls `0x002EF640`; those functions are documented
  on [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md),
  [global state accessors](../Engine-Core/global-state-accessors.md).
- Script VM: `0x00320AB0` is called by `0x0050FD00`, `0x0050FD50`, `0x0050FDD0`, `0x0050FE20`, `0x0050FE80`, `0x0050FED0`,
  `0x0050FF20`; `0x00327930` is called by `0x00348B40`; those functions are documented on
  [battle unit construction](../Characters-And-Objects/battle-unit-construction.md).
