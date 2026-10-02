---
system: The VBF archive and the st2e authored table format
category: 02-Resource-And-Asset-Pipeline
status: DOCUMENTED - was REOPENED; the reopening trigger (pass 7's 40-to-82 manifest overturn) is resolved and re-measured, and a non-author falsification pass on 2026-10-01 CORRECTED the st2e header struct (+0x18 / +0x1C, headerSize 0, heap 0x20) with its regression applied (owner re-status 2026-10-01, OPUS, on SWE2-STRUCT's swe2struct-reopened3-0930)
owner_layer: none in the executable - this is the data side of the contract
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
  archive: FFXII_TZA.vbf, 31,196,932,183 bytes, SRYK, 89,414 entries
  method: archive index parsed and entries decompressed selectively; headers read from
    the extracted bytes and checked against file length arithmetic
last_reviewed: 2026-09-12
archive_formats:
  - "st2e | explained | the 73 st2e table units (.bin member): 32-byte header {st2e, count, recordSize, headerSize (32, or 0 when no record array), 0, heapOffset, +0x18, +0x1C (0, or a record-array end the registrar rebases)}, fixed-record and string-heap shapes (sections 2, 7); battle_pack sections bound to the registry by the STATIC delivery binder (the-encoded-id-space-and-the-query-record.md section 2.5), standalone copies requested by (kind, id) - per-table rows are registry slots (R family), not this row"
  - "battlepack | explained | battle_pack.bin (.bin member): section directory {u32 count 71, u32 sectionOffset[72], the last an end sentinel; equal neighbours = an empty section} over st2e tables and bank containers (section 'battle_pack.bin is a superset pack'; directory entry i at +4+4i, entry 61 = word.bin byte for byte) - the STATIC delivery binder reads each directory word into a registry descriptor (the-encoded-id-space-and-the-query-record.md section 2.5, battle-text-banks.md section 2.1)"
  - "commandpack | explained | commandpack.bin (.bin member): {u32 count, u32 offsets[count+1], {u16 actionId, u8 weight, u8 0} lists} - a byte copy of battle_pack directory +0x2C, read through registry slot 02EBF160 by the weighted-id resolver (AY-4 / AY-12)"
  - "shopdata | explained | shop_data.bin (.bin member): a byte copy of battle_pack directory entry 39 - the shop table {tag 0x64, stride 8, count 57, data 0xC} three-level layout of the-shop-table-and-its-stock-gates.md, read through its registry slot; the standalone copy is never requested (AY-12 paragraph)"
  - "wepjobmatrix | explained | wepjob_matrix.bin (.bin member): a byte copy of battle_pack directory entry 0 - {u16 stride 1, u16 count 23, u8 row[23]}, read through registry slot 02EBF180; the standalone copy is never requested (AY-12 paragraph)"
audit:
  passes: 8
  last_pass: 2026-10-01
  last_pass_kind: falsification
  last_pass_state: swe2struct-falsification-2026-10-01 - st2e header struct CORRECTED (+0x18 and +0x1C non-zero in 4 + 4, headerSize 0 in 14, heap 0x20 in 2 mons_act); the 82-entry manifest trigger re-measured and resolved
  crossref_clean: true
  reopened_count: 1
container_format: st2e
---

# The VBF archive and the `st2e` authored table format

> **Everything the executable does not contain is in one 31 GB file.** `FFXII_TZA.vbf` holds
> **89,414 entries**, and the authored tables inside it share **one header** — a four-byte magic and
> three counts — so a single reader walks all of them. ~~**`action_data.bin` is the file behind the
> action definition table**, and its own count field says **543**, which is exactly the bound the
> executable enforces.~~ *Corrected 2026-10-01 (SWE2-STRUCT for OPUS):* the action definition table is
> bound from `battle_pack.bin`'s directory entry `+0x3C` (§12, AY-6). `action_data.bin` is a copy of that
> section, shipped in four languages and requested by nothing (falsification pass 2026-10-01 below). Its
> count field says **543**, which is exactly the bound the executable enforces.

**For a player.** This is where the game actually lives: every spell's data, every menu string in
nine languages, every map, every sound bank. The executable is the machine; this is what it reads.

---

## 1. The archive

| | |
|---|---|
| path | `FFXII_TZA.vbf` beside the game directory |
| size | **31,196,932,183 bytes** |
| magic | `SRYK` |
| entries | **89,414** |
| access | the index is a header parse; **entries decompress individually** |

**The whole archive never has to be unpacked.** `analysis-kit`'s sibling tool
`agent_flow/tools/vbfextract.py` reads the index and pulls one entry at a time, which is what every
measurement here used.

```
gamedata      39,653      ps2data      39,578      prefetchdata   9,351      jsondata   832
```

| ext | count | | ext | count | |
|---|---:|---|---|---:|---|
| `.phyre` | 35,984 | Phyre assets | `.sab` | 4,609 | **SQEX sound banks** |
| `.txt` | 10,253 | | `.mot` | 4,392 | motion |
| `.ebp` | 10,045 | **scripts** | `.efx` | 3,288 | effects |

**Three existing documents are corroborated by the extension census alone** — `.sab` is
`SQEX::Sd::SabFile` from
[the sound engine](../../18-Audio/sead-engine-identity-and-diagnostics.md), `.ebp` is the script
container, and `.phyre` is the middleware's asset format.

## 2. The `st2e` table header

Authored binary tables begin with a 32-byte header whose first four fields are all that is needed to
walk them:

```c
struct St2eHeader {          /* 32 bytes */
    char  magic[4];          /* "st2e" */
    u32   count;             /* number of records            */
    u32   recordSize;        /* bytes per record             */
    u32   headerSize;        /* ~~32~~ 32 in 393 of 407; 0 in 14 (no record array) */
    u32   reservedA;         /* 0 in all 407 shipped files   */
    u32   heapOffset;        /* ~~headerSize + count*recordSize, or 0 when~~ */
                             /* ~~the table carries no heap (section 7)~~    */
                             /* headerSize + count*recordSize in 255; 0x20 in the  */
                             /* 2 mons_act copies (headerSize 0); 0 in 150        */
    u32   reservedB;         /* ~~0 in all 407 shipped files~~ 0 in 403 of 407 */
    u32   reservedC;         /* ~~0 in all 407 shipped files~~ 0 in 403 of 407 */
};
```

*Corrected 2026-10-01 (SWE2-STRUCT for OPUS), by the falsification pass of that date at the end of this page:* the struct's comments are struck
inside the block, because four of them were false over the 407 shipped files.
- **`+0x18` and `+0x1C` are not reserved.** `+0x18` is `0x7144` in the four `eitm_data.bin` copies and `+0x1C` is
  `0x98` in the four `tutorial_data.bin` copies. Each value is that file's record-array end, and the registrar rebases
  both. The AY-3 box in *Open questions* already carried this correction (FABLE, 2026-09-15). The struct above had
  not been updated to match.
- **`headerSize` is 0 in 14 files**, each with no record array (`count * recordSize == 0`): the empty tables of AY-11
  and the two `mons_act.bin` copies.
- **The heap rule misses those two `mons_act.bin` copies.** Their `heapOffset` is `0x20`, the first byte after the
  header, while `headerSize + count * recordSize` is 0.
- `+0x10` is 0 in all 407, as stated.

**Verified by arithmetic on the file length**, which is a check the format supplies itself:

| file | bytes | count | record | `count*rec + 32` |
|---|---:|---:|---:|---|
| `action_data.bin` | 32,612 | **543** | **60** | **exact** |
| `ability_data.bin` | 1,056 | 128 | 8 | **exact** |
| `attribute_data.bin` | 48 | 8 | 2 | **exact** |

### Two shapes, and the second one is a string table

Files whose `recordSize` is 4 or 8 do **not** satisfy that arithmetic — `help_action.bin` declares
322 × 4 and is 9,848 bytes.

> **CORRECTED in section 7.** This section said "the records are offsets". **They are string IDs**,
> and header field `+0x14` is the heap offset. The heap has its own `{one, base, size, count,
> offsets[count+1]}` header.

| file | count | rec | bytes |
|---|---:|---:|---:|
| `listhelp_action.bin` | 251 | 4 | 7,556 |
| `help_action.bin` | 322 | 4 | 9,848 |
| `questtitle.bin` | 257 | 4 | 3,032 |
| `key_signal.bin` | 69 | 4 | 824 |
| `battle_message.bin` | 102 | 8 | 6,668 |

**Fixed-record tables and string tables are distinguished by whether the arithmetic closes** — not by
a flag. `commandpack.bin` and `word.bin` carry no `st2e` magic and are a different format again.

## 3. `action_data.bin` — ~~the file behind registry slot `0x02EBF138`~~ a copy of it *(corrected §12: the slot is filled from `battle_pack.bin` `+0x3C`)*

[The authored data table registry](../authored-data-table-registry.md) documents slot `0x02EBF138` as
the **action definition table, ids `0`..`0x21E` (543)**, with ~~720~~ 723 references *(corrected 2026-10-02, OPUS: 722 reads and one `lea` over every function body)* — the second-highest in
the array — and records that the bound was confirmed independently from `BattleUnit_CommitAction`.

~~**This is very probably the file that fills it** — see the correction in section 5 —~~ *Corrected 2026-10-01
(SWE2-STRUCT for OPUS): it is a copy of the section that fills it (§12). The copy* supplies
what the code side could not:

```
ps2data/image/ff12/test_battle/<lang>/binaryfile/action_data.bin
   magic "st2e"   count 0x21F = 543   recordSize 0x3C = 60   headerSize 0x20 = 32
```

> **The file's own count field is `0x21F`. The executable's bound is `cmp di, 0x21E`.**
> A third independent derivation of 543, this time from the data rather than the code.

**The record size — 60 bytes — is new.** The registry document reads a row stride from the in-memory
header at `+0x08`, but never recorded the value for this table. Two known fields sit inside those 60
bytes: a byte at `+0x10` feeding `g_fFormulaScratchScale`, and a byte at `+0x12` used as a
hit/avoid/guard threshold.

~~**It is per-language.** Nine directories — `ch cn de es fr in it kr us` — matching the nine languages~~ *(Overturned 2026-09-12, §12: four directories carry the file; the table itself is identical in all nine `battle_pack.bin` files.)* ~~matching the nine languages
of [the locale system](../../19-Save-Load-Settings/Language-And-Locale/language-selection-and-locale-ids.md),
which means action data is localised, not merely its strings.~~

## 4. What this unblocks

[The battle action handler table](../../07-Combat-Action/Action-Dispatch/battle-action-handler-table.md)
closed **AT-5** with a hard negative: the executable contains **no action-name table**, so id→name
cannot be completed from the binary. **These files are the missing half** — `help_action.bin`,
`listhelp_action.bin` and `battle_message.bin` are per-language string tables in the same directory
as the 543-record definition table.

**Not yet read.** The offset-and-heap layout is established by arithmetic; the strings themselves,
their encoding, and whether their indices align with action ids are **not**. **AY-1.**
*(Read since; pointer 2026-10-01 (SWE2-STRUCT for OPUS): §7 decodes the strings, their custom charset and the
`40000 + category*100 + slot` id grid, and AY-1 is ANSWERED.)*

## Open questions

- [x] ~~Whether the string tables' indices align with action ids, and what encoding the heap uses.~~
      **ANSWERED — no.** Ids are `40000 + category*100 + slot` on a hundreds grid; encoding is a
      **custom charset**, `A`–`z` contiguous from `0x20`. Section 7. **AY-1.**
