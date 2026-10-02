# Reconstruction readiness — `FFXII TZA/03-World-Area-Field/`

| | |
|---|---|
| Stream | R (reconstruction readiness), per [`docs/cloud-briefs/re-readiness.md`](../../docs/cloud-briefs/re-readiness.md) |
| Board task | `OPUS-CLOUD-R-READINESS-03-1002` |
| Date | 2026-10-02 |
| Snapshot | this repo's text snapshot only (`df2c9f47`); no executable, Ghidra or live game was used |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every item is a quotation or a paraphrase of a page, with its location. |

**Counts:**
- **Coverage:** 15 of 15 `.md` pages read in full (4 contracts, 10 system pages, `README.md`); 16 `.tsv` files checked for layout and counts only.
- **Interface:** **41 entry-point rows** mapped (4 trigger, 9 field record, 12 weather, 5 field-init fan-out, 11 map pack).
- **Gaps:** **19** self-stated + **17** structural.
- **Contradictions:** **74** in all.
  - **28 value-changing**, all "page-text only - needs local check": 12 have a favoured side settled by a dated correction (C-V1–C-V4, C-V9–C-V12, C-V17, C-V18, C-V21, C-V25); 16 have no favoured side.
  - **46 stale / banner.**
- **Rating: NOT YET** overall.
  - READY: the field record table and accessors.
  - MOSTLY: weather decide/commit, `map_ref.bin`, the pack loader, `ACTL` / `LGT2` / `SP1`, the LegacyPS2GS rebuild.
  - NOT YET: weather materialisation and presentation, trigger points as a drivable system, `YM00` per-chunk semantics.

Citation form: `path:line`, where `path` is relative to `FFXII TZA/03-World-Area-Field/`. Example:
`Weather/weather-slot-state-model.md:138` is line 138 of
`FFXII TZA/03-World-Area-Field/Weather/weather-slot-state-model.md`. Line numbers are those of snapshot `df2c9f47`;
several of these pages are being edited by other lanes, so the quotes are the snapshot's text.

"Not stated" means none of the 03 pages says it. Where only another category's page makes a point, this report gives
the pointer as a path from `FFXII TZA/`. That page was not audited for this report.

## Pages read

All 15 `.md` pages were read in full. The `.tsv` files were used only to confirm layouts and counts, and no item below
rests on a `.tsv` alone. The six `gen_*.py` / `label_table_scan.py` scripts are tools, not pages, and were not used.

| page | lines | status line as the page states it |
|---|---:|---|
| `README.md` | 82 | category index; "Functions \| 108" (`README.md:8`); `Weather/` "**documented**" (`:16`), `Field-Record-Table/` "**documented**" (`:24`), `Map-Pack/` "**documented 2026-09-12**" (`:30`); a "Not yet documented" list at `:37-42` |
| `CONTRACT-authored-trigger-points.md` | 285 | `readiness: CONTRACT READY` (`:6`); `confidence: PROVEN` (`:7`); `last_reviewed: 2026-09-29` (`:19`) |
| `walking-into-an-authored-trigger-point.md` | 171 | `status: AUDITED` (`:4`); `last_reviewed: 2026-09-03` (`:18`) |
| `CONTRACT-field-environment-variant.md` | 247 | `readiness: CONTRACT READY` (`:6`); `confidence: PROVEN` (`:7`); `last_reviewed: 2026-09-29` (`:18`) |
| `choosing-the-field-environment-variant.md` | 250 | `status: AUDITED — every register row is closed (owner re-status 2026-09-30, OPUS) …` (`:4`); `last_reviewed: 2026-09-30` (`:19`) |
| `CONTRACT-field-record-accessors.md` | 616 | `readiness: DIFFERENTIAL TESTED   # the ALGORITHM, over a PLANTED table; the authored data is unread — see §13` (`:6`); `last_reviewed: 2026-09-11` (`:17`) |
| `Field-Record-Table/field-record-table-navimapdata.md` | 1,224 | `status: AUDITED` (`:4`); `last_reviewed: 2026-09-08` (`:21`) |
| `Field-Record-Table/field-record-bit15-action-permission.md` | 347 | `status: AUDITED` (`:4`); `last_reviewed: 2026-09-02` (`:18`) |
| `CONTRACT-weather.md` | 751 | `readiness: BEHAVIORALLY UNDERSTOOD` (`:6`); `confidence: PROVEN` (`:7`); `last_reviewed: 2026-09-21` (`:19`) |
| `Weather/weather-slot-state-model.md` | 366 | `status: DOCUMENTED` (`:4`); `last_reviewed: 2026-09-02` (`:20`) |
| `Weather/weather-probability-and-transition-roll.md` | 409 | `status: DOCUMENTED` (`:4`); `last_reviewed: 2026-09-02` (`:19`) |
| `Weather/weather-apply-and-environment-materialization.md` | 575 | `status: DOCUMENTED` (`:4`); `last_reviewed: 2026-09-02` (`:19`) |
| `Weather/mweather-resource-format.md` | 418 | `status: DOCUMENTED` (`:4`); `last_reviewed: 2026-09-02` (`:19`) |
| `Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md` | 339 | `status: DOCUMENTED` (`:4`); `last_reviewed: 2026-09-02` (`:19`) |
| `Map-Pack/the-map-ctrl-pack.md` | 1,850 | `status: AUDITED` (`:4`); `last_reviewed: 2026-09-12` (`:20`); `corpus_validated: "550 / 550 .mpk in the archive index, all split, 2026-09-12"` (`:19`) |

| `.tsv` (layout / count check only) | rows | agrees with |
|---|---:|---|
| `authored-trigger-live-set-accesses.tsv`, `authored-trigger-live-entry-accesses.tsv` | 12 + 12 | the ring at `02EC3EA0`: `+0x24` index and `+0x28` count written by `002FB3B0`, "stride=0xC count=3" (`CONTRACT-authored-trigger-points.md:97-100`). These files also list two readers that no page describes, `002F82F0` and `002FA740` (see G-2). |
| `map-ref-image-header-accesses.tsv`, `map-ref-field-row-accesses.tsv`, `map-ref-weather-block-accesses.tsv`, `map-ref-weather-lane-accesses.tsv` | 15 + 18 + 4 + 4 | `map_ref.bin` row reads: `word [+0]` (`00264F10`, `0026D910`), `word [+2]` (`00264F40`, `00264FD0`, `0026D910`), `word [+4]` (`00264ED0`) and `word [+6]` (`00264F90`, `0026DB30`); block stride `0x10`, 93 blocks. These are the 16-bit reads `choosing-the-field-environment-variant.md:24` and `Field-Record-Table/field-record-table-navimapdata.md:1139-1143` describe (see C-V20). |
| `group-persistent-bank-accesses.tsv` | 18 | `02099FF0` bank import/export (`WorldPersistence_*`); no 03 page discusses it beyond `Weather/weather-slot-state-model.md:70`, `:137` (`scratch2`) |
| `Weather/shadow-settings-01f82ea8-accesses.tsv` | 18 | the shadow-parameter object through `01F82EA8` (`Weather/weather-apply-and-environment-materialization.md:178-179`, `:213-220`) |
| `Field-Record-Table/members/label-tables-scanned.tsv` | 6 | the UQ-82/UQ-85 label search (`Field-Record-Table/field-record-bit15-action-permission.md:207-209`) |
| `Map-Pack/members/map-ref-field-packs.tsv` | 1,315 data rows | row word `+0`: 531 distinct values, range 1..775. These are the same count and range `CONTRACT-weather.md:342` gives for "MWeather selectors" (see G-6). Block word `+0`: 93 distinct values, max 772. |
| `Map-Pack/members/actl-census.tsv`, `sp1-census.tsv`, `wd-census.tsv`, `mrp-census.tsv`, `ym00-census.tsv`, `ym00-tag2226-census.tsv` | 270 / 456 / 46 / 2 / 8,297 / 918 data rows | the per-section censuses `Map-Pack/the-map-ctrl-pack.md` §2.1–§2.5 cite; the headers match the documented layouts |

---

## 1. Interface

The category holds four systems that share a few accessors but do not call each other in a cycle:

- **Authored trigger points.** A per-call proximity test over at most 32 authored points per field. A fixed 75/25 roll
  picks one of two outcomes, a once-only bit is cleared, and a story flag is set
  (`CONTRACT-authored-trigger-points.md`, `walking-into-an-authored-trigger-point.md`).
- **The field record table** (`navimapdata.bin`). One 3-byte record per field, read by seven accessors. Its bit 15
  waives the KO / Stone / X-Zone "out of play" rule. Two save-payload bits can override or veto parts of it
  (`CONTRACT-field-record-accessors.md`, `Field-Record-Table/*`).
- **Weather.** A slot in `1..3` per field. It is chosen once per field setup by a retention roll and committed by
  `0026D910`. It is published as gameplay globals (combat element scaling) and handed to the presentation backend, with
  `map_ref.bin` and the MWeather (`GRMI`) table as authored inputs (`CONTRACT-weather.md`,
  `CONTRACT-field-environment-variant.md`, `choosing-the-field-environment-variant.md`, `Weather/*`).
- **The map-control pack** (`.mpk`). Two packs per field, each split into 32 sections and dispatched to sound,
  navigation, world data (`YM00`), actor control (`ACTL`), lights (`LGT2`), emitters (`SP1`) and minimap pictures
  (`Map-Pack/the-map-ctrl-pack.md`). The LegacyPS2GS texture rebuild `002F7380` consumes `YM00` data and the weather
  slot (`Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md`).

### 1.1 Entry points (functions, with their callers)

#### Authored trigger points

| entry | callers | what it does | cite |
|---|---|---|---|
| `BattleUnit_TryTriggerNearbyAuthoredFieldAction` `002F8060` (648 B) | **not stated** in 03 | eligibility test; for each of at most `min(count, 32)` live points: a 2-D distance against `1.2999999523` (both heights zeroed); on a hit, a `% 100` roll against 75, set the flag, deliver, notify, clear the bit, `break` | `CONTRACT-authored-trigger-points.md:49`, `:69-107`, `:145-147`; `walking-into-an-authored-trigger-point.md:30`, `:44-105` |
| `002FB3B0` ring store | "called only by this body after a fire" | stores `{field, mask}` into the 3-slot ring at `02EC3EA0`, write index `+0x24`, count `+0x28`, index modulo 3 | `CONTRACT-authored-trigger-points.md:97-100`, `:247-248` |
| `002FA230` ring clear | two call sites, "one inside the battle-system runtime reset"; named as `00233C10` and `00237DF0` | zeroes `02EC3EA0`..`02EC3EC8` | `CONTRACT-authored-trigger-points.md:100`, `:251-252`; `Weather/weather-slot-state-model.md:337-343` |
| callees named only | — | `003A1920` 3-D distance + `sqrtf` (`walking-into-an-authored-trigger-point.md:138-141`); `00379CD0` MT19937 thunk; `0032AD70` `PersistentFlag_SetBank512Low`; `002FB8C0` "build the activation" (`+0x0A` fast path, `CONTRACT-authored-trigger-points.md:61-62`); `0046A9D0` "hand the chosen value to the acting unit"; `003EC700(index, 3)` "notify" | `walking-into-an-authored-trigger-point.md:90-92` |

#### The field record table

| entry | callers | returns | cite |
|---|---|---|---|
| `00377C20` `FieldData_GetActiveFieldRecordBit15` (78 B) | 79 sites in 66 functions, plus thunk `00313F60` (5 B) with 67 sites in 47 functions; the counts disagree between pages (C-V8) | bit 15 of the active-or-pending field's record; 0 on failure | `CONTRACT-field-record-accessors.md:45`, `:127-137`; `Field-Record-Table/field-record-bit15-action-permission.md:47-69` |
| `00377480` (61 B) | 1 caller, `ActorManager_BindLoadedDefinitionPayload` `0026C8C0` | bit 15 by explicit id | `CONTRACT-field-record-accessors.md:46`, `:135`; `Field-Record-Table/field-record-table-navimapdata.md:135`, `:237` |
| `00377A40` (67 B) | 5 UI functions; `003F92B0` reads it, then calls `00377870` | bit 14 (area-name display) | `Field-Record-Table/field-record-table-navimapdata.md:136`, `:518` |
| `00377BA0` (102 B) | **only** through thunk `00320160` (8 sites, 4 functions): `002F9400`, `002F91A0`, `002F9240`, `AiOrder_EvaluateTargetSelector` `00301AD0` | bits 12–13 (the MP regime), or the save override | `CONTRACT-field-record-accessors.md:48`, `:136-143`; `Field-Record-Table/field-record-table-navimapdata.md:563-568` |
| `003779F0` (72 B) | 9 functions: UI, achievements `003160C0`, `00576A50` | bits 0–11, the navigation-map id; `0xFFF` → `-1` | `CONTRACT-field-record-accessors.md:49`; `Field-Record-Table/field-record-table-navimapdata.md:516` |
| `00377700` (77 B) | 6 ActorEntity / Movement functions; `0026A1D0` and `00268D10` fold it into `02099DE7` | third byte bit 0, inverted, vetoed by payload `+0x1062` bit 0 | `CONTRACT-field-record-accessors.md:50`, `:79-83`; `Field-Record-Table/field-record-table-navimapdata.md:576-582` |
| `00377C70` (68 B) | `PartyFocus_SelectAndRequestDefaultActor` `00326500`, `BattleGroup_RefreshFourActorDefinitions` `003266C0`, `0031C000` | third byte bits 4–6, the default focus id in runtime mode 3 | `Field-Record-Table/field-record-table-navimapdata.md:140`, `:537-550` |
| `00378540` `WorldAreaField_RequestAuthoredMapTables` (943 B) | sole caller `00377CC0` | registers seven publishers (`MapInfo` → `00378B80` → `02ADD100`; `MWeather` → `00378F70` → `02ADD0B0`; …) | `Field-Record-Table/field-record-table-navimapdata.md:73-102`, `:213`, `:217` |
| `0030D9A0` `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` (105 B) | not stated in 03 | bit 15 → mode 3, pre-empting mode 2; calls `00377C20` directly | `Field-Record-Table/field-record-table-navimapdata.md:643-646`; `Field-Record-Table/field-record-bit15-action-permission.md:306-310` |

