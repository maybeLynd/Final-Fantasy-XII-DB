---
title: "Languages: the Language setting, the nine language codes, the locale id each maps to, the data folder it selects, the Windows-locale default, and the confirm and cancel buttons"
kind: "system"
category: "Saving, loading and settings"
addresses: "0x0017E270, 0x001DE050, 0x0022A0B0, 0x00229E40, 0x00229E50, 0x00254A10, 0x002DF9A0, 0x0017E210"
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

Every option lives in the GameSetting.ini object whose address is held at `0x01F82D20`, stored once
by `0x00798261` after the constructor `0x001DE050` runs (`0x00798257`). Field `+0x00` is the Language
setting: an index into the code table at `0x01DF0030`, ten pointers to the strings packed at
`0x008C5904` on a 4-byte pitch:

| Index | Code | Index | Code |
|---|---|---|---|
| 0 | `jp` | 5 | `es` |
| 1 | `en` | 6 | `kr` |
| 2 | `fr` | 7 | `ch` |
| 3 | `de` | 8 | `cn` |
| 4 | `it` | 9 | `none` |

The Config screen's value names for the setting (row 0 of the table at `0x01DFD150`) point at the
same strings. `0x0017E210` reads the sibling field `+0x64`, the DecideButton setting.

### The default on a fresh install

