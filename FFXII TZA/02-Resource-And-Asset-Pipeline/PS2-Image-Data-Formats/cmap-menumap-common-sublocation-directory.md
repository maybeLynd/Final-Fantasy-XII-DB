---
system: The `cmap` common-map sub-location directory — `worldmap/menumap_common.bin`
category: 02-Resource-And-Asset-Pipeline
status: DOCUMENTED — no register row is open; owner read 2026-09-30 (OPUS): layout, loader contract and the shared name-id join are read, and nothing on the page is carried as open
owner_layer: CodeDomain:Presentation.Menu
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-21 (FABLE) - 23 addresses cited - 1 data, 10 entry, 11 interior, 1 literal, every one resolving into a known section of the authority image.
    **This records a check performed on that date, NOT the method of the
    original derivation**, which this block never carried; see this
    document's own evidence section for that.
corpus_validated: "all nine locale copies of menumap_common.bin extracted from FFXII_TZA.vbf — byte-identical; all three sections count-closed to EOF; every section offset is natively read; name-id join to menu_mapname.bin 48/48 with wrong-offset controls, 2026-09-15"
archive_formats:
  - "cmap | explained | menumap_common.bin (.bin member): layout section 2 - (kind 7, 0xA4) by 003BC2D0 into widget +0xE8, readers 003BD4DD / 003BE45A / 003C17E0 / 003C1DF4, section 3"
last_reviewed: 2026-09-15
audit:
  passes: 1
  last_pass: 2026-09-17
  last_pass_state: falsification-pass
  crossref_clean: false
  reopened_count: 0
---

# The `cmap` common-map sub-location directory — `worldmap/menumap_common.bin`

> **The shared half of the map menu: the 48 sub-location records plus two auxiliary
> tables.** 1,760 bytes: an 8-byte directory of sub-location entries, a 369-entry
> u16 per-map array, and a 77-record gate table that is scanned **backwards** to pick the
> map data for the current game state.

**Corpus validation, before anything else.**

| | |
|---|---|
| file examined | `ps2data/image/ff12/myoshiok/<lang>/worldmap/menumap_common.bin` — all **9** locale copies |
| distinct contents | **1** — byte-identical across all nine locales (SHA-256 `e83074728f…`) |
| magic | `cmap` + `u32 0x000000CB` (`amap`=`0xC9`, `wmap`/`lmap`=`0xCA`, `cmap`=`0xCB`) |
| closure | directory 48×8B, sec2 `u16[369]` ends `0x474` (4-aligned), sec3 77×8B ends exactly at EOF `0x6E0` |
| decoder | `Tools/work/DATA/menumap/decode_menumap.py` (session scratch — untracked, not linkable) |

## 1. What the player sees

The map screen's "common" layer — which sub-location pages exist, which persistence group
each reports under, and which map graphic variant applies for the story's current state.
The file is locale-invariant: nothing here is a string.

## 2. Layout

```
struct CmapHeader {                    /* 0x0C bytes */
    char  magic[4];     /* 'cmap' */
    u32   fileId;       /* 0x000000CB */
    u16   offDir;       /* +0x08 = 0x0C  */
    u16   offSec2;      /* +0x0A = 0x190 */
};
```

### 2.1 Directory `@ 0x0C` — `{u32 count=48, entry[48]}` — the 48 sub-locations

```c
struct CmapEntry {                    /* 8 bytes */
    u8   persistenceGroup;  /* +0 joins lmap array-A +12 — measured 384/384 (lmap sheet §10) */
    u8   page;              /* +1 0 in 45; 1 at entry 40 (gil01_s02), 2 at entry 46 (bhm01_s01);
                               native check `byte[+1] != 0` sets widget flag 0x800 at 003BE48A */
    i16  auxId;             /* +2 -1 in 45; 81 / 82 / 265 at entries 8 / 10 / 47
                               (nac01_s01, nal01_s01, sav01_s02) — fits the field-id range
                               0..0xFFE of accessor 003779F0; sec2[81,82,265] all read -2.
                               Probably a per-sub-location field/map id — unbound. */
    u32  nameId;            /* +4 menu_mapname string id 60138..60187 — 48/48 in-table (§4) */
};
```

47 distinct persistence groups over 48 entries: **group 14 appears twice** — entries 13 and
47 (`sav01_s01`/`sav01_s02`, the Giza Plains dry/rains pair; the same doubled group the
[lmap sheet](lmap-menumap-location-graph.md) §10.6 recorded).

