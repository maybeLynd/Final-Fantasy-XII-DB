---
system: The `hctg`/`hchk`/`hdat` handbook index family — `handbook/menuhandbook_<family>{.bin,.dat,NNN.dat}`
category: 02-Resource-And-Asset-Pipeline
status: AUDITED
owner_layer: CodeDomain:Presentation.Menu
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-21 (FABLE) - 145 addresses cited - 15 data, 97 entry, 33 interior, every one resolving into a known section of the authority image.
    **This records a check performed on that date, NOT the method of the
    original derivation**, which this block never carried; see this
    document's own evidence section for that.
corpus_validated: "all 54 hchk files (6 families × 9 locales), all 101 hdat files, and all 54 hctg family .bin files parsed 2026-09-18; hchk record count == hctg record count == hdat record total per family; hdat +0x08 base-ordinal chain closed with zero violations across all locales; non-monster hchk w6 monotonicity verified corpus-wide"
archive_formats:
  - "hctg | explained | Handbook family catalog — {tag, aux region, 12-byte {textId, group, index} record table} + monster-only indexed tail; drives the family's resource-id arithmetic and page dispatch."
  - "hchk | explained | Handbook unlock predicates — 8-byte 4-slot conjunctive gates over save-block flag/nibble banks + scenario-flag threshold; monster records are 16-byte u16[8] kill/state vectors. Results are synced into the Clan Primer save flag arrays by 00577550."
  - "hdat | mostly-explained | Handbook record headers — {u16 baseOrdinal, u16 count} + variable-length {12+4k}-byte records + encoded-string blob + at most one TIM2; record interiors only partially field-bound."
last_reviewed: 2026-09-18
audit:
  passes: 1
  last_pass: 2026-09-18
  last_pass_state: falsification-pass
  crossref_clean: true
  reopened_count: 0
---

# The `hctg` / `hchk` / `hdat` handbook index family

> **Three companion formats wrap the handbook's page images.** The `himg` bundles
> ([the himg page](himg-handbook-image-bundles.md)) are the *payload*; this page covers the
> *indexing layer*: `hctg` (the per-family catalog `.bin`), `hchk` (the unnumbered `.dat`
> unlock-predicate table), and `hdat` (the numbered record headers). Together they turn raw
> page images into "show this entry, unlock it when the story reaches flag X".

**Corpus validation, before anything else.**

|| |
|---|---|
| files examined | **all 54 `hchk` + all 101 `hdat` + all 54 `hctg`** shipped in `FFXII_TZA.vbf` (6 families × 9 locales each; hdat count varies by family) |
| directories | `ps2data/image/ff12/myoshiok/<lang>/handbook/` — `menuhandbook_<family>.bin` = hctg, `menuhandbook_<family>.dat` = hchk, `menuhandbook_<family><NNN>.dat` = hdat then himg |
| structural failures | **0** — every file parses, every record walk closes to EOF, every offset lands in bounds |
| cross-file invariant | `hchk.count == hctg.word[+0x0E] == Σ hdat.count` per family — zero violations |
| `hdat` `+0x08` chain | `+0x08` of file `NNN` equals the running record total of files `000`–`NNN−1` — **zero violations across all 101 files** → `+0x08` = base ordinal (same role as `himg`'s) |

Per-family record counts: story 69, world 74, person 57, knowledge 100, tutorial 16, monster 384.

Validator: `members/gen_hb_index_census.py` → `members/hb-index-census.tsv` — replays every
check on this page over the extracted corpus (54 loc×family rows, 6,300 `hdat` records, 0
length/tail/ordinal failures).

## The resource-id enumeration — how the three formats share one id space

The six families are bound to kind-7 resource ids whose bases sit in the `u16[6]` table at
`.rdata 00D23740` (`{0x228, 0x294, 0x2CC, 0x2F4, 0x31C, 0x354}` — story/world/person/
knowledge/tutorial/monster; `00575C4E` loads it, `00575C60` indexes it, `00576FE9` re-uses it
to queue the six TIM2 loads). Within a family, the resource *delta* walks the family's files
in archive order:

| delta | file | format |
| --- | --- | --- |
| 0 | `menuhandbook_<fam>.bin` | `hctg` |
| 1 | `menuhandbook_<fam>.dat` | `hchk` |
| 2 … `1+hctg.u16[+0x14]` | `menuhandbook_<fam>{000..}.dat` | `hdat` |
| `2+hctg.u16[+0x14]` … | `menuhandbook_<fam><NNN>.dat` | `himg` |

This is native-proven: `005773D2` stores `hctg.word[+0x14] + 2` into the request descriptor
field `+0xCA` — the first `himg` delta. `hctg +0x14` therefore = **the family's `hdat` file
count** (1 for story/world/person/tutorial, 2 for knowledge, 4 for monster — matching the
shipped file names exactly, corpus-verified). The sibling `menuhandbook.bin`/`order.bin` pair
uses a different id space (kind-6 base `0x80`); the `menuquest.dat` bind uses `0x128` — the
first entry of the `00D23740`-style base table's kind-0 slot.

## `hctg` — the family catalog (`menuhandbook_<fam>.bin`)

```
+0x00  char[4]  magic      'hctg'
+0x04  u32      familyTag  {6400, 6401, 3954, 6403, 6404, 3877} — per-family constant
+0x08  u16      packed     low nibble = family ordinal 0..5 (consumed by `00576CA0` and
                          the `005760A0` monster check); high 12 bits copied verbatim into
                          the family descriptor `out+0x04` (00576061: word>>4) — **dead on
                          the data path**: none of `00576030`'s three callers (`00570BF0`,
                          `00571F60`, `00574080`) ever reads `out+0x04`. Per-family values
                          {story 0x1900, world 0x1901, person 0xF72, knowledge 0x1903,
                          tutorial 0x1904, monster 0xF25} look textId-shaped but are unbound
+0x0A  u16      recTableOff file offset of the 12-byte record table
                          (story 0xB0, monster 0x48C — verified against table bounds)
+0x0C  u16      pageMapOff file offset of the `u16[+0x10]` page→resource-slot map — read by
                          `00575DD0` (`word[hctg + pageMapOff + pageIdx·2]`, `0xFFFF` checked
                          as the unavailable sentinel but never ships); values run
                          0..+0x16−1, non-decreasing; a 0 pad u16 follows in non-monster files
+0x0E  u16      recordCount = hchk entry count = Σ hdat record count
+0x10  u16      pageCount  {65, 46, 41, 45, 1, 384} — the family's page count in the paged
                          view; `00575DD0` bounds the page index against it (req desc +0x0A)
+0x12  u16      captionN   **section count** {4, 10, 4, 7, 4, 32} — bounds `00576A50`'s
                           index; copied to req descriptor +6. Corpus-exact: the record
                           table's `group` field takes exactly the values
                           0..captionN−1 in every file — `group` IS the section index
+0x14  u16      hdatCount  = number of leading numbered `hdat` files (native-proven, §above)
+0x16  u16      slotCount  {17, 12, 21, 12, 1, 192} — the map's value bound = resource-slot
                          count in the family's resource block (max = +0x16 − 1 on all 54
                          files). The loader `00575C30` computes `resource id =
                          word[00D23740 + desc.kind·2] + word[widget+0xCA] + sel`, so `sel` is
                          the resource-delta slot the page's `himg` lives at; monster's
                          map = `i/2` — 192 slots ↔ 192 two-page himg files
```

**Aux region** at `+0x18` — the **section-header table**: one conditional caption per
section, read by the section resolver `00576A50(out, sectionIdx)`:

```
+0x18              u32 textId[word+0x12]     caption text ids (0x11495–0x116E5 space, the
                                           same message-table space as the record table);
                                           0xFFFFFFFF = none
+0x18 + 4·captionN  {u16 count; u16 relOff[count]}  index into per-entry gate blobs
                   (relOff relative to this sub-table's start; only monster ships blobs —
                   count=32; all other families write count=0)
blob               {u8 pad4|nCond<<4; u8 nNav; u16 condId[nCond]; u16 navimapId[nNav]}
```

`00576A50` semantics: `i < word[+0x12]`; `idTable[i] == -1` → return empty. If a blob exists,
each `condId` is queried through `00309EC0` (encoded-id set check) and each `navimapId` against
the current map (`003779F0(003148F0())`, visited via `00255120` / `00255060(…,0x20)` when it
equals the current navimap). **Any pass** → resolve `idTable[i]` through `002F9920` (a
`id·0x68DB8BAD`-reciprocal hash lookup into the 28-bucket text table); **all fail** →
`002F9860(0x3EC)` — the locked-caption placeholder id `0x3EC`. Output record:
`{ptr resolvedCaption; u16 entryIdx; u8 blobByte0 & 0xF | 0xFF}`.

So monster's 32 aux entries are the **conditionally-revealed section headers** (hunt-mark /
rare / elite categories that only show their title once the player has encountered the
content); the other five families' section captions are unconditional.