The constructor `0x001DE050` copies the 31 defaults from the table at `0x00900CE0` (16 bytes per
setting; Language's default is 1, `en`) and then overwrites the Language index from
`GetUserDefaultLangID()`:

| Windows LANGID | Index |
|---|---|
| `0x0404`, `0x0C04`, `0x1404` (Traditional Chinese; `0x1C04` is excluded) | 7 `ch` |
| primary language `0x0C` (French) | 2 `fr` |
| primary `0x07` (German) | 3 `de` |
| primary `0x10` (Italian) | 4 `it` |
| primary `0x0A` (Spanish) | 5 `es` |
| primary `0x11` (Japanese) | 0 `jp` |
| primary `0x12` (Korean) | 6 `kr` |
| primary `0x04` (other Chinese) | 8 `cn` |
| anything else | 1 `en` |

The Traditional test runs first on the whole LANGID (`(id - 0x404) & 0xFFFFE7FF == 0` and
`id != 0x1C04`); the primary language is `id & 0x3F`.

### From code to locale id

`0x0017E270` reads the code the index points at, compares its two letters and terminator, and returns
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
(`0x0017E3F0`-`0x0017E406`): the `cn` arm yields 11 and the default arm 10.

### Where the locale id lives

The first boot frame mode `0x0022A0B0` calls `0x0017E270` and stores the result at `0x01E02814`
(`0x0022A0C6`-`0x0022A0CB`); that store is the only write to the word in the image. `0x00229E40` returns
it (36 call sites in 16 functions), and `0x00229E50` returns 0 for the ids 0, 7, 8, 10 and 11 (mask
`0xD81`) and 1 otherwise; `0x00254A10` is the same test with the result inverted (1 for those ids).
The same boot mode stores the constant 10 from `0x0017E410` at `0x01E0281C`.

### The data folder and the file size table

Boot mode 0 then calls `0x002DF9A0(localeId, [0x01E0280C])` (`0x0022A159`). It selects the per-locale
file table pointers by locale id (arms for 1 to 8 and 11, with 10 and every other id on the
default arm) and reads the locale's file size table into `0x02EC3EE0` (820,000 bytes): the path is
`sprintf("%sFileSizeTables/FileSizeTable_%s.fst", "../", folder[localeId])` with the folder code
table at `0x01E88B00`:

| Locale id | Folder | Locale id | Folder |
|---|---|---|---|
| 0 | `JP` | 6 | `UK` |
| 1 | `US` | 7 | `KR` |
| 2 | `FR` | 8 | `CH` |
| 3 | `DE` | 9 | `ASIA` |
| 4 | `IT` | 10 | `IN` |
| 5 | `ES` | 11 | `CN` |

So Japanese (id 10) loads the `IN` tables; the `JP`, `UK` and `ASIA` entries have no id that reaches
them. A missing or short file is reported through `0x00863100` (`0x002E045D`, `0x002E0486`) and the code then
writes a zero dword to address 0 (`0x002E0462`, `0x002E048B`).

What a language changes besides the text is in its file size table. [languages-kinds.tsv](languages-kinds.tsv) compares,
for every resource kind, each entry's size in the nine tables a locale reaches. Only eight kinds have entries whose
size differs between languages:

- the zone files (kind 5, 585 of 896: the scripts with their companion files) and the event files (kind 8, 202 of
  1,080, and kind 37, 195 of 1,080);
- the event effects (kind 12, 186 of 534);
- 27 of the 81 battle-test files (kind 2), 23 of the 545 menu files (kind 7), one sound-environment file (kind 1) and
  one map table (kind 9).

Every model, motion, map pack, magic effect, sound bank and movie entry has one size in all nine. A different size
proves different content; the table gives the groups of languages that share a size.

The shipped files give the same comparison by content.
[languages-content-files.tsv](languages-content-files.tsv) takes every file under a language folder, in the 12
folders of the archive that have language folders, by its path inside the language folder. For each path it gives
the languages that ship it and the groups of languages whose files have the same SHA-256.
[languages-content.tsv](languages-content.tsv) counts the paths per folder and file type.

Three of the 12 folders have one language folder only, `in`: `gamedata/titleimage`, `ps2data/cdi` and
`ps2data/obj_finish` (4,233 paths). Of the 5,578 paths in the other nine:

- 1,605 have one content in every language folder of their folder, among them all 488 `plan_master` motions, all
  256 `plan_master` sound files and 199 of the 201 `.vpc` files;
- 2,341 are in every language folder with more than one content: 1,033 `prefetchdata` lists, 871 `plan_master`
  scripts, 198 `myoshiok` `.dat` and 38 `.bin` files, the 132 `sound/shout` banks (`us` and `jp`) and 29
  `test_battle` files;
- 1,632 are in some language folders only, 754 of them in one.

Five of the folders have a `jp` folder: the font folder, `prefetchdata`, `effect_finish`, `movie_finish` and
`sound/shout`.

### Rules that depend on the language

- The kill chain cap and display: `0x00317ED0` caps the length at 998 and posts it plus one whenever
  the id is non-zero, which it always is (see the kill chain page).
- `0x002AB7D0`: for ids 7, 8 and 11 (`(id - 7) & 0xFFFFFFFA == 0` and `id != 12`, so Korean and the
  two Chinese languages, not Japanese) it sets `0x01E0CDF8` to 28 and `0x0209CC38` to 1; otherwise
  `0x01E0CDF8` = 24.
- `0x002ABAA0(flag)` reads the id but has no language dependence in the shipped game: every id
  returns `0x0024ABA0()` scaled by 15.0 (`0x00916314`) with the flag set or 10.0 (`0x008F8180`) with it
  clear; its 26.0 arm (`0x00916484`) needs id 7 after `0x00254A10` returned 0, which that id never
  does.
- Script verbs: `0x5C6` (`0x0033FED0`) returns the id with 10 read as 0; `0x59C` (`0x0034BA00`) returns
  the id with 7, 8, 10 and 11 read as 0; `0x5AA` (`0x0034C010`) returns `0x00229E50()`.
- `0x0029CE40` passes the id to `0x0017F9E0` at area setup; `0x002DDE60` and `0x003B1BA0` read it seven and
  eight times for text layout; `0x002AC5F0`, the text control-code interpreter, reads it at
  `0x002ACBD3`, `0x002ACCFC` and `0x002ACE2E`.

### Confirm and cancel

In the same boot mode, `0x0017E210` returns DecideButton (`+0x64`). The confirm mask `0x01E0C2A0` and
the cancel mask `0x01E0C2A4` are set from it (`0x0022A0E1`-`0x0022A119`), and `0x01FD4A64` records whether
it was non-zero:

| DecideButton | Confirm `0x01E0C2A0` | Cancel `0x01E0C2A4` |
|---|---|---|
| 0 | `0x2000` | `0x4000` |
| non-zero | `0x4000` | `0x2000` |

The battle menu `0x002778C0` treats the two differently: the confirm branch tests its handler's
result and plays sound 2 only on failure (`0x00277EB8`-`0x00277ECE`), the cancel branch discards the
result and always plays sound 3 (`0x00277E36`-`0x00277E53`).

## Operations

| Function | Role |
|---|---|
| `0x001DE050` | GameSetting.ini object constructor: defaults, then the Language index from the Windows LANGID |
| `0x0017E270` | language code to locale id |
| `0x0022A0B0` | boot frame mode 0: stores the locale id, the confirm and cancel masks, loads the file size table |
| `0x00229E40` | returns the locale id |
| `0x00229E50`, `0x00254A10` | the Asian-language test, both polarities |
| `0x002DF9A0` | selects the per-locale tables and loads `FileSizeTable_<folder>.fst` |
| `0x0017E210` | returns DecideButton |

## State

| Address | Width | Meaning | Written by |
|---|---|---|---|
| `[0x01F82D20] + 0x00` | `i32` | Language index 0-9 | `0x001DE050`, the Config screen |
| `[0x01F82D20] + 0x64` | `i32` | DecideButton | the Config screen |
| `0x01E02814` | `i32` | locale id | `0x0022A0B0` (`0x0022A0CB`) |
| `0x01E0281C` | `i32` | the constant 10 from `0x0017E410` | `0x0022A0B0` (`0x0022A0D6`) |
| `0x01E0C2A0` / `0x01E0C2A4` | `u16` | confirm and cancel button masks | `0x0022A0B0` (`0x0022A119`, `0x0022A10C`) |
| `0x01FD4A64` | `i32` | DecideButton was non-zero | `0x0022A0B0` (`0x0022A0FD`) |
| `0x02EC3EE0` | 820,000 bytes | the locale's file size table | `0x002DF9A0` |

## Modding notes

- A new language needs a code in the table at `0x01DF0030`, an arm in `0x0017E270`, a folder code in
  `0x01E88B00` and the file tables `0x002DF9A0` selects; the ids 0, 6 and 9 and the folders `JP`, `UK`
  and `ASIA` are free.
- Everything downstream reads the id from `0x01E02814` through `0x00229E40`; writing that word after
  boot changes the language-dependent rules without reloading the data folder.
- DecideButton is a plain setting read at boot (`0x0022A0B0`) and again whenever the Config screen's Confirm
  Button row or the Controls screen's Default changes it: `0x0017E6E0` and `0x0023E020` both rebuild the masks
  through `0x0022A4F0`.

## Related

- [Kill chain: chain count, chain level, the chain coin and resets](../Rewards-EXP-Gil-And-Loot/kill-chain.md)
