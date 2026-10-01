---
system: The `A7` big-endian offset-table graphics container — `bin_menu/*.as7`
category: 02-Resource-And-Asset-Pipeline
status: DOCUMENTED — every register row is closed (owner re-status 2026-09-30, OPUS, on SWE2-CONTRACT's reconciliation; superseded readings are marked on the page) — the payload subformat, the tailOff block and the offsets[] walker answered (RC-22..RC-24: an LZ stream decoded by 00248500, its codec head and dictionary, the walker 0024AA00); the silhouette group answered (RC-25: the member's party row 0-5 selects the six groups, other rows turn it off; SWE2-DATA round 2, 39d08c02f); no registered residue left; the item_gra request and palette path answered from the Item_Clut read (status line current 2026-09-30, SWE2-CONTRACT)
owner_layer: CodeDomain:Presentation.Menu
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-21 (FABLE) - 15 addresses cited - 13 entry, 2 interior, every one resolving into a known section of the authority image.
    **This records a check performed on that date, NOT the method of the
    original derivation**, which this block never carried; see this
    document's own evidence section for that.
corpus_validated: "all 18 shipped .as7 files extracted from FFXII_TZA.vbf and hashed, 2026-09-14; offset-table arithmetic verified on all 18"
archive_formats:
  - "as7 | explained | A7 big-endian offset-table container — u16be count + u32be tail + count x u32be file-absolute offsets; one format, the third/fourth bytes are the count."
last_reviewed: 2026-09-30
audit:
  passes: 1
  last_pass: 2026-09-17
  last_pass_state: falsification-pass
  crossref_clean: false
  reopened_count: 0
---

# The `A7` big-endian offset-table container — `bin_menu/*.as7`

> **A PS2-style big-endian page directory.** `A7` magic, a u16 **big-endian** entry count, a u32
> tail offset, then `count` big-endian u32 payload offsets. The table is exactly `8 + 4*count`
> bytes and `offsets[0]` always equals `8 + 4*count` — payloads run sequentially from the end of
> the directory. The `00 40` vs `0C 18` "two variants" reported earlier are **the same field**:
> u16be counts 64 and 3,096 — one format, not two.

**Corpus validation, before anything else.**

|| |
|---|---|
| files examined | **18 of 18** shipped `.as7` entries — `in`/`ch` copies of the same 9 names = **9 distinct contents**; the format ships in exactly these two locale trees and no other |
| names | `char_silhouette.as7`, `item_gra00..07.as7` |
| size range | 6,190 B (`item_gra07`) – 2,134,185 B (`char_silhouette`) |
| count field | 64 in all 8 `item_gra*`; 3,096 in `char_silhouette` |
| `offsets[0] == 8 + 4*count` | 18 of 18 |
| offsets monotonic, `last < tailOff < fileSize` | 18 of 18 |

## 1. What the player sees

- `item_gra00..07` — the eight item-category icon sheets (weapons, armor, items…). The menu
  icon pipeline loads these by slot.
- `char_silhouette` — the license-board/party silhouette pages — 3,096 pages at 2.1 MB.

## 2. The layout — **big-endian throughout**

```struct As7Header base=file
+0x00  char[2]  magic    'A7' - 41 37, 18 of 18
+0x02  u16be    count    payload count — 64 (item_gra*) or 3,096 (char_silhouette)
+0x04  u32be    tailOff  file offset of a tail block after the last payload — offsets[count-1] < tailOff < fileSize in 18 of 18
+0x08  u32be[]  offsets  count × file-absolute payload offsets, strictly monotonic
```

`offsets[i]` points at payload *i*; payload *i* runs to `offsets[i+1]` (or `tailOff` for the last).
Sample `item_gra00`: count 64, offsets `0x108, 0x272, 0x520, 0x7ED … 0xE227`, `tailOff 0xE4C5`,
size `0xE849`. Sample `char_silhouette`: count 3,096, `offsets[0] = 0x3068 = 8 + 4*3096` — the
directory ends exactly where the payloads begin.

The payload bytes themselves are image data — `item_gra00` payloads open with repeated
`7C 05` units — but the per-payload subformat is not decoded this pass (§7).

## 3. The loader contract