#### Weather: decide, commit, publish

| entry | callers | what it does | cite |
|---|---|---|---|
| `002620E0` field-runtime init core (231 B) | `ActorManager_RunFieldRuntimePass` `0025D9E0` | gates: `dword[rcx+0x28] == 0` (primary manager) and `byte[rcx+0x10] & 4` clear; runs the roll and the EFB / resource posts, sets bit 4; posts `003601C0(0x0B)`, `(0x0C)` on every pass | `CONTRACT-weather.md:64-65`, `:131-139`, `:252-261` |
| `0025ACA0` the roll (107 B) | sole direct caller `002620E0` | retention roll; tail-jumps into `0026D910` at `0025AD06` | `CONTRACT-weather.md:64`, `:67`, `:468-473`; `Weather/weather-probability-and-transition-roll.md:173` |
| `0025ABA0` alternate resolver (253 B) | `0025ACA0` | from slot 1: 2, then 3, then 1; from 3: 2, then 1, then 3; from 2: one draw, `<50` → 3 then 1, else 1 then 3, else 2 | `CONTRACT-weather.md:297-308`, `:475-480` |
| `002658B0` probability (112 B) | `0025ACA0`, `0025ABA0` | `signed byte[section + 1 + clamp(s−1, 0, 2)]` from script header `+0x64`; 33 when no script | `CONTRACT-weather.md:312-320`, `:482-485` |
| `0026D910` the apply (418 B) | the roll (tail jump); `003565C0`; `00266D10` at `00266E74` and `00266E7B`. The pages disagree on this set (C-V14). | clamp, latch gate, commit `+0x1060`, publish `00180620` and four globals, extract the MWeather preset, clear `+0x1061`, tail-jump `002E3D40(0,0,0,0)` | `CONTRACT-weather.md:64-67`, `:434-457`; `choosing-the-field-environment-variant.md:77-105` |
| `003565C0` `setweatherslot` handler, verb `0x021A` (99 B) | the script VM verb table | three guards on `[02099D70]`, clamp 1..3, `0026D910(slot)` then `0026D8F0()` | `CONTRACT-weather.md:263-266`, `:322-328` |
| `0026D8F0` arm-restore (21 B) | `003565C0` | sets payload `+0x1061 = 1` | `CONTRACT-weather.md:64`, `:79`; `Weather/weather-slot-state-model.md:69` |
| `00268320` `WorldPersistence_ResetBanksAndMarkInitializationState` (88 B) | `00280140`, `0036FCC0`, `00394130` | sets `+0x1061` when `dword 0209AC10 == 0`; clears `scratch1` always and `scratch2` conditionally | `Weather/weather-slot-state-model.md:70`, `:89-92`, `:137` |
| `00265920` canonical getter (41 B) | 20 callers (5 measured) | debug override if positive, else `s8(payload+0x1060) + 1` | `Weather/weather-slot-state-model.md:58-60`, `:66`; `Weather/weather-apply-and-environment-materialization.md:432-437` |
| `002E3D40` presentation refresh / "map wind" entry (116 B) | the `0026D910` tail jump (mode 0); `setmapwind` `0034B6C0` (mode 1, three pops); `defaultmapwind` `0034BD10` (mode 0) | mode 0: preset, azimuth and elevation from the MWeather extractors for the current field and committed slot; mode 1: the script's three values; then `jmp 0040AAD0` | `README.md:50-57`; `Weather/mweather-resource-format.md:316-367`; `choosing-the-field-environment-variant.md:141` |
| `003777C0` packed reader (144 B), wrappers `00377850` (preset), `003777A0` (azimuth), `003777B0` (elevation) | `0026D910`, `002E3D40` | `9·(3·selector + slot)` bit base, MSB-first walk, selector bound `word[+6]`, slot unbounded | `CONTRACT-weather.md:157-170`, `:459-466`; `Weather/mweather-resource-format.md:47-59`, `:369-382` |
| `0040AAD0` presentation backend init (286 B) | `002E3D40` | `0040B3B0` preset, 16 × 22.5° azimuth, elevation 0 / +30° / −30°, ±0.15 rad PRNG perturbation, `0040B430` frame publish | `Weather/mweather-resource-format.md:61-122` |

#### Field-init fan-out and the LegacyPS2GS rebuild

| entry | callers | what it does | cite |
|---|---|---|---|
| `00379290` field-resource bridge (53 B) | only `002620E0` | if `[02ADD090]` is non-null: `byte[02ADD0E9] = 1`, tail `0026E8D0(00265920())`; else clear and fall into `00379630` | `Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md:60-62`, `:121`; `Weather/weather-probability-and-transition-roll.md:326` |
| `00379630` (291 B), `00379760` (249 B) | `00379290` | rebuild the `02ADD125` preset handles from the `0x50`-stride preset table `02C1F460` (5 entries, `0037AD10`) | `Weather/weather-probability-and-transition-roll.md:327-330` |
| `0026E8D0` Movement resource reconfiguration | `003792B0`, `003796A2` | stores the slot into `0209A6E8` and sets dirty | `Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md:64-66`, `:276` |
| `0026E290` (97 B) | not stated in 03 | on `*(0209A670)`: if `0209A708` is set, `002F7380(object, *0209A668)` and clear the flag; then the `+0x130` callback | `Map-Pack/the-map-ctrl-pack.md:1823` |
| `002F7380` LegacyPS2GS mip-budget / slot-table rebuild | `0026E290` | three passes (measure, count references, select under budget), then a `count × 40` table at `+0x218` | `Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md:184-241`, `:297-320` |

#### The map-control pack

| entry | callers | what it does | cite |
|---|---|---|---|
| `00331990(field)` | not stated in 03 | `00378A60(field, MapRef_GetAuxValue0(field), 0)`, then `00378A60(field, MapRef_GetPrimaryFieldValue(field), 1)` | `Map-Pack/the-map-ctrl-pack.md:1074-1081` |
| `00378A60` / `00378030` | `00331990`; debug verb `mapload` `0x2001` (mode 1) | sizes with `0032E400(4, index)`, allocates `MapN`, submits with completion `00378BC0`, stores `MapRef_GetAuxValue1(field) + 500` at `02ADD078`; mode 1 also calls `00379A10(4, index)` | `Map-Pack/the-map-ctrl-pack.md:1081-1090` |
| `00377DC0` | before the pack request | requests the loose `PS2Data\efb\<map>.efb` (completions `003788F0` / `003789A0`) | `Map-Pack/the-map-ctrl-pack.md:1085-1087` |
| `0036B980` split (727 B) | `0036B970` from the completion | carves 32 arena blocks in place; rejects `count > 32` or a size-sum mismatch | `Map-Pack/the-map-ctrl-pack.md:1092-1106`, `:1405-1423` |
| `00378BC0` dispatch | the load completion | routes slots per mode, frees 1, 12 and 13 (and, in mode 1, also 0 and 10), sets pending and bind bits, calls `003775D0` when nothing else is pending | `Map-Pack/the-map-ctrl-pack.md:1108-1135` |
| `003775D0` bind, `00378120` (266 B) | `00378BC0` | sound (`003635C0`, `003635E0`), `ACTL` (`003E8940`), lights (`0037AA90(lights, 0)`, `003DE920`), `YM00` (`0026E7D0` mode 0 / `0026E760` mode 1 → `002F6AB0`), navigation, picture 0, placement 0 | `Map-Pack/the-map-ctrl-pack.md:1141-1152`, `:1470-1479` |
| `002F6AB0` the `YM00` constructor (2,118 B) | `0026E760`, `0026E7D0` | tag-indexed chunk dispatch (34-case table at `002F72F8`); installs callbacks `002F5450` (destructor), `002F4520` (update), `002F5550` (presentation), `002F5540` (getter) | `Map-Pack/the-map-ctrl-pack.md:1158-1206`, `:768-781` |
| `ACTL` family: `003E8940` install, `003E8230` lookup, `003E7EC0` first-touch pass, `003E8D50` activate-all, `003E82F0` query, `003E8BF0` activate-by-id, `003E88C0` / `003E8900` retag, `003E8890` / `003E8860` pause | `00314020` (first-touch); verbs `animeplay 0x213`, `animesync 0x214` (`003567F0` / `00355300`), `animepause 0x218`, `animepauseclear 0x219`, `animeplaytiming 0x280` | the per-record state machine of §2.1 | `Map-Pack/the-map-ctrl-pack.md:299-330`, `:385-404` |
| `LGT2` family: `0037AA90` installer, `0037A450` charge tick, `0037A5B0` channel evaluator, `0037B030` pending test | slot-17 binder (group 0); `0032F1B0(idx)` (groups 1–4) | light groups at `02EBF420` (5 × `0x50`) | `Map-Pack/the-map-ctrl-pack.md:244-251`, `:340-383` |
| `SP1` family: `003635C0` install, `003631B0` walker, `003638B0` voice start, `00363B40` weather-variant list | `003775D0`; `002620E0` (`00363B40`) | emitter records, listener grid, per-slot volume | `Map-Pack/the-map-ctrl-pack.md:882-934` |
| `map_ref.bin` loader and accessors: `00268750` `MapRef_BeginLoadResources` (requests (9,4) → `02099D88` and (9,2) → `02099D98`); `00264F10` primary value (row `+0`); `00264F40` aux 0; `00264FD0` aux 1; `00264ED0` area (row `+4`); `00264F90` group (row `+6`) | bootstrap | the field-indexed authored table | `choosing-the-field-environment-variant.md:107-128`; `Map-Pack/the-map-ctrl-pack.md:1281-1283`; `Field-Record-Table/field-record-table-navimapdata.md:1138-1143` |

### 1.2 Inputs and outputs (data read and written, with record layouts)

#### Authored trigger point record (stride and container not stated: G-1)

```
+0x00  s16  first coordinate, tenths   (÷ 10.0, constant at 008F8180)
+0x02  s16  second coordinate, tenths
+0x04  u8   persistent flag id, 0xFF = set none
+0x06  u16  outcome on the < 75 branch
+0x08  u16  outcome on the >= 75 branch
+0x0A  u8   read by 002FB8C0: zero takes a fast path   ("so the record is at least 11 bytes")
```

`CONTRACT-authored-trigger-points.md:54-63`; `walking-into-an-authored-trigger-point.md:82-88`. The live set is a ring
of three `{field, mask}` records, 12 bytes each, at `02EC3EA0`, with the write index at `+0x24` and the count at `+0x28`
(`CONTRACT-authored-trigger-points.md:97-100`).

Eligibility is read from the acting unit's record at `+0x698` (`walking-into-an-authored-trigger-point.md:109`):
- bit 26 of `(rec[+0x64] | rec[+0x3C])`;
- bit `0x20` of `rec[+0x6C]` and of `rec[+0x7C]`;
- `rec[+0x05] != 1`, and when `rec[+0x05] == 0`, `rec[+0x04]` outside `0x1B … 0x27` (the thirteen Espers).

Cites: `walking-into-an-authored-trigger-point.md:111-114`; `CONTRACT-authored-trigger-points.md:109-120`, `:185-191`.

**Outputs:**
- one persistent flag (`0032AD70(id, 1)`) unless the id is `0xFF`;
- the chosen outcome to `0046A9D0`;
- `003EC700(index, 3)`;
- the cleared live bit through `002FB3B0`.

Cites: `walking-into-an-authored-trigger-point.md:90-96`; `CONTRACT-authored-trigger-points.md:130-132`.

#### The field record table (`navimapdata.bin`, kind 9 index 8, published to `02ADD100`)

