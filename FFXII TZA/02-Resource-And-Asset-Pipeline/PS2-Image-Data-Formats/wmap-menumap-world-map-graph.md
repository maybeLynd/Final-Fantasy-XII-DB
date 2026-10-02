---
system: The `wmap` world-map area/route graph — `worldmap/menumap_world.bin`
category: 02-Resource-And-Asset-Pipeline
status: DOCUMENTED — no register row is open; owner read 2026-09-30 (OPUS): layout, loader contract, the header constants and the 60000-range ids are read, and nothing on the page is carried as open
owner_layer: CodeDomain:Presentation.Menu
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-21 (FABLE) - 24 addresses cited - 1 data, 7 entry, 15 interior, 1 literal, every one resolving into a known section of the authority image.
    **This records a check performed on that date, NOT the method of the
    original derivation**, which this block never carried; see this
    document's own evidence section for that.
corpus_validated: "all nine locale copies of menumap_world.bin extracted from FFXII_TZA.vbf and hashed (4 distinct contents); every section boundary is count-closed against its own header and every populated offset is natively read; name-id join to menu_mapname.bin verified with wrong-offset controls, 2026-09-15"
archive_formats:
  - "wmap | explained | menumap_world.bin (.bin member): layout section 2 - (kind 7, 0xA2) by 003BC2D0 into widget +0xD8, 23 accessor sites, section 3"
last_reviewed: 2026-09-15
audit:
  passes: 1
  last_pass: 2026-09-17
  last_pass_state: falsification-pass
  crossref_clean: false
  reopened_count: 0
---

# The `wmap` world-map area/route graph — `worldmap/menumap_world.bin`

> **The world map's topology file: which areas exist, which region each belongs to, which
> routes connect them, and where the Strahl can land.** 2,040 bytes, four count-prefixed
> sections reached through a `u16` offset directory, plus a parallel per-area sub-table.
> Every count is reproduced by the shipped generator header `menumap_world.h` (~~§5~~ §4 *(corrected 2026-10-02, OPUS: the header-constant section is §4)*), and every
> name field resolves into `menu_mapname.bin`'s string-id table (~~§6~~ §5 *(corrected 2026-10-02, OPUS: the 60000-range ids are §5)*).

**Corpus validation, before anything else.**

| | |
|---|---|
| file examined | `ps2data/image/ff12/myoshiok/<lang>/worldmap/menumap_world.bin` — all **9** locale copies, 2,040 B each |
| distinct contents | **4**: `{us, ch, cn, de, kr}`, `es`, `fr`, `{in, it}` — every differing byte sits inside the area table's position/label fields; **no id or route byte ever differs** (~~§7~~ §6 *(corrected 2026-10-02, OPUS: locale behaviour is §6)*) |
| magic | `wmap` + `u32 0x000000CA` in all copies (`menumap_location.bin` carries the same `0xCA`; `menumap_area.bin` is `amap`/`0xC9`, `menumap_common.bin` is `cmap`/`0xCB`) |
| section closure | four populated offsets; each section is `{u32 count, count × fixed record}` and the last ends exactly at EOF |
| decoder | `Tools/work/DATA/menumap/decode_menumap.py` (session scratch — untracked, not linkable), full dump `decode_menumap.out.txt` |

## 1. What the player sees

The world-map screen draws a region ribbon, area labels with a cursor that moves along
authored links, travel routes between areas, and the Strahl destination list. This file is
that screen's authored data: 38 real areas plus a none record, 60 routes, 18 Strahl landing
points, 12 region slots.

## 2. Layout

```
struct WmapHeader {                      /* 0x14 bytes */
    char  magic[4];        /* 'wmap' */
    u32   fileId;          /* 0x000000CA in all copies */
    u16   offRegions;      /* +0x08 = 0x14  */
    u16   offAreas;        /* +0x0A = 0x48  */
    u16   offRoutesLo;     /* +0x0C = 0x5C8 (read as u16; +0x0E slot = 0) */
    u16   slot3;           /* +0x0E = 0 — never read by any found accessor */
    u16   offStrahl;       /* +0x10 = 0x7AC (read as u16; +0x12 slot = 0) */
    u16   slot5;           /* +0x12 = 0 — never read */
};
```

The six u16 slots can equally be read as `{u16, u16, u32, u32}` — the accessors only ever
load 16-bit words at `+8 / +0xA / +0xC / +0x10`, so the on-disk encoding is stated as the
six-slot form with the two zero slots flagged.

### 2.1 Region table `@ 0x14` — `{u32 count=12, u32 id[12]}`

Slot 0 is the `0xFFFFFFFF` "none" sentinel; slots 1–11 hold name ids **60000–60010**
(`0xEA60+n`). 60000 resolves to "Dalmasca", 60001 "Nabradia", 60002 "Archadia" … through
`menu_mapname.bin` (§6). `region_MAX` in the generator header is 11 — the table carries the
maximum, slot 0 is the empty entry.

