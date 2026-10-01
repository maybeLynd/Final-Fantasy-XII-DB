# GR-6 answered: a bit-15-clear action-row `+0x24` word is an effect id (OPUS, 2026-09-30)

Register row GR-6 asks what the 436 action-row `+0x24` words with bit 15 clear select.

- The selector `0030AC50` returns `+0x24 & 0x7FFF` only for bit 15 set (39 rows).
- A `0xFFFF` word falls back to the weapon row (68 rows).
- `00325476` and `00325968` send every other word down a branch the page had not read.

The page is [the action definition row](../../../07-Combat-Action/Action-Definition-Row/the-action-definition-row.md),
§2.2 and §7.

Method: static reads of the certified image plus the shipped rows. The checker is `gr6_row24_check.py` (output
`gr6_row24_check.out`, **`FAILS 0`**). It uses the kit's `retool.py`, `regval.py` and `structflow.py`, and the UQ-80
record's `pack.py` (battle_pack directory `0x3C`, 543 × 60 B).

## The answer (OPUS)

**The low 15 bits of `+0x24` are an effect id, the action's own visual effect.** With bit 15 set, the word belongs to
the weapon / reaction selector path instead (`0030AC50`, `0031ADB0`).

**G1: who reads `+0x24`.** `structflow` ran from every `02EBF138` row-pointer formation, depth 3. It finds nine
functions and fourteen sites: `00309230`, `0030A190`, `0030AC50`, `0030CA80`, `00310DB0`, `0031ADB0` (×3),
`00325260` (×3) and `003257D0` (×3). All are reads.

**G2: what the four readers that accept a bit-15-clear word do with it.**

| reader | use |
|---|---|
| `BattleAction_GetPresentationParameter` `0030A190` | Returns the word when it is not `0xFFFF`, `+0x0C` bit 30 is clear and bit 15 is clear. The word then goes to the effect request `002FCBF0` (resource kind `0xB`) via `0030CBE0`, and to the effect budget `002FCAC0` via `0030C890`. See the [GR-4/GR-5 record](../gr4-gr5-action-row-readers-0930/README.md), S6–S7. |
| `0030CA80` | Makes the same three tests, then calls `002FCB40(word)`. That returns bit 5 of the 8-byte entry at `02EC19C4 + word × 8`, which is the effect table the budget reads. |
| `BattleUnit_RunPeriodicCombatMaintenance` `00310DB0` | Clears bit 15 (`btr`) and calls `002EACD0(…, 1, …, word)`, which calls `003B02A0` with kind 5. That is the effect instantiation, per target of a periodic action. |
| `00309230` | Returns the row's word to `00306BD0`, the special-sequence step. That step passes it to `WorldSimulation_ProcessDeferredModeRequest(3, word)`, the manager-3 load. |

**G3: where the other readers send a bit-15-clear word.** Nowhere.

- `0031ADB0` sends a bit-15-set word to the `+0x34` reaction path (`0031B254` `jl`) and skips the rest (`0031B2AC`).
- `00325260` and `003257D0` compare the word with `0xFFFF` (`di` = `0xFFFF`) and return on any other value. The
  branches the row calls "unread", `00325702` and `003259E3`, are just their exits (`mov eax, 1; … ret` and the
  epilogue).
- `0030AC50`'s `+0x24` path takes only bit 15 set. That is the row's premise; this record checks only its read site.

**G4: the data.** Of the 436 bit-15-clear rows:

- **374 have `+0x0C` bit 30 clear.** They hold 340 distinct values, 0–396. These are the effect ids that `0030A190` /
  `0030CA80` serve.
- **62 have bit 30 set** (rows 148–274, 29 distinct values). These are the summon-class rows `0030A190` refuses. For
  them the word is what the special-sequence step loads. The page's neighbour already names these as the
  `sum_<x>0001` set ids for rows 183–207.

**In player terms:** this number picks the visual effect an ordinary action plays when it lands. For a summon it names
the cinematic set the game loads.

## Limits

- `0030AC50` and `0031ADB0`'s bit-15-set arm are not re-read here; bit-15-set words are not GR-6's question.
- What each effect id draws is the effect files' matter ([the effect pages](../../../17-Presentation-Rendering/Effect-File-Formats/)),
  not this row's.
- `003B02A0`'s special id cases (`0x64`–`0x67`, `0x94`) are seen but not interpreted.

## Consumers (routed, not edited here)

- The action-row page: the `+0x24` cell and the §7 GR-6 box. That page is FABLE's.
- Register row **GR-6**, via a DATA restatement request.