```
+0x00  u32  magic 'N''A''V' 0x02   (0x0256414E)
+0x04  u32  fieldCount  1154        bound every accessor tests, UNSIGNED (jae)
+0x08  records, stride 3 (never padded to 4)
  record +0x00 u16 flags (composed from two byte loads; no 16-bit load anywhere)
    bits 0-11 navigation-map id (0xFFF = none -> -1) | 12-13 MP regime | 14 area-name display | 15 action-permission override
  record +0x02 u8 thirdByte ("packedOptions")
    bit 0 safe-area flag (read inverted) | bits 1-3 authored, read by nothing | bits 4-6 default focus id | bit 7 unused
```

`Field-Record-Table/field-record-table-navimapdata.md:277-296`, `:334-349`, `:524-535`;
`CONTRACT-field-record-accessors.md:53-69`, `:95-97`.

**Save overrides** (payload base `02164280 + 0x200`):
- `00377BA0` returns `(+0x1063 >> 4) & 3` instead of the table when `+0x1062` bit 7 is set. This is a replacement, done
  by tail jump.
- `00377700` returns 0 when `+0x1062` bit 0 is set. This is a veto.

Cites: `CONTRACT-field-record-accessors.md:150-221`, `:360-364`.

**Failure constants:**
- 0 for bits 15, 14 and 12–13;
- `−1` for bits 0–11;
- **1** for `00377700`;
- 0 for bits 4–6.

Cites: `CONTRACT-field-record-accessors.md:239-246`. The reproduction formula is `CONTRACT-field-record-accessors.md:321-347`.

**The gate the table answers:** `refuse = ((bkbi[+0x64] | bkbi[+0x3C]) & 0x80000003) != 0 && 00377C20() == 0`. The third
mask `+0x38` is not consulted (`Field-Record-Table/field-record-table-navimapdata.md:357-367`). There are 55 mask sites
with no waiver (`:660-664`).

**Shipped census** (`Field-Record-Table/field-record-table-navimapdata.md:474-522`):
- bit 15 on 193 of 1,154 fields;
- third-byte bit 0 on 170 fields, all inside the bit-15 set;
- bits 12–13 = `0`:945, `1`:36, `2`:69, `3`:104;
- bits 4–6 zero everywhere.

#### `map_ref.bin` (kind 9 index 4, `MRF` v2, at `[02099D88]`, guard `[02099D90]`)

| header | holds | cite |
|---|---|---|
| `+0x04` | field-row array, stride 8, 1,315 rows | `CONTRACT-weather.md:94`; `choosing-the-field-environment-variant.md:85-91` |
| `+0x08` | 16-byte block array, 93 blocks | `CONTRACT-weather.md:95` |
| `+0x10` | count, then `u32[]`: the environment-class table, 16 entries `{4,4,4,0,0,1,2,2,3,0,…}` | `CONTRACT-weather.md:96` |
| `+0x14` | count, then `u32[]`, 32 entries, "not read by this subsystem" | `CONTRACT-weather.md:97` |
| `+0x18` | count, then `u8[]`: the boolean table, 16 entries | `CONTRACT-weather.md:98` |
| `+0x0C`, `+0x1C`, `+0x20`–`+0x2F` | zero; nothing reads them | `CONTRACT-weather.md:99-100` |

The field row and the block lanes are typed differently on different pages (see C-V20, G-6):
- `CONTRACT-weather.md:102-117` gives the row as `{u16 mweatherSelector; s16 blockIndex; s32 (not read by weather)}` and
  the block as four `u8[4]` lanes.
- `choosing-the-field-environment-variant.md:24` gives the row as `{u16, i16, u16 area, u16 group}`.
- `Map-Pack/the-map-ctrl-pack.md:1283` gives the row as `{u16 own pack index, i16 block index, i16, i16}` and the block
  as `{i16 mode-0 pack index, i16 aux1, ...}`.

The weather lane for committed slot `c` (`0..2`) is `block + (c + 1)·4`:
- byte `+0` is `environmentIndex` (indexes both `+0x10` and `+0x18`);
- byte `+2` goes to `02099DB0`;
- bytes `+1` and `+3` are not read.

Cites: `CONTRACT-weather.md:108-117`, `:444-454`.

**Siblings:** `test_area_ref.bin` (9,2) is loaded to `02099D98` and never read; `test_map_ref.bin` (9,1) has no
requester (`choosing-the-field-environment-variant.md:107-128`).

#### Weather state and published values

| item | layout / rule | cite |
|---|---|---|
| payload `+0x1060` | the committed slot, `s8`, `0..2` | `CONTRACT-weather.md:78`; `Weather/weather-slot-state-model.md:77` |
| payload `+0x1061` | `bInitializationRestoreState`: when set, the next apply discards the request; cleared at `0026DA92` on every path | `CONTRACT-weather.md:79`, `:151-155` |
| debug `+0xAAC` | `s32` override; the singleton is named as `01F81428` on one page | `CONTRACT-weather.md:80`; `Map-Pack/the-map-ctrl-pack.md:852` |
| script `weatherProbability` | `.ebp` header `+0x64` → `u8 count, u8[count]`; retention probability per slot | `Weather/weather-probability-and-transition-roll.md:91-107`; `CONTRACT-weather.md:312-317` |
| MWeather / `gramap_weatherinfo.bin` (`GRMI01`) | count `u16` at `+6` = 776; 9-bit records from `+8`: bits 0–2 preset `0..7`, 3–6 azimuth sector, 7–8 elevation class | `Weather/mweather-resource-format.md:21`, `:151-161`; `CONTRACT-weather.md:124-125` |
| `02099DA8` | `A[4 + envIdx·4]` if `envIdx < A[0]`, else 0 (authored values `0..4`) | `CONTRACT-weather.md:449`, `:345` |
| `02099DAC` | `0` if preset `0`, `2` if preset `>= 4`, else `1`, computed from the **requested** slot | `CONTRACT-weather.md:450-451`, `:181-197` |
| `02099DB0` | lane byte `+2` (0 in all 279 shipped lanes) | `CONTRACT-weather.md:452`, `:347` |
| `02099DBC` | zeroed at entry, then `B[4 + envIdx]` | `CONTRACT-weather.md:438`, `:454` |
| `00180620` → `001A7E40` | publishes the committed slot's environment parameter bank: the shadow parameter set (`+0x140` / `+0x144` lerp minimums, light direction, `+0x870`..`+0x878` cascade partitions) | `CONTRACT-weather.md:441`; `Weather/weather-apply-and-environment-materialization.md:128-132`, `:213-225` |
| `0040B430` output | `02CA43A0` = `v/|v|`, `02CA43B0` = `normalize({0, 1, ~1e-5} × dir)`; gate ε = 1e-6 | `Weather/mweather-resource-format.md:74-104` |
| combat use | `0038B220`: `02099DAC == 2` → Fire ×1.2, Water ×0.5, Wind ×1.2; `02099DA8` arms for 0–3 only | `Weather/mweather-resource-format.md:253`; `CONTRACT-weather.md:422-426` |
| EFB posts | `0026FAD0(0, slot+1, mgr)` and `0026FAD0(0x1F, slot+1, mgr)`; enable byte `+7 + value` per binding row (meaning of the third argument disputed: C-V19) | `CONTRACT-weather.md:257-258`; `Weather/weather-probability-and-transition-roll.md:156-171` |

The full reproduction pseudocode for apply, the MWeather read, the roll, the resolver and the probability is
`CONTRACT-weather.md:433-486`.

#### Map-control pack (`.mpk`)

- **Header and slots.** `{u32 count = 32; u32 size[32]}`, padded to `0x40`. Each non-empty section is preceded by a
  `0x40` slot; there are no offsets. Slot usage and consumers are tabled at `Map-Pack/the-map-ctrl-pack.md:62-86`.
- **`ACTL`.** Header `:112-120`; id index and lookup (`id/100`, `id%100`, stride `0x16`) `:122-132`; record layout
  `:134-227`; aux rows and the `02EBF420` group resolution `:229-242`.
- **`LGT2`.**
  - The installer and the `{u16 size, u16 tag}` sub-record chain: `:244-269`.
  - Sub-record interiors: `:271-297`.
  - Member object fields and kinds 0, 1 and 2 (static, lerp, cubic curve): `:340-383`.
- **`YM00`.** Header and the fixed 17-tag schema `:430-478`; tag 11 `:486-502`; tag 30 `:504-525`, with runtime expansion
  `:527-576`; tag 22 `:642-688`; tag 26 `:610-629`.
- **`SP1`.**
  - Header: `:815-829`.
  - Emitter record: `:835-880`. Volume is `vol = (volMax−volMin)·(range−dist)/range + volMin`, then scaled by the
    per-slot percent and clamped to 0..127 (`:848-850`).
  - Listener grid (16×16): `:917-934`.
- **`WD` and `MRP`.** Both are decoded but are dead data (`:940-1064`).

#### LegacyPS2GS rebuild (`002F7380`)

- **Arrays.** Records at `[[rdi+0x150]+8]`, stride `0x60`, count `[rdi+0x224]`. Entries at `[rdi+0x178]`, stride `0x30`,
  count `[rdi+0x174]` (`Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md:198-201`).
- **Mask.** `1 << ([0209A6E8] + 0x17)` (`:187-194`).
- **Budget.** `(0x1007FF − 3·[022D8EAC]·[022D8EB4] − [02CA6008] − [02CA6004]) & ~0x7FF` (`:297-301`).
- **Output.** `[rdi+0x218]` holds `count × 40` bytes; only `+0x00` .. `+0x20` are written (`:231-238`).

### 1.3 State (globals and objects, with lifetime)

| state | lifetime as stated | cite |
|---|---|---|
| trigger ring `02EC3EA0` (3 × 12 B, `+0x24`, `+0x28`) | until `002FA230` (the battle-system runtime reset); when that reset runs relative to field entry is "not traced"; whether an evicted field re-arms is "not established" | `CONTRACT-authored-trigger-points.md:97-102`, `:251-252` |
| `02ADD100` field record table pointer | published by `00378B80` "once per boot", or bound "at area load" (C-V6) | `Field-Record-Table/field-record-table-navimapdata.md:681-682`; `Field-Record-Table/field-record-bit15-action-permission.md:162` |
| persistent payload `02164280 + 0x200`: `+0x1044` saved field id (clamped by `cmovs`), `+0x1060` / `+0x1061` weather, `+0x1062` / `+0x1063` field-record overrides | save image: "save, reload, and the slot is unchanged" | `CONTRACT-field-record-accessors.md:207-212`, `:360-364`; `CONTRACT-weather.md:421`; `CONTRACT-field-environment-variant.md:217` |
| `02099DA8`, `02099DAC`, `02099DB0`, `02099DBC` | rewritten per apply; only `02099DBC` is pre-zeroed, so the other three keep the previous field's values when the table is unloaded | `CONTRACT-field-environment-variant.md:101-109`; `CONTRACT-weather.md:400-403` |
| `02099DB4`, `02099DB8` | read by nine `cmp` sites and by `00264180`; **writers not stated** | `CONTRACT-weather.md:230-232` |
| ActorManager record (stride `0x288`) `+0x10` bit 4, `+0x28` index | bit 4 is set once per "qualifying manager-record lifecycle" | `Weather/weather-probability-and-transition-roll.md:73`, `:110-113` |
| MT19937 state `02EB3870` (624 dwords), index `02EB4230`, flag `02EB4234` | shared with combat formula and other layers; lazily seeded with 5489 | `CONTRACT-weather.md:351-358`, `:637-649` |
| `0209A6E8` | written by `0026E8D0` (the slot) and reset to 1 at `0026E653`; meaning disputed (C-V15) | `Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md:274-279` |
| party-hold bytes `02099DE3`–`02099DE7` | `DE7 = 0xFF` "not decided yet"; written by `002628B0`, `00263050`, `0026A1D0`, `00268D10` and `00266D10` | `Field-Record-Table/field-record-table-navimapdata.md:584-613` |
| `.mpk` statics `02ADD010`..`02ADD0B8`, pending / bind bits `02ADD0EC` / `02ADD0F0` | per pack load; teardown `00378230` and `003784A0` | `Map-Pack/the-map-ctrl-pack.md:1251-1266`, `:1801` |
| `YM00` context (`0x240` B), `0209A670` / `0209A668`, chunk globals `0209A660`, `02B5F1A0` / `02B5F1B0`, slot family `02EBB6E0` (`0x50` stride) | built by `002F6AB0`; freed by the `002F5450` destructor | `Map-Pack/the-map-ctrl-pack.md:764-781`, `:1158-1206` |
| `ACTL` pointer `02B5D080`, gate `02B5D088`; flag channels `u8[64]` at `02F8F23C` | install `003E8940`; teardown `003E82B0` | `Map-Pack/the-map-ctrl-pack.md:166-186`, `:299-318` |
| `LGT2` groups `02EBF420` (5 × `0x50`) | `0037B230` init; `0037AA50` clear | `Map-Pack/the-map-ctrl-pack.md:233-251` |
| `SP1` `022CBAF0`, `SPP1` `022CBAF8`, gather array `022CBB58` | `003635C0` and `003635E0` installs | `Map-Pack/the-map-ctrl-pack.md:882-915` |
| `LegacyPs2GsTextureContext` `0209A670`, table `+0x218` | reallocated on every rebuild; `+0x00` and `+0x20` are reset every frame by `002F4520` | `Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md:280-296` |