### 2.2 Area table `@ 0x48` — `{u32 count=39, area rec[39]}` + per-area second table

Each record is **28 bytes** — the stride is fixed natively, not inferred: every bounds-checked
accessor computes `buf + [buf+0xA] + 4 + idx*0x1C` (`003BCCB3`, `003BCD56`, `003BD143`,
`003BD238`, `003BD672`, `003BFEBB`, `003C08C4`, `003C0B74`, `003C0BE4`, `003C0C54`,
`003C1D76`).

```c
struct WmapArea {                 /* 28 bytes */
    i16  cx, cy;       /* +0  area centroid on the map image (px) */
    u8   link[4];      /* +4  directional neighbour area ids; 0xFF = none (cursor nav) */
    i16  aux8;         /* +8  -1 in 37 of 39; 10 at rec13, 1450 at rec37 — unbound */
    u8   regionId;     /* +10 joins region table (1..11); rec0 = 0 */
    u8   selfIndex;    /* +11 1..38 (rec0 = 0); read natively at 003C1DB4 */
    i16  labelDx;      /* +12 label offset (−14..+34 shipped) */
    i16  labelDy;      /* +14 (−50..+46) */
    u32  nameId;       /* +16 menu_mapname id 60099+selfIndex; rec0 = -1 */
    i16  anchorX;      /* +20 0x4000|n tag or -1 — native-read at 003C0Bxx (+0x14) */
    i16  anchorY;      /* +22 0x8000|n tag or -1 — native-read at 003C0Bxx (+0x16) */
    u32  nameId2;      /* +24 duplicates +16 in every shipped record */
};
```

Immediately after the 39 records (at `0x490`, no header offset points to it) sits a second
count-less table, **39 × 8 bytes** `{i16 a, u16 flag, u32 pad}`: `a` is `-1` in 27 records
and `0x402F..0x4062` in the other 12; `flag` ∈ {0,1}; `pad` = 0 always. `a` reads as a
u16-fixed-point angle or an id in the `0x40xx` band shared with `cmap`'s gate keys — **not
bound; recorded as measured**.

### 2.3 Route table `@ 0x5C8` — `{u32 count=60, route rec[60]}`

```c
struct WmapRoute {                /* 8 bytes */
    u8   areaA, areaB; /* +0,+1 endpoint area ids (1..38) */
    u16  routeType;    /* +2  0 = normal; 1..15 = special (native filter: byte+2 == 0 at 003C0060) */
    u16  x, y;         /* +4,+6 label/midpoint pixel position; (0,0) on four records */
};
```

Measured against `menumap_world.h`: **45 type-0 routes + 15 special routes = 60 total** —
exactly `route_MAX`/`sroute_MAX`. The 15 specials are seven `a↔b` directional pairs (types
1–14) plus `route 59 = {22,22,type15,(0,0)}` — a self-loop terminator. Per-area route counts
stay within the header's `MAX 6` bounds (max normal 4, max special 3 shipped).

### 2.4 Strahl table `@ 0x7AC` — `{u32 count=18, dest rec[18]}` — **closes to EOF**

```c
struct WmapStrahl {               /* 4 bytes */
    u16  pos;      /* +0 position on map (142..1151 shipped) */
    u8   areaId;   /* +2 landing area (native compared at 003C0280) */
    u8   pad;      /* +3 = 0 in all 18 */
};
```

`shtoral_MAX` = 18 ✓.

## 3. Loader contract

The world-map menu widget singleton at `02B457E0` loads this file as **kind-7 resource id
`0xA2`** via the shared request queue (`0032E620`) in `003BC2D0`, storing the buffer at
**widget `+0xD8`** — verified by 23 distinct accessor sites that load `[rip→02B457E0]` then
`[reg+0xD8]` (rip-census list in `decode_menumap.out.txt`). `0032E620` is the generic
resource-request API — its other callers sit in ActorEntity (`0032FCA0`, `00330310`), Input
(`00291C80`) and Presentation (`003B2310`, `003B53C0`) requesting unrelated resources;
those edges are fellow API consumers, not `wmap` readers. Sibling slots: `+0xE0` = id
`0xA3` (`menumap_location.bin`, the `lmap` table), `+0xE8` = id `0xA4`
(`menumap_common.bin`, the `cmap` table — [cmap sheet](cmap-menumap-common-sublocation-directory.md)).
All three are heap-freed and flag-cleared together in the teardown at `003BC5B8`.

## 4. Header-constant agreement (`menumap_world.h`)

| header constant | file measurement | verdict |
|---|---|---|
| `region_MAX 11` | 11 named region ids + 1 sentinel | match |
| `AREA_MAX 38` | 39 records = 38 + none record | match |
| `route_MAX 45` / `sroute_MAX 15` | 45 + 15 = 60 records | match |
| `route_type_MAX 16` | types seen: 0..15 | match |
| `shtoral_MAX 18` | 18 records, closes to EOF | match |
| `sloc_MAX 48` | (in `cmap`, not here) 48 entries | see sibling sheet |
| `loc_MAX 59` | (in `lmap`, not here) | see lmap sheet |

