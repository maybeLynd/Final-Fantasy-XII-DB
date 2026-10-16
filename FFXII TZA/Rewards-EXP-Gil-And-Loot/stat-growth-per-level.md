---
title: "Stat growth on level-up: HP, MP, Strength, Magick Power, Vitality and Speed per level, starting stats, and the level-up notices"
kind: "system"
category: "Rewards: EXP, LP, gil and loot"
addresses: "0030C650, 002F9A60, 002F9B20, 002F9BD0, 0030C470, 00863BF0"
---

## What the player sees

Each level adds a fixed amount of Strength, Magick Power, Vitality and Speed that depends on the
character, and an amount of max HP and max MP that is the same for everyone at a given level plus a
small random bonus. A big kill can raise several levels at once; the stats grow once per level gained,
and the notice, popup and sound play once, for the last level. Levels stop at 99. A summoned Esper is
grown on the spot to its summoner's level with its own growth values; the Chocobo's four stats are at
the cap from its first level. Neither gains levels from kills, because kills give them no EXP.

## How it works

### The level walk

`0030C650(record, target, flags)` raises a stats record from its current level
`+0x1C2` to `min(target, 99)` one level at a time (`0030C67A`-`0030C682`, back-edge `0030C865`). It
never lowers a level: when the target is not above the current level it returns at once. Each step:

1. When the record is a party record (stats byte `+0x05` = 0) and the level is below 99, the stats grow
   (`0030C6CC`, `0030C6D9`). `L` is the level before the step, and `row` is row `+0x04` (the
   character's type id) of `chr_data`, the table in registry slot `02EBF130` (`battle_pack.bin`
   directory `+0x44`, 40 rows of `0x80` bytes):
   - max HP `+0x08` (dword) `= 002F9A60(L, HP)`;
   - max MP `+0x0C` (i16) `= 002F9B20(L, MP)`;
   - Strength `+0x10` (float) `= 002F9BD0(Strength, row.b[+0x1F])`;
   - Magick Power `+0x14` `= 002F9BD0(Magick Power, row.b[+0x22])`;
   - Vitality `+0x18` `= 002F9BD0(Vitality, row.b[+0x25])`;
   - Speed `+0x1C` `= 002F9BD0(Speed, row.b[+0x28])`.

   Every `chr_data` row is built as a party record (`0023AC80`, kind 0 sets `+0x05` = 0), the Espers
   (rows 27-39) and the Chocobo (row 26) included, so this applies to them too.
2. The level byte goes up by one, capped at 99.
3. On the last step only: the derived stats are rebuilt (`0030FED0(record, 0)`), and the notices
   below are posted unless flags bit 1 is set.

The notices, for a party record:

- message 4 carrying the record and the new level, through `0046A690` and `0046AB10`;
- when `0031B860` finds the record's unit on the field and that unit's stats are party-kind
  (`[unit+0x698]` byte `+0x05` = 0): the HUD popup `002905D0(unit id, from level, new level)`
  (`[0209BE80] + 0x7FB0`), a call to `002EACD0(unit id)`, and sound 7 (`003A1180` / `002DF220`, then
  `00329210(1)`).

### HP and MP growth

HP and MP growth read `hpmpbase_data`, the table in registry slot `02EBF108` (`battle_pack.bin`
directory `+0x28`, 99 rows of 2 bytes, row = level before the step):

```c
// 002F9A60: b = row.hp (byte 0)
bonus = (b / 5.0f >= 0.01f) ? (MT() % (int)(b / 5.0f * 100.0f)) / 100.0f : 0;
HP   += b + (int)bonus;                     // bonus is 0 .. b/5 - 0.01, truncated

// 002F9B20: b = row.mp (byte 1)
bonus = (b >= 0.01f) ? (MT() % (int)(b * 100.0f)) / 100.0f : 0;
MP   += b + (int)bonus;                     // 0 .. b - 1 extra
```

`MT()` is `00863BF0`, the Mersenne Twister whose state starts at `02EB3870` (index `02EB4230`). On its
first use it seeds itself with 5489 (`0x1571`, `00866D60`).