**The section-header resolver `00576740(out, sectionIdx)`** closes the loop: resolves the
section's caption via `00576A50(sectionIdx)` into `out+0x00`/`out+0x08`, then scans the
whole record table for `word[rec+4] == sectionIdx` and writes `out+0x0A` = first matching
record index (0xFFFF if none), `out+0x0C` = member count, `out+0x0E` = count of members
passing `00576CA0(root, hctg.word[+0x08] & 0xF, recIdx)` — which ignores `recIdx` and
returns the **family-tab availability flag** instead (`byte[00D23750 + fam]` → save-byte
reader `003154B0` for fam 0–5/7; fam 6 → `0037F060(menuquest.dat, 1)`; else 1) — so
`out+0x0E` is the member count when the tab is active at all, else 0 (a
visible/locked toggle, not a per-record progress numerator). `005766E0(recIdx)` is the
plain accessor returning `word[rec+4]` — the record's section index.

**Record table** at `recTableOff`: `recordCount` × 12-byte records.

```
+0x00  u32  textId     message/string-table id (story: 70600, 70601, …; monster: non-monotonic)
+0x04  u16  group      section index — exactly 0..captionN−1 (corpus-exact); the record's
                     membership in the section whose conditional header lives at aux
                     index `group`. Readers: `005766E0` (accessor), `005760A0` (copied to
                     detail out+0x10), `00576740` (membership scan)
+0x06  u16  hdatFile   which numbered `hdat` file the record lives in — copied to the
                     00575D10 request descriptor +0x32 (the resource-delta slot);
                     corpus-exact: per-value histogram equals the per-file record counts
                     (knowledge {0:88, 1:12}, monster {0:71, 1:74, 2:98, 3:141}, all 0 in
                     single-hdat families)
+0x08  u16  index      record's local ordinal / page index — read by 00575D10 and 00577970
+0x0A  u8   flag      monster-only kill-count-category marker: 1 exactly on the 172 records
                     whose tail category v3 ∈ {0,1} (corpus-exact join); copied to out+0x14
+0x0B  u8   pad       0
```

Records are **not** guaranteed unique: story ships four adjacent identical records
(textId `0x113D6`, `index` 10, all fields equal) — duplicates are authored, not
artifacts.

**Monster-only tail** at `hctg + recTableOff + recordCount·12` (file offset `0x168C`):
`{u16 count = 384; u16 relOff[count]}` where each offset is relative to the tail's own start
and lands on an 8-byte aux record `{u16 v0; u16 v1; u16 v2; u16 v3}`. **The native reader is
`005760A0` at `0x57625F`**: it computes the same tail base (`buf + word[+0x0A] +
word[+0x0E]·12`), bounds-checks `recIdx < count`, dereferences `relOff[recIdx]`, and reads
**byte 0 = `v0` as the number of hchk slots to materialize** — it then loops
`00576860(root, family, recIdx, slot)` for `slot < v0`, packing each authored `v[slot]` operand
into `out+0x18+slot`. Corpus joins: `v0` == the record's `hdat` `strCount` byte 384/384,
locale-invariant — i.e. the monster record has `v0` active display slots whose rendered
strings are exactly the hdat `strOff[]` list; `v1`/`v2` = constant `1`; **`v3` = a 15-value
per-monster category id** ({0:164, 6:41, 7:26, 8:23, 2:22, 15:18, …} — the bestiary genus
classification; `v3 ∈ {0,1}` is exactly the set `record+0x0A flag == 1`). `v1`–`v3` are not
read by `005760A0`, and the tail base `buf + word[+0x0A] + word[+0x0E]·12` is computed by
**no other function** — the complete `root+0x108` consumer set is enumerated
(`00574E00`/`00574E80` bind, `00575D10` content request, `00575DD0`/`00577970` page
requests, `00575F10`/`005776D0`/`00577880`/`005771F0` state, `00576030` family descriptor,
`005766E0` group accessor, `00576740` section resolver, `00576A50` caption resolver,
`00576DA0` all-loaded check) — so `v1`/`v2`/`v3` are dead-authored (v3 redundantly encodes
the `rec+0x0A` category flag that IS read).

### The detail resolver `005760A0(out, recIdx)`

Called for the selected record; fills the detail-panel descriptor:

