---
system: Where a stat number comes from
category: 08-Combat-Formula
status: DOCUMENTED — owner read done (owner re-status 2026-09-30, OPUS, on FABLE's 2026-09-30 content pass as accepted by SWE2-AUDIT-SEM's review auditsem-review-dd-gameplay-0930); every register row it names is closed. The byte-width ambiguity ~~remains open~~ is CB-12, ANSWERED 2026-09-14; CB-5, CB-9, CB-10 and CB-13 are ANSWERED; and every item of the page's own "does not claim" list is now answered on the page. No open residue is left
owner_layer: PrimaryOwner:CombatFormula
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 8 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-03
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: first-read-repos-55
  crossref_clean: false
  reopened_count: 0
---

# Where a stat number comes from

`BattleStats_RebuildEffectiveStatsAndAffinityState` at **`002FEF30`**, 2,859 bytes. **A previous pass
declared this gap deliberately** — *"I read its prologue and base-stat entry, not its contribution
formula"* — and the cut's body-versus-claim ranking put it fifth of twenty-two on its own.

## What the player sees

**Every effective stat is a sum, computed from nothing, in a fixed order:**

```
base (from a table)  +  equipment  +  status bonuses  ->  clamp
```

**The output block is zeroed at entry** before any source is read — 36 bytes, four qwords and a dword —
so **nothing survives from the previous computation.** This is the same architecture as the auto-status
rebuild one level up: *there is no un-apply step because nothing is ever applied in place.*

## The caps, read from the code

| written to | cap |
|---|---:|
| the main value | **9,999** for the party side · **1,000,000,000** for foes |
| — when the actor type falls in the `0x1B … 0x27` band | **32,767** |
| the second value | **999** |
| four stats (`+0x06`, `+0x07`, `+0x08`, `+0x09`) | **99** each |
| three values (`+0x0A`, `+0x0B`, `+0x0C`) | **255** each |
| four values (`+0x0D`, `+0x0E`, `+0x0F`, `+0x10`) | **100** each |
| one byte (`+0x13`) | **3** |

> **The famous 9,999 is a `cmp` in this function**, and it applies **only to the party side** — foes
> are clamped a hundred thousand times higher. *(Qualified 2026-09-30, FABLE: 32,767 is not a third alternative.
> It is a second store over the first. It is taken only for party rows `0x1B`–`0x27`, the Espers (`002FF7E5`–`002FF805`),
> as the [contract](CONTRACT-stat-derivation.md)'s D-4 corrective says. The foe cap is the literal `0x3B9ACA00`,
> 1,000,000,000, at `002FF7C3`.)* **And the 13-value actor-type band gets its own cap of
> 32,767**, which is the fourth distinct behaviour that band has been found to control.

**Every clamp is two-sided:** a negative intermediate is written as **0**, not as its negative. So a
stat cannot be driven below zero by subtractive equipment or statuses — **the floor is in the writer,
not in the sources.**

*Qualified 2026-09-30 (FABLE):* the main value (max HP) floors at **1**, not 0. It is compared with `r15 = 1` at
`002FF7B1` and replaced by it at `002FF7B6`. Every other clamp floors at 0 (for example MP at `002FF80D`–`002FF812`).
This matches the [battle-stats field map](Battle-Stats-Record/the-battle-stats-record-field-map.md) (`+0x024`,
`clamp(sum, 1, cap)`) and the [stat-derivation contract](CONTRACT-stat-derivation.md) §10.

## The party side: a table plus level

Base values come from a per-actor-type record (`02EBF130`, indexed by the type byte at `+0x04`) through
two helpers that take ~~the **level** at `+0x08`~~ the stats record's base HP (`+0x08`) and base MP (`+0x0C`), plus four
`float` fields converted to `int`. **Two ~~dwords of affinity flags~~ status-word masks are OR-ed in** from the same record.

*Corrected 2026-09-30 (FABLE), from the bytes:*
- `+0x08` is not a level: the [battle-stats field map](Battle-Stats-Record/the-battle-stats-record-field-map.md) names it
  the base HP, and the helpers scale it by the party row.
- `002F8E50` (30 B) returns `(row[+0x18] + 1) × stats[+0x08] × row[+0x19] / 100` into the HP slot (`002FF06F`–`002FF08B`).
- `002F9180` (21 B) returns `(s16)stats[+0x0C] × row[+0x1D] / 100` into the MP slot (`002FF080`–`002FF0A6`).
- Both divide through the reciprocal `0x51EB851F` with `sar 5`, a signed division by 100 that truncates toward zero.
- The two dwords are status masks, not affinity flags. Row `+0x4C` is ORed into output `+0x14`, stats `+0x38`, the
  refused-status word (`002FF0A3`, `002FF0D3`). Row `+0x48` is ORed into output `+0x18`, stats `+0x3C`, status word 2
  (`002FF0D6`, `002FF0D9`).
- The [UQ-80 record](../_index/candidates/uq80-table-field-coverage/README.md) names the same row bytes (`chr_data`
  `+0x18`, `+0x19`, `+0x1D`, `+0x48`, `+0x4C`).

