---
system: Attack-vs-defence preparation and stat scaling
category: 08-Combat-Formula
status: AUDITED
owner_layer: PrimaryOwner:CombatFormula
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 3
  last_pass: 2026-09-02
  last_pass_state: falsification-pass
  crossref_clean: true
  reopened_count: 0
---

# Attack-vs-defence preparation and stat scaling

> The seven ways FFXII turns a stat into a damage multiplier — and the reason a dagger, a katana
> and a pole scale off different attributes.

**DOCUMENTED.** The seven preparation variants are read at instruction level, and — since
2026-09-02 — so is the consumer that turns their three values into a damage number. The full
equation is in section 2. What remains open is which weapon type selects which variant, and the
many *modifier* stages that sit between preparation and the final write.

## 1. What the player sees

Two characters with the same Strength do different damage with different weapons — and not just
because the weapons have different Attack. **The weapon decides which of your attributes is
multiplied in.** That is why Speed matters on some weapons and not others, and why a character built
for one weapon type underperforms with another.

It is also why the same attack on the same enemy does not deal the same damage twice. There is a
deliberate random component, and it is applied to the weapon's Attack value, not to the result.

**And it is why a high-Defence enemy can shrug you off completely no matter how strong you are.**
The engine subtracts Defence from Attack *first*, and only then multiplies by the attribute-derived
multiplier. If Defence is at or above your rolled Attack, the result is a hard **zero** — the
multiplier is never reached. Strength cannot rescue a weapon whose Attack is too low; only Attack
can. That ordering is read from the binary in section 2.

And it is why the four "weaken the enemy" Technicks exist as a matched set: **Wither, Addle, Expose
and Shear reduce exactly the four stats this system reads** — the attacker's Strength and Magick
Power, and the target's Defence and Magick Resist. *(That correspondence is an inference from the
effect set; nothing in the binary names them — see section 7.)*

## 2. Native mechanism

### One template, seven variants

Seven `BattleFormula_Prepare*` functions share a body shape of 208–216 bytes. Each reads the
attacker's **Level** at `+0x1C2` and one or two **attributes**, and each writes the same three-slot
scratch record. Read from the disassembly:

| Function | Addr | Size | Attacker stats read | Target stat |
|---|---|---:|---|---|
| `PrepareStrengthAttackVsDefense` | `0038AAF0` | 208 | `+0x2A` | `+0x2F` |
| `PrepareStrengthAttackVsDefenseScaled150` | `0038AD70` | 216 | `+0x2A`, **× 1.5** | `+0x2F` |
| `PrepareMagickPowerAttackVsDefense` | `0038AE50` | 208 | `+0x2B` | `+0x2F` |
| `PrepareMagickStrengthAttackVsDefense` | `0038A1F0` | 212 | `+0x2B`, `+0x2A` | `+0x2F` |
| `PrepareSpeedStrengthAttackVsDefense` | `0038A110` | 212 | `+0x2D`, `+0x2A` | `+0x2F` |
| `PrepareVitalityStrengthAttackVsDefense` | `0038A2D0` | 208 | `+0x2C`, `+0x2A` | `+0x2F` |
| **`PrepareStrengthAttackVsMagickResist`** | `0038A3A0` | 208 | `+0x2A` | **`+0x30`** |

**Six of the seven measure against the target's `+0x2F`. One measures against `+0x30` instead.**
That single changed offset is the whole difference — a weapon using that variant is checked against
a different defensive stat, which is exactly the behaviour players describe as a weapon "ignoring"
Defence.

### The arithmetic

From `0038AAF0`, the plainest variant, read instruction by instruction:

```c
A   = attacker[statOffset];        /* the scaling attribute      */
L   = attacker[0x1C2];             /* Level                      */
ATK = attacker[0x2E];              /* the attack value           */
D   = target[0x2F];                /* or target[0x30]            */

scratch[0] = ((L + A) * A) * (1/256.0) + 1.0;

/* random component, applied to ATK and nothing else */
if (0.01 > ATK * 0.125) {
    r = 0;
} else {
    N = (int)(ATK * 0.125 * 100);
    r = (rand() % N) / 100.0;      /* 0 <= r < ATK * 0.125, in 1/100 steps */
}
scratch[1] = ATK + r;
scratch[2] = (float)D;
```

