---
system: Loot drops and the enemy chain
category: 13-Rewards-Progression-Economy
status: AUDITED — the loot tables' layout (AE-1..AE-3, section 8c) and what builds and breaks a chain (AE-4, section 8b) are read; every section-7 box is ticked (AE-1..AE-13); status line brought up to date 2026-09-18 (FABLE)
owner_layer: PrimaryOwner:Rewards_Progression_Economy
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN158 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN158 this document cites none of batch R109's 109; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 1
  last_pass: 2026-09-02
  last_pass_state: modulus-universal-verified-exhaustively-AD-6-answered
  crossref_clean: true
  reopened_count: 2
origin: found by a write-scan of the shared gameplay LCG state (AD-5), not by reading this category
registry_slots:
  - "0x02EBF0C0"
---

# Loot drops and the enemy chain

> **Every loot roll in FFXII is `draw % 100` against an authored percentage** — and the draw comes
> from a generator seeded by a **counter**, not a clock. Loot is deterministic.

**PARTIAL.** The roll shapes, the chain rank bounds and the RNG source are read at tier 1. The
profile table layouts and the chain's full state machine are not.

## 1. What the player sees

Kill something, it drops loot — sometimes one item, sometimes several, sometimes none. Chain kills
of the same enemy and the drops get better; break the chain and you start over.

Two things the game never tells you, both established here:

**The rolls are plain percentages.** No hidden pity timer, no accumulating luck — each slot is an
independent `roll under N` check against an authored number.

**The randomness is not random.** Loot draws come from a generator seeded by *how many areas you
have loaded this session*, incremented by one each time. Given the same sequence of area loads and
the same actions, **the same things drop**.

## 2. Native mechanism

### Every roll is `% 100`

`Loot_RollAdditionalItemChance` is the clearest, and it is complete:

```c
bool Loot_RollAdditionalItemChance(short candidate_item_id, short condition_id, int chance_percent)
{
    if (candidate_item_id != -1 && condition_id != -1) {
        if (BattleEncodedId_QueryMode0Positive(condition_id)) {
            /* shared gameplay LCG, inlined */
            a     = g_uSharedGameplayLcgState * 0x41C64E6D + 0x3039;
            b     = a * 0x41C64E6D + 0x3039;
            state = b * 0x41C64E6D + 0x3039;
            g_uSharedGameplayLcgState = state;
            draw  = (state >> 16 & 0x3FF) ^ ((b >> 16 & 0x3FF) ^ ((a >> 16 & 0x7FF) << 10)) << 10;

            return (int)(draw % 100) < chance_percent;
        }
    }
    return false;
}
```

**`(draw % 100) < chance_percent`.** That is the whole rule. `-1` is the null sentinel for both the
item id and the condition id — the same "no item" convention the equipment system uses as `0xFFFF`.

`Loot_RollNormalSlotChance(chance_profile_index, slot_index)` uses the identical inlined draw and
the identical `% 100`, then indexes a profile table at `DAT_02EBF0C0` whose entry count sits at
`+4`.

### Quantity is a four-bucket cumulative weight walk

`Loot_RollNormalSlotQuantityBucket(quantity_profile_index, slot_index)` draws `% 100` and then walks
**up to four cumulative signed-byte weights** at `row + slot_index * 4 + 6`, returning the bucket
index the draw falls into.

So a slot that drops does not carry a fixed count — the **quantity is a second, independent roll**
over at most four authored buckets.

### Profile selection is itself weighted

`Loot_SelectChanceProfileByWeight()` takes no arguments, draws from the same LCG, and performs a
weighted selection to choose *which* chance profile applies. So a single kill involves a chain of
draws: pick the profile, roll each slot, then roll each surviving slot's quantity.

### The enemy chain — four ranks, authored thresholds

```c
void EnemyChain_TryAdvanceRank(void)
{
    count = DAT_022C315C - _DAT_022C3170;                 // chain count minus a base

    if (DAT_022C3158 < 3) {                               // current rank; max rank is 3
        threshold = (&AU_00d0c00e.field_0x47c6)[DAT_022C3158];   // authored, per rank

        if (count <= threshold) {
            if ((DAT_022C3178 & 1) == 0)
                count -= (DAT_022C3158 + 1) * DAT_022C3174;      // penalty scaled by rank

            if (count < 0) count = 0;
            else if (count > 10) count = 10;                      // clamped 0..10
            ...
```

**Ranks run 0..3** — four chain tiers, matching what the game displays. Each rank has its **own
authored threshold**, read from a table at `AU_00d0c00e + 0x47C6` indexed by the current rank.

The penalty term is the interesting part: `count -= (rank + 1) * DAT_022C3174` — the deduction
**scales with the rank you are already at**, so each successive tier is harder to reach than a flat
threshold would make it. A flag bit (`DAT_022C3178 & 1`) can waive the penalty entirely.

`AU_00d0c00e` is the same authored data blob the item-classification function reads — a shared
authored table, not a loot-specific one.

## 3. Key addresses

| Address | Name | Size | Verified |
|---|---|---:|---|
| `00318510` | `Loot_RollAdditionalItemChance` | — | ✅ read, complete |
| `003185D0` | `Loot_RollNormalSlotChance` | — | ✅ read (partial — table walk) |
| `003186F0` | `Loot_RollNormalSlotQuantityBucket` | — | ✅ read (partial) |
| `00318820` | `Loot_SelectChanceProfileByWeight` | — | ✅ read (partial) |
| `003183D0` | `EnemyChain_TryAdvanceRank` | — | ✅ read (partial) |
| `00317ED0` | `EnemyChain_UpdateOnDefeat` | — | ✅ read — see section 8b |
| `00319530` | **chain-rank weighted outcome selector** — **AD-6 answered** (§8d) | — | ✅ read, complete |
| `00318960` | *(profile-count helper)* | — | ✅ read |
| `01EED3B8` | **4 x 7 chain-rank outcome weight table**, every row sums to 100 | — | ✅ read from `.data` |
| `022C3158` | chain-rank index, bounded `0..3`; indexes both `01EED3B8` and the table in `EnemyChain_TryAdvanceRank` | — | ✅ read |
| `022C256C` | `g_uSharedGameplayLcgState` | — | — |
| `02EBF0C0` | loot chance-profile table (count at `+4`) | — | — |
| `022C3158` | current chain rank (0..3) | — | — |
| `022C315C` / `022C3170` | chain count and base | — | — |
| `022C3174` | per-rank penalty factor | — | — |
| `022C3178` | chain flags; bit 0 waives the penalty | — | — |
| `AU_00d0c00e + 0x47C6` | authored per-rank chain thresholds | — | — |

