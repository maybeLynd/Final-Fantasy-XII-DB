---
system: The `gmap` map-guide text files — `worldmap/menumap_guide00..04.bin`, 77 guide strings and an optional TIM2 per locale
category: 02-Resource-And-Asset-Pipeline
status: AUDITED
owner_layer: CodeDomain:Presentation.Menu
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the requester 003C1DF0 and the readers 003BD890 / 003BD8F0 / 003BD860 disassembled from the shipping
    image; an immediate sweep for the id range 0x496..0x4A5 with the three documented 003BC2D0 requests as
    its positive control; every shipped copy decoded and size-closed
corpus_validated: "all 35 menumap_guide00..04.bin copies (5 units x 7 locales) close under the layout; 30 carry an embedded TIM2 ending exactly at EOF; guide00's 77 entries join menumap_common section 3 record by record 77/77 (shifted control 0/77); .fst sizes exist for kind 7 ids 0x496..0x49A only, 2026-09-29"
archive_formats:
  - "gmap | explained | menumap_guide##.bin (.bin member): {gmap, u32 0x64, u16 textOff, u16 tim2Off, u16 0, u16 count, {u16 gate, u16 key, u16 textRel, u16 0}[count], strings, optional TIM2} - (kind 7, 0x496 + record byte +4) by 003C1DF0 into widget +0xF8, read by 003BD890 / 003BD8F0; only guide00 is ever requested, sections 2-3"
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-gmap-falsification-pass-1
  crossref_clean: true
  reopened_count: 0
  promoted: 2026-10-01 DOCUMENTED -> AUDITED by SWE2-AUDIT-SPEC (FRONTIER eligibility census sweep): falsification record opus-gmap-falsification-pass-1; audit_crossrefs at HEAD reports 0 unresolved findings; cross-subsystem neighbours dispositioned in their section; killer observations recorded in the pass; promoter is not the last substantive author (last substantive commit: OPUS)
---

# The `gmap` map-guide text files — `worldmap/menumap_guide00..04.bin`

> **The map menu's guide strings.** Each file is a small header, one 8-byte entry per guide line
> (a gate/key pair and a text offset), the zero-terminated strings, and — in 30 of the 35 shipped
> copies — a TIM2 picture after the text. The map widget requests file `0x496 + n`, and **`n` is 0
> in every shipped selection record, so only `menumap_guide00.bin` is ever loaded**; guide01–04
> ship and nothing selects them. `OPUS-REQ-DATA-BUCKET-MEMBER-FORMATS` (the `.bin` bucket's member `gmap`).

**Corpus validation, before anything else.**

| | |
|---|---|
| files | `ps2data/image/ff12/myoshiok/<lang>/worldmap/menumap_guide00..04.bin` — 5 units, **35** entries, 3,632–20,032 B |
| closure | text section at `0x10 + 8·count`; strings back to back; file ends at `align4(text end)`; where a TIM2 is present it starts at `align16(text end)` and `'TIM2' + 16 + Σ picture sizes` ends exactly at EOF |
| TIM2 | 30 of 35 carry one; the five Latin-alphabet `guide00` copies (`us`/`de`/`es`/`fr`/`it`) do not — their TIM2 offset points at or past the file end |
| check | [`check_gmap.py`](../../_index/candidates/bucket-members-0929/checks/check_gmap.py) → [output](../../_index/candidates/bucket-members-0929/checks/check_gmap.out.txt): 198 checks, FAILS 0 |

## 1. What the player sees

The explanatory line the world-map menu shows for the selected map entry.

## 2. The layout

```struct GmapHeader base=file size=0x10
+0x00  char[4]  magic          'gmap' - not compared by the readers found
+0x04  u32      tag            0x64 - not read by the readers found
+0x08  u16      textOff        start of the string section = 0x10 + 8*count
+0x0A  u16      tim2Off        start of the TIM2 (0xFFFF = none, as the reader tests)
+0x0C  u16      zero           0 - not read
+0x0E  u16      count          entries
```

```struct GmapEntry base=file+0x10 size=0x8
+0x00  u16      gate           equals menumap_common section-3 record's gate at the same index - not read here
+0x02  u16      key            0x40xx; equals the same record's key - not read here
+0x04  u16      textRel        offset of the string from textOff, ascending; 0xFFFF = none
+0x06  u16      zero           0
```

## 3. The loader contract

**Request.** `003C1DF0` walks [`cmap`](cmap-menumap-common-sublocation-directory.md) section 3
through its record picker, stores the chosen record at widget `+0xF0`, then requests kind 7 with
**id `0x496` + the record's byte `+4`** (`003C1EA7`, `add r8d, 0x496` at `003C1EB1`, call
`003C1EBC`) and stores the data at widget `+0xF8` (`003C1ECC`). Byte `+4` is 0 in all 77 records
in all nine locales, so the request is always `0x496` = `menumap_guide00.bin`; the `.fst` has sizes
for `0x496`–`0x49A` (the five files) and none for `0x49B`–`0x4A5`.

