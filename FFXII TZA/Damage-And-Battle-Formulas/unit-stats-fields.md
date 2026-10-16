---
title: "Unit stats fields: every field of a unit's combat stats record, what it holds, and what writes and reads it"
kind: "reference"
category: "Damage and battle formulas"
summary: "Each field of the 0x1C8-byte combat stats record every battle unit carries (unit +0x698), from the kind byte and the party or enemy base values to the computed stats, status words, affinities, HP and MP, equipment, effect layers, timers, experience, license points, licenses and level, with its width, its meaning and the functions that write and read it."
addresses: "002FEF30, 0030FED0, 0030E360, 00300530, 0030C470"
---

## What it lists

Every battle unit has a combat stats record at unit `+0x698`. Party records sit in the battle state block
at `[02EBF190] + 8 + k * 0x1C8`; an enemy's record is the stats page of its spawn record. Byte `+0x05` says
which kind a record is, and several fields mean different things for the two kinds:

- for a party record (kind 0), `+0x08`-`+0x20` hold the base values the stats are grown from;
- for an enemy record (kind 1), the same bytes hold signed adjustments added to the enemy's area table
  values ([Stats](stats.md)).

The computed stats `+0x24`-`+0x44` are rewritten from these by `002FEF30`, and the augment layer `+0x78`
by `0030FED0` ([Augments](augments.md)).

## Columns

`unit-stats-fields.tsv`, one row per field:

| Column | Meaning |
|---|---|
| `offset` | the field's offset in the record |
| `width_type` | its width and type; "or" separates the party and enemy readings |
| `field` | a short name |
| `meaning` | what the field holds, with the instruction that fixes it |
| `writers`, `readers` | how many functions write or read the field, and up to six of them with one site each |

The writers and readers come from an access census of the record: every function that loads unit
`+0x698` or the party array, followed through register copies and through calls that pass the record,
three calls deep. A store counts for every field its width covers, so the word store at `0023AD8E`
writes both `+0x04` and `+0x05`.

The census misses accesses through a computed base or index (the effect layers in `0030E130`, the
License bits in `00323910` and `0030FED0`), records passed in a register it does not follow (the gambit
loader `00327CB0`, the two License Board setters), and writes made before a record is bound to a unit.
The writers and readers of those kinds that were read by hand are marked "by hand"; outside them, a
count of 0 means "none on the census routes".

## Related

- [Stats](stats.md) - how `+0x24`-`+0x37` are computed.
- [Augments](augments.md) - the augment layer, the immunity word and the clamps.
- [Elements](elements.md) - the affinity bytes `+0x40`-`+0x44`.
- [HP and KO](hp-and-ko.md) - current HP `+0x48`.
- [Action results](../Battle-Actions/action-results.md) - the applier that writes the enemy adjustments.