## 4. Data structures and formulas

**The shared LCG draw** (inlined into every function above — see the RNG document):

```
a     = state * 0x41C64E6D + 0x3039
b     = a     * 0x41C64E6D + 0x3039
state = b     * 0x41C64E6D + 0x3039
draw  = (state >> 16 & 0x3FF) ^ ((b >> 16 & 0x3FF) ^ ((a >> 16 & 0x7FF) << 10)) << 10
```

**Additional-item roll — complete:**

```
drops  iff  candidate_item_id != -1
       &&   condition_id != -1
       &&   BattleEncodedId_QueryMode0Positive(condition_id)
       &&   (draw % 100) < chance_percent
```

**Normal-slot roll:**

```
roll = draw % 100                       compared against a profile at DAT_02EBF0C0
                                        entry count at DAT_02EBF0C0 + 4
```

**Quantity bucket:**

```
roll = draw % 100
walk up to 4 cumulative signed-byte weights at  row + slot_index * 4 + 6
return the bucket the roll lands in
```

**Chain rank advance:**

```
count = chainCount - chainBase                       (022C315C - 022C3170)
rank  = 022C3158                                     0..3, max rank 3

if rank < 3 and count <= authoredThreshold[rank]:
    if (chainFlags & 1) == 0:
        count -= (rank + 1) * penaltyFactor          penalty scales with current rank
    count = clamp(count, 0, 10)
```

## 5. Call chain

```
enemy defeated
  -> EnemyChain_UpdateOnDefeat (00317ED0)
       -> foe-class gate + authored exclusion flag (field_0x28 & 2)
       -> bGenusId == DAT_022C3168 ?  count+1 (cap 999/998)  :  count = 0
  -> EnemyChain_TryAdvanceRank (003183D0)
       -> authored threshold for the current rank
       -> rank-scaled penalty, clamp 0..10

loot generation
  -> Loot_SelectChanceProfileByWeight (00318820)     LCG draw -> which profile
     -> Loot_RollNormalSlotChance (003185D0)          LCG draw % 100 -> does the slot drop
        -> Loot_RollNormalSlotQuantityBucket (003186F0)  LCG draw % 100 -> how many
     -> Loot_RollAdditionalItemChance (00318510)      LCG draw % 100 < chance_percent

every draw advances g_uSharedGameplayLcgState, seeded once per area load
  by g_uAreaInitLcgSeedSequence++ in BattleSystem_InitializeAreaState
```

**Upstream:** combat death.
**Downstream:** inventory.

**Do not confuse with:** EXP and LP award, which are a separate computation in this category and use
the `0x80000003` functional gate. Loot has no such gate in the functions read.

## 6. Modding notes

- **Loot chances are plain percentages.** `roll % 100 < chance` — editing an authored chance value
  changes the drop rate linearly, with no hidden modifiers in these functions.
- **Quantity is a separate roll** over at most four buckets. A slot dropping and a slot dropping
  *three* are independent decisions.
- **`-1` is the null item/condition sentinel** here, matching `0xFFFF` elsewhere.
- **Chain has four ranks (0..3)** with per-rank authored thresholds at `AU_00d0c00e + 0x47C6`, and
  the penalty **scales with your current rank** — later tiers are deliberately harder.
- **`DAT_022C3178` bit 0 waives the chain penalty.** That is the single most interesting knob here.
- **Loot is deterministic.** The LCG is seeded from an incrementing counter per area load, so a
  given area load produces a fixed draw sequence. Save-scumming a drop works only if it changes the
  *number of draws* before it.
- **XIIOnline:** loot is rolled on the shared LCG, which is per-client state. **Two clients will
  disagree about drops** unless the LCG is synchronised or loot is made authoritative. This is a
  harder problem than it looks, because the loot functions **inline** the generator — you cannot
  hook `RNG_SharedGameplayLCG_NextU32` and catch them.

## 7. What is not known

- [x] ~~The loot chance-profile table layout.~~ **AE-1 ANSWERED in section 8c** — `+0x04` count,
      `+0x08` stride, `+0x0C` RVA; row holds 5 chance bytes then 5x4 quantity weights.
- [x] ~~The quantity row layout.~~ **AE-2 ANSWERED in section 8c** — 4 signed-byte cumulative
      weights at `row + slot*4 + 6`; stride from the header.
- [x] ~~How many normal loot slots exist per enemy.~~ **AE-3 ANSWERED — five** (`slot_index > 4`
      rejects), each with **four** quantity buckets.
- [x] ~~Which profile index a given enemy uses — the caller is unread.~~ **AE-12 ANSWERED
      2026-09-12 (FABLE):** none of its own — the chance profile is the **chain rank** (0–3) and the
      quantity profile the **same-model tier** (0–3, thresholds 8 / 16 / 24 consecutive kills); the
      enemy contributes only its five item words and two Monograph entries (§8b correction).
- [x] ~~What the profile-row byte at `+0x05` holds.~~ **AE-13 ANSWERED 2026-09-12 (FABLE): the
      row's same-model chain requirement.** `Loot_RollDropEntries` walks the table's four rows
      from row 0 and admits a row only while the second counter `DAT_022C3160` **exceeds** the row's
      signed byte `+0x05` — 8, 16, 24 and −1 in the shipped table (`003181C7`–`003181DE`: a
      negative byte or a counter ≤ the byte stops the walk; `ebp = min(rows admitted, n)`), so the
      count of admitted rows is the **quantity tier** 0–3 — the chain-loot rule, keyed on the model
      streak; the drop *chance* profile is the chain rank (AE-12, and the §8b correction).
