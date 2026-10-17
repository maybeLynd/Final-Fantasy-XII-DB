---
title: "Languages: the Language setting, the nine language codes, the locale id each maps to, the data folder it selects, the Windows-locale default, and the confirm and cancel buttons"
kind: "system"
category: "Saving, loading and settings"
addresses: "0017E270, 001DE050, 0022A0B0, 00229E40, 00229E50, 00254A10, 002DF9A0, 0017E210"
---

## What the player sees

The Config screen offers nine languages: Japanese, English, French, German, Italian, Spanish,
Korean, Traditional Chinese and Simplified Chinese. On a fresh install the game picks the one
matching Windows' display language, English when none matches.

The choice decides which data folder the text, voices and fonts load from, and a few rules change
with it: the kill chain counter is capped at 998 and shown one higher, one text parameter differs
for Korean and the two Chinese languages, and a handful of scripts ask which language is running.
A separate option, DecideButton, swaps which of two buttons confirms and which cancels.

## How it works

### The setting

Every option lives in the GameSetting.ini object whose address is held at `01F82D20`, stored once
by `00798261` after the constructor `001DE050` runs (`00798257`). Field `+00`<sub>h</sub> is the Language
setting: an index into the code table at `01DF0030`, ten pointers to the strings packed at
`008C5904` on a 4-byte pitch:

| Index | Code | Index | Code |
|---|---|---|---|
| 0 | `jp` | 5 | `es` |
| 1 | `en` | 6 | `kr` |
| 2 | `fr` | 7 | `ch` |
| 3 | `de` | 8 | `cn` |
| 4 | `it` | 9 | `none` |

The Config screen's value names for the setting (row 0 of the table at `01DFD150`) point at the
same strings. `0017E210` reads the sibling field `+64`<sub>h</sub>, the DecideButton setting.

### The default on a fresh install