### 1.4 Order (what runs when, and what triggers it)

1. **Boot.**
   - `00377CC0` → `00378540` registers the map tables (`Field-Record-Table/field-record-table-navimapdata.md:629-633`).
   - `0022A0B0` → `00266D10` → `0026D910(1)` at `00266E74`, then again at `00266E7B`. If a restore is armed, pass 1
     materialises the saved slot and disarms it, and pass 2 commits slot 1 (`CONTRACT-weather.md:268`;
     `Weather/weather-apply-and-environment-materialization.md:76-94`, `:152-164`).
2. **Field entry: pack load.**
   - `00331990(field)` requests the mode-0 (block, sound) pack and the mode-1 (own) pack. The completion `00378BC0` splits
     and dispatches them, and binding runs in `003775D0` once nothing is pending
     (`Map-Pack/the-map-ctrl-pack.md:1074-1152`).
   - **Not stated:** when `00331990` runs relative to `0025D9E0` / `002620E0`, or whether binding is guaranteed to finish
     before the weather roll (G-7).
3. **Field-runtime pass** (`0025D9E0` → `002620E0`, once per qualifying manager-record lifecycle), in this order:
   - `00259B30`, `003E8980(0)`;
   - the roll `0025ACA0` → the apply `0026D910` → `002E3D40` → `0040AAD0`;
   - `0026FAD0` channels 0 and `0x1F`;
   - `00379860`, `00379290`, `003DE920(0,1,0)`, `00363B40`;
   - set init bit 4;
   - `003601C0(0x0B)`, `003601C0(0x0C)`. These two also run when the init bit is already set.

   Cites: `CONTRACT-weather.md:252-261`, `:383-385`; `Weather/weather-probability-and-transition-roll.md:313-322`.
   "**There is no weather timer**" (`CONTRACT-weather.md:384-385`).
4. **Runtime script.** `setweatherslot` → `0026D910(slot)` → `0026D8F0()` (arms the restore for the **next** apply). It
   does not reach the Movement / GS rebuild (`CONTRACT-weather.md:263-266`;
   `Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md:94-103`).
5. **Per frame** (callers named, frame position not stated):
   - `0026E290` → `002F7380` when `0209A708` is set, then the `YM00` update callback `002F4520`
     (`Map-Pack/the-map-ctrl-pack.md:1823`);
   - the presentation pass `002F5550` (`:775`);
   - the `SP1` driver `0x362ACE` (`:928-931`);
   - `ACTL` first-touch `00314020` → `003E7EC0` (`:399`);
   - `LGT2` charge `+1.0`/tick (`:352`).
6. **Trigger points.** One call fires at most one point (`CONTRACT-authored-trigger-points.md:92-96`). Who calls it and
   how often is **not stated** (G-1).
7. **Field-record accessors.** Pure reads on demand. The id comes from `003148F0` "active-or-pending", so during a
   transition the answer is already for the field being entered
   (`Field-Record-Table/field-record-bit15-action-permission.md:61-62`, `:176-178`).

### 1.5 Dependencies (on other systems)

| system | what 03 needs from it | cite |
|---|---|---|
| Script VM (01) | the verbs `setweatherslot` `0x021A`, `setmapwind` `0x0481`, `defaultmapwind` `0x0482`, `animeplay` / `animesync` / `animepause` / `animepauseclear` / `animeplaytiming`, `initgauge` `0x01AB`, `mapload` `0x2001`; the `.ebp` container `[02098E10]` | `README.md:50-53`; `Map-Pack/the-map-ctrl-pack.md:385-397`; `CONTRACT-weather.md:312-317` |
| Save / load (19) | the persistent payload base `002EF2B0` → `02164280 + 0x200`; `00280140` restore route | `CONTRACT-field-record-accessors.md:360-364`; `Weather/weather-apply-and-environment-materialization.md:158-160` |
| RNG (21) | the gameplay MT19937 `00379CD0` / `00863BF0`, one stream shared with combat | `CONTRACT-weather.md:351-358`, `:637-641` |
| Story flags (14) | `PersistentFlag_SetBank512Low` `0032AD70` | `walking-into-an-authored-trigger-point.md:90` |
| Status (10) | the three status masks and `0x80000003`; `0030E360` | `Field-Record-Table/field-record-table-navimapdata.md:157-197`, `:369-418` |
| Combat formula (08) / AI (09) | readers of `02099DAC` / `02099DA8` (`0038B220`, `00301AD0`); bits 12–13 consumers | `CONTRACT-weather.md:212-220`; `Field-Record-Table/field-record-table-navimapdata.md:563-568` |
| Presentation (17) | `0040AAD0`, `0040B3B0`, `0040B430`, `0040FF30` (the oscillator), the shadow object `001F0850`, EFB `0026F470` | `Weather/mweather-resource-format.md:61-122`, `:223-232`; `Weather/weather-apply-and-environment-materialization.md:178-225` |
| Movement / navigation (06) | `0026E8D0`, `Navigation_BindAndRebaseDataset` (slot 4) | `Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md:64`; `Map-Pack/the-map-ctrl-pack.md:77` |
| Audio (18) | `SeSep` `002DF070`, `SPP1`, the voice path `002DF410` / `002DEFA0` | `Map-Pack/the-map-ctrl-pack.md:80`, `:838-840`, `:931` |
| Actor (04) | `ActorManager_RunFieldRuntimePass` `0025D9E0`, `Actor_GetWorldPosition`, `ActorManager_BindLoadedDefinitionPayload` | `CONTRACT-weather.md:253`; `walking-into-an-authored-trigger-point.md:156-157` |
| Resource (02) | `Resource_SubmitRequest` `0032E620`, `0032E400`, the `(kind, index)` path table, `0020E600` / `0020E620` | `Field-Record-Table/field-record-table-navimapdata.md:114-118`, `:221-222` |
| Party (11) | `00326500` default focus (mode 3) | `Field-Record-Table/field-record-table-navimapdata.md:537-550` |

---

## 2. Gaps

### 2.1 Gaps the pages state themselves (still open, or live-only)