- [x] ~~`EnemyChain_UpdateOnDefeat` — how the chain rises and breaks.~~ **AE-4 ANSWERED in section
      8b** — keyed on `bGenusId`; a different genus zeroes the count.
- [x] ~~What the `0..10` clamp in the chain advance feeds.~~ **AE-5 ANSWERED 2026-09-12 (FABLE):
      the column of an authored 3 × 11 chance table.** `EnemyChain_TryAdvanceRank` computes
      `progress = count − base` (`022C315C − 022C3170`); if it exceeds the rank's threshold — the
      three bytes at `00D107D4`, **30 / 50 / 80** for ranks 0 → 1 / 1 → 2 / 2 → 3 — the rank rises
      outright (`00318414`–`00318417`); otherwise the penalty is subtracted (AE-6), the result clamped
      to `0..10`, and a roll `r = LCG % 100` must be **below** `table[rank × 11 + progress]` — the 33
      bytes at `00D106F8`: rank 0 `0,0,0,0,0,0,40,60,80,90,100`, rank 1 `0,0,0,0,0,0,20,30,50,60,100`,
      rank 2 `0,0,0,0,0,0,10,20,30,40,100` (`0031843E`–`003184D7`). So a rank-up is impossible below
      6 net kills, certain at 10, and forced at 30 / 50 / 80; on a rank-up the base is set to the
      count, the pickup counter zeroed and the HUD told (`003184D9`–`003184F6`).
- [x] ~~What `DAT_022C3178` bit 0 represents — it waives the rank penalty.~~ **AE-6 ANSWERED
      2026-09-12 (FABLE): a latched luck roll, and the penalty it waives is the loot you picked up.**
      The penalty is `(rank + 1) × DAT_022C3174`, and `022C3174` is **the number of loot pickups
      collected since the last rank-up** — incremented once per pickup by
      `Loot_CollectWorldPickupAndGrantInventory` (`00319974`), zeroed at every rank-up
      (`003184EC`): collecting loot slows the chain's rank. Bit 0 is recomputed on every same-type
      kill from a roll on the shared gameplay LCG (`022C256C`, inlined, three steps, `% 100`,
      `00317FC1`–`00318032`; [the RNG streams page](../21-RNG-And-Determinism/rng-streams.md)): when the bit is **clear** it turns on if `r < 5`, when
      **set** it stays on if `r ≥ 40` (`00318034`–`0031804B`, stored at `003180C6`) — a 5 % chance
      to start and a 60 % chance per kill to keep; while it holds, the rank advance skips the
      penalty (`0031841D`–`00318424`). The bit is passed to the HUD writer `0028EF70` as its second
      argument and cleared with the chain (`003183A0`).
- [x] ~~Whether chain rank affects loot profile selection.~~ **AE-7 ANSWERED in section 8b — not in
      the functions read.** No chain global appears in any `Loot_*` function.
- [x] ~~Why the chain count has two caps, 999 and 998, split by `FUN_00229E40()`.~~ **AE-9 ANSWERED
      2026-09-12 (FABLE): the language.** `FUN_00229E40` returns the cached **language id**
      `01E02814` ([the locale page](../19-Save-Load-Settings/Language-And-Locale/language-selection-and-locale-ids.md), AV-4; 0 = Japanese). The stored count is capped at 999 in Japanese
      and 998 otherwise **because the HUD number differs by one**: the display calls at
      `00318050`–`00318065` and `00318071`–`00318083` pass `count + 1` when the id is non-zero and
      `count` when it is 0, so both locales show at most 999 — the Japanese HUD counts the chain
      from the second kill, the localised ones from the first.
- [x] ~~What the second counter `DAT_022C3160` tracks.~~ **AE-10 ANSWERED 2026-09-12 (FABLE):
      consecutive kills of the same model.** Its key `DAT_022C316C` is the class row's word `+0x40`
      (`00317F77`–`00317F7B`, stored at `00317FB6`), the model id palette-swaps share (§8b note); it
      counts up to 999 while the model repeats and resets to 0 on a different model of the same type
      (`00317F83`–`00317FA5`); the loot walk reads it (AE-13). Killing Wolves and Alpha Wolves keeps
      it climbing; a Worgen keeps the type chain but restarts it.
- [x] ~~What `pAuthoredArdClass->field_0x28 & 2` marks — enemies excluded from chaining.~~ **AE-11
      ANSWERED 2026-09-12 (FABLE):** the `.ard` class row's "does not chain" flag — set only on the
      54 bosses, Espers, Judges, story foes and Marks in the shipped areas (§8b note).
- [x] ~~What `BattleEncodedId_QueryMode0Positive(condition_id)` tests.~~ **AE-8 ANSWERED
      2026-09-12 (FABLE): "does the party hold at least one free copy of that id".** Mode 0 of the
      query record is `owned − reserved` ([the encoded-id space page](../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md) §2.4), so the test is *possession*. The
      entries that reach it are the spawn row's two additional-drop triples — bytes `+0x42` / `+0x43`
      the chance, words `+0x48` / `+0x4C` the condition, `+0x4A` / `+0x4E` the loot (`0031823A`–
      `00318283`; the decompiled argument names are swapped: `rdx` is the condition) — and over all
      1,146 shipped spawn rows the condition is always one of **eight key items**: `0x8065` Sage's,
      `0x8066` Hunter's, `0x8067` Knight's, `0x8068` Dragoon's, `0x8069` Mage's, `0x806A` Warmage's,
      `0x806B` Scholar's Monograph and `0x806C` the Canopic Jar (bank 12, [the battle text banks](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md)), with the
      loot **Arcana** (`0x204C`, 526 entries), **High Arcana** (`0x204D`, 49), **Pebble** (`0x209D`,
      277) or the enemy's own genus loot (`0x209E`–`0x20EF`) as the candidate. This is the Monograph
      mechanic, read: own the book, and the extra roll runs at the row's chance.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Additional-item roll is `(draw % 100) < chance_percent` | complete body of `00318510` | 1 |