- [x] The unmapped character in `Magicks ? Technicks` (almost certainly `&`), and whether the CJK
      tables use a different glyph set. **AY-8.**
      *Half answered 2026-09-15 (FABLE): the byte is `0xA0`, and it is `&`.* In the `us` battle pack's 15 text banks
      (3,837 strings) `0xA0` occurs 16 times, every time where `&` belongs: `Axes & Hammers` (seven licence nodes),
      `Yagyu Darkblade & Mesa`, `Shikari Nagasa & Mina`, `Magicks & Technicks`, `Tinctures & Tonics`,
      `Light & Sturdy Garb`, and `Smelling Salts, &c.`. The last, the old abbreviation for *et cetera*, admits no
      other character. The same census reads **`0xAA` as `:`** (280 occurrences, e.g. every `Foe: …` gambit target
      name). **The CJK half stays open:** no CJK battle pack is in the local extract.
      *Confirmed from the bytes 2026-09-17 (FABLE): in the `us` `battle_pack.bin`, `Axes` is followed by `04 A0 04` and `Hammers`, `Salts` by `A7 04 A0 3C A8` (", &c."), and `Foe` by `AA` in 159 of its 160 occurrences; the battle-text-banks page's charset line, which had `0xAA` as `&`, is corrected to match. The CJK half is unchanged: still no CJK pack in the extract.*
      ***ANSWERED 2026-09-18 (FABLE) — the character is `&` (from the bytes, 2026-09-17), and the CJK copies do use a different glyph set.** The second half closes by cross-reference: [the battle text banks](St2e-Carriers/battle-text-banks.md) §5.2 (FX-3, 2026-09-11) extracted every `test_battle/<lang>/binaryfile/battle_pack.bin` from the archive index — all nine languages, `kr`, `cn`, `ch` and `in` included — and found the same fifteen banks with the same counts and byte-identical authored tables, while the strings differ in encoding: the five Latin-script copies spell *Vaan* with the same four charset bytes `35 3A 3A 47`, and the four CJK copies spell it with multi-byte sequences of their own. So the custom charset decoded here is the Latin one, and the CJK packs carry their own encoding over the same bank layout. The earlier note that no CJK pack was in the local extract was true of the extract, not of the archive. DATA: nine packs read from the `.vbf` index.*
- [x] What joins `action_data.bin`'s 543 records to the description ids. *(Marker normalised 2026-09-30 (FABLE, [record](../../_index/candidates/qid-marker-truth-fable-0930/README.md)): AY-9 is ANSWERED, negative now exhaustive.)* **NEGATIVE NOW EXHAUSTIVE** —
      u8/u16/u32 at every alignment, across `action_data` and all 37 tables inside `battle_pack.bin`.
      Nothing resolves. Section 9. **AY-9.**
- [x] ~~Whether the `40000 + category*100 + slot` ids are **authoring keys** rather than runtime string
      ids — they fall **outside the resolver's domain** (group 40 against a bound of 28). Needs the
      group tables at `0x02EC3D80` / `0x02F973C0`, which are **null in the file and populated at
      load**: a live-memory question.~~ **AY-10** — **answered 2026-09-08 in the negative** by the
      live read of the group tables: slot 4 is populated and its first ids are
      `40000, 40100, 40101, 40102`, so they **are** runtime string ids (section 9's contradiction
      box; [`EXP-002`](../../_experiments/EXP-002-st2e-group-tables.md)). What `FUN_002F9860`'s
      ÷ 1,000 path serves is the residue, carried by EXP-002. Box ticked propagated 2026-09-11, ASTRA-REQ-FABLE-STALE-I6-AY10.
      *(Pointer 2026-10-01 (SWE2-STRUCT for OPUS): that residue is answered in §9's correction of 2026-09-15. The ÷ 1,000
      path is positional over the same bank descriptor, and the ÷ 10,000 path is associative.)*
- [x] The 60-byte action record's field layout beyond `+0x10` and `+0x12`. **AY-2.** *Narrowed 2026-09-12:*
      [the action definition row](../../07-Combat-Action/Action-Definition-Row/the-action-definition-row.md) maps every byte by shipped values and names the readers of
      most; eighteen bytes have no reader yet.
      **Narrowed further 2026-09-18 (FABLE):* two of the eighteen are now named from the data on the action page (`+0x38` the player's list position, `+0x30` the shared performance id of the non-player actions); the readers of those two lie outside the combat idiom and are still to be found.*
      **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): every one of the 60 bytes is placed.** The action page maps them all, and after the 2026-09-19 narrowing (`+0x02` / `+0x03` / `+0x05` read by the range-band and reach code) only `+0x21` lacked a reader. It is an authored `u8` (6 on 174 rows, 0 on 129, 8 on 64, …), and **two independent instruments find no reader of it.** The first is the two-hop provenance census on the action page. The second sweeps every one of the 129 functions referencing the table's registry slot `02EBF138`, and it does see the `+0x20` byte accesses. Its only three `+0x21` operands are stores into a query record's `+0x21`, copied from other records' `+5` and `+0x26` (`0031E09A`, `0031E233`). So `+0x21` is a shipped value that nothing in this build consumes, and its authored meaning is not claimed. The layout itself is complete. Control: `_index/candidates/ay2-byte21/byte21_census.py` (3 checks).
- [x] ~~The last 16 bytes of the `st2e` header, unread here.~~ **AY-3 ANSWERED 2026-09-15 (OPUS) —
      read over every shipped carrier, not sampled.** All 407 `st2e` files in `FFXII_TZA.vbf`
      (73 distinct names across 9 language directories) were decompressed and their headers read.
      ~~Of the 16 bytes, **only `+0x14` ever carries a value; `+0x10`, `+0x18` and `+0x1C` are zero in
      all 407.** Those twelve bytes are reserved and the shipped data never uses them.~~
      ⚠ **WRONG, and corrected 2026-09-15 by FABLE (`2d08091f`) while answering AY-11 — the residual
      this very answer opened. The error was OPUS's.** `+0x10` is zero in all 407. **`+0x18` and
      `+0x1C` are not:** `+0x18` carries `0x7144` in the four `eitm_data.bin` copies and `+0x1C`
      carries `0x98` in the four `tutorial_data.bin` copies — **403 of 407** each, not 407.
      **And the values are the answer to AY-11.** `0x7144` is 28,996 and `0x98` is 152, each exactly
      `headerSize + count * recordSize` for its own file — the offset where the record array ends and
      the trailing bytes begin. So the “unexplained trailing data” this answer split out as AY-11 was
      declared by two header fields the same answer called always-zero, and **the two figures 28,996
      and 152 appear in AY-11's own text**, written there by me, without my noticing they were sitting
      in the header.
      *Cause, recorded because it repeated:* `measured-from-a-listing`. The scan printed a truncated
      `most_common()` of the tail tuples and I read “all zero except `+0x14`” off the visible rows;
      the four outliers sat past the printed lines. Same instrument as the `.bin`/`.dat` signature
      census earlier the same day, which reported 39 of 59 signatures for the same reason.
      **AY-11's other two shapes, closed 2026-09-19 (OPUS).** The correction above answers
      `eitm_data.bin` and `tutorial_data.bin`. AY-11 named two more things, and neither is reached
      by `+0x18`/`+0x1C`:

      - **`hpmpbase_data.bin` (234 bytes against 230) has all four words ZERO**, so nothing
        declares its tail — because there is nothing to declare. **Its four trailing bytes are all
        zero: padding.**
      - **The four "header-only files that record `headerSize` as 0 rather than 32" are EMPTY
        TABLES.** `actionchip_data.bin` (count 0, stride 8), `jochumodel_data.bin` (count 0,
        stride 4), `s_daiji_data.bin` (count 0, stride 10) and `bukitye_data.bin` (**count 23,
        stride ZERO**) are each exactly 32 bytes with nothing after the header. `headerSize` is 0
        because **no array follows it** — the field is an offset to an array that does not exist,
        not a mis-written 32.

      **The closure, over all 73 distinct st2e names:** 33 carry no trailing data; **35 carry
      trailing data declared by a header word equal to `headerSize + count * recordSize`**; 1 is
      the zero padding above; 4 are the empty tables above; and **0 carry undeclared non-zero
      trailing data.** So there is no unexplained trailing data anywhere in the st2e corpus, which
      is what AY-11 asked and is more than the three files it listed.

      > *One caution on that census, from its own first run.* Classifying by "a header word equals
      > the array end" reports the four empty tables as **declared**, because their array ends at 0
      > and their words are 0 — a **vacuous match**. They are separated above by hand. A
      > re-run must exclude `headerSize == 0 && count * stride == 0` before counting.

      `+0x14` is the **heap offset already identified in section 7** — this does not re-derive it, it
      pins it: in **255** files `+0x14` is *exactly* `headerSize + count * recordSize`, the first byte
      past the record array, and the dword at that offset is `00000001` in **all 255** — the heap's own
      `one` field. In **150** files it is `0`, and **126** of those end exactly at
      `headerSize + count * recordSize`, i.e. they have no heap to point at.
      It is also **language-invariant**: `help_action.bin` is 7,904–12,748 bytes depending on language
      but `+0x14` is 1,320 in all nine, because the record array is the same size and only the heap
      differs. That is the strongest evidence it is the heap's **start**, not its size.
      *Residual — 7 names, carried by [AY-11](#ay-vbf-archive):* `eitm_data.bin`, `tutorial_data.bin`
      and `hpmpbase_data.bin` have trailing bytes past the record array with `+0x14` still `0`;
      `actionchip_data.bin`, `jochumodel_data.bin`, `s_daiji_data.bin` and `bukitye_data.bin` are
      header-only files that record `headerSize` as `0` rather than 32. Neither shape contradicts the
      reading of the 16 bytes; both are unexplained trailing data, which is a different question.
      > **Corrected 2026-09-15 (FABLE) — `+0x18` and `+0x1C` are not always zero, and the engine reads both.** A re-census
      > of the same 407 files (`work/FABLE/drift4/ay11_st2e_trailers.py`, full extract `D:/FFXII_TZA_extract`) finds
      > `+0x10` zero everywhere but `+0x18` non-zero in **4** files and `+0x1C` in **4**. They are exactly the AY-11
      > residue. The `+0x14` counts reproduce: 255 heaps at the array end, plus two `mons_act.bin` copies with `+0x14 = 0x20`.
      > - **The registrar rebases them.** `AreaData_BindAndRebaseSectionDescriptor` (`003845F0`) adds the header's own
      >   address to each of `+0x0C`, `+0x10`, `+0x18` and `+0x1C` that is non-zero (`00384600`–`00384640`), before
      >   `+0x14`'s heap walk. That is [the row-lookup contract](../CONTRACT-authored-table-row-lookup.md) §7.
      > - **`+0x18` is the equipment attribute-block heap.** In `eitm_data.bin` (`kr` / `in` / `cn` / `ch`) it is `0x7144`,
      >   the end of the 557 × 52 array, and the file's 4,224 trailing bytes are 176 blocks of 24 bytes.
      >   - The pack binder's `00238160` adds `[slot 02EBF0F8 + 0x18]` to every equipment row's `+0x28` handle and
      >     stores it back (`00238225`–`0023823E`).
      >   - The stat rebuild ([the definition-record flag pair](../../04-Actor-Entity/the-definition-record-flag-pair.md)) then reads those blocks: `+0x08`
      >     permanent statuses, `+0x0C` immunities, bytes `+0x10`–`+0x14` affinities.
      >   - `battle_pack.bin`'s `+0x38` section carries the same header, and the file equals that section's first 33,220
      >     bytes.
      > - **`+0x1C` is a group-end list.** In `tutorial_data.bin` it is `0x98`, the end of the 6 × 20 array. The 24
      >   trailing bytes are `{u32 count = 5; u32 end[5] = 0, 2, 4, 5, 6}`.
      >   - `0032A230`, called from `BattleMenu_BuildCommandEntryList`, reads `[slot 02EBF020 + 0x1C]`
      >     (`0032A25A`), bounds the group index by `count` and takes rows `[end[i−1], end[i])`, empty for `i = 0`.
      >   - The file equals the first 176 bytes of `battle_pack.bin`'s `+0x70` section.
      > - **`hpmpbase_data.bin`'s 4 extra bytes are zero**, and no header field points at them. The file is the first 234
      >   bytes of the pack's `+0x28` section, which continues with zeros, so they are padding.
      > - **A `headerSize` of 0 is the format's "no record array" value.** `+0x0C` is an offset the registrar rebases
      >   only when non-zero.
      >   - `jochumodel_data.bin` and `s_daiji_data.bin` have count 0 and equal the first 32 bytes of the pack's `+0x14`
      >     and `+0x94` sections, which carry the same zero.
      >   - `actionchip_data.bin` (count 0, record size 8) and `bukitye_data.bin` (count 23, record size 0) ship only
      >     for `cn` / `kr` and have no pack counterpart. Both declare no bytes of records.
      > So *"those twelve bytes are reserved and the shipped data never uses them"* holds for `+0x10` only. AY-11 is
      > answered by this note.
- [x] **UQ-72.** What the path pool at `0x01E4D830` contains beyond the 82-entry battle/menu region. It runs
      for **thousands** of slots; the loader registers bases at slots 0, 84, 128, 450 and 1640, and
      the later regions hold `.nmb` and `.ebp` paths keyed by **map codes** (`tst_a`, `bts_a`,
      `e00_a`), not languages. **PROPOSED-reposd2-7.**
      **ANSWERED 2026-09-15 (FABLE), static: it is not one pool.** The memory after the 82-entry array holds other
      resource kinds' path arrays laid end to end, and each registered base is the start of one of them.
      - **What installs them.** `ResourcePath_Init` (`002DF9A0`) is the only function that references the region.
        Every array address it loads is stored into one slot of `g_pathTables` (`0215F000`, 41 kinds), either
        unconditionally or in one arm of its language switch.
      - **The five bases are these arrays:**
  ***NARROWED 2026-09-17 (FABLE):** the action-row page's hop census (`UQ-106`) now names readers for eleven of the eighteen bytes that lacked one; `+0x02`, `+0x03`, `+0x21`, `+0x30` and `+0x38` remain reader-less at one hop.*

        | pool slot | address | installed at | kind | first entries |
        |---:|---|---|---:|---|
        | 0 | `01E4D830` | `002DFF55` | 2 | the 82 battle files (§6, §11) |
        | 84 | `01E4DAD0` | `002DFD83` | 9 | `NULL`, then `common\test_map_ref.bin` … `summoneffectdata.bin` |
        | 128 | `01E4DC30` | `002DFAE4`, unconditional | 26 | the 321 `in` `.nmb` paths ([the `.nmb` sheet](St2e-Carriers/area-nmb-index.md)) |
        | 450 | `01E4E640` | `002DFD98` → `002DFF7F` | 7 | `NULL`s, then `myoshiok\...\Bin_Menu\fontcolor.bin`, the menu resources |
        | 1640 | `01E50B70` | `002DFCD1` | 5 | `plan_work\de\plan_map\tst_a\tst_a01\global\tst_a01.ebp`, `.mot`, `.fpk` — the per-map triple |

      - **The "regions" are consecutive arrays from different arms, not one ordered pool.**
        - Kind 2 at slot 0 is stored in the arm at `002DFF39`, but kind 9 at slot 84 and kind 7 at slot 450 in the arm at
          `002DFD4B`, and kind 5 at slot 1640 in yet another.
        - Their path strings carry different language directories (`in` for 0–449, mostly `es` at 450–1639, `de` from
          1640).
        - Walking pointer slots from `01E4D830` runs 80,974 slots before the first non-pointer.
        - That walk measures `.rdata` layout, not an array length. Lengths are the callers' (the FileSizeTable's 5,000
          ids per kind), as the `.nmb` sheet §3 already warns.
      - **What each kind holds** is the `.nmb` sheet's *every resource kind in the table*: slot, number of variants
        and first entries for all 41.
      - Census: `work/FABLE/drift4/uq72_path_pool.py`, and the lea / store pairs of `002DF9A0`.