|| |
|---|---|
| requesters | `00291C80` and `002C8EE0` — item-icon and silhouette load paths, dynamic kind-7 indices (not in the constant-request census; the id is register-held). `00291C80` is catalogued under the Input subsystem — the item-icon loader lives in the input-adjacent menu module, which is why its call edges cross into Input |
| path resolution | kind-7 per-language path array: `…\myoshiok\<lang>\bin_menu\<name>.as7` |
| request chain | `0032E400` size + `0032E620` request via `0024AB90` helper family. These are the generic resource-pool entry points — the same pair is called by ActorEntity (`0032FCA0`, `00330310`, `003306E0`), Presentation (`003B2310`, `003B53C0`) and Script_VM_Native_Bridge (`0050DF70`, `0050DFE0`) clients for their own resources; those edges are fellow API consumers, not `.as7` readers |
| consumer family | menu icon renderer — the large draw code around `0028E000` and helper `0029376E` (11 refs) reads the slot buffers |
| silhouette proc | `002CF440` reads `SilhouettePosX`/`SilhouettePosY`/`SilhouetteWidth` ([menu atlas](../../16-UI/Menu-Screen-Atlas/the-menu-screen-atlas.md)) |
| magic check | none found — no `A7`/`0x3741` constant compare located |

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| `A7` magic | nothing found | — | — | no compare found |
| `+0x02` count | slot binder (dynamic) | — | — | reader not isolated to field *(since read: the walker `0024AA00` reads it big-endian at `0024AA0A` / `0024AA26`, RC-22..24; pointer 2026-09-30)* |
| `+0x04` tailOff | — | — | — | no reader found *(since read: the tail block every page decode `00248500` reads, RC-23)* |
| `offsets[]` | page/payload indexer | — | — | field-level walk not isolated *(since read: the walker `0024AA00`, RC-24)* |

*(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../../_index/candidates/auditspec-review-dd-02-b2-0930/REVIEW.md) correction 1: the three Inert cells above carry their answers.)*

## 4. Key addresses

| Address | Role |
|---|---|
| `00291C80` | `item_gra*` load path (dynamic kind-7) |
| `002C8EE0` | `char_silhouette` load path |
| `002CF440` | silhouette UI procedure — reads SilhouettePos fields |
| `0028E000` / `0029376E` | menu-icon draw region / per-image binder |
| `0024AB90` | resource-request helper used by these paths |

## 5. Corpus survey — 18 files (9 names × 2 dirs)

|| |
|---|---|
| `A7` magic | 18 of 18 |
| count 64 | `item_gra00..07` in `in` and `ch` |
| count 3,096 | `char_silhouette` in `in` and `ch` |
| `offsets[0] == 8 + 4*count` | 18 of 18 — directory ends at payload start |
| `ch` vs `in` | byte-identical names between the two dirs (same hashes) — the `ch` copy is a duplicate, not a CJK variant |

## 6. Falsification pass — 2026-09-14

| attack | result |
|---|---|
| "Two format variants `00 40` vs `0C 18`" | **Wrong** — one u16be count field: 64 vs 3,096. Same layout. |
| Little-endian header? | **No** — count and all offsets are big-endian (PS2 authoring heritage). |
| Do offsets start at `+0x10`? | **No** — at `+0x08`; `+0x04` is the separate `tailOff` field (earlier read had it in the table). |
| `offsets[0]` arbitrary? | **Deterministic** — equals `8 + 4*count` in 18 of 18; the directory is self-delimiting. |

## 7. What this document does not claim

- **The payload subformat** — what each page is (raw texels? a sub-table?) is undecoded.
- **What `tailOff` points at** — a footer section after the last payload; content unexamined.
- **The field-level binder** — which instruction walks `offsets[]`; the consumer family is known
  (icon renderer), the parser body is not isolated.
- **Whether `char_silhouette`'s 3,096 pages are all used** — no usage census done.

*Reconciled 2026-09-30 (SWE2-CONTRACT), citing [the bin_menu images page](binmenu-guest-face-and-map-effect-images.md)
§5b (SWE2-DATA, 2026-09-29, `b5_item_clut.py` 43 checks):* the `item_gra` request is traced — a loop in `00291C80`
requests kind 7 ids `0x98`–`0xA1` (`itemgra_c.tm2`, `Item_Clut.bin`, `Item_Gra00`–`07.as7`) through `0024AB90` and
`0032E620`, filling 16-byte slots of the table at `0209BEA0`; `00291D90` copies them into its object; and `00292390`
picks one 1,024-byte `Item_Clut` palette per item graphic by `id >> 6`. That the 64 payloads of sheet *n* are the ids
`64n..64n+63`, drawn as 8-bit indexed pixels against that palette, fits both counts and is **not claimed** — the walker
of `offsets[]` is still not isolated. Tier 1 for the request and palette reads.

