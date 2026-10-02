# Reconstruction readiness — `FFXII TZA/03-World-Area-Field/`

| | |
|---|---|
| Stream | R (reconstruction readiness), per [`docs/cloud-briefs/re-readiness.md`](../../docs/cloud-briefs/re-readiness.md) |
| Board task | `OPUS-CLOUD-R-READINESS-03-1002` |
| Date | 2026-10-02 |
| Snapshot | this repo's text snapshot only (`df2c9f47`); no executable, Ghidra or live game was used |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every item is a quotation or a paraphrase of a page, with its location. |

**Counts:** _filled in when the report is complete (see the end of this header in the final commit)._

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