**Four** constants carry the whole shape, and all four were read from `.rdata` *(the sentence
read "three" until 2026-09-15 while the table listed four; `008F3134`, the `100` that quantises
the random step, is not part of the multiplier and was left out of the count. Found by
`check_counts_vs_tables.py`, the gate built for EC-5's defect class):*

| Constant | Value | Role |
|---|---|---|
| `009088D8` | `0.00390625` | exactly **1/256** — the scaling divisor |
| `00915508` | `0.125` | the variance band: **12.5 % of Attack** |
| `01CEBBA8` | `1.0` | the `+1` that makes the multiplier start at unity |
| `008F3134` | `100` | quantises the random step to `0.01` |

**So the multiplier is `1 + (Level + Stat) × Stat / 256`** — unity at zero stat, growing
quadratically in the attribute. And the damage roll is **upward-only**: attack power lands in
`[ATK, ATK × 1.125)`, never below the weapon's own Attack.

### The two variants that break the template

- **`PrepareSpeedStrengthAttackVsDefense`** does not use `1/256`. It uses a `divss` by the literal
  **218** (`00D112D0`), a divisor that appears nowhere else in the family.
- **`PrepareVitalityStrengthAttackVsDefense`** is the only variant with **no `+1.0`** — its
  multiplier is not floored at unity.
- **`PrepareStrengthAttackVsDefenseScaled150`** adds one `mulss` by **1.5** (`00901B3C`).

### The shared scratch record

All seven write the same three consecutive floats:

```
02AEE054   float   the multiplier      ((L + Stat) * Stat)/256 + 1
02AEE058   float   attack + variance
02AEE05C   float   the target's defensive stat
```

These are **global**, not per-unit — so **one attack resolves at a time**. `BattleFormula_ResetScratchState`
(`003849B0`) clears all three, which is what a shared scratch record needs.

Downstream use is heavy and is **not read here**: `02AEE054` alone is touched at **380 sites across
45 functions**, every one of them `CombatFormula`-owned.

## 3. The stat block, cross-validated

The attribute offsets are not guessed from the function names. A **separate family** confirms them —
four small functions that scale a single stat and write the result to a global:

| Function | Addr | Reads | Multiplier | Precision |
|---|---|---|---|---|
| `BattleFormula_ReduceStrengthTo70Percent` | `0038E870` | `+0x2A` | **0.7** | double |
| `BattleFormula_ReduceMagickPowerTo70Percent` | `0038E8B0` | `+0x2B` | **0.7** | double |
| `BattleFormula_ReduceDefenseTo90Percent` | `0038E8F0` | `+0x2F` | **0.9** | float |
| `BattleFormula_ReduceMagickResistTo90Percent` | `0038E920` | `+0x30` | **0.9** | float |

Each names a stat and reads exactly the offset this document assigns to it — **independent
confirmation from code that shares no call path with the preparation family.** Both 0.7s are the
same constant (`00D112C8`); both 0.9s are the same constant (`008FCC8C`, the nearest float to 0.9).

All four also share a floor: **if the stat byte is zero they write `1`, not `0`** — a reduced stat
never becomes nothing.

Resulting layout:

```
BattleStatsRecord (BKBI) stat block -- the record at unit +0x698, NOT the BattleUnit
  +0x2A  byte   Strength         <- confirmed by ReduceStrengthTo70Percent
  +0x2B  byte   Magick Power     <- confirmed by ReduceMagickPowerTo70Percent
  +0x2C  byte   Vitality         <- from the function name only
  +0x2D  byte   Speed            <- from the function name only
  +0x2E  byte   Attack           <- the value the variance is applied to
  +0x2F  byte   Defence          <- confirmed by ReduceDefenseTo90Percent
  +0x30  byte   Magick Resist    <- confirmed by ReduceMagickResistTo90Percent
  +0x1C2 byte   Level
```

**The owning type is the stats record, not the unit** (corrected 2026-09-11, OPUS-PREPTYPE-FIX):
every offset the family reads — `+0x2A` … `+0x30`, `+0x1C2`, and the `+0x50` equipment words — is
a declared `BattleStatsRecord` field, and none exists on `BattleUnit`; the unit does have bytes at
`+0x2C` and `+0x30` that mean something else (a presentation event parameter and the killer id), so
a reimplementation that took the unit would compile and read the wrong struct silently.

**Every attribute is a single byte** — but that is a fact about the *storage*, and **four of
the seven do not reach 255.** The stat rebuild clamps Strength, Magick Power, Vitality and
Speed (`+0x2A`-`+0x2D`) to **99**; only Attack, Defence and Magick Resist (`+0x2E`-`+0x30`) take
the 255 ceiling. See section 13 — this document originally inferred the cap from the type, which
is wrong in the same way as naming a field from its position.

## 4. Data structures and formulas

```
multiplier = 1 + (Level + Stat) * Stat / 256          /* 218 for the Speed variant */
                                                      /* no +1 for the Vitality variant */
                                                      /* x1.5 for the Scaled150 variant */
attack     = ATK + (rand() % (int)(ATK * 12.5)) / 100 /* only when ATK * 0.125 >= 0.01 */
defence    = target[0x2F]   or   target[0x30]

reduced(Str)  = max(1, floor(Str * 0.7))
reduced(Mag)  = max(1, floor(Mag * 0.7))
reduced(Def)  = max(1, floor(Def * 0.9))
reduced(MRes) = max(1, floor(MRes * 0.9))
```

## 5. Call chain

```
weapon slot -> recipe table -> one of the seven Prepare* variants
                                  |
                                  +-> reads attacker Level +0x1C2 and 1-2 attributes
                                  +-> reads target +0x2F or +0x30
                                  +-> rand()  (only for the attack variance)
                                  v
                        02AEE054 / 02AEE058 / 02AEE05C     shared scratch
                                  |
                    45 CombatFormula functions read and rewrite these
                    (380 sites on the multiplier slot alone)  -- NOT read here
```

Two of the seven are already bound to weapon slots by
[`../Recipe-System/ranged-weapon-recipes.md`](../Recipe-System/ranged-weapon-recipes.md):
slot **66** (Bow) uses `0038A110`, slot **65** (Crossbow) uses `0038AAF0`.

**Where the slot lands (2026-09-11, OPUS-REQ-FABLE-PREPTABLE).** A slot indexes the calculator
function table at `01EFA5C0`: `BattleFormula_ResolveTargetResult` calls
`[imageBase + slot × 8 + 0x1DDA5C0]` (`003863D0`; the image base is `0x120000`, so the operand
resolves to `01EFA5C0 + 8 × slot`), after resolving the recipe through the pointer table the same
way (`0038635D`, `01EF96C0`). The Prepare* variants are **slots 60–79**, twenty pointers at
`01EFA7A0`–`01EFA838` (OPUS read them out of `.data`): `00389F80`, `0038AA90`, `00389DD0`, `00389F80`,
`0038AA90`, then the seven above in the order `0038AAF0` (65), `0038A110` (66), `0038A1F0`, `0038A2D0`,
`0038A3A0`, then `0038A470`, `0038A590`, `0038A680`, `0038A820`, `0038A9D0`, `0038AA90`, `0038AAF0`,
`0038ABC0`, `0038AD70`, `0038AE50` — **sixteen distinct functions: the seven this page names and
nine it does not** (corrected 2026-09-11, OPUS-CONTRA-PREPCOUNT — the first reading subtracted
seven names from twenty entries and called the difference functions). Three functions sit in more
than one slot: `00389F80` at 60 and 63, `0038AA90` at 61, 64 and 75, `0038AAF0` at 65 and 76 — so a
mod that edits one of those slots' pointers changes one variant, but a mod that patches the function
changes every slot that holds it. The `_guard_check_icall` fillers on either side are unassigned slots, not the
table's edges: slot 0 is `00387F40`, and slots 35, 36, 42, 43, 49, 121, 122, 144 and 146 bound by
[the ranged-weapon](../Recipe-System/ranged-weapon-recipes.md) and
[count-clock](../Recipe-System/the-count-clock-and-bank-recipes.md) pages all land at
`01EFA5C0 + 8 × slot`. The other nine are named in §5.1 (2026-09-11); what each of the sixteen reads — which
attacker byte, which defender byte, which authored row — is tabulated slot by slot in
[CONTRACT-preparation-step-family](../CONTRACT-preparation-step-family.md) §15, with the seven named
variants reproduced as its positive control.

### 5.1 The sixteen, named — and what reaches each of them (2026-09-11, E-3 for slots 60–79)

The nine functions §5 left unnamed are read below the same way the seven were: every constant from
`.rdata`, every read attributed after the argument registers were bound (`rcx` = the attacker's
**`BattleStatsRecord`**, `rdx` = the target's, `r8` = the evaluation context — stats records, not
battle units, see §3). Three things the seven did not show up:
**a second multiplier base — `2.0` (`01CEBC08`) — for the magick and technick families**, an
**attack term that is an authored action power rather than the attacker's `+0x2E`**, and one
member that **branches on the evaluation context**.

The "action power" is byte `+0x10` of the current action's row in the action definition table
(registry slot `02EBF138`, row = `0032E400`-resolved base + stride × the action id the resolver
parks at `02AEDFD4`); `+0x11` is the row's second byte. The variance on it is the same
`[P, P × 1.125)` band as on Attack.

| slots | function | name | `02AEE054` multiplier | `02AEE058` attack | `02AEE05C` defence |
|---|---|---|---|---|---|
| 60, 63 | `00389F80` | `BattleFormula_PrepareMagickPowerActionPowerNoDefense` | `2 + (L + MAG) × MAG / 256` | action power + variance | **0** (`0038A0E8`) |
| 62 | `00389DD0` | `BattleFormula_PrepareMagickPowerActionPowerVsMagickResist` | `2 + (L + MAG) × MAG / 256` | action power + variance | target `+0x30` |
| 61, 64, 75 | `0038AA90` | `BattleFormula_PrepareActionPowerAsMultiplier` | **the action power itself** | *untouched* | *untouched* |
| 70 | `0038A470` | `BattleFormula_PrepareAttackTimesAttackNoDefense` | `ATK + variance` | `ATK + variance` (a second, independent roll; skipped with the first when `ATK × 0.125 < 0.01`) | **0** (`0038A573`) |
| 71 | `0038A590` | `BattleFormula_PrepareStrengthAttackPlusLevelStrengthVsDefense` | `1 + (L + STR) × STR / 256` | `(ATK + L + STR) + variance over (L + STR)` | target `+0x2F` |
| 72 | `0038A680` | `BattleFormula_PrepareStrengthAttackOrUnarmedHalfLevelStrengthVsDefense` | `(L + STR) × STR / 256` — **no `+1`** | context `+0x1B` bit 1 set **and** the attacker's weapon word `+0x52` is `0x1000` (Unarmed) or above the equipment range → `((STR + L) + variance over (L + STR)) × 0.5`; otherwise `ATK + variance` | target `+0x2F` |
| 73 | `0038A820` | `BattleFormula_PrepareStrengthActionPowerVsDefenseNoUnity` | `(L + STR) × STR / 256` — no `+1` | action power + variance | target `+0x2F` |
| 74 | `0038A9D0` | `BattleFormula_PrepareActionPowerPair` | action row `+0x11` | action row `+0x10` | *untouched* |
| 77 | `0038ABC0` | `BattleFormula_PrepareStrengthActionPowerVsDefenseBase2` | `2 + (L + STR) × STR / 256` | action power + variance | target `+0x2F` |

The seven of §2 keep their names: 65 / 76 `PrepareStrengthAttackVsDefense`, 66 the Speed variant
(÷218), 67 Magick + Strength, 68 Vitality (no `+1`), 69 Strength vs Magick Resist, 78 Strength ×1.5,
79 `PrepareMagickPowerAttackVsDefense`.

**Two corrections to [the contract's](../CONTRACT-preparation-step-family.md) §15 read sets, from
the bodies.** Slot 70 reads the **attacker's** `+0x2E` twice — `rbx` is bound to `rcx` at `0038A47A`
and `rcx` is not reassigned before `0038A4CD` — and zeroes the defence word; it does not read the
defender. Slot 72 reads the defender's `+0x2F` only (`0038A7F6`, through `rsi` = `rdx`); its `+0x2A`,
`+0x1C2` and `+0x2E` reads are the attacker's through `rbx`. The rest of the table stands, and its
`+0x52` is the **stats record's** weapon slot (`+0x50 + 2 × 1`, [the equipment page](../../12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md)),
not the battle unit's `+0x52`. The context bit is **id 9** of the merged status / augment layers —
Silence as a status, and as an augment *"increases physical damage dealt while empty-handed"*
([the evaluation context](../Evaluation-Context/the-evaluation-context-field-map.md) §2.2) — so slot
72 is the unarmed formula with the Brawler augment folded in.

**Which recipe reaches which slot — and how a weapon chooses its recipe.** `BattleFormula_ResolveTargetResult`
takes the recipe from the action row's byte `+0x08` (`0038617E`). **When that byte is 0** — the plain
Attack — it reads the attacker's weapon word (`stats +0x50`): a value in the equipment range
(`0x1000` … `0x1000 + count`) selects that equipment row, and **the row's byte `+0x19` is the
recipe** (`003861A7`–`00386201`); a word above the range returns −2 and no formula runs
(`00386242`). So the weapon *type* → formula link is a byte on every weapon row, not a category
table. Crossing the 109 recipe lists (`01EF96C0`, two `−1`-terminated lists each), the 543 action
rows' `+0x08` (`action_data.bin`) and the 308 weapon rows' `+0x19` (`battle_pack.bin` directory
`+0x38`, rows with kind byte `+7` below `0x20`) gives every user of slots 60–79 in the shipped game:

| slot | recipe(s) | reached by |
|---|---|---|
| 60 | 4, 83 (71 has no user) | **Cure, Cura, Curaga, Curaja, Cura Mote, Boon**; Self-Sacrifice, Self-Destruct, Mass-Destruct, Kamikaze |
| 61 | 6 | **Raise (power 40), Arise (100)** — the power *is* the multiplier |
| 62 | 7, 11, 63, 105 | the 56 attack magicks (Fire 22, Thunder 23, Blizzard 25 … Holy 157); Drain, Malaise; Breakart Pentagram; the Esper ultimates Hellfire … Eschaton |
| 63 | 12 | Syphon |
| 64 | 8, 14, 68, 108 (106 unused) | Balance, Balance Mote, Gravity Well; Gravity, Graviga, Gravity Mote, Piercing Graviga; Blaster, Hell Blaster, the three Touches, Tri-Attack; Big Bang |
| 65 | **20**, **26**, 45 | **swords, greatswords, spears, rods** (106 rows, recipe 20); **crossbows** (8, recipe 26); Souleater |
| 66 | **21**, **25** | **daggers, ninja swords** (21 rows); **bows** (19 rows) |
| 67 | **22** | **katana, staves** (22 rows) |
| 68 | **23** | **axes, hammers, hand-bombs** (20 rows) |
| 69 | **24** | **poles** (13 rows) |
| 70 | **27** | **guns, measures** (25 rows, with a handful of special rods, maces and swords) |
| 71 | 28 | **nobody** — no weapon row and no action carries recipe 28 |
| 72 | **29** | **Unarmed** (`0x1000`), the only row |
| 73 | — | **no recipe lists it** — a dormant slot |
| 74 | 31, 32 | Potion, Hi-Potion, X-Potion (`+0x11` = 12 / 45 / 150); Ether, Hi-Ether |
| 75 | 37 | Soleil Fang, Rime Fang, Lightning Fang |
| 76 | 30, 64, 67 | Wild Charge; the 58 "NOT USED" weapon rows (recipe 64); Leech |
| 77 | 65, 66 | **85 enemy technicks** (Darkness, Fangs, Screech, …) and the boss / Esper set (Temblor, Judgment, Cyclone, Bitter End, Monarch Sword, Megaflare, Teraflare, Ascension …) |
| 78 | 103 | the ten monster basic attacks — Ram, Gnaw, Lunge, Rake, Slap, Kick, Rush, Snap, Poke, Divine Sword — all power 0 |
| 79 | **104** | **maces** (15 rows) |

Eight recipes have no user at all — 15, 28, 44, 71, 80, 81, 89, 106 — and two preparation slots
(71, 73) are reachable only through one of them or through nothing.

**What this changes for a modder.** A weapon's formula is its row's `+0x19`; to give a sword the
gun formula, write 27 there. A magick's power is its action row's `+0x10`, and the magick family
starts its multiplier at **2**, not 1. Slot 72 is the only member that consults a status bit.

## 6. Modding notes

- **The scaling attribute is chosen by the weapon, not the character.** Changing which `Prepare*`
  variant a weapon slot uses changes which attribute that weapon rewards.
- **Four of the seven attributes cap at 99, not 255.** The storage is a byte, so 255 would fit;
  the rebuild refuses to write it. Strength, Magick Power, Vitality and Speed are clamped to
  **99** — the same 99 the Licence Board and the status screen show. **Raising an authored
  Strength row past 99 changes nothing**, because the value is recomputed and re-clamped every
  time the unit's stats are rebuilt. Attack, Defence and Magick Resist do take 255.
- **The damage roll is upward-only.** Attack power never falls below the weapon's Attack value; the
  variance adds up to 12.5 %.
- **The `1/256` divisor is shared by five of the seven variants** and is a single `.rdata` float at
  `009088D8`. Editing it changes the scaling of all five at once — including for enemies.
- **`0x2AEE054`–`0x2AEE05C` is global scratch, not per-unit.** Do not treat it as belonging to a
  combatant; it holds whichever attack is currently resolving.
- **XIIOnline:** damage preparation is deterministic given the stat bytes plus one `rand()` draw.
  Two clients agree only if both the attribute bytes **and** the RNG stream agree. The scratch record
  is global, so it must never be sampled asynchronously.

## 7. What is not known

- [x] ~~**Which weapon type uses which variant.** Only Bow and Crossbow are bound, via the recipe
      table. The other five are unmapped, and naming them "katana", "pole" and so on would be
      guessing. Needs the weapon-slot recipe table.~~ **AJ-1 ANSWERED on this page, §5.1
      (2026-09-11; item reconciled 2026-09-12, FABLE):** the weapon row's byte `+0x19` is its recipe,
      and the 308 shipped weapon rows map **swords, greatswords, spears, rods and crossbows** to
      slot 65 (Strength vs Defence), **daggers, ninja swords and bows** to 66 (Speed × Strength),
      **katana and staves** to 67 (Magick + Strength), **axes, hammers and hand-bombs** to 68
      (Vitality, no `+1`), **poles** to 69 (Strength vs Magick Resist), **guns and measures** to 70
      (Attack × Attack, no defence) and **maces** to 79 (Magick Power vs Defence).
- [x] ~~The final damage equation.~~ **ANSWERED 2026-09-02** —
      `damage = trunc((attack − defence) × multiplier)`, floored at **0** when defence ≥ attack, read
      from `BattleFormula_FinalizeTargetHpMagnitude` (`0038D280`). Section 10. **AJ-2.**
- [x] ~~The modifier chain between preparation and the finalizer.~~ **AJ-8 ANSWERED 2026-09-12
      (FABLE) — every shipped weapon recipe enumerated and the four unread stages read; §11a.**
      *Earlier state:* **STRUCTURE ANSWERED, CONTENT PARTLY READ 2026-09-02** — the stages are entries in the
      [202-slot step table](../Step-Table/combat-formula-step-table.md), named per action by a
      recipe. For the Bow pipeline, three stages scale the multiplier *before* the finalizer and one
      scales the integer *after* it; slot 98 (`×2`) and slot 165 (`×1.2`, `×2`) are read exactly.
      Section 11. **AJ-8.**
- [x] ~~What selects among slot 96 and 97's multiplier constants; the values suggest elemental
      affinity.~~ **ANSWERED 2026-09-02 — it is NOT elemental affinity.** Step 97's constants are
      **pairs** chosen by unit category via `FUN_002F8E90` (returns `1/2/4/8/0x10`; `test al, 7`
      splits `{1,2,4}` from `{8,0x10}`); step 96 is gated by integer comparisons instead.
      Section 12. **AJ-10.**
- [x] ~~What step 97's HP-like comparison means — it derives a value from the status pair
      (`rdi[0x64] | rdi[0x3C]`, bits 16 and 28) and compares it against `rdi[0x48]`, with `rdi[0x24]`
      conditionally doubled.~~ **AJ-12 ANSWERED 2026-09-12 (FABLE): "is the caster at full HP?"** —
      the value is the HP cap the HP write uses (`max(+0x48, 1)` under bit 16 Disease, else `+0x24`
      doubled under bit 28 Bubble), and step 97 fires its branch when current HP **equals** it
      (`0038BC80`, `cmp [rdi+0x48], eax / jne`). The branch is the augment **Focus** — merged effect
      id 11, *"Raises strength when character has full HP"* — and the whole step is the
      HP-conditioned augment step (§12).
- [x] ~~What `FUN_0038F9D0` (slot 171) does. It sits in the damage pipeline but touches no scratch slot
      and uses no float constant, so it is not a damage modifier.~~ **AJ-11 ANSWERED 2026-09-12
      (FABLE): it loads the on-hit percent gate from the weapon — or the ammunition.** Read whole
      (`0038F9D0`, 420 B): it takes the attacker's stats record, reads the weapon word `+0x50` and
      resolves its equipment row; if that row's partner class `+0x11` is **23–26** (a bow, crossbow,
      gun or hand-bomb that takes ammunition, [the item-id page](../../12-Items-Equipment-Shops-License/item-id-encoding-and-equipment-compatibility.md) §11) **and** the off-hand word `+0x52`
      is a valid equipment id other than Unarmed, it takes the **ammunition row** instead
      (`0038FA54`–`0038FAEF`); then it copies the chosen row's **byte `+0x1F`** into `02AEDFE8`
      (`0038FB44`–`0038FB48`), writing 0 when the weapon word is not an equipment id (`0038FB63`).
      `02AEDFE8` is the **percent gate** ([the scratch block](../Scratch-Block/the-formula-scratch-block.md)) that the two rolling steps after it —
      `BattleFormula_RollPercentGateAndMarkResolved` (`0038FB80`) and
      `…SetResultFlag1000` (`0038FBC0`, slot 176) — roll against before slot 182 applies the
      candidate statuses; and the shipped byte is the weapon's **on-hit effect chance**: 0 on 227
      of 308 weapon rows, and where set it is the chance players know — Mage Masher, Ancient Sword
      and Dragon Whisker 15, Yakei / Kagenui / Orochi 10, Deathbringer 12, Yagyu Darkblade, Zodiac
      Spear and Sledgehammer 20, Ragnarok 25, Vrsabha 50, Rod of Faith 60, the measures 70, Blood
      Sword / Healing Rod / Bonebreaker 100 — and on ammunition 25 on the sixteen status arrows,
      bolts and shot, 0 on the plain ones. So slot 171 is why a bow's on-hit status comes from its
      arrows: the gate is taken from the ammunition whenever the weapon uses any.
- [x] ~~Which of the two result slots `02AEE004` / `02AEE008` is which, and what
      `test dword ptr [r8+8], 0x1000` selects.~~ **AJ-9 ANSWERED 2026-09-12 (FABLE).** `02AEE004` is
      the **HP-loss** magnitude and `02AEE008` the **HP-gain** magnitude: the resolver turns the
      `−1` sentinels into 0 (`0038659C`–`003865E5`) and the applier's HP delta is
      `N(gain 02AEE008) − N(loss 02AEE004)`, damage negative ([the result record](../../07-Combat-Action/Result-Record/the-result-record-field-map.md) `+0x24`). The test
      `test dword ptr [r8+8], 0x1000` reads **bit 12 of the target's status presence word**
      (`ctx+0x08 = target +0x64 | +0x3C`, [the evaluation context](../Evaluation-Context/the-evaluation-context-field-map.md)) — status 12, **Reverse**, *"damage and
      healing reversed"* ([the thirty-two statuses](../../10-Status-Periodic-Terminal/the-thirty-two-statuses.md)) — and both finalizers implement it literally: the plain
      finalizer `0038D280` (slots 113 / 125) writes the truncated magnitude into the loss slot and,
      when Reverse holds, moves it to the gain slot and writes `−1` into the loss slot
      (`0038D2E1`–`0038D2F7`); the zero-damage arm does the same on the other side
      (`0038D302`–`0038D318`). The Cure-family finalizer `0038D0E0` (slot 110, recipe 4: Cure, Cura,
      Curaga, Curaja, Cura Mote, Boon) picks its default slot first by `ctx+0x18 == 0xD` — the target
      unit's genus byte `+0x55`, and genus **13 is Undead** (bank 13 of [the battle text banks](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md): Hume,
      Humanoid, Giant, Dragon, Beast, Insect, Plant, Avion, Amorph, Fiend, Elemental, Warmech, ?,
      Undead) — writing the magnitude as a **loss** for an Undead target and a **gain** otherwise
      (`0038D10D`–`0038D158`), then applies the Reverse swap on top. So "Cure damages the undead"
      and "Reverse turns healing into damage" are both this test pair, and a Reversed Undead is
      healed by Cure. The context builder forces `+0x18` from `0xD` to 0 when the result's byte `+0`
      has bit 5 (`003848AD`–`003848B4`), which is what lets an action treat the undead as living.
