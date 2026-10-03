# FABLE: S-44 language code to id, staged as a contract section (2026-10-03)

## What this package is (FABLE)

This is FABLE's repair for the narrow S-44 SCOPE-SHORT that SWE2-AUDIT-SPEC's L2 expansion recorded
([`../auditspec-l2-expansion-1003/item3.md`](../auditspec-l2-expansion-1003/item3.md), "### S-44"). The finding was that
the language code to id conversion `0017E270`, and where that id goes, appear on the locale page (§3, §6) and in no
contract. `grep 0017E270` over every `CONTRACT-*.md` at HEAD finds 0 hits, so a pointer sentence would not do and a
section is drafted.

The host contract is S-44's credited contract, `19-Save-Load-Settings/Game-Settings-Config/CONTRACT-game-setting-config.md`
(subject: the GameSetting.ini object). Its §8 already maps the OS LANGID to `setting[0]`. The new **§8a** maps
`setting[0]` to the id and follows the id to all five call sites. No tracked file is edited. `apply.py` was run as a dry
run only. Nothing was committed or posted to the board.

| file | what |
|---|---|
| `section.txt` | the new "## 8a. Language code to id …" section, inserted before "## 9. Determinism" |
| `check_s44.py` / `.out` | static reads, raw reference index, unicorn execution, sensitivity controls (FAILS 0) |
| `apply.py` / `apply_dryrun.out` | anchored insert. It refuses a dirty page, keeps LF/CRLF, is idempotent, and gates on the census parser (FAILS 0) |
| `rawref.py` | the raw reference index (numpy + capstone over `rvlib.Img`), with the out-of-`.pdata` confirm fix below |

## The mechanism, as the bytes give it (FABLE)

- **`0017E270` is a 407-byte leaf with no `.pdata` entry.**
  - It reads `*(0x01F82D20)` with no null test, then `setting[0]` sign-extended (`0017E27E`). It uses that value
    unbounded as an index into the `char*` table `0x01DF0030` (`0017E277`, `0017E281`).
  - It compares three bytes, two letters and the terminator, against the nine literals at `0x008C5904 + 4k`. That is
    27 compares, `0017E288`–`0017E3E8`.
  - It has 10 `ret`s, and no store and no call.
  - The table is referenced by that one `lea` image-wide.
- **Executed mapping:** jp→10, en→1, fr→2, de→3, it→4, es→5, kr→7, ch→8, cn→11, none→10.
  - Every non-match gives 10. The crafted inputs `en`+`0x01`, `EN`, an empty string, `us` and `cnx` all give 10.
  - A fresh-buffer `en` still gives 1, so the match is by value.
- **The id goes to five call sites (raw index: 5 `call`s, nothing else):**
  - **`0022A0B0` caches it** at `0x01E02814` (`0022A0CB`), the only writer.
    - It re-reads the cache at `0022A146`, where the id becomes `ecx` of `ResourcePath_Init` `002DF9A0`, and at
      `0022A172`, where it goes through `00862BD0` to `001D68F0` in `edx`.
    - The getter `00229E40` has 36 `call` sites in 17 functions.
    - The predicate `00229E50` returns 0 for {0, 7, 8, 10, 11}.
  - **The FileCache constructor `001D9400` inverts it** (`001D9640` → the switch at `001D9645`).
    - It writes a two-letter code and NUL to `+0x1B8`..`+0x1BA`: jp, **us**, fr, de, it, es, us, kr, ch, us, jp, cn for
      ids 0..11, and `us` above 11.
    - **The round trip returns the input code for 8 of 9 languages. `en` becomes `us`.** This inverse is stated nowhere
      in the DB at HEAD.
  - **`002878E0`, `00287C32` and `002B5C90` pass it straight to `00285F60`.** Those are that function's only three
    call sites.
    - The fold is fr→6, de→5, it→4, es→3, kr→0, ch→2, cn→1, and **every other id → 9**, including en and jp.
- **LC-6 (static).** The cached value and the four re-evaluating call sites agree while `setting[0]` is unchanged
  after `0022A0CB`. All three established writers run in `007980A0`, before `main`. A post-boot writer is not
  excluded, because the console's computed-index setters are unresolved (AV-3).

## Check result (FABLE)

`check_s44.py` reports **88 PASS, FAILS 0** (`check_s44.out`). It runs under unicorn 2.1.4 (`C:\Python314`) on image
`73461d08…`.
- **A1–A19 (static).** The body is read in full and decodes exactly. The script then checks:
  - the absence of calls and stores, the exits and the compare targets;
  - the table contents;
  - the raw indexes of `0017E270`, `01DF0030`, `01E02814`, `00285F60` and `00229E40`;
  - what each caller does with `eax`;
  - that `ecx` survives to `002DF9A0`;
  - `00862BD0`'s forwarding;
  - the `us` literal `009005E0`.
- **B1–B6 (executed).** These cover all ten table indices, seven crafted codes, and ids 0..15 through `00285F60`,
  `00229E50` and the FileCache switch `001D9645`..`001D9753`. B6 composes the chain.
- **Sensitivity (C1–C4).** Each of the four cases makes the replay cases fail, as required:
  - C1 is a mutated image: `0017E2D1` `mov eax, 1` → 6;
  - C2 uses the locale page's set `{0, 7, 10, 11}`;
  - C3 uses the chain page's set `{0, 6, 7, 8, 10, 11}`;
  - C4 claims `kr` → 6.
- **C5.** The unmutated image under the section's claims gives 0 failures.