### Strength, Magick Power, Vitality and Speed

The four stats grow by `002F9BD0`: `value + byte / 128`, and a result above 100.0 becomes
99.99999 (`002F9BD7`-`002F9BEC`). There is no random part.

### Starting values

`0030C470(record, level, ...)` sets the level byte to 0 (`0030C496`). For a party
record it then copies the row's starting values:
- max HP from `row.u16[+0x16]` and max MP from `row.u16[+0x1A]` (`0030C4F9`-`0030C507`);
- the four stats from the base bytes `+0x1E`, `+0x21`, `+0x24`, `+0x27` (`0030C50B`-`0030C546`);
- byte `+0x20` from `row.b[+0x46]`, or from `00324100(record)`, the largest licence-granted value, when
  that is larger.

Then it calls `0030C650(record, level, 2)` (`0030C562`-`0030C56E`), so a new character grows silently
from level 0 to its starting level, and sets the EXP total `+0x18C` to `002F8F20(level - 1)`, the EXP
needed for that level, capped at 99,999,999 (`0030C573`-`0030C586`). The summon start calls it as
`0030C470(Esper record, summoner's level, 0)` (`003069EE` in `00306760`), so an Esper is rebuilt from
level 0 to the summoner's level every time it is summoned. A character's starting gil (`row.u16[+0x3E]`) is added once, on its
first activation (see the gil page).

**Who calls the level walk:**

| Caller | Call | Target level | Flags |
|---|---|---|---|
| `0030C470` | `0030C56E` | the starting level | 2 (silent) |
| `00312280` | `003124A3` | the level the EXP total reaches (see the EXP page) | 0 |
| `003112F0` | `003113DF` | result byte `+0x11C` (the target's new level, `0xFF` = none) | 0 |
| `003112F0` | `003113FD` | result byte `+0x11D` (the source's new level) | 0 |
| `00305960` | `003059CB` | 99, for every record of party map 3 | 0 |

## Layouts

`ChrDataRow` (`0x80` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `16` | `u16` | startMaxHp | max HP at level 0 |
| `18` | `...` | gap18 | not read by the growth code |
| `1A` | `u16` | startMaxMp | max MP at level 0 |
| `1C` | `...` | gap1C | not read by the growth code |
| `1E` | `u8` | strBase | Strength at level 0 |
| `1F` | `u8` | strGrowth | Strength gained per level, in 1/128 |
| `20` | `u8` | pad20 | 0 in every shipped row |
| `21` | `u8` | magBase | Magick Power at level 0 |
| `22` | `u8` | magGrowth | Magick Power gained per level, in 1/128 |
| `23` | `u8` | pad23 | 0 in every shipped row |
| `24` | `u8` | vitBase | Vitality at level 0 |
| `25` | `u8` | vitGrowth | Vitality gained per level, in 1/128 |
| `26` | `u8` | pad26 | 0 in every shipped row |
| `27` | `u8` | spdBase | Speed at level 0 |
| `28` | `u8` | spdGrowth | Speed gained per level, in 1/128 |
| `29` | `...` | tail29 | not read by the growth code |

## Shipped data

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

```text
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

## Modding notes

- HP and MP growth are shared by every character: edit `hpmpbase_data` (directory `+0x28`). A
  character's own HP and MP differ only by its starting values `+0x16` / `+0x1A`.
- Per-character growth of the four stats is `chr_data` bytes `+0x1F`, `+0x22`, `+0x25`, `+0x28`, in
  1/128 per level; with the base bytes, a stat at level `L` is `base + L × growth / 128`.
- The level cap 99 is code (`0030C650`, and `002F8F20` on the EXP page), not data.

## Related

- [EXP, LP and level-ups from kills: who receives them, the formulas, the split, the doublers and the EXP table](exp-lp-and-level-ups.md)
- [Gil: storage, the gil cap, every way gil changes, and the Plunderer and Spendthrift counters](gil.md)