- [x] ~~Why the Speed variant divides by **218** rather than 256.~~ **AJ-3 CLOSED 2026-09-12 (FABLE)
      as an intent residue — the image carries no reason, only the consequence:** for the Speed
      family (daggers, ninja swords, bows) the multiplier `1 + (L + SPD) × SPD / 218` is `256 / 218 ≈
      1.174` times steeper in its stat term than the six `/ 256` siblings, so a Speed-scaled weapon
      gains about **17 % more multiplier per point of stat** than a Strength-scaled one at equal
      numbers. Whether that was a deliberate compensation for daggers' low attack is not recoverable
      from the shipped data.
- [x] ~~Why the Vitality variant has no `+1.0` floor when the other six do.~~ **AJ-4 CLOSED
      2026-09-12 (FABLE) as an intent residue, consequence stated:** for axes, hammers and hand-bombs
      the multiplier is `(L + VIT) × VIT / 256` with no unity term, so at low level and Vitality it is
      **below 1** — `(L + VIT) × VIT < 256`, e.g. level 5 with Vitality 20 gives `0.98`, level 1
      with Vitality 10 gives `0.43` — and the weapon deals *less* than `attack − defence` until the
      product passes 256; the same shape as slots 72 and 73 (§5.1), which also drop the `+1`. The
      floor's absence is a fact of the code; the reason is not in it.