- [x] **UQ-73.** Whether the interior NULL at slot 40 is a sub-group boundary the game uses at a level above
      this loader, or padding. It is reproduced identically in every language block, so it is
      authored, not incidental. **PROPOSED-reposd2-8.**
      **ANSWERED 2026-09-15 (FABLE): neither — slot 40 is an empty entry of `battle_pack.bin`'s own 71-entry directory,
      and the numbering runs straight through it.** This is an authored-data census of all nine language packs in
      the full extract `D:/FFXII_TZA_extract` (`work/FABLE/drift4/uq73_manifest_vs_pack.py`). An entry's length is the
      distance to the next entry's offset.
      - **The manifest is the pack's directory order.** `battle_pack.bin` opens with ~~`{u32 count = 71; u32 offset[71]}`~~ `{u32 count = 71; u32 offset[72]}`, the last an end sentinel *(corrected 2026-10-02, OPUS: the binder's `+0x56` `lea rbx, [r9 + 4]` and `+0x97` `add rbx, 4`, over count + 1 entries to its `+0x9B` `cmp rdi, rax` and the `jle` at its `+0x9E`)*
        in all nine languages, and **manifest slot *k* is pack entry *k*** (directory `+4 + 4k`) for *k* = 0 … 70.
        - `WepJob_Matrix` is `+0x04`, `commandpack` `+0x2C`, `action_data` `+0x3C`, `status_data` `+0x40`,
          `attribute_data` `+0xA8`, `word.bin` `+0xF8` and `license_board` `+0x11C`.
        - The registry map's directory offsets (the row-lookup contract §7a) are these same entries.
        - Slots 71–82 (`board_1` … `board_12`) lie past the pack's directory.
      - **Two kinds of slot, told apart by the pack entry.**
        - **40 slots** have a non-empty entry in every pack, and their file ships standalone only in `in`, `kr`, `cn` and
          `ch`. In 33 of them all four copies equal the pack entry byte for byte (trailing pack bytes zero). The other
          seven differ in some copies: `license_data`, `action_data` (`kr` / `cn`, as §12 found), `menkyo_data`,
          `horidashi`, `ability_data`, `savemember_data` and `movie`.
        - **27 slots** are the localised files, whose pack entry is empty in all nine packs and whose file ships in
          all nine languages: `key_signal`, `menu_*`, `help_*`, `listhelp_*`, `questtitle`, `penelosdiary`, `menu00`–`04`
          and `battle_pack.bin` itself.
        - `battle_message` and `word.bin` are both packed and shipped in all nine, equal to their entries.
      - **Slot 40 is an empty entry with no file.** Its entry (`+0xA4`) has the same offset as slot 41's in all nine
        packs, and no language ships a file for it.
        - Slot 67 (`menu05.bin`) is the same case with a name: an empty entry and no file in any language.
        - The indices after 40 keep their pack positions: 41 is `+0xA8`, 42 `+0xAC`.
        - So the NULL is an unused index inside one list, not a group boundary and not padding between groups.
        - Why that index was left unnamed is authoring history the data does not record.
      - **This also explains the four-language pattern of AY-5 and AY-12.** The `in` / `kr` / `cn` / `ch` directories
        carry the individual tables that `battle_pack.bin` packs; the other five languages ship only the pack.
        Whether any loader opens those standalone copies is still not shown.
        *Answered 2026-10-01 (SWE2-STRUCT for OPUS), static: no request by constant reaches any of the 40. The kind-2
        loader `00384420` is called only for `0x13` (`battle_pack.bin`), for `0x47 + n` (the boards) and for the ids
        in `01E09F68`, which are the 26 localised slots plus 67. No direct call to a request API carries `(2, k)` for
        any of the 40 ([record](../../_index/candidates/swe2struct-reopened3-0930/README.md), checks Q1-Q6). An id computed at run time is outside this census.*
- [x] ~~**UQ-74.** The three dwords at `0x0215EFF4`, immediately below the `0x0215F000` directory, which
      `FUN_002DF780` takes the address of. **PROPOSED-reposd2-9.**~~ **Answered 2026-09-14 (FABLE)** from a RIP census of `0215EFF0`–`0215F004`:
      - **`0215EFF4` is the read status word**, already closed as FZ-14 on [the resource request queue](../the-resource-request-queue.md) §8. The two read issuers `002DF6C0` and `002DF780` pass its address as the result pointer to the loose-file open or the archive read. The reader remembers the pointer (`01F82CC0`) and writes −1 when the job is queued (`001D6FF4`). The completion callback `001D6D70` stores the job's result through the pointer and forgets it. The pump's `0046DFE0` waits while the word is −1, and `0046E0E0` hands the settled value to state 5 (≥ 0) or 6 (negative).
      - **`0215EFF8` is a data slot of the directory itself.** The directory initialiser `002DF9A0`, reached from the boot subtree, stores its address into directory entry `0215F018` (`002DF9D3`–`002DF9DA`). No other RIP-relative reference touches it.
      - **`0215EFFC` has no RIP-relative reference.** It is not claimed as a separate field, and may be the second half of the `0215EFF8` slot.
      So the three are not one structure: a live status word, and a pointer target published by the directory it sits below.
- [x] ~~`commandpack.bin` and `word.bin` carry no `st2e` magic — what format they are.~~
      **AY-4 ANSWERED 2026-09-15 (OPUS). Both use the directory shape this database already
      documents — they are not a new format.** The layout is
      `{ u32 count; u32 offsets[count+1]; payload }`, the offsets **absolute from the start of the
      file** and ascending, with `offsets[count]` an end sentinel equal to the file length. That is
      the same `count + 1` offset table as `battle_pack.bin`'s bank directory
      ([the battle text banks](St2e-Carriers/battle-text-banks.md) §2.1) and as the `st2e` heap's own
      `offsets[count+1]` (§7). **Verified as a falsifiable prediction on all 13 copies** — 4 of
      `commandpack.bin` and 9 of `word.bin` — requiring `offsets[0]` to equal the table end and
      `offsets[count]` to equal the file size exactly: 13 of 13 PASS.
      **`word.bin` is the fifteen battle text banks as a standalone file.** It is the shape applied
      twice: 15 blocks, each itself `{count, offsets[count+1], payload}`, 15 of 15. The block counts
      are 545 · 544 · 1 · 362 · 63 · 32 · 284 · 16 · 629 · 128 · 129 · 512 · 512 · 16 · 64 — **identical to
      the fifteen banks already censused** on the battle-text-banks page. Leaves are packed strings in
      the §7 `us` charset behind a leading `u16`. *Both of that page's positive controls pass against
      `word.bin`*: bank 0 `0x106`–`0x112` decodes as the thirteen Espers (Belias … Zodiark) and bank 5
      entries 2 / 16 / 17 as Petrify / Disease / Lure. It differs in all nine languages, as localised
      text must.
      **`commandpack.bin` is 826 variable-length entries of `u16` pairs.** Every one of the 826 entry
      lengths is a multiple of 4 and the bodies read as `(u16, u16)` pairs — entry 0 is
      `(01AB,001E) (0096,0046)`, entry 1 `(0154,0014) (01AB,001E) (0096,0032)` — so an entry is a list
      of key/value words, not a fixed record. It is **byte-identical in all four copies**, and it ships
      for **only four languages — `kr`, `in`, `cn`, `ch`** — with no `us`, `de`, `es`, `fr` or `it`
      copy in the archive at all. *What the pair keys mean is not read here*; `0x0096` recurs as a key
      in most entries. Carried by [AY-12](#ay-vbf-archive).
      **AY-12 half answered 2026-09-15 (FABLE) — the pairs are weighted action lists, and the file is a copy.**
      This is an authored-data census of all nine language directories of the full extract `D:/FFXII_TZA_extract`
      (`work/FABLE/drift4/ay12_commandpack.py`).
      - **It is a copy of a `battle_pack.bin` section.** `commandpack.bin` (17,660 B, the same in `kr`, `in`, `cn` and
        `ch`) equals the first 17,660 bytes of `battle_pack.bin`'s directory `+0x2C` section. The section's last four
        bytes are zero padding. That section is byte-identical in all nine `battle_pack.bin` copies.
      - **A pair is `{u16 action id, u8 weight, u8 0}`.**
        - Byte `+3` is 0 in all 3,587 records.
        - Every id is below 543, an action-table row. The commonest is `0x96` *Attack* (726 records).
        - The weights of **each of the 826 lists sum to exactly 100**.
      - **The reader fixes that meaning.** The weighted-id resolver, reached through registry slot `02EBF160`,
        takes an order record's selector at or above `0x8000` as list `selector − 0x8000` (§8i of
        [the gambit page](../../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md)).
        - It draws `r = rand % 100`.
        - It walks the 4-byte records adding byte `+2` and returns the first id whose running sum exceeds `r`,
          else `0xFFFF`.
        - Byte `+3` is never read.
        - Entry 0, `(0x1AB, 30) (0x96, 70)`, is a 30 % *Ram* / 70 % *Attack* choice.
      - **Why only four languages carry the copy stays open.** It is the same pattern as `action_data.bin` (AY-5, §12):
        the four CJK-script directories carry standalone copies of shared `battle_pack.bin` sections.
        - The copy is not localised.
        - No reader of the standalone file is shown, although manifest slot 10 (§6) names it.
        - *Pointer 2026-10-01 (SWE2-STRUCT for OPUS):* AY-12's register answer (2026-09-19) records the four-language
          shipping as a packaging fact, not content. No request by constant reaches slot 10 either (the UQ-73 note
          above, checks Q1-Q6).
      **The same holds for `shop_data.bin` and `wepjob_matrix.bin` (2026-09-29, SWE2-DATA,
      `OPUS-REQ-DATA-BUCKET-MEMBER-FORMATS`; check
      [`b6_battle_copies.py`](../../_index/candidates/bucket-members-0929/checks/b6_battle_copies.py), 34 checks, FAILS 0).**
      Each ships in the same four directories (`ch`, `cn`, `in`, `kr`) and is a byte copy of a
      `battle_pack.bin` directory entry, identical in all nine `battle_pack` copies:
      - `wepjob_matrix.bin` = the first 27 bytes of entry 0 (directory `+0x04`) plus 5 zero bytes:
        `{u16 stride = 1, u16 count = 23, u8 row[23]}` (`4 + 1·23 = 27`). The section is bound to
        registry slot `02EBF180` and read as `[slot + stride·category + 4]` (reader sites in
        [`b6_battle_copies.out.txt`](../../_index/candidates/bucket-members-0929/checks/b6_battle_copies.out.txt)).
      - `shop_data.bin` = the first 11,892 bytes of entry 39 (directory `+0xA0`) plus 4 zero bytes:
        the header `{tag 0x64, stride 8, count 57, data 0xC}` of
        [the shop table](../../12-Items-Equipment-Shops-License/the-shop-table-and-its-stock-gates.md),
        whose three-level walk reproduces 57 rows, 267 lists and 2,512 ids. The section is rebound
        to `02EBF158` and read by the shop listing and shop-name readers that page names.
      - **The standalone copies are not requested.** They are kind-2 path entries 0 and 39; no call
        to a request API passes `(2, 0)` or `(2, 0x27)`, the kind-2 loader is reached only with `0x13`
        (`battle_pack.bin`), `0x47 + n` (the boards) or ids from the message table `01E09F68`, which
        holds neither, and no prefetch list names them.
