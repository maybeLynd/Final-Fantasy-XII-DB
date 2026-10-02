---
system: The `qstl` quest-list string index — `quest/menuquest.lst`
category: 02-Resource-And-Asset-Pipeline
status: DOCUMENTED — every register row is closed (owner re-status 2026-09-30, OPUS, on SWE2-CONTRACT's reconciliation; superseded readings are marked on the page) — no registered residue left: the field-level readers answered (RC-31: 0037EFC0 and 0037E5B0, order-independent; +0x04 read by neither reader nor any of the 27 functions holding the list pointer 02AED490 (census scope), +0x08 read as u16, correcting §2) (status line current 2026-09-30, SWE2-CONTRACT)
owner_layer: CodeDomain:Presentation.Menu.QuestList
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-21 (FABLE) - 9 addresses cited - 7 entry, 2 interior, every one resolving into a known section of the authority image.
    **This records a check performed on that date, NOT the method of the
    original derivation**, which this block never carried; see this
    document's own evidence section for that.
corpus_validated: "all 9 shipped .lst files extracted from FFXII_TZA.vbf and hashed, 2026-09-14; directory arithmetic verified on all 9"
archive_formats:
  - "lst | explained | qstl quest-list string index — sparse u16 id -> variable-length encoded-string blob; requested at 0037F76F by widget proc 0037F4D0."
last_reviewed: 2026-09-30
audit:
  passes: 1
  last_pass: 2026-09-17
  last_pass_state: falsification-pass
  crossref_clean: false
  reopened_count: 0
---

# The `qstl` quest-list string index — `quest/menuquest.lst`

> **The quest-list name strings.** One file per language — `menuquest.lst` in all nine locale
> directories — holding a sparse `questId → encoded string` directory over a blob of
> variable-length records. It is *not* a build artefact: the binary's own path string is
> `quest\menuquest.lst`, and the request site sits inside the quest-list widget procedure.

**Corpus validation, before anything else.**

|| |
|---|---|
| files examined | **9 of 9** shipped `.lst` entries — all `quest/menuquest.lst`, one per language, **9 distinct contents** (unlike the rest of this family, locale text differs) |
| size range | 1,684 B (`in`) – 2,036 B (`es`) |
| magic `qstl` | 9 of 9 — `71 73 74 6c` |
| header triple | `+0x04` = 0x64 (100), `+0x08` = 0x220, `+0x0E` u16 = 66 — identical in 9 of 9 |

Sizes/paths/hashes frozen at `Tools/work/DATA/extract/manifest.tsv`.

## 1. What the player sees

The Quests tab of the clan primer — the scrollable list of hunt marks and side-quests with their
titles. `menuquest.lst` is the list's string table; the per-quest payload data lives in the sibling
`menuquest.dat` (`qstd`), requested 0x12 ids earlier by the same function.

## 2. The layout

### 2.1 Header — `0x10` bytes + a `0x210`-byte directory

```struct QstlHeader base=file size=0x10
+0x00  char[4]  magic     'qstl' - 71 73 74 6c, 9 of 9
+0x04  u32      capacity  0x64 = 100 in all 9 — quest-slot capacity, larger than dirCount
+0x08  u32      dataOff   0x220 in all 9 — start of the string blob
+0x0C  u16      _zero0C   0 in all 9
+0x0E  u16      dirCount  0x42 = 66 in all 9 — directory entry count
```

```struct QstlDirEntry base=+0x10 stride=8 count=dirCount
+0x00  u16   questId    all 66 distinct, NOT sorted — shipped order runs 0,3,4..22, then 128..167, then 172 BEFORE 168,169,170,171, then 50,51
+0x02  u16   dataRel    byte offset into the string blob at dataOff — non-decreasing
+0x04  u32   kind       a u32, not two u16s: only three values ship — 3 (×44), 0 (×21), 4 (×1)
```

`+0x10 + 8*dirCount == dataOff` holds exactly (0x10 + 0x210 = 0x220). Entry 0 is all-zero
(`questId` 0 with `dataRel` 0 — a real string target at blob base, or the empty row; both readings
consistent).

`dataRel` arithmetic: early entries step `0x0C` (the repeating 12-byte default string); later
entries share offsets (ids 50 and 51 both point at +0x59B). **Offsets land immediately after a NUL
in 66 of 66 entries** (verified on `us`; OPUS verified `us`/`fr`/`ch`) — each target is a
NUL-terminated string and `dataRel` points at its first byte.

### 2.2 The string blob — `dataOff` .. EOF

Variable-length NUL-terminated strings in the game's encoded text (not ASCII), padded to 4-byte
alignment: bytes cluster in `0x21..0x4D` with `0xA8`/`0xAE`/`0xAF` separators — e.g.
`… 3a 47 3a 4c 4d 4b 3e af 00 00`. The repeating 12-byte head pattern is one default string
repeated — **not de-duplicated**: 19 of 66 records point at byte-identical 12-byte strings at
different offsets; 46 distinct bodies in all (OPUS measurement). Locale-varying: the blob is
1,140 B in `in`, 1,492 B in `es`; `us`/`fr` are ~83% printable-or-NUL, `ch` ~33%. The substitution
encoding is the same family used by other `qst*`/`menuquest` text — mapping is owned by the
text-data sheets, not re-derived here.

## 3. The loader contract

|| |
|---|---|
| requester | `0037F4D0` — the quest-list widget procedure (747 B; answers widget messages 1/16/18; also requests `menuquest.dat`) |
| request site | `0037F76F` — kind `0x7`, id `0x13A`, through `00249210`. `00249210` is the shared pool core — the SaveLoad screen `00582790` also calls it (the load-menu reuse), an API-sharing edge, not a `.lst` consumer |
| path resolution | kind-7 path array: `…\myoshiok\<lang>\quest\menuquest.lst` |
| buffer consumer | quest-list subsystem — ~~the pane builder `00575710` resolves rows from the loaded quest data~~ *(corrected 2026-10-02, OPUS: `00575710` is the handbook image pane's bind: it registers the pane's `+0xF0` buffer as a TIM2 at `00575710+0x5C` and keeps the handle at `+0xF8`, `00575710+0x55`; the `.lst` readers are RC-31's two)*; the `.lst` half is the string side (see §7) |
| magic check | none found — no `qstl`/`0x6C747371` constant in `.text` |

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| `qstl` magic | nothing found | — | — | no compare found in `.text` |
| `+0x04` capacity | — | — | — | no reader found by census/xref |
| `+0x08` dataOff | — | — | — | no field-level reader isolated *(since read: `0037EFC0` reads it as a u16 at `0037F02A`, RC-31)* |
| `+0x0E` dirCount | — | — | — | no field-level reader isolated *(since read: `0037EFC0` `0037EFD9` and `0037E5B0`, RC-31)* |
| dir `questId`/`dataRel` | quest-list row lookup (screen family) | — | — | exact reader not isolated *(since read: `0037EFC0` compares `+0` and takes `+2` (`0037F01C`); `0037E5B0` takes the `+4` byte's low nibble, RC-31)* |

*(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../../_index/candidates/auditspec-review-dd-02-b2-0930/REVIEW.md) correction 3: the three Inert cells above carry their answers.)*

## 4. Key addresses

| Address | Role |
|---|---|
| `0037F4D0` | quest-list widget procedure — loads `menuquest.dat` (`0037F740`, id `0x128`) and `menuquest.lst` (`0037F76F`, id `0x13A`) |
| `0037F76F` | the `.lst` request site |
| `00576F50` / `005771F0` | quest-data loader / quest-list parent widget ([quest page](../../16-UI/Quest-List/the-quest-list-screen.md)) |
| `00575710` / `00575870` | pane resolver / pane instance (×3) |

## 5. Corpus survey — 9 files

|| |
|---|---|
| `qstl` | 9 of 9 |
| capacity `+0x04` = 100, dataOff `+0x08` = 0x220, dirCount `+0x0E` = 66 | 9 of 9 — same directory, different string blob per language |
| sizes | `in` 1,684 · `cn` 1,736 · `ch` 1,748 · `fr`/`kr` 1,864 · `de` 1,936 · `it` 1,960 · `us` 1,980 · `es` 2,036 |
| dir→data arithmetic | `0x10 + 8*66 == 0x220` in 9 of 9 |

## 6. Falsification pass — 2026-09-14

| attack | result |
|---|---|
| Earlier claim "count 100 at +0x08, dataOff at +0x0C" | **Wrong offsets** — corrected: capacity at `+0x04`, dataOff at `+0x08`, dirCount u16 at `+0x0E`. |
| Are the 8-byte units really the directory? | **Yes** — 66×8B spans `+0x10`..`+0x220` exactly = `dataOff`; ids are sparse and ascending. *("Ascending" is superseded by §2's census: the ids are NOT sorted — 172 precedes 168–171 and 50, 51 come last. Noted 2026-09-30, SWE2-CONTRACT.)* |
| Are data records fixed 12-byte? | **No** — only the leading identical default string repeats at 12 B; later `dataRel` values are non-multiples (0x59B) and shared between ids → variable-length strings. |
| Is the blob ASCII? | **No** — encoded text (`0x21..0x4D` + `0xAx` separators + `0x00` terminators). |
| Is `.lst` dead PS2 baggage? | **No** — it sits in the boot-installed kind-7 path array (10/10 membership) and is requested by a live widget procedure. |

## 7. What this document does not claim

- **Which function parses the directory/string blob field-by-field** — the consumer family is
  identified (quest-list), the field-level reader is not isolated.
- **What `+0x04` = 100 bounds** — it exceeds `dirCount` (66); consistent with a quest-slot
  capacity, unconfirmed.
- **`aux` (`dir+0x04`) semantics** — nonzero on some late entries. *(The same field §2 names `kind`, a u32 taking only
  3, 0 and 4; one field, two names. Noted 2026-09-30, SWE2-CONTRACT.)*
- **The text encoding table** — owned by the text/font sheets.
- **Why ids 50/51 sort after 171** — the tail order is shipped order, not id order; unmodeled.

*Searched 2026-09-30 (SWE2-CONTRACT):* [the quest list screen](../../16-UI/Quest-List/the-quest-list-screen.md) names
no reader of the `.lst` bytes; the kind-7 path-array membership (10/10) is [the file-size tables page](../Loose-Files-And-Size-Tables/file-size-tables-fst.md)'s
check.

- [x] **RC-31.** Which function parses `menuquest.lst` (the widget `0037F4D0` requests it as kind 7 `0x13A`): its
  reader of the directory and string blob, what `+0x04` = 100 bounds, what the directory's `+0x04` word (3, 0 or 4)
  selects, and whether the lookup depends on the shipped id order. Registered 2026-09-30 (SWE2-CONTRACT); static.
  *Applied 2026-09-30 (records) RC-31:* **ANSWERED 2026-09-30 (static; SWE2-DATA's record `_index/candidates/rc22-34-resource-readers-0930/` §4, commit `1261e2044`, `lst_reader.py`): the readers are `0037EFC0` and `0037E5B0`**; the lookup is order-independent; header `+0x04` is read by neither reader nor any of the 27 functions holding the list pointer `02AED490` (census scope), `+0x08` is read as a u16; the directory `+0x04` word's low nibble is a threshold compared against `0037EE10`. *(This corrects §2's `+0x08` "u32 dataOff" width and `+0x04` "capacity" reading — see the note under §7.)*

*Superseded readings, 2026-09-30 (SWE2-CONTRACT, from SWE2-DATA's record `_index/candidates/rc22-34-resource-readers-0930/` §4, commit `1261e2044`): §2's `+0x08` "u32 dataOff" is read as a u16, and `+0x04` "capacity" is read by neither reader nor any of the 27 functions holding the list pointer `02AED490` (census scope; RC-31); the directory's `+0x04` (`kind` / `aux`) low nibble is a threshold against `0037EE10`. The struct is kept as written.*

## 8. Related

- [`the-quest-list-screen.md`](../../16-UI/Quest-List/the-quest-list-screen.md) — the consumer family.
- [`constant-resource-requests.tsv`](../VBF-Archive-And-Authored-Tables/members/constant-resource-requests.tsv) — rows for `0x7 0x13A`.
- [`README.md`](README.md) — the `ps2data/image` long tail.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-FRONTIER for SWE2-DATA, 2026-09-30)

*Added 2026-09-30 (SWE2-FRONTIER, executing SWE2-DATA's pass-22 debt). These are the layers pass 22 still reported for this page at HEAD `4dfe4a006`. Every edge was listed in full, and each cited helper was read at its instructions.*

**UI — CLIENT (4 edges).** `003C9950`, `00561390` and `00562F90` claim slots through the shared pool entry `00249210`, which also loads `menuquest.dat` here. The quest-list parent `005771F0` calls the quest-data loader `00576F50`. The pool is shared, and the quest widgets own the `.lst` read.

**SaveLoad and Save_Load_Settings — CLIENT (2 edges).** `00582790` claims a slot through `00249210`, and `SaveLoad_ControllerLifecycleHandler` (`00582860`) calls `00582790`. This is the load-menu reuse the page already names, not a `.lst` consumer.

**Presentation — CLIENT (2 edges).** `00579420` calls `0037E5B0`, and `0037E8D0` calls `0037EFC0`: the two field-level readers RC-31 answered. These are the render-side callers of the list's field readers.