- [x] ~~What `+0x2C` and `+0x2D` actually are. Vitality and Speed come from the GFZ function names;
      unlike the other five attributes, no second family confirms them.~~ **AJ-5 ANSWERED 2026-09-12
      (FABLE) by two second families** ([the stats field map](../Battle-Stats-Record/the-battle-stats-record-field-map.md)): `+0x2C` is the **Vitality** the status write's
      duration formula reads (`vit = target.+0x2C`, [the status write](../../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md) §2.4a — statuses last longer on a
      high-Vitality target, the game's rule), and `+0x2D` is the **Speed** the charge-time computation
      divides by (`BattleAction_ComputeChargeLimitTicks`, `002F869F`: a zero byte makes the charge the
      fixed `[global] × 9000`, otherwise the byte is the divisor — the game's charge-time rule).
- [x] ~~Which effects invoke the four `Reduce*` functions. Wither / Addle / Expose / Shear match the
      stat set exactly, but that is an inference from the game's effect list, not read.~~ **AJ-6
      ANSWERED 2026-09-12 (FABLE) from the shipped tables:** the four are calculator slots **136–139**
      (`01EFA5C0`), and the recipe lists at `01EF96C0` ([the count-clock page](../Recipe-System/the-count-clock-and-bank-recipes.md)) run them in exactly four
      recipes — **46 `[11, 47, 136]`, 47 `[11, 47, 137]`, 51 `[11, 47, 138]`, 52 `[11, 47, 139]`** — whose
      only actions, by `action_data.bin`'s names ([`recipe-users.tsv`](../Recipe-System/recipe-users.tsv)), are **`0xA6` Wither** (Strength
      to 70 %), **`0xA7` Addle** (Magick Power to 70 %), **`0xAB` Expose** (Defence to 90 %) and
      **`0xAC` Shear** (Magick Resist to 90 %). Read from the tables, not inferred.
- [x] ~~Which RNG stream `0x379CD0` draws from, and whether the attack variance shares it with the
      hit/miss roll.~~ **AJ-7 ANSWERED 2026-09-12 (FABLE): the one MT19937, and yes — they share it,
      in recipe order.** `00379CD0` is the thunk onto `RNG_MT19937_NextU32` (`00863BF0`), whose
      state is a single static Mersenne Twister — one 624-word table and one index, lazily seeded
      on first use (`00863BF4`–`00863C2B`; [the RNG streams page](../../21-RNG-And-Determinism/rng-streams.md) §3, the "gameplay stream"). Every roll in a
      weapon recipe draws from it through the same thunk: the **preview** list's rolls first —
      knockback (slots 5 / 6, `00388350` / `00388440`), guard-parry (8, `003884F0`), the combo count
      (10, `00388660`), the reaction chance (29, `00389140`) and the **evade ladder** (41–44,
      `003896B0` / `00389820` / `00389950` / `00389A50`, [the ranged-weapon page](../Recipe-System/ranged-weapon-recipes.md)), i.e. the hit / miss
      determination — then the **effect** list's: the attack **variance** inside the preparation
      step (65–79, all seven `Prepare*` bodies call the thunk) and the on-hit gate (176, `0038FBC0`).
      So the variance is drawn from the same generator as the hit roll, after it, and any consumer
      that reproduces one must reproduce the whole sequence in slot order (53 formula-side callers
      in all). **AJ-7.**
- [x] ~~What bounds the weapon's recipe in the resolver — `cmp eax, r13d` at `00386204` after
      `+0x19 + 1`, returning −2 when exceeded — and what the −2 / −1 returns mean to the caller.~~
      **ANSWERED 2026-09-11.** `r13d` is the constant **1** (`0038610F` `or r15d, −1`; `00386113`
      `lea r13d, [r15 + 2]`), so the test refuses a weapon row whose recipe byte is 0 and the next
      two (`00386209`–`00386210`) refuse a negative or ≥ 109 value: a weapon's recipe must be 1 … 108.
      The resolver returns −2 for a weapon word outside the equipment range or a zero recipe byte and
      −1 for a bad recipe, and **all seven call sites discard the return** (`Battle_ProcessActionTarget`
      `00307419` / `00307577`, `BattleFormula_QueryResolvedScalarPreview` `00308BE3`,
      `BattleAction_ResolveSpecialSequenceTargets` `0030ECA4`, `BattleUnit_RunPeriodicCombatMaintenance`
      `0031108C` / `0031124D`, `BattleUnit_HandleActorTimelineEvent` `0031A0CD` — none tests `eax`
      before overwriting it): a failed resolution simply leaves the scratch block as the reset left it.
      **FZ-17.**

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Seven preparation variants, their sizes and the stats each reads | full disassembly of all seven (208–216 B each) | 1 |
| `multiplier = 1 + (Level + Stat) * Stat / 256` | body of `0038AAF0`: `add`/`imul` on `+0x1C2` and `+0x2A`, `mulss` `0.00390625`, `addss` `1.0` | 1 |
| `0.00390625` is exactly 1/256 | IEEE-754 decode of `009088D8` | 1 |
| Attack variance is upward-only and capped at 12.5 % | `comiss` guard, `mulss 0.125`, `div`, `divss 100` in `0038AAF0` | 1 |
| One variant measures against `+0x30`, the rest against `+0x2F` | `movzx eax, byte ptr [rbx+0x30]` in `0038A3A0` vs `[rbx+0x2F]` in the other six | 1 |
| The Speed variant divides by 218 | `divss` against the literal `218` at `00D112D0` | 1 |
| The Scaled150 variant multiplies by 1.5 | extra `mulss` against `1.5` at `00901B3C` | 1 |
| Stat offsets `+0x2A`, `+0x2B`, `+0x2F`, `+0x30` | **independent** confirmation from the four `Reduce*` bodies, which name the stat and read the offset | 1 |
| Reduction multipliers 0.7 / 0.7 / 0.9 / 0.9, and the floor of 1 | full bodies of `0038E870`, `0038E8B0`, `0038E8F0`, `0038E920`; constants decoded from `.rdata` | 1 |
| The three scratch slots are shared globals | all seven write `02AEE054`/`58`/`5C`; `BattleFormula_ResetScratchState` clears them | 1 |
| 380 sites / 45 functions touch the multiplier slot | RIP-relative displacement scan of `.text`, attributed to containing functions | 1 |
| Bow and Crossbow slot bindings | [`../Recipe-System/ranged-weapon-recipes.md`](../Recipe-System/ranged-weapon-recipes.md) | 2 |

**Scope honesty:** this document establishes what the preparation stage *computes*. It does **not**
establish how damage is finally derived from those three values — that is 45 unread functions away,
and no equation of the form "damage = (attack − defence) × multiplier" is asserted here.

## 9. Related

- [`../Recipe-System/ranged-weapon-recipes.md`](../Recipe-System/ranged-weapon-recipes.md) — the slot→variant binding, and the two variants already mapped
- [`../Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md`](../Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md) — scaling applied elsewhere in the same pipeline
- [`../../07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`](../../07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md) — whether the action is allowed at all, before any of this runs

## 10. Falsification pass 2026-09-02 — AJ-2 answered: the damage equation

**Attack chosen.** The document shipped refusing to state a damage equation, saying the three
prepared values were "45 unread functions away". That refusal was correct at the time and is exactly
the thing to attack next: **find the consumer.**

`BattleFormula_FinalizeTargetHpMagnitude` (`0038D280`, 180 B) is it.

### The equation

Every RIP-relative operand below was resolved **by the disassembler**, not by hand — this document
had already published one hex slip elsewhere in the session, and the headline claim should not rest
on mental arithmetic:

```
0038D280  movss  xmm1, [rip+0x2760dd0]   -> 02AEE058   scratch[1] ATTACK
0038D28B  subss  xmm1, [rip+0x2760dc9]   -> 02AEE05C   scratch[2] DEFENCE
0038D293  comiss xmm0(0.0), xmm1
0038D296  jbe    .continue
0038D298  mov    [rip+...] , 0           -> 02AEE004   result = 0, RETURN
   .continue:
0038D2D3  mulss  xmm1, [rip+0x2760d79]   -> 02AEE054   scratch[0] MULTIPLIER
0038D2DB  cvttss2si eax, xmm1                          truncate toward zero
          -> stored to 02AEE004 and/or 02AEE008
```

So, completing what section 2 prepares:

```
raw     = (ATK + variance) - DEF
damage  = (raw <= 0) ? 0
                     : trunc( raw * (1 + (Level + Stat) * Stat / 256) )
```

**Three properties fall straight out of the instruction order, and all three matter in play:**

1. **Subtraction precedes multiplication.** The multiplier scales the *post-defence* remainder, not
   the raw attack. A weapon whose Attack does not exceed the target's Defence deals **exactly
   zero**, regardless of Strength, Level or weapon variant.
2. **The floor is hard and early.** `comiss` + `jbe` writes `0` and returns before the multiplier is
   ever loaded. There is no minimum-damage-of-1 rule on this path.
3. **The result is truncated, not rounded.** `cvttss2si` rounds toward zero, so fractional damage is
   always lost in the target's favour.

### The scratch record is larger than three slots

The finalizer reads two more globals below the prepared triple and writes two result slots:

| Address | Role as read |
|---|---|
| `02AEDFC0` | set to `1` on the early-out branch |
| `02AEDFCC` | mode flag; when nonzero, the finalizer writes `-1` and ORs `1` into `[[r8+0x10]+0x140]` |
| `02AEDFD0` | second mode flag, selecting which result slot is written |
| `02AEE004` | result slot A — **the HP-loss magnitude** (AJ-9, 2026-09-12) |
| `02AEE008` | result slot B — **the HP-gain magnitude**; `test dword ptr [r8+8], 0x1000` is the target's **Reverse** status, which sends the magnitude to the other slot (AJ-9) |
| `02AEE054`–`5C` | the prepared triple (section 2) |

`-1` is used as a **not-set sentinel**: the tail does `cmp eax, -1` and tail-jumps to `00387B00`
only when the value is *not* the sentinel. Which of A and B is HP versus something else is **not**
established — both are written by the same truncated integer, and only a flag distinguishes them.

The tail-jump target `00387B00` (`BattleRuntime_MarkTargetHistoryBit`, 165 B) is now read: it
marks the **target's id bit in the attacker's 0x40-byte history record** — record base
`0208D480 + [rcx+4]·0x40` when kind byte `[rcx+5] == 0` (`00387B1A`–`00387B51`), else
`0208DE80 + [resolved+0xEA9]·0x40` with the object resolved via `0031B860` (`00387B32`–
`00387B55`); the bit index is the target's `[+0xEA9]`, falling back to `[+4]` or `−1`
(which `shl` reduces to bit 31 — an unresolved-target sentinel) at `00387B6A`–`00387B90`,
and the write is `or [rbx+0xC], 1 << cl` at `00387B95`/`00387B97`.

### What this does not settle

This is the *arithmetic core*, not the whole pipeline. Between preparation and this finalizer sit
element affinity (`BattleFormula_ApplyActionElementAffinity`,
`BattleFormula_ApplyEquipmentElementAffinity`), combo and knockback rolls, guard/parry outcome, and
`BattleFormula_ApplyTargetHpPostMultipliers` — 45 functions in total touch the scratch record, and
most rewrite the very slots this equation reads. **The equation is exact for the values present when
the finalizer runs; it does not say those values are still the ones section 2 wrote.** That is the
honest boundary, and it is the next thing to establish.

**AJ-2 is answered** as posed — the final combination is `(attack − defence) × multiplier`,
truncated, floored at zero. The modifier chain that feeds it is registered as **AJ-8**.

## 11. Falsification pass 2026-09-02 (second) — AJ-8: the modifier stages, partly read

**Attack chosen.** Section 10 closed the damage equation but flagged that 45 functions rewrite the
scratch record between preparation and the finalizer, so the equation is exact only *for the values
present when the finalizer runs*. With the
[step table](../Step-Table/combat-formula-step-table.md) and its interpreter now read, that chain is
no longer anonymous: a recipe names its stages, in order, and they can be read one at a time.

### A real pipeline, resolved

The Bow family's committed recipe is `[29, 66, 96, 97, 98, 99, 125, 165, 171, 176, 182]`. Resolved
against the step table, and marking what has actually been read:

| Slot | Step | Read? |
|---:|---|---|
| 29 | `RollPrimaryFormulaResourceReactionMode2Chance` | name only |
| 66 | `PrepareSpeedStrengthAttackVsDefense` | **read** (section 2) |
| 96 | `FUN_0038B950` — scales the **multiplier** | constants only |
| 97 | `FUN_0038BC00` — scales the **multiplier** | constants only |
| 98 | `FUN_0038BE00` — scales the **multiplier** | **read** |
| 99 | `ApplyEquipmentElementAffinity` | name only |
| **125** | **`FinalizeTargetHpMagnitude`** | **read** (section 10) |
| 165 | `ApplyTargetHpPostMultipliers` | **read** |
| 171 | `FUN_0038F9D0` | **read enough to exclude** |
| 176 | `RollPercentGateAndSetResultFlag1000` | name only |
| 182 | `CalcApplyCandidateStatusesOptional` | name only |

**The shape is now clear: three multiplier-scaling stages run *before* the finalizer, and a
post-multiplier stage runs *after* it on the finished integer.**

### Read exactly: slot 98 — a conditional doubling of the multiplier

35 bytes, in full:

```c
rec = arg3->[0x10];
if (rec[0x18] & 1)
    scratch[0] *= 2.0f;        /* the multiplier, before the finalizer */
```

The constant is a literal `2.0` in `.rdata`. One flag bit doubles the damage multiplier.

### Read exactly: slot 165 — 1.2× and 2× on the finished damage

```c
flags = arg3[0x20];
v = resultA;                                  /* 02AEE004 */
if ((flags & 2) && v != -1) { v = trunc(v * 1.2f); resultA = v; }
if (flags & 4) {
    if (v != -1) { v += v; resultA = v; }     /* exactly doubled */
    [02AEE014] = v;
}
```

Two independent bits: **bit 1 gives +20 %, bit 2 doubles.** Both act on the *integer* produced by
the finalizer, so both are applied after truncation — and the ×1.2 is truncated again.

Because they are separate bits, **both can apply**: `trunc(v × 1.2) × 2`. And the `-1` sentinel from
section 10 is respected here — a not-set result is left alone rather than scaled.

This also reveals a **third** result slot, `02AEE014`, written only on the doubling path.

### Profiled, not read: slots 96 and 97

Both scale `scratch[0]`, and their `.rdata` float constants are:

```
slot 96   10, 1.5, 1.3, 0.75, 3
slot 97   2, 1.7, 1.5, 1.4, 0.5, 3, 0.125
```

`2`, `0.5` and `0.125` are the shape of elemental affinity — weak, resistant, strongly resistant —
and slots 95 and 99 either side of them are the two named `ApplyElementAffinity` functions. **That
is a lead, not a finding**: only the constants were extracted, not the conditions that select them,
and this document does not claim which value applies when. **AJ-10.**

### A useful negative: slot 171 is not a damage modifier

`FUN_0038F9D0` (420 B) sits inside the damage pipeline, immediately after the post-multipliers — and
touches **none** of the scratch slots and uses **no** float constants. Whatever it does, it does not
scale damage. Recorded because a step's position in the recipe is otherwise easy to over-read.
*Read 2026-09-12 (FABLE, AJ-11 in §7):* it loads the **on-hit percent gate** `02AEDFE8` from byte
`+0x1F` of the weapon row, or of the ammunition row when the weapon takes ammunition — the
on-hit effect chance the next two steps roll against.

### What this changes

AJ-8 asked whether the equation in section 10 describes what actually lands. The answer so far:
**the multiplier is scaled by up to three stages before the finalizer, and the result is scaled again
after it.** The equation is correct at the point it runs, and is not the whole story — exactly as
section 10 cautioned. The stages are now enumerable rather than merely countable.

### 11a. AJ-8 answered 2026-09-12 (FABLE) — the whole chain, for every weapon family

**Which recipes.** The equipment table's recipe byte `+0x19` over the 557 rows: categories 0–17 (the
weapons) carry recipes **20–29, 64 and 104**, the bow-family categories 7 / 8 / 9 carry **25 / 26 / 27**
([the step table](../Step-Table/combat-formula-step-table.md) for the slot numbers). Their committed lists are one shape:

