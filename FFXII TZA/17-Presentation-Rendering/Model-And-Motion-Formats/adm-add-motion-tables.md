---
system: .adm — the add-motion per-bone tables named by add_motion_list.txt
category: 17-Presentation-Rendering
status: AUDITED
owner_layer: PrimaryOwner:Presentation
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 10 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
corpus_validated: "39 / 39 .adm in the archive index, all walked by the parser's own rules, 2026-09-13"
last_reviewed: 2026-09-13
archive_formats:
  - "adm"
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-adm-tables-pass-1 - all eleven corpus figures reproduced by re-walking the parser's rules over 39 files; NEW: +0x00=1, +0x01=0, +0x02=0 and an all-zero first group header mark THE SAME 35 tracks, every one track 0 of the 35 four-track files, all with recordCount 4
  crossref_clean: true
  reopened_count: 0
---

# `.adm` — the add-motion tables

> Small binary tables in `ps2data/add_motion/`, one per model stem named in `add_motion_list.txt`, some with a
> `_town` twin: tracks of groups of 28-byte per-bone records, parsed once at load and walked by the skeleton
> code while it composes a pose.

**Corpus validation.**

| | |
|---|---|
| files examined | **39 of 39** `.adm` |
| the parser's walk ends exactly at the file size | **39 / 39** |
| stems | `hc…` 30 files, `hn…` 7, `hs…` 2 |
| tracks per file | 4 in 35, 2 in 2, 1 in 2 |
| groups per track | 2 (90 tracks), 3 (22), 4 (34) |
| records per group | 4, 6, 8, 12, 13, 15, 17 or 18 |
| `add_motion_list.txt` | **23 names**; all 23 have `<name>.adm`, 15 (all `hc…`) also `<name>_town.adm` |
| shipped but never loaded | **`hn1018_12.adm`** (not in the list) |

Census: [`census.py`](../../_experiments/evidence/adm-add-motion/census.py) →
[`census.out.txt`](../../_experiments/evidence/adm-add-motion/census.out.txt) (ties sorted, two runs
byte-identical).

---

## 1. What the player sees

**Per-bone adjustments for 23 character models.** Each name in the list is a model resource stem
(`hc1004_02`, `hn1017_03`, `hs0003_01`, …); the skeleton code indexes the table's records by bone while
composing the model's final pose. What the adjustment looks like on screen~~, and what the `_town` twin changes,~~
is not established (§7) *(answered: see the `_town` answer near the end - the civilian-area variants of the same additive-pose tracks; 2026-10-02, OPUS)*.

## 2. The layout

The file is a flat stream; nothing is addressed by offset.

```struct AdmHeader base=file size=0x02
+0x00  i16       trackCount   4 in 35 files, 2 in 2, 1 in 2 (read movsx)
```

```struct AdmTrack base=record size=0x08
+0x00  u8        field00      0 in 111 tracks, 1 in 35   -> parsed track +0x06
+0x01  u8        field01      0 / 1 / 2 in 35 / 74 / 37  -> parsed track +0x07
+0x02  u16       field02      0 in 35; 26 distinct values 9..84 in the other 111 -> parsed track +0x00
+0x04  u16       groupCount   2, 3 or 4; used signed      -> parsed track +0x04
+0x06  u16       recordCount  per group; used signed      -> parsed track +0x02
```

Each track is followed by `groupCount` groups; each group is a 28-byte header followed by
`recordCount` 28-byte records.

```struct AdmGroup base=record size=0x1C
+0x00  byte[8]   field00      copied as one 8-byte piece; the 28-byte header is all zero in
                             46 of 382 groups, 35 of them the FIRST group of a track (§9)
+0x08  u32       field08
+0x0C  byte[8]   field0C      copied as one 8-byte piece
+0x14  u32       field14
+0x18  u32       field18      0 in 291 of 382 groups, 1 / 2 / 3 in 31 / 31 / 29
```

```struct AdmRecord base=record size=0x1C
+0x00  i32       bone         the bone index AddMotion_ApplyBonePose keys its tables by (00371711)
+0x04  byte[24]  values       copied as 8 / 4 / 8 / 4-byte pieces; the element types are not fixed by the code   <- corrected 2026-10-02, OPUS - the full disassembly below reads a record as {i32 bone; f32 eulerDeg[3]; f32 offset[3]}
```