Entry order is the `menumap_world.h` sub-location enumeration (`rbn01_s01` … `sav01_s02`).

### 2.2 Section 2 `@ 0x190` — `{u16 count=369, u16 a[369]}`

A per-map lookup indexed by the field-id accessor `003779F0` (returns `0..0xFFE`, −1 = none)
— the reader `003C17E0` gates on `> 0` and indexes the array at `003C17FF`
(`count`-bounds-checked, `buf+off+2+idx*2`). `003779F0` is the shared field-record accessor
([CONTRACT-field-record-accessors](../../03-World-Area-Field/CONTRACT-field-record-accessors.md))
— its other callers include PlatformOnlineAchievements (`003160C0`); that edge is a fellow
API consumer, not a `cmap` reader. Values shipped: **358× `-2`, 10× `-1`, 1× `0`** —
a mostly-sentinel array; the comparison downstream (`003C17E0` → `003C0380` → `003C1070` →
`edx >= byte[elem]`) reads the element's low byte as a threshold. What the threshold means is
**not bound**; the indexing source is.

### 2.3 Section 3 `@ 0x474` — `{u32 count=77, rec[77]}` — **closes to EOF**

```c
struct CmapGateRec {                  /* 8 bytes */
    u16  gate;   /* +0 ascending thresholds 0x00..? — compared against the value 00265270 returns */
    u16  key;    /* +2 0x40xx-range id, validated through 0032A8A0; 0xFFFF = skip */
    u16  pad;    /* +4 = 0 in all 77 */   /* <- corrected 2026-10-02, OPUS: read: the guide-text request adds this byte to 0x496 (gmap sheet G2) */
    u16  seq;    /* +6 0..76 sequential */
};
```

The loader `003BD950` walks the records **from last to first** and takes the first whose
`gate` is satisfied by the current state *and* whose `key` passes `0032A8A0` — a
priority-ordered selection table (highest matching gate wins). The chosen record's buffer is
stored at **widget `+0xF0`** (`003C1DF4`–`003C1E59`). The `0x40xx` keys sit in the same band
as `wmap`'s B2 `a` field — a shared id space for map-graphic variants, likely.

`00265270` and `0032A8A0` are shared helpers, not `cmap` internals: `00265270` is also called
from CoreRuntimeScheduling, Input, PlatformOnlineAchievements and Presentation code, and
`0032A8A0` from Input and Save_Load_Settings code — fellow consumers of the same APIs, not
readers of this file.

## 3. Loader contract

The widget at `02B457E0` loads this file as **kind-7 id `0xA4`** (`003BC2D0`), buffer at
**widget `+0xE8`**. Native readers found in the rip-census:

| accessor | reads |
|---|---|
| `003BC5FF` | frees `+0xE8` (shared teardown for all three map buffers) |
| `003BD4DD` | walks the 48-entry directory (`u16[+8]`, `u32 count`, `stride 8`), comparing entry `+0` to a group arg; calls `003C1680` per match |
| `003BE45A` | bounds-checked entry read; tests `byte[+1] != 0` → sets flag `0x800` |
| `003C17E0`/`003C17FF` | sec2 indexed by `003779F0`'s field id |
| `003C1DF4` | sec3 pointer (`off+2+count*2`, 4-aligned) → `003BD950` → widget `+0xF0` |

## 4. The name-id join (shared with `wmap`)

`+4` is a `menu_mapname.bin` string id — measured **48/48 in the 285-entry id table**;
wrong-offset controls read `+0`→0/48 and `+2`→0/48. All 48 ids sit in `60138–60187`; every
string is empty except `60153` = "Giza Plains - The Dry" — sub-location pages fall back to
the parent location's name, and Giza's dry variant is the one exception that ships text.

## 5. Falsification notes

- The directory entry's `+1` byte is real data (two nonzero shipped values), not padding —
  the native gate at `003BE484` reads it.
- `sec2` count is `u16` (369), not `u32`: the reader at `003C181A` loads `word [rcx]`.
- `sec3`'s start is **derived**, not header-pointed: `offSec2 + 2 + count*2`, 4-aligned —
  `003C1E21`–`003C1E40` does exactly that arithmetic.
- The `+2` auxId and sec2's value semantics stay unbound; both are reported measured.

## What this document does not claim (SWE2-STRUCT for OPUS)

*(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../../_index/candidates/auditspec-review-dd-02-b2-0930/REVIEW.md) correction 6. These are declared limits, not open register rows; the status-line wording that names them is proposed for OPUS in [swe2struct-awn-wave-b-1001](../../_index/candidates/swe2struct-awn-wave-b-1001/README.md).)*