| `-1` is the null sentinel for item and condition | explicit guards in the same body | 1 |
| Normal-slot chance uses the same `% 100` shape | inlined draw + `% 100` in `003185D0` | 1 |
| Quantity is a 4-bucket cumulative weight walk | `003186F0` structure; offsets from the GFZ annotation | 1 / 3 |
| Profile selection is itself a weighted LCG draw | `00318820` takes no argument and draws | 1 |
| Chain ranks are 0..3 | `if (DAT_022C3158 < 3)` in `003183D0` | 1 |
| Per-rank authored thresholds at `AU_00d0c00e + 0x47C6` | indexed read in the same body | 1 |
| Penalty scales with rank | `count -= (rank + 1) * DAT_022C3174` | 1 |
| Value clamped to 0..10 | explicit clamp in the same body | 1 |
| All of these use the shared LCG | the recurrence constants `0x41C64E6D` / `0x3039` appear inline in each | 1 |

### How this document was found

**Not by reading the Rewards category.** It was found by scanning for *writes* to
`g_uSharedGameplayLcgState` while closing an RNG question (AD-5). Seven functions turned up that
write the generator state without calling it — six of them named `Loot_*` or `EnemyChain_*`.

That is worth recording as a technique: **for a small, hot arithmetic routine, the consumers are
found by scanning writes to its state, not by following call edges.** A call-graph census had
already been run over this same generator and found none of these six.

### Why PARTIAL

The three roll *shapes* are exact. ~~The **tables they roll against are not read** — `DAT_02EBF0C0`'s
layout, the quantity row stride, and the number of loot slots per enemy are all open (AE-1 to AE-3).
So this document can tell a modder *how* a loot chance is evaluated but not yet *where the numbers
live*, which is the same gap the render-parameter document had before its data files were located.~~ *Superseded 2026-09-26 (FABLE, Claude Opus 5.5): the tables are read in §8c. **AE-1**: the header is `+0x04` i32 count, `+0x08` u16 stride, `+0x0C` u32 RVA, the shape of the equipment table. **AE-2**: a row begins with five i8 drop chances. This page's own AE-3 box, the number of loot slots, is answered there too. The register's **AE-3** is the loot-pickup chain bonus, answered on 2026-09-12.*

## 8b. Reopened 2026-09-02 - AE-4: what builds a chain, and what breaks it

`EnemyChain_UpdateOnDefeat` (`00317ED0`) runs on every kill:

```c
void EnemyChain_UpdateOnDefeat(FFXII_BattleUnit_Partial *defeated_foe)
{
    if (foe
        && foe->pBkbi
        && foe->pBkbi->wDefinitionSelector[+1] == 1              // foe-class gate
        && (foe->pAuthoredArdClass->field_0x28 & 2) == 0)        // authored exclusion flag
    {
        if ((int)DAT_022C3168 >= 0) {                            // a genus is currently chained
            if (foe->bGenusId == DAT_022C3168) {                 // SAME GENUS -> chain continues
                cap   = FUN_00229E40() ? 0x3E6 : 999;            // 998 or 999
                count = min(DAT_022C315C + 1, cap);
                _DAT_022C3158 = CONCAT44(count, DAT_022C3158);   // store the new count
                DAT_022C3164  = 0;

                if (foe->pAuthoredArdClass[1].aUnknown_012_017 == DAT_022C316C) {
                    DAT_022C3160++;                              // a second counter, clamped 0..999
                }
            }
            ...
            else {
                _DAT_022C3158 = 0;                               // DIFFERENT GENUS -> chain resets
            }
```

### What the player experiences, and why

**The chain is keyed on `bGenusId` - the creature *type*.** `DAT_022C3168` holds the genus
currently being chained. Kill a foe of that genus and the count rises; kill anything else and
`_DAT_022C3158` is **set to zero**.

That is the rule every FFXII player knows - *chain by killing the same kind of enemy* - and this is
the comparison that enforces it.

**Some enemies never count.** `pAuthoredArdClass->field_0x28 & 2` is an authored per-class exclusion
flag checked before anything else. An enemy with that bit set neither builds nor breaks a chain, it
is simply invisible to the system.

> *Named 2026-09-12 (FABLE, AE-11).* `pAuthoredArdClass` is unit `+0xE68`: the **`.ard` slot-0 class
> row** (84 bytes, `02EBF150`) the installer selects by the spawn row's word `+0x00` and reads its
> type byte `+5`, kind `+4`, word `+6` and reward indices from (`0023A6F0`–`0023A6FC`, `0023A8E6`–
> `0023A91C`; [the area-file loader](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md)) — not the stats page. Over the 166 shipped area files (954 class rows
> behind 1,146 spawn rows) **bit 1 of `+0x28` is set on 106 rows naming 54 enemies, every one a boss,
> Esper, Judge, story foe or Mark** — Belias … Zodiark, the five Judges, Vayne, Vayne Novus, The
> Undying, Gilgamesh, Yiazmat, Omega Mark XII, Hell Wyrm, Elder Wyrm, Demon Wall, King Bomb, Rogue
> Tomato, Firemane, Rafflesia, Fury, Chaos, Ahriman … — and clear on all 403 ordinary names; no name
> carries it in one area and not another. So the bit is **"does not chain"**, the boss / Mark flag.
> The same census names the two keys: the chain's own key `bGenusId` is unit `+0x56` = the class
> row's **type byte `+5`** — sixty-four values in the shipped areas (Wolf 4, Wild Saurian 11, Rogue
> Tomato 23, Baknamy 41, the Espers 43, Cactoid 55), the *type* players chain, finer than the sixteen
> genera of bank 13 — and the second key `DAT_022C316C` is the class row's **word `+0x40`**, a
> 434-value **model id** shared by palette-swaps (Wolf and Alpha Wolf 511, Cactite and Cactoid 732,
> each elemental and its Chaosjet), which is what the second counter counts (AE-10 below).