- [x] ~~Why action data is **per-language** rather than shared with localised strings alongside.~~
      **AY-5 — premise false (2026-09-12, §12):** it is not per-language; the table is byte-identical in all
      nine `battle_pack.bin` files, and `action_data.bin` exists only in `ch`, `cn`, `in` and `kr`.
- [x] **Prove the binding** `action_data.bin` → registry slot `0x02EBF138`. **AY-6 ANSWERED 2026-09-12, the other
      way (§12):** the slot is bound from `battle_pack.bin`'s directory `+0x3C` by `00237FC0`, called from the
      STATIC delivery binder at `00236D85`; `action_data.bin` is not the source. Original text: The manifest is now found
      (section 6) and its loader registers it into **`0x0215F000`**, not `0x02EBF008` — so the route,
      if any, is not through `FUN_002DF9A0`. **AY-6.**
- [x] ~~What the pointer registry at `0x0215F000` is.~~ **ANSWERED — the asset-category path
      directory**, 41 slots, one per content type, read by 4 `Resource` functions. **Disjoint from the
      `0x02EBF008` content registry**: no function references both. Section 8. **AY-7.**

## 5. Falsification pass 2026-09-02 — the slot binding was asserted, not proven

**Attack chosen.** Section 3 said *"this is the file that fills [slot `0x02EBF138`]"*. That rested on
a **count match**: the registry documents 543 entries, the file declares 543. By this database's own
standard a count match is suggestive, not deciding — a second table of 543 anything would satisfy it
equally.

### What the attack strengthened

**The executable contains the path literal.** Searched as ASCII and UTF-16:

```
PS2Data\image\FF12\test_battle\in\BinaryFile\action_data.bin      VA 0x00A42148
PS2Data\image\FF12\test_battle\ch\BinaryFile\action_data.bin      VA 0x00C1BFF8
```

**The game demonstrably loads that specific file** — a much stronger statement than "a 543-record
file exists in the archive". `test_battle` appears **398** times, so the other languages' paths are
present too.

### What the attack failed to prove — and the claim is downgraded

**Nothing in `.text` references those strings.** A `lea`-target scan across all 34,270 function
bodies finds **zero** references to either address. The path is never materialised by code.

Instead the strings sit in a **mixed pool** in `.rdata` — consecutive entries are different
languages and unrelated asset types (`.vpcjp`, `.fpk`, `.mot`, `.ebp`, `.efx`, `.dat`, `.snd`) — with
**8-byte pointers into it from `.data`**.

> **PARTLY WRONG — corrected in section 6.** This section concluded from that "a runtime-indexed
> resource path pool, **not a static manifest**". **There is a static manifest**: a 40-entry
> `const char*` array at `0x01E4D830`, per language, in fixed order. This section looked at the
> strings and stopped; it should have followed the pointers **to** them.

> **Downgraded:** `action_data.bin` → slot `0x02EBF138` is a **strongly supported lead**, resting on
> two independent circumstantial facts — the exact path literal in the executable, and a record count
> matching the enforced bound `0x21E` — and **not on any observed binding**. **AY-6.**

**What would settle it** is the loader: the code that reads a pooled path, pulls the entry, and stores
the resulting pointer into the registry array at `0x02EBF008`–`0x02EBF1F8`. That is a runtime
association, so a static proof needs the pool's index structure read, not more string searching.

### What is unaffected

The `st2e` header, the two file shapes, and the arithmetic that distinguishes them are read directly
from the bytes and stand. So does the observation that **the file's own count field is `0x21F` = 543**
while the executable enforces `cmp di, 0x21E` — that remains a genuine third derivation of the bound,
independent of which slot the table lands in.

## 6. The authored-data manifest — and a correction to section 5

### Section 5 was wrong about the manifest

It concluded: *"a runtime-indexed resource path pool, not a static manifest."* **There is a static
manifest.** Section 5 looked at the **strings** and found them pooled and unreferenced, which is true
— and stopped there. It should have followed the **pointers to** those strings.

### The manifest

```
0x01E4D830 .. 0x01E4D968     40 x const char*     one language block
```

Forty path pointers in a **fixed order**, repeated per language, each entry
`PS2Data\image\FF12\test_battle\<lang>\BinaryFile\<file>`.

> **OVERTURNED in section 11 — this is not the complete set.** The region is **82 entries**
> (slots 0..82, with one interior NULL at slot 40), and the loader's next registered base is slot
> **84**, not 40. The forty below are correct and correctly ordered; they are the first forty of
> eighty-two, cut at an interior NULL that the loader does not treat as a boundary. The 42 omitted
> include `attribute_data`, `ability_data`, `word.bin`, `listhelp_action` and `listhelp_status` — five files **this document analyses elsewhere**.

The forty, in order:

| # | file | | # | file | | # | file |
|---:|---|---|---:|---|---|---:|---|
| 0 | `WepJob_Matrix` | | 14 | **`action_data`** | | 27 | `tutorial_data` |
| 1 | `key_signal` | | 15 | `status_data` | | 28 | `price_data` |
| 2 | `battle_message` | | 16 | `chr_data` | | 29 | **`maho_data`** |
| 3 | `damagemp_data` | | 17 | `comac_data` | | 30 | **`waza_data`** |
| 4 | `jochumodel_data` | | 18 | `dougu_data` | | 31 | `yugoyaku_data` |
| 5 | `sobicategory_data` | | 19 | `battle_pack` | | 32 | `eventitem_data` |
| 6 | **`drop`** | | 20 | `menu_command` | | 33 | `m_daiji_data` |
| 7 | `targetchip_data` | | 21 | `menu_message` | | 34 | `g_daiji_data` |
| 8 | **`gambit_data`** | | 22 | `help_menu` | | 35 | `q_daiji_data` |
| 9 | `hpmpbase_data` | | 23 | `help_action` | | 36 | `s_daiji_data` |
| 10 | `commandpack` | | 24 | `listhelp_daijinamono` | | 37 | `eis_data` |
| 11 | `mgccategory_data` | | 25 | `questtitle` | | 38 | `questreward_data` |
| 12 | **`license_data`** | | 26 | `menkyo_data` | | 39 | **`shop_data`** |
| 13 | `eitm_data` | | | | | | |

**This is the index to the game's content**, and it names systems this database documents from the
code side without ever seeing their data: `gambit_data` for
[gambit evaluation](../../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md), `drop` for
[loot](../../13-Rewards-Progression-Economy/loot-drops-and-enemy-chain.md), `license_data`,
`maho_data` (magick), `waza_data` (technick), `shop_data`, `price_data`.

**`action_data.bin` is index 14.**

### The loader, and what it does not do

The manifest has **exactly one code reference in the image**: `002DFF47`, inside **`FUN_002DF9A0`**
(2,831 B, owner `Resource`), which takes the array base.

That function is a long initialiser that fills a **large pointer array at `0x0215F000`** with the
addresses of `.data` structures — dozens of `lea reg,[rip+X]` / `mov [rip+Y],reg` pairs at
`0x0215F000`, `+0x18`, `+0x20`, `+0x30`, `+0x50`, `+0x58` and onward.

> **`0x0215F000` is a second pointer registry, distinct from the `0x02EBF008` registry** documented in
> [the authored data table registry](../authored-data-table-registry.md). Neither the manifest nor
> this loader touches `0x02EBF008` — a scan for registry-slot references inside the function finds
> none.

**That does not confirm AY-6; if anything it complicates it.** The manifest is registered into the
`0x0215F000` array, so the route from `action_data.bin` to slot `0x02EBF138` — if it exists — does
not run through this function. **AY-6 stays open**, and **AY-7** is the new question: what
`0x0215F000` is, and how the two registries relate.
*(Pointer 2026-10-01 (SWE2-STRUCT for OPUS): AY-6 was answered the other way on 2026-09-12 (§12), and AY-7 in §8.)*

**What is now firmly established** is narrower and still worth having: the game loads a fixed,
ordered set of named authored tables **per language** — **82 of them**, see section 11 — `action_data.bin` is one of them at fixed index **14**, and its path is in the
executable.

## 7. The text format decoded — and section 2 was wrong about the string tables

### Correction: the records are string IDs, not offsets

Section 2 called the `recordSize`-4 files "string tables … the records are offsets and the remainder
is a text heap". **The records are string IDs**, and they point nowhere in the file — values run
40000+, 100000+, 120000+, and none lands inside the file at any base.