## The foe side: base plus growth × the experience difference

Four records are resolved — by type byte, then by two ids **read out of the first** (`+0x22`, `+0x24`),
then a fourth by its `[+0x00]`. Then every stat is

```
stat = growth[field] * (rec[+0x1C2] - rec[+0x88]) + base[field] + own[field]
```

> **`rec[+0x1C2] − rec[+0x88]` is the same difference the experience formula multiplies by.** One
> quantity drives both **how strong a foe is** and **how much it is worth** — read independently in two
> functions, and it is the tightest cross-check in the combat category.

**And two of the growth terms are conditional on flag bits in the first record** (`+0x15` bits 0 and
1), which also **suppress the corresponding equipment contributions later** — the same two booleans
gate a base term and an equipment term.

> **CB-9 answered 2026-09-12 (FABLE) — the "flagged-but-dead" rows are not a contradiction.** The
> first record is the `.ard` slot-2 row ([the .ard loader page](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md)); over the 166 `in` areas its 1,146 rows split
> **1,020 with bit 1 clear / 126 with bit 1 set**, reproducing the earlier census exactly. The bit is a
> **source selector, not a liveness promise**: when it is set the block and magick-evade terms come
> from the row's own bytes `+0x02` / `+0x03` (and their growth from the slot-6 row the word `+0x24`
> names, bytes `+0x28` / `+0x29`) instead of the shield — so a flagged row whose own bytes are zero
> simply has **no shield-side evasion at all**, by authoring. Which rows those are: 30 of the 126 have
> `+0x02 = +0x03 = 0`, and every one names **Imperial Swordsman** (Nalbina Fortress `naf_a` / `naf_b`
> at level 255, Rabanastre `rsn_b` / `rsn_c` and `dor_d` at level 6), **Urutan-Yensa** (`enw_a`) or
> **Baknamy** (`bog_b`) — story-scene soldiers and two field enemies with no block. The earlier count of
> 43 rested on a "dead growth pair" predicate the ledger row does not define; the three natural readings
> (the slot-6 row's `+0x28` / `+0x29` zero, its `+0x26`–`+0x29` zero, the whole row zero) give 47, 47
> and 47 flagged-and-zero rows against 470, 265 and 262 unflagged-and-zero — none of which is a
> contradiction either, because a zero growth term is a valid authored growth. (A note on the names:
> a spawn row's name word at or above `0x4000` is `bank << 11 | index`, not a plain bank-8 index.)

> *CB-10 answered 2026-09-12 (FABLE): bit 4 of `+0x15` has no consumer anywhere in `.text`.* The
> search that "had not been run" was run three ways over every function in `functions.tsv`:
> (1) every immediate-form bit test on a `+0x15` byte (`test` / `and` / `or` / `cmp byte ptr
> [reg + 0x15], imm`) — ten sites, all on other records, testing bits 0 or 1 only; (2) every
> `movzx` / `mov` of a `+0x15` byte followed within five instructions by a `test` / `and` / `bt` on
> the loaded register — twenty-four sites, and the rebuild's own is among them (`002FF325 movzx
> r13d, byte ptr [r13 + 0x15]` → `002FF32A test r15b, r13b` with `r15b = 1`, the bit-0 test this
> page reads), with the masks `1`, `2`, `4`, `6`, `0xF`, `3` and never `0x10`; (3) the `bt reg, 4`
> form — none. So the flag is authored (set on 126 rows) and read by nothing; a reimplementation
> may carry it for fidelity and cannot diverge on it. The one form the census would miss is a
> wider load (`word` / `dword` at `+0x14`) masked with `0x1000`, which the same scan over `+0x14`
> loads did not find either.

## What indexes the fourth record, settled by a second consumer

**The pair frontier's fifth candidate: `02EBF150`, five touchers, three documented, no document citing
two of them.** This function is one of them; comparing it with `BattleUnit_ApplyUnitDefinition`
(`0023A570`) settles what indexes that slot.

```asm
0023A6A1  mov   rdx, qword ptr [0x02EBF150]
0023A6AD  mov   ecx, dword ptr [rdx + 0x4]     ; the slot's COUNT
0023A6B4  movzx eax, word ptr [rsi]            ; the id: the u16 at offset 0 of the record
0023A6B7  dec   ecx
0023A6B9  cmp   eax, ecx
0023A6BB  ja    <reject>                       ; id > count-1  ->  refuse
0023A6C6  mov   ecx, dword ptr [rdx + 0xc]     ; the slot's resolver handle
0023A6C9  call  0x0020E600
```

> **That is the class validator's rule — `0 <= id < count`, with the count at `slot + 4` — performed
> inline instead of called.** The same function *also* calls the validator elsewhere, so **this is not
> ignorance of the helper; it is one site choosing to inline the check it needs.**

**And the id is the `u16` at offset 0 of a unit-definition record — the same field this function uses**
to reach `02EBF150` for the foe base table. **Two consumers, two routes, one indexing rule.**

**ANSWERED 2026-09-03: `02EBF150` is class 4**, extracted from the validator's own 32-entry jump table
rather than from any caller. **What is established here is how it is addressed** — from two functions
that never mention each other — **and the class number now names it in the registry.**

## Equipment: five slots, and every item contributes twice

Each of five ids is validated by `BattleEncodedId_IsValidForClass(6, id)` and resolved with a
`(id − 0x1000)` stride. **Its kind decides which of three stat pairs it adds to** — and then, **whatever
its kind, every valid item also adds through a sub-record**: two `u16`, four bytes, and **five separate
flag fields OR-ed into the output.**

> **A weapon and a piece of armour take different branches for their stat pair and the same path for
> everything else.**

The three branches, read 2026-09-11 (`0031E9A0` classifies the item row; `002FF451`–`002FF4A4`):
**kind 1 (weapons)** adds row `+0x1A` to attack and row `+0x1D` to **weapon evade** (stats `+0x32`)
unless the definition's `+0x15` bit 0 substitutes the `.ard` column; **kind 2 (shields)** adds row
`+0x18` to **shield evade** (stats `+0x33`) and `+0x19` to **magick evade** (`+0x34`) unless bit 1;
**kind 3 (armour)** adds row `+0x18` to defence and `+0x19` to magick resist. The four rate columns
of the `.ard` map below are these same four evasions — [the scratch block](Scratch-Block/the-formula-scratch-block.md)
§2.3 is where the roller spends them.

## Statuses that add flat bonuses — three tables, 44 ids

```asm
002FF708  test byte ptr [rdx + rdi + 0x68], r9b     ; layer 0
002FF70F  test byte ptr [rdx + rdi + 0x78], r9b     ; layer 1
002FF746  movzx ecx, byte ptr [rbx + ... + 0xBF02B0] ; the id list
002FF754  imul ecx, edx                              ; id x record stride
```

Three authored lists — **16, 16 and 12 status ids** — each mapped to a `u16` in a record indexed by the
status id. **A status in either layer counts**, and **which list an id is in decides which stat it
raises.**

> **Forty-four statuses grant flat stat bonuses, and the grouping is data, not code.** Moving an id
> between the three lists changes which stat it boosts without touching a single instruction.

## The tail: a stat change can cancel the action in flight

When the party side is being rebuilt and two specific flag bits changed (`^ … & 0x8000020`), the engine
**cancels the unit's in-flight action** — with three exceptions guarding action ids `0x113` and `0x95`
— then clears a batch of runtime fields and calls `00307D10`.

*Anchored 2026-09-30 (FABLE):*
- **The guards.** The tail runs only for a party record (`edi`, the class byte `+0x05`, is 0: `002FF970`) on a live
  unit (`[rsp+0x64]`, set when the owning unit was found: `002FEF73`–`002FEF89`, tested at `002FF978`), and only if
  bits 5 or 27 of status word 2 changed. The test XORs output `+0x18` (stats `+0x3C`) with the value saved at entry
  (`002FEF82`) and tests `0x8000020` (`002FF982`–`002FF98E`).
- **Those bits are Confuse (5) and Berserk (27)**, the pair [the thirty-two statuses](../10-Status-Periodic-Terminal/the-thirty-two-statuses.md)
  lists as "action-control reset". So gaining or losing Confuse or Berserk through a stat rebuild cancels the action in
  flight.
- **The cancel is skipped** in three cases:
  - the unit word's bit 24 is set (`002FF99C`);
  - the unit's action id `+0x714` is at most `0x21E` and its `+0x6B4` is at least 9 (`002FF9A3`–`002FF9BD`);
  - that action id is `0x113` (`002FF9BF`).
  Otherwise the action-cancel routine is called at `002FF9C7`.
- **After it**, the tail does the following:
  - clears `+0x6F8`, `+0x748` and `+0x770` (`002FF9CC`–`002FF9DA`);
  - clears the unit word's bit 14 unless `+0xBA0` holds `0x113` or `0x95` (`002FF9E1`–`002FFA11`);
  - clears `+0x788` bit 10 and `+0x6B0` bit 1 (`002FFA14`, `002FFA22`);
  - zeroes `+0x750` and `+0x74C`;
  - sets `+0x04` bit 21 (`002FFA38`);
  - calls `00307D10` (`002FFA40`).

> **Changing a stat can interrupt what a character was doing**, and exactly which two flags do it is
> recorded here as a mask rather than as a meaning. *(Meaning added 2026-09-30, FABLE: Confuse and Berserk, above.)*

## Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Is 9,999 a cap or a coincidence? | It is the constant in a `cmp`/`cmov` pair on the party path only, against `1000000000` on the other. **Two literals, one branch.** |
| Is the band's 32,767 a separate cap or the same clamp? | **Separate** — it is applied *after* the first clamp, overwriting it, and only when the band predicate held at entry. |
| Are the three status lists one list read at three offsets? | **Three different base addresses and three different loop bounds** (16, 16, 12), each accumulating into a different variable. |
| Is `rec[+0x1C2] − rec[+0x88]` really the experience quantity? | The same two displacements on the same record, subtracted in the same order, in `002F8BB0`. **Two functions, read hours apart, no shared code.** |
| Does the output block really start empty? | **Zeroed at entry** — four qword stores and a dword — before any source is consulted. |

**What this document does not claim:** which stat each output offset holds, what the three status lists
are called, what the two conditional growth flags mean, what `002F8E50` and `002F9180` compute from
level, or what the cancel-on-change flag pair represents.

*Updated 2026-09-30 (FABLE): each of those is now answered.*
- **Which stat each output offset holds.** The column map below, and the field map's `+0x24`–`+0x36`.
- **The three status lists.** They are named by the register each one feeds; the ids are effect-layer bit numbers,
  tested in either layer. Each id's bonus is the `u16` at `+4` of its row in registry slot `02EBF040`.
  - `00D10290`: 16 ids, 64–68, 35, 42–47 and 60–63. They go to Strength (`r12d`, stored at output `+6`, `002FF840`).
  - `00D102A0`: 16 ids, 69–73, 19, 22, 24, 26, 87 and 97–102. They go to Magick Power (`r13d`, output `+7`, `002FF85A`).
  - `00D102B0`: 12 ids, 74–85. They go to max HP (`r14`, output `+0`, `002FF7E2`); OPUS's replay executed this list
    ([record](../_index/candidates/s24-opus-replay-stat-derivation/README.md), `D5_either_layer_pays_the_bonus`).
- **The two conditional growth flags.** CB-9: bits 0 and 1 of `+0x15` select the source.
- **`002F8E50` / `002F9180`.** The HP and MP scalings above; they take no level.
- **The cancel pair.** Confuse and Berserk.

## Extension 2026-09-07 — the two stat paths, and the `.ard` growth/base column map

`xiionline-61`, GN160 `fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708`.
`BattleStats_RebuildEffectiveStatsAndAffinityState` (`0x002FEF30`) re-read for `CB-5`.

### What a player sees

A party character and a Marlboro both have Strength, and **the game does not compute them the same
way.** A character's growth comes from a class/growth definition and is stored as *fractional*
values; an enemy's comes from the area's own battle tables and is stored as whole numbers scaled by
how far the enemy's level sits above its table's base level. **One function produces both**, and it
picks the path from a single byte on the definition record.

That is why editing an enemy's Strength and editing a character's are different jobs in different
files, and why a tool that assumes one layout will silently write nonsense into the other.

### The selector, and the two paths

`rec[+0x05]` — the byte this document already records as *"gates whether any of it happens"* — selects
between two complete, non-overlapping stat sources:

| | `rec[+0x05] == 0` | otherwise |
|---|---|---|
| source | growth definitions at registry slot **`0x02EBF130`** | the four **`.ard`** tables |
| shape | **`float`** fields read from the record | `growth[col] * K + base[col] + record modifier` |
| `K` | not used | `bLevel − bGrowthBaseLevel` |
| who | party characters | area units / enemies |

**Both paths write the same output slots and hit the same clamps.** That is the join that lets the
columns be named.

### The `.ard` growth / base column map

Derived by pairing each computed value with **the clamp it lands on**, and using the output names
this database already proved *from readers* (99 for the four core attributes, 255 for the three
derived combat values, 100 for the rate fields, 999 for MP):

| `.ard` column | width | feeds | clamp |
|---|---|---|---:|
| `+0x20` | `int` | **HP** | `0x7FFF` |
| `+0x24` | `s16` | **MP** | 999 |
| `+0x26` | byte | **Strength** | 99 |
| `+0x27` | byte | **Magick Power** | 99 |
| `+0x28` | byte | **Vitality** | 99 |
| `+0x29` | byte | **Speed** | 99 |
| `+0x2A` | byte | **innate evade** — stats `+0x31`, the roller's third band | 100 |
| `+0x2B` | byte | **Defence** | 255 |
| `+0x2C` | byte | **Magick Resist** | 255 |
| `+0x2D` | byte | **Attack** | 255 |
| `+0x2E` | byte | **parry (weapon-side evade)** — stats `+0x32`, in place of weapons when `+0x15` bit 0 | 100 |
| `+0x02` | byte | **block (shield-side evade)** — stats `+0x33`, in place of shields when `+0x15` bit 1 | 100 |
| `+0x03` | byte | **magick evade** — stats `+0x34`, in place of shields when `+0x15` bit 1 | 100 |

**The four core attributes are four consecutive bytes, `+0x26`–`+0x29`**, in the on-screen order
Strength / Magick Power / Vitality / Speed. The three 255-clamped values are **not** contiguous with
them and are not in screen order: `+0x2B` Defence, `+0x2C` Magick Resist, `+0x2D` Attack.

`+0x2E`, `+0x02` and `+0x03` are reached only through the two `[spine+0x15]` flag-gated blocks
already documented, which is why they are separated from the rest.

> **Modder consequence:** an enemy's Strength growth is **one byte at `.ard` column `+0x26`** of the
> growth table (registry slot `0x02EBF140`), and its flat base is the same column of the base table
> (`0x02EBF148`). The final value is
> `growth[+0x26] × (level − growthBaseLevel) + base[+0x26] + record modifier`, clamped to `[0, 99]`.

### ⚠ The GFZ's typed struct names this record inconsistently, and at least four are wrong

The decompiler renders this function against a `target_bkbi` struct carrying names like
`nStrengthModifier` and `nWeaponGuardRateModifier`. **Those names are a prior session's claim, and
the function itself refutes them.** The *same* output slot is fed differently on the two paths:

| output slot | `rec[+0x05] == 0` path | `.ard` path | final clamp |
|---|---|---|---:|
| slot A | `(float)`**`nAttackPowerModifier`** | `growth[+0x26]·K + base[+0x26] +` **`nStrengthModifier`** | **99** |
| slot B | `(float)`**`nMagickResistModifier`** | `growth[+0x27]·K + base[+0x27] +` **`nMagickPowerModifier`** | **99** |
| slot C | `(float)`**`nWeaponGuardRateModifier`** | `growth[+0x28]·K + base[+0x28] +` **`nVitalityModifier`** | **99** |
| slot D | `(float)`**`nSpecialGuardRateModifier`** | `growth[+0x29]·K + base[+0x29] +` **`nSpeedModifier`** | **99** |

**Every one of those four slots clamps at 99**, and 99 is the cap this database proved *from readers*
belongs to Strength, Magick Power, Vitality and Speed. So on the character path, the fields the
struct calls **AttackPower, MagickResist, WeaponGuardRate and SpecialGuardRate are read as floats and
become Strength, Magick Power, Vitality and Speed.**

Either the struct named those four offsets after the wrong path, or **the same record bytes carry
different meanings depending on `rec[+0x05]`** — which is exactly what a record that serves two
disjoint layouts would do. **The function cannot distinguish those two readings**, and this document
does not choose between them.

> **`CB-12` answered 2026-09-14 (FABLE): the second reading. The record is two layouts, selected by `rec[+0x05]`.**
> The earlier pass compared *names*. The operand **widths** in the same function settle the question, because the
> two branches do not read the bytes at the same size:
>
> | record offset | `rec[+0x05] == 0` path | `.ard` path |
> |---|---|---|
> | `+0x08` | `dword`, argument of the call whose result fills the HP slot `[rsp+0x40]` (`002FF078`) | `s16`, added to Strength (`002FF245`) |
> | `+0x0A` | — (inside the `+0x08` dword) | `s16`, added to Magick Power (`002FF265`) |
> | `+0x0C` | `s16`, argument of the call whose result fills the MP slot `[rsp+0x28]` (`002FF084`) | `s16`, added to Vitality (`002FF27C`) |
> | `+0x0E` | — (not read) | `s16`, added to Speed (`002FF293`) |
> | `+0x10` | **`float`** → Strength (`cvttss2si`, `002FF0C2`) | **`s16`** → Attack: `+ base[+0x2D] + growth[+0x2D]·K` (`002FF347`), clamped to 255 and stored at stats `+0x0A` (`002FF8CA`–`002FF8F2`) |
> | `+0x12` | — (inside the `+0x10` float) | `s16`, added to Defence (`002FF2C1`) |
> | `+0x14` | **`float`** → Magick Power (`002FF0CD`) | **`s16`**, added to Magick Resist (`002FF2E0`) |
> | `+0x18` | **`float`** → Vitality (`002FF099`) | **`s16`** (`002FF20A`), use not traced here *(the parry modifier: CB-5 table below)* |
> | `+0x1C` | **`float`** → Speed (`002FF0B7`) | **`s16`** (`002FF23D`), use not traced here *(the magick evade modifier: CB-5 table below)* |
> | `+0x20` | byte (`002FF0AA`) | `s16` (`002FF2F1`) |
>
> The branches meet at `002FF3D0` holding the same four core values in the same places. `r12d` is Strength on both;
> the `.ard` path moves Magick Power into `r13d` at `002FF381`, where the other path left the `+0x14` float;
> Vitality and Speed are `[rsp+0x2C]` / `[rsp+0x30]` on both. So a 4-byte float at `+0x10` on one path covers
> the two `s16` fields `+0x10` and `+0x12` on the other. No single field layout can be read both ways, so the same
> bytes carry different values depending on `rec[+0x05]`.
>
> *Prior art, missed by this section when written:* the
> [battle-stats field map](Battle-Stats-Record/the-battle-stats-record-field-map.md) §2.2 recorded this union on
> 2026-09-11 (`OPUS-CONTRA-STATUNION`), naming `+0x05` the kind byte (0 party, 1 spawn-backed). The two agree;
> this section adds the `.ard`-side widths for `+0x08`–`+0x0E` and `+0x20`.
>
> **What this does to the GFZ names.** `nStrengthModifier` (`+0x08`), `nMagickPowerModifier`, `nVitalityModifier`,
> `nSpeedModifier` and `nAttackPowerModifier` (`+0x10`) describe the **`.ard` layout** correctly: each is the `s16`
> that path adds to that stat. The other `.ard` names are not checked here (`CB-5`). On the `rec[+0x05] == 0` layout
> the struct does not apply at all. The advice below stands in narrowed form: use the names only for records with a
> non-zero `+0x05`.

> **Do not adopt the `n*Modifier` names from decompiler output for a record whose `+0x05` is 0.** On that
> layout the offsets are a dword, an `s16` and four floats, not modifiers (`CB-12`, above). The inconsistency
> is only visible if you read both branches.

### What `CB-5` still owes

`CB-5` asked what the **eleven `s16` per-stat fields at record `+0x08`–`+0x1C`** are called. **This
pass mapped the `.ard` columns, not those eleven** — the record-side modifiers are the *other* term
in the same sum, and naming them requires resolving the two-path ambiguity above first. `CB-5`
remains open, with the ambiguity now stated rather than latent. *(Superseded by the answer that follows: CB-5 ANSWERED;
noted 2026-09-30, FABLE.)*

> **`CB-5` answered 2026-09-14 (FABLE), for the `.ard` layout** (`rec[+0x05] != 0`; on the other layout these
> bytes are not `s16` fields, `CB-12`). Each of the eleven is the record term of exactly one column's
> `growth[col]·K + base[col] + rec[off]` in `002FEF30`, so it takes that column's name from the map above:
>
> | record | column | name | where the sum is built |
> |---|---|---|---|
> | `+0x08` | `+0x26` | Strength modifier | `002FF205`–`002FF24D` |
> | `+0x0A` | `+0x27` | Magick Power modifier | `002FF250`–`002FF269` |
> | `+0x0C` | `+0x28` | Vitality modifier | `002FF26B`–`002FF280` |
> | `+0x0E` | `+0x29` | Speed modifier | `002FF282`–`002FF297` |
> | `+0x10` | `+0x2D` | Attack modifier | read at `002FF2E6`; the column terms are added inside the `+0x15` bit-0 block (`002FF32A`–`002FF362`), so with the bit clear the slot holds the modifier alone |
> | `+0x12` | `+0x2B` | Defence modifier | `002FF2B0`–`002FF2C5` |
> | `+0x14` | `+0x2C` | Magick Resist modifier | `002FF2C7`–`002FF2E4` |
> | `+0x16` | `+0x2A` | innate evade modifier | `002FF299`–`002FF2AE` |
> | `+0x18` | `+0x2E` | parry modifier | read at `002FF20A`; column terms in the bit-0 block (`002FF36D`–`002FF373`) |
> | `+0x1A` | `+0x02` | block modifier | read at `002FF20F`; column terms in the `+0x15` bit-1 block (`002FF3A3`–`002FF3C0`) |
> | `+0x1C` | `+0x03` | magick evade modifier | read at `002FF23D`; column terms in the bit-1 block (`002FF3AA`–`002FF3C8`) |
>
> All eleven agree with the GFZ decompile's struct. Besides the five quoted above, it names `+0x12`
> `nDefenseModifier`, `+0x16` `nAvoidRateModifier`, `+0x18` `nWeaponGuardRateModifier`, `+0x1A`
> `nShieldGuardRateModifier` and `+0x1C` `nSpecialGuardRateModifier`. **Two further `s16`**, which the struct
> leaves as `field_0x1e` / `field_0x20`,
> sit past the eleven and join no column: `+0x1E` (`002FF2D6`) becomes a term of the sum clamped to 100 at output
> `+0x11`, together with the block, parry and innate-evade values (`002FF780`–`002FF7A5`, `002FF8A7`–`002FF8B6`).
> `+0x20` (`002FF2F1`) is added to the magick-evade value in the sum clamped to 100 at output `+0x12`
> (`002FF791`–`002FF7AE`, `002FF8B9`–`002FF8D2`). The field map names those outputs by composition, stats `+0x35`
> **total evade** and `+0x36` **total magick evade**. So `+0x1E` is the total-evade modifier and `+0x20` the
> total-magick-evade modifier (`CB-13`, answered). Nothing enumerated reads either output (`FE-2`).

## Key addresses (FABLE, 2026-09-30)

*Added 2026-09-30 (FABLE): addresses the page already cites, with body sizes from the function list.*

| Address | Working name | Body | Role |
|---|---|---:|---|
| `002FEF30` | `BattleStats_RebuildEffectiveStatsAndAffinityState` | 2,859 B | the rebuild: zero the output block, sum base + equipment + status bonuses, clamp, and on the party side the cancel-on-change tail |
| `002F8E50` | (HP scale) | 30 B | `(row[+0x18] + 1) × base HP × row[+0x19] / 100` |
| `002F9180` | (MP scale) | 21 B | `base MP × row[+0x1D] / 100` |
| `0031E9A0` | (item-row classifier) | 68 B | the equipment kind that picks a stat pair (`002FF451`) |
| `00307D10` | `BattleUnit_UpdateEngagementStateFlag` | 224 B | the tail's last call (`002FFA40`) |
| `0023A570` | `BattleUnit_ApplyUnitDefinition` | 1,808 B | the second consumer of `02EBF150`, same indexing rule |
| `002F8BB0` | `Reward_ComputeExperienceForRecipient` | 430 B | the experience formula, the other reader of `rec[+0x1C2] − rec[+0x88]` |

### Data addresses cited by this document (FABLE, 2026-09-30)

| Address | Name | Kind | Contents |
|---|---|---|---|
| `02EBF130` | party growth table slot | registry slot | the party row: HP / MP scale bytes, four float bases, two status masks |
| `02EBF150` | class-4 slot | registry slot | the foe base table, indexed by the definition's `u16` at `+0` |
| `02EBF140` / `02EBF148` | `.ard` growth / base slots | registry slots | the column map below |
| `02EBF040` | ability table slot | registry slot | the per-id bonus word `+4` the three status lists add |
| `00D10290` / `00D102A0` / `00D102B0` | the three status-id lists | `.rdata` byte arrays | 16 / 16 / 12 effect-layer ids (Strength / Magick Power / max HP) |

## Call chain (FABLE, 2026-09-30)

*Added 2026-09-30 (FABLE), from the raw call index.*

```
status change, level-up, definition install ... (25 call sites)
  -> BattleStats_RecomputeDerivedStateAndAutoStatuses 0030FED0   (calls at 003103AD)
     -> BattleStats_RebuildEffectiveStatsAndAffinityState 002FEF30   <- THIS PAGE
        -> 002F8E50 / 002F9180 (party HP / MP), 0031E9A0 + the id validator (equipment), 0020E600 (every table)
        -> [party, live unit, Confuse or Berserk changed] action cancel (002FF9C7), then 00307D10
equipment screen candidate loadout
  -> Equipment_EvaluateCandidateLoadoutAndBuildDerivedStats 0030A4E0   (calls at 0030A6B7, with an output buffer)
     -> 002FEF30   (it passes an output buffer at 0030A6AA, so the tail's live-unit guard stays 0)
```

**Upstream (who causes this):** exactly two direct callers, `0030FED0` and `0030A4E0`.
- `0030FED0`, the auto-status recompute, is the owner transition. Its 25 call sites are triggers: status writes, the
  level-up recompute and the definition install among them.
- `0030A4E0` computes a candidate loadout's numbers for the equipment screen without touching the live record's tail
  state.

**Downstream (what this causes):** the effective-stats block at stats `+0x24`–`+0x36`, and the status words `+0x38` /
`+0x3C`. Every formula that reads an effective stat is downstream of them. On the party side the tail can also cancel
the unit's action and refresh its engagement flag.

**Do not confuse with:** the auto-status rebuild one level up (`0030FED0`'s own work). That is the
[contract](CONTRACT-stat-derivation.md)'s sibling S-24, not this sum.

## Modding notes (FABLE, 2026-09-30)

- **Best intervention point:** the authored inputs, not the output block. The block is zeroed and rebuilt on every call
  (`002FEFB9`–`002FEFC8`), so a direct write to stats `+0x24`–`+0x36` lasts only until the next status change.
- **Enemy stats** are the `.ard` columns (the map above): growth × (level − growth base level) + base + the record's
  modifier.
- **Party stats** are the party row's scale bytes and float bases, plus equipment and the three status-bonus lists.
- **Moving an id between the three lists** changes which stat it raises without touching code.
- **Caps are code:** 9,999 / 999 / 99 / 255 / 100 are `cmp` literals in this body. Raising one is a code patch.
- **XIIOnline:** the output is derived state. Two clients agree on it when they agree on the record, the equipment and
  both effect layers, so replicate those inputs, not the block.

## Evidence (FABLE, 2026-09-30)

*Added 2026-09-30 (FABLE). Tier per `_index/EVIDENCE-STANDARD.md`.*

| Claim | Evidence | Tier |
|---|---|---|
| the output block is zeroed before any source is read | `002FEFB9`–`002FEFC8`: four qword stores and a dword at `rsi` | 1 |
| the caps and their branches | `002FF7B1`–`002FF805` (main value), `002FF817`–`002FF824` (MP), `002FF829`–`002FF874` (99-capped) | 1 |
| the party HP / MP scaling | `002F8E50` and `002F9180` read whole; call sites `002FF07B`, `002FF090` | 1 |
| the two status masks from the party row | `002FF0A3` / `002FF0D3`, `002FF0D6` / `002FF0D9` | 1 |
| the foe path and the `.ard` column map | the Extension 2026-09-07 section and CB-5 / CB-12 / CB-13 above, with their instruction ranges | 1 |
| the three status lists: addresses, sizes, ids, target stat | loops `002FF5B2`–`002FF63C`, `002FF650`–`002FF6DA`, `002FF6F0`–`002FF77A`; ids dumped by `wsn_lists.py` in the [2026-09-30 DD record](../_index/candidates/dd-content-fable-0930/) (control: `008F8180` reads 10.0) | 1 |
| either effect layer pays the bonus | OPUS's executed replay, `D5_either_layer_pays_the_bonus` ([record](../_index/candidates/s24-opus-replay-stat-derivation/README.md)) | isolated original code |
| the cancel tail: guards, exceptions, writes | `002FF970`–`002FFA40`, read whole | 1 |
| bits 5 / 27 are Confuse / Berserk | [the thirty-two statuses](../10-Status-Periodic-Terminal/the-thirty-two-statuses.md) status table | 1 (by reference) |
| exactly two direct callers | the raw call index: `003103AD` (in `0030FED0`) and `0030A6B7` (in `0030A4E0`) | 1 |

## What is not known (FABLE, 2026-09-30)

Nothing on this page is open as of 2026-09-30. Every item of the "does not claim" list is answered above. CB-5, CB-9,
CB-10, CB-12, CB-13 and FE-2 are ANSWERED in the register. The in-game names of the 44 effect-layer ids in the three
lists are the [thirty-two statuses](../10-Status-Periodic-Terminal/the-thirty-two-statuses.md) and augment pages'
subject, not this page's.

## Related (FABLE, 2026-09-30)

- [`CONTRACT-stat-derivation.md`](CONTRACT-stat-derivation.md): the implementation contract for this page.
- [`Battle-Stats-Record/the-battle-stats-record-field-map.md`](Battle-Stats-Record/the-battle-stats-record-field-map.md):
  the record the block is written into.
- [`../10-Status-Periodic-Terminal/the-thirty-two-statuses.md`](../10-Status-Periodic-Terminal/the-thirty-two-statuses.md):
  the Confuse / Berserk pair.
- [`Scratch-Block/the-formula-scratch-block.md`](Scratch-Block/the-formula-scratch-block.md): where the four evasions are
  spent.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL and recorded in the registry.*

**Presentation — CLIENT.** `BattleUnit_UpdateEngagementStateFlag` (`00307D10`), which the stats rebuild updates, is
also read by `BattleUnit_ComputePartyBattleStance`. So the party battle-stance computation reads the engagement state
that the stats rebuild updates.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Rewards_Progression_Economy — CLIENT.** `BattleUnit_ProcessDefeatRewardsAndLoot`, owned by that layer, calls `002F8BB0` on this page. That caller is defeat-and-loot processing, which reads the defeated unit's `+0x698` block, needs `byte[+5] == 1`, and is suppressed entirely by bit 3 of `byte[+0xE9A]`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**ActorEntity — CLIENT and SERVICE (5 edges).** The definition installer `BattleUnit_ApplyUnitDefinition` `0023A570` calls `BattleUnit_ResetStateForReuse` `00236A60` and `00322050`, which zeroes the unit's `+0xEA4` / `+0xEA8` and re-keys its actor handle at `+0x08`; `BattleUnit_TeardownAndDespawn` `00300E40` and `BattleGroup_RefreshFourActorDefinitions` `003266C0` call `0023A570`; and `Reward_ComputeExperienceForRecipient` `002F8BB0` calls `BattleUnit_FindMappedDefinitionSelectorByIndex` `0031B810`. The unit pool drives the installer that fills the stats record this page reads, the installer uses the pool's reset and handle re-key helpers, and the experience function resolves the recipient's definition through the pool's selector map.

**Gameplay — SERVICE and CLIENT (8 edges).** `0023A570` and `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` call the id validator `BattleEncodedId_IsValidForClass` `00322C50`; `002FEF30` calls `BattleUnit_UpdateEngagementStateFlag` `00307D10`, which calls `BattleUnit_HasActiveEngagementEvidence` `00307CE0`, `BattleUnit_HasRelationshipClass2PlusInTrackedActorList` `0030B050` and `BattleUnit_IsPointerInEngagementRecordPools` `0030BF20`; the item-row classifier `0031E9A0` calls `BattleDefinition_MapByte9ToRuntimeCategory` `0031E9F0` and is called by the encoded-id query-record builder `0031C5D0`, which stores its band at `+0x50`. The rebuild's tail refreshes the unit's engagement flag from those engagement tests, the rebuild and installer validate ids through the shared validator, and the id query record reuses the same kind-to-band classifier the equipment branches use.

**Items_Equipment_Shops_License — CLIENT (1 edge).** `Equipment_EvaluateCandidateLoadoutAndBuildDerivedStats` `0030A4E0` calls `002FEF30`. The equipment layer computes a candidate loadout's derived stats by running this page's stats rebuild.

**Spawn_Encounter_Lifecycle — CLIENT and SERVICE (2 edges).** `Spawn_ApplyScriptSelectedUnit` `0023A3B0` calls `0023A570`, and `0023A570` calls `SpawnKeep_ResolvePrimaryEntry` `00236100`. A spawn installs its unit's definition through this installer, and for a definition id whose high byte is 1 the installer resolves the spawn record from the lane map through that layer's helper.

**Status_Periodic_Terminal — CLIENT (3 edges).** `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` calls `002FEF30` and `0031E9A0`; `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360` calls `00307D10`. The auto-status recompute is the caller that runs the stats rebuild and the item-row classifier, and the status write refreshes the engagement flag after a change.

**WorldAreaField — SERVICE (2 edges).** `0023A570` calls the thunk `FieldData_GetActiveFieldRecordBit15` `00313F60`, and `00307D10` calls `FieldData_GetActiveFieldRecordBit15` `00377C20`. Both read the active field record's action-permission bit (bit 15); what the installer branches on it is not read here.