**The count caps at 999**, or **998** (`0x3E6`) on a branch gated by `FUN_00229E40()` - two caps
differing by one, which is an oddity worth flagging rather than smoothing over (**AE-9**).

**A second counter exists.** `DAT_022C3160` advances only when a *different* authored key on the
foe's class record matches `DAT_022C316C`, and is separately clamped to `0..999`. So the system
tracks two things at once, not one. **AE-10.**

### AE-7 answered - no, chain rank does not reach the loot rolls

The question was whether chain rank feeds loot profile selection - the connection a player would
most expect.

**In the functions read, it does not.** All 22 references to the chain globals (`DAT_022C3158`,
`DAT_022C315C`, `DAT_022C3170`, `DAT_022C3174`) fall inside `EnemyChain_UpdateOnDefeat` and
`EnemyChain_TryAdvanceRank`. **Not one appears in any `Loot_*` function.**

> **Corrected 2026-09-12 (FABLE) — the negative was bounded to the wrong six functions.** The
> caller that was "not read", `Loot_RollDropEntries` (`003180F0`, from
> `BattleUnit_ProcessDefeatRewardsAndLoot`), reads three chain globals: it takes **the chance
> profile index from the chain rank** `DAT_022C3158` (`00318116`) — or from
> `Loot_SelectChanceProfileByWeight()` when `DAT_022C3164` is positive (`0031815C`–`0031816A`) — and
> derives **the quantity profile index from the same-model counter** `DAT_022C3160`: it walks the
> loot profile table's rows from row 0 and counts those whose signed byte `+0x05` the counter
> exceeds (`00318181`–`003181EF`). The shipped table (`battle_pack.bin` directory `+0x1C`, bound to
> `02EBF0C0` at `00236CD7`) has **exactly four rows** — the four chain levels:
>
> | row | slot chances (%) | `+0x05` | quantity weights, slot 0 |
> |---:|---|---:|---|
> | 0 | 40 / 25 / 3 / 1 / 100 | 8 | 100 / 0 / 0 / 0 |
> | 1 | 45 / 30 / 6 / 2 / 100 | 16 | 65 / 35 / 0 / 0 |
> | 2 | 50 / 35 / 8 / 3 / 100 | 24 | 30 / 50 / 20 / 0 |
> | 3 | 55 / 40 / 12 / 5 / 100 | −1 | 0 / 60 / 30 / 10 |
>
> So chain rank 0–3 raises the four slots' drop chances from 40 / 25 / 3 / 1 to 55 / 40 / 12 / 5 (the
> fifth slot is always 100), and the same-model streak — more than 8, 16, 24 consecutive kills of
> one model — moves the quantity profile from row 0 (always one) to rows 1, 2 and 3 (up to four of
> an item). Then each of the spawn row's five drop words `+0x28`–`+0x30` (`0xFFFF` = none) is rolled
> with `Loot_RollNormalSlotChance(rank, slot)` — a slot whose chance fails is retried through
> `0017D340()` against the slot index (`0031820C`–`00318213`) — and, on success, its quantity with
> `Loot_RollNormalSlotQuantityBucket(tier, slot) + 1` (`003181F8`–`00318238`). **AE-7's answer is
> therefore reversed: chain rank sets the drop chance, and the model streak the quantity.**

`Loot_SelectChanceProfileByWeight` takes **no arguments** and reads no chain global, so its weighting
is not rank-dependent. `Loot_RollNormalSlotChance` receives `chance_profile_index` from a caller.

So if chain rank influences drops, it does so by **the caller choosing a different profile index** -
a path that has not been read. The negative is bounded to the six functions examined, and recorded
that way rather than as "chain does not affect loot".

### A seventh sighting of the foe-class gate

`wDefinitionSelector[+1] == 1` gates this function too. That constant now appears in **seven**
independently-read functions.

## 8c. Reopened 2026-09-02 - AE-1, AE-2, AE-3: the loot table, read

Both roll functions were read in full. The table layout is now exact.

### Five slots, four quantity buckets each

Both `Loot_RollNormalSlotChance` and `Loot_RollNormalSlotQuantityBucket` reject `slot_index > 4`,
and the quantity walk runs exactly four iterations:

> **Every enemy has five normal loot slots, and each slot's quantity is chosen from four buckets.**

### The table

```c
bool Loot_RollNormalSlotChance(int chance_profile_index, uint slot_index)
{
    roll  = <inline LCG> % 100;
    count = DAT_02EBF0C0 ? *(int *)(DAT_02EBF0C0 + 4) : 0;

    if (chance_profile_index < 0 || chance_profile_index > count - 1 || slot_index > 4)
        return false;

    base   = ImageAddress_ResolveRuntimePointer(*(dword *)(DAT_02EBF0C0 + 0xC));
    stride = *(ushort *)(DAT_02EBF0C0 + 8);

    return roll < (char)base[stride * chance_profile_index + slot_index];
}
```

```c
uint Loot_RollNormalSlotQuantityBucket(int quantity_profile_index, uint slot_index)
{
    roll = <inline LCG> % 100;
    /* same bounds check, same table, same stride */
    row  = base + stride * quantity_profile_index;

    cum = 0; bucket = 0;
    for (i = 0; i < 4; i++) {
        cum += (char)row[slot_index * 4 + 6 + i];     // signed byte weight
        if (roll < cum) return bucket;                 // first bucket the roll falls into
        bucket++;
    }
    return cum;
}
```

**The row layout:**

```
Loot profile table    header at DAT_02EBF0C0
  +0x04   i32     profile count
  +0x08   u16     row stride
  +0x0C   u32     RVA -> row array   (via ImageAddress_ResolveRuntimePointer)

Profile row           (stride bytes)
  +0x00 .. +0x04     i8[5]      per-slot drop chance, as a percentage
  +0x05              -          unaccounted
  +0x06 + slot*4     i8[4]      per-slot cumulative quantity weights   (slots 0..4 -> +0x06..+0x19)
```

**Chance and quantity live in the same row**, indexed off the same profile - so a "profile" is a
complete drop table for one enemy class: five chances followed by five groups of four weights.

