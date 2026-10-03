---
system: The `CHSE` per-class tables — charseinfo_*.bin
category: 02-Resource-And-Asset-Pipeline
status: DOCUMENTED — every register row is closed (owner re-status 2026-09-30, OPUS, on SWE2-CONTRACT's reconciliation; superseded readings are marked on the page) — SB-2 answered (FABLE 2026-09-25, the reader section); the Audio helper 003A1650 is the SE block registration (seb-se-block-index.md §3.2); slot 3 answered (the actor's fallback pack key, read by 002ED910) and the header fields shown unread, both by SWE2-CONTRACT's record swe2contract-ddres-b5-0930; nothing registered open (status line current 2026-09-30, SWE2-CONTRACT)
owner_layer: CodeDomain:Presentation.Audio
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  parent_tag: GN160
corpus_validated: "16 of 16 files (8 units x 2 locales), all 943 records walked, 2026-09-06"
container_format: chse
last_reviewed: 2026-09-30
archive_formats:
  - "CHSE | explained | charseinfo_[bcgmnstw].bin (.bin member, 8 units): size = 16 + count*16 layout, section 2; loader 002EA530 (kind 9, 0x0B + i) into 021641A0 + 8i and the reader traced in 'The reader, traced - SB-2 answered'"
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-chse-pass-1 - corpus re-walked from the archive and exact; slots 0-2 are SE block ids (943/943 in the shipped .seb set, slot 3 the failing control); slot 3 range corrected to 0x0000-0x003F; filed as a candidate for SB-2, not closed
  crossref_clean: false
  reopened_count: 0
---

# The `CHSE` per-class tables — `charseinfo_*.bin`

> **Eight small tables, one per character-class letter, each a flat array of four-slot records.**
> The layout is completely established; what the four slots select is not, and the name is the only
> evidence for it — which in this folder is not enough.

**Corpus validation, before anything else.**

| | |
|---|---|
| files | **16** — 8 units x 2 locale copies |
| units | `charseinfo_` **`b c g m n s t w`** |
| locales | **`ch` and `in` only** — no other locale ships one |
| copies byte-identical | **8 / 8 units** |
| `16 + count * 16 == size` | **8 / 8** |
| records | **943**, every one walked |

---

## 1. What the player sees

**Nothing directly, and the honest version of what it causes is short.** These are eight small
lookup tables the game consults for a character class — `charseinfo` reads as *character SE info*,
and **SE** is the standard Japanese game-development abbreviation for *sound effect*. If that is
right, this is where a class's sounds are assigned.

**That reading rests entirely on the filename, and this folder has already been burned twice by
name-driven guesses** — its README records `.lst` assumed to be a build artefact (it is quest menu
data) and `.ico` assumed to be a PS2 icon (it is a Windows ICO). **So this sheet documents the
structure and does not assert the purpose.** §7 says so plainly.

What *is* certain and is worth a modder's attention: **three of the eight tables are completely
empty** — every record in `charseinfo_b`, `_g` and `_t` is the empty pattern. Whatever these
assign, three classes have none of it.

## 2. The layout

```struct ChseHeader base=file size=0x10
+0x00  char[4]  magic    'CHSE' - 43 48 53 45, in 8 of 8
+0x04  u16      version  1 in 8 of 8
+0x06  u16      letter   the ASCII letter of the filename, in 8 of 8
+0x08  u32      count    16 .. 327
+0x0C  u32      _zero0   0 in 8 of 8
```

**`+0x06` carries the filename's own letter**: `charseinfo_b` holds `0x62` (`'b'`), `_c` holds
`0x63`, through to `_w` holding `0x77`. **Eight of eight.** The file identifies its own class rather
than relying on the path — so a renamed file still declares which class it belongs to.

```struct ChseRecord base=record size=0x10
+0x00  u16  slot0    0xFFFF = empty
+0x02  u16  slot1    0xFFFF = empty
+0x04  u16  slot2    0xFFFF = empty
+0x06  u16  slot3    0xFFFF = empty
+0x08  u32  _zero0   0 in all 943 records
+0x0C  u32  _zero1   0 in all 943 records
```

**`16 + count * 16` is the whole file in 8 of 8** — no header slack and no tail.