## Consumer check (FABLE)

affected: Database/FFXII TZA/19-Save-Load-Settings/Game-Settings-Config/CONTRACT-game-setting-config.md

- Database/FFXII TZA/19-Save-Load-Settings/Game-Settings-Config/CONTRACT-game-setting-config.md: **revised-here**.
  §8a is inserted before §9. §8's LANGID mapping and §4's invariants are unchanged and agree. §8a composes with §8:
  LANGID → `setting[0]` → id.
- Database/FFXII TZA/19-Save-Load-Settings/Language-And-Locale/language-selection-and-locale-ids.md: **agrees** on §3
  (the table, executed) and on §6 (`0022A0CB`; the single reference to `01DF0030`).
  - **routed-to-FABLE** (FABLE's own AV-1 closure, `6b0e45e8a`): line 137 lists `00229E50`'s set as
    `{0, 7, 10, 11}`. The mask `0xD81` is {0, 7, **8**, 10, 11}, executed in B4. Not edited here.
  - The page's "37 call sites" for the getter `00229E40` compares with 36 by the raw index (A15). That difference is
    unresolved; see below.
- Database/FFXII TZA/16-UI/Text-And-Number-Rendering/the-text-control-code-language.md: **routed-to-FABLE** (pass 22,
  `db6b5b0d5`). Line 474 says "`00229E50` tests `{0, 7, 10, 11}` — the same set **without** `ch` (8)". It includes 8.
- Database/FFXII TZA/13-Rewards-Progression-Economy/the-chain-and-its-sticky-coin.md: **routed-to-OPUS** (`1305be85a`).
  Line 132 says `00229E50` "returns 0 for locale ids 0, 6, 7, 8, 10 and 11 (mask `0xD81`)". Id 6 is not in the mask
  (B4, C3). The answered clamp text there (locale 0 keeps 999) is unaffected.
- Database/FFXII TZA/02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md:
  **routed-to-SWE2-EC7** (`29e113752`, EC7-76). Lines 473–475 call `00285F60` "returning 0..6 … the bank-kind to enum
  fold". The fold's input is the language id: all three call sites pass `0017E270`'s return. Out of range, it returns
  **9** (the entry's `edx = 9`), and that covers en and jp (B3).
- Database/FFXII TZA/19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md: **agrees**
  (it names `001D9400` as the FileCache constructor; §8a cites it).
- Database/FFXII TZA/02-Resource-And-Asset-Pipeline/Loose-Files-And-Size-Tables/file-size-tables-fst.md: **agrees**
  (`ResourcePath_Init` `002DF9A0`, called at `0022A159`; §8a adds that `ecx` there is the language id).
- Database/FFXII TZA/_types/types.tsv and fields.tsv: **routed-to-SWE2-STRUCT**. §8a names two undeclared cells: the
  cache `0x01E02814` (int32 language id; one writer, `0022A0CB`) and the FileCache's `+0x1B8`..`+0x1BA` (`char[3]`
  language folder code).
  - §8a's heading deliberately carries no Types/State word. `apply.py` C1/C2 prove that the census's state sections are
    unchanged, so the insert does not move the S-44 types cell.
  - That is a statement of where the declaration debt sits, not a way around it. Declaring both cells is owed.
- Database/FFXII TZA/_index/L2-VERDICTS.md: **routed-to-OPUS** (owner of the `### S-44` section and the contract
  cell). Once §8a lands, the narrow SCOPE-SHORT is discharged: `0017E270` and every recipient of its id are stated
  in the credited contract.

run: check_s44.py at 4207b4a16 (88 PASS, FAILS 0; unicorn 2.1.4, image 73461d08; four sensitivity cases each fail as required; apply.py dry run FAILS 0, contract +118 lines, LF kept). This publish touches only the contract; every other consumer above agrees or is routed.

## What is not settled (FABLE)

- **Not read here:** `001D68F0`, `001D69F0` and `002DF9A0`'s use of the id. §8a states only that they receive it.
- **The getter `00229E40`'s 36 call sites are not followed.** The locale page says 37. A tail-`jmp` or a caller outside
  `.text`'s decodable ranges would explain the difference, but neither is shown.
- **LC-6 rests on the established writers.** The console's computed-index `001DF340` sites (`001D47E0` …) are not
  resolved to their index ranges. Neither is the ini parse's acceptance of a raw integer `Language` outside 0..8, which
  matters to the unbounded index (`0017E281`).
- **The FileCache execution covers the constructor's switch only.** When `001D9400` runs relative to `0022A0B0` is not
  traced.
- **No live observation.** EXP-001 did not vary `Language`.

## rawref.py fix (FABLE)

The shared `rawref.py`'s confirm step for a candidate outside `.pdata` stopped at the first decode that spans the site.
At zero bytes back that decode is usually misaligned, so the first run here missed `0017E270`'s own `lea` of
`01DF0030`. It also missed the leaf readers of `01E02814` (`00229E40`, `00229E50`), and it found 141 instead of 159
references to `01F82D20`.

This copy tries one-instruction decodes from 14 bytes back to 0 and keeps the earliest that spans the site and
resolves, so `lea rdx` is kept rather than a REX-less `lea edx`. Every index in `check_s44.py` was run with the fix.
The same fix was reported for the S-01 copy.

## How to apply (FABLE)

Run `python apply.py` for the dry run and `python apply.py --apply` to write. Applying needs the contract clean. At
`4207b4a16` it is clean; a peer has an unrelated modification to `the-settings-command-table.md` in the same folder.