| id | gap | cite |
|---|---|---|
| S-1 | **What a trigger point does when it fires.** "**What this document does not claim:** what the two outcome values are, what `0046A9D0` does with the chosen one, what the persistent flag ids mean, what `003EC700`'s second argument `3` selects". The crossings section repeats that "the argument `3` remains unread". | `walking-into-an-authored-trigger-point.md:130-132`, `:159-160` |
| S-2 | **How long "once" lasts.** "Whether an evicted field is re-armed when revisited is not established". The ring clear's timing: "When it runs relative to field entry is not traced here". Persistence across save: "Whether it persists across a save is not established here." | `CONTRACT-authored-trigger-points.md:101-102`, `:251-252`; `walking-into-an-authored-trigger-point.md:127` |
| S-3 | Trigger points: "**None.** No experiment executes this body." (but see C-S6) | `CONTRACT-authored-trigger-points.md:178-181` |
| S-4 | **The null field-record window is live-only.** "Is `02ADD100` ever null while gameplay is running? … One breakpoint on `00377C5F` settles it"; and "everything a *player* could see" is not established. | `CONTRACT-field-record-accessors.md:310-314`, `:391-398`, `:427-429` |
| S-5 | Field record residues: third-byte bits 1–3 "authored and never read — **PROPOSED-repos2d-3**"; "the regime's authored name is not in the binary"; the designer names for bit 15 (UQ-82) and for the selector (UQ-85) are "OUT OF EVIDENCE BOUNDARY" | `Field-Record-Table/field-record-table-navimapdata.md:521`, `:574`, `:622-624`, `:767-770`; `Field-Record-Table/field-record-bit15-action-permission.md:207-209` |
| S-6 | "**What `00316A50` counts is not established here**" (the defeat path's achievement edge); "The area-id space behind `00377870` / `MapRef_GetPersistenceGroupId` was not derived" | `Field-Record-Table/field-record-table-navimapdata.md:984-987`, `:957-958` |
| S-7 | **GB-1 / I-7: is the two-slot divergence a defect or a design?** The variant page says "**NO ADMISSIBLE SOURCE**"; the weather contract's §14.1 says "Routed to ASTRA" | `choosing-the-field-environment-variant.md:138`; `CONTRACT-weather.md:502-504` |
| S-8 | "**What does `02099DA8` = 4 mean?**", a naming residue | `CONTRACT-weather.md:505-508` |
| S-9 | **The presentation consumers of the weather output.** The shadow-light direction's "shader binding at the descriptor's `+0x560` is still unread". The MWeather basis "*Not claimed:* that anything besides the oscillator reads the basis through another route, or what the preset field selects." | `Weather/weather-apply-and-environment-materialization.md:211-212`, `:224-225`; `Weather/mweather-resource-format.md:231-232` |
| S-10 | F-3 residue: "whether the controller path and the reset run in that order in a real load, and what `0x05BE`/`0x05BF` do in authored scripts" | `Weather/weather-slot-state-model.md:137` |
| S-11 | F-2's limit: "`edges.tsv` carries **direct calls**. An indirect or virtual call into `0026D910`, `00379290` or `0026E8D0` would be **invisible to this method**" | `Weather/weather-probability-and-transition-roll.md:173` |
| S-12 | EFB binding rows: "Which effect a row instantiates (its `+5` definition id through `0024F610`) and the rest of `0026F470` are the residue." | `Weather/weather-probability-and-transition-roll.md:169-170` |
| S-13 | LegacyPS2GS: "**What the 1-vs-4 factor MEANS is still open** — `D-6`"; "What sets those bits in the authored entries is not read here" (the slot-membership bits 24–26) | `Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md:261-262`, `:279` |
| S-14 | **Map pack residues.** `YM00` "per-tag contents open". Tag 12 binds against "the tag-32 payload (`not read`)". "Not established: which `00D12510`/`00D12520` table row each `0046xxxx` object registers under". `WD`'s X/Y "(unresolvable — no consumer)". The `ACTL` owner byte's writers are "a VM-lane question". Audio crossings "not read". `0026E760` / `0026E7D0` "◐ calls only"; teardown "◐". | `Map-Pack/the-map-ctrl-pack.md:78`, `:1176`, `:1221-1222`, `:1361-1362`, `:222-226`, `:1450`, `:1246`, `:1249` |
| S-15 | Weather runtime: "**Empty. Nothing in this contract has been observed on a running game.**" TIMING, INTEGRATION, PRESENTATION and FULL SUBSYSTEM are not tested | `CONTRACT-weather.md:488-496`, `:576-584` |
| S-16 | "NOT claimed: what `01F82E38`/`01DFE0C0` name semantically"; `0023A110` "weather-mode byte setter" of `0208D455`, with no reader or meaning given | `Weather/weather-apply-and-environment-materialization.md:414`, `:427` |
| S-17 | The category index still lists as "Not yet documented": "Area/zone identity and transitions" (the other three items there are now covered; see C-S1) | `README.md:37-42` |
| S-18 | `test_map_ref.bin`: "no requester found … the sweeps cannot see a kind/id computed at run time" | `choosing-the-field-environment-variant.md:123-128` |
| S-19 | Map-pack falsification: "the raw `.mpk` bytes were **not** re-read … Nothing was executed or observed live." | `Map-Pack/the-map-ctrl-pack.md:1425-1428` |

### 2.2 Structural gaps found while mapping (a port needs these and no 03 page states them)

| id | what is missing | why a port needs it | where the gap shows |
|---|---|---|---|
| G-1 | **Where the authored trigger points come from, and who runs the test.** Not stated: the container and stride of the point records; the `count` the loop bounds with `min(count, 0x20)`; how a field id selects its point array; the caller of `002F8060`, how often it runs and which unit it passes. | Without them the system cannot be driven at all. | `CONTRACT-authored-trigger-points.md:49`, `:104-107`; `walking-into-an-authored-trigger-point.md:30`, `:103-105` |
| G-2 | **Two more readers of the trigger live set.** `authored-trigger-live-set-accesses.tsv` lists `002F82F0` and `002FA740` reading `02EC3EA0`. No page describes `002F82F0`. `002FA740` is named only as "a 477-byte sibling … queries `PersistentFlag_QueryBank512Low` and draws the gameplay MT". | A second trigger-like path may share the ring and the generator. | `choosing-the-field-environment-variant.md:238-239`; `CONTRACT-weather.md:647`; the `.tsv` rows |
| G-3 | **The trigger's hit path.** `002FB8C0` is given only its `+0x0A` fast path; `0046A9D0` and `003EC700` are named, not described. | The visible effect of a trigger. | `CONTRACT-authored-trigger-points.md:61-62`; `walking-into-an-authored-trigger-point.md:90-92` |
| G-4 | **TP-6 drops a condition.** The page says "`rec[+0x05] != 1`, and when `rec[+0x05] == 0`, …". The contract states only "**`rec[+0x05]`** with, when it is 0, `rec[+0x04]` outside `0x1B … 0x27`". | Whether units with selector 1 are eligible. | `walking-into-an-authored-trigger-point.md:114`; `CONTRACT-authored-trigger-points.md:113-114` |
| G-5 | **When `navimapdata.bin` is loaded relative to gameplay** (boot or each area, see C-V6), and so whether the null-table window of S-4 exists. | The null window *grants* a permission at `00377700`, so the answer changes behaviour. | `Field-Record-Table/field-record-table-navimapdata.md:629-633`, `:681-682`; `CONTRACT-field-record-accessors.md:393-396` |
| G-6 | **No single `map_ref.bin` layout.** Three pages each type the bytes they need. Row word `+0` is the "MWeather selector" on one page and the "own pack index" on another; no page says it is one value used both ways. The `.tsv` gives 531 distinct values in 1..775 for row `+0`, the same count and range as the "selectors". Block bytes `+0..+3` are "lane 0 — NEVER read by weather" on one page and `{i16 mode-0 pack index, i16 aux1}` on another. Header `+0x14` (32 entries) has no reader named. | A port must write one reader for one file. | `CONTRACT-weather.md:97`, `:102-117`, `:342`; `Map-Pack/the-map-ctrl-pack.md:1077-1081`, `:1283`; `choosing-the-field-environment-variant.md:24` |
| G-7 | **The field-transition sequence.** Not stated, in order: when `00331990` (pack requests) runs relative to `0025D9E0` / `002620E0` (the weather roll); whether the asynchronous pack completion and binding can still be pending when the roll runs; when `003148F0` switches from "pending" to "active"; what `WorldTransition_StageFieldTransition` does. The README lists "Area/zone identity and transitions" as not documented. | Entering a field is the trigger for every system here. | `README.md:42`; `Map-Pack/the-map-ctrl-pack.md:1074-1090`, `:1130`; `CONTRACT-weather.md:383-385`; `Weather/weather-slot-state-model.md:137` (the only description of `003145E0`'s field-`0xC` branch) |
| G-8 | **How the committed slot picks the environment bank.** `publishEnvironmentBank(committed)` is `00180620 -> 001A7E40`, and `001A7E40(table, i)` "copies entry `i`". The per-index table is filled from the map JSON's light angles (`001C78D0(i, …)`). No page says how `i` relates to the weather slot, or what `00180620` passes. | Lighting / shadow per weather slot. | `CONTRACT-weather.md:441`; `Weather/weather-apply-and-environment-materialization.md:185-187`, `:202-206`; `Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md:337` |
| G-9 | **The presentation half of an apply.** Not stated: what the eight presets of `0040B3B0` are; the render PRNG behind the ±0.15 rad perturbation (`003D8E50`, "advances the shared Presentation PRNG by 14 steps"); the rotations `0046D160` / `0046D200`. | The sky / wind visual a slot produces. | `Weather/mweather-resource-format.md:64-69`, `:146`, `:175-179`; `Weather/weather-apply-and-environment-materialization.md:91-92` |
| G-10 | **The rest of the field-init core.** These callees appear only by name or callee list: `00259B30` ("a weather apply body", 699 B), `003E8980(0)`, `00379860` → `00379F50`, `003DE920(0,1,0)`, `00363B40` (partly described from the `SP1` side), and the meaning of events `0x0B` / `0x0C`. | Their order is stated (§1.4) but not what they do. | `CONTRACT-weather.md:255-261`; `Weather/weather-apply-and-environment-materialization.md:445`; `Weather/weather-probability-and-transition-roll.md:329`; `Map-Pack/the-map-ctrl-pack.md:890-915` |
| G-11 | **The EFB binding table** that `0026FAD0` / `0026F470` walk: only the channel byte `+4` and the enables `+7 + value` are given, and the operation itself is disputed (C-V19). | Weather-selective effects. | `Weather/weather-probability-and-transition-roll.md:156-171`; `Map-Pack/the-map-ctrl-pack.md:175-186` |
| G-12 | **The rest of the published block.** `02099DB4` / `02099DB8` have readers but no writer stated. The `02099DBC` reader `00264D50` ← `002E9D90` is not described. What `00301AD0` does with `02099DA8` is not stated. | A port publishing four cells may need six. | `CONTRACT-weather.md:217-220`, `:230-232`, `:674` |
| G-13 | **The `setweatherslot` guards:** `[02099D70]` `dword[+0x28] == 0`, `byte[+0x12] != 0`, `word[*(singleton)+0x50] == word[actorRecord]`. What the singleton and its fields are is not stated. | Which scripts can change weather. | `CONTRACT-weather.md:324-328` |
| G-14 | **`YM00` per-chunk semantics.** Not described: tag 23's builder `00466E70` beyond the slot-family header; tag 12 / `00468160` and the tag-32 payload; tag 25 `003ED190` and tag 9 `003ED3F0` (callee lists only); the two `0x68` sub-records (tags 17 / 31); the tag-24 `0xE0` entry beyond `+0xBC` / `+0xC0` / `+0xC8`; the full `0x50`-stride slot record at `02EBB6E0` (`+0x38` and `+0xA8` are used); runtime `+0x1FC` / `+0x200` "(their semantic names unproven)". | `YM00` is the world data of every field pack. | `Map-Pack/the-map-ctrl-pack.md:477`, `:1174-1182`, `:1193-1196`, `:739-744`, `:146`, `:363`, `:678-679` |
| G-15 | **The `LGT2` output's consumer:** `0037AExx` / `0037AF4D` collect `member+0x30` pointers into `02EBF5C0` "for the renderer". No 03 page says what the renderer does with it. | Light animation. | `Map-Pack/the-map-ctrl-pack.md:353` |
| G-16 | **Weather → spawn.** Two pages say spawn eligibility depends on weather. No 03 page names the reader. | Ordering on field entry and late join. | `Weather/weather-probability-and-transition-roll.md:150-152`; `Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md:109-112` |
| G-17 | **Serialization of the payload bytes** (`+0x1044`, `+0x1060`–`+0x1063`) is deferred: "the two payload bytes are covered by the save-image layout, which owns its own parity". | Save / load parity. | `CONTRACT-weather.md:582-583` |

---

## 3. Contradictions (statements a re-implementer would have to choose between)

Quotes are exact; `…` marks an elision only, and `/` separates two quoted lines. "Favoured" is named only where a dated
correction on the pages settles the point. Otherwise the item says **no favoured side**. Every item in 3.1 is
**page-text only - needs local check**: this session cannot see the executable. A favoured side is a reading of the
pages, not a verification.

### 3.1 Value-changing (counts, offsets, addresses, constants, formulas, behaviour) — page-text only - needs local check

**C-V1. Does the unit's height count in the trigger radius?**
- Side A, `walking-into-an-authored-trigger-point.md:54-57`: "**The authored point has no height.** The third component
  is written **zero** (`002F81C1`, … while the unit's own position is real in all three. **The unit's height therefore
  counts against the 1.3 budget directly**".
  - The same page at `:140-141`: "the zero height of the authored point counts against it linearly".
  - The contract's own §12 at `CONTRACT-authored-trigger-points.md:174-175`, unstruck: "Place it at the point's
    coordinates but a height away and assert the height is charged against the same budget (TP-2)."
- Side B, `CONTRACT-authored-trigger-points.md:79-86`: "~~The authored point has NO HEIGHT …~~ BOTH HEIGHTS ARE ZEROED,
  so the radius is horizontal. *(Corrected 2026-09-25, FABLE, …, on OPUS block 317, which executed it; bytes re-read.)*
  … `002F8150 mov [rsp+0x54], edi` overwrites the height … **Height does not count at all.**" Falsification P2 (`:279`)
  agrees.
- **Favoured: side B** (dated correction 2026-09-25). Page-text only - needs local check.

**C-V2. The trigger threshold.**
- Side A, `walking-into-an-authored-trigger-point.md:51-52`: "The threshold is **1.3**."
- Side B, `CONTRACT-authored-trigger-points.md:69-71`: "the threshold is the float NEAREST 1.3 … against `xmm7` =
  **`1.2999999523162842`**, the `f32` at `00901B34`". The 2026-09-25 correction (`:74-77`) restates it: "The original
  fires only for `d ≤ 1.2999999523`."
- **Favoured: side B** (dated correction 2026-09-25, which restates the constant). Page-text only - needs local check.

**C-V3. "Once, ever" versus a three-field ring.**
- Side A:
  - `walking-into-an-authored-trigger-point.md:35-36`: "Walk close enough to one and it fires — once, ever."
  - The same page at `:99-101`: "**The live set is a 32-bit mask stored per field** in a 12-byte-stride table at
    `0x2EC3EA0`, found by scanning for the current field id. **Clearing the bit is what makes the trigger once-only**".
  - Unstruck in the contract: `CONTRACT-authored-trigger-points.md:146-147`, "A point transitions `live → spent` exactly
    once and never back."; and `:168`, "makes something happen once and never again".
- Side B, `CONTRACT-authored-trigger-points.md:97-101`: "**The "once-ever" is bounded by a ring** *(Corrected
  2026-09-25 …)*. The field's live mask is held in a **three-slot ring** at `02EC3EA0` … So a cleared bit is remembered
  for the three most recently fired-in fields, until that clear." The `.tsv` route "stride=0xC count=3" fits side B.
- **Favoured: side B** (dated correction 2026-09-25). Page-text only - needs local check.

**C-V4. What `00377700` returns when there is no table.**
- Side A, `Field-Record-Table/field-record-table-navimapdata.md`:
  - `:127-130`: "**fails to a fixed default record** … the *restrictive* value for every flag."
  - `:683-685`: "**It fails closed.** An absent table or an out-of-range field id yields record `0x0FFF` / third byte
    `0`: no navigation map, and every flag clear — the restrictive answer."
  - `:306`: "/* the fail-closed default record */"
- Side B:
  - `CONTRACT-field-record-accessors.md:245`: "| `00377700` | `xor dl, dl`, then **its own** `not` / `test al,1` |
    **1**, unless the save vetoes — **CORRECTED 2026-09-11** |"
  - `CONTRACT-field-record-accessors.md:264`: "**A missing table is therefore the most PERMISSIVE input to this
    accessor, not the least.**"
  - The navimapdata page's own `:531-533`: "its failure default is bit 0 *clear* — the permissive value"
- **Favoured: side B** (dated correction 2026-09-11, by execution). Page-text only - needs local check.

**C-V5. Which bits of the third byte `00377C70` takes.**
- Side A, `CONTRACT-field-record-accessors.md:65`: "| | **bits 4–7** | `00377C70` | `shr 4` |". Also `:69`: "**Bits 1–3
  of the byte are the only part no accessor touches.**"
- Side B:
  - `CONTRACT-field-record-accessors.md:51`: "byte 2, bits 4–6"
  - `CONTRACT-field-record-accessors.md:425-426`: "**Bit 7 of that byte is also dead** — `00377C70` does `shr 4` then
    `and 7`, so it takes three bits, not four."
  - `Field-Record-Table/field-record-table-navimapdata.md:294-295`, `:324`
- **No favoured side.** The execution note at `:423-426` supports side B, but it is not a dated correction of `:65`.
  Page-text only - needs local check.

**C-V6. When the field record table is loaded.**
- Side A:
  - `Field-Record-Table/field-record-table-navimapdata.md:629-633`: "area load / transition / -> 00377CC0
    WorldAreaField_BootMapTables / -> 00378540 … request (9, 8) navimapdata.bin"
  - `Field-Record-Table/field-record-bit15-action-permission.md:149-150`: "area load / transition / -> field record
    table bound (DAT_02add100)"
  - The same page at `:162`: "the field record table bound at area load"
- Side B:
  - `Field-Record-Table/field-record-table-navimapdata.md:73`: "`00378540` is the World/Area/Field boot-time
    registration routine"
  - The same page at `:681-682`: "the file is published once per boot into `02ADD100` and read directly thereafter."
- **No favoured side.** It decides whether the null window (S-4, G-5) recurs on every area change. Page-text only -
  needs local check.

**C-V7. The `0x80000003` mask-site census does not add up.**
- `Field-Record-Table/field-record-table-navimapdata.md:149`: "In **117 of the 173 instructions** in the image that test
  the constant `0x80000003`"
- `:660`: "55 of the 173 mask sites have no escape call at all."
- `:936`: "Re-run at ±8 instructions: 116 PAIRED, 55 NO-ESCAPE. At ±25: 117 / 55."
- 117 + 55 = 172 and 116 + 55 = 171; neither total is 173. **No favoured side.** Page-text only - needs local check.

**C-V8. Who calls `00377C20`, and how many.**
- Side A:
  - `Field-Record-Table/field-record-bit15-action-permission.md:109`: "**65 direct callers**, **110 including the
    thunk**"
  - The same page at `:227`: "65 distinct callers across 13 subsystems"
  - The same page at `:279-280`: "**called both ways** | **2**" / "**union** | **110** | **15**"
  - The same page at `:315`: "**65 direct callers** — matches exactly."
  - `Field-Record-Table/field-record-table-navimapdata.md:134`: "65 direct callers + 47 through thunk `00313F60`"
  - The same page at `:519`: "110 functions, 15 subsystems"
  - `README.md:27`: "65 callers across 13 subsystems, 17 in CombatAction"
- Side B: `CONTRACT-field-record-accessors.md:122-130`, "**RE-DERIVED 2026-09-11, and the old numbers did not
  survive.** ~~`00377C20` has 65 direct callers plus 47 through the thunk.~~ … | `00377C20` bit 15 | **79** | **66** |
  … the 65 does not match either column".
- Side C, the same contract's pass 1 (2026-09-12), `CONTRACT-field-record-accessors.md:477-480`: "**110 distinct
  functions across 16 subsystems reach it** … 65 directly and 47 through the 5-byte thunk `00313F60`. (§6's own census
  counts *call sites* and gets 79/66 and 67/47 … and three functions use both routes.)"
- Direct callers are 65 or 66, functions using both routes 2 or 3, and subsystems 13, 15 or 16.
- **No favoured side.** The 2026-09-11 strike is followed by a 2026-09-12 restatement of 65. Page-text only - needs
  local check.

**C-V9. When the weather resolver draws the RNG.**
- Side A, `Weather/weather-probability-and-transition-roll.md:61-63`, unstruck: "picks the single eligible one directly,
  and draws MT19937 only when two remain."
- Side B:
  - The same page at `:377-383` (2026-09-21, `CON-147`): "The **only** call to `00379CD0` in the 253-byte body is at
    `0025ABB8`, inside the arm taken when the current slot is **2** — and it is taken *before* any probability is read.
    … **Both are deterministic, and slot 2 always wins when eligible**"
  - `CONTRACT-weather.md:297-308`, with the draw-count table at `:360-369`
- **Favoured: side B** (dated 2026-09-21 correction). Draw counts change every later gameplay roll on the shared stream
  (`CONTRACT-weather.md:571`). Page-text only - needs local check.

**C-V10. Probability 0: "always re-roll" or "pinned".**
- Side A, `Weather/weather-probability-and-transition-roll.md`:
  - `:37`: "some always re-roll (probability 0)"
  - `:48`: "probability **0** → current slot cannot be retained → pick an alternate"
- Side B:
  - The same page at `:385-389` (2026-09-21): "**And every arm falls back to the current slot.** … So
    `weatherProbability = {0, 0, 0}` **pins the weather permanently** — the opposite of what "probability 0 → current
    slot cannot be retained" implies."
  - `CONTRACT-weather.md:172-179` (I-6, citation corrected 2026-09-29)
- **Favoured: side B** (dated 2026-09-21 correction). Page-text only - needs local check.

**C-V11. What the field-init latch skips.**
- Side A, `Weather/weather-probability-and-transition-roll.md`:
  - `:70`: "if already set, the whole weather/resource initialization core is skipped"
  - F-2 at `:173`: "skips its whole body if `byte [rcx + 0x10] & 4`"
- Side B:
  - The same page at `:391-397` (2026-09-21, `CON-148`): "`002620E0`'s init-bit test at `002620F3` jumps to
    `002621A8`, **not** to the return. `002621A8` runs `003601C0(0x0B)` and tail-jumps `003601C0(0x0C)`"
  - `CONTRACT-weather.md:135-139` (P-2)
- **Favoured: side B** (dated 2026-09-21 correction). Page-text only - needs local check.

**C-V12. The domain of `02099DA8`.**
- Side A, `Weather/weather-apply-and-environment-materialization.md:119`, unstruck: "`02099DA8         u32  global
  environment class 0..3`"
- Side B:
  - The same page at `:524-534` (2026-09-21, `CON-146`): "**The authored domain is `0..4`.** … **So `02099DA8` = 4 for
    246 of 279 lanes**"
  - `CONTRACT-weather.md:345`, `:560-561`
- **Favoured: side B** (dated 2026-09-21 correction). Page-text only - needs local check.

**C-V13. What the `+0x1061` gate does to a second apply.**
- Side A, `CONTRACT-field-environment-variant.md:84-88`: "**EV-3 — The selector is latched, and the latch is
  FIRST-WRITER-WINS and released on exit.** … *So the selector written by whoever got there first is consumed exactly
  once per pass, and a second caller within the same pass publishes the first caller's choice.*"
  - The same contract's `:149`: "A latch already held means this call publishes someone else's selector (EV-3)."
  - Its reproduction formula, `:159-160`: "Call twice within one pass with different counts and assert the second
    publishes the **first's** selector (EV-3)."
  - `choosing-the-field-environment-variant.md:79`: "; a latch: first writer wins".
- Side B, `CONTRACT-weather.md:79`: "`bInitializationRestoreState` | `u8` | world-transition policy; gates the commit and
  is consumed by it | tested `0026D951`, cleared `0026DA92`, set `0026D8F9`". `0026D8F9` is inside the arm-restore
  `0026D8F0`, not inside `0026D910`.
  - I-3 at `CONTRACT-weather.md:151-155`: "When `payload[0x1061] != 0` the requested slot is thrown away … The flag is then
    cleared at `0026DA92` … so it is consumed exactly once per apply".
  - The setters listed elsewhere are `0026D8F0` (the `setweatherslot` arm) and `00268320`. `00280140` clears it
    (`Weather/weather-apply-and-environment-materialization.md:156-160`;
    `Weather/weather-slot-state-model.md:51-53`, `:69-70`).
- Side B names no writer inside `0026D910` that sets the flag. Side A's "a second caller … publishes the first caller's
  choice" needs the flag held between the two calls.
- **No favoured side.** Page-text only - needs local check.

**C-V14. Who calls `0026D910`.**
- Side A, `Weather/weather-apply-and-environment-materialization.md:65-72`: "Only **four** direct control-flow entries
  exist in the whole executable" — `0025ACA0` (tail jump), `00266E74`, `00266E7B`, `003565C0`. Fits
  `CONTRACT-weather.md:67` ("`0025ACA0` likewise tail-jumps into it at `0025AD06`") and
  `choosing-the-field-environment-variant.md:169-171`.
- Side B, D-3 (2026-09-12), on two pages: `Weather/weather-slot-state-model.md:138` and
  `Weather/weather-apply-and-environment-materialization.md:165`. "`WorldField_InitializeCurrentFieldRuntimeParameters`
  (`0026D910`) has exactly three call sites: the script verb **`setweatherslot`** … and two back-to-back native calls
  with argument 1 at `00266E74` / `00266E7B` … So at runtime every weather apply comes through the VM verb".
- Side C, F-2 (2026-09-16), `Weather/weather-probability-and-transition-roll.md:173`: "`0026D910` has **three** direct
  callers: the roll `0025ACA0`, one CoreRuntimeScheduling path, and **`003565C0`**".
- Side B's "every weather apply comes through the VM verb" omits the field-entry roll that side A and side C both
  include.
- **No favoured side.** Page-text only - needs local check.

**C-V15. What `0209A6E8` is.**
- Side A, `Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md:274-279` (UQ-88, answered 2026-09-14): "it
  is **the Weather Slot cached for the resource rebuild**, 1-based … slots 1, 2 and 3 select bits **24, 25 and 26** of
  each entry's flags dword."
- Side B, `Map-Pack/the-map-ctrl-pack.md:592-595` (§2.2, decoded 2026-09-20): "**the flag dword's bits 24–31 (the byte
  at `+0x0F`) are a per-bank presence mask** (`0209A6E8` = the active bank, so bank *n* = bit *n*+0x17; the census
  `+0x0E` values `0x8000`/ `0x8700`/`0x9700` decode as banks {14} / {7,8,9,14} / {7,8,9,11,14})".
  - Also `:606`: "**the active-bank working set**"; `:608`: "`002F7380` is the bank-change reselection".
  - Side B's own formula does not give its own decode. `0x8700` in the `u16` at `+0x0E` sets dword bits 24, 25, 26 and
    31, which "bit *n*+0x17" maps to *n* = 1, 2, 3, 8, not {7, 8, 9, 14}.
- **No favoured side.** Neither text corrects the other, and side B is the later one. Page-text only - needs local check.

**C-V16. The `00466220` type filter.**
- Side A, `Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md:317`: "passes only when `byte[rec] ∈ {0x14,
  0x1C, 0x24, 0x2C}` … and returns 1 for `{0x14, 0x24, 0x2C}`, 0 for `0x1C`"
- Side B, `Map-Pack/the-map-ctrl-pack.md:604-605`: "a type filter `00466220` (`byte[entry]` ∈ `{0x14,0x1C}`)"
- **No favoured side.** Page-text only - needs local check.

**C-V17. Is the `+0x218` slot table zeroed?**
- Side A, `Map-Pack/the-map-ctrl-pack.md:605-606`: "The survivors (`ctx+0x228` count) get a `count×0x28` zeroed table at
  `ctx+0x218`"
- Side B, `Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md:231-237`: "**Correction, 2026-09-15 (OPUS)**,
  … This sentence said *“zeroed on creation”* … **Neither is true of the whole entry.** … `+0x21`..`+0x27` are
  uninitialised allocator memory for the life of the table"
- **Favoured: side B** (dated correction 2026-09-15). Page-text only - needs local check.

**C-V18. The pass-1 increment in `002F7380`.**
- Side A, `Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md:204-205`, unstruck in the sentence:
  "`00466220(rec)` is a predicate selecting an increment of either `i+1` or `4`"
- Side B, the inline note on the same line: "*(Corrected 2026-09-14 (FABLE): the increment is **1**, not `i+1`.*"
  - The same page at `:300`: "the sum of 1 per 4-bit-indexed record and 4 per other record"
- **Favoured: side B** (dated correction 2026-09-14). Page-text only - needs local check.

**C-V19. What `0026FAD0` does, and what its third argument is.**
- Side A:
  - `Weather/weather-probability-and-transition-roll.md:157-164`: "`0026FAD0(channel, value, manager)` is the effect
    registry's instantiate call … looks up the kind-2 record `{2, channel, manager}` (`0024F680`), allocates one if
    absent, and runs `0026F470` over the EFB's **binding table** … instantiating every row whose channel byte `+4`
    equals `channel` … and whose enable byte at **`+7 + value`** is set"
  - `CONTRACT-weather.md:257-258`: "`0026FAD0(0, committedSlot+1, managerIndex)`"
- Side B:
  - `Map-Pack/the-map-ctrl-pack.md:175-180`: "`0026FAD0(idx, value, mode)` — gated on `byte[02F8F238]` — probes
    `0024F680` and, finding nothing pending, posts a type-2 message `{u16 idx; u16 mode}` through `0026F470` … then
    marks `flags[idx] |= 8` and `|= 4` when bit0 clear."
  - The same page at `:186`: "the alternator ops call `0026FAD0` with `mode = s8[+0x15]`"
- The third argument is a manager index on one side and a mode / group on the other. The operation is "instantiate
  binding rows" on one side and "post a message and set flag bits" on the other.
- **No favoured side.** Page-text only - needs local check.

**C-V20. `map_ref.bin` row `+0x04`.**
- Side A, `CONTRACT-weather.md:106`: "`+0x04  s32  (not read by weather)`"
- Side B:
  - `choosing-the-field-environment-variant.md:24`: "`{u16, i16, u16 area, u16 group}`"
  - The same page at `:120`: "the area index `MapRef_GetAreaArdFieldResourceIndex` returns (`00264EF9`)" (row word `+4`)
  - `Field-Record-Table/field-record-table-navimapdata.md:1142`: "`word[slot+6]` is the answer"
  - `Map-Pack/the-map-ctrl-pack.md:1283`: "`{u16 own pack index, i16 block index, i16, i16}`"
- `map-ref-field-row-accesses.tsv` shows 16-bit loads at `+4` (`00264EF9`) and `+6` (`00264FB9`, `0026DBB2`, `0026DBE7`).
  That fits side B as a layout.
- Signedness also differs on side B: `u16` versus `i16`.
- **No favoured side.** Page-text only - needs local check.

**C-V21. Can the image-address base `01F83530` be written?**
- Side A, `Map-Pack/the-map-ctrl-pack.md:901-904`: "it is zero-initialised `.data` that no instruction in the image
  writes — the static route to a writer is exhausted … so the decode is zero-extension for the process life"
- Side B, `Field-Record-Table/field-record-table-navimapdata.md:725`: "*(Scope corrected 2026-09-25, FABLE, …: `01F83530`
  is **zero at image load** … one in-image store route can. The texture-id table writer `00210570` … so id `0xFFFB`
  stores a pointer into `01F83530`. … the route is **undriven, not absent**. "Zero for the process's life" is
  supported, not proven."
- **Favoured: side B** (dated correction 2026-09-25). Page-text only - needs local check.

**C-V22. Function sizes that disagree.**
- `Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md:332`: "`0026D910`
  (`WorldField_InitializeCurrentFieldRuntimeParameters`, ~44 B)". Against: "418 bytes"
  (`choosing-the-field-environment-variant.md:36`; `CONTRACT-field-environment-variant.md:47`; `CONTRACT-weather.md:64`).
- `Field-Record-Table/field-record-table-navimapdata.md:1111`: "`00378540` (~85 B)". Against: the same page's `:75` and
  `:213`, "943 bytes" / "943 B".
- `Field-Record-Table/field-record-table-navimapdata.md:1100`: "`00326500` (`PartyFocus_SelectAndRequestDefaultActor`,
  ~119 B)". Against: `:235`, "274 B".
- **No favoured side.** Page-text only - needs local check.

**C-V23. The MWeather bit base: which slot domain?**
- Side A:
  - `Weather/mweather-resource-format.md:50`, `:156`: "`9 * (3 * selector + weatherSlotIndex)`"
  - The same page at `:21`, `:208-209`: "bit base `9 × (3 × selector + slot)`, `width` bits read most-significant
    first". This is the rule the D-7 corpus decode used.
  - `choosing-the-field-environment-variant.md:135`: "whose bit base is `9 × (3 × selector + slot)`", with the caller
    passing `selector+1`.
- Side B, `CONTRACT-weather.md:157-164` (I-4): "**That `-10` is a `-9` for the slot bias and a `-1` for the MSB-first
  walk**: the effective entry index is `3*selector + slot - 1` … not the one a literal `3*selector + slot` would need."
  - The file-size argument is at `:599`.
- With the authored slot `1..3`, side A read literally is off by one entry.
- **No favoured side.** Side B is not a dated correction of side A. Page-text only - needs local check.

**C-V24. The signedness of `+0x1060`.**
- Side A, `Weather/weather-probability-and-transition-roll.md:248`: "`+0x1060   u8   field runtime parameter`"
- Side B: `Weather/weather-slot-state-model.md:77`, "`+0x1060  s8   currentWeatherSlot`"; `CONTRACT-weather.md:78`
  (`s8`), `:440` ("`(int8)payload[0x1060]`"); `Weather/weather-apply-and-environment-materialization.md:436`
  ("`sign-extended byte [rax+0x1060] + 1`").
- **No favoured side.** It matters only for out-of-domain bytes. Page-text only - needs local check.

**C-V25. Does `02099DA8` have a reader?**
- Side A, `CONTRACT-weather.md:553`, the evidence row, unstruck: "sibling `02099DA8` identical (one store, `0026DA26`)".
  In context this means one accessor total, no reader.
- Side B:
  - The same contract's `:518-523`: "*Corrected 2026-09-30 …: `02099DA8` is not the same shape. It has a reader, the
    7-byte getter `00263E10`*"
  - `CONTRACT-weather.md:217`
- **Favoured: side B** (dated correction 2026-09-30). Page-text only - needs local check.

**C-V26. Tag-30 flag bit 30 and the tag-24 entry `+0xC0`: who writes it, and what it means.**
- Side A, `Map-Pack/the-map-ctrl-pack.md`:
  - `:535`: "bit 30 = has tag-24 link"
  - `:537-540`: "writes `-1` to `entry+0xC0` — a deferred-alloc marker; a later pass (`002F71F0`) allocates"
  - `:741-743`: "`qword[entry+0xC0]` is a **byte-bitmap pointer** (the `-1` expansion write is its unset sentinel)"
- Side B, the same page:
  - `:1181`: "**the per-instance presentation-entry array** (the periodic tick's post-recovery mark writes `+0xC0` of
    entry `[+8]`)"
  - `:1200-1202`: "honoring the bit-30 post-recovery mark by writing `-1` into the unit's `0xE0` presentation entry
    `+0xC0` (`002F701D`–`002F7037` — the periodic-tick contract)"
- Side B adds a second writer, the status layer's periodic tick, and gives the bit another meaning.
- **No favoured side.** Page-text only - needs local check.

**C-V27. The argument `002620E0` passes to `00379860`.**
- Side A:
  - `Weather/weather-probability-and-transition-roll.md:129`: "`00379860(weatherSlot)`"
  - The same page at `:319-321`: "The three `0026FAD0` posts each take `0017D490()` when positive else
    `byte[002EF2B0()+0x1060]+1` … against channels `0`, `0x1F`, and the arg to `00379860`". That is the debug override
    when positive.
- Side B, `CONTRACT-weather.md:259`: "`00379860(committedSlot+1)`", with no override.
- **No favoured side.** It differs only while the debug override is positive. Page-text only - needs local check.

**C-V28. The `00377BA0` "mask".**
- Side A, `CONTRACT-field-record-accessors.md:578-580`: "`byte[rcx+rax+9]` and `byte[rcx+rax+8]` are the compared kind
  bytes (`00377BD4`/`00377BDD`), and the value is masked to `0xFFF` (`00377BF4`) — matching the documented `shr 0xC /
  and 3` two-bit read."
- Side B, the same contract's `:61`: "**bits 12–13** | `00377BA0` | `shr 0xC` / `and 3`". Its `:243`: "`00377BA0` |
  `(0xFFF >> 12) & 3` | **0**", where `0xFFF` is the failure constant.
- Read literally, a mask to `0xFFF` before `shr 0xC` always yields 0. "Compared kind bytes" are the two bytes of the
  `u16`.
- **No favoured side.** Side A is probably a description of the failure-path constant, but no page says so. Page-text
  only - needs local check.

### 3.2 Stale "not read / open" claims, struck-but-repeated text, and banner disagreements

These do not change a value; a re-implementer would only be misled about what is known.

| id | stale or banner text | answered or contradicted by |
|---|---|---|
| C-S1 | `README.md:37-41`: "### Not yet documented / - MapRef root and auxiliary data layout / - Field runtime parameter derivation (`002E3D40` zero-mode path) / - The field environment table and target-local environment index resolution" | `map_ref.bin` decoded: `choosing-the-field-environment-variant.md:85-91`, `:107-128` (2026-09-13 / 09-29); `CONTRACT-weather.md:87-117`. `002E3D40` read 2026-09-18 (`choosing-the-field-environment-variant.md:141`); `Weather/mweather-resource-format.md:316-343` |
| C-S2 | The README index lists only `field-record-bit15-action-permission.md` under `Field-Record-Table/` and none of the four contracts or the two root pages (`README.md:14-35`); it calls Weather and the record table "**documented**" (`:16`, `:24`) | `Field-Record-Table/field-record-table-navimapdata.md:4` and `Field-Record-Table/field-record-bit15-action-permission.md:4` say `status: AUDITED`; the contracts exist (`CONTRACT-*.md`) |
| C-S3 | `README.md:55-57`: "`002E3D40(mode, a, b, c)` is the engine's **map wind** entry point" | `choosing-the-field-environment-variant.md:141` and `CONTRACT-field-environment-variant.md:130`, `:195`: "the **weather-to-presentation refresh**". Same function, two names; `Weather/mweather-resource-format.md:223-226` (D-9, 2026-09-26) supports "wind" for the basis it builds. |
| C-S4 | `walking-into-an-authored-trigger-point.md:30`: "`BattleUnit_TryTriggerNearbyAuthoredFieldActivation`" | the same page `:153` and `CONTRACT-authored-trigger-points.md:49`: "`BattleUnit_TryTriggerNearbyAuthoredFieldAction`" |
| C-S5 | `walking-into-an-authored-trigger-point.md:116-118`: "**Two unrelated systems excluding the same band of kinds is a fact about the band, and neither function says what it is.**"; `:130-132`: does not claim "what the excluded kind band `0x1B … 0x27` contains" | `CONTRACT-authored-trigger-points.md:185-191`: "**CLOSED 2026-09-23 (SWE2-CONTRACT): the thirteen Espers.**" |
| C-S6 | `CONTRACT-authored-trigger-points.md:180`: "**None.** No experiment executes this body." | the same contract `:74`, `:80`, `:97`: "on OPUS block 317, which executed it"; `:83`: "OPUS measured it"; `:273`: "TP-4's ring behaviour is OPUS block 317's execution" |
| C-S7 | `CONTRACT-authored-trigger-points.md:33-34`: "the environment variant remains uncontracted and this document does not claim it"; `:139`: "**Uncontracted** \| the field environment variant"; `:201`: "The field environment variant, S-11's other uncontracted page." | `CONTRACT-field-environment-variant.md:30-32`: "**this takes the environment variant**, so all three of S-11's pages now have a contract" (`readiness: CONTRACT READY`, `:6`) |
| C-S8 | `CONTRACT-authored-trigger-points.md:247`: "**CombatAction — OWNER.** The body is that layer's by primary owner." | the same contract `:222`: "**WorldAreaField — internal.** The body is this category's own."; `walking-into-an-authored-trigger-point.md:5`: `owner_layer: PrimaryOwner:WorldAreaField` |
| C-S9 | `walking-into-an-authored-trigger-point.md:18`: `last_reviewed: 2026-09-03`, `status: AUDITED` (`:4`) | its TP-2 and once-only text was overturned on the contract on 2026-09-25 (C-V1, C-V3) and is unstruck on the page |
| C-S10 | `CONTRACT-field-environment-variant.md:76-79`: "The variant page records this as the **fourth** distinct way this executable's decompiled output has misdescribed a function boundary" | `choosing-the-field-environment-variant.md:68-71`: struck, "*(Struck 2026-09-30, SWE2-DATA: the three earlier cases are not cited, so the count has no anchor.…)*" |
| C-S11 | `CONTRACT-field-environment-variant.md:173`: "What the five globals feed — published here, consumed elsewhere." and `:174`: "What the three variants mean to a player; three states exist and nothing names them." (unstruck §14) | `choosing-the-field-environment-variant.md:132-133` and `:136-137`, both "*Answered by reconciliation 2026-09-30*"; the count "five" is itself corrected to four at `choosing-the-field-environment-variant.md:40`, `:75`, while `CONTRACT-field-environment-variant.md:243` reconciles "five" as "the four plus the selector" and `CONTRACT-weather.md:73` still says "five published globals" |
| C-S12 | `CONTRACT-field-environment-variant.md:198-199`: "**whether any of it reaches the save image is not established here**" | `choosing-the-field-environment-variant.md:137`, `:149`: "the choice survives save and load"; `CONTRACT-weather.md:421`; the same contract's `:217` (the selector lives in the persistent payload) |
| C-S13 | `CONTRACT-field-environment-variant.md:40-41`: "publish the result for the presentation side to read" | `choosing-the-field-environment-variant.md:147-148`: "The combat side follows it through `02099DAC`, the weather class the damage formula reads" |
| C-S14 | `CONTRACT-field-record-accessors.md:17`: `last_reviewed: 2026-09-11` | dated additions on the same page 2026-09-12 (`:75-88`, `:457`) and 2026-09-25 (`:107`, `:111`, `:219`) |
| C-S15 | `CONTRACT-field-record-accessors.md:420-422`: "The four bytes at the table's `+0x00`, left undeclared … **Still open**" | `Field-Record-Table/field-record-table-navimapdata.md:279`: "`+0x00  u32   magic          'N''A''V' 0x02`"; `:334-335` (fence, 2026-09-10); the contract itself at `:225`: "magic `NAV\x02`" |
| C-S16 | `CONTRACT-field-record-accessors.md:410-411`: "What the bit regions mean. The referenced page carries what is known; this contract deliberately adds nothing to it." | the same contract `:75-88`: "**The semantics arrived, and they are cited here**" (2026-09-12) |
| C-S17 | `Field-Record-Table/field-record-table-navimapdata.md:21`: `last_reviewed: 2026-09-08`; `:27` `last_pass: 2026-09-02` | dated edits on the page to 2026-09-26 (`:438`) and 2026-09-27 (`:770`) |
| C-S18 | `Field-Record-Table/field-record-table-navimapdata.md:74-76`: "**Three were read here; two more were found on 2026-09-08** … so five is a floor"; `:111-112`: "**the string keys were not read**"; `:213`: "requests all three map tables"; the call chain `:631-633` shows three tables | the same page `:86-96` (2026-09-14): "`00378540` installs **seven** publishers … the string keys for the two previously unread rows are now decoded" |
| C-S19 | `Field-Record-Table/field-record-table-navimapdata.md:517`: "The `AiOrder_EvaluateTargetSelector` use is **not** examined, so **PROPOSED-repos2d-2 stays open**"; `:716-718`: "**The `AiOrder_EvaluateTargetSelector` consumer is still unread, so this box stays unticked.**" | the same page `:568` (2026-09-12): "one selector predicate compares the raw value with its operand (`00303043`–`0030304D`…)"; the box at `:708-710` is ticked "**C-11 ANSWERED**" |
| C-S20 | `Field-Record-Table/field-record-table-navimapdata.md:1023-1026`: "**What the toggle is remains unnamed** — that is 15-Input's to close"; `Field-Record-Table/field-record-bit15-action-permission.md:204-205`: "what the toggle *is* remains open and belongs to 15-Input" | `Field-Record-Table/field-record-table-navimapdata.md:759-765` (2026-09-12): "`020927E0` is the **R2 force-fight toggle**"; the bit-15 page's own marker on the same bullet, `:203`: "C-12 is ANSWERED" (2026-09-30) |
| C-S21 | `Field-Record-Table/field-record-table-navimapdata.md:959`: "`audit_crossrefs.py` has not yet been run against this document — `crossref_clean: false`." | the same page `:29`: `crossref_clean: true`; `:1062-1063`: "Both documents in the folder are now `crossref_clean: true`" |
| C-S22 | Status 31 is "**Vanished**" in `Field-Record-Table/field-record-table-navimapdata.md:186`, `:472` and `Field-Record-Table/field-record-bit15-action-permission.md:189` | `Field-Record-Table/field-record-table-navimapdata.md:449` (2026-09-26): "bank 5's entries decode to the status names: 0 KO, 3 Stop, 6 Doom, 31 X-Zone"; `:730`: "Status 31 is *X-Zone* in the name bank" |
| C-S23 | `Field-Record-Table/field-record-bit15-action-permission.md:81`: "Both effect layers are OR'd"; `:76` `statusLayer0 \| statusLayer1` | the same page `:211-217` (2026-09-02): "There are in fact **three** 32-bit status masks … They are also a different structure from the 128-bit effect layers" |
| C-S24 | `Field-Record-Table/field-record-bit15-action-permission.md:18`: `last_reviewed: 2026-09-02` | its marker normalisation 2026-09-30 (`:203`) and relabel 2026-09-27 (`:209`) |
| C-S25 | `Weather/weather-slot-state-model.md:301`: "`02099DBC` is cleared first and nothing here reads it back; what it means is not established." | `CONTRACT-weather.md:98`, `:246-248`: the `+0x18` boolean table, second writer `0026AB40`, reader `00264D50` (`:220`) |
| C-S26 | `Weather/weather-slot-state-model.md:341-343`: `002FA230` is "the twin reset to `002FA260`'s `02BE3E60` block, same shape, different slot array", filed as "the fixed-shape reset the slot model applies on reinit" | `CONTRACT-authored-trigger-points.md:100`: "`002FA230` clears the ring" — the trigger points' live-set ring at `02EC3EA0`, not weather state |
| C-S27 | `Weather/weather-apply-and-environment-materialization.md:434-437`: "`0017D490()` answers the pending-state count … the stored mode plus one, the "next state" convention" | `Weather/weather-slot-state-model.md:67`: "`0017D490` \| `WorldField_GetDebugWeatherSlotOverride` \| 20 B \| returns `[debugSingleton+0xAAC]`"; `CONTRACT-weather.md:80` |
| C-S28 | `0026D910` is named "`WorldField_ApplyWeatherSlotAndDerivedEnvironmentState`" on `Weather/weather-slot-state-model.md:71`, `Weather/weather-probability-and-transition-roll.md:87`, `Weather/weather-apply-and-environment-materialization.md:106` | "`WorldField_InitializeCurrentFieldRuntimeParameters`" on `choosing-the-field-environment-variant.md:36`, `CONTRACT-field-environment-variant.md:47`, `CONTRACT-weather.md:706`; the equivalence is recorded at `Weather/weather-probability-and-transition-roll.md:213-231` |
| C-S29 | `Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md:56-57`: "publish to notification channel 0" / "publish to notification channel 0x1F" | `Weather/weather-probability-and-transition-roll.md:156-157` (2026-09-12): "**they are EFB binding channels, not notification channels.**" |
| C-S30 | `Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md:263-267`: "**Two of the forty bytes are read.** `+0x00` is cleared and `+0x20` is set to `0xFF`" (writes, called reads); `:323-324`: "UQ-89 (the `0x28`-byte selected-record entries' content) stays open" | the same page `:280-296`: "**UQ-89.** … **ANSWERED 2026-09-26 …: only their initial and per-frame reset values, because nothing reads them.**" |
| C-S31 | `Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md:254-256`: "All seven callees … are still unnamed `FUN_` in the ledger" | the same page `:303-320`: "all 6 members bound" |
| C-S32 | `Weather/*.md` and the call-chain page: `last_reviewed: 2026-09-02`, `status: DOCUMENTED` (`Weather/weather-slot-state-model.md:4`, `:20`; `Weather/weather-probability-and-transition-roll.md:4`, `:19`; `Weather/weather-apply-and-environment-materialization.md:4`, `:19`; `Weather/mweather-resource-format.md:4`, `:19`; `Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md:4`, `:19`) | dated corrections on those pages run to 2026-09-29 (`Weather/weather-probability-and-transition-roll.md:385`), and the contract for them is `BEHAVIORALLY UNDERSTOOD` (`CONTRACT-weather.md:6`) |
| C-S33 | `CONTRACT-weather.md:59`: "The subsystem has **four entry points**" | the same table `:64` lists six; front matter `:9` lists ten `entries`; `:68` sends the resolver to "(I-5)", which is the slot-bounds invariant — the resolver's is I-6 (`:172`) |
| C-S34 | `CONTRACT-weather.md:83-85`: "obtained **four separate times** inside one `0026D910` call (`0026D94C`, `0026D959`, `0026D96A`, `0026D9AF`, `0026DA83`; five call sites, four of them before the tail)" | `choosing-the-field-environment-variant.md:175`: "the payload getter    five times" |
| C-S35 | `CONTRACT-weather.md:230`: "`02099DB4` is read by five `cmp` sites" | the same line lists nine addresses (`0026324D` … `0026E012`) |
| C-S36 | `CONTRACT-weather.md:528`: "**F-1 — thread/frame requirements for calling `0026D910` safely.** Unchanged and still open."; `:578`: "**TIMING** and **INTEGRATION** — the frame phase and thread requirements are open (§14.4)" | the same contract `:390-394`: "*F-1 SUPERSEDED 2026-09-26 …*"; the same note on `Weather/weather-slot-state-model.md:139-144` and `Weather/weather-apply-and-environment-materialization.md:226-231` |
| C-S37 | `CONTRACT-weather.md:222-224`: "**`02099DB0` is published and never read.** … It is inert in the shipped build by both routes."; `Weather/weather-apply-and-environment-materialization.md:549`: "read by nothing" | `choosing-the-field-environment-variant.md:193` (2026-09-30): "~~is written and never read, so editing that byte has no effect in the shipped build.~~ is written, and no reader is found (GB-3)"; `CONTRACT-weather.md:241-244`, residual |
| C-S38 | `CONTRACT-weather.md:19`: `last_reviewed: 2026-09-21` | dated edits on the same page 2026-09-23 (`:511`), 2026-09-26 (`:390`), 2026-09-29 (`:175`), 2026-09-30 (`:518`) |
| C-S39 | `Weather/mweather-resource-format.md:233-242`: "***NARROWED, NOT ANSWERED, 2026-09-20 (OPUS)** … Naming it still needs `0040FF30`, the sole identified consumer, read" | the same box `:223-226`: "**ANSWERED 2026-09-26 …: it is the map's wind direction**" |
| C-S40 | `Weather/mweather-resource-format.md:282-284`: "**Width caveat:** … The widths 4 and 2 are inferred …, not read directly." | the same page `:369-382`: "**The field widths are read, not inferred — §9's caveat is closed**" |
| C-S41 | `Weather/mweather-resource-format.md:198-199`: `MapRef_BeginLoadResources` "requests at bootstrap as loader id 9, kinds 4 and 2" (for the one map-reference table) | `choosing-the-field-environment-variant.md:113-122` (2026-09-29): `(9, 2)` is `test_area_ref.bin`, "loaded and never read"; `map_ref.bin` is "kind 9 id 4" (`:85`) |
| C-S42 | `Weather/mweather-resource-format.md:414`: "`003777C0` (144 B) is the 3-bit weather preset body" | the same page `:141`: "packed bitfield reader … shared by all three extractors"; `:416`: `00377850` is the preset extractor |
| C-S43 | `Map-Pack/the-map-ctrl-pack.md:1275-1277`: "## 6. Falsification pass / Not yet run." | the same page `:1374`: "## 9. Falsification pass 1 — 2026-09-13 (OPUS)"; front matter `:24-26` |
| C-S44 | `Map-Pack/the-map-ctrl-pack.md:570-571`: "`+0x20C`'s writer is outside `002F6AB0` (residue)." | the same page `:783-795`: "`ctx+0x20C` is now **closed — it was never a standalone field**" |
| C-S45 | `Map-Pack/the-map-ctrl-pack.md:477`: "`00466E70` (1453 B handler, unread)" | the same page `:1180` (it builds the `02EBB6E0` slot family) and `:1216`: "interior verified 2026-09-17, SWE2-FRONTIER" |
| C-S46 | `Map-Pack/the-map-ctrl-pack.md:20`: `last_reviewed: 2026-09-12`; `README.md:30`: "**documented 2026-09-12**" | dated edits on the page to 2026-10-01 (`:402`, `:1809`) |

---

## 4. Rating

**Overall: NOT YET.** The parts are uneven:

| part | rating | why |
|---|---|---|
| Field record table and its seven accessors | **READY** apart from G-5 | Contracted and executed against the shipped bodies: 426 cases, 0 mismatches (`CONTRACT-field-record-accessors.md:366-368`). The reproduction formula, failure constants and save gates are all stated (`:239-246`, `:321-347`). The two value disagreements, C-V4 and C-V5, go the contract's way on the page text. Open: when the table is loaded (C-V6 / G-5), which decides whether the permissive null window ever opens. |
| Weather: decide and commit (roll, resolver, probability, apply, MWeather read) | **MOSTLY** | `CONTRACT-weather.md:433-486` is a complete reproduction formula with real constants, draw counts and the multiply-high scaling. C-V9 to C-V12 are each settled by a dated correction, but the stale side is still printed on the roll and apply pages. Still open: the `+0x1061` gate's behaviour across two applies (C-V13), the caller set (C-V14), the MWeather slot domain (C-V23), the `+0x1060` signedness (C-V24), and the guards and published cells a port cannot name (G-12, G-13). |
| Weather: materialisation and presentation (`00180620` bank, `002E3D40` → `0040AAD0`, EFB posts, field-init fan-out) | **NOT YET** | **Structural gaps.** No page says how the slot selects the environment bank (G-8). The eight presets and the render PRNG are not described (G-9). The EFB binding operation is disputed (C-V19, G-11). Half the field-init core's callees are names only (G-10). The shader binding is unread (S-9). |
| Authored trigger points | **NOT YET** as a system; the per-call algorithm is READY | TP-1 to TP-7 with the 2026-09-25 corrections fully specify one call (`CONTRACT-authored-trigger-points.md:69-126`). But no page says where the point records come from or who calls the test (G-1). Two more readers of the live set are undescribed (G-2), and the hit's effect is unread (G-3, S-1). C-V1 to C-V3 are settled by dated corrections, but the walking page still states the overturned versions. |
| `map_ref.bin` | **MOSTLY** | Header, row and block offsets are known and censused (`CONTRACT-weather.md:87-117`, `:335-347`), but the three pages type the same bytes three ways (C-V20, G-6). |
| Map-control pack: request, split, dispatch, bind | **MOSTLY** | Loader arithmetic and slot routing are read in full (`Map-Pack/the-map-ctrl-pack.md:1070-1154`), but the order against the field-runtime pass is not stated (G-7). |
| Map-control pack sections | `ACTL`, `LGT2`, `SP1` **MOSTLY**; `YM00` **NOT YET**; `WD` / `MRP` dead data (nothing to port) | `ACTL`, `LGT2` and `SP1` are decoded to the record and state-machine level (§2.1, §2.3). `YM00`'s container is decoded, but tag 23, tag 12 / 32, tags 9 / 25, the `0x68` sub-records and the slot family are callee lists only (G-14). The tag-30 flag bit 30 and the `0209A6E8` mask are disputed (C-V26, C-V15). |
| LegacyPS2GS rebuild (`002F7380`) | **MOSTLY** | The mechanism and budget formula are stated (`Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md:184-241`, `:297-320`), and the output table is "read by nothing". The type filter and the mask-index meaning are disputed (C-V16, C-V15), and the 1-vs-4 factor is open (S-13). |

**To reach MOSTLY overall**, the database would need:
- a local check of the 16 value items with no favoured side, above all:
  - C-V13 (the `+0x1061` gate);
  - C-V14 (the callers of `0026D910`);
  - C-V15 (`0209A6E8`);
  - C-V19 (`0026FAD0`);
  - C-V20 (the `map_ref` row);
  - C-V23 (the MWeather slot domain);
  - C-V26 (tag-30 bit 30);
- striking the stale sides of the 12 settled items where they are still printed;
- the trigger points' data source and caller (G-1);
- the field-transition order across pack load, binding and the weather roll (G-7);
- the slot → environment-bank mapping (G-8);
- one joined `map_ref.bin` layout (G-6).
