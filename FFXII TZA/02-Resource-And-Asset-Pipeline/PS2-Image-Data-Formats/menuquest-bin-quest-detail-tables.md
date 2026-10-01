---
system: The quest-menu detail tables — `quest/menuquest00..02.bin`, one per quest group, a 20-byte record per quest over six sections
category: 02-Resource-And-Asset-Pipeline
status: AUDITED
owner_layer: CodeDomain:Presentation.Menu
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the requester 003800D0, its caller chain 0037FFD0 / 0037FD50 and the readers 0037E8D0 / 0037EE10 /
    0037EF70 / 0037FEA0 / 00473D50 / 00473DB0 / 00473B70 / 00473BB0 / 00473CC0 disassembled from the shipping
    image; an immediate sweep for ids 0x129..0x139 with the two documented menuquest.dat requests as its
    positive control; every shipped copy decoded and size-closed
corpus_validated: "all 27 menuquest00..02.bin copies (3 units x 9 locales): off[0] = 16 + 20*N and off[5] + 28*N = file size in every copy; N = 19 / 45 / 2 equals menuquest.dat's per-group quest counts in all nine locales (shifted control fails) and sums to menuquest.h's menuquest_NUM 66; .fst sizes exist for kind 7 ids 0x12A..0x12C only, 2026-09-29"
archive_formats:
  - "menuquest | explained | menuquest00/01/02.bin (.bin member; the leading dwords are off[0], off[1]): {u16 off[6], u16 0xFFFF, u16 N, 20-byte rec[N], three string sections, QHD0 and QHT0 chunk sections, N x 28-byte nibble rows} - (kind 7, 0x12A + group) by 003800D0, read by 0037E8D0 / 0037EF70 and rebased by 00473D50 / 00473DB0, sections 2-3"
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-menuquest-falsification-pass-1
  crossref_clean: true
  reopened_count: 0
  promoted: 2026-10-01 DOCUMENTED -> AUDITED by SWE2-AUDIT-SPEC (FRONTIER eligibility census sweep): falsification record opus-menuquest-falsification-pass-1; audit_crossrefs at HEAD reports 0 unresolved findings; cross-subsystem neighbours dispositioned in their section; killer observations recorded in the pass; promoter is not the last substantive author (last substantive commit: OPUS)
---

# The quest-menu detail tables — `quest/menuquest00..02.bin`

