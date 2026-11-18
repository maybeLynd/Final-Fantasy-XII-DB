[Home](../../README.md) / [Rewards: EXP, LP, gil and loot](README.md) / Stat growth on level-up

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Stat growth on level-up: HP, MP, Strength, Magick Power, Vitality and Speed per level, starting stats, and the level-up notices | system | Rewards: EXP, LP, gil and loot | EXP, loot and progression | What changes when a character gains a level: the shared HP/MP growth table with its random bonus, the per-character Strength, Magick Power, Vitality and Speed growth bytes with each character's values, the starting stats and starting gil, the cap of 99, who can set a level, and the level-up message, popup and sound. | 0x0030C650, 0x002F9A60, 0x002F9B20, 0x002F9BD0, 0x0030C470, 0x00863BF0 |

## What the player sees

Each level adds a fixed amount of Strength, Magick Power, Vitality and Speed that depends on the
character, and an amount of raw max HP and max MP that is the same for everyone at a given level plus a
small random bonus.

Each character's max HP is `raw HP × (+0x18 + 1) × +0x19 / 100` and its max MP `raw MP × +0x1D / 100`, kept as
whole numbers (`0x002FEF30` through `0x002F8E50` and `0x002F9180`; [the party table](../Party/party-table.md)).
`+0x19` and `+0x1D` are each character's own, 147 and 134 for Vaan and 132 and 152 for Penelo, and `+0x18` is 0
except on the Espers' rows, which have 1 to 3. So the same growth gives different characters different maximums,
before equipment and other adjustments.

A big kill can raise several levels at once; the stats grow once per level gained, and the notice, popup and sound
play once, for the last level. Levels stop at 99.

A summoned Esper is grown on the spot to its summoner's level with its own growth values and never gains levels from kills,
because the EXP formula pays Espers nothing. The Chocobo's four stats are at the cap
from its first level, and it is left out when a kill's EXP is divided ([EXP, LP and level-ups](exp-lp-and-level-ups.md)).

The growth numbers come from two tables in `battle_pack.bin`. One is a list of HP and MP gains per level that every
character shares; the other is the character table `chr_data`, whose row for each character holds its starting stats
and its Strength, Magick Power, Vitality and Speed gain per level.

## How it works

### The level walk

`0x0030C650(record, target, flags)` raises a stats record from its current level
`+0x1C2` to `min(target, 99)` one level at a time (`0x0030C67A`-`0x0030C682`, back-edge `0x0030C865`). It
never lowers a level: when the target is not above the current level it returns at once. Each step:

| Step | What happens | Where in the code |
|---|---|---|
| 1 | When the record is a party record (stats byte `+0x05` = 0) and the level is below 99, the stats grow. `L` is the level before the step, and `row` is row `+0x04` (the character's type id) of `chr_data`, the table in registry slot `0x02EBF130` (`battle_pack.bin` directory `+0x44`, 40 rows of `0x80` bytes):<br>• raw HP `+0x08` (dword) `= 0x002F9A60(L, HP)`, which `0x002FEF30` turns into max HP (above);<br>• raw MP `+0x0C` (i16) `= 0x002F9B20(L, MP)`, likewise for max MP;<br>• Strength `+0x10` (float) `= 0x002F9BD0(Strength, row.b[+0x1F])`;<br>• Magick Power `+0x14` `= 0x002F9BD0(Magick Power, row.b[+0x22])`;<br>• Vitality `+0x18` `= 0x002F9BD0(Vitality, row.b[+0x25])`;<br>• Speed `+0x1C` `= 0x002F9BD0(Speed, row.b[+0x28])`. | `0x0030C6CC`, `0x0030C6D9` |

   Every `chr_data` row is built as a party record (`0x0023AC80`, kind 0 sets `+0x05` = 0), the Espers
   (rows 27-39) and the Chocobo (row 26) included, so this applies to them too.
2. The level byte goes up by one, capped at 99.
3. On the last step only: the derived stats are rebuilt (`0x0030FED0(record, 0)`), and the notices
   below are posted unless flags bit `0x2` is set.

The `chr_data` row is the table's word `+8` times the type id plus the value `0x0020E600` gives for the table's
`+0xC`, added in 32 bits¹, so the upper half of that pointer is dropped. Nothing guards
it: when `[0x02EBF130]` is null or `0x0020E600` gives 0 the row is 0², HP and MP still grow, and the
Strength read at `0x0030C757` faults. A step that starts at level 99 or above changes nothing, the last-step work
included³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030C70B`-`0x0030C71D` |
| ² | `0x0030C721` |
| ³ | `0x0030C6D3` |

</details>

The notices, for a party record:

- message 4 carrying the record and the new level, through `0x0046A690` and `0x0046AB10`;
- when `0x0031B860` finds the record's unit on the field and that unit's stats are party-kind
  (`[unit+0x698]` byte `+0x05` = 0): the HUD popup `0x002905D0(unit id, from level, new level)`
  (`[0x0209BE80] + 0x7FB0`), a call to `0x002EACD0(unit id)`, and sound 7 (`0x003A1180` / `0x002DF220`, then
  `0x00329210(1)`).
- the popup is reached through the jump `0x0035D8C0`¹ with the level the walk started from and the new
  level byte; `0x002EACD0` takes `(unit id, 1, unit + 8, 0x71)`²; the sound step asks
  `0x003A1180(7)` for a handle, stops when it is -1³, and otherwise plays `0x002DF220(handle, 0x40, 0x7F)`
  and hands its result to `0x00329210(1, result)`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030C815` |
| ² | `0x0030C81A`-`0x0030C82C` |
| ³ | `0x0030C83E` |
| ⁴ | `0x0030C840`-`0x0030C857` |

</details>

### HP and MP growth

HP and MP growth read `hpmpbase_data`, the table in registry slot `0x02EBF108` (`battle_pack.bin`
directory `+0x28`, 99 rows of 2 bytes, row = level before the step):

```c
// 0x002F9A60: b = row.hp (byte 0)
bonus = (b / 5.0f >= 0.01f) ? (MT() % (int)(b / 5.0f * 100.0f)) / 100.0f : 0;
HP   += b + (int)bonus;                     // bonus is 0 .. b/5 - 0.01, truncated

// 0x002F9B20: b = row.mp (byte 1)
bonus = (b >= 0.01f) ? (MT() % (int)(b * 100.0f)) / 100.0f : 0;
MP   += b + (int)bonus;                     // 0 .. b - 1 extra
```

`MT()` is `0x00863BF0`, the Mersenne Twister whose state starts at `0x02EB3870` (index `0x02EB4230`). On its
first use it seeds itself with 5489 (`0x1571`, `0x00866D60`).

All 99 rows, with the smallest and largest gain each formula allows, are in [hp-mp-growth.tsv](hp-mp-growth.tsv),
read from the shipped file.

### Columns of hp-mp-growth.tsv

| Column | Holds |
|---|---|
| `hp_base` | byte 0 of the row, the base raw-HP gain `b` for the level-up from `level` |
| `hp_gain_min` | the smallest raw-HP gain, `b` itself (bonus 0); equal to `hp_base` on all 99 rows |
| `hp_gain_max` | the largest raw-HP gain, `b + (int(b / 5 × 100) - 1) / 100` rounded down, or `b` when `b / 5` is below 0.01 |
| `mp_base` | byte 1 of the row, the base raw-MP gain `b`: 1 to 5 |
| `mp_gain_min` | the smallest raw-MP gain, `b`; equal to `mp_base` on all 99 rows |
| `mp_gain_max` | the largest raw-MP gain, `b + (int(b × 100) - 1) / 100` rounded down, which is `2b - 1` |

The gains are to the raw values `+0x08` and `+0x0C`. A raw-HP gain `g` moves max HP from `HP × k / 100` to
`(HP + g) × k / 100` with `k = (+0x18 + 1) × +0x19`, and a raw-MP gain the same way with `k = +0x1D`.

### Strength, Magick Power, Vitality and Speed

The four stats grow by `0x002F9BD0`: `value + byte / 128`, and a result above 100.0 becomes
99.99999¹. There is no random part.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002F9BD7`-`0x002F9BEC` |

</details>

### Starting values

`0x0030C470(record, level, ...)` sets the level byte to 0¹. For a party
record it then copies the row's starting values:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030C496` |

</details>
- raw HP from `row.u16[+0x16]` and raw MP from `row.u16[+0x1A]`¹;
- the four stats from the base bytes `+0x1E`, `+0x21`, `+0x24`, `+0x27`²;
- byte `+0x20` from `row.b[+0x46]`, or from `0x00324100(record)`, the largest licence-granted value, when
  that is larger.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030C4F9`-`0x0030C507` |
| ² | `0x0030C50B`-`0x0030C546` |

</details>

Then it calls `0x0030C650(record, level, 2)`¹, so a new character grows silently
from level 0 to its starting level, and sets the EXP total `+0x18C` to `0x002F8F20(level - 1)`, the EXP
needed for that level, capped at 99,999,999². The summon start calls it as
`0x0030C470(Esper record, summoner's level, 0)` (`0x003069EE` in `0x00306760`), so an Esper is rebuilt from
level 0 to the summoner's level every time it is summoned.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030C562`-`0x0030C56E` |
| ² | `0x0030C573`-`0x0030C586` |

</details>

An enemy record (kind byte `+5` = 1) skips the row copy and stores the third argument at `+0x88`¹; a
record of any other kind keeps only the level byte 0 and returns². For a party record the row read is
unguarded: when `[0x02EBF130]` is null³ or `0x0020E600` returns 0⁴, the row base is 0 and
`0x0030C4F9` reads the word at address `0x16`, which faults, because the first 64 KB of a Windows x64 process are
never mapped.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030C4B1` |
| ² | `0x0030C4AB` |
| ³ | `0x0030C4C7` |
| ⁴ | `0x0030C4D4` |

</details>

After the EXP total it removes the statuses in `0x0208D320 | 0x0208D324` when that is non-zero¹ and reconciles HP and MP². It then sets the starting MP `+0x4C`:
`+0x28` times row byte `+0x47` / 100 for a party record, `+0x28` for an enemy, 0 for either when layer byte `+0x6C`
or `+0x7C` is negative³. Last it rebuilds the derived state with `0x0030FED0(record, 0)`
(`0x0030C602`; [battle unit construction](../Characters-And-Objects/battle-unit-construction.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030F690`, `0x0030C58C`-`0x0030C59D` |
| ² | `0x0030F340`, `0x0030F5A0` |
| ³ | `0x0030C5B2`-`0x0030C5F9` |

</details>

The EXP formula pays the Esper type ids `0x1B`-`0x27` nothing: `0x002F8BB0` returns 0 when `(u8)(type - 0x1B) <= 0x0C`
for the record's type id `+0x04` (`0x002F8BF2`-`0x002F8BFA`; [EXP, LP and level-ups](exp-lp-and-level-ups.md)), so kills
do not raise an Esper's level. A character's starting gil (`row.u16[+0x3E]`) is added once, on its
first activation (see [Gil](gil.md)).

**Who calls the level walk:**

| Caller | Call | Target level | Flags |
|---|---|---|---|
| `0x0030C470` | `0x0030C56E` | the starting level | 2 (silent) |
| `0x00312280` | `0x003124A3` | the level the EXP total reaches (see [EXP, LP and level-ups](exp-lp-and-level-ups.md)) | 0 |
| `0x003112F0` | `0x003113DF` | result byte `+0x11C` (the target's new level, `0xFF` = no level change) | 0 |
| `0x003112F0` | `0x003113FD` | result byte `+0x11D` (the source's new level) | 0 |
| `0x00305960` | `0x003059CB` | 99, for every record of party map 3 | 0 |

## Layouts

<details>
<summary>Show the memory layouts</summary>

`ChrDataRow` (`0x80` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x16` | `u16` | startHp | raw HP at level 0; Vaan's 46 gives max HP 67 |
| `+0x18` | `u8[2]` | hpFactors | the max-HP factor and percentage; not read by the growth code |
| `+0x1A` | `u16` | startMp | raw MP at level 0 |
| `+0x1C` | `u8[2]` | mpPercent | `+0x1C` is 0 on every row, `+0x1D` the max-MP percentage; not read by the growth code |
| `+0x1E` | `u8` | strBase | Strength at level 0 |
| `+0x1F` | `u8` | strGrowth | Strength gained per level, in 1/128 |
| `+0x20` | `u8` | pad20 | 0 in every shipped row |
| `+0x21` | `u8` | magBase | Magick Power at level 0 |
| `+0x22` | `u8` | magGrowth | Magick Power gained per level, in 1/128 |
| `+0x23` | `u8` | pad23 | 0 in every shipped row |
| `+0x24` | `u8` | vitBase | Vitality at level 0 |
| `+0x25` | `u8` | vitGrowth | Vitality gained per level, in 1/128 |
| `+0x26` | `u8` | pad26 | 0 in every shipped row |
| `+0x27` | `u8` | spdBase | Speed at level 0 |
| `+0x28` | `u8` | spdGrowth | Speed gained per level, in 1/128 |
| `+0x29` | `...` | tail29 | `+0x29` to `+0x7F`, the rest of the row; not read by the growth code |

The whole row, with the readers of the fields the growth code skips, is on
[party-table](../Party/party-table.md).

</details>

## Shipped data

<details>
<summary>Show the shipped data</summary>

Growth bytes (`+0x1F` Strength, `+0x22` Magick Power, `+0x25` Vitality, `+0x28` Speed) and starting gil
(`+0x3E`) of the `chr_data` rows, names from the row's name reference (`+0x30`), in the
`test_battle/us` `battle_pack.bin`:

| Row | Name | Str | Mag | Vit | Spd | Gil |
|---:|---|---:|---:|---:|---:|---:|
| 0 | Vaan | 72 | 67 | 48 | 18 | 0 |
| 1 | Ashe | 68 | 70 | 44 | 17 | 0 |
| 2 | Fran | 64 | 63 | 47 | 18 | 300 |
| 3 | Balthier | 67 | 59 | 45 | 19 | 300 |
| 4 | Basch | 69 | 56 | 36 | 16 | 0 |
| 5 | Penelo | 65 | 72 | 48 | 16 | 150 |
| 6 | Reks | 68 | 59 | 42 | 15 | 0 |
| 7 | Amalia | 68 | 70 | 44 | 17 | 1230 |
| 8, 9 | Basch | 69 | 56 | 36 | 16 | 0 |
| 10 | Lamont | 65 | 66 | 48 | 16 | 0 |
| 11, 12 | Vossler | 70 | 50 | 36 | 18 | 0 |
| 13 | Larsa | 65 | 66 | 48 | 16 | 0 |
| 14 | Reddas | 67 | 60 | 42 | 19 | 1868 |
| 15 | Basch | 68 | 50 | 36 | 16 | 0 |
| 16 | Reddas | 67 | 60 | 42 | 19 | 0 |
| 26 | Chocobo | 100 | 255 | 255 | 255 | 0 |
| 27-39 | Belias, Mateus, Adrammelech, Hashmal, Cúchulainn, Famfrit, Zalera, Shemhazai, Chaos, Zeromus, Exodus, Ultima, Zodiark | 75-78 | 75-78 | 35 | 30 | 0 |

Rows 17-25 have the placeholder name "No name". The Chocobo's bases are 255 and its growth bytes push
every stat past 100.0 at the first step, so its four stats sit at 99.99999. The Esper rows are used each
time an Esper is summoned (above).

`hpmpbase_data`, level before the step : HP byte / MP byte:

```python
 0:10/3   1:11/3   2:12/3   3:13/3   4:14/3   5:15/3   6:16/3   7:17/3   8:18/3   9:19/3
10:20/4  11:21/4  12:22/4  13:23/4  14:24/4  15:25/4  16:26/4  17:27/4  18:28/4  19:29/4
20:30/4  21:31/4  22:32/4  23:33/4  24:34/4  25:33/4  26:32/4  27:31/4  28:30/4  29:29/5
30:28/5  31:27/5  32:26/5  33:25/5  34:27/5  35:29/5  36:31/5  37:33/5  38:35/5  39:37/5
40:39/5  41:41/5  42:43/5  43:45/4  44:47/4  45:49/4  46:51/4  47:53/4  48:55/4  49:53/4
50:51/4  51:49/4  52:47/4  53:45/4  54:43/4  55:41/4  56:39/4  57:37/4  58:35/4  59:33/4
60:31/3  61:29/3  62:27/3  63:25/3  64:23/3  65:21/3  66:19/3  67:20/3  68:21/3  69:22/3
70:23/3  71:24/3  72:25/3  73:26/3  74:27/3  75:28/3  76:29/3  77:30/3  78:31/3  79:32/3
80:33/2  81:34/2  82:35/2  83:36/2  84:37/2  85:38/2  86:39/2  87:40/2  88:41/2  89:42/2
90:43/1  91:44/1  92:45/1  93:46/1  94:47/1  95:48/1  96:49/1  97:50/1  98:51/1
```

The fixed parts sum to 3,210 HP and 333 MP from level 0 to 99, before the random bonuses.

</details>

## Modding notes

- HP and MP growth are shared by every character: edit `hpmpbase_data` (directory `+0x28`). A
  character's own HP and MP differ by its starting values `+0x16` / `+0x1A`, its percentages `+0x19` and
  `+0x1D` and its factor `+0x18`, which `0x002FEF30` applies to the raw values
  ([the party table](../Party/party-table.md)).
- Per-character growth of the four stats is `chr_data` bytes `+0x1F`, `+0x22`, `+0x25`, `+0x28`, in
  1/128 per level; with the base bytes, a stat at level `L` is `base + L × growth / 128`.
- The level cap 99 is code (`0x0030C650`, and `0x002F8F20` on [EXP, LP and level-ups](exp-lp-and-level-ups.md)), not data.

## Related

- [EXP, LP and level-ups from kills: who receives them, the formulas, the split, the doublers and the EXP table](exp-lp-and-level-ups.md)
- [Gil: storage, the gil cap, every way gil changes, and the Plunderer and Spendthrift counters](gil.md)
