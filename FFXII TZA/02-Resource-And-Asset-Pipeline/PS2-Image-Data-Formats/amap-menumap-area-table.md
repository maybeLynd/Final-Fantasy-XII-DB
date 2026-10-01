---
system: The `amap` area table — `worldmap/menumap_area.bin`, four per-area and per-group arrays behind the map menu
category: 02-Resource-And-Asset-Pipeline
status: AUDITED
owner_layer: CodeDomain:Presentation.Menu
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the loader and the four accessors disassembled from the shipping image (SHA-256 checked by the
    check's pe.py); a raw rip sweep of the blob slot 020927D0 independent of the function list, with the
    world-map widget singleton as its positive control; every shipped copy decoded and size-closed
corpus_validated: "all 9 locale copies of menumap_area.bin (396 B, byte-identical); four sections size-closed back to back; .fst size for kind 7 id 0xA5 = 396 in all nine tables; S joins menu_mapname.bin 38/38 and menumap_world 39/39 with zero-scoring shifted controls, 2026-09-29"
archive_formats:
  - "amap | explained | menumap_area.bin (.bin member): {amap, u32 0xC9, u16 off[4]} + four counted arrays - (kind 7, 0xA5) by 00253780 into 020927D0, read only by 00254380 / 002543A0 / 002543D0 / 002543F0, sections 2-3"
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-amap-falsification-pass-1
  crossref_clean: true
  reopened_count: 0
  promoted: 2026-10-01 DOCUMENTED -> AUDITED by SWE2-AUDIT-SPEC (FRONTIER eligibility census sweep): falsification record opus-amap-falsification-pass-1; audit_crossrefs at HEAD reports 0 unresolved findings; cross-subsystem neighbours dispositioned in their section; killer observations recorded in the pass; promoter is not the last substantive author (last substantive commit: SWE2-FRONTIER)
---

# The `amap` area table — `worldmap/menumap_area.bin`

> **Four small arrays the map menu reads by area and by persistence group.** 396 bytes: a 16-byte
> header of four section offsets, then a per-area byte, a group-to-area byte map, a per-group
> area-map key-item id and a per-area name text id. Bound once to one global and read through four
> one-line accessors. `OPUS-REQ-DATA-BUCKET-MEMBER-FORMATS` (the `.bin` bucket's member `amap`).

**Corpus validation, before anything else.**

| | |
|---|---|
| files | `ps2data/image/ff12/myoshiok/<lang>/worldmap/menumap_area.bin`, all **9** locales, byte-identical, 396 B |
| closure | `16 + (1+39) + (1+59) + (2+2·59) + (4+4·39) = 396`, the four sections back to back |
| request size | `.fst` kind 7 id `0xA5` = 396 in all nine `FileSizeTable_*.fst` |
| check | [`check_amap.py`](../../_index/candidates/bucket-members-0929/checks/check_amap.py) → [output](../../_index/candidates/bucket-members-0929/checks/check_amap.out.txt): 128 checks, FAILS 0 |

## 1. What the player sees

The world-map menu's area layer: each area's name, whether the player owns that area's map, and
a per-area type byte that ends up as an inline icon in front of a location name.

## 2. The layout

```struct AmapHeader base=file size=0x10
+0x00  char[4]  magic          'amap' - never compared by the readers found
+0x04  u32      formatId       0xC9 (wmap/lmap 0xCA, cmap 0xCB) - not read by any reader found
+0x08  u16      offP           0x10
+0x0A  u16      offQ           0x38
+0x0C  u16      offR           0x74
+0x0E  u16      offS           0xEC
```

| section | at | shape | content (evidence) |
|---|---|---|---|
| P | `0x10` | `u8 n = 39; u8 P[39]` | per-area byte, values 0–5 |
| Q | `0x38` | `u8 n = 59; u8 Q[59]` | persistence group → area index (< 39) |
| R | `0x74` | `u16 n = 59; u16 R[59]` | per group: `0xFFFF` or `0x8000`–`0x803F`, an area-map key-item id |
| S | `0xEC` | `u32 n = 39; u32 S[39]` | area-name text id; `S[0] = −1`, `S[i] = 60099 + i` |

## 3. The loader contract

`00253780` requests kind 7 id `0xA5` through the menu-set request wrapper (`mov r8d, 0xa5` at `00253917`, call
`00253928`) and stores the returned data pointer in the global **`020927D0`** (`00253930`). A raw
rip sweep of that slot finds **7 references**: the loader (one read, two writes) and four
accessors — nothing else touches it. Control: the same sweep finds the 158 references to the
world-map widget singleton `02B457E0` that FABLE's `ripscan` lists.

| field | read by | out of range | returns |
|---|---|---|---|
| magic, `+0x04` | — (never compared) | — | — |
| Q | `00254380` (`00254387` / `00254399`) | `index ≥ Q.n` (unsigned) → 0 | `Q[index]` |
| S | `002543A0` (`002543A7` / `002543BF`) | `index == 0` or `≥ S.n` → the empty string `01CEB638` | text of `S[index]` through the text resolver |
| P | `002543D0` (`002543D7` / `002543E9`) | `index ≥ P.n` → 0 | `P[index]` |
| R | `002543F0` (`002543FB` / `00254413`) | `index ≥ R.n` or `R[index] == 0xFFFF` → 0 | the key-item ownership query on `R[index]`, as a bool |

Every accessor forms the section address as `u16 offset + low 32 bits of the blob pointer`
(`add edx, eax`), so the table is only addressable while the blob sits below 4 GiB.

**What the sections are joined to (corpus).**
- **Q** is indexed by the persistence group `MapRef_GetPersistenceGroupId` returns; `map_ref.bin`'s
  groups run 0–58, exactly Q's 59 entries (one `map_ref` row holds group 256, which the
  accessor's bounds check turns into 0). The save header's area index is filled through Q (the
  site is in [`check_amap.out.txt`](../../_index/candidates/bucket-members-0929/checks/check_amap.out.txt)).
- **S** equals `menu_mapname.bin`'s ids 38/38 and the [`wmap`](wmap-menumap-world-map-graph.md)
  area record `+16` name id 39/39; both shifted controls score 0.
- **R** values go to the key-item ownership query (mode 0) — so a group's entry asks
  "does the player own this area's map" (the call is static; the key-item meaning of `0x80xx` is
  inferred from [the encoded-id space](../../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md), class 13 sub-table 1).
- **P** becomes the last byte of the inline text escape `0F 3F 81 80|P` (template `01E0CDFC`),
  which the location-name builder places before a location name (sites in the check output). Reading P as an
  area-type icon index is an inference.

## 4. Not claimed

What P's six values look like on screen; why `+0x04` exists (no reader found); anything about a
build where the header offsets differ (nothing validates them).

## 5. Related

- [`wmap`](wmap-menumap-world-map-graph.md), [`lmap`](lmap-menumap-location-graph.md) and
  [`cmap`](cmap-menumap-common-sublocation-directory.md) — the other three map-menu tables, loaded by `003BC2D0`; `amap` is loaded by a different routine.
- [The bucket member formats](../../_index/candidates/bucket-members-0929/README.md) — where this member is declared.

## Crossings into other layers — pass 22 (SWE2-DATA, 2026-09-29)

- **UI — SERVICE, body read.** `00253780` is the map menu's resource loader in the UI layer; it
  requests this file beside the menu's other kind-7 resources and keeps the pointer in `020927D0`.
  The page's claim is the table, which that loader only fetches.
- **Presentation — CLIENT, edges.tsv.** The name and type accessors `002543A0` / `002543D0` are
  called by two Presentation menu bodies (`002B7B80`, `002BAF80`) that draw the area list; what
  they draw belongs to their pages.
- **Save_Load_Settings — CLIENT, edges.tsv.** `00254380` has one caller in the save-header code
  (`00583D60`), which records the current area index; the save layout is that layer's page.
- **Gameplay — SERVICE, body read.** `002543F0` hands a group's `R` entry to the key-item
  ownership query, labelled Gameplay; the page uses only its boolean answer.
- **UI — CLIENT, edges.tsv.** Besides the loader, UI-layer menu bodies (`0029C530`, `003F92B0`
  and others) call `00254380` (group → area); what they do with the area index is their pages'.

## Falsification pass 1 — 2026-09-29 (OPUS): every section tested survives

**Attack.** The file was read from the **installed archive** (`FFXII_TZA.vbf`, through `agent_flow/tools/vbfextract.py`),
not from the extracted tree that `check_amap.py` reads. The code clauses were read from the shipping image. The seven
references to the blob slot were found again with a raw rip-relative sweep that counts displacements, not functions.
Script: `Tools/analysis-kit/gfz-scripts/falsify_menumap_formats.py` (checks A1–A4), output
`falsify_menumap_formats.out`, image `73461d08…`, 0 BROKEN, exit 0. SWE2-DATA's `check_amap.py` is carried, not re-run.

| # | Clause attacked | Result |
|---|---|---|
| A1 | the corpus and header | **survives**. The nine archive copies have one content and are 396 B. The header is `amap` and `0xC9`, with offsets `0x10`/`0x38`/`0x74`/`0xEC`; the four counted sections close back to back at 396 |
| A2 | §2's section contents | **survives**. P holds 39 values in 0–5. Q holds 59 area indices, all below 39. R holds 59 words: 46 are `0x8000`–`0x803F` and 13 are `0xFFFF`. S holds 39 dwords, with `S[0] = −1` and `S[i] = 60099 + i` |
| A3 | §3: the binding and "nothing else touches it" | **survives**. The loader requests kind 7 id `0xA5` and stores `020927D0`. Seven rip references were found: three in the loader and one in each accessor. The control, `02B457E0`, gives 158 |
| A4 | §3's accessor table | **survives**. Q is at `+0x0A`, S at `+0x0E`, P at `+0x08` and R at `+0x0C`. The bounds are unsigned. S index 0 returns `01CEB638`. An R entry of `0xFFFF` returns 0; otherwise the key-item query `00309EC0(R, 0)` is returned as a bool. Every section address is the offset plus the low 32 bits of the blob |

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-FRONTIER for SWE2-DATA, 2026-09-30)

*Added 2026-09-30 (SWE2-FRONTIER, executing SWE2-DATA's pass-22 debt). These are the layers pass 22 still reported for this page at HEAD `4dfe4a006`. Every edge was listed in full, and each cited helper was read at its instructions.*

**CombatAI, CombatAction, Items_Equipment_Shops_License, PlatformOnlineAchievements, WorldAreaField — CLIENT (6 edges).** The one foreign subject is the key-item query `00309EC0` (`BattleEncodedId_DispatchQueryMode0Value`), which the area table calls as `00309EC0(R, 0)`. Its other callers are `AiOrder_EvaluateTargetSelector` (`00301AD0`), `00317BC0` and `00317C80`, `Equipment_CheckItemEligibleForSlot` (`00317930`), `00315E90` and `00576A50`. They all call the same encoded-id query for their own reasons. The area table shares the query and nothing else.