| out field | source |
| --- | --- |
| `+0x00` ptr | name line — `002F9920(textId)` for families 0–4; for monster `002B58B0(003214B0(textId), 0)` — `textId` is a `bank:index` packed word into the battle-text banks (`02EBF170`; `003214B0` is the bounds-checked bank resolver whose sole caller is this function, `002B58B0` the packed-string indexer) |
| `+0x08` ptr | subtitle line, only when `textId ∈ [0x4210, 0x421C]` — exactly 13 monster records per locale (the Espers): `.rdata 00D23790` 13-dword table indexed by `textId − 0x4210`, `entry + 0x106` → `0035D330` encoded-id row → `row+0x18` name → `002B58B0` |
| `+0x10` u16 | `word[rec+4]` — the record's section index |
| `+0x12` u16 | `recIdx` |
| `+0x14` u8 | `byte[rec+0xA]` — the kill-count-category flag |
| `+0x15` u8 | tail `v0` byte — slot count (bounds `out+0x18` fill) |
| `+0x16` u16 | monster only: `00315420(recIdx)` — the live kill counter from save `+0x3404` (−1 → 0) |
| `+0x18` … | `byte[v0]` — the materialized `v[slot]` operands via `00576860` |

`00576030(out)` fills the family half of the descriptor from the bound object `root+0x108`:
`out+0x00` = `byte[obj+0xD2]` (the bound object's **family ordinal** byte — compared against 5
for monster), `out+0x04` = `hctg.word[+0x08] >> 4`, `out+0x06` = `word[+0x12]` (captionN),
`out+0x08` = `word[+0x0E]` (recordCount), `out+0x0A` = `word[+0x10]` (the page/resource
selection value).

### The two request paths — `00575D10` (content) and `00575DD0` (page image)

Both build a `{u8 kind; u16 sel; u16 idx}` descriptor, validate through `00575A50`, and
notify via `00247510`:

- `00575D10(root, kind, recIdx)` — the record→content request. Requires bound `root+0x110`
  (the `hdat` object); bounds `recIdx < hctg recordCount`, loads the 12-byte record, and fills
  `sel = word[rec+0x06]` (the groupHi half), `idx = recIdx`.
- `00575DD0(root, kind, pageIdx)` — the page→image request. Bounds `pageIdx < word[+0x10]`
  (pageCount), reads `sel = word[hctg + pageMapOff + pageIdx·2]` (the page→resource-slot map,
  `0xFFFF` = unavailable), `idx = pageIdx`; on success calls `00575B80` on `root+0x118` — the
  bound `himg` object — which is the `hb_tex` TIM2 page switcher documented on the himg page.