**Half the record is reserved.** The last eight bytes are zero in **943 of 943** records, so a
record carries four `u16` slots in a sixteen-byte cell. That is a measured invariant, not an
inference from one file.

## 3. The loader contract

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| `+0x00` magic | — | **never** | — | **yes** — `CHSE` occurs **0 times in the image**, as ASCII or as the dword `0x45534843` |
| everything else | — | — | — | **no reader found — see below** |

**The contract rebuilt from the traced reader (2026-09-30, SWE2-CONTRACT; [`swe2contract-ddres-b5-0930`](../../_index/candidates/swe2contract-ddres-b5-0930/README.md), [`chse_slot3.py`](../../_index/candidates/swe2contract-ddres-b5-0930/chse_slot3.py) T1–T11).** It supersedes the
table's last row. The only code that takes the eight table pointers is the loader `002EA530` (one `lea` of the base)
and the row reader `002ED950` (T1); the loader reads no field of the buffer (T11).

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| `+0x00` magic | — | never | — | yes (unchanged) |
| `+0x04` version, `+0x06` letter, `+0x0C` | — | never | — | yes — no code that reaches the tables reads them (T1, T11) |
| `+0x08` count | `002ED950` (`002ED9C2`) | row `>=` count → null | — | no |
| row `+0x00` / `+0x02` / `+0x04`, slots 0–2 | `002E60F0` (`002E6157`, `u16` at `+2·pass`) | bit 15 set → no SE block (`js`) | — | no |
| row `+0x06`, slot 3 | `002ED910` (`002ED939`, signed) | — | — | no — the fallback pack key, §7 |
| row `+0x08` .. `+0x0F` | — | — | — | yes — no caller of `002ED950` reads past `+0x06` (T4) |

Rows are 0-based after the 16-byte header: `002ED950` returns `table + 16·(row + 1)` (T2).

**Located by hardcoded path.** Sixteen path strings ship in `.rdata`, e.g.
`…\ff12\in\common\charseinfo_b.bin` at `0x00956C55` — **eight letters, two locales, sixteen
strings**, matching the shipped file count exactly. As with every other `.bin` format examined this
round, the file is found by a compile-time path and its magic is never compared.