> **One file per quest group, one 20-byte record per quest.** The Clan/hunt menu's list
> ([`menuquest.dat`](five-small-bin-tables.md) §12, `qstd`) says which group a quest is in; the
> menu then loads `menuquest0<group>.bin` and reads the quest's record at its position inside the
> group. The files are **not image data** — their "several leading patterns" (`8C 01 70 02`,
> `8C 01 74 07`, `94 03 94 03`, `38 00 38 00`) are the first two section offsets.
> `OPUS-REQ-DATA-BUCKET-MEMBER-FORMATS` (the `.bin` bucket's member `menuquest`).

**Corpus validation, before anything else.**

| | |
|---|---|
| files | `ps2data/image/ff12/myoshiok/<lang>/quest/menuquest00.bin` / `01` / `02` — 3 units × 9 locales = **27** |
| closure | `off[0] = 16 + 20·N` and `off[5] + 28·N = file size` in all 27 |
| join | N = **19 / 45 / 2**, the per-group quest counts of `menuquest.dat`, in all nine locales; the sum 66 is `menuquest_NUM` in the shipped `menuquest.h` (`menuquest_group_NUM` = 3 = the three files) |
| check | [`check_menuquest.py`](../../_index/candidates/bucket-members-0929/checks/check_menuquest.py) → [output](../../_index/candidates/bucket-members-0929/checks/check_menuquest.out.txt): 228 checks, FAILS 0 |

## 1. What the player sees

The detail pane of a quest in the quest menu: its text lines and the progress-dependent part.

## 2. The layout

```struct MenuQuestHeader base=file size=0x10
+0x00  u16[6]   off            section offsets from file start; off[0] = 16 + 20*N
+0x0C  u16      pad            0xFFFF - not read
+0x0E  u16      N              record count - never bounds-checked by the readers
```

```struct MenuQuestRecord base=file+0x10 size=0x14
+0x00  u16[6]   rel            per-section offset of this quest's item, 0xFFFF = none; rel[5] always 0 - not read
+0x0C  u16[4]   fill           0x0FFF in every record - not read
```

| section | shape | read by |
|---|---|---|
| 0–2 | zero-terminated strings | `0037E8D0` (header `0037E9FE` / `0037EA27` / `0037EA51`, record `0037EA01` / `0037EA2B` / `0037EA55`) |
| 3 | `'QHD0'` chunk `{magic, u32 count, u32 offset[count]}` | `0037FEC4` / `0037FECD` → `00473D50` |
| 4 | `'QHT0'` chunk, same shape | `0037FF1B` / `0037FF24` → `00473DB0` |
| 5 | N rows of 28 bytes at `off[5] + 28·k`, a nibble array; bytes 26–27 zero in every row | `0037E9D3` / `0037EF01` (`imul 0x1C`), nibble fetch `0037EFAA` |

## 3. The loader contract

**Request.** `003800D0` asks kind 7 for **id `0x12A` + group** (`movzx ebx, byte [rdx+2]` /
`add ebx, 0x12a` at `00380120`, request call at `00380145`); its type-4 arm asks `0x129`
(`menuquest.nfs`) instead. It is called only from `0037FFD0`, which `0037FD50` feeds: the group is
the low byte of the quest's `menuquest.dat` payload (`0037FD93`) and the record index is the
quest's position within its group (`0037FDE9`). The `.fst` has sizes for `0x12A`–`0x12C` only,
matching the three files.

**Search control.** For ids `0x129`–`0x139` the only requesters are `00380112` and `00380120`; the
same sweep finds both documented `menuquest.dat` requests (`0037F733`, `0057704A`).

**The chunk sections are rebased in place.** `00473D50` (and `00473DB0` for `QHT0`) publishes the
chunk at `02CA6C68` (`02CA6C70`), adds the low 32 bits of the chunk address to each of its
`count` offsets, and sets bit 31 of the count as the done flag (`00473D9E`). A raw rip sweep finds
only the `00473B50`–`00473DE8` family touching those two globals; the world-map widget reads them
through `00473B70`, `00473BB0` and `00473CC0`. Because the rebased values are 32-bit and
`00473B7A` sign-extends them, the chunks are only addressable below 2 GiB (a placement limit, not
a claim about where the data is loaded).

**Section 5's index** is the quest's saved progress byte (save payload `+0x1064 + quest id`,
through its getter; site in the check output) divided by 5.

## 4. Not claimed

What the `QHD0` / `QHT0` entry fields mean beyond their access shape (the `us` `QHT0` strings read
as romanized-Japanese placeholders — an inference); sections 0–2 hold `not use.`-style
placeholders or `0xFFFF` in most locales and real strings only in `in`; `rel[5]`, the `0x0FFF`
words and the header's `+0x0C` have no reader found; `N` is never bounds-checked.

## 5. Related

- [Five small `.bin` tables](five-small-bin-tables.md) §12 — `menuquest.dat` (`qstd`), the list that selects the group and index.
- [`menuquest.lst`](lst-menuquest-list.md) — the sibling quest list.
- [The bucket member formats](../../_index/candidates/bucket-members-0929/README.md).

## Crossings into other layers — pass 22 (SWE2-DATA, 2026-09-29)

- **UI — CLIENT, body read.** The quest menu that requests (`003800D0`) and reads (`0037E8D0`,
  `0037EF70`) these files, and the world-map widget that reads the rebased chunks through
  `00473B70` / `00473BB0` / `00473CC0`, are UI-layer consumers; what they display is theirs.
- **Presentation — CLIENT, edges.tsv.** `0037EF70` is also reached from the quest detail painter
  `0037E8D0`, labelled Presentation; the same reading of section 5, drawn.

## Falsification pass 1 — 2026-09-29 (OPUS): every section tested survives

**Attack.** The 27 files were read from the **installed archive** through `agent_flow/tools/vbfextract.py`, not from
the extracted tree that `check_menuquest.py` reads. The requester and the chunk rebaser were read from the shipping
image. Script: `Tools/analysis-kit/gfz-scripts/falsify_menumap_formats.py` (checks M1–M2), output
`falsify_menumap_formats.out`, image `73461d08…`, 0 BROKEN, exit 0. SWE2-DATA's `check_menuquest.py` is carried, not
re-run.

| # | Clause attacked | Result |
|---|---|---|
| M1 | §2: the layout and the corpus closure | **survives**. There are 27 copies, and every one closes: `off[0] = 16 + 20·N` and `off[5] + 28·N = size`. N is 19, 45 and 2 by group in all nine locales. The header pad is `0xFFFF`. Every record has `rel[5] = 0` and four `0x0FFF` fill words. Sections 3 and 4 open with `QHD0` and `QHT0`. Bytes 26–27 of every section-5 row are zero |
| M2 | §3: the request and the in-place rebase | **survives**. The request is kind 7 id `0x12A` plus the group (`0038011C`/`00380120`, call `00380145`); the other arm asks `0x129`. `00473D50` publishes the chunk at `02CA6C68`, adds the chunk's low 32 bits to each offset from `+8`, and sets bit 31 of the count at `00473D9E` |