- `00577970(root, kind, recIdx)` — the record→page bridge: bounds `recIdx < word[+0x0E]` on
  the bound `root+0x108` object, reads `word[rec+0x08]` (the record's page index), and calls
  `00575DD0(root, kind, rec.index)` — selecting a detail record loads its page image.

## `hchk` — the unlock-predicate table (`menuhandbook_<fam>.dat`)

```
+0x00  char[4]  magic    'hchk'
+0x04  u32      tag      103
+0x08  u16      count    = hctg record count (per family: 69/74/57/100/16/384)
+0x0A  u16      family   {18 story/world/person/knowledge, 0 tutorial/monster} — counts
                          nothing in-file (no trailing region) and has no reader in the
                          handbook family; dead header field, value shape suggests a
                          vestigial rows-per-page constant for the paged lore lists
+0x0C  rec[]    count × record — 8 bytes for the five non-monster families, 16 for monster
```

### Non-monster record — an 8-byte, four-slot conjunctive gate

`00575E80` evaluates it field-by-field; every populated slot must hold or the entry is locked:

| field | type | sentinel | check |
| --- | --- | --- | --- |
| `+0x00` | u8 sel | `0xFF` | `00315470(sel)` — save nibble `sel` of the `+0x336C` array (i < 0x100) — must **equal** `+0x01` |
| `+0x01` | u8 val | — | the required nibble value |
| `+0x02` | u8 bit | `0xFF` | `00315620(bit)` — bit `bit` of the `+0x334C` array (i < 0x100) must be set |
| `+0x03` | u8 flags | — | not read by the predicate; corpus: `0x80` on every record except record 0 (tutorial: all `0x00`) — gated-entry marker, consumer unbound |
| `+0x04` | u16 id | `0xFFFF` | `0032A8A0(id)` — low 14 bits index the save `+0x14F4` bit array (`id==0`→pass, `id==1`→fail, `id≥0x200`→fail); bit 14 selects the authored-threshold resolver `00377970` |
| `+0x06` | u16 min | `0xFFFF` | `i16` scenario-flag word 0 (`00265270` — element 0 of the `02098E58` kind-3 script-operand bank, `global_flag[0]`, the story-progress variable) must be **≥ min** |

A record is "available" iff every non-sentinel slot passes. The story family is almost purely
`w6`-gated — thresholds 10, 13, 19, …, 6450, monotonic non-decreasing across **all nine
locales** (corpus-verified): each record unlocks when the story flag passes its threshold.
Tutorial carries a mix of always-open (`FF FF FF 00 FF FF FF FF`) and `w6`-gated records.

### Monster record — a 16-byte `u16[8]` state vector

`hchk` monster records are read through two accessors:

- `00576860(root, 5, recIdx, slot)` — returns `word[buf + 0x0C + recIdx*16 + slot*2]`, the
  authored operand for slot `slot` (0–6); slot 7 is not a data read.
- `00576E30(kind, recIdx, slot)` — the per-slot unlock predicate. `kind != 5` returns 1
  (non-monster entries are gated elsewhere). For monster it combines `v[slot]` with a mode
  derived from `v[7]`'s low bits:
  - `v[7]` bit 0 → **mode 1**: `scenario_flag[0] ≥ v[slot]` (sentinel `0xFFFF` = locked).
  - `v[7]` bit 1 → **mode 2**: `00315420(recIdx) > 0` **or** `00315420(v[slot]) ≥ 1`.
  - neither → **mode 0**: `v[slot] != 0xFF` and `00315420(recIdx) ≥ v[slot]`.
- `00315420(i)` reads `byte[save + 0x3404 + i] − 1` (−1 when the byte is 0) — the per-record
  counter bank the bestiary kills/lore counts live in (`i < 0x200`; see the persistent-flag
  contract page). Mode 0 is therefore the **kill-count unlock**: "lore slot N appears once
  `counter[recIdx] ≥ v[slot]`".
- `005768E0` reads `v[7]`'s two bits directly into a 0/1/2 status code (bit1→2, bit0→1) used by
  the entry resolver for display state.

### Where the results land — the Clan Primer flag arrays

The predicate results are *persisted* into the save block's Clan Primer region, not recomputed
per frame:

- `00577550(root, kind)` — the per-family sync pass, called from the handbook panel's message
  arms (`0056F79B`, `0056FB5C`, `00571FC1`, `005750AF`). For families 0–4 it walks
  `word[buf+8]` 8-byte records at `buf+0x0C`, calls `00575E80` on each, and writes the 0/1
  result through `00315910(cat, i, result)` — **set/clear bit `bases[cat] + i` of the save
  `+0x32CC` bit array**. `cat` is the family remapped through `byte[00D23750]` =
  `{0,1,2,3,4,6}` (monster lands on category 6).
- `00577550` kind 5 (monster) instead walks 16-byte records, evaluates `00576E30` per slot, and
  writes the per-record byte at save `+0x3604` via `00315AD0(6, recIdx, slot, val)` — **bit
  `slot` of byte `+0x3604 + recIdx`**, the bestiary's 8-slot flag byte per monster.
- `00576920(tab)` — the tab-label driver: iterates `word[00D23758 + tab*2]` entries
  (bounds `{160, 96, 64, 120, 56, 512, 48, 30}`) reading `003154B0`/`00315670` — the `+0x32CC`
  bit getter and the bank-6 `+0x3604` byte-slot getter — to count unlocked entries / find the
  first newly-unlocked slot for the "new" badge.

So `+0x32CC` = the unlock-bit array (indexed `bases[cat] + record`), `+0x334C`/`+0x336C` =
the bit/nibble *input* banks the predicates read, `+0x3404` = the counter bank (kill counts),
`+0x3604` = the monster slot-flag bytes. All are save-payload offsets resolved through
`002536A0`/`002EF2B0` — see [the persistent-flag-banks contract](../../14-Story-Event-Quest-Hunt/CONTRACT-persistent-flag-banks.md)
for the save-side ownership.

## `hdat` — the record headers (`menuhandbook_<fam><NNN>.dat`, the low-numbered files)

```
+0x00  char[4]  magic      'hdat'
+0x04  u32      tag        103
+0x08  u16      baseOrdinal family-global index of this file's first record
                            (running-total chain, zero violations corpus-wide)
+0x0A  u16      count      records in this file
+0x0C  u32      tim2Off    offset of the trailing TIM2 page, or 0xFFFFFFFF
+0x10  u16      stringsOff offset of the encoded-string blob
+0x12  u16      recOff[count] per-record offsets into the record region
…      rec[]     variable-length records — `len = 12 + 4·strCount` (below)
…      strings   encoded-string blob (record fields index into it)
…      TIM2      at most one page image per file
```

**Record layout** — corpus-proven on all **6,300** records, zero violations:

```
+0x00  u8    strCount   number of u32 string-blob offsets — {1, 2, 3, 7} observed;
                        record length is exactly 12 + 4·strCount
+0x01  u8    arg        locale-invariant cumulative serial — corpus union is a set of
                        contiguous blocks in a global index space: story 14–35, person
                        57–74, knowledge 123–153, world 242–255 wrapping to 0–8 (mod
                        256), tutorial/monster all-zero. Non-decreasing within a family
                        (9 violations = the world wrap), nonzero on multi-string records
                        too, increments tracking unique-textId changes. **No native
                        reader located**: `byte[rec+1]` never appears in the handbook
                        family (`00575000–00578000` sweep) and `00577A40`/`00575D10`/
                        `00577970`/`005760A0` all skip it — authored-order serial,
                        semantics unbound (possibly dead-authored).
+0x02  u16   globalIdx  the family-global record ordinal — equals file baseOrdinal + i
                        (verified: knowledge001 starts at 88, monster001 at 71)
+0x04  u32   strOff[strCount]  offsets into this file's string blob (relative to stringsOff)
tail (8 B)     {u16 a; u16 b; u16 c; u8 chapter; u8 pad} — **read by the line builder
               `00576300` into out+0x48/+0x4A/+0x4C/+0x4E**; ships constant
               `00 80 00 80 FF FF FF` + chapter (the reader substitutes the same
               0x8000/0xFFFF/0xFF defaults when the record is absent — the sentinels are
               "unset" markers the UI resolves downstream). Chapter byte: 0xFF = none
               (world/person/knowledge), sparse section ids elsewhere (story: 20
               distinct values 0–25)
```

So each `hdat` record = `{kind, arg, ordinal, string-offset list, fixed sentinel tail,
chapter}` — one logical handbook entry's display strings (type 3 = monster name/lore/title
triple, type 7 = the five-record special shape in `monster003`), while the matching `hchk`
record carries its unlock gate.

**The string blob entries and their readers `00577A40` / `00576300`.** `strOff[slot]` is
blob-relative to `stringsOff`; every entry is `{u16 textOff = 4; u16 flags = 0; encoded
NUL-terminated text}` — `word[entry]` is a self-relative offset to the text payload
(`00576300` computes `entry + word[entry]`; `0xFFFF` = empty → the default string
`01CEB638`), constant `4` across all **12,168** shipped entries (corpus-verified), and the
payload uses the section-002 message encoding (`0x10` opcode bytes visible in the stream).