**Both values are signed bytes** compared against a `0..99` roll, so a chance of `0` or negative
never drops and `100+` is unrepresentable - the maximum effective chance is 127, i.e. always.

### The header format is shared with the equipment table

```
DAT_02EBF0C0  (loot)        +0x04 count   +0x08 stride   +0x0C RVA
DAT_02EBF0F8  (equipment)                 +0x08 stride   +0x0C RVA
```

The equipment definition table documented in the Items category uses **the same header shape** -
stride at `+0x08`, an RVA at `+0x0C` resolved through `ImageAddress_ResolveRuntimePointer`. Two
unrelated subsystems, one authored-table convention.

That is now the **fourth** sighting of `ImageAddress_ResolveRuntimePointer` as the access path for
authored data (equipment, resource sections, the weighted-id table, and now loot), which makes it a
general mechanism rather than a per-system detail.

### What this does not close

The **profile index** passed to both functions still comes from the caller, unread - so which
profile a given enemy uses is unknown, and AE-7's negative (chain rank does not reach the loot
rolls) still leaves that path open. **AE-12.**

The byte at row `+0x05` is not touched by either function. **AE-13.**

## 9. Related

- [`../21-RNG-And-Determinism/rng-streams.md`](../21-RNG-And-Determinism/rng-streams.md) — the shared LCG, its seeding, and why loot is deterministic
- [`experience-and-license-point-award.md`](experience-and-license-point-award.md) — EXP and LP, the other half of this category
- [`../12-Items-Equipment-Shops-License/item-id-encoding-and-equipment-compatibility.md`](../12-Items-Equipment-Shops-License/item-id-encoding-and-equipment-compatibility.md) — the null-sentinel convention and where dropped items land
- [`../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md`](../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md) — the other major LCG consumer

## 8d. Falsification pass 2026-09-02 — the universal holds, and AD-6 is answered

**Attack chosen.** The headline is a **universal**: *"Every loot roll in FFXII is `draw % 100`."*
Two of the four roll sites were marked *read (partial)*, and a universal asserted from partial reads
is where a counter-example hides. The killer looked for was **any roll site using a different
modulus or a different comparison**.

**Result: SURVIVED, now verified exhaustively.** All **seven** roll sites in the family were
decompiled complete and every one computes `% 100`:

| Function | Modulus | Comparison |
|---|---|---|
| `Loot_RollAdditionalItemChance` (`00318510`) | `% 100` | `< chance_percent` |
| `Loot_RollNormalSlotChance` (`003185D0`) | `% 100` | `< row[slot]` |
| `Loot_RollNormalSlotQuantityBucket` (`003186F0`) | `% 100` | `< cumulative` |
| `Loot_SelectChanceProfileByWeight` (`00318820`) | `% 100` | `< cumulative` |
| `EnemyChain_TryAdvanceRank` (`003183D0`) | `% 100` | threshold |
| `EnemyChain_UpdateOnDefeat` (`00317ED0`) | `% 100` | threshold |
| `00319530` (**AD-6**) | `% 100` | `< cumulative` |