- [x] **RC-22.** The per-payload subformat of an `.as7` page (the `item_gra` payloads open with repeated `7C 05`
  units): raw indexed texels, a compressed stream or a sub-table. Registered 2026-09-30 (SWE2-CONTRACT); static.
  *Applied 2026-09-30 (records) RC-22:* **ANSWERED 2026-09-30 (static; SWE2-DATA's record `_index/candidates/rc22-34-resource-readers-0930/` §1, commit `1261e2044`, `as7_decode.py`): each page is a static-dictionary LZ stream**, decoded by the codec `00248500`; every page of all 18 shipped files decodes.
- [x] **RC-23.** What the block at `tailOff` (after the last payload) holds, and whether anything reads it.
  Registered 2026-09-30 (SWE2-CONTRACT); static.
  *Applied 2026-09-30 (records) RC-23:* **ANSWERED 2026-09-30 (the same record §1): the `tailOff` block is the codec head plus the shared dictionary** (`{mode, k, be16 outLen, dictionary}`), read for every page.
- [x] **RC-24.** Which instruction walks an `.as7`'s `offsets[]` (and reads `count` / `tailOff`) — the consumer
  side of the `0209BEA0` slots for `item_gra`, and of `002C8EE0`'s buffer for `char_silhouette`. Registered 2026-09-30
  (SWE2-CONTRACT); static.
  *Applied 2026-09-30 (records) RC-24:* **ANSWERED 2026-09-30 (the same record §1): the `offsets[]` walker is `0024AA00`**, with two callers.
- [x] **RC-25.** Which of `char_silhouette`'s 3,096 pages any shipped path indexes. Registered 2026-09-30
  (SWE2-CONTRACT); static first (the silhouette procedure `002CF440`'s index source).
  *Applied 2026-09-30 (records) RC-25:* **NARROWED 2026-09-30 (the same record §2, `silhouette_pages.py`):** `002CEFD0` decodes whole 516-page groups (two runs of `0x102`), group `g = {0,1,3,2,4,5}[s]` with `s` the byte at `+0x10D` (0–5), so the six groups tile the 3,096 pages. **Residue (static):** which values the setter `002CEE00`'s two call sites pass in shipped play.
  *Round 2 (records) RC-25:* **ANSWERED 2026-09-30 (SWE2-DATA's round-2 record `_index/candidates/rc-residue-0930/`, commit `39d08c02f` §1, `rc25_domain.py`):** the menu record's word `+0x60`, which the pane reset `0056A010` passes to `002CEE00`, is the member's party row: `00329220` writes it only as `0xFFFF` or as the stats page's byte `+4`, which `0023AC80` sets to the page index `0`–`0x27`. The shipped scripts add main characters `0`–`5` and guests `7`–`14`. So rows `0`–`5` select the six groups `{0,1,3,2,4,5}` and together use all 3,096 pages; row 6, the guests and higher rows turn the silhouette off. *Corroborated by OPUS's independent static reading (coordination message, 2026-09-30): `0056A044` word `+0x60` of the `0209AC30 + 0xAC8` record → `00329220` `+0x60` = unit byte `+4`, the party row index (`0032957A`–`0032958E`); `00283270` counts members with `+0x60 <= 5` (`002833C5`). The independent review is `DATA-REQ-AUDITSEM-RC-RESIDUE-0930`.*
  *Round 3 (records) RC-25:* **stays ANSWERED; the writer premise narrowed 2026-09-30 (SWE2-CONTRACT, `_index/candidates/swe2contract-rc-round3-0930/`, applying SWE2-AUDIT-SEM's exact wording N3 in `_index/candidates/auditsem-review-rc-residue-0930/REVIEW.md` §6):** `0023AD8E` is the only byte/word writer of a page's `+4` among code that reaches the block through `02EBF190`. The block is static (`021B290C` = `02164280 + 0x4E68C`) and `002EF4A0` (called only from `00235AF0`) overwrites all 40 pages from the mirror `02166480`; a page's `+4` therefore also takes the mirror's value (mirror writers: the live-block snapshot `00229B76`, the save-load copy `00866A4D`, and `00583C00` from an untraced external buffer). The domain is `0`–`0x27` or `0xFFFF`, provided the mirror carries pages written by the same initialiser. *Independent corroboration: SWE2-ORACLE's `_index/candidates/rc25-party-definition-rows-0930/` (`be7c6fcd6`, `rc25_rows.py` FAILS 0) reaches the same rows (record `k` carries row `k`, `k = 0..39`; rows 0–5 are Vaan, Ashe, Fran, Balthier, Basch, Penelo; guests, the Chocobo and the Espers get no silhouette). Its "nothing else in the image writes `+0x04`" rests on the same only-writer premise and takes the same proviso. Review pending: `ORACLE-REQ-AUDITSPEC-RC4-5-25-30-0930`.*

*Superseded readings, 2026-09-30 (SWE2-CONTRACT, from SWE2-DATA's record `_index/candidates/rc22-34-resource-readers-0930/`, commit `1261e2044`): §2's "per-payload subformat is not decoded", §3's `+0x04 tailOff` "no reader found" and the `offsets[]` "field-level walk not isolated" are answered by RC-22..RC-24 above (the walker `0024AA00`, the LZ codec `00248500` and its tail dictionary). The same answer closes the binmenu page's §5b "`offsets[]` walker not isolated" (SWE2-DATA's page; its reconciliation line is this one). The §3 table is kept as written.*

## 8. Related

- [`the-menu-screen-atlas.md`](../../16-UI/Menu-Screen-Atlas/the-menu-screen-atlas.md) — silhouette proc and screen ownership.
- [`README.md`](README.md) — the `ps2data/image` long tail.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-FRONTIER for SWE2-DATA, 2026-09-30)

*Added 2026-09-30 (SWE2-FRONTIER, executing SWE2-DATA's pass-22 debt). These are the layers pass 22 still reported for this page at HEAD `4dfe4a006`. Every edge was listed in full, and each cited helper was read at its instructions or is named as the page reads it.*

**ActorEntity, WorldAreaField, World, Presentation, Input, Save_Load_Settings, Script_VM_Native_Bridge — CLIENT (request path).** These layers use the generic pool entry points this page names: the per-kind size lookup `0032E400` (`[022C51F0][kind][id]`, `id < 0x400`) and the request queue `0032E620`. The actor loaders `ActorResource_BeginManagerResourceSetLoad` (`0032FCA0`, reached from `0032FC30`), `ActorResource_BeginPrimaryPayloadLoad` (`00330310`) and `003306E0` call them, along with their own calls (`002628B0`, `0032ED80`, `00263FF0`, `003304A0`, and `003306E0`'s calls to `002561C0`, `002566E0` and `0037DC30`). The field loaders `MapRef_BeginLoadResources` (`00268750`), `003319D0`, `00378030`, `00379A10` and `AreaArd_LoadOrUnloadFieldResource` (`003EA820`) call them, as do `00378540` and the render bodies `003B2310` / `003B53C0` (reached from `003B25D0` and `CharacterRenderSystem_Initialize` `004269A0`). So do `00291C80`, the save-slot loader `002EF300` and the script adapters `0050DF70` / `0050DFE0`, which pop their arguments through `00267E10`; `0050DF70` writes the result through `0026B4E0`, while `0050DFE0` queues through `0032E620`. These are fellow API consumers for unrelated resources, not readers of this format. `00291C80` reaches the pair through `0024AB90`, a tail jump to `0032E400`.

**ActorEntity, CombatAI, Gameplay, Items_Equipment_Shops_License, Rewards_Progression_Economy — CLIENT and SERVICE (party-row path).** `BattleStats_InitializeDefinitionRecord` (`0023AC80`) sets the stats page's byte `+4` to the page index. It is called by `BattleUnit_ApplyUnitDefinition` (`0023A570`) and `00237DF0`, and it calls `00326030` / `00327CB0` / `00327DE0`, `0031A630` / `00323910` and `0030C470`. The party-row writer `00329220` calls the slot accessors `BattleUnit_GetSlotCount` (`00236850`) / `BattleUnit_GetBySlotIndex` (`00236820`), `00263C20`, `00263E30`, `003588B0`, `003589B0` and `FieldData_GetActiveFieldRecordBit15` (`00313F60`), and also calls `003879C0`, `00387090`, `00324020` and `002F8F20`. The loader `00235AF0` calls the validator `00322C50` (Gameplay). These write and read the party row the container's pages index; the owners are the battle and party layers.

**Party, CombatAction, CombatFormula, PlatformOnlineAchievements, Save_Load_Settings — CLIENT (member count and save mirror).** `00283270` counts members with `+0x60` in 0..5 and record bit 1 clear (`002833BD`/`002833BF`), incrementing `+0xB2C` of `[0209AC30]` (`002833C5`). It calls `00327BE0` and is called by `00328BD0`, `00316930` and the save bodies `00582860` / `005844A0`. `00329220` also calls `00263750` and `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`). The save mirror path is `00235AF0` and `SaveUI_RestoreActiveHeaderFromControllerBackup` (`00583C00`, called by `00580840`), both of which read `SaveImage_GetActiveRuntimeBuffer` (`002EF640`). The party row enters and leaves through the save image, and this page reads it only as an index.