**Header field `+0x14` is the heap offset** (~~`== headerSize + count*recordSize`~~ `headerSize + count*recordSize` in 255 files, but `0x20` in the two `mons_act.bin`, whose `headerSize` and `recordSize` are 0 *(corrected 2026-10-02, OPUS: the shipped headers, `headerSize` 32 in 393 of 407; §2's corrected struct)*), which separates the
two shapes without guessing:

```c
struct St2e {                     struct Heap {                 /* at +0x14 */
    char magic[4];   /* st2e */       u32 one;                  /* 1        */
    u32  count;                       u32 base;                 /* 12       */
    u32  recordSize;                  u32 heapSize_minus_1;
    u32  headerSize; /* 32 */         u32 count;   /* <- corrected 2026-10-02, OPUS: headerSize is 32 in 393 of 407 and 0 in 14; the two mons_act.bin keep heapOffset 0x20 with headerSize 0 */
    u32  zero;                        u32 offsets[count + 1];   /* +1: end sentinel */
    u32  heapOffset;                  char text[];              /* relative to heap + base */
};                                };
```

**`count + 1` and `base = 12` are both forced by the data**, and this is the trap in the format:
with `count` offsets and a heap-relative base **every string still decodes** — as its own last ten
characters. `"oenix Down"`, `"old Needle"`. **A wrong reading here produces plausible text rather
than garbage**, which is exactly the failure mode that survives a glance.

### The character set is custom — neither ASCII nor Unicode

```
0x20..0x39 -> 'A'..'Z'  (+0x21)      0x04 -> space      0x00 -> terminator
0x3A..0x53 -> 'a'..'z'  (+0x27)      0x02 -> line break
0xA8 '.'   0xA7 ','   0xAC '\''   0xA2 '/'   0xA3 / 0xA5 hyphen
0xA0 '&'   0xAA ':'                 (added 2026-09-15, AY-8: from every occurrence in the us text banks)
{0F}xx -> inline escape (colour or numeric variable)
```

`A`–`z` is one contiguous run starting at `0x20`; punctuation lives above `0xA0`. **This is the `us`
table only.** The CJK tables index a different glyph set and were not tested — the mapping above must
not be assumed to carry.

**The set is incomplete:** entry 15 of the command block decodes as `Magicks ? Technicks`, where `?`
is an unmapped byte (almost certainly `&`). **AY-8.**

### `word.bin` is a container, and block 3 is the battle command menu

`word.bin` carries no `st2e` magic because it holds 15 blocks:
~~`{u32 count = 15; u32 headerSize = 68; u32 blockOffsets[15]}`~~ `{u32 count = 15; u32 offsets[16]}`, `offsets[0]` = 68 being block 0's start and `offsets[15]` the end *(corrected 2026-10-02, OPUS: the binder `003846F0` rebases count + 1 words from `+4` (`003846F0+0x56`, `003846F0+0x9B` / `003846F0+0x9E`) for slot `02EBF170`, called at `00236C30+0x3BA`; AY-4 above)*, each block
`{u32 count; u32 offsets[count+1]; records}` with offsets relative to the block.

**Its validity check is `offsets[0] == 4 + (count+1)*4`**, which holds on every block — verified
independently here.

**Block ~~3~~ 4, 63 entries — the player's battle command list** *(corrected 2026-10-02, OPUS: 0-based, `offsets[4]` = 35,444 in `us`; the binder `003846F0` rebases all sixteen words from `+4`, and the struck `headerSize` reading numbered it 3)*, decoded from the bytes:

```
 0 Attack        5 Summon       10 Gambits            18 White Magicks   23-30 Fire Lightning Ice
 1 Magicks       6 Quickening   15 Magicks & Technicks 19 Black Magicks        Earth Water Wind
 2 Technicks     7 Foecraft     16 Mist                20 Time Magicks         Holy Dark
 3 Items         8 Dismiss                             21 Green Magicks
                                                       22 Arcane Magicks
```

### The developers shipped their own `NOT USED` markers

**Ten entries in the retail data are labelled `NOT USED`**, naming cut command slots for free:

```
 4 NOT USED concentration    13 NOT USED escape          53 NOT USED crown
 9 NOT USED trap             14 NOT USED escape-cancel   61 NOT USED etc
11 NOT USED cancellation     17 NOT USED order           62 NOT USED monshands
12 NOT USED all-cancel
```

**A cancelled "concentration" command, a trap command, an order command, and a three-way
cancel/escape group** — features that reached the string table and not the game.

### The description ids are `40000 + category*100 + slot`

`help_action.bin`'s 322 ids resolve to a hundreds grid, **not** to action ids — only 82 of 322 fall
below 543:

| block | range | n | contents |
|---:|---|---:|---|
| 1 | 100–117 | 18 | White Magick |
| 2 | 200–217 | 18 | Black Magick |
| 3 | 300–314 | 15 | Time Magick |
| 4 | 400–414 | 15 | Green Magick |
| 5 | 500–514 | 15 | Arcane Magick |
| 6 | 600–641 | 42 | Items |
| 8 | 800–823 | 24 | Technicks |
| 9 | 900–917 | **18** | Quickenings |
| 10 | 1000–1012 | **13** | Espers |
| 11 | 1100–1195 | 96 | enemy actions |

**Three checkable validations, not readings of prose:** block 10 has **13** entries and FFXII has
exactly **13 Espers**; block 9 has **18 = 6 characters × 3 quickening ranks**; and blocks 1–5 appear
in White, Black, Time, Green, Arcane order — **the same order as `word.bin` block ~~3~~ 4 *(corrected 2026-10-02, OPUS: 0-based, as corrected above)* entries 18–22**,
two independently derived orderings agreeing.

### The negative that remains

**`action_data.bin`'s 543 records do not reference the text by string id.** Every `u16` and `u32`
field at every byte alignment was scanned against the id sets of nine string tables; **no field
resolves**. The best partial (238 of 411 non-zero) is coincidence on small values and is not reported
as a finding.

Two leads, explicitly not findings: `+0x34` is a **permutation of 0..542** (543 distinct values, max
542 — an ordering, but not the record index), and `+0x2E` runs 10000, 10001, 10002… in the id range
`menu_command.bin` uses — but that file decodes to the **job list** ("White Mage", "Uhlan",
"Machinist", "Knight", "Monk", "Foebreaker", "Archer", "Shikari"), so the pairing resolves to the
wrong table.

**What would settle it:** something indexed 0..542 carrying a (category, slot) pair — either a
543-entry index table elsewhere in the archive, or a packed bitfield inside `action_data`'s record.

> **Settled 2026-09-11 — the `+0x34` lead was the answer, and the negative was scoped too narrowly.**
> `action_data.bin` does not reference the string-id files at all; its names live in
> [the battle text banks](St2e-Carriers/battle-text-banks.md) — a two-level section of
> `battle_pack.bin` (directory entry at the blob's `+0xF8`, registry slot 45) that the HUD reads
> through row `+0x34` as a 5 : 11 `bank : index` word (`00305F94`–`00305FD8`). All 543 rows resolve
> inside bank 0 (545 action names, 528 of them at the row's own index — the "permutation"), and
> `0x113` decodes as **Dismiss**, `0x95` as **Dismount**, `0x106`–`0x112` as the thirteen Espers.
> The negative above stands for the nine string-id files; it never covered the banks.
`battle_pack.bin` (281 KB, same directory) is the obvious unopened candidate. **AY-9.**

## 8. AY-7 — `0x0215F000` is the asset-category path directory

Section 6 found the manifest registered into a pointer array at `0x0215F000` and asked what that
array is. **It is the directory of every asset category the game loads** — 41 slots, each holding a
pointer to one category's path table.

| slot | category | slot | category |
|---:|---|---:|---|
| 0 | `PS2Data\cdi\<lang>\system.cnf` | 25 | `obj_finish/treasure` |
| **2**~~**, 8**~~ | ~~**the 40-entry battle manifest**~~ **the 82-entry battle manifest** (§11); slot 8 is an event-script path array, `plan_master\<lang>\event\…\*.ebp` / `.mot` *(corrected 2026-10-01, SWE2-STRUCT for OPUS, checks T5-T6)* | 26 | `plan_master/plan_map/area` |
| 4 | `plan_master/map_ctrl` | 27 | `sound/wave` |
| 5 | `plan_work/plan_map` | 28 | `movie_finish` |
| 10 | `effect_finish/common` | 30, 34 | `obj_finish/monster` |
| 11, 38 | `effect_finish/magic` | 31 | `sound/music/*.bgm` |
| 13 | `obj_finish/gadget` | 32 | `sound/se/block/*.seb` |
| 14 | `obj_finish/chara` | **33** | **`sound/shout/us/*.sab`** |
| 15, 20, 24 | `obj_finish/high/*` (high-detail variants) | 35 | `image/ff12/overlay` |
| 16 | `obj_finish/weapon` | **39** | **`sound/shout/jp/*.sab`** |
| 19 | `obj_finish/npc` | 22 | `obj_finish/bg_obj` |
| 23 | `obj_finish/summon` | | |

### Two registries, disjoint by construction

| | `0x0215F000` | `0x02EBF008` |
|---|---|---|
| slots | **41**, all filled | 63 |
| written by | `FUN_002DF9A0` only | various |
| **referencing functions** | **4** | **450** |
| all owners | `Resource` | many subsystems |

**No function in the image references both.** The 4 that touch `0x0215F000` are adjacent —
`002DF780`, `002DF880`, `002DF980`, `002DF9A0`.

> **They are not two views of one thing.** `0x0215F000` is a **private loader directory** — *where
> files live*, consulted by four Resource functions. `0x02EBF008` is the **public content registry** —
> *where parsed tables live*, consulted by 450 functions across every subsystem. **File paths in,
> parsed structures out.**

That also explains why AY-6 cannot be settled from this side: the loader directory has no reason to
know registry slot numbers, and it doesn't.

### AS-2 advanced: `ShoutAudioBank` is voice

[The RTTI object model](../../00-Engine-Core-Runtime/Object-Model/rtti-vtable-object-model.md)
recorded `ShoutAudioBank` / `ShoutAudioController` as a **lead** — a suggestive name for battle voice
lines, with the caveat that a name is not evidence. The path directory supplies the evidence:

```
slot 33   PS2Data\sound\shout\us\shout00\shout00.win.sab
slot 39   PS2Data\sound\shout\jp\shout00\shout00.win.sab
slot 32   PS2Data\sound\se\block\se000.seb          <- NOT per-language
slot 31   PS2Data\sound\music\data\music000.bgm     <- NOT per-language
```

**`shout` has one path table per language; sound effects and music have one each.** Localisation is
the discriminator: only recorded speech needs a separate table per language. **`shout` is voice**, and
the `.sab` extension puts it in `SQEX::Sd::SabFile`, matching the sound engine document.

~~**Still not established:** that it is specifically *battle* voice rather than all character speech.
The directory shows two shout tables, not what triggers them. **AS-2 remains open on that narrower
point.**~~ *Superseded 2026-09-26 (FABLE, Claude Opus 5.5).* AS-2 was answered on 2026-09-22 on
[the `.sab` container page](../../18-Audio/Sound-Bank-And-Voice-Formats/sab-sound-bank-container.md): it is battle
voice specifically, because every sample in the banks is named for a battle event. What triggers the load is now
read too (BD-1, [the bank family](../../18-Audio/Audio-Bank-And-Controller-Family/audio-bank-and-controller-family.md)):
the party read-in's voice-pack load step requests one member's bank from slot 33 and slot 39. Its completion
callbacks hand each buffer to the `ShoutAudioController`. Nothing else reads the two slots.

## 9. The runtime string resolver — and why the join was never going to be found

### The resolver

`FUN_002F9860` (low pool) and `FUN_002F9920` (high pool) turn a string id into text. Both are a
reciprocal divide, a **28-group bound**, and a fixed empty string on failure:

```asm
002F9866  mov   eax, 0x10624DD3      ; reciprocal of 1000
002F986D  imul  ecx
002F986F  sar   edx, 6               ; edx = id / 1000        <- the GROUP
002F9879  cmp   edx, 0x1C            ; 28 groups
002F987C  jl    ok
002F987E  lea   rax, [0x01CEB638]    ; OUT OF RANGE -> a fixed empty string
002F98A8  imul  eax, edx, 0xFFFFFC18 ; -1000  ->  index = id % 1000
002F989D  cmp   qword ptr [group table 0x02EC3D80 + group*8], 0
002F98B3  lea   rdi, [data table 0x02F973C0 + group*8]
002F98CF  call  ImageAddress_ResolveRuntimePointer
```

The high pool is the same shape with `0x68DB8BAD` / `sar 12` — divide by **10000** — and the same
`0x1C` bound. Entry is `cmp ecx, 100000`: below it the low pool, above it `id - 100000` into the high.

**It resolves through `ImageAddress_ResolveRuntimePointer`** — the same RVA-to-pointer conversion the
[authored data table registry](../authored-data-table-registry.md) documents. The two systems share
their addressing.

| pool | divisor | groups | domain |
|---|---:|---:|---|
| low | 1,000 | 28 | **0 – 27,999** |
| high | 10,000 | 28 | **100,000 – 379,999** |

### `help_action`'s ids are outside the domain

```
menu_command      10,000  ->  group 10   accepted
listhelp_action  100,000  ->  high pool, group 0   accepted
listhelp_status  120,000  ->  high pool, group 2   accepted
help_action       40,000  ->  group 40  >= 28   ->  REJECTED, returns the empty string
```

**`40,000–41,243` falls in the gap between the two pools** — above the low pool's 27,999 ceiling and
below the high pool's 100,000 floor. **This resolver can never return text for a `help_action` id.**

> ### ⚠ CONTRADICTED 2026-09-08 by a live read — the gap does not exist
>
> The group tables were read in a running process. **16 of 28 slots are populated, every one with
> magic `st2e`, 3,969 entries in total — and slot `n` holds ids beginning at exactly `n × 10,000`,
> 16 of 16.**
>
> **Slot 4 is populated and its first ids are `40000, 40100, 40101, 40102`** — precisely the
> `40000 + category*100 + slot` shape. So `help_action` ids **are** runtime string ids, `AY-10` is
> answered in the negative, and the paragraph above is wrong.
>
> **What survives:** every mechanical reading in this section — both reciprocal divides, the
> 28-group bound, the fixed empty string, both table addresses, the resolution through
> `ImageAddress_ResolveRuntimePointer`. **What did not survive is the inference built on top of
> them**, and it failed for a reason no re-reading of the code could have fixed: **the table's
> indexing is not in the code.** It is in the data, and the data exists only at runtime.
>
> ~~**It also puts the two divisors in tension.** Both resolvers read these same two tables — the
> displacements are identical in both bodies — and the table is ÷ 10,000-indexed, so
> `FUN_002F9860`'s ÷ 1,000 path cannot be indexing it correctly for any id ≥ 10,000. What that path
> serves is **left unresolved** rather than guessed.~~
>
> **Corrected 2026-09-15 (`OPUS-REQ-FABLE-ST2E-DIVISOR-NO-TENSION`, re-derived by FABLE): there is no tension.** The two
> resolvers share the presence table and the 28 bank descriptors, but they index different arrays inside a descriptor.
> - **`FUN_002F9860` (÷ 1,000) is positional.** It computes `slot = id − group × 1000`, bounds it by the descriptor's count
>   `[bank+0x04]` (`002F98C7`), then resolves `[bank+0x14]` and that block's `+4` table, and reads `[table + slot×4 + 4]`
>   (`002F98CC`–`002F98EF`).
> - **`FUN_002F9920` (÷ 10,000) is associative.** It never computes a slot. It loops `0 … count − 1` over the record array at
>   `[bank+0x0C]`, stepping by the `u16` stride at `[bank+0x08]`, and compares each record's first dword with the **whole**
>   id (`002F99B0`–`002F99F7`).
> - So bank `g` serves ids `g000`–`g999` by position **and** ids `g0000`–`g9999` by key. The ÷ 1,000 path is a second, correct
>   discipline over the same descriptor, not a mis-indexing. What the data puts in each array is still a runtime fact (above).
> [`EXP-002`](../../_experiments/EXP-002-st2e-group-tables.md).

### What that implies, and how far it can be taken

> ⚠ **Superseded 2026-09-08 (propagated 2026-09-11, ASTRA-REQ-FABLE-STALE-I6-AY10).** The lead below was contradicted by the live read
> in the box above: the ids are runtime string ids, slot 4 holds them, and no join to a dense
> `listhelp` index is needed. Kept as history; the paragraph that closes this section is struck.

> **LEAD, not established.** The `40000 + category*100 + slot` ids read as **authoring keys**, not
> runtime string ids. The runtime would reach descriptions through the **dense `listhelp` space**
> (100,000+, index = id − 100,000), which is exactly the form the high pool wants.

If that is right, **no field anywhere will ever carry a 40,000-range value** — which is consistent
with every scan run so far, and reframes the hunt from *"find the join to `help_action`"* to
*"find action id → `listhelp` index"*.

~~**It is not proven.** Settling it needs the group tables at `0x02EC3D80` and `0x02F973C0`, and those
are **null in the file and populated at load** — a live-memory question, not a static one.~~ **AY-10**
— settled 2026-09-08 by that live read, **in the negative**: the lead is withdrawn.

### `battle_pack.bin` is a superset pack

71 slots: **37 `st2e` tables**, 2 `word.bin`-style containers, 3 unknown, 29 empty. It **re-contains
files that also ship standalone** — block 14 is `action_data` (`count=543 rec=60`), block 61 is
`word.bin`, block 2 is `battle_message` — each with a 4-byte pad, plus roughly thirty tables with no
standalone file in the directory.
*Pointer 2026-10-01 (SWE2-STRUCT for OPUS), checks K1-K4: the three "unknown" sections are known formats.*
- Entry 0 is the WepJob matrix `{u16 stride 1, u16 count 23, u8 row[23]}`.
- Entry 39 is the shop table `{tag 0x64, stride 8, count 57, data 0xC}`.
- Entry 70 is a `licd` 24 × 24 licence grid ([its format](../../12-Items-Equipment-Shops-License/license-board-grid-format.md)).
- The two containers are entry 10 (`commandpack`, AY-4) and entry 61 (`word.bin`).

**Its container header does not carry a clean check**: the offset table ends at 292 while the first
offset is 296, and the last offset is 281,124 against a 281,128-byte file. **Two off-by-fours that
could have been explained away as alignment** — so the reading does not rest on them. It rests on the
sub-blocks carrying **`st2e` magic**, which announced itself when a first pass read the magic as a
count and printed `1697805427` = `0x65327473` = `"st2e"`.

### `action_data`'s `+0x34` — the identity with a dent

Recorded earlier as "a permutation of 0..542". **True but misleading.** It is the **identity for 528
of 543 records**, with a single contiguous disturbed window:

```
records 128..142 :  136 137 128 129 130 138 139 140 141 135 142 131 132 133 134
max displacement : 8      non-identity positions : 15 / 543
```

**One region, nothing else** — the shape of a late authoring edit inside one category, not a sort key.

### The join negative, now exhaustive — and a gap that was reported

Every **u8, u16 and u32** field at **every byte alignment**, in `action_data.bin` and in all 37 packed
tables, against three id sets. **Nothing resolves.**

**The earlier negative was weaker than it was presented**, and this is recorded because the analyst
said so: the first scan tested **u32 only**, and `40,000–41,243` fits in a **u16**. The gap is now
closed — u16 returns nothing either — but the earlier statement overclaimed its coverage.

Two pairings crossed 85 % and were **rejected as coincidence**: block 33 at 48/48 and block 35 at
104/109, both on **constant fields** where every non-zero value is the same number that happens to
lie in the id set. Same shape as the 238/411 declined previously.

## 12. `action_data.bin` is not what fills `0x02EBF138` — and it is not in nine languages (2026-09-12, FABLE)

**Two claims of section 3 are overturned; AY-6 and AY-5 close.**

**The binding, statically.** `BattleStorage_InitializeWorkArrays` requests loader id **`0x13`** with the
delivery callback `00238850` and the name `"STATIC"` (`002369BB`–`002369CE`). Loader ids are kind-2 path-array
positions — the same resolution that makes ids `0x47`–`0x52` the twelve `board_N.bin` files
([the registry page](../authored-data-table-registry.md) §M-7) — and position **19** of the manifest in section 6
is **`battle_pack`**; `action_data` is position 14. The callback stores the blob at `0208E680` and tail-jumps to
the binder `00236C30`, which loads `ecx = [blob + 0x3C]` and calls `00237FC0` (`00236D7B`–`00236D85`), and that
binder registers the header into **`0x02EBF138`** ([the row-lookup contract](../CONTRACT-authored-table-row-lookup.md) §7a). So the action
definition table is **`battle_pack.bin`'s directory entry `+0x3C`**, bound once at boot.

**The data agrees, and says more** ([census](../../_experiments/evidence/action-table-language-census/census.py), [output](../../_experiments/evidence/action-table-language-census/census.out.txt),
read-only over the archive). The name filter that lists `battle_pack.bin` in all nine language directories — the
positive control — lists `action_data.bin` in **four**: `ch`, `cn`, `in`, `kr`. There is no `us`, `de`, `es`, `fr` or
`it` copy. `battle_pack.bin`'s `+0x3C` section is an `st2e` table of 543 × 60 and is **byte-identical in all nine
languages**. The `ch` and `in` `action_data.bin` files equal it byte for byte, header included; `cn` and `kr` differ
in 15 bytes, each the `+0x34` name word of one row set to 0 (rows 104–110, 124, 128, 129, 133–136 and 138).

- ~~**It is per-language.** Nine directories~~ — the action table is **not localised**; four languages carry an
  extra standalone copy, which no loader is shown to read.
- ~~`action_data.bin` — the file behind registry slot `0x02EBF138`~~ — the slot is filled from `battle_pack.bin`.
  Section 3's field observations (count 543, stride 60, `+0x10`, `+0x12`) hold for both, because the rows are the
  same.

**Why the earlier reading was reachable.** Section 3 matched a count to a bound, which any identical copy
satisfies, and listed "nine directories" from the language set rather than from a per-file census. AY-6 was then
carried as an unproven binding for ten days while the binder that settles it was being decoded elsewhere.

**Still open from this page:** what, if anything, reads the four `action_data.bin` copies, and why `cn` / `kr` zero
fifteen name words.
*Answered 2026-10-01 (SWE2-STRUCT for OPUS), as far as the bytes go.*
- Nothing requests the copies by constant: slot 14 is one of the 40 in the UQ-73 note (checks Q1-Q6).
- So the game reads only the pack's section, which is identical in all nine languages. The fifteen words zeroed in
  `cn` / `kr` reach no reader.
- Why the authors zeroed them is authoring history the shipped data does not record, like the unnamed slot 40
  (UQ-73).

## 11. Falsification pass 7 — 2026-09-02 (repos-d2, independent)

**Program state.** Parent `2ed8affb…`, snapshot `46f02e26…`, embedded EXE `73461d08…`,
ledger 38,161 / 38,003 / 158. `Verify-GfzCheckpoint.ps1` — `CHECKPOINT VERIFIED` in project
`proj_hd2` / `GFZ_HD2` before any reading.

**Why this pass could reach further than the previous six.** They were run by the document's own
author against its own reasoning. This one was run by a session that had independently built the
VBF extraction corpus for unrelated work, so the archive claims could be **re-measured from the
archive** rather than re-read, and the binary claims re-derived with a capstone census over all
**38,161** ledger bodies — a wider population than the **34,270** section 5 states it scanned.

### The kill: section 6's completeness claim

**Was believed.** *"Forty path pointers in a fixed order, repeated per language… **This is the
complete authored-data table set**."*

**Now believed.** The region is **82 path entries**, slots 0..82 of the pool at `0x01E4D830`, with a
single interior NULL at slot 40 and a double NULL at 83/84 closing it.

**What proved it, three ways.**

1. **Direct read of the pool.** Slot 40 is NULL; slot 41 is `attribute_data.bin` and the entries
   continue unbroken through slot 82 (`board_12.bin`).
2. **The loader's own boundaries.** `FUN_002DF9A0` forms exactly **five** `lea` targets into this
   pool — slots **0, 84, 128, 450 and 1640**. The next base it registers after slot 0 is
   slot **84**, not 40. *The forty-entry boundary is not a boundary the loader recognises.*
3. **The per-language blocks reproduce the same shape.** The `ch` block at `0x01E6BB40` carries the
   identical layout: `WepJob_Matrix` at 0, `action_data` at 14, `shop_data` at 39, **NULL at 40**,
   `attribute_data` at 41, `listhelp_action` at 47, `word.bin` at 61, `board_12` at 82, NULL at 83
   and 84. The interior NULL is **authored and repeated**, not incidental to one block.

**The document contradicted itself and the contradiction went unread for six passes.** Five files it
analyses in detail are outside the set it calls complete:

| file | pool slot | where this document uses it |
|---|---:|---|
| `attribute_data.bin` | 41 | §2 — one of the three header-arithmetic verifications |
| `listhelp_action.bin` | 47 | §2 table; §4 *"the missing half"*; §9 resolver (100,000 ids) |
| `listhelp_status.bin` | 49 | §9 resolver (120,000 ids) |
| `ability_data.bin` | 58 | §2 — a second header-arithmetic verification |
| `word.bin` | 61 | the whole of §7 |

**Why the earlier reading was reachable, and the transferable lesson.** A NULL in a pointer array
reads as a terminator, and reading it that way produced a list that was *entirely correct as far as
it went* — forty real paths in the right order. **A truncation that is correct on every element
it contains looks exactly like a complete list**; nothing inside the forty is wrong, so no
inconsistency surfaces while checking them. What exposes it is not re-reading the array but asking
**what the consumer treats as the boundary** — and the consumer's own `lea` targets say 84.
*Do not infer an array's extent from its contents when the code that walks it is available.*

### What survived, and what the attack could not break

| Claim | How it was attacked | Result |
|---|---|---|
| Archive: 31,196,932,183 B, `SRYK`, **89,414** entries | index re-parsed from `FFXII_TZA.vbf` independently | **SURVIVED, exactly.** |
| `gamedata` 39,653 / `ps2data` 39,578 / `prefetchdata` 9,351 / `jsondata` 832 | recounted; they sum to 89,414 with no remainder | **SURVIVED, all four.** |
| Extension census `.phyre` 35,984, `.txt` 10,253, `.ebp` 10,045, `.sab` 4,609, `.mot` 4,392, `.efx` 3,288 | recounted from the index | **SURVIVED, all six.** |
| §5: the two `action_data.bin` path literals exist at `00A42148` / `00C1BFF8` | bytes read at those VAs | **SURVIVED.** Both present, exact. |
| §5: **nothing in `.text` references them** | re-run over **38,161** bodies (not 34,270), 1,786,589 instructions, covering RIP-relative operands **and** `movabs` immediates — a wider form than the `lea`-target scan | **SURVIVED, on a wider population and a wider instruction form.** |
| §6: the forty entries and their order | every pointer resolved and compared name by name | **SURVIVED.** All forty correct, in order, `action_data` at 14. |
| §6: *repeated per language* | the `ch` block located and walked | **SURVIVED.** |
| §8: **no function references both registries** | full census over 38,161 bodies | **SURVIVED.** Intersection empty. |
| §9: resolver constants `0x10624DD3` / `sar 6` / `cmp 0x1C` / `imul -1000`, and `0x68DB8BAD` / `cmp 0x1C` | re-disassembled | **SURVIVED, byte for byte.** |

### The positive control section 5 did not have

Section 5's *"a scan finds **zero** references"* is an absence claim, and **a zero from an
instrument that cannot fire looks identical to a real zero.** No control was recorded. One was run
here: the same query, in the same run, against `009146B8` — the `btlKeepCharWork1` tag string,
known referenced from `BattleStorage_InitializeWorkArrays`.

```
00A42148  action_data path (in)                  0 code references
00C1BFF8  action_data path (ch)                  0 code references
009146B8  CONTROL: btlKeepCharWork1              1 code reference   lea rdx,[rip+0x6ddd66]  @ 0023694B
```

**The instrument fires on exactly the form the absence rests on.** The absence is real.

It is also **shape-checked**, which a bare control would not give: the two paths carry **6 and 3
pointer references from `.data`** and zero from code; the control string carries **one from code and
zero from data**. They are opposites, and the pointer at `0x01E4D8A0` is pool slot **14** — an
independent confirmation of both the pool base and `action_data`'s index, arrived at from the string
rather than from the array.

### A miscount of my own, chased rather than reported

My first census returned **3** functions referencing the `0x0215F000` directory against the
document's **4**, and 449 against 450. Rather than report a disagreement, I checked the missing one:
`FUN_002DF780` forms `lea rax,[rip+0x1E7F7E5]` — **`0x0215EFF4`, twelve bytes below the base I
had scanned from**. The document's count of 4 is right; my window was too narrow, and the same edge
explains the off-by-one at the other registry. **A count disagreement is a question about two
populations before it is a finding about either.** Recorded because the near-miss is the useful part:
those twelve bytes are an unread header on the directory (**PROPOSED-reposd2-9**).

### What was tried and did not break anything

- **Tried to break the archive figures by recounting from the index rather than the extracted
  tree.** Every one of the eleven published counts reproduced, and the four top-level counts sum to
  the entry total exactly — an internal check the document did not claim but passes.
- **Tried to widen section 5's absence into a false negative** by adding `movabs`-immediate forms
  and 3,891 more function bodies than it scanned. Still zero.
- **Tried to make the two registries overlap** by scanning both address windows across every body.
  Empty intersection; the disjointness is the document's load-bearing claim in section 8 and it
  holds.
- **Checked for banned evidence in the citation chain.** No `.pdata`, `.xdata`, unwind, EH map or
  `_IMAGE_RUNTIME_FUNCTION_ENTRY` reasoning appears in this pass. Address adjacency was available
  and refused: the 82-entry extent is asserted from the **loader's registered bases**, never from the
  entries being neighbours.

### Reopening propagation

- **This document reopens** on the section 6 correction. Sections 1, 5, 8 and 9 were attacked and
  held; sections 2, 3, 4, 7 and 10 were not re-attacked in this pass.
- [`../authored-data-table-registry.md`](../authored-data-table-registry.md) should be checked
  against the corrected extent: if it cites *"40 authored tables"* from here, it inherits the error.
- **AY-6 is unaffected.** The binding of `action_data.bin` to registry slot `0x02EBF138` rests on
  the path literal and the count match, neither of which this pass disturbed, and the two-registry
  disjointness that explains why it cannot be settled from the loader side survived.
  *(Pointer 2026-10-01 (SWE2-STRUCT for OPUS): AY-6 was answered the other way on 2026-09-12. The slot is bound from
  `battle_pack.bin`, §12.)*

## 10. Testing the reframe statically — the test has no discriminating power

Section 9's lead says the runtime reaches descriptions through the **dense `listhelp` space**
(index = id − 100,000), not the `40000`-range authoring keys. **That is testable without the live
group tables**, and the test is one nobody had run: every previous scan looked for the *id sets*
(40,000-range, `cat*100+slot`, 100,000-range). **A dense index is invisible to all of them** — it
holds values `0..250`, not six-figure ids.

Run against all 543 records, every `u8` and `u16` field at every alignment, requiring ≥95 % of
non-zero values below 251 and ≥30 distinct:

```
+0x08 u8   470 non-zero  100%  89 distinct      +0x00 u8   542  99%  194 distinct
+0x10 u8   301 non-zero  100%  91 distinct      +0x34 u8   540  98%  255 distinct
+0x2E u8   200 non-zero   98% 200 distinct      +0x30 u8   185  99%  116 distinct
```

**Every hit is a `u8`, and no `u16` field qualifies at all.**

### Why that settles nothing

**A byte satisfies "below 251" for 98 % of its range by construction.** Eight `u8` fields passing a
`< 251` test is what a 60-byte record full of small counters looks like — it is not evidence of an
index into a 251-entry table. **The test cannot distinguish the hypothesis from the null.**

Two of the hits illustrate it: `+0x34` is the record index
(section 9 — the identity with a dent), read as a byte it saturates at 255; and `+0x2E` is the low
byte of a `u32` counter running 10000, 10001, 10002…, which produces 200 distinct values for reasons
that have nothing to do with descriptions.

**The one informative part is the negative:** **no `u16` field holds a dense `0..250` index.** If the
join were stored at 16 bits it would have shown here. So either it is a single byte — indistinguishable
by range from every other byte in the record — or it is not in `action_data` at all.

### What this means for AY-10

**The reframe cannot be confirmed or refuted from `action_data`'s fields**, and the reason is
structural rather than a gap in effort: a 0..250 index fits in a byte, and the record is full of
bytes. Closing it needs a discriminator this file does not contain — the category assignment of each
action, which is the very thing the join would supply.

**AY-10 therefore genuinely requires the group tables at `0x02EC3D80` / `0x02F973C0`**, which are null
in the file and populated at load. **This pass rules out the cheap static route rather than leaving it
untried**, which is the useful outcome: the live read is not a first resort here, it is what remains.

**Done since (propagated 2026-09-11, ASTRA-REQ-FABLE-STALE-I6-AY10):** the live read happened on 2026-09-08 and answered `AY-10` in the
negative (section 9's contradiction box; [`EXP-002`](../../_experiments/EXP-002-st2e-group-tables.md)).
This section's negative stands; its "what remains" has been carried out.

## 13. What the code asks for by constant — 2026-09-13 (FABLE)

§8 names the directory. This section names the **callers** that ask it for a fixed file. The census
([`members/res_request_census.py`](members/res_request_census.py) → [`members/constant-resource-requests.tsv`](members/constant-resource-requests.tsv))
takes every direct `E8`/`E9` site of the request API, in two conventions:

- the pool family `00249210` / `002493D0` / `00249350` / `00249180`, with `edx` = kind and `r8d` = id;
- the path family `0032E400` (size) / `0032E620` (request) / `0032E3F0`, with `ecx` = kind and `edx` = id.

It tracks register constants through the calling body (`mov r, imm`, `xor r, r`, `lea r, [r' + imm]`, register copies; a
call clears the volatile registers). When the kind or id at the call is still the function's own entry argument, it goes
**one hop further** and reads the constants at each direct caller of that function. The file is then resolved through
`0215F000[kind]` as `002DF9A0` first fills it, from `rax` or `rcx` stores alike (41 slots). One site can yield several
rows, one per constant caller:

| | rows |
|---|---:|
| rows (182 direct sites, expanded per constant caller) | **238** |
| resolved to a file | **147** |
| … of them through a caller one hop up | 66 |
| constant, but the kind has no directory entry | 2 |
| kind or id not constant within one hop | **89** |

**The unresolved rows are the census's blind spot, by construction.** Values that arrive from further up, from memory or
from tables are not followed, so a file absent from this table is not a file nobody loads. That runtime question stays
with ASTRA's AQ-14. **Control:** the map-data widget's loader `003BC2D0` resolves to `menumap_world` / `_location` /
`_common` exactly as read on the [lmap page](../PS2-Image-Data-Formats/lmap-menumap-location-graph.md) §10.1.

**One identity this settles:** kind 9 id 4 is **`map_ref.bin`**. `00268750` sizes it (`00268762`), stores the allocation
in `02099D88` (`002687CF`), and requests the file into it (`00268809`) with the completion callback
`MapRef_OnPrimaryResourceLoaded` (`002687A4`). That global is the map-reference table the
[field-environment page](../../03-World-Area-Field/choosing-the-field-environment-variant.md) reads, whose file was not named.

| loader | files requested by constant (kind id, call site; `via` = the wrapper that makes the request) |
|---|---|
| `002467A0` | `texpack_ys.bin` (0x7 0xd6, `00246887`) |
| `00253780` | `menumap_area.bin` (0x7 0xa5, `00253928`) |
| `00259DF0` | `behindcamera.bin` (0x9 0x3, `00259DFE`) |
| `00268750` | `map_ref.bin` (0x9 0x4, `00268762`); `test_area_ref.bin` (0x9 0x2, `00268814`) |
| `00280750` | `tex2pack_ys.bin` (0x7 0xd7, `00280861`) |
| `002808D0` | `mrppack_ys.bin` (0x7 0xd3, `0028090A`); `clutpack_ys.bin` (0x7 0xd4, `00280951`) |
| `00291C80` | `itemgra_c.tm2` (0x7 0x98, `00291CD2` via `0024AB90`) |
| `0029CED0` | `fontcolor.bin` (0x7 0x5, `0029CEF6`) |
| `0029DC90` | `key_signal_data.bin` (0x7 0x24, `0029DCBF`) |
| `002C8EE0` | `monotone_chr.bin` (0x7 0x74, `002C8F2F` via `0024AB90`) |
| `002CBD50` | `Shop_8_c.tm2` (0x7 0x63, `002CBD85` via `002493D0`) |
| `002D6EE0` | `Tuto_win_c.tm2` (0x7 0xd8, `002D6F59` via `00249380`) |
| `002E60F0` | `se000.seb` (0x20 0x0, `002E61A8`) |
| `003158B0` | `menuhandbook.bin` (0x7 0xc8, `003158F8`) |
| `00324510` | `tst_a.nmb` (0x1a 0x0, `00324637`) |
| `0032F430` | `pre_z0000.ebp` (0x8 0x350, `0032F670`) |
| `0035C5B0` | `menubtlwndinfo.bin` (0x7 0x25, `0035C5D7`); `mini_guest_face.bin` (0x7 0xd, `0035C604`) |
| `00360C70` | `musicinfo.bin` (0x9 0x6, `00360CA9`) |
| `003658F0` | `fontpack_fs.bin` (0x7 0xd2, `00365935`) |
| `00378540` | `planmapname.bin` (0x1 0x20, `00378566`); `navimapdata.bin` (0x9 0x8, `003785FA`); `gramap_weatherinfo.bin` (0x9 0x27, `00378673`); `mapjumpgroupflagrom.bin` (0x9 0xa, `0037870A`); `mapjumpgroupinit.bin` (0x9 0x28, `0037877C`); `eventmemorylist.bin` (0x9 0x29, `003787EE`); `soundfoottable.bin` (0x9 0x9, `0037884D`) |
| `00379E90` | `eventvib.bin` (0x9 0x7, `00379E9E`) |
| `0037F4D0` | `menuquest.dat` (0x7 0x128, `0037F740`); `menuquest.lst` (0x7 0x13a, `0037F76F`) |
| `00393FF0` | `title.mrp` (0x7 0x3a, `00394048` via `00249320`); `title_logo.tm2` (0x7 0x3d, `00394029` via `002493D0`) |
| `0039C3F0` | `fontpack_it.bin` (0x7 0xd5, `0039C432`) |
| `003B0660` | `c_all.efx` (0xa 0x0, `003B06E5`) |
| `003B53C0` | `summoneffectdata.bin` (0x9 0x2a, `003B5407`) |
| `003BC2D0` | `menumap_world.bin` (0x7 0xa2, `003BC312`); `menumap_location.bin` (0x7 0xa3, `003BC340`); `menumap_common.bin` (0x7 0xa4, `003BC36A`) |
| `003DCBC0` | `pc_skillmotion.bin` (0x9 0x5, `003DCC59`) |
| `003EAB60` | `musicctrl.bin` (0x9 0x20, `003EAB73` via `0051ED10`) |
| `003EAC40` | `npcdic.bin` (0x9 0x1f, `003EAC53` via `0051ED10`) |
| `003F4840` | `shop_new.mrp` (0x7 0x96, `003F492D` via `00249320`) |
| `00404060` | `Loca.mrp` (0x7 0xbf, `00404107` via `00249320`); `Loca_8_c.tm2` (0x7 0xb9, `00404093` via `002493D0`); `LocaBack_c.tm2` (0x7 0xba, `004040C2` via `002493D0`); `w_line01.tm2` (0x7 0xb0, `004040F0` via `002493D0`) |
| `00473D20` | `questbase.bin` (0x9 0x21, `00473D33` via `0051ED10`) |
| `0053EB90` | `sf_logo_c.tm2` (0x7 0x47, `0053ECDF` via `002493D0`) |
| `00556500` | `lic_4_c.tm2` (0x7 0x79, `00556541` via `002493D0`) |
| `00558FB0` | `lic_B_4_c.tm2` (0x7 0x77, `0055926E` via `002493D0`); `Maru_c.tm2` (0x7 0x70, `0055929E` via `002493D0`); `Maru_c_2.tm2` (0x7 0x71, `005592CE` via `002493D0`); `lic_B_8_c.tm2` (0x7 0x76, `005592FE` via `002493D0`) |
| `00561390` | `Lic_Bk.tm2` (0x7 0x7a, `0056169E` via `002493D0`); `cm2_win_c.tm2` (0x7 0x2b, `005616CE` via `002493D0`); `lic_8_c.tm2` (0x7 0x78, `005616FE` via `002493D0`); `lic_8_c2.tm2` (0x7 0x7c, `0056172E` via `002493D0`); `lic_8_c3.tm2` (0x7 0x7d, `0056175E` via `002493D0`); `meshdata.mg` (0x7 0xa8, `0056163B`); `license_chip.bin` (0x7 0x7e, `00561663`) |
| `00562F90` | `w_menu.mrp` (0x7 0xa6, `00563048` via `00249350`); `w_shade_p.tm2` (0x7 0xaa, `0056301F` via `002493D0`); `meshdata.mg` (0x7 0xa8, `00562FC6`) |
| `0056F2A0` | `HandBack2_c.tm2` (0x7 0xd0, `0056F39B` via `002493D0`) |
| `00572D80` | `menuhandbook_order.bin` (0x7 0xc9, `00572DEB`) |
| `00576F50` | `menuquest.dat` (0x7 0x128, `00577057`) |
| `00582790` | `icon.sys` (0x7 0x2c, `005827FE`); `icon1.ico` (0x7 0x2d, `00582826`) |

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver / encoder fan-out is MECHANICAL.*

**ActorEntity, Presentation and Script_VM_Native_Bridge — CLIENT.** The path family `0032E400` (size) / `0032E620` (request) is also issued by `ActorResource_BeginPrimaryPayloadLoad`, `ActorResource_BeginManagerResourceSetLoad` and a 3,882-byte actor loader, by two Presentation bodies (119 B and 337 B) and by script-verb bodies (75 B and 115 B). The 177-byte Input-filed item-graphics loader is another client.

- **ActorEntity — CLIENT.** `0032E3F0` (`"TkFileGetFilename.IlligalFunction"`, 8 B) is called by the 3,882-byte actor
  loader. `002DF980` is called by `ActorResource_BeginManagerResourceSetLoad`.
- **Presentation — CLIENT and SERVICE.** The `summoneffectdata.bin` loader `003B53C0` is called by
  `CharacterRenderSystem_Initialize`. The `c_all.efx` loader `003B0660` calls a 1,934-byte body. `002DF980` is read by a
  1,636-byte body.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — CLIENT.** `ResourcePath_Init` and two other cited Resource bodies are called from the core start-up subtree's root, and a table body is called by `MainLoop_UpdateAndRenderFrame` and two core frame bodies. The archive's tables are installed at core start-up and consulted per frame.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Input — CLIENT.** `FUN_00291c80`, owned by that layer, calls `0024AB90` on this page. That caller is a 177-byte walk of the table at `0209BEA0`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).
- **Audio — SERVICE (1 edge).** 1 outbound (page-cited `002E60F0` call Audio bodies `003A1650`). Substantive edges include `002E60F0` calls `003A1650`.
- **CombatAI — CLIENT and SERVICE (2 edges).** 1 inbound (CombatAI bodies `GambitTargetDefinition_BindAndBuildMenuLookup` (00238880) call page-cited `AreaData_BindAndRebaseSectionDescriptor` (003845F0)); 1 outbound (page-cited `00236C30` call CombatAI bodies `GambitTargetDefinition_BindAndBuildMenuLookup` (00238880)). Substantive edges include `00236C30` calls `GambitTargetDefinition_BindAndBuildMenuLookup` (00238880); the remaining edges run through shared helpers the page cites.
- **CombatAction — CLIENT and SERVICE (2 edges).** 1 inbound (CombatAction bodies `00237FC0` call page-cited `AreaData_BindAndRebaseSectionDescriptor` (003845F0)); 1 outbound (page-cited `00236C30` call CombatAction bodies `00237FC0`). Substantive edges include `00236C30` calls `00237FC0`; the remaining edges run through shared helpers the page cites.
- **Items — SERVICE (1 edge).** 1 outbound (page-cited `00236C30` call Items bodies `00238660`). Substantive edges include `00236C30` calls `00238660`.
- **SaveLoad — CLIENT (1 edge).** 1 inbound (SaveLoad bodies `00582790` call page-cited `00249210`). Substantive edges include `00249210` is called by `00582790`.
- **Save_Load_Settings — CLIENT (2 edges).** 2 inbound (Save_Load_Settings bodies `002EF300`, `SaveLoad_ControllerLifecycleHandler` (00582860) call page-cited `0032E620`, `00582790`). Substantive edges include `0032E620` is called by `002EF300`; `00582790` is called by `SaveLoad_ControllerLifecycleHandler` (00582860).
- **UI — CLIENT and SERVICE (32 edges).** 20 inbound (UI bodies `00253780`, `00562F90`, `00561390` call page-cited `00249210`, `002493D0`, `00249180`); 12 outbound (page-cited `00558FB0`, `00561390`, `00253780` call UI bodies `00291D70`, `00291D80`, `0035C630`). Substantive edges include `002467A0` is called by `00253780`; `00249180` is called by `0035C5B0`; `00249180` is called by `00253780`; `00249210` is called by `00561390`; the remaining edges run through shared helpers the page cites.
- **World — CLIENT and SERVICE (9 edges).** 8 inbound (World bodies `00266D10`, `00378540`, `003847B0` call page-cited `AreaData_BindAndRebaseSectionDescriptor` (003845F0), `MapRef_BeginLoadResources` (00268750), `0032E400`); 1 outbound (page-cited `00236C30` call World bodies `003847B0`). Substantive edges include `00236C30` calls `003847B0`; `MapRef_BeginLoadResources` (00268750) is called by `00266D10`; `0032E400` is called by `00378540`; `0032E620` is called by `00378540`; the remaining edges run through shared helpers the page cites.
- **WorldAreaField — CLIENT and SERVICE (28 edges).** 19 inbound (WorldAreaField bodies `00236C30`, `00379A10`, `003319D0` call page-cited `0032E400`, `0032E620`, `002F9920`); 9 outbound (page-cited `00236C30`, `00238850`, `00237FC0` call WorldAreaField bodies `AreaData_BindAndRebaseSectionDescriptor` (003845F0), `003846F0`, `00236C30`). Substantive edges include `00236C30` is called by `00238850`; `00236C30` calls `003846F0`; `00237FC0` is called by `00236C30`; `00238160` is called by `00236C30`; the remaining edges run through shared helpers the page cites.

## Falsification pass 2026-10-01 (SWE2-STRUCT for OPUS)

*Run by a Claude session in the SWE2-STRUCT lane for OPUS, a non-author of this page. Record and checker:
[`swe2struct-reopened3-0930`](../../_index/candidates/swe2struct-reopened3-0930/README.md),
[`p1_vbf_st2e.py`](../../_index/candidates/swe2struct-reopened3-0930/p1_vbf_st2e.py) (34 checks, FAILS 0).*

**Attack chosen: §2's `St2eHeader` struct.** It is the page's most load-bearing claim, for three reasons:
- the front matter's `st2e` format row rests on it;
- every authored-table reader in this database decodes through it;
- pass 7 (§11) did not re-attack §2.

The struct states a value for every field: `headerSize` 32, the heap rule, and *"0 in all 407 shipped files"* for
three words. The killer looked for was one shipped file that breaks any field's comment.

**Method.** Every `.bin` entry of `FFXII_TZA.vbf` (1,439) was decompressed from the archive index, and the 407 that
begin with `st2e` were kept: 73 names, all under `test_battle/<lang>/binaryfile`. Each header was compared, field by
field, with the struct. **Positive control:** the page's own length rows reproduce exactly. They are
`action_data` 32,612 = 32 + 543 × 60, `ability_data` and `attribute_data`, plus the five string-table rows.

**Result: CORRECTED.** Four of the struct's comments were false, and they are struck in §2.

| field | the struct said | measured over 407 | checks |
|---|---|---|---|
| `+0x0C` `headerSize` | 32 | 32 in 393; **0 in 14**, each with `count * recordSize == 0` (12 empty-table copies, 2 `mons_act.bin`) | H4, H9 |
| `+0x10` | 0 in all 407 | **0 in all 407 (survives)** | H1 |
| `+0x14` `heapOffset` | `headerSize + count * recordSize`, or 0 | that value in 255, 0 in 150, **`0x20` in the 2 `mons_act.bin` copies**; the heap's `one` word is 1 in all 257 | H5, H6 |
| `+0x18` | 0 in all 407 | **`0x7144` in the 4 `eitm_data.bin` copies**, the record-array end | H2 |
| `+0x1C` | 0 in all 407 | **`0x98` in the 4 `tutorial_data.bin` copies**, the record-array end | H3 |

**Why it was reachable.** The AY-3 answer of 2026-09-15 made the same claim, and FABLE corrected it the same day in
the *Open questions* box. That correction was never carried up to the struct in §2, so the page contradicted itself.
The struct also attached reserved names to two live words.

### The reopening trigger is resolved (SWE2-STRUCT for OPUS)

This page reopened on pass 7's correction of §6: the manifest has 82 entries, not 40. The correction is in place in
§6 (the OVERTURNED box, and "82 of them"), and it re-measures exactly from the image (checks T1-T4):
- **The entries.** The pool `01E4D830` is NULL in slots 0-84 only at 40, 83 and 84.
- **The slot names.** The ones §11 places are where it says (slots 0, 14, 19, 39, 41, 47, 49, 58, 61 and 82).
- **The `ch` block.** At `01E6BB40` it has the same names and the same NULLs.
- **The loader.** `002DF9A0` forms pool `lea`s at slots 0, 84, 128, 450 and 1640 only.

**One consumer of the old extent was still on this page.** §8's directory table had a row *"2, 8: the 40-entry
battle manifest"*. That row is corrected twice:
- the manifest has 82 entries;
- in all ten language arms of `002DF9A0`, slot 8 receives an event-script path array, not the manifest (T5, T6).

The other consumer pass 7 named, [the registry page](../authored-data-table-registry.md), cites no 40-table extent.

### What else the attack settled (SWE2-STRUCT for OPUS)

- **The lede is corrected.** It still said `action_data.bin` is the file behind the action definition table. §12
  overturned that on 2026-09-12, and the lede now says so. §3's *"very probably the file that fills it"* is
  corrected the same way.
- **The three "unknown" sections in §9 are three known formats** (K1-K4): the WepJob matrix (entry 0), the shop table
  (entry 39) and a `licd` licence grid (entry 70).
- **The 40 standalone copies.** Four directories ship copies of 40 packed slots, `action_data.bin` and
  `commandpack.bin` among them. No request by constant reaches any of them (Q1-Q6). The kind-2 loader's three callers
  take `0x13`, `0x47 + n` and the localised slots in `01E09F68`.
  - Over all 122,250 call sites, no direct call to a request API carries `(2, k)` for any of the 40.
  - The census's control (`MapRef`, `00268762`, kind 9 id 4) is reported.
  - The three register calls that carry such a pair do not reach a request API.

**What this pass did not attack:** §1's archive figures (pass 7 re-measured them), §7's charset and §9's resolver
bytes (pass 7), and §13's request census.