```
recipe   preparation                                   before finalizer   finalizer  after
20–24    65 / 66 / 67 / 68 / 69                        96 97 98 99        125 (23: 126)  165 171 176 182
25 / 26 / 27 (bows)  66 / 65 / 70                      96 97 98 99        125            165 171 176 182
28       71                                            96 97 98 99        125            165 171 176 182
29       72                                            96 97 98            125            165
64       76                                            96 97 98 99        125            165 166 171 176 182
104      79                                            96 97 98 99        125            165 171 176 182
```

Every list opens with slot 28 (a no-op, AK-5). So **the modifier chain between preparation and the
finalizer is exactly four stages, in this order: 96, 97, 98, 99** — 96 / 97 the paired constant
scalers of §12, 98 the conditional `×2` of §11, and 99 read now — and after the finalizer **165
(the HP post-multipliers), 171 (the on-hit gate load), 176 and 182**, with 166 inserted after 165 on
recipe 64 alone and recipe 29 stopping at 165.

**Slot 99 — `BattleFormula_ApplyEquipmentElementAffinity` (`0038BE30`, 2,791 B), read whole.** The
length is one resolution inlined five times. Each pass resolves **the attacker's weapon row** from
stats `+0x50` (id − `0x1000`, bounds-checked against the equipment registry) and, **when the weapon's
category byte `+0x11` is `0x17`–`0x1A` (the ammunition users), the ammunition row from `+0x52`
instead** (`0038BE69`–`0038BFA0`), takes that row's **element byte `+0x1E`** and tests it against one
of the target's affinity bytes ([the five affinity bytes](../elemental-affinity-and-the-five-bytes.md), [the battle-stats field map](../Battle-Stats-Record/the-battle-stats-record-field-map.md)):