Per-area fan-out bounds (`route_PER_AREA_MAX 6`, `sroute_PER_AREA_MAX 6`) hold: shipped
maxima are 4 and 3.

## 5. The 60000-range ids — resolved

The recurring `0xEA60`-band values are **string ids into `menu_mapname.bin`**
(`ps2data/image/ff12/test_battle/<lang>/binaryfile/menu_mapname.bin`), an `st2e` string-id
table: `count=285`, `recordSize=4` — the records *are* the ids — heap at `+0x14 = 0x494`
(`{one=1, base=0xC, size=0xA96, count=285, offsets[286]}`).

Joins, all measured in `decode_menumap.out.txt`:

| source field | ids | in-table | wrong-offset control |
|---|---|---|---|
| wmap region table slots 1–11 | 60000–60010 | **11/11** | slot0 is −1 by design |
| wmap area `+0x10` / `+0x18` | 60100–60137 | **38/38** | `+0xC`→0/39, `+0x14`→0/39 |
| cmap entry `+4` | 60138–60187 | **48/48** | `+0`→0/48, `+2`→0/48 |
| lmap (60000-band dwords) | 60201–60244 | 42 distinct, all present | — |
| negative control | `meshdata.mg` dwords | **0 hits** | — |

Decoded ranges: `60000–60010` region names, `60100–60137` area names (Rabanastre … Bahamut),
`60138–60199` sub-location name slots (all present, strings empty except `60153` "Giza Plains
- The Dry" — empty = parent-name fallback), `60201–60243` "To X" destination labels.

## 6. Locale behaviour

| file | distinct contents | groups |
|---|---|---|
| `menumap_world.bin` | 4 | `{us,ch,cn,de,kr}` · `es` · `fr` · `{in,it}` |
| `menumap_common.bin` | 1 | all nine identical |
| `menumap_area.bin` | 1 | all nine identical |
| `menumap_location.bin` | 6 | `{us,ch,cn,kr}` · `de` · `es` · `fr` · `in` · `it` |

Every differing `wmap` byte lands inside an area record's coordinate/label fields
(`cx/cy`, `labelDx/Dy`, `anchorX/Y`) — per-locale label positioning for different-length
names. Ids, regions, routes and Strahl entries are byte-identical across all nine.

## 7. Falsification notes

- The 36-byte area-record stride is **refuted** by native `imul …,0x1C`; 28 bytes is forced.
- The `+0xE`/`+0x12` directory slots are zero in all nine copies and no accessor reads them.
- The `+8` aux i16 (`-1`, twice otherwise) and the `B2` sub-table remain unbound; both are
  stated as measured, not named.

## What this document does not claim (SWE2-STRUCT for OPUS)

*(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../../_index/candidates/auditspec-review-dd-02-b2-0930/REVIEW.md) correction 6. These are declared limits, not open register rows; the status-line wording that names them is proposed for OPUS in [swe2struct-awn-wave-b-1001](../../_index/candidates/swe2struct-awn-wave-b-1001/README.md).)*

- **The area record's `+8` aux i16** (§2.2, §7): -1 in 37 of 39 records, 10 at record 13 and 1450 at record 37; not
  named.
- **The `B2` sub-table** (§2.2, the 39 × 8-byte table after the area records, §7): measured, not bound.
- **The corpus figures** on this page come from the session-scratch decoder `Tools/work/DATA/menumap/decode_menumap.py`
  (full dump `decode_menumap.out.txt`), which is untracked. No tracked tool re-derives this page's figures.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-FRONTIER for SWE2-DATA, 2026-09-30)

*Added 2026-09-30 (SWE2-FRONTIER, executing SWE2-DATA's pass-22 debt). These are the layers pass 22 still reported for this page at HEAD `4dfe4a006`. Every edge was listed in full, and each cited helper was read at its instructions.*

**ActorEntity — CLIENT and SERVICE (9 edges).** The world-map graph loads through the shared request queue `0032E620`. Its actor-side callers are `ActorResource_BeginManagerResourceSetLoad` (`0032FCA0`) and `ActorResource_BeginPrimaryPayloadLoad` (`00330310`). Their own calls (`002628B0`, `0032ED80`, `003306E0`, `00263FF0`, `003304A0`, and `0032FCA0` -> `00330310`) are the actor layer's request path. The queue is shared.

**Presentation — CLIENT (4 edges).** `003B2310` and `003B53C0` request through `0032E620`, and they are reached from `003B25D0` and `CharacterRenderSystem_Initialize` (`004269A0`).

**Input, Save_Load_Settings, Script_VM_Native_Bridge — CLIENT (3 edges).** `00291C80`, the save-slot loader `002EF300` and the script adapter `0050DFE0` each file requests through `0032E620`. All three are clients of the same queue.