**A near-miss worth recording.** A regex scan for the modulus reported that `003186F0` and
`00318820` had none — which would have falsified the headline. They do have it; the decompiler had
wrapped `%` and `100` onto separate lines, and the pattern did not span lines. **The bodies were
read before the finding was believed**, per the positive-control rule. This is the fourth
instrument-shaped blind spot recorded in this database and the first caught *before* it reached a
document; it is tabulated in
[`../_index/EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md).

### The mechanism the document was missing: one draw, cumulative thresholds

Three of the seven are not simple pass/fail rolls. They are **roulette-wheel weighted selections**,
and the important property is that **the LCG advances exactly once per call** — the single draw is
then compared against a *running cumulative total*:

```c
draw = LCG_next() % 100;          // ONCE, before the loop
acc  = 0;
for (i = 0; i < n; i++) {
    acc += weight[i];
    if (draw < acc) return i;     // first bucket whose cumulative total exceeds the draw
}
```

This matters for two reasons. It is why weight rows must **sum to 100** — and they do (below). And
it means a weighted selection costs **one** LCG step, not one per candidate, which is load-bearing
for this document's determinism claim: the number of draws per kill is fixed by the *number of
selections*, not by table sizes.

### AD-6 answered: `00319530` is the chain-rank outcome selector

The function was previously listed only as *"unowned; writes LCG state"*. Read complete, it is 34
lines and entirely self-contained:

```c
int FUN_00319530(void) {
    draw = LCG_next();
    if (3 < DAT_022C3158) return 0;              // chain index guard, 0..3
    acc = 0; out = 0;
    for (i = 0; i < 7; i++) {
        acc += ((byte *)&DAT_01EED3B8)[i + DAT_022C3158 * 7];
        if ((draw % 100) < acc) break;
        out++;
    }
    if (out == 7) out = 0;                        // fallback
    return out;
}
```

`DAT_022C3158` is bounded `0..3` and is **the same global that indexes the table in
`EnemyChain_TryAdvanceRank`** — so it is the chain rank. (The *name* is inference; the bound, the
stride and the shared use are read.)

### The authored table at `01EED3B8`

Read straight out of `.data` — 4 rows of 7 bytes, and the bytes after row 3 are zero, confirming
exactly four rows:

| Chain rank | Outcome weights (0–6) | Row sum |
|---:|---|---:|
| 0 | `100, 0, 0, 0, 0, 0, 0` | **100** |
| 1 | `80, 10, 10, 0, 0, 0, 0` | **100** |
| 2 | `50, 20, 20, 5, 0, 5, 0` | **100** |
| 3 | `40, 25, 25, 0, 5, 0, 5` | **100** |

**Every row sums to exactly 100.** That is independent structural confirmation of the `% 100` rule:
the authored data is written to be consumed by a modulo-100 cumulative comparison, and would be
malformed under any other modulus.

**What the player experiences.** This is the numeric core of *"keep your chain up for better
drops"*. At chain rank 0 outcome 0 is certain — there is no variety at all. Rank 1 opens outcomes 1
and 2 at 10% each. Rank 2 halves outcome 0 to 50% and unlocks outcomes 3 and 5 at 5% each. Rank 3
drops outcome 0 to 40%, pushes outcomes 1 and 2 to 25% each, and swaps in outcomes 4 and 6 at 5%.
The rarest results exist **only** at high chain, and even there they are one-in-twenty.

**Not established:** what the seven outcomes *are*. The selector returns an index `0..6`; which loot
tier or table that indexes has not been traced. Registered as **AE-3**.

> **AE-3 answered 2026-09-12 (FABLE): the seven outcomes are the loot-pickup chain bonus — nothing,
> 10 % HP, 10 % MP, Protect for the picker, Protect for the party, Shell for the picker, Shell for
> the party.** The selector's one caller is `BattleUnit_RunPeriodicCombatMaintenance`
> (`00310DB0`), on the path that collects a world pickup the unit overlaps
> (`Loot_FindOverlappingPickupIndex` `002FB150` → `Loot_CollectWorldPickupByIndex` `00319A00`,
> `00311105`–`00311141`) and only for a **party** unit (`[+0x698]+5 == 0`, `00311130`). It then
> calls `00319530` (`00311146`) and, for an outcome `1`–`6`, gathers the mapped party members
> (`BattleStats_GetByMappedBattleSlot(i, 1)`, slots 0–8, skipping any that are out of play unless
> the field's bit-15 waiver holds, `00311173`–`003111B7`) and, for each, resolves and applies
> **action `0xF5` — the row named "Chain Bonus"** (bank 0; recipe 102, [the action definition row](../07-Combat-Action/Action-Definition-Row/the-action-definition-row.md)) —
> through `BattleFormula_ResolveTargetResult` and `BattleFormula_ApplyTargetResult`
> (`0031124D`, `0031126C`) with a result record whose flag byte carries a **variant** in bits 3–4:
> `table[outcome]` at `00D102C0` = `{−1, 0, 1, 2, 2, 3, 3}`. **Outcomes 3 and 5 apply to the
> picker alone** — the member's owning actor handle must equal the unit's own (`003111DD`–
> `003111F1`); 4 and 6 apply to everyone gathered. Recipe 102 is the single slot 201 (`003908A0`),
> which switches on the variant:
>
> | outcome | variant | what slot 201 does |
> |---:|---:|---|
> | 0 | — | nothing (the selector's 0 skips the whole block, `00311150`) |
> | 1 | 0 | **HP gain = 10 % of the HP cap** — `cap × 10 / 100` into the gain slot `02AEE008`, the cap being `max(HP, 1)` under Disease, else max HP doubled under Bubble (`00390A4E`–`00390A94`; [the HP write](../08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md)) |
> | 2 | 1 | **MP gain = 10 % of max MP** — `+0x28 × 10 / 100` into `02AEE010`, 0 when either MP layer byte is negative (`00390A17`–`00390A46`) |
> | 3 / 4 | 2 | **Protect** (status 18): refused if already present, or by the status row's `+6` bit 5 / bit 8 flags for the target's kind (`003908DF`–`003909E3`, `02AEDFBC = 1`), else added through `00387BB0` |
> | 5 / 6 | 3 | **Shell** (status 19), the same gate ([the thirty-two statuses](../10-Status-Periodic-Terminal/the-thirty-two-statuses.md)) |
>
> So at chain rank 0 a pickup gives nothing; rank 1 adds a 10 % chance each of the HP and MP
> tenths; rank 2 halves "nothing" and adds Protect (5 % picker-only, 5 % party-wide); rank 3 pushes
> HP and MP to 25 % each and swaps the Protect rolls for Shell — the authored table of §8d read
> against the code that consumes it.

### Row layout refined

The consumers give exact offsets into a chance-profile row, and they are not quite contiguous:

```
row + 0x00 .. 0x04   5 chance bytes, one per slot   (Loot_RollNormalSlotChance: row[slot])
row + 0x05           NOT read by any consumer seen
row + 0x06 .. 0x19   5 slots x 4 quantity weights   (row + slot*4 + 6 + bucket)
row + 0x22           per-profile selection weight   (Loot_SelectChanceProfileByWeight)
```

Section 8c described the row as *"5 chance bytes then 5x4 quantity weights"*, which implies the
quantity block starts at `+0x05`. It starts at **`+0x06`**, and bytes `0x1A`–`0x21` are likewise
unaccounted for. Both slot indices are validated with `4 < slot_index`, confirming **5 slots**.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CombatFormula — SERVICE and CLIENT.** Cited functions call `BattleFormula_ResolveTargetResult`, `BattleFormula_ApplyTargetResult`, `BattleStats_ModifyPrimaryResource`, `BattleStats_GetByMappedBattleSlot` and `BattleStats_GetOwningActorHandle`. They are called by `BattleFormula_ResolveCandidateStatusApplications` and a 516-byte formula body.

*Citation spellings (R5), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **UI — CLIENT.** A 7-byte getter this page cites is also read by a 1,692-byte UI body.
- **Presentation — CLIENT.** The same 7-byte getter is read by Presentation bodies of 610, 896 and 6,441 bytes.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**ActorEntity — SERVICE and CLIENT (4 edges).** `Loot_FindOverlappingPickupIndex` `002FB150` calls `Actor_GetWorldPosition` `00265020` and `ActorRuntime_GetClass3FloatPair` `00265090`; the maintenance tick `BattleUnit_RunPeriodicCombatMaintenance` `00310DB0` calls `BattleUnit_FindByCombatantId` `0031B770` and is called by `BattleUnit_UpdateLifecycleAndCombatFrame` `00233F70`. The pickup test reads the unit's world position and a pair of floats from its class-3 runtime context to test each pickup for overlap, and the unit's per-frame lifecycle is what runs the tick that collects pickups and rolls the chain bonus.

**CombatAI — SERVICE (1 edge).** `00310DB0` calls `BattleEnmity_UpdatePeriodicDecay` `00321530`. The same tick that runs the pickup and chain-bonus path also decays enmity once per pass; the two share a caller and no data.

**CombatAction — SERVICE (3 edges).** `00310DB0` calls `BattleUnit_TryTriggerNearbyAuthoredFieldAction` `002F8060`, `BattleTarget_ComputeGlobalEligibilityMask` `0030B770` and `BattleTarget_ComputeUnitEligibilityMask` `0030B7F0`. The tick also fires nearby authored field actions and computes the target-eligibility masks; these are other duties of the tick, not part of the loot or chain path this page follows.

**CoreRuntimeScheduling — SERVICE (2 edges).** `00310DB0` calls `GameClock_GetRawTickCounter` `0032A150`, and `EnemyChain_UpdateOnDefeat` `00317ED0` calls `00229E40`, a 7-byte getter of one scheduling global. The tick reads the raw game clock, and the chain update reads the scheduling global only to decide whether the count it hands to the HUD chain counter is increased by one.

**Gameplay — SERVICE and CLIENT (3 edges).** `00310DB0` calls `BattleEncodedId_IsValidForClass` `00322C50`; `BattleSystem_ResetRuntimeState` `00237DF0` calls the chain teardown `003183A0`; `Loot_RollAdditionalItemChance` `00318510` calls `BattleEncodedId_QueryMode0Positive` `0030B0E0` and draws only when it answers non-zero. A battle-system reset clears the chain record, and the extra-item roll is gated on the encoded-id query for the item.

**Party — SERVICE (1 edge).** `00310DB0` calls `PartyFocus_IsCurrentPackedActorHandle` `003273B0`. The tick asks whether the unit is the player's focus; the pickup path itself is gated on the unit being a party member (the stats kind byte), not on focus.

**Script_VM_Native_Bridge — CLIENT (2 edges).** `0033FED0` and `0034BA00` call `00229E40`. Two script-bridge bodies read the same scheduling global the chain update reads; they do not touch the chain.

**Status_Periodic_Terminal — SERVICE and CLIENT (7 edges).** The tick `00310DB0` calls `002FB150`, `Loot_CollectWorldPickupByIndex` `00319A00` and the chain-rank outcome selector `00319530`, and also `BattleUnit_ResolvePeriodicPrimaryResourceRecoveryStep` `002F9400` and `BattleFormula_BuildPeriodicStatusResult` `00385DF0`; `BattleFormula_AppendStatusAddOperation` `00387BB0` calls `BattleStatus_ComputeDefaultShortTimer` `003876D0` and `BattleStatus_ComputeDefaultDwordParameter` `00387730`. The periodic tick is where a pickup is collected and the chain bonus is rolled, and the Protect/Shell outcomes are added through the status-add operation, which takes its default timer and parameter from the status layer.

**WorldAreaField — SERVICE and CLIENT (2 edges).** `00310DB0` calls `FieldData_GetActiveFieldRecordBit15` `00377C20`, and `BattleSystem_InitializeAreaState` `002342F0` calls `003183A0`. The bonus's party gather skips out-of-play members unless the field's bit-15 waiver holds, and entering an area clears the chain record.

## The `00317ED0` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`00317ED0` `EnemyChain_UpdateOnDefeat` (149 B) — the defeat-side chain
update. Gates: `rax = [rcx+0x698]` unit definition, `byte[rax+5] == 1`
(`00317EF8`); `[rcx+0xE68]` runtime object, `byte[rax+0x28] & 2`
(`00317F09`); `byte[rdi+0x56]` vs `dword[022C3168]` (`00317F21`/
`00317F25`); `00229E40` (`00317F2D`), then `edx = 0x3E7` — the 999
chain cap — compared against `dword[022C315C]` (`00317F34`/`00317F4A`).

| member | role | interior |
| --- | --- | --- |
| `0028EF00` | chain-record field writes on the `[0209BE80]` manager — `dword[+0x7C7C] = 0` (`0028EF07`), `word[+0x7C78] = cx` (`0028EF39`), `word[+0x7C82] = dx` (`0028EF47`) | [`0028EF39`](../_index/ADDRESS-INDEX.md) |
| `0028EF70` | chain-record update — `0028F0C0` helper (`0028EF7F`), then `word[[0209BE80]+0x7C82] = di` (`0028EFA9`) | [`0028EFA9`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00229E40`, `0028F0C0`. The chain
counters are `dword[022C315C]` (current, capped at 999) and
`dword[022C3168]`; the record fields `+0x7C78`/`+0x7C7C`/`+0x7C82` live
on the shared `[0209BE80]` manager.

## The `003183D0`/`00318820` exclusive-subtree pair — both roots bound (SWE2-FRONTIER, followup queue)

`003183D0` (`EnemyChain_TryAdvanceRank`, ~29 B) — `022C315C` minus
`022C3170` delta under `movsxd 022C3158` (`003183D6`/`003183E6`) — the
same chain-counter bank `00317ED0` publishes.

| member | role | interior |
| --- | --- | --- |
| `0028EF50` | `0209BE80` base — `or dword[+0x7C7C], 4`, `word[+0x7C82] = cx` (`0028EF57`/`0028EF65`) | [`0028EF57`](../_index/ADDRESS-INDEX.md) |

`00318820` (`Loot_SelectChanceProfileByWeight`, ~155 B) — opens with
`imul eax, [022C256C], 0x41C64E6D` — the MSVC LCG advance on the loot
stream (`00318834`).

| member | role | interior |
| --- | --- | --- |
| `00318960` | `qword[02EBF0C0]` base + `edi = 0` walk (`0031896F`/`00318976`) | [`0031896F`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## SWE2-EC7-26 update (2026-09-18) — `003183A0` chain-record reset

`003183A0` (42 B) is the chain teardown this page already names:
`dword[022C3178] &= ~1`, `022C3170`/`022C3160`/`022C3158` zeroed, and
`022C3168 = -1` — the four-qword record plus flag bit cleared when the
chain ends. Interior anchor `003183BE` (the `-1` store).