- **The entry `+2` auxId** (§2.1, §5): measured (-1 in 45 entries; 81 / 82 / 265 at entries 8 / 10 / 47), not bound
  to a meaning.
- **Section 2's value semantics** (§2.2, §5): the 369 values and their indexing source are read; what the threshold
  means is not bound.
- **The corpus figures** on this page come from the session-scratch decoder `Tools/work/DATA/menumap/decode_menumap.py`,
  which is untracked. SWE2-AUDIT-SPEC's tracked
  [cmap_corpus.py](../../_index/candidates/auditspec-review-dd-02-b2-0930/cmap_corpus.py) reproduces this page's
  figures from all nine shipped copies without it; that is a review re-derivation, not the page's own tool.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-FRONTIER for SWE2-DATA, 2026-09-30)

*Added 2026-09-30 (SWE2-FRONTIER, executing SWE2-DATA's pass-22 debt). These are the layers pass 22 still reported for this page at HEAD `4dfe4a006`. Every edge was listed in full, and each cited helper was read at its instructions or is named as the page reads it.*

**WorldAreaField, Story_Event_Quest_Hunt, StoryEvent, Input, Presentation, CoreRuntimeScheduling — CLIENT (16 edges).** `FieldData_GetVariable0` (`00265270`, a field-variable read gated on a flag byte) is the value the directory's thresholds compare against. It is also read by `001EDCD0`, `WorldTransition_StageFieldTransition` (`003145E0`), `003EAA70`, the loader `003BD950`, `PersistentFlag_QueryAuthoredThresholdSchedule` (`00377970`), `001ED240`, `InputGameplay_ArbitrateDigitalInputAndModalState` (`00253C70`), the row renderer `001CD0E0` and `001EC760`. `003BD950` and `00253C70` also read the flag gate `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` (`0032A8A0`), which calls `00377970`. The field-id reads (`003160C0`, `003C1070` -> `WorldTransition_GetActiveOrPendingFieldId` `003148F0`; `003C0380` -> `MapRef_GetPersistenceGroupId` `00264F90`) and `00576A50` -> `003779F0` complete the set. These are shared state reads, and the directory adds no writer to any of them.

**PlatformOnlineAchievements, UI, Save_Load_Settings, Script_VM_Native_Bridge — CLIENT (11 edges).** `003154B0` and `003161A0` read `00265270`. `00315E90` calls `003160C0`, which reads the field id and calls the sub-location accessor `003779F0` (a table read from a global). UI bodies call `0032A8A0` (`00281AE0`, `0029C530`), `003779F0` (`003C5E50`) and `003C0380` (`003BE950`). The save finaliser `00583D60` calls `0032A8A0`, which reads the persistent payload through `002EF2B0`, and the script body `0034E0B0` calls `0032A8A0`. They are clients of the same accessors.

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-cmap-menumap-common-sublocation-director-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0029C530` | 569 B | switches on the dword at `rdx`: 2 and 3 return 0; 14 ORs 8 and 15 ORs 4 into word `+0xE6` of `rcx` and return 0; other values tail-jump `005C5230` with `rcx` and `rdx` as passed in; 1 takes `p = 002432B0(rcx+0x50, qword +0x8 of the object qword 0209AC30 points to, 0x14, rcx)` and copies p's words `+0x4` to `+0xA` to `+0x98` to `+0x9E` (skipped when `rcx` is null; the later `rcx`-null tests only substitute a null entry pointer), then with `f = WorldTransition_GetActiveOrPendingFieldId()` stores `003778B0(00314910())` when `0032A8A0(0x5E)` is non-zero, else `003778B0(f)`, at `+0x18` of the entry at qword `+0x18` of qword `+0x60`, `00377B60(f)` at `+0x18` of the `+0x20` entry (each with `0020E620(0)` at entry `+0x20`) and the word `002543D0(00254380(00264F90(f)))` at `+0xA` of the `+0x28` entry; copies dword `+0x24` and words `+0xC` to `+0x12` of the `+0x18` and `+0x20` entries to `+0xC0`/`+0xC4`..`+0xCA` and `+0xD0`/`+0xD4`..`+0xDA`, calls `00247930(rcx, 0xA0)` and `00247570(rcx, 002735E0(3))`, zeroes word `+0xE0` and returns 0 | `0029C564`, `0029C5B5`, `0029C60A`, `0029C6A6`, `0029C750` |