| pass | target byte | effect |
|---|---|---|
| 1 | `+0x43` immune | `02AEDFCC = 1` and **return** — the rest of the chain never runs (`0038C00C`–`0038C01C`) |
| 2 | `+0x40` weak | multiplier `02AEE054 × 2.0` (`0038C1C9`–`0038C1DE`) |
| 3 | `+0x42` resist | `× 0.5` (`0038C577`–`0038C588`) |
| 4 | `+0x41` absorb | `02AEDFD0 = 1`, the absorb flag (`0038C74E`–`0038C75F`) |
| 5 | the **source's** `+0x44` | `× 1.5` — the attacker's own element boost (`0038C8D9`–`0038C8E1`) |

**Slot 176 — `RollPercentGateAndSetResultFlag1000` (`0038FBC0`):** one MT draw `% 100` against the
on-hit gate `02AEDFE8` that slot 171 loaded from the weapon or ammunition row's `+0x1F`; below the
gate the result record's `+0x140` gains **bit 12** (the on-hit effect fires, [the result record](../../07-Combat-Action/Result-Record/the-result-record-field-map.md)), otherwise a
scratch flag is set and nothing else happens. **Slot 182** is
`BattleFormula_ResolveCandidateStatusApplications` with its fourth argument 0 — the *optional* status
pass (181 is the same body with 1, the required pass). **Slot 166** (recipe 64 only, `0038F8E0`)
adds `value × row +0x15 / 100` to a scratch value keyed by the parked action row — a per-row percent
bonus applied only to that family.

**The preview list is the hit roll, and it is now readable too.** `[5, 6, 7, 8, 9, 10, 22, 33, 34, 41]`
(bows: `[5, 6, 22, 33, 34, 35 / 36 / 44, 42 / 43]`): knockback chance and roll (5, 6), parry chance
from Speed and the guard / parry mode roll (7, 8), combo chance and count (9, 10), then **22** loads
the target's evade bytes `+0x33` (block), `+0x32` (parry), `+0x31` (innate evade) into the roller's
three bands and sets the hit base to 100 (`00388FB0`), **33** adjusts them by the action row's flags
(`+4` bit 31 halves the first band; `+4` bit 24, `+8 & 0x2018` and `+8` bit 14 zero bands,
`00389310`), **34** adds the attacker's augment bonuses — effect ids 88 / 89 / 90 (`+0x73` / `+0x83`
bits 0–2) add the augment rows `0x58` / `0x59` / `0x5A` word `+4`, effect id 3 adds row 3, and
`+0x68` / `+0x78` bit 4 adds 25 or 30 by unit class — clamps the total at 100, zeroes the three
bands when the action's `+0x1A` has bit 2, and lets `00384E50`'s bits veto each band
(`00389370`–`003895C2`); **41** rolls the outcome. So the equation of §10 is exact, and what feeds it
is now ordered stage by stage rather than counted.

## 12. Falsification pass 2026-09-02 (third) — AJ-10 answered, and the lead was wrong

**Attack chosen.** Section 11 recorded a lead: steps 96 and 97 scale the multiplier with constants
`2, 1.7, 1.5, 1.4, 0.5, 3, 0.125`, and `2 / 0.5 / 0.125` looks like elemental affinity — weak, half,
strongly resistant — with the two named `ApplyElementAffinity` steps sitting either side. It was
explicitly flagged as a lead because only the constants had been extracted. **Reading the conditions
kills it.**

### The constants are pairs, not a table

Step 97's multipliers do not form an affinity ladder. They come in **pairs**, each selected by the
same three-bit test:

```
call  FUN_002F8E90(unit)      ; returns a category
test  al, 7
je    -> use constant B
      -> use constant A
```

| Stage | `al & 7` nonzero | `al & 7` zero |
|---|---:|---:|
| A | **× 2** | **× 1.7** |
| B | **× 1.5** | **× 1.4** |
| C | **× 0.5** | … |