~~**What parses the records was not found**~~ **The reader is found (2026-09-25, FABLE, Claude Opus 5.5): see
[§ The reader, traced](#the-reader-traced--sb-2-answered-fable-claude-opus-55-2026-09-25).** *History:* the search that failed is the one already documented
in [`sloc`](sloc-menumap-container.md) §3: the per-locale path table is populated once at boot by
`FUN_002DF9A0`, and its consumers are reached by argument or accessor, which an address-based scan
cannot follow. **Status is `PARTIAL` for that reason** and no `Inert` row is claimed for any field
but the magic.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `0x00956C55` | the `charseinfo_b.bin` path string (`in` locale) | data |
| `0x002DF9A0` | populates the per-locale path table that locates these files | partial — established in [`licd`](../../12-Items-Equipment-Shops-License/license-board-grid-format.md) §3 |

~~**No address is cited as a reader of this format, because none was found.**~~ *(2026-09-25: the loader is
`002EA530` and the row reader is `002ED950`; see [§ The reader, traced](#the-reader-traced--sb-2-answered-fable-claude-opus-55-2026-09-25).)*

## 5. Corpus survey

| unit | records | empty | populated |
|---|---:|---:|---:|
| `charseinfo_b` | 18 | **18** | **0** |
| `charseinfo_c` | 23 | 3 | 20 |
| `charseinfo_g` | 104 | **104** | **0** |
| `charseinfo_m` | 254 | 17 | 237 |
| `charseinfo_n` | 175 | 24 | 151 |
| `charseinfo_s` | 26 | 13 | 13 |
| `charseinfo_t` | 16 | **16** | **0** |
| `charseinfo_w` | 327 | 75 | 252 |
| **total** | **943** | **270** | **673** |

**Three of eight tables are entirely empty**, and one (`_s`) is exactly half. `_w` is the largest at
327 records.

**Slot occupancy across all 943 records:** slot0 is `0xFFFF` in 691, slot1 in 605, slot2 in 590,
slot3 in **904**. So slot3 is almost never used — 39 records in the whole corpus set it.

**Corrected 2026-09-13 (§9): the three populated slots occupy *disjoint* bands**, and slot3's
range was understated:

| slot | non-empty | distinct | range |
|---|--:|--:|---|
| 0 | 252 | 60 | `0x00FA`–`0x02C5` |
| 1 | 338 | 46 | `0x00C8`–`0x00F9` |
| 2 | 353 | 111 | `0x012C`–`0x01B2` |
| 3 | 39 | **35** | `0x0000`–**`0x003F`** (~~`0x0000`–`0x000E`~~) |

> **Slot 3 is a different kind of field from slots 0–2** — now on a discriminating test rather
> than on occupancy and range: **every one of the 943 values in slots 0–2 is a shipped `.seb` SE
> block number and only 4 of slot 3's 39 are** (§9).

### The `ch`/`in`-only distribution is not unique to this format

**These files ship under exactly two locale trees, `ch` and `in`, and under no other.** That is
**the same two-tree distribution as `.ard`**, whose README records it as an open oddity:

> *"a per-area data file shipping under exactly two locale trees, neither of them `us` or `jp`, is
> not what a localisation split looks like. Neither is explained."*

**It is now two formats with the identical distribution**, which moves it from a possible `.ard`
quirk to a shipping pattern that wants one explanation covering both. Recorded as
**PROPOSED-repos-c7-21**.

## 6. Falsification pass — 2026-09-06

| attack | result |
|---|---|
| Is `+0x08` the record count? | `16 + count*16 == size` in 8 of 8, exactly, with no remainder. |
| Is the record 16 bytes or 8 with 8 of padding between? | Either fits the arithmetic. **The trailing 8 bytes are zero in 943 of 943**, so the sheet reports four slots in a 16-byte cell and says the second half is reserved rather than guessing which. |
| Is `+0x06` really the filename letter? | Eight units, eight different values, each matching its own filename. A ninth unit would test it further; there is no ninth. |
| Is `0xFFFF` "empty" or a real id? | It is 691 of 943 in slot0 and 904 of 943 in slot3, and three whole tables consist of nothing else. A real id would not fill three complete files. |
| Is `charseinfo` = character sound effect? | **Not claimed.** The expansion is conventional and the folder has two recorded misses from name-driven guesses. §7 leaves it open. |
| Did the census actually run? | **Caught a real instance of this.** The first run filtered paths on `/binaryfile/` and these files live in `/common/`, so it reported *"0 records"* for every field — a clean-looking empty result. The script now asserts a non-empty file list before reporting. **"Scanned nothing" and "found nothing" read identically**, which is `COVERAGE.md` line 575. |

## 7. What this document does not claim

- [x] ~~**What the four slots select.** Not sound ids, not anything else — the values are described
  in §5 and named nowhere.~~ **Slots 0–2 answered 2026-09-13 (§9): they are SE block ids.** All
  **943** non-empty values across those three slots — 217 distinct — are **shipped `.seb` block
  numbers, 100 %, no exceptions**, while slot 3 fails the same test (4 of 39). **What slot 3
  selects is still open.**
  *Answered 2026-09-30 (SWE2-CONTRACT, [`swe2contract-ddres-b5-0930`](../../_index/candidates/swe2contract-ddres-b5-0930/README.md), [`chse_slot3.py`](../../_index/candidates/swe2contract-ddres-b5-0930/chse_slot3.py)):* **slot 3 is the actor's fallback pack key.** Its one reader is
  `002ED910` (T3, T9, T10: no other caller of `002ED950` reads `+6`, and no pointer to either function exists). It is called
  only by the party read-in state machine `0037B4D0`, in state 4, with the actor's definition key (`0031C250` →
  `002EB7A0`, T8). `002ED910` asks `003212E0` first: the signed word `+0x26` of `[actor + 0xE60]` when the record at
  `[actor + 0x698]` has byte `+5 == 1`, else −1 (T6). Only when that is negative, or there is no actor, does it return
  slot 3 as a signed word. The result is the key `0036F0F0` takes at `0037B896`: the refcounted voice/resource pack
  swap of [the party read-in page](../../01-Script-VM-Native-Bridge/Party-Presentation-Verbs/the-party-read-in-state-machine.md)
  (UQ-50). A negative key (`0xFFFF`) sends the machine to state 7 and skips the swap (T7). The 39 authored values are
  `_c` 14 (0–14), `_m` 1 (17), `_n` 11 (6–63), `_s` 13 (18–30) (D2). Which shipped actors reach state 4 with no
  battle-record key, and so use these values, is not bounded here.
- [x] ~~**What `charseinfo` stands for.** The obvious expansion is stated in §1 as an unproven
  reading.~~ **Corroborated 2026-09-13 (§9) by structure rather than by the name** — which is the
  standard §1 set for itself. It is still a reading; it is no longer a *name-driven* one.
- **What the eight letters are.** `b c g m n s t w` are character-class initials on the evidence of
  nothing but their being letters.
  *Narrowed 2026-09-30 (SWE2-CONTRACT):* the letter is bits 16–23 of the actor's definition key. `002ED950` selects
  the table by it (the reader section), and the same letter/number split is the model-id format
  ([character-render-object.md](../../17-Presentation-Rendering/Character-Rendering/character-render-object.md): `c1004`).
  So a table serves the actors whose model id carries its letter. What each letter family is, as a class of
  character, is still not claimed.
- **Why three tables ship empty.** *(2026-09-30, SWE2-CONTRACT: the effect is static — an actor whose key names `b`, `g`
  or `t` loads no SE block through `002E60F0` and has no fallback pack key; the reason is authoring intent, which this
  page does not claim.)*
- ~~**Anything about the loader.** None was found; §3 names the search that failed.~~ *Superseded 2026-09-30
  (SWE2-CONTRACT): the loader `002EA530` and the reader `002ED950` are traced in the reader section, and §3 carries
  the rebuilt contract.*
- ~~**Whether `version = 1` gates anything.** Constant in 8 of 8, no reader found.~~ *Answered 2026-09-30
  (SWE2-CONTRACT, [`chse_slot3.py`](../../_index/candidates/swe2contract-ddres-b5-0930/chse_slot3.py) T1, T11): it gates nothing. No code that reaches the tables reads `+0x04`.*

## 8. Related

- [`README.md`](README.md) — the `ps2data/image` long tail, and the two recorded name-driven misses
  this sheet's §1 defers to.
- [`sloc-menumap-container.md`](sloc-menumap-container.md) — the same path-table location route and
  the same structural limit on finding a parser.
- `../VBF-Archive-And-Authored-Tables/St2e-Carriers/README.md` — the `.ard` `ch`/`in`-only
  distribution this format shares.
- `Tools/work/formats/bin-signature-census.tsv` — the frozen census this unit came from.

## 9. Falsification pass 2 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run first, one query at a time and read in full — which is how `SB-2`
below was found before anything was claimed.)*

### The corpus reproduces exactly, re-walked from the archive

Re-extracted from `FFXII_TZA.vbf` and walked with independent code: **16** files, **`ch` and `in`
only**, the eight units `b c g m n s t w`, **8 / 8** locale pairs byte-identical, magic `CHSE`,
`version = 1`, `+0x06` = the filename's letter and `+0x0C` = 0 all **8 / 8**, `16 + count × 16 = size`
**8 / 8**, **943** records, and the trailing eight bytes zero in **943 / 943**. §5's per-unit table is
exact row for row — 18/18/0, 23/3/20, 104/104/0, 254/17/237, 175/24/151, 26/13/13, 16/16/0,
327/75/252, totalling **943 / 270 / 673** — and so is the slot occupancy: `0xFFFF` in **691, 605,
590, 904**.

### ✔ What slots 0–2 select: SE block ids

The three populated slots occupy **disjoint value bands** (§5, corrected). Those bands are not
arbitrary — they are the shipped `.seb` numbers. Testing membership against the **248** SE blocks
censused from the archive:

| slot | non-empty values | in the shipped `.seb` set |
|---|--:|---|
| 0 | 252 | **252 / 252 — 100 %** |
| 1 | 338 | **338 / 338 — 100 %** |
| 2 | 353 | **353 / 353 — 100 %** |
| **3** | 39 | **4 / 39 — 10 %** |

**All 943 values in slots 0–2, 217 distinct, are shipped SE block numbers, with no exceptions — and
slot 3 is the control that shows the test discriminates.**

Two further agreements with
[the `.seb` block index](../../18-Audio/Sound-Bank-And-Voice-Formats/seb-se-block-index.md):

* it records that the actor-resource step reads **up to three** `u16` block ids, *"one per pass,
  three passes"* — and a CHSE record has **three** populated slots;
* it records that **an id with bit 15 set means "none"** — and CHSE's empty marker is **`0xFFFF`**.

> **So `charseinfo` = character *SE* info is carried by structure now, not by the filename.** §1
> refused to assert it because this folder *"has already been burned twice by name-driven guesses"*.
> That caution was right and it is what makes this worth stating: **the reading is unchanged, the
> evidence under it is not.** A closed-set membership test over an entire corpus, with a failing
> control in the same record, is a different kind of argument from an abbreviation.

### → A candidate answer to `SB-2`, filed and not closed

`SB-2` ~~is open and~~ asks *(answered 2026-09-25, FABLE, the reader section; pointer 2026-09-30, OPUS)*: *"Which actor-resource records supply the three SE block ids `002E60F0`
reads (through `002ED950`)?"* **CHSE is now the leading candidate**, on the evidence above.

*(2026-09-25: the reader is now traced and the candidate is confirmed, in
[§ The reader, traced](#the-reader-traced--sb-2-answered-fable-claude-opus-55-2026-09-25).)* **It is not claimed as the answer.** No reader for CHSE has been found — §3 still stands — so this is
a closed-set membership test, **not a traced data path** from `002ED950` to these bytes. Closure
needs the reader, and belongs with `SB-2`'s owner.

### What the location route looks like, measured

§3's *"sixteen path strings ship in `.rdata`"* is exact: **16**, e.g.
`PS2Data\image\ff12\in\common\charseinfo_b.bin` beginning at `00956C38` (§4 cites `00956C55`,
which is the `charseinfo_b.bin` tail of that same string). They are referenced from **ten separate
eight-entry pointer blocks** — `01E0E410`, `01E126C0`, `01E27330`, `01E4DB30`, `01E586D0`,
`01E6BE40`, `01E81050`, `01EAEC50`, `01EBF7A0`, `01EDFD70` — **one per locale**, which is exactly the
per-locale path table §3 says `FUN_002DF9A0` populates at boot. The structural wall §3 describes is
confirmed, not breached.

**Not claimed.** What **slot 3** selects — it is not an SE block id and nothing here says what it is.
Why three tables ship empty. Whether `version = 1` gates anything. The CHSE **reader**: still not
found, and the ten-block measurement above locates the data without finding the code. Whether the
`ch`/`in`-only distribution shared with `.ard` has one explanation — `PROPOSED-repos-c7-21` is
untouched. The archive was **read, never written**, and nothing was executed.

*Superseded readings, 2026-09-30 (SWE2-CONTRACT): this section's "no reader for CHSE has been found" and "the CHSE
reader: still not found" predate the reader section below (FABLE, 2026-09-25), which traces it. Slot 3 and
`version` are answered in §7. The text above is kept as the record of pass 2.*

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Audio — SERVICE** *(the helper is `003A1650`, the SE block registration, [seb-se-block-index.md](../../18-Audio/Sound-Bank-And-Voice-Formats/seb-se-block-index.md) §3.2; pointer 2026-09-30, OPUS)*~~, not read~~. A 491-byte body this page cites calls a 256-byte Audio-filed helper. ~~What that helper does is not read here.~~ *(answered: see the line below - the helper is the SE block registration; 2026-10-02, OPUS)*
  *Answered 2026-09-30 (SWE2-CONTRACT, from the database):* the body is `002E60F0` and the helper is `003A1650`, the SE
  block registration, read in full at [seb-se-block-index.md §3.2](../../18-Audio/Sound-Bank-And-Voice-Formats/seb-se-block-index.md).
  `002E60F0` stores its return at `002E61E9`.

*Citation spellings (R5), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — CLIENT.** `ResourcePath_Init` (2,831 bytes), which this page cites, is called from the 978-byte core start-up root.
- **ActorEntity — CLIENT and SERVICE (10 edges).** 3 inbound (ActorEntity bodies `0037B4D0` call page-cited `0031C250`, `002EB7A0`, `002ED910`); 1 outbound (page-cited `0031C250` call ActorEntity bodies `ActorWork_GetBattleUnitRaw` (00263E30)).
- **Gameplay — SERVICE (3 edges).** 3 outbound (page-cited `0037B4D0`, `0031C250` call Gameplay bodies `BattleEncodedId_IsValidForClass` (00322C50), `WorldActor_GetDefinitionByte12OrMinus1` (002E9C00), `ActorHandle_GetPrimaryFormulaResourceByte26` (00321380)).
- **Movement — SERVICE (11 edges).** 4 outbound (page-cited `0037B4D0` call Movement bodies `00263560`, `002681D0`, `Actor_SetDesiredMovementHeading` (0026A0D0)).
- **Party — SERVICE (2 edges).** 2 outbound (page-cited `0031C250`, `0037B4D0` call Party bodies `PartyRoster_GetActorBySlot` (00263750), `PartyRoster_IsFourSlotIndex` (002647C0)).
- **Script_VM_Native_Bridge — CLIENT (1 edge).** 1 inbound (Script_VM_Native_Bridge bodies `003466A0` call page-cited `0036F0F0`).
- **WorldAreaField — SERVICE (2 edges).** 2 outbound (page-cited `0037B4D0` call WorldAreaField bodies `00377A90`, `00377DB0`).
## The `002E60F0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`002E60F0` (~~~62 B~~ 491 B *(corrected 2026-10-02, OPUS: its last instruction ends at `002E60F0+0x1EB`; 62 B is the member `003A1290`)*) — `dword[rcx]`-keyed table op (`002E60FA`).

| member | role | interior |
| --- | --- | --- |
| `003A1290` | `ecx == -1` → `r8d = 0` else `movzx ecx, dx` — index normalize (`003A1292`/`003A129C`) | [`003A1292`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.


## The reader, traced — SB-2 answered (FABLE, Claude Opus 5.5, 2026-09-25)

*Static, from the shipping bytes, and a check over both locale copies.*

**The loader.** `002EA530` loops `i = 0 … 9` (`002EA55A`–`002EA5CC`). For each it loads resource kind
**9**, id **`0x0B + i`**, into a fresh buffer (the size query at `002EA56B`, the allocation at `002EA586` and the read at `002EA5A9`), and
stores the pointer at **`021641A0 + 8·i`** (`002EA596`). Kind 9's path array (the `in` arm at `01E4DAD0`)
names ids 12–19 as **`charseinfo_b`, `_c`, `_g`, `_m`, `_n`, `_s`, `_t`, `_w`**, while 11 and 20 are empty.
So `021641A8` … `021641E0` hold the eight tables in letter order. The call at `002EA5BB` passes the
buffer, the string `"ChSEinfo"` and `i` to the allocator's header tagger. Its body copies seven
characters of that string into the block's debug header and stores `i`. **It is not a magic check,
and §3's "magic never compared" stands.**

**The row reader.** `002ED950` takes a packed actor resource id in `ecx`:
- Bits 16–23 carry a letter: `movzx eax, cl` after `shr ecx, 0x10`, rebased by `−0x62` (`002ED953`–`002ED959`).
- A jump table sends each letter to its own table: `b` → `021641A8`, `c` → `021641B0`, `g` → `021641B8`,
  `m` → `021641C0`, `n` → `021641C8`, `s` → `021641D0`, `t` → `021641D8`, `w` → `021641E0`
  (decoded from the table at `002ED9D8`).
- The low 16 bits are the row, bounded by the table's `+8` count (`002ED9C2`).
- `002E60F0` reads the three `u16` of that row as SE block ids.

**The data path, end to end**: actor resource id → letter → `charseinfo_<letter>` → row → slots 0–2 →
`002E60F0`'s index rule → the kind-32 `se<n>.seb` load.

**Whether the rule can go wrong on shipped data.**
[`members/chse_se_index_check.py`](members/chse_se_index_check.py) pushes every authored value through
`index = id < 500 ? id − 192 : id − 392` into the kind-32 array (`01E7FCF0`, 608 entries) and checks
the landing file:
- **943 values, 217 distinct, 200–709. Every one lands on its own `se<n>.seb`.**
- **None lies in 3–199 or 500–699.** Slot 0 jumps from below 500 straight to 700–709.
- The `ch` and `in` copies of all eight tables are byte-identical (SHA-256 compared), so one census
  covers both locales.