The parser copies the 8-byte pieces with `movsd` and the 4-byte ones as dwords, so it fixes positions and widths
but not element types. Read as `f32`, the first three records' values are `(-179.719, 0.468, -15.674, 0.057,
-0.055, -0.033)`, `(-179.719, 0.468, -15.674, 0.057, -0.055, 0.033)` and `(-180.0, 0.0, 21.265, 0.057, -0.055,
-0.033)` — plausible numbers~~, which is a reading of the data and not a traced type~~ *(answered: see the full disassembly of `003714A0` below - `{i32 bone; f32 eulerDeg[3]; f32 offset[3]}`; 2026-10-02, OPUS)* (§7). The most common bone
indices are 6 and 7 (123 records each), 28 (94), 27 (79), 9 (77) and 29 (74).

## 3. The loader contract

**`AddMotion_LoadResources` (`001BDD20`)**, called once from `001BDC40` (`001BDC7F`), opens
`./PS2Data/add_motion/add_motion_list.txt` (`008F9628`, `001BDD97`), splits it on CRLF (`008F9654`,
`001BDE03`), and for every name:

1. opens `./PS2Data/add_motion/%s.adm` (`008F9658`, `001BDF9F`) and, if present, reads it whole, parses it
   (`AddMotion_ParseFile`, `001BE00F`), copies the name into the parsed record's `+0x00` and appends it;
2. opens `./PS2Data/add_motion/%s_town.adm` (`008F9678`, `001BE072`) and, if present, parses it and names
   it `"%s_town"` (`008F96A0`, `001BE0F6`).

A file absent from the list is never opened, so `hn1018_12.adm` is dead data.

**`AddMotion_ParseFile` (`001BE1A0`)** allocates a 32-byte record (`+0x14` track count, `+0x18` track array
of 16 bytes per track), then for each track a `0x28`-byte-per-group array (`+0x08`), and for each group a
record array of `recordCount × 0x1C` (`+0x20`), copying the file stream in order (`001BE260`–`001BE373`).

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| `trackCount` | `001BE1FB` (`movsx`) | — | none; the sign-extended count is multiplied with an unsigned `mul`, overflow saturating to all-ones by `cmovo` (`001BE210`–`001BE213`), and the result goes to the allocator and then to `memset` as the sign-extended count `<< 4` (`001BE21F`–`001BE231`) before the signed loop test (`001BE23D`); what the allocator `00210EC0` does with a saturated size is not read | — |
| track `groupCount`, `recordCount` | `001BE27B`, `001BE283`; used `movsx` at `001BE28B`, `001BE314` | — | none; the same `mul` / `cmovo` pattern | — |
| group and record bytes | copied `001BE2E0`–`001BE373` | — | — | — |
| the file length | — | **not checked** — the walk trusts the counts | — | — |
| record `bone` | `00371711`, `00371725` (`movsxd`) | — | **none** — used directly as an index into two tables sized from the skeleton (`[r13 + 0x88] × 4` bytes, filled with `0xFF` at `003716CC`); no bound against that count is taken in `003716E2`–`0037174C` | — |

**The consumers.** `AddMotion_LookupByModelName` (`001BE430`, one caller `00863110`) finds a model's record and
its `"%s_town"` twin by name. `AddMotion_ApplyBonePose` (`003714A0`, one caller `Skeleton_ComposeFinalPose`
`00373860` — interior read 2026-09-17, SWE2-FRONTIER: 1,170 B, `0020E600` ×7 + a `00202xxx` transform-helper band (`00202FE0`/`00202D70`/`00203170`), first call [`00373891`](../../_index/ADDRESS-INDEX.md)) walks the parsed tracks: for each track it takes **group 0's** record array - *corrected 2026-09-19 (FABLE): for a
track of kind 1 the group is the one whose id equals the value of a pose-sequencer slot, not group 0;
[the pose sequencer](the-pose-sequencer.md)* - and writes, per record,
`table1[record.bone] = trackIndex` and `table2[record.bone] = recordIndex` (`003716E2`–`0037174C`), then builds
rotations with `Matrix4x4f_BuildEulerRotation` (`00371D27`).

**Who binds a record to its tables (added 2026-09-19, FABLE; three bodies read whole).** The two handles the pose
applier chooses between sit on the character render record at `+0x6E8` and `+0x6F0`. They are stored by
`002EDF90(recordIndex, request, resourceId)` (179 B), a **five-state machine on the record's `+0x6C8`**:

| state | meaning | request 1 / 2 | request 0 |
|---:|---|---|---|
| 0 | unbound | becomes the state; **2 also runs the lookup** | - |
| 1 | base record of a pair | - | → 3 |
| 2 | the record that carries the binding | - | → 4 |
| 3 | 1, released | → 1 | - |
| 4 | 2, released | → 2, **no second lookup** | - |

The lookup is `00863110` (183 B): it turns the resource id into its file path, takes the base name between the
last backslash and the first dot, and hands it to the name lookup above, which fills the two handles - the
model's own record and its `_town` twin. The one caller is the element binder of the actor's secondary context
([the party read-in state machine](../../01-Script-VM-Native-Bridge/Party-Presentation-Verbs/the-party-read-in-state-machine.md),
the k-enum): its body-model **set** operation sends request 1 to the base element's record and request 2 to the
body-model element's record; its **clear** operation sends 0 to both. One other body reads the state, `002E7CE0`
(226 B): it applies a 16-bit value to the base record and, **only while that record is in state 1**, to the
body-model record too. *What that value is was not established.* Interior: `002EDFB5`, `002EDFCE`, `002EDFEA`,
`002EDFF9`, `002EE00C`, `002EE025`, `002EE038`; `00863137`, `00863144`, `0086315C`, `00863174`, `008631AD`;
`002E7D1B`, `002E7D55`, `002E7D5A`, `002E7D94`, `002E7DAD`.

**The write path.** None.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `001BDD20` | `AddMotion_LoadResources` | ✅ full body |
| `001BE1A0` | `AddMotion_ParseFile` | ✅ full body |
| `001BE430` | `AddMotion_LookupByModelName` | ✅ full body |
| `003714A0` | `AddMotion_ApplyBonePose` | ◐ the track/record walk `003716B0`–`0037175C` and the rotation call *(answered: see the full disassembly below; 2026-10-02, OPUS)* |

### Data addresses

| Address | Name | Kind | Contents |
|---|---|---|---|
| `008F9628` | list path | `.rdata` | `./PS2Data/add_motion/add_motion_list.txt` |
| `008F9658` / `008F9678` | file formats | `.rdata` | `./PS2Data/add_motion/%s.adm`, `./PS2Data/add_motion/%s_town.adm` |
| `008F96A0` | twin name format | `.rdata` | `%s_town` |

## 5. Corpus survey

146 tracks in 39 files, 382 groups. Of the tracks, 111 have `field00 = 0` and 35 have `1`; 35 have
`field02 = 0`, the other 111 carry one of 26 values from 9 to 84. Whether the 35 `field00 = 1` tracks are the 35
`field02 = 0` tracks ~~was not cross-tabulated~~ *(answered: see §6's pass - the same 35 tracks, tested as set equality; 2026-10-02, OPUS)*.

## 6. Falsification pass

~~Not yet run.~~ *(answered: see Falsification pass 1 — 2026-09-13 (OPUS), below; 2026-10-02, OPUS)* The census walk is the positive control for the layout (39 / 39 end exactly at the file size);
the census also corrected this sheet's draft twice — a `field02` range read from the top-twelve list only, and a
sixth bone index that was a tie-order artefact.

## 7. What this document does not claim

- [x] **MA-1.** Track bytes, group fields and record value bytes — **answered 2026-09-24 (SWE2-DATA)**, §10:
      the record is `{i32 bone; f32 eulerDeg[3]; f32 offset[3]}`, the group header is a keyframe whose lane
      `field01` is the driven scalar, and groups 1–3 are reached either by key interpolation (kind 0) or by
      `+0x18` id match (kind 1). Still open: who consumes the second triple (dead to the sole traced consumer),
      and what the group header's other floats mean.

## 8. Related

- [Model and motion formats](README.md) — the folder's format plan.
- **Siblings in `ps2data/add_motion/` this sheet does not cover:** `skeletonmapping.bin` (string `00D110A8`, read by
  `AddMotion_LoadSkeletonMapping` `0036FFF0`), `highmodelreplace.bin` (`00D11190`, `AddMotion_LoadHighModelReplace`
  `0037CCC0`), and the text files `hc1004_02.txt`, `pc1004_02_open.txt`, `pc1004_02_close.txt` — none read here.

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run first, one query at a time and read in full.)*

### Every figure reproduces, walked from the archive by the parser's rules

The walk was re-implemented from §2 — `i16 trackCount`, then per track an 8-byte header, then
`groupCount` groups of a `0x1C` header plus `recordCount × 0x1C` records — and run over all 39 files:

| claim | measured |
|---|---|
| **39** `.adm`; `hc` 30, `hn` 7, `hs` 2 | **39**; **30 / 7 / 2** |
| the walk ends exactly at the file size | **39 / 39** |
| tracks per file — 4 in 35, 2 in 2, 1 in 2 | **exactly** |
| groups per track — 2 in 90, 3 in 22, 4 in 34 | **exactly** (146 tracks, **382** groups) |
| records per group — 4, 6, 8, 12, 13, 15, 17, 18 | **exactly those eight** |
| track `+0x00` 0 in 111, 1 in 35 | **111 / 35** |
| track `+0x01` 0 / 1 / 2 in 35 / 74 / 37 | **35 / 74 / 37** |
| track `+0x02` 0 in 35; 26 distinct values 9…84 in the other 111 | **35 zeros; 26 distinct, 9…84** |
| group `+0x18` 0 in 291 of 382; 1 / 2 / 3 in 31 / 31 / 29 | **291 / 31 / 31 / 29** |
| `add_motion_list.txt` — 23 names, all with `<name>.adm`, 15 (all `hc`) with a `_town` twin | **23 / 23 / 15**, and all 15 are `hc` |
| `hn1018_12.adm` ships and is not in the list | **confirmed** |

### ✔ New: the first track of every four-track file is a distinguished track

§2 reports the three track fields as three independent distributions and mentions the all-zero group
header as an aside. **They are one fact.** The set of tracks with `+0x00 = 1`, the set with
`+0x01 = 0`, the set with `+0x02 = 0` and the set whose **first group header is 28 zero bytes** are
**the same 35 tracks** — tested as set equality, not as matching counts:

* every one is **track index 0** of its file;
* they are exactly the **35 files whose `trackCount` is 4**;
* every one has `recordCount` **4**, while the other 111 tracks take 4, 6, 8, 12, 13, 15, 17 or 18;
* the four files with **no** such track are exactly the two-track and one-track files —
  `hn1017_03`, `hn1018_12`, `hs0003_01`, `hs0020_01`.

> **So the track array is not homogeneous**, and a reimplementation that treats track 0 like the rest
> is reading a header as data. Four independent fields mark it, which is why this is worth stating as
> structure rather than as four distributions that happen to total 35.

~~**What it is for is not established.**~~ *(answered: see the answers near the end - the `field00 = 1` tracks are the id-match track 0, and its sentinel is the base pose; 2026-10-02, OPUS)* The marking is measured; the meaning is not, and §7's
unknowns stand.

### Two notes for anyone re-running the census

**The sixth most common bone is a tie.** 6 and 7 at **123**, 28 at **94**, 27 at **79**, 9 at **77**,
then **29 and 41 both at 74**. §5 lists 29; the census's own note says ties are sorted, so that is its
tie-break — but a re-runner whose counter returns 41 will think the figure disagrees. It does not.

**The "first three groups" aside is order-dependent.** Counted properly, **46 of 382** group headers
are all zero, across 35 files, **35 of them the first group of a track**. In archive order only the
first group of `hc1004_02.adm` falls in the first three, so the sentence does not survive a different
traversal; the 46 / 382 / 35 figures do.

**Not claimed.** What the marked track carries, or what distinguishes it beyond the four fields. The
element types inside a record — §2 already says the parser fixes positions and widths but not types,
and this pass adds nothing there. What the `_town` twin changes. Whether `AddMotion_ApplyBonePose`
treats track 0 differently — **the loader and the parser were not re-read here; this pass walked the
data.** The archive was **read, never written**, and nothing was executed.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CoreRuntimeScheduling — CLIENT.** `FUN_0022a0b0`, owned by that layer, calls `0037CCC0` on this page. That caller is a startup sequence that WRITES the globals the small scheduling getters read - `[02064AA4]`, `[01E02814]` and `[01E0281C]`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**The `00377C20` fan-out — TWELVE subsystem labels, one crossing (2026-09-17, SWE2-FRONTIER).**
`00377C20` is `FieldData_GetActiveFieldRecordBit15`, the shared action-permission accessor this page's
`0017FFB0` row consults. Its callers fan out across ActorEntity (`0025C830`, `00266C60`), CombatAI
(`003014C0`, `00301AD0`, `00305AB0`), CombatAction (`002FFA60`, `002FFCF0`, `002FFF50`, `00305110`),
CombatFormula (`00300530`), Gameplay (`00307D10`, `0030A8A0`, `0030C210`, `0030D9A0`), Input
(`00253C70`), InputGameplay (`00313A00`), Items_Equipment_Shops_License (`00309FB0`, `0030FD10`),
Movement (`0025B470`, `0026C3E0`, `002E28E0`, `00310920`), Party (`00304180`),
Rewards_Progression_Economy (`00312280`), Script_VM_Native_Bridge (`00344740`, `00352FA0`,
`003537D0`, `00355680`) and Status_Periodic_Terminal (`0030E360`, `0030F690`, `00310DB0`). Every one of
those is a client of the shared accessor asking "is this action permitted in the active field state" —
the accessor's own fan-out, accounted at
[`the-shared-neighbours-pass-22-keeps-finding.md`](../../00-Engine-Core-Runtime/Shared-State-Accessors/the-shared-neighbours-pass-22-keeps-finding.md),
not anything this page's add-motion tables hand those layers.

**Input — CLIENT (the second edge kind).** `00197160`, `00197790` and `00197800`, owned by that layer,
call `001D50D0` — the 66 B singleton accessor this page's `00180060`/`00180090` rows use for the
interpolation-override flag (`+0xCF1`) and value (`+0xCF4`). The crossing is three input-layer bodies
reading the same override object this page's getters read; not shared ownership.

**Audio — MECHANICAL (SWE2-EC7-36, 2 edges).** `00202DE0` and `00203080` — the shared UI helpers this page cites inside `003F7930` — are each called by the same Audio body. Shared-helper fan-in; no audio relationship to the motion tables.
- **Application - CLIENT (1 edge).** `001BE3E0` is called by bodies filed to Application: `0017D6B0` - shared machinery across the layer boundary, no shared ownership.
- **PlatformOnlineAchievements - SERVICE (2 edges).** `001CD0E0`, BattleUnit_ProcessDefeatRewardsAndLoot (`00312280`) reach bodies filed to PlatformOnlineAchievements: `003166F0`, `00316A50` - shared machinery across the layer boundary, no shared ownership.
- **Resource - SERVICE (24 edges).** AddMotion_LoadResources (`001BDD20`), `001CD0E0`, `001D1660`, `0022A0B0` (+6 more) reach bodies filed to Resource: `001D6E80`, `001D6EE0`, `001D6F20`, `001D6FA0` (+12 more) - shared machinery across the layer boundary, no shared ownership.
- **SaveLoad - CLIENT (1 edge).** `0019C580` is called by bodies filed to SaveLoad: `00866200` - shared machinery across the layer boundary, no shared ownership.

## The `003714A0` exclusive subtree — all 4 members bound (SWE2-FRONTIER, followup queue)

`AddMotion_ApplyBonePose` (`003714A0`, 3,387 B) resolves the motion record's
section via `0020E600` (`00371537`), turns `word[+0xA8]` into a `0x740`-stride
attach record in the `[022C6F28]` table with a `+0x284` liveness gate
(`00371559`–`00371572`), does the same for the parent record reached through
`+0xC` (`003715A1`–`003715F2`), then picks between the two ADM handles at
`+0x6E8`/`+0x6F0` — the combat flag from `00377C20`, overridden by member
`0017FFB0`: return `1` forces handle 1, return `2` forces handle 0
(`003715F6`–`00371623`). The main loop lazily allocates the per-record
scratch triplets at `rsi+0x708` through `0019C580` with `00861EC0` clears
(`00371640`–`003716CC`), then per bone channel solves
`(frame − key0) / span * rate` with a `00180060`/`00180090` flag-and-value pair
choosing whether the solved parameter or a fixed override is used
(`00371ADA`–`00371B0F`), walks the packed key stream `word[r12+r14+4]`
(`00371B13`), writes bones through `0046D380`, and on the `al == 1` tail
(`00371F2E`) resolves the skeleton's `+0xDA0` object via `0020E600` into
`004780B0` (`00371F4D`) and member `004776D0` (`00371F64`) before scanning the
`0x28`-stride bone list for the channel target (`00371F69`–`00371F96`).

| member | role | interior |
| --- | --- | --- |
| `0017FFB0` (32 B) | combat-look override getter — `001BE420()` singleton, returns `dword[obj+0x20]`; the caller maps `1 → handle 1`, `2 → handle 0`, else `00377C20`'s flags | [`0017FFC3`](../../_index/ADDRESS-INDEX.md) |
| `00180060` (36 B) | `001D50D0()` singleton → `byte[obj+0xCF1]` — the flag that decides whether the solved interpolation parameter or the override is taken | [`00180073`](../../_index/ADDRESS-INDEX.md) |
| `00180090` (40 B) | `001D50D0()` singleton → `float[obj+0xCF4]` — the override value substituted when the flag says so | [`001800A3`](../../_index/ADDRESS-INDEX.md) |
| `004776D0` (117 B) | the packed channel-table decoder — `r9 = 02CA6CA0 + cl*0x40` validated by `[r9+4] == ecx`, `word[r9] != 0`, `byte[r9+r8+0x10] != 0`; walks `byte[r8+0x20]`-seeded u16 offsets through `[rdx]` with `byte[r8+0x28]`/`byte[r8+0x30]` branch selects, returns `byte[rcx+rax*4+5]`, `-1` on any failed gate | [`004776E4`](../../_index/ADDRESS-INDEX.md) |

Shared callees deliberately outside the census: `0020E600`, `00377C20`,
`0019C580`, `00861EC0`, `00808F10`, `00861F02`/`00861F14`, `0046D380`,
`004780B0`, `001BE420`, `001D50D0`, `00808C40`.

## Interior citation — frontier hub `00202D80` (2026-09-18, SWE2-EC7)

`00202D80` — 81 B, 10 callers (five of them Presentation-side: `00373860`, `003F7930`,
`00505570`, `00505E00`, `005621A0`); a bare vec4 element-wise multiply — `out[i] =
a[i] * b[i]` for `i` in 0..3 through a spill/reload of the four `mulss` results
([`00202DC5`](../../_index/ADDRESS-INDEX.md)). The `adm`/`add` motion-table evaluators call it
wherever a channel scale vector multiplies a basis or weight vector.

## SWE2-EC7-36 update (2026-09-19) - `003F7930`

`003F7930` (651 B) is an adm/add-motion body - `01EFF4E0`/`01CEBBA8`/`01CEBD80`, `00202DE0`/`00202C90` pairs plus `00203080`/`00202D80`/`00808C40`. Interior anchor `003F799C` (a `00202DE0` call).

## SWE2-EC7-45 update (2026-09-19) - `002FFA60`

`002FFA60` (243 B) is a body - `0020E600`/`00377C20`. Interior anchor `002FFA9D` (a `0020E600` call).

## SWE2-EC7-46 update (2026-09-19) - `001BE430`

`001BE430` (235 B) is a body - `0017D2E0`/`00808C40`. Interior anchor `001BE466` (an `0017D2E0` call).

## SWE2-EC7-58 update (2026-09-19) - `00352FA0`

`00352FA0` (166 B) is an adm-add-motion body - `00262F50`/`00263750`/`00264050`/`002647C0`/`00267E10`/`0026B4E0`/`00377C20`. Interior anchor `00352FB8` (a `00267E10` call).

## SWE2-EC7-60 update (2026-09-19) - `00344740`

`00344740` (156 B) is an adm-add-motion body - `00233D70`/`00263750`/`00264050`/`002EB430`/`002ECA00`/`002ED020`/`0035AE10`. Interior anchor `00344744` (a `00377C20` call).


## SWE2-EC7-82 update (2026-09-20) - `00477130` quaternion-to-matrix measured

`00477130` (430 B, no calls) is the quaternion -> rotation-matrix
builder the motion caller runs: the four-vector at `[rdx]`/`[+0xC]`
is squared, summed and reciprocated (`1 / (x2+y2+z2+w2)`), then the
nine `2r`-scaled cross terms land at `+0..+0x24` in the classic
`1-(yy+zz)` / `xy+-zw` / `xz+-yw` layout, with `0` columns and the
`1.0f` homogeneous element at `+0x38` - a 4x4 transform row-block.
Interior anchor `00477166` (the `mulss` square head).

## SWE2-EC7-86 update (2026-09-20) - `003E6310` resolve-then-forward measured

`003E6310` (39 B) is the resolve gate the motion-table callers
run: `002EDBD0(rcx)` resolves the record; on null it returns
untouched, otherwise a tail `004FE2F0(resolved, edx)` runs the
forward.
Interior anchor `003E6332` (the `004FE2F0` tail).

## SWE2-EC7-104 update (2026-09-20) - `002647C0` measured

`002647C0` (9 B) is the range predicate
`00351F40`, `00352FA0`, `003537D0`,
`0037B4D0` and `0050C610` call:
`return ecx <= 3` - the four-slot bound check
shared across the motion-table arms and the
script bridge.
Interior anchor `002647C2` (the `cmp ecx,
3`).

## SWE2-EC7-105 update (2026-09-20) - `00264050` measured

`00264050` (103 B) is the scoped-global swap
`00344740`, `00352FA0` and `003537D0` run
around the `02099D70` table pointer: the old
value is saved, `rcx` (or `02098E10` when
null) is installed, then `edx >= 0` runs
`00358940(new)` while `edx < 0` runs
`003590D0()` and - only when that count is
nonzero - `003588B0(count)`. The old pointer
is restored on every path - a
swap-evaluate-restore bracket the motion
arms reuse.
Interior anchor `00264079` (the `00358940`
call).

## SWE2-EC7-109 update (2026-09-20) - `00202CF0` measured

`00202CF0` (41 B) is the vec3
scalar divide `003C7B30`,
`00505570` and `00505E00` call:
`[rcx + i*4] = [rdx + i*4] /
xmm2` for `i = 0..2` - the
uniform scale-down the motion
table normalizations use.
Interior anchor `00202CF4` (the
first `divss`).

`00372610` (245 B) is the staged-record submit `00373860` runs: a `0x48` stack record is zeroed (plus `[rsp+0x5C]` and `xmm0` field), `00202D70(&rec, rdx, r8)` opens it, `00202FE0` fires four times against the staged fields, then `00202D70` twice more and `00202FE0` once carry the `rsi`/`rdi` operand legs - the add-motion row the table builder emits per call.

Interior anchor `0037266C` (function `00372610`).


## 10. MA-1 answered — the semantic layer (2026-09-24, SWE2-DATA)

*Method: full disassembly of `AddMotion_ApplyBonePose` (`003714A0`) against the shipped EXE, plus a
re-walk of the 3,553 authored records in all 39 `.adm` files.*

**A record is `{i32 bone; f32 eulerDeg[3]; f32 offset[3]}`.** The apply loop
(`00371C01`–`00371D27`) reads exactly bytes `+0x04`..`+0x0F` — three floats, lerped between the
selected group and the next — scales them by `π/180` (constants `xmm9 = 3.1415927` @
`[rip+0x197A2C8]`, `xmm10 = 180.0` @ `[rip+0x5817A3]` — the stored values are **degrees**), stores
the result at bone-record `+0x190`/`+0x194`/`+0x198`, and feeds all three to
`Matrix4x4f_BuildEulerRotation` (`0046D380`). Authored data agrees: the first triple spans
**±195°** across 3,553 records; the second triple spans **±0.133** — a magnitude, nothing more;
no unit or meaning is established by that number.

**The second triple is dead-to-TZA within the enumerated accessor domain.** The domain was
closed before the claim was made (2026-09-26, SWE2-DATA, on FABLE's review): the parsed-`.adm`
registry singleton `0x1F81250` is touched by exactly two functions — its installer `001BE3E0` and
the getter `001BE420` — and the getter's five callers are `0017FFB0` / `00183240` / `001CD0E0` /
`001D1660`, which read or write only the registry's own `+0x20` flag dword, and `00863110`, which
performs the name lookup. `AddMotion_LookupByModelName` (`001BE430`) has exactly one inbound
reference under all four instruments (call/jmp edge, code operand, immediate, data qword): the
call in `00863110`; `00863110`'s only caller is the binder `002EDF90`, whose only output is the
two handle slots `+0x6E8`/`+0x6F0`. An image-wide operand census of those two fields, then
discriminated by type (the offsets are shared by unrelated structs — 0x68-stride arrays, float
fields, vector spills, vtable stores — which is why the field-offset scan alone was never
sufficient), finds **exactly one function that dereferences a slot value into the parsed object
and walks its `+0x20`-pointer / `0x1C`-stride record array: `003714A0`**. Every other touch
stores, nulls, compares, or performs a shallow read on the slot value — including `007B5E50`,
which treats the value as a packed handle and resolves it through the global handle table
`02EAD730`. Within that sole consumer, no instruction reads record bytes `+0x10`..`+0x1B`
(operand scan of the whole body; positive control — the same scan finds the `+0x00` bone-index
reads and the `+0x04`..`+0x0F` euler reads, and finds `+0x10`..`+0x1B` displacements in hundreds
of unrelated functions, so the instrument is positive for the access class). The loader's
wholesale group/record byte copy (`001BE2E0`–`001BE373`) is the only other physical touch.
The offset half is authored and nonzero in all 3,553 records; *inference, unproven:* a
bone-space translation the PS2 pose path applied and the TZA path dropped.

**The group header is a keyframe.** The parsed track is the 16-byte object the file header fields
land in (`+0x00` `field02`, `+0x02` `recordCount`, `+0x04` `groupCount`, `+0x06` `{field00,
field01}`, `+0x08` group array). Two selection modes, keyed by `field00` (`al` tested at
`003719BC`/`00371F2E`):

- **`field00 = 0` — keyed interpolation** (`00371B13`–`00371B95`): the group array itself is the
  key stream. `field01` picks which float lane of each group header is the driven scalar —
  `byte[track+7] * 4` is added to the group base, so lane values 0/1/2 select the floats at group
  `+0x00`/`+0x04`/`+0x08` (matching the authored distribution 35/74/37). The solver brackets the
  current channel parameter between `lane[g]` and `lane[g+1]`, emits group index `g` and local
  `t = (param − lane[g]) / (lane[g+1] − lane[g])`, and the record loop then lerps
  `euler[g]·(1−t) + euler[g+1]·t` for every record. The parameter may be overridden per channel by
  the `00180060`/`00180090` flag/value pair (`+0xCF1`/`+0xCF4` of the `001D50D0` singleton).
- **`field00 = 1` — id-match selection** (`00371F36`–`00371FB7`): the track's `field02` is handed
  to `004776D0` (the packed channel-table decoder, table base `02CA6CA0`, called with
  `ecx/edx` from the `+0xDA0` sub-object) which returns the live pose-slot value; the code then
  scans the group array's `+0x18` u32 for an equal id (`00371F69`–`00371F96`) and applies that
  single group's records. This is exactly the track set OPUS flagged in §9 — all 35 kind-1 tracks
  are **track 0** of the 35 four-track files, and they alone populate group `+0x18` (values 1/2/3
  in 91 groups, 0 in the 291 groups under kind-0 tracks — the field is their selector, unused
  elsewhere).

**`field02` is the channel id.** The u16 (26 distinct values, 9..84) is the argument the kind-1
path passes to the channel-table decoder and the kind-0 path pairs with its key stream — the name
of "which pose parameter this track listens to". Track 0's `field02 = 0` matches its id-match
role: it has no parameter to bracket.

**The index tables key on group 0 by design.** The `table1[bone] = trackIndex` /
`table2[bone] = recordIndex` build (`003716E2`–`0037174C`) always walks **group 0's** record array
(`[groupArray + 0x20]`), because records are parallel keyframes: record *i* names the same bone in
every group. The apply loop then reads `record i` inside whichever groups the selector picked.
Group 0's all-zero header in the 35 four-track files is therefore not data — it is the base-pose
sentinel for the id-match track.

**Out-of-range bone.** `record.bone` is `movsxd`'d straight into `[table + bone*4]` stores with no
check against the skeleton's bone count (`[r13+0x88]`) — an authored out-of-range index writes past
both scratch tables. The shipped corpus never does this: all 3,553 bone indices are non-negative
and the maximum is **84**.

**The `_town` twin** selection is as documented in §3 — the `002EDF90` five-state binder hands the
applier both handles at `+0x6E8`/`+0x6F0`, and `003715F6`–`00371623` pick by the combat flag
`00377C20` under the `0017FFB0` override (`1`→town handle, `2`→base handle). `_town` tables are the
civilian-area variants of the same additive-pose tracks.

*Evidence class: NATIVE/STATIC for every semantic above — read from the shipping EXE — with the
authored-data ranges measured over all 39 files.*

`00262F50` (50 B) is the probe-and-flag shim the motion-table registration callers share: it runs `00262F90(rcx)` first and only when that returns nonzero calls `002ECCF0(rcx, 1)` before handing the probe result back - a conditional mark on the registered object.

Interior anchor `00262F70` (function `00262F50`).

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-adm-add-motion-tables-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00183240` | 32 B | when `001BE420()` returns non-null, calls `001BE420()` again and stores `ecx` at dword `+0x20` of the result; otherwise returns without work | `00183248`, `0018324D`, `00183252`, `00183257` |
| `00351F40` | 65 B | calls `00267E10(r9)` and stores its low byte at byte `+0xD` of `r8`; stores 1 at byte `+0xC` of `r8` when `002647C0` of that result is non-zero, else 0 (`setne`); then tail-jumps `0026B4A0(rdx, 0xB)` | `00351F53`, `00351F5A`, `00351F5D`, `00351F6F`, `00351F7C` |