`2` and `0.5` are not "weak" and "resistant" — they are the *same stage's* value for two different
unit categories. A separate, independently gated stage applies **× 0.125** on
`test byte ptr [rbx+9], 0x10`.

### What the selector actually is

`FUN_002F8E90` (`002F8E90`, 131 B) is a **unit-category classifier**, read in full:

```c
/* `record` is the BattleStatsRecord (BKBI): +5 is its kind byte, +4 its type byte;
   BattleStats_FindOwningBattleUnit maps it to the unit. Renamed from `unit` 2026-09-11. */
if (record == NULL)  return 0x10;
kind = record[5];
if (kind == 0)     return ((byte)(record[4] - 0x1B) <= 0xC) ? 2 : 1;
if (kind != 1)     return 0x10;
v = FUN_00263C20(BattleStats_FindOwningBattleUnit(record) ? owner[0x10] : 0);
if (v == 3)             return 4;
if (v - 1 <= 1 || v == 7) return 8;
return 0x10;
```

It returns one of **`1, 2, 4, 8, 0x10`** — a one-hot category. `test al, 7` therefore splits
`{1, 2, 4}` from `{8, 0x10}`: **two groups of unit categories, each getting its own multiplier.**

`record[5]` is the **same class selector** the availability cascade branches on (see
[`../../07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`](../../07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md),
where `raw[5]` values `0` and `1` take different gates). Two independently documented systems branch
on the same byte, which raises its importance: it is not a local detail.

### Two-layer convention, fourteenth sighting — at a fourth offset pair

Step 97 gates one of its stages on:

```
test byte ptr [rbx + 0x68], 0x20
jne  take
test byte ptr [rbx + 0x78], 0x20
je   skip
```

`+0x68` / `+0x78` — again a **`0x10` stride**, and a **fourth** distinct pair after status
(`+0x3C`/`+0x64`), rewards (`+0x6B`/`+0x7B`) and action cost (`+0x6C`/`+0x7C`). The convention is now
attested across four field pairs in four subsystems.

Step 97 also re-reads the status pair directly — `eax = rdi[0x64] | rdi[0x3C]` — testing bits 16 and
28 to pick a comparison value, then compares it against `rdi[0x48]`. Two HP-like fields (`+0x24`,
`+0x48`) are involved, one of them conditionally doubled. ~~**What that comparison means is not
established** and is not guessed here.~~ **Read whole 2026-09-12 (FABLE) — step 97 is the
HP-conditioned augment step**, `0038BC00(casterStats, targetStats, ctx)`, four gates on one
multiplier slot `02AEE054`, each scaled by a constant the caster's category picks (`FUN_002F8E90`,
`test al, 7`: `{1, 2, 4}` first, `{8, 0x10}` second):

| gate (`0038BC0F`–`0038BDE6`) | effect id, by the shipped help text ([the battle text banks](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md) §5.1) | scale |
|---|---|---|
| caster merged id **10** (`ctx+0x1B` bit 2, [the evaluation context](../Evaluation-Context/the-evaluation-context-field-map.md) `+0x1A`) **and** caster status 29 HP Critical (`ctx+4` bit 29) | **Adrenaline** — *"Raises strength when HP Critical"* (licence node 223) | ×2 / ×1.7 |
| caster merged id **11** (`ctx+0x1B` bit 3) **and current HP == cap** — the cap is `max(+0x48, 1)` under bit 16 Disease, else `+0x24` doubled under bit 28 Bubble, exactly [the HP write](../Current-HP/the-hp-write-and-the-lethal-transition.md)'s rule | **Focus** — *"Raises strength when character has full HP"* (node 225) | ×1.5 / ×1.4 |
| target layer id **5** (`[target+0x68]` / `[target+0x78]` byte 0 bit 5) **and** target status 29 (`ctx+8` bit 29) | **Last Stand** — *"Reduces physical damage taken when HP Critical"* (node 227) | ×0.5 / ÷3 |
| target layer id **40** (`+0x6D` / `+0x7D` bit 0), through a registry lookup (`0038BD06`–) | augment row 40 — *"NOT USED"* in the shipped texts | ×0.125 |

So the "HP-like comparison" is the **full-HP test** for Focus, and the slot-97 constants the profile
listed (`2, 1.7, 1.5, 1.4, 0.5, 3, 0.125`) are these seven, none of them elemental. **AJ-12.**

### Step 96 is gated differently again

Its multipliers pair with integer comparisons rather than the category test — `× 1.3` after
`cmp ecx, 0x15`, `× 0.75` after `cmp eax, 0x12`, `× 3` after `test bl, 1`. So the two steps are not
variants of one mechanism; they are separate modifier stages that happen to be adjacent.

### The lesson

The lead was built from **constants alone**, and constants are exactly the kind of evidence that
invites pattern-matching: `2` and `0.5` look like elemental multipliers because elemental systems in
many games use those values. The conditions were what distinguished the two readings, and they were
one disassembly away. **A set of plausible-looking constants is not evidence of a mechanism** — it is
a prompt to go and read the branch that selects them.

**AJ-10 is answered: not elemental affinity.**

## 13. Correction 2026-09-06 — the 255 cap is wrong for four of seven values

**What was believed.** *"Every attribute is a single byte, so all of them cap at 255."* Stated twice
— in section 3 as a conclusion and in section 6 as modding advice.

**What is now believed.** `BattleStats_RebuildEffectiveStatsAndAffinityState` (`0x002FEF30`) clamps
the four core attributes to **99**:

```
002FF829  mov   r15d, 0x63          ; 99
002FF83C  cmovg r12d, r15d          ; -> +0x2A  Strength
002FF851  cmovg r13d, r15d          ; -> +0x2B  Magick Power
002FF86B  cmovg r8d,  r15d          ; -> +0x2C  Vitality
002FF885  cmovg r9d,  r15d          ; -> +0x2D  Speed
```

Only `+0x2E`-`+0x30` — Attack, Defence, Magick Resist — take the 255 ceiling, and the rate fields
above them are clamped to **100**, which is what a percentage looks like.

**What proved it.** `repos-c7`'s complete read of `0x002FEF30`, 2026-09-06, against GN160
`fa0db293...d2f708`. Merged 2026-09-07 as a correction under `CB` in
[`../../_index/OPEN-QUESTIONS.md`](../../_index/OPEN-QUESTIONS.md).

**Why the earlier reading was reachable, which is the part worth keeping.** The cap was inferred
from the **storage type** rather than from a **writer**. A byte holds 0-255, so 255 looked like the
range — and nothing in this document's own evidence contradicted it, because this document never
read the function that writes the block.

> **A field's width is not its range.** This is the same failure shape as naming a field from its
> position: both substitute a property of the encoding for a property of the mechanism. Anywhere
> this database states a limit without citing the instruction that enforces it, the same mistake is
> available.

**The independent check that agrees.** The four clamped to 99 are exactly the four FFXII caps at 99
on screen; the three clamped to 255 are the derived combat values the player never sees a cap for.
The naming of those seven offsets was taken from readers, not from the clamps — so the clamps
agreeing field for field is corroboration rather than circularity.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL and recorded in the registry.*