The constructor `001DE050` copies the 31 defaults from the table at `00900CE0` (16 bytes per
setting; Language's default is 1, `en`) and then overwrites the Language index from
`GetUserDefaultLangID()`:

| Windows LANGID | Index |
|---|---|
| `0404`<sub>h</sub>, `0C04`<sub>h</sub>, `1404`<sub>h</sub> (Traditional Chinese; `1C04`<sub>h</sub> is excluded) | 7 `ch` |
| primary language `0C`<sub>h</sub> (French) | 2 `fr` |
| primary `07`<sub>h</sub> (German) | 3 `de` |
| primary `10`<sub>h</sub> (Italian) | 4 `it` |
| primary `0A`<sub>h</sub> (Spanish) | 5 `es` |
| primary `11`<sub>h</sub> (Japanese) | 0 `jp` |
| primary `12`<sub>h</sub> (Korean) | 6 `kr` |
| primary `04`<sub>h</sub> (other Chinese) | 8 `cn` |
| anything else | 1 `en` |

The Traditional test runs first on the whole LANGID (`(id - 404h) & FFFFE7FFh == 0` and
`id != 1C04h`); the primary language is `id & 3Fh`.

### From code to locale id

`0017E270` reads the code the index points at, compares its two letters and terminator, and returns
the locale id the rest of the game uses:

| Code | Locale id |
|---|---|
| `jp` | 10 |
| `en` | 1 |
| `fr` | 2 |
| `de` | 3 |
| `it` | 4 |
| `es` | 5 |
| `kr` | 7 |
| `ch` | 8 |
| `cn` | 11 |
| anything else, `none` included | 10 |

Ids 0, 6 and 9 are never produced. The two last arms are branchless arithmetic
(`0017E3F0`-`0017E406`): the `cn` arm yields 11 and the default arm 10.

### Where the locale id lives

The first boot frame mode `0022A0B0` calls `0017E270` and stores the result at `01E02814`
(`0022A0C6`-`0022A0CB`); that store is the only write to the word in the image. `00229E40` returns
it (36 call sites in 16 functions), and `00229E50` returns 0 for the ids 0, 7, 8, 10 and 11 (mask
`D81`<sub>h</sub>) and 1 otherwise; `00254A10` is the same test with the result inverted (1 for those ids).
The same boot mode stores the constant 10 from `0017E410` at `01E0281C`.

### The data folder and the file size table

Boot mode 0 then calls `002DF9A0(localeId, [01E0280C])` (`0022A159`). It selects the per-locale
file table pointers by locale id (arms for 1 to 8 and 11, with 10 and every other id on the
default arm) and reads the locale's file size table into `02EC3EE0` (820,000 bytes): the path is
`sprintf("%sFileSizeTables/FileSizeTable_%s.fst", "../", folder[localeId])` with the folder code
table at `01E88B00`:

| Locale id | Folder | Locale id | Folder |
|---|---|---|---|
| 0 | `JP` | 6 | `UK` |
| 1 | `US` | 7 | `KR` |
| 2 | `FR` | 8 | `CH` |
| 3 | `DE` | 9 | `ASIA` |
| 4 | `IT` | 10 | `IN` |
| 5 | `ES` | 11 | `CN` |

So Japanese (id 10) loads the `IN` tables; the `JP`, `UK` and `ASIA` entries have no id that reaches
them. A missing or short file is reported through `00863100` (`002E045D`, `002E0486`) and the code then
writes a zero dword to address 0 (`002E0462`, `002E048B`).

### Rules that depend on the language

- The kill chain cap and display: `00317ED0` caps the length at 998 and posts it plus one whenever
  the id is non-zero, which it always is (see the kill chain page).
- `002AB7D0`: for ids 7, 8 and 11 (`(id - 7) & FFFFFFFAh == 0` and `id != 12`, so Korean and the
  two Chinese languages, not Japanese) it sets `01E0CDF8` to 28 and `0209CC38` to 1; otherwise
  `01E0CDF8` = 24.
- `002ABAA0(flag)` reads the id but has no language dependence in the shipped game: every id
  returns `0024ABA0()` scaled by 15.0 (`00916314`) with the flag set or 10.0 (`008F8180`) with it
  clear; its 26.0 arm (`00916484`) needs id 7 after `00254A10` returned 0, which that id never
  does.
- Script verbs: `5C6`<sub>h</sub> (`0033FED0`) returns the id with 10 read as 0; `59C`<sub>h</sub> (`0034BA00`) returns
  the id with 7, 8, 10 and 11 read as 0; `5AA`<sub>h</sub> (`0034C010`) returns `00229E50()`.
- `0029CE40` passes the id to `0017F9E0` at area setup; `002DDE60` and `003B1BA0` read it seven and
  eight times for text layout; `002AC5F0`, the text control-code interpreter, reads it at
  `002ACBD3`, `002ACCFC` and `002ACE2E`.

### Confirm and cancel

In the same boot mode, `0017E210` returns DecideButton (`+64`<sub>h</sub>). The confirm mask `01E0C2A0` and
the cancel mask `01E0C2A4` are set from it (`0022A0E1`-`0022A119`), and `01FD4A64` records whether
it was non-zero:

| DecideButton | Confirm `01E0C2A0` | Cancel `01E0C2A4` |
|---|---|---|
| 0 | `2000`<sub>h</sub> | `4000`<sub>h</sub> |
| non-zero | `4000`<sub>h</sub> | `2000`<sub>h</sub> |

The battle menu `002778C0` treats the two differently: the confirm branch tests its handler's
result and plays sound 2 only on failure (`00277EB8`-`00277ECE`), the cancel branch discards the
result and always plays sound 3 (`00277E36`-`00277E53`).

## Operations

| Function | Role |
|---|---|
| `001DE050` | GameSetting.ini object constructor: defaults, then the Language index from the Windows LANGID |
| `0017E270` | language code to locale id |
| `0022A0B0` | boot frame mode 0: stores the locale id, the confirm and cancel masks, loads the file size table |
| `00229E40` | returns the locale id |
| `00229E50`, `00254A10` | the Asian-language test, both polarities |
| `002DF9A0` | selects the per-locale tables and loads `FileSizeTable_<folder>.fst` |
| `0017E210` | returns DecideButton |

## State

| Address | Width | Meaning | Written by |
|---|---|---|---|
| `[01F82D20] + 00h` | `i32` | Language index 0-9 | `001DE050`, the Config screen |
| `[01F82D20] + 64h` | `i32` | DecideButton | the Config screen |
| `01E02814` | `i32` | locale id | `0022A0B0` (`0022A0CB`) |
| `01E0281C` | `i32` | the constant 10 from `0017E410` | `0022A0B0` (`0022A0D6`) |
| `01E0C2A0` / `01E0C2A4` | `u16` | confirm and cancel button masks | `0022A0B0` (`0022A119`, `0022A10C`) |
| `01FD4A64` | `i32` | DecideButton was non-zero | `0022A0B0` (`0022A0FD`) |
| `02EC3EE0` | 820,000 bytes | the locale's file size table | `002DF9A0` |

## Modding notes

- A new language needs a code in the table at `01DF0030`, an arm in `0017E270`, a folder code in
  `01E88B00` and the file tables `002DF9A0` selects; the ids 0, 6 and 9 and the folders `JP`, `UK`
  and `ASIA` are free.
- Everything downstream reads the id from `01E02814` through `00229E40`; writing that word after
  boot changes the language-dependent rules without reloading the data folder.
- DecideButton is a plain setting read at boot (`0022A0B0`) and again whenever the Config screen's Confirm
  Button row or the Controls screen's Default changes it: `0017E6E0` and `0023E020` both rebuild the masks
  through `0022A4F0`.

## Related

- [Kill chain: chain count, chain level, the chain coin and resets](../Rewards-EXP-Gil-And-Loot/kill-chain.md)
