# An embedded-record detector that does not work, and the control that says so

**OPUS, 2026-09-16. A negative result, recorded so the next agent does not rebuild it.**

## What prompted it

`SpawnRecord+0x80` turned out to be an embedded `BattleStatsRecord`: 23 of `SpawnRecord`'s 37 rows
model the same memory twice, and 11 of them are already named on the other type
([the evidence](spawnrecord-battlestats-overlap.tsv)). One instance is an accident. The store holds
**251 types and 1,991 rows**, and the obvious next question is whether it happens elsewhere.

## The method

For every ordered pair of types `(A, B)` and every displacement `K` derived from an actual pair of
rows of **equal size**, count how many of `A`'s rows at offset `o` have a `B` row at `o − K` of the
same size. Report alignments at least 5 rows deep covering at least 60 % of `A`'s rows inside the
implied window.

## Why it is being thrown away

**It fails its own known case.** `SpawnRecord → BattleStatsRecord` at `K = 0x80` — the one embedding
established from the bytes and confirmed twice against a page's own citations — scores:

| | |
|---|---|
| size-matched hits | 11 |
| rows in the implied window `[0x080, 0x242]` | 21 |
| fraction | **0.52**, against a 0.60 threshold |
| verdict | **FAILS** |

Meanwhile it reported `CharacterRenderRecord` as embedding **ten different records** at ten different
offsets — `BattleUnit`, `BattleFormulaScratch`, `PhyreClusterHeader`, `SaveImageHeader`,
`SteeringRecord`, `PClusterHeaderBase`, `MovementContext`, `CharacterRenderSystemTail`,
`PMeshInstance`, `ImageAddressArenaBlockHeader` — at 62–100 %. A record does not embed ten records at
ten offsets. **A detector that misses the true case and reports ten false ones is measuring
something other than structure.**

## The control that quantifies it

Offsets shuffled **within each type**, preserving every type's row count and every row's size, so
only the *arrangement* is destroyed:

| store | type-pairs passing |
|---|---:|
| real | **745** |
| shuffled, seed 1 | 330 |
| shuffled, seed 2 | 314 |
| shuffled, seed 3 | 306 |

**Chance reproduces about 42 % of the result.** A ratio of 2.35× is not a detector — it is a
measurement of row density in a store where sizes are overwhelmingly 1, 2, 4 and 8 bytes, so
near-arbitrary displacements align.

## What would be needed instead

Not a lower threshold. Tuning until the one known case passes, with hundreds of chance hits below it,
is fitting to noise. A usable detector needs evidence the store does not carry: a **writer** that
fills the window as a unit (the `0030C470` block copy is what made the `SpawnRecord` case real), a
**block copy or `memcpy` of the window's exact size**, or a **call passing the window's base by
address** — the census route `arg0+0x80` that the `SpawnRecord` rows already cite. Offset arithmetic
alone cannot distinguish an embedding from two records that happen to be the same shape.

**The `SpawnRecord` finding stands** — it rests on the writer and on two independently confirmed
offsets, not on this sweep, which did not exist when it was found and does not support it now.