**Movement — CLIENT.** `BattleStats_FindOwningBattleUnit` is also used by two locomotion bodies, of 89 and 706 bytes, to
find a stats record's unit. They are lookups and play no part in the attack-versus-defense scaling.

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Resource — CLIENT, not read.** One cited function is called by eight Resource bodies (136 to 522 bytes). What those Resource bodies do with it is not read here.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**ActorEntity — CLIENT (9 edges through 4 of this page's functions).** The ActorEntity layer reaches this page at `00263C20`, `0032E400`, `0031B860`, `002F8E90`. `BattleUnit_GetBySlotIndex` is the worked example, read in full - it is **37 bytes that give the record its width**: the index is bounded against `[0208E6A0] - 1` and indexes `[0208E688]` at a **`0xF50`-byte stride** - 3,920 bytes, the same figure the slot-pool page states from the other end; **6 of the 9 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Party — CLIENT (1 edge).** `002E73C0`, the `+0x284`-gated render-record resolve above, is also called from the party layer — the same resolve serves both surfaces. Crossing accounted at subsystem level (SWE2-EC7, 2026-09-18).

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. Most edges come from four shared bodies this page cites: the generator thunk `RNG_MT19937_NextU32_Thunk` (`00379CD0`, AJ-7), the stats-record owner lookup `BattleStats_FindOwningBattleUnit` (`0031B860`), the rebuild `BattleStats_RebuildEffectiveStatsAndAffinityState` (`002FEF30`, cited in section 13 for its clamp), and the render-record chain the appended `00389370` subtree note walks (`002E7FD0` into `CharacterRenderRecord_RefreshFCPPayloadByRecordId` `002EDBD0`).*

**CoreRuntimeScheduling — CLIENT, MECHANICAL (2 edges).** `0022B6E0` and `0022B7E0`, two per-frame main-loop bodies, call `00379CD0`: they draw from the same single MT19937 state the attack variance draws from (AJ-7), so their draws move the shared sequence; no formula is shared.

**Gameplay — OUT-OF-SCOPE (2 edges).** `002FEF30` calls `BattleUnit_UpdateEngagementStateFlag` (`00307D10`) and `BattleEncodedId_IsValidForClass` (`00322C50`): this page cites the rebuild only for the ceilings it applies to the stat block (section 13), and its engagement update and id validation play no part in the attack-versus-defence scaling.

**Items_Equipment_Shops_License — CLIENT, OUT-OF-SCOPE (5 edges).** `Equipment_EvaluateCandidateLoadoutAndBuildDerivedStats` (`0030A4E0`) calls `002FEF30` to preview a candidate loadout's stats, and `BattleStats_SetEquipmentSlotByStatsIndex` (`0031A410`), `BattleStats_SetEquipmentSlotByMappedId` (`0031A510`), `BattleStats_SetEquipmentSlotDirect` (`0031A630`) and `BattleStats_SetLicenseNodeStateAndApplySideEffects` (`00323910`) call `0031B860`. Equipment changes reach the stat block this page's preparers read only through that rebuild; the slot setters share the owner lookup and nothing else.

**Presentation — SERVICE and CLIENT, OUT-OF-SCOPE (36 edges).** The payload validity check `002E7FD0` tails into `002EDBD0`, which caches the `FCP@` section pointer and tails into `CharacterRenderRecord_GetFCPPresentationConfigurationPayload` (`003E55F0`); `002EDBD0` is also called by `003E6150`, `004256E0` and `0046CC70`; and the rest are render bodies calling the lookups this page's appended notes cite — `003E55F0` (seven callers, `0041EDE0` and `00427320` among them), `ResourceEntry_FindSectionPointerByTagAndName` `00409660` (six, among them `PresentationEntry_InitializeFromResourceDefinition` `0041D220`), the 17-byte id guard `00409F50` (fifteen, among them `PresentationAuthoredCommand_Class09_ActivateLoadedResourceState` `00417F40` and `CharacterRenderRecord_MaintainPresentationResourceReferences` `00422A30`), the table lookup `0032E400` (`003B2310`, `003B53C0`) and the packed-field decoder `004FE2F0` (`004256E0`). The preparation step reaches the render record's presentation payload through one validity check; the page asserts nothing about what the renderer does with it.

**RNG_Random_Selection — SERVICE and DEPENDENCY (27 edges).** Every roll-taking preparer and roll on this page calls `00379CD0` — the seven `Prepare…AttackVsDefense` variants (`BattleFormula_PrepareStrengthAttackVsDefense` `0038AAF0`, `BattleFormula_PrepareMagickPowerAttackVsDefense` `0038AE50` and five more), the preview rolls `BattleFormula_ComputeKnockbackChance` (`00388350`), `BattleFormula_RollKnockback` (`00388440`), `BattleFormula_RollGuardParryMode` (`003884F0`), `BattleFormula_RollAndStoreComboCount` (`00388660`), the evade ladder `003896B0`, `00389820`, `00389950`, `00389A50`, and the percent gates `0038FB80`, `0038FBC0` among them — and `RNG_MT19937_NextU32` (`00863BF0`) calls `RNG_MT19937_TwistState` (`00866B90`) and `RNG_MT19937_SeedState` (`00866D60`). The attack variance and every recipe roll depend on that layer's one lazily seeded Mersenne Twister, drawn in recipe order (AJ-7).

**Rewards_Progression_Economy — CLIENT, MECHANICAL (4 edges).** `Reward_ComputeExperienceForRecipient` (`002F8BB0`) and `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` (`0030C650`) call `0031B860`, and `002F9A60` and `002F9B20`, which the level advance calls, call `00379CD0`: rewards and levelling find a record's owner with the same lookup and the level advance draws from the same generator, sharing the sequence and no formula with this page.

**Script_VM_Native_Bridge — CLIENT, MECHANICAL (4 edges).** The script natives `00354BF0` (the `rand` verb, id `0x29`) and `00355140` call `00379CD0`; `003401D0` calls the render-record resolve `002E73C0`; and `0050DF70` calls the table lookup `0032E400`. Script draws share the gameplay generator's sequence, and the other two calls are shared helpers; no script native reaches the preparers.

**Status_Periodic_Terminal — CLIENT (8 edges).** `BattleFormula_BuildRuntimeCounterPeriodicHpCredit` (`00386860`) calls the unit-category classifier `002F8E90` and `0031B860`; `BattleStats_RecomputeDerivedStateAndAutoStatuses` (`0030FED0`) calls `002FEF30` and `0031B860`; `BattleUnit_ResolvePeriodicPrimaryResourceRecoveryStep` (`002F9400`), `BattleStats_ChangeStatusAndProcessSideEffects` (`0030E360`) and `BattleStats_RemoveStatusesFromMaskAndRecompute` (`0030F690`) call `0031B860`; and `BattleFormula_AdvanceStatusTimersAndBuildResult` (`00386C70`) calls `00379CD0`. Status code classifies units with the same classifier, rebuilds the stat block the preparers read and draws from the same generator; it does not call the preparers.

**UI — CLIENT, OUT-OF-SCOPE (7 edges).** `ActorRuntime_GetClassNibble` (`00263C20`), which section 12 cites inside the category selector, is called by `BattleMenu_RecordSelectedTargetAndCursorContext` (`0027D330`), `002734F0`, `002BF0E0`, `002C7660`, `00322A80`, `003C5130` and `003C8B70`: menu and HUD code reads the same actor class nibble, and none of it takes part in the scaling.

**WorldAreaField and World — CLIENT, MECHANICAL (8 edges).** `MapRef_BeginLoadResources` (`00268750`), `AreaArd_LoadOrUnloadFieldResource` (`003EA820`), `003319D0`, `00378030`, `00379A10` and the World-filed `00378540` call `0032E400` — an 80-byte lookup that returns a per-id dword from a table of up to 1,024 entries, or a fallback, rounded up to a multiple of 64 — and the weather-slot selectors `0025ABA0` and `0025ACA0` call `00379CD0`. Field loaders use the same lookup and weather selection draws from the same generator; neither reaches the attack-versus-defence preparation.

## The `00389370` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`00389370` (258 B) — the attack/defense preparation step:
`002F8E90` ×2 (`00389394`/`003893A9`), `dword[02AEDFEC]` counter
check/read/write-back (`0038939D`/`003893AE`/`003893BF`),
`dword[02AEDFF0]` vs `esi` (`003893C7`), then `[02EBF040]` context +
`0020E600` row lookups (`003893E2`/`003893FB`/`0038940F`).

| member | role | interior |
| --- | --- | --- |
| `002E7FD0` (33 B) | payload validity check — `[rcx+0xC0]` null-gate (`002E7FD5`), `dword[rax] == -1` (`002E7FE1`), tail `002EDBD0` (`002E7FE9`) | [`002E7FE1`](../../_index/ADDRESS-INDEX.md) |
| `00384E50` (225 B) | unit resolve — `0031B860` → `[02EBF188]` publish (`00384E66`/`00384E6B`), `qword[rax+0x10]` nonzero gate (`00384E77`) | [`00384E6B`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `002F8E90`, `0020E600`, `0031B860`,
`002EDBD0`. The `02AEDFEC`/`02AEDFF0` cells are the shared
preparation counters.


### Interior citation — frontier hub `002EDBD0` (2026-09-18, SWE2-EC7)

`002EDBD0` — 183 B, 7 callers, `CharacterRenderRecord_RefreshFCParam`: the
tail `002E7FD0`'s validity check hands to. Read from the shipping image:
`cx == -1` returns 0; the `0x740` resolve off `022C6F28` requires
`[+0x284]` non-zero (the inverse of the `002E73C0` siblings); `word[+0x408]`
(`-1` gated) feeds `0020E600` then `00409F50` on `[+0xD90]`, and
`00409660(0x50434640, &rec+0x3C)` — the `FCP@` lookup — caches `result+0x30`
into `[+0x400]` at [`002EDC33`](../../_index/ADDRESS-INDEX.md) before tailing
`003E55F0`.

## SWE2-EC7-82 update (2026-09-20) - `004FE2F0` packed-field decoder measured

`004FE2F0` (204 B) is the encoded-value decoder the stat callers
share: `edx == 0x40000000` returns `byte[rcx+1]`; `edx >> 29 == 1`
uses byte `[rcx+0x32]` as a bound - inside it, `word[rcx +
((edx>>18)&0x1F)*2]` offsets a record whose `[(edx>>8)&0xFF]`-indexed
dword returns, else the fallback `01EB16B0` table answers; `edx >>
29 == 3` instead offsets through `word[+0x12]` and extracts the
`(edx>>18)&0x1F` shift's low byte; other kinds return -1.
Interior anchor `004FE33A` (the fallback-table dword fetch).