**Search control.** An immediate sweep for `0x497`–`0x4A5` followed by a request call finds only
`003C1EB1`; the same sweep over `0xA2`–`0xA4` finds the three documented `003BC2D0` requests.

| field | read by | rejected if | result |
|---|---|---|---|
| `count` | `003BD890` (`003BD8C2`), `003BD8F0` (`003BD8F8`) | `index ≥ count` → null | — |
| entry `textRel` | `003BD890` (`003BD8CE`), `003BD8F0` (`003BD930`) | `0xFFFF` → null | `low32(blob) + textOff + textRel` |
| `textOff` | `003BD8DE`, `003BD93A` | — | — |
| `tim2Off` | `003BD8F0` (`003BD915`) | `0xFFFF` → null | `low32(blob) + tim2Off`, checked by the TIM2 test `0039BEC0` (called from `003BC7C3`) |
| gate, key, `+0x04`, `+0x0C` | none found | — | — |

`003BD890` indexes the file by the chosen record's word `+6` (its sequence number) and gates on
widget `+0xD0` bit `0x40`; `003BD860` returns the cached picture pointer at widget `+0x108`. The
text and picture pointers are passed together to the menu's text-box builder (site in the check output).

## 4. Not claimed

- **A latent over-read (inferred, not run).** For the five Latin-alphabet `guide00` copies the
  TIM2 offset is not `0xFFFF` but points at or past the end of the file, so `0039BEC0` compares
  four bytes beyond the data against `'TIM2'`; for `us` that address is one byte past the loaded
  buffer (0x1278 rounded to 64 = 0x1280).
- How the `0x18xx` text codes use the embedded TIM2; why guide01–04 exist (`ch`/`in` guide01
  carry `0xFFFF` keys, `kr` guide01 has 32 entries); whether anything writes the selection
  record's byte `+4` at run time (no writer was searched for); widget `+0xF8` readers were
  sought only among the 77 functions that reference the widget by rip, its message procedure and
  `003BC970`.

## 5. Related

- [`cmap`](cmap-menumap-common-sublocation-directory.md) section 3 — the 77 selection records this file is joined to.
- [`amap`](amap-menumap-area-table.md), [`wmap`](wmap-menumap-world-map-graph.md), [`lmap`](lmap-menumap-location-graph.md) — the other map-menu tables.
- [TIM2 and the seven-slot registry](tim2-images-and-the-seven-slot-registry.md) — the embedded picture's format.
- [The bucket member formats](../../_index/candidates/bucket-members-0929/README.md).

## Crossings into other layers — pass 22 (SWE2-DATA, 2026-09-29)

- **UI — CLIENT, body read.** The requester `003C1DF0` and the readers `003BD890` / `003BD8F0` /
  `003BD860` belong to the world-map menu widget (`02B457E0`), a UI-layer object; the UI layer is
  the only consumer of this file. Their other callers draw the menu and are that layer's pages.

## Falsification pass 1 — 2026-09-29 (OPUS): every section tested survives

**Attack.** The 35 files and the nine `menumap_common.bin` copies were read from the **installed archive** through
`agent_flow/tools/vbfextract.py`, not from the extracted tree that `check_gmap.py` reads. The requester and both readers
were read from the shipping image. Script: `Tools/analysis-kit/gfz-scripts/falsify_menumap_formats.py` (checks G1–G3),
output `falsify_menumap_formats.out`, image `73461d08…`, 0 BROKEN, exit 0. SWE2-DATA's `check_gmap.py` is carried, not
re-run.

| # | Clause attacked | Result |
|---|---|---|
| G1 | the corpus and closure | **survives**. There are 35 copies (guide00–04: 9, 8, 6, 6, 6). Each has `gmap`, `0x64` and `textOff = 0x10 + 8·count`, and every live `textRel` ascends. 30 end in a TIM2 that starts at `align16(text end)` and closes at EOF. The five without one are exactly `us`/`de`/`es`/`fr`/`it` guide00, and each of their TIM2 offsets is at or past EOF |
| G2 | §3: "only `menumap_guide00.bin` is ever loaded" | **survives**. The request id is `0x496` plus byte `+4` of the chosen record (`003C1EA7`/`003C1EB1`/`003C1EBC`), stored at widget `+0xF8`. In `menumap_common.bin` section 3, all 77 records in all nine locales close at EOF, and all 693 bytes at `+4` are 0 |
| G3 | §3's reader table | **survives**. `count` is at `+0x0E`, bounded unsigned. The entry's `textRel` is at `+4` (`0xFFFF` gives null), `textOff` at `+0x08`, and `tim2Off` at `+0x0A` (`0xFFFF` gives null). The widget's `+0xD0` bit `0x40` gates the text reader |