`00576300(out)` is the **record line builder** — the main content path: resolves the
selected record (`obj+0xCE` global ordinal window-checked against `base@+8`/`count@+0xA`),
copies the 8-byte tail to `out+0x48…+0x4E`, writes `out+0x00` = global ordinal, then loops
`slot = 0..strCount` calling **`00576E30(familyOrd, globalIdx, slot)` — the per-slot hchk
gate** — and only materializes `strBlob + strOff[slot]` (via the `word` offset) into the
`out+0x08` slot array when the gate passes; `out+0x03` = the count of gated-in slots. So
`strOff[slot]` and the record's `hchk` slot vector are **1:1** — each display line is
independently gated (monster: name/lore/title lines revealed as kill thresholds pass).
`00577A40(root, slot)` is the second blob reader: it resolves the bound `hdat`
resource (`root+0x110` object; its `word[obj+0xCE]` must lie in the buffer's
`[base@+8, base+count@+0xA)` window), walks `recOff[]` at `+0x12` to the record, bounds-checks
`slot < strCount`, and lands on `stringsOff + strOff[slot]`. It then interprets the same
4-byte header as **an embedded op-program prefix** — `{u8 textOffLo=4; u8 0; u8 nOps; u8 0;
{u8 op; u8 target; u8 arg; u8 pad}[nOps]}` at `entry+4` — executing `op 0/2/3` as `00315CD0` nibble writes (`set` / `+arg sat 15` /
`−arg clamp 0`) and `op 1` as `00315A20(target, arg==1)` bit writes — the same `+0x336C` /
`+0x334C` save banks the `hchk` predicates read. **All 12,168 shipped programs carry
`nOps = 0`** — the executor is dead-on-ship; whether ops were ever authored is open. The
return value is a plain 1/0 success flag; the string pointer itself is not consumed by this
path (display text comes from the `hctg` record's `textId`). The `arg` byte's target remains
open.

## The buffer graph — who owns what

Root object at `02CA9738` (the handbook menu singleton):

| offset | content |
| --- | --- |
| `+0xC8` … `+0xF0` | six family `hchk` buffers (48-byte stride, `{u16 count; rec[]}` at +8/+0x0C) |
| `+0xF8` | `menuquest.dat` (qstd) resource handle — consumed by `00576CA0`'s family-6 path (`0037F060(handle, 1)`) |
| `+0x100` | state bits — bit 0/1 set on load completion (`00576F50`), bit 3 armed by `00575F10` |
| `+0x108`, `+0x110`, `+0x118` | bound resource objects — `+0x108` = `hctg` (`00576030`/`005760A0`/`00577970`), `+0x110` = `hdat` (`00577A40`: `+0xCE` = selected record's global ordinal, window-checked), `+0x118` = `himg` (`00575DD0` → `00575B80` page switcher) |
| `+0xC0` | global pointer stored by `00577A00` |

`00576F50` performs the bind: checks resource slots 7/8 (`002F8040`), queues the six family
loads through `002491B0` using the `00D23740` base table, stores the six handles at `+0xC8…+0xF0`,
additionally loads `0x128` (`menuquest.dat`) into `+0xF8`, then sets `+0x100` bit 1.

## Unbound / residual items

- `hctg` `+0x08` high 12 bits — written to descriptor `out+0x04` but **unread by all three
  `00576030` callers** (dead-on-ship payload; textId-shaped values, semantics unbound).
- `hctg` monster tail `v1`/`v2`/`v3` — dead-authored: the tail base is computed only by
  `005760A0`, which reads `v0` alone (complete `root+0x108` consumer set enumerated).
  `v3` = a 15-value bestiary-category id that redundantly encodes `rec+0x0A`'s flag.
- `hchk` `+0x0A` — dead header field: 18 for the four paged-list families, 0 for
  tutorial/monster; counts nothing in-file, no reader located. Possibly a vestigial
  rows-per-page constant.
- `hchk` `+0x03` flag byte — `0x80` on every gated record, `0x00` on record 0 of every file
  and all tutorial records (180 zeros / 2,664 `0x80`); confirmed **not read** by the
  evaluator `00575E80` (which touches `+0x00`/`+0x01`/`+0x02`/`+0x04`/`+0x06` only) —
  authored "gated" marker with no consumer, effectively dead data.
- `hdat` `arg` byte — corpus-characterized as a locale-invariant global serial (family
  blocks in a shared index space, wraps mod 256) with **no located native reader**;
  semantics unbound, possibly dead-authored. `strOff[]` slot roles are partially bound: entries carry a
  constant `04 00 00 00` header + section-002-encoded NUL text, and `00577A40`'s embedded
  op-program (nibble/bit writes into `+0x336C`/`+0x334C`) ships empty in all 12,168 entries —
  the per-slot display roles and whether ops ever authored remain open.
- The `b3`/`v[7]` semantics are *recorded as written*; no claim beyond the disassembled reads.

`00577100` (125 B) is the `02CA9738` once-register `00574E80` runs: only while the global is absent it `00244F50(0x120, 005771F0, &ctx)`s — the context carries flag byte 1, a zero dword, the caller's `rcx`, and a zero qword — and returns 1; an already-present global returns 0. The handbook state object's install guard.

Interior anchor `0057714D` (function `00577100`).

`00576CA0` (115 B) is the per-kind membership predicate `00571F60`/`00576740` consult: `ecx` < 0 or > 7 returns 1 vacuously; kinds 0..5 and 7 read bank byte `00D23750[kind]` and return `003154B0(byte, edx)` != 0 — the flag/nibble test; kind 6 instead requires `[02CA9738]+0x100` bit 2 clear and `+0xF8` live, then returns `0037F060(+0xF8, 1)` != 0 — the object-presence arm.

Interior anchor `00576CFF` (function `00576CA0`).

`005768E0` (62 B) is the kind-5 flag read `00577550`'s sync uses: requires `rcx`, `edx == 5`, and `[rcx+0xF0]`'s `+0xC` table; entry `r8d` sits at stride `0x10` — word `+0xE` bit 1 returns 2, bit 0 returns 1, anything else (and every failed gate) returns 0. The 16-byte stride matches the kill/state vector records.

Interior anchor `0057690B` (function `005768E0`).

`00576740` (286 B) is the section-header resolver this page names, measured: `02CA9738`'s `+0x108` record must have `+0xC9` == 1 and a live `+0xF0` table; `00576A50(&rec, dx)` resolves the caption and `[out]` takes the result pointer with `+8` = `dx`; then the `rdx + u16[+0xA]`-relative table is scanned at stride `0x0C` for entries whose `+4` word equals `dx` — the first match index lands in `[out+0xA]`, the total match count in `[out+0xC]`, and `[out+0xE]` counts only the members `00576CA0(i, [rsi+8] & 0xF)` passes; returns 1, or 0 when any gate fails.

Interior anchor `00576827` (function `00576740`).

`00576030` (98 B) is the `+0xF0`-table row read `00570BF0`/`00571F60`/`00574080` share: gates on `02CA9738`'s `+0x108` record being live with `+0xC9` == 1 and a `+0xF0` table present; then copies `tbl[+0xD2]` -> `[out]`, `tbl[+8] >> 4` -> `[out+4]`, and words `+0x12`/`+0xE`/`+0x10` -> `[out+6]`/`[out+8]`/`[out+0xA]` — returns 1, else 0 on any failed gate.

Interior anchor `0057605F` (function `00576030`).

`00575F10` (281 B) is the three-record teardown `00574E80` runs on bind: sets `02CA9738`'s `+0x100` bit 3, then for each of `+0x108`/`+0x110`/`+0x118` sets `+0xEC` bit 0, clears `+0xD3`, and branches on `+0xC9` — <= 1 runs `00575640(rec)`, clears the bit, and releases through `00244F00(rec)`; == 2 is promoted to 3; already-3 is left alone. A null global returns early.

Interior anchor `00575F5F` (function `00575F10`).

`00575E80` (139 B) is the 8-byte conjunctive gate the unlock predicates use: record `{b0, b1, b2, w4, w6}` — `b0 != 0xFF` requires `00315470(b0) == b1`; `b2 != 0xFF` requires `00315620(b2)` nonzero; `w4 != 0xFFFF` requires `0032A8A0(w4)` nonzero; `w6 != 0xFFFF` requires `00265270() >= w6`. Returns 1 only when every non-skipped arm passes.

Interior anchor `00575EB9` (function `00575E80`).

`00575DD0` (173 B) is the `+0x118` (himg) content submit this page's table names: requires `this+0x118` live and `02CA9738`'s `+0x108` `+0xC9` == 1 with `+0xF0` table; `r8w` must be under `tbl[+0x10]` and resolves `u16[tbl + tbl[+0xC] + r8w*2]` (reject `0xFFFF`); clears `+0x100` bit 9; builds `{b=dl, w=entry, w=r8w}` -> `00575A50` and, on success, `00575B80(this+0x118)` then `00247510(this, 0x10, 2)`.

Interior anchor `00575E1B` (function `00575DD0`).

`00575D10` (186 B) is the `+0x110` (hdat) sibling of `00575DD0`: same `02CA9738`/`+0x108`/`+0xF0` gating, but `r8w` bounds-checks against `tbl[+0xE]` and the entry sits at stride 12 — `tbl + tbl[+0xA] + r8w*12`, word `[ent+6]` feeds the descriptor; clears `+0x100` bit 8, validates through `00575A50`, and notifies `00247510(this, 0x10, 1)` — the subtype-1 arm of the same `{0x10, sub}` message. (The `00247510` notify, `00575A50` validation and the `00244F50`/`00246AD0` create/bind helpers these sections name are shared presentation-layer machinery — fan-in on the helpers, not a handbook relationship.)

Interior anchor `00575D68` (function `00575D10`).

`005755D0` (111 B) is the paired flag write `00574E80` performs on the `01E0C1F8`/`01E0C248` `.data` records: for each, `0024A5A0(rec)` must yield a live object, then `[obj+0x38]` bit 7 is rewritten to `!(ecx & 1)` — the arg's low bit inverted into the high bit.

Interior anchor `0057560D` (function `005755D0`).

`00574E00` (125 B) is the `+0x108` (hctg) lazy-create `00574E80` runs: `002F9860(0x4BC)` resolves the caption text and `00574A00(text, 0)` registers it; while `this+0x108` is still null it `00244F50(0xC0, 0056F410, &ctx)`s with context `{0, this, this+0x128}` and stores the created record.

Interior anchor `00574E36` (function `00574E00`).

`00574D00` (244 B) is the `+0xD8`/`+0xE0` record-pair create `00574E80` runs: `00244F50(0x178, 0056F810, &ctx)` lands in `+0xD8` and `00244F50(0xD0, 0056F550, &ctx)` in `+0xE0`, both with context `{0, this, this+0x128}`; when `02CA9718`'s `+0xC0` bit 6 is set it notifies `00247510(this, 0x8001, 6)`, else it defers through `00246AD0([+0xD8]+0xC0, +0xD8)` and the same for `+0xE0` — an immediate-bind versus deferred fork on a global flag.

Interior anchor `00574D8B` (function `00574D00`).

`00574CB0` (76 B) is the `00574E80` handler factory `00281ED0` dispatches: `00244F50(0x130, 00574E80, &{0,0,0})` — a `0x130`-kind create with an all-zero context.

Interior anchor `00574CD3` (function `00574CB0`).

`00576D20` (120 B) is the kind-mapped flag predicate sibling of `00576CA0` that `00577C30` (save pane) and `00570930` consult: kinds other than 5 read the same `00D23750` bank byte and tail-jump `003156E0(byte, edx)`; kind 5 instead loops `ebx` 0..7 requiring both `00576E30(5, edx, ebx)` and `00315670(6, edx, bx)` — returns 0 on the first failed pair, 1 when all eight pass.

Interior anchor `00576D6B` (function `00576D20`).

`00574A00` (141 B) is the `02CA9718` `+0x100` release-and-recreate `00574E00`/`0056F2A0`/`00574A90` invoke: a live `+0x100` object is released through `00245020` when the global's `+0xC0` byte has bit 5 set, else `00244F00`, and the slot nulled; it then re-registers `00244F50(0xD8, 00574AD0, &ctx)` with context `{0, ecx, edx}` — the caption record's handler swap.

Interior anchor `00574A76` (function `00574A00`).

`00570930` (167 B) is the packed-word append `00571F60` runs on the page object: `rbx = this + 0xF0 + word[+0xEE]·2` selects the next u16 slot, `00576D20(byte[+0xE8], dx)` supplies the flag verdict, and the slot is rebuilt as `(dx & 0x3FF) << 4 | (kind != 5) << 15 | (verdict == 0) << 14 | 1`; `+0xEE` then increments — a {kind-gate, verdict, index} triple packed per entry.

Interior anchor `0057095D` (function `00570930`).

`0056F5F0` (340 B) is the item-list populate `0056F810`/`0056FAD0` run on the `+0xD8` record: `0056F750(this+0xCE)` yields the count into `[+0xCD]`, `002CD4D0(this+0xD8, this+0xE8)` preps the record, and `02CA9718`'s `+0xC0` bit 6 clear selects `002526F0(3, 6)` for the highlight index `r15d` (else 0). For `i < +0xCD`: `bl = [this+0xCE + i]`, `cl = min(bl, 3)`... `bl < 4 ? bl : 0` selects the `00D23688` 6-byte triple, `002CD3C0(tbl.w0, tbl.w2)` resolves the text, and `bl == r15d` marks `ebp = i`. `002C9BF0(this, this, this+0xD8, 0, {1.0f, 01E0C3B0})` then creates the icon object into `[+0x168]`, `002D46F0(obj, ebp)` selects it, and `[[+0x170]+0x20]`'s `0020E600` result's `+0x1BC`/`+0x1BE` words land in `[+0x98]`/`[+0x9A]`.

Interior anchor `0056F69F` (function `0056F5F0`).

`0056F2A0` (281 B) is the pane-kind switch `00574E80` runs: `dl` lands in `[+0xC8]`; kinds <= 5 call `00577880(dl)`, kinds 6/7 call `005776D0` with kind 7 adding `005704E0(0xC8)`, kinds > 7 skip both. Kind 5 with `+0xCC` bit 3 clear then creates the named child — `00249580()` -> `002493D0(obj, 7, 0xD0, 2, "handbook2_c", 2)` into `[+0xF8]`, `00249410` registers — while any other kind with the bit set releases `[+0xF8]` through `0024A680(obj, 1)` and clears it. Every path ends `002F9860(00D236A0[min(dl, 8)·3].w0)` -> tail `00574A00(text, 0)` — the caption rebind.

Interior anchor `0056F39B` (function `0056F2A0`).

`00577880` (107 B) is the kind <= 5 arm `0056F2A0` calls on `02CA9738`: a set `+0x100` bit 0x40 returns 0 early; otherwise a `{cl, 0}` scratch pair is built, and when `+0x108` is live `+0x100` bit 7 clears, `00575A50(rec, &scratch)` runs, and a nonzero verdict posts `00247510(this, 0x10, 0)`. Returns 1 on every open path.

Interior anchor `005778C8` (function `00577880`).

`005776D0` (239 B) is the kind-6/7 arm `0056F2A0` calls on `02CA9738` (a null global returns 0): `+0x100` is masked to clear bits 7-9 and set bit 6, then each of `+0x108`/`+0x110`/`+0x118` is walked — a `+0xC9` byte <= 1 runs `00575640(rec)` and posts `00247510(this, 0x10, 3|4|5)`, a byte of 2 is promoted to 3, higher bytes are left. Returns 1 — the three-record state promote/teardown.

Interior anchor `0057775E` (function `005776D0`).

`005704E0` (68 B) is the `02CA9718` `+0x110` lazy-create `0056F2A0` runs on kind 7: a live slot is a no-op; a null slot `002CCCA0(00D236E0, ecx)`-materializes the object into `+0x110` and tail-enters `002CD150(0x37)`.

Interior anchor `00570511` (function `005704E0`).

`003934F0` (153 B) is the record-factory fan-out `00574E80` runs on bind: for each of the arg-count `0x18`-stride source rows at `r8` it calls `002493D0(r15, 7, [row+0], [row+?]`, passing the row's lead dwords and the `[rsi]`-or-2 selector, stores the new record into the out array at `[r14 + i*8]`, and stamps `[rax+0x40]` with the row's `+0x10` dword - the handbook's N-record build.

Interior anchor `00393554` (function `003934F0`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-CONTRACT)

- **ActorEntity — MECHANICAL (6 edges).** 6 ActorEntity-side calls into shared helper(s) the page cites (`SaveImage_GetPersistentPayloadBase` (002EF2B0), `WorldTransition_GetActiveOrPendingFieldId` (003148F0), `002B58B0`) - the helpers' general call surface, not a ActorEntity relationship of this page's subjects.
- **Audio — MECHANICAL (2 edges).** 2 Audio-side calls into shared helper(s) the page cites (`SaveImage_GetPersistentPayloadBase` (002EF2B0), `WorldTransition_GetActiveOrPendingFieldId` (003148F0)) - the helpers' general call surface, not a Audio relationship of this page's subjects.
- **CombatAI — CLIENT (1 edge).** 1 inbound (CombatAI bodies `AiOrder_EvaluateTargetSelector` (00301AD0) call page-cited `BattleEncodedId_DispatchQueryMode0Value` (00309EC0)). Substantive edges include `BattleEncodedId_DispatchQueryMode0Value` (00309EC0) is called by `AiOrder_EvaluateTargetSelector` (00301AD0).
- **CombatAction — CLIENT (4 edges).** 4 inbound (CombatAction bodies `00317BC0`, `00317C80`, `002FA740` call page-cited `BattleEncodedId_DispatchQueryMode0Value` (00309EC0), `WorldTransition_GetActiveOrPendingFieldId` (003148F0)). Substantive edges include `BattleEncodedId_DispatchQueryMode0Value` (00309EC0) is called by `00317BC0`; `BattleEncodedId_DispatchQueryMode0Value` (00309EC0) is called by `00317C80`; the remaining edges run through shared helpers the page cites.
- **CoreRuntimeScheduling — CLIENT (1 edge).** 1 inbound (CoreRuntimeScheduling bodies `001EC760` call page-cited `FieldData_GetVariable0` (00265270)). Substantive edges include `FieldData_GetVariable0` (00265270) is called by `001EC760`.
- **Gameplay — CLIENT and SERVICE (3 edges).** 1 inbound (Gameplay bodies `0031C5D0` call page-cited `BattleEncodedId_DispatchQueryMode0Value` (00309EC0)); 2 outbound (page-cited `0035D330`, `00576A50` call Gameplay bodies `0031C5D0`, `BattleEncodedId_DispatchQueryMode0Value` (00309EC0)). Substantive edges include `BattleEncodedId_DispatchQueryMode0Value` (00309EC0) is called by `0031C5D0`; `00576A50` calls `BattleEncodedId_DispatchQueryMode0Value` (00309EC0); the remaining edges run through shared helpers the page cites.
- **Input — CLIENT (3 edges).** 3 inbound (Input bodies `InputGameplay_ArbitrateDigitalInputAndModalState` (00253C70), `00291D90` call page-cited `0024A680`, `FieldData_GetVariable0` (00265270), `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` (0032A8A0)). Substantive edges include `0024A680` is called by `00291D90`; `FieldData_GetVariable0` (00265270) is called by `InputGameplay_ArbitrateDigitalInputAndModalState` (00253C70); `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` (0032A8A0) is called by `InputGameplay_ArbitrateDigitalInputAndModalState` (00253C70).
- **Items_Equipment_Shops_License — CLIENT (1 edge).** 1 inbound (Items_Equipment_Shops_License bodies `Equipment_CheckItemEligibleForSlot` (00317930) call page-cited `BattleEncodedId_DispatchQueryMode0Value` (00309EC0)). Substantive edges include `BattleEncodedId_DispatchQueryMode0Value` (00309EC0) is called by `Equipment_CheckItemEligibleForSlot` (00317930).
- **Movement — MECHANICAL (3 edges).** 3 Movement-side calls into shared helper(s) the page cites (`WorldTransition_GetActiveOrPendingFieldId` (003148F0)) - the helpers' general call surface, not a Movement relationship of this page's subjects.
- **PlatformOnlineAchievements — CLIENT and SERVICE (30 edges).** 24 inbound (PlatformOnlineAchievements bodies `003160C0`, `00315E90`, `003154B0` call page-cited `002536A0`, `00315420`, `FieldData_GetVariable0` (00265270)); 6 outbound (page-cited `003154B0`, `005760A0`, `00576920` call PlatformOnlineAchievements bodies `00315420`, `003154B0`, `00316930`). Substantive edges include `002536A0` is called by `00315420`; `002536A0` is called by `00315390`; `002536A0` is called by `00316930`; `002536A0` is called by `00315820`; the remaining edges run through shared helpers the page cites.
- **Presentation — CLIENT and SERVICE (23 edges).** 22 inbound (Presentation bodies `00579420`, `002B7B80`, `002BAF80` call page-cited `0024A5A0`, `00247510`, `00249410`); 1 outbound (page-cited `00577C30` call Presentation bodies `0037E5B0`). Substantive edges include `00247510` is called by `00579420`; `00247510` is called by `002D2DB0`; `00249410` is called by `002B7B80`; `00249410` is called by `002BAF80`; the remaining edges run through shared helpers the page cites.
- **SaveLoad — CLIENT (4 edges).** 4 inbound (SaveLoad bodies `00280140`, `00582790` call page-cited `00245020`, `00249410`, `00249580`). Substantive edges include `00249410` is called by `00582790`; `00249580` is called by `00582790`; the remaining edges run through shared helpers the page cites.
- **Save_Load_Settings — CLIENT and SERVICE (12 edges).** 9 inbound (Save_Load_Settings bodies `SaveImage_FinalizeHeaderAndChecksum` (00583D60), `SaveWrite_OperationStateCallback` (0057E4D0), `0057E950` call page-cited `00247510`, `00245020`, `WorldTransition_GetActiveOrPendingFieldId` (003148F0)); 3 outbound (page-cited `SaveImage_GetPersistentPayloadBase` (002EF2B0), `WorldTransition_GetActiveOrPendingFieldId` (003148F0), `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` (0032A8A0) call Save_Load_Settings bodies `SaveImage_GetPersistentPayloadBase` (002EF2B0), `SaveImage_GetActiveRuntimeBuffer` (002EF640)). Read (2026-09-30, SWE2-CONTRACT): the save controllers' calls into `00247510` are the shared helper, MECHANICAL. Two edges carry the relationship: the persistent-flag gate `0032A8A0` that a handbook row's `+0x04` id is tested with is also run by `SaveImage_FinalizeHeaderAndChecksum` (00583D60), and the page-cited payload-base getter `SaveImage_GetPersistentPayloadBase` (002EF2B0) resolves through the save layer's `SaveImage_GetActiveRuntimeBuffer` (002EF640). Substantive edges include `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` (0032A8A0) is called by `SaveImage_FinalizeHeaderAndChecksum` (00583D60); `SaveImage_GetPersistentPayloadBase` (002EF2B0) calls `SaveImage_GetActiveRuntimeBuffer` (002EF640); the remaining edges run through shared helpers the page cites.
- **Script_VM_Native_Bridge — CLIENT (3 edges).** 3 inbound (Script_VM_Native_Bridge bodies `00357450`, `0033F310`, `0034E0B0` call page-cited `WorldTransition_GetActiveOrPendingFieldId` (003148F0), `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` (0032A8A0)). Substantive edges include `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` (0032A8A0) is called by `0034E0B0`; the remaining edges run through shared helpers the page cites.
- **Spawn_Encounter_Lifecycle — MECHANICAL (1 edge).** 1 Spawn_Encounter_Lifecycle-side calls into shared helper(s) the page cites (`WorldTransition_GetActiveOrPendingFieldId` (003148F0)) - the helpers' general call surface, not a Spawn_Encounter_Lifecycle relationship of this page's subjects.
- **StoryEvent — CLIENT (1 edge).** 1 inbound (StoryEvent bodies `001ED240` call page-cited `FieldData_GetVariable0` (00265270)). Substantive edges include `FieldData_GetVariable0` (00265270) is called by `001ED240`.
- **Story_Event_Quest_Hunt — CLIENT and SERVICE (18 edges).** 14 inbound (Story_Event_Quest_Hunt bodies `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` (0032A8A0), `PersistentFlag_QueryAuthoredThresholdSchedule` (00377970), `PersistentFlag_QueryBank64B` (0032AA00) call page-cited `SaveImage_GetPersistentPayloadBase` (002EF2B0), `FieldData_GetVariable0` (00265270), `PersistentFlag_QueryAuthoredThresholdSchedule` (00377970)); 4 outbound (page-cited `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` (0032A8A0), `0056F750`, `0056FAD0` call Story_Event_Quest_Hunt bodies `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` (0032A8A0), `PersistentFlag_QueryAuthoredThresholdSchedule` (00377970)). Substantive edges include `FieldData_GetVariable0` (00265270) is called by `PersistentFlag_QueryAuthoredThresholdSchedule` (00377970); `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` (0032A8A0) calls `PersistentFlag_QueryAuthoredThresholdSchedule` (00377970); the remaining edges run through shared helpers the page cites.
- **UI — CLIENT and SERVICE (166 edges).** 155 inbound (UI bodies `00571F60`, `00281AE0`, `002D70F0` call page-cited `00245020`, `0035D330`, `0024A5A0`); 11 outbound (page-cited `00281ED0`, `0056F5F0`, `0056F810` call UI bodies `00291D80`, `002C2280`, `005678A0`). Read (2026-09-30, SWE2-CONTRACT): the widest fan-ins are UI-wide helpers the page cites (`00247510`, `00245020`, `0035D330`, `002B58B0`), MECHANICAL. The relationship is menu code building image records the way the handbook does: the menu widgets `00558FB0`, `00561390` and `00562F90` create named child records through `002493D0` (the creator the handbook calls for `handbook2_c`), and `00253780` loads its handles through `002491B0`. Substantive edges include `002493D0` is called by `00558FB0`; `002493D0` is called by `00561390`; `002493D0` is called by `00562F90`; `002491B0` is called by `00253780`; the remaining edges run through shared helpers the page cites.
- **World — CLIENT (1 edge).** 1 inbound (World bodies `003C63A0` call page-cited `0024A680`). Substantive edges include `0024A680` is called by `003C63A0`.
- **WorldAreaField — CLIENT and SERVICE (50 edges).** 44 inbound (WorldAreaField bodies `00576A50`, `WorldTransition_StageFieldTransition` (003145E0), `WorldPersistence_ResetBanksForFieldTransition` (0026DB30) call page-cited `SaveImage_GetPersistentPayloadBase` (002EF2B0), `WorldTransition_GetActiveOrPendingFieldId` (003148F0), `FieldData_GetVariable0` (00265270)); 6 outbound (page-cited `003154B0`, `PersistentFlag_QueryAuthoredThresholdSchedule` (00377970), `00575E80` call WorldAreaField bodies `FieldData_GetVariable0` (00265270), `00576A50`, `WorldTransition_GetActiveOrPendingFieldId` (003148F0)). Substantive edges include `00255060` is called by `00576A50`; `00255120` is called by `00576A50`; `FieldData_GetVariable0` (00265270) is called by `WorldTransition_StageFieldTransition` (003145E0); `FieldData_GetVariable0` (00265270) is called by `003EAA70`; the remaining edges run through shared helpers the page cites.
