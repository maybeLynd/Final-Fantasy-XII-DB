# UQ-107 — every flag bit of the action row, read

FABLE, Claude Opus 5.5, 2026-09-27. **NATIVE/STATIC plus authored data. Nothing was executed.**
Control: `uq107_flag_bits.py` (3 checks, FAILS 0). It runs `action_row_follower.py`, the GA-1 row follower pointed
at the action table. Detail: [`findings.md`](findings.md) (per bit, with shipped row counts) and
[`plus-0x2C-bit5.md`](plus-0x2C-bit5.md). Correction record: [`consumer-check.md`](consumer-check.md).

UQ-107 asked about three things. `+0x13` beyond bit 0 closed on 2026-09-17: it is the element mask. The other two
close here.

**`+0x0C` bits 12–31.**
- **The census.** The follower finds **60** provenance-verified reads of the action row's `+0x0C` (F1). The
  2026-09-18 table held 23; all 23 are among the 60. The bits each read tests are classified from the bytes (F2).
- **Readers.** Bits 12, 13, 14, 16, 17, 19, 21, 24, 25, 26, 27, 28, 29, 30 and 31 have readers. Bits 15, 18, 20, 22
  and 23 have none.
- **Row counts** come from the 543 shipped rows (us `battle_pack.bin`). They match the page's own `+0x0C` profile.

| bit | rows | what it does (reader) |
|---|---:|---|
| 12 | 18 | the Quickenings: the shape descriptor `0031A990` reports no area (shape 0, or 5 = whole party with bit 1) |
| 13 | 162 | **magick class**: a target under layer id 56 (Magick Shield) voids the result as kind 7 (`00390EE5`, `003910C3`); sets bit 8 of the flag word `00312170` builds; zero charge time under layer id 54 (`002F8689`) |
| 14 | 207 | **physical class**: a target under layer id 55 (Paling) voids the result as kind 7 (`00390E9A`, `00391076`); sets bit 9 of that flag word |
| 15 | 24 | no reader: authored, never read |
| 16 | 78 | **bounced by Reflect** (status 23), unless the source has augment 31; result kind 8 onto the nearest unit in reach (`00390DF1`) |
| 17 | 28 | runs the special-guard roll against the target's `+0x34` (`00388058`) |
| 18 | 1 | no reader (Attack) |
| 19 | 97 | adds Silence (status 9) to the statuses that disable the action (`002FFE56`; mask `0x8000221B` for `0x8000201B`) |
| 20 | 81 | no reader: authored, never read |
| 21 | 26 | area circle centred on the actor instead of the target (`0030D271`, `0031A99A`) |
| 22, 23 | 0 | unused: no reader, no row |
| 24 | 49 | cone, half-angle `+0x07` degrees (`0030D2C0`, `0030D3AE`, `0031A99A`) |
| 25 | 5 | line, half-width `+0x07`; never with bit 24 |
| 26 | 35 | the weapon's figures replace the action's: reach, range band, and an admission flag (`00309377`, `00320D74`, `00320F39`, `00390C7F`) |
| 27 | 1 | charge value from the weapon's equipment row `+0x27` (`002F8494`) |
| 28 | 36 | the cure and raise magicks and the curative items: two changes to the battle menu's command entry (`0031F0EF`, `0031F157`). No page names those entry bits; medium confidence. |
| 29 | 112 | the action has a resource cost (MP, or gil on the gil channel), carried by its menu entry (`0031F000`) |
| 30 | 87 | runs the global special sequence: summon, Quickening, concurrence, mount (17 sites) |
| 31 | 64 | item-consuming: the menu entry carries the item's quantity query (`0031F077`) |

**`+0x2C` bit 5 (`0x20`, 166 rows): read by nothing.** The six sites the 2026-09-17 narrowing credited to "register
masks built by the status-mask family" test immediates loaded just before them: `0x2000`, `0x200` (three sites),
`0x400`, `0x800`, and `0x8000` through an unsigned `cmp`. The bare value reads mask `& 7`, test `0x40`, or shift by
12 or 15. No read of the 40 tests `0x20`.

**Not established:** the names of the command-entry bits bit 28 changes. The reader-less bits are stated as
reader-less over the verified sites and a two-hop sweep. A row copied into another record would escape both.
