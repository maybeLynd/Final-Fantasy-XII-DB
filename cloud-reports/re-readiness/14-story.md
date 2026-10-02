# Reconstruction readiness — `FFXII TZA/14-Story-Event-Quest-Hunt/`

| | |
|---|---|
| Stream | R (reconstruction readiness), per [`docs/cloud-briefs/re-readiness.md`](../../docs/cloud-briefs/re-readiness.md) |
| Board task | `OPUS-CLOUD-R-READINESS-14-1002` |
| Date | 2026-10-02 |
| Snapshot | this repo's text snapshot at `df2c9f47` only; no executable, Ghidra or live game was used |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every item quotes or paraphrases a page and gives its location. Text is quoted as the snapshot has it; several of these pages are being edited by other lanes. |

**Counts:** _(filled in when the report is complete; see the end of the commit series)_

Citation form: `page:line`, where `page` is the file name inside `FFXII TZA/14-Story-Event-Quest-Hunt/`. The pages are:

- `README.md` (35 lines)
- `persistent-flag-banks.md` (1,437 lines)
- `CONTRACT-persistent-flag-banks.md` (654 lines)
- `event-memory-at-actor-bind.md` (393 lines)

"Not stated" means none of these four pages says it. Where another category's page is the only place a point is made,
the pointer is given as the 14 page cites it; that other page was not audited for this report.

## Pages read

| page | status as the page states it |
|---|---|
| `README.md` | category index; "Functions \| 15" (`README.md:8`); lists one system only, `persistent-flag-banks.md`, as "**DOCUMENTED, tier 1.**" (`README.md:14`, repeated in a duplicated section at `README.md:33`); does not list `event-memory-at-actor-bind.md` or the contract |
| `persistent-flag-banks.md` | `status: AUDITED` (`:4`); `readiness: BEHAVIORALLY UNDERSTOOD` (`:8`); `confidence: PROVEN` (`:9`); `last_reviewed: 2026-09-08` (`:21`); `audit.passes: 2`, `last_pass: 2026-09-02` (`:26-27`); `reopened_count: 6` (`:30`) |
| `CONTRACT-persistent-flag-banks.md` | `readiness: CONTRACT READY` (`:6`); `confidence: PROVEN` (`:7`); `entries:` 17 addresses (`:9`); `last_reviewed: 2026-09-08` (`:17`); `audit.passes: 1`, `last_pass: 2026-09-12` (`:19-20`); `crossref_clean: false` (`:22`) |
| `event-memory-at-actor-bind.md` | `status: AUDITED — DS-1 resolved 2026-09-16 … this page has no open item of its own` (`:4`); `readiness: BEHAVIORALLY UNDERSTOOD` (`:8`); `confidence: HIGH` (`:9`); `last_reviewed: 2026-09-08` (`:22`); `audit.passes: 1`, `last_pass: 2026-09-13` (`:26-27`) |
| `persistent-flag-payload-accesses.tsv` (layout check only) | header `function name site disp kind instruction route note` and 13 data rows: one `lea` at `002EF2E1` (the reset's base), eleven reads/writes of payload `+0x1044`..`+0x1054` by `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` `00584210`, and the `+0x1535` store at `002EF37D` in `002EF370`. **No page in the folder links this file**; its `+0x1535` row agrees with `persistent-flag-banks.md:461-462`. |
| `members/mapjump-flag-census.tsv` (layout and counts only) | 3 comment lines, header `id preset set release is scripts areas`, **330 data rows** = "328 flag ids and 2 threshold-query ids" — agrees with `persistent-flag-banks.md:378`; its comment line "pre-set on a new game 46 of 52" and the six unnamed pre-set ids agree with `persistent-flag-banks.md:376`, `:378` |
| `members/*.py` | read only for their header comments (the census domains); not run |

No item below rests on a `.tsv` or `.py` file alone.

---

## 1. Interface

The folder documents one small native core and several authored mechanisms built on it:

- **The persistent flag banks.** Five storage regions (the pages also say "six"; see contradiction C-V1) at fixed
  offsets in the save's persistent payload, eleven bit accessors, and one *authored gate* that either reads the
  `Primary` bank or consults an **authored threshold schedule** that is not a flag at all.
- **The new-game initial set.** A `memset` of the whole payload followed by a shipped list of `Primary` ids.
- **Event memory at actor bind.** One shipped id list (`eventmemorylist.bin`) consulted when an actor definition is
  bound, gating a buffer reallocation; plus a consult of the field record table (owned by 03).
- **Two RNG-fed authored writers** of `Bank512` (traps and treasure chests), documented here though owned by Combat
  Action / unowned.
- **The bestiary block** (Clan Primer sighting / defeat counts), native and separate from the banks.
- **Hunts:** not a native system — "a flag convention plus a counter, authored in script" (`event-memory-at-actor-bind.md:190`).

### 1.1 Entry points (functions, with their callers)

#### Flag-bank accessors (the 15 owned functions, plus the reset and payload base)

All take the id in `ecx`, MS x64, and reach the payload only through `SaveImage_GetPersistentPayloadBase`
`002EF2B0` (`CONTRACT-persistent-flag-banks.md:47-48`).

| entry | signature / returns | callers as stated | cite |
|---|---|---|---|
| `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` `0032A8A0` (122 B; but see C-V3) | `(uint16 encodedId ecx)` → `eax` 0/1 | **32 callers** (`persistent-flag-banks.md:424`, `:1057-1059`; `CONTRACT-persistent-flag-banks.md:145`), "including two five-byte thunks the §3 table does not list" (`persistent-flag-banks.md:1058`). Named: `InputGameplay_ArbitrateDigitalInputAndModalState`, `FUN_00281AE0`, `FUN_0029C530` (UI), `SaveImage_FinalizeHeaderAndChecksum` (`persistent-flag-banks.md:624-627`); input body `00253C70` (`CONTRACT-persistent-flag-banks.md:633`); the `ismapjumpgroupflag` verb handler (`persistent-flag-banks.md:376`). The other callers are **not stated** individually. | `persistent-flag-banks.md:131-150`, `:263`; `CONTRACT-persistent-flag-banks.md:52`, `:73-74` ("There is no query for Primary") |
| `PersistentFlag_QueryAuthoredThresholdSchedule` `00377970` (127 B) | `(int index ecx)` → 0/1 | the gate only ("The body above is its only reader" of `02ADD0C8`, `persistent-flag-banks.md:201`; subtree table `CONTRACT-persistent-flag-banks.md:650-652`) | `persistent-flag-banks.md:169-186`, `:273` |
| `PersistentFlag_QueryBank2048` `0032A930` (100 B) | `(int id)` → 0/1 | display-name resolver `00263990`, its by-id twin `002639E0`, shop name readers `002B9C70` and `002BA530`/`002BA548` (C-V4), script handler `0034E980`; "seven call sites in five functions" | `persistent-flag-banks.md:640`; `CONTRACT-persistent-flag-banks.md:388-392`, `:488` |
| `PersistentFlag_SetBank2048` `0032ABF0` (119 B) | `(int id, int value)` | message-window opener `002E16B0` (`SetBank2048(actor word +0x102, 1)` at `002E16DF`..`002E16EB`); script handlers `0034DFA0`, `0034E320` (`settalknpcname` `0x399`, `releasetalknpcname` `0x39A`) | `persistent-flag-banks.md:640`, `:496`; `CONTRACT-persistent-flag-banks.md:393-394` |
| `PersistentFlag_QueryBank64A` `0032A9A0` / `QueryBank64B` `0032AA00` (93 B each) | `(int id)` → 0/1 | `0034D940` (site `0034D953`) / `0034DDB0` (site `0034DDC3`) — verbs `isshutoralappear` `0x2F8` / `isshutoralenable` `0x2FB`; **no shipped script uses them** | `CONTRACT-persistent-flag-banks.md:248-258`, `:449-456`; `persistent-flag-banks.md:496` |
| `PersistentFlag_SetBank64A` `0032AC70` / `SetBank64B` `0032ACF0` (116 B) | `(int id, int value)` | `0034CA20`/`0034D190` and `0034CD40`/`0034D600` — the `clear`/`set` `shutoral` verbs `0x2F9`/`0x2FA`, `0x2FC`/`0x2FD`; no shipped use | same as above |
| `PersistentFlag_QueryBank512Low` `0032AA60` (100 B) | `(int id)`, id `0..0xFF` | trap arming `002FA740` (skips a record whose flag is set, `persistent-flag-banks.md:748-749`); verb `istreasurebattleflag` ("no shipped use", `:369`); VM query `00354540` or `00354000` (which one is Low is **not stated**, `:612`) | `CONTRACT-persistent-flag-banks.md:56`, `:632` |
| `PersistentFlag_QueryBank512High` `0032AAD0` (104 B) | `(int id)` — "**adds `0x100` itself**" | verb `istreasureflag` (26 uses) | `persistent-flag-banks.md:369`, `:376`; `CONTRACT-persistent-flag-banks.md:57`, `:320-322` |
| `PersistentFlag_SetBank512Low` `0032AD70` / `High` `0032ADF0` (119/123 B) | `(int id, int value)` | Low: trap trigger `002F8060` and treasure open `002FAFD0` (`persistent-flag-banks.md:822-828`); VM setters `00353750`, `00353BD0`, `00352EA0`, `00353390` (`:612`; `event-memory-at-actor-bind.md:367` names `00353750`, `00353BD0` as callers of `0032AD70`); which VM handler is set/clear/High is **not stated** | `CONTRACT-persistent-flag-banks.md:61` |
| `PersistentFlag_SetPrimary` `0032AB60` (121 B) | `(int id, int value)`; accepts `2..0x1FF` | `00379160` (new-game applier); VM handlers `0034DD90`, `0034EE20` = `setmapjumpgroupflag` / `releasemapjumpgroupflag`, which "pop one integer and tail-jump to `PersistentFlag_SetPrimary` with 1 and 0" | `persistent-flag-banks.md:376`, `:608`, `:1146`, `:1171-1174` |
| `PersistentFlag_ApplyAuthoredInitialPrimarySet` `00379160` (86 B) | `()` | **only** the tail-jump at `002EF2F1` in `002EF2D0`; zero `E8` callers | `persistent-flag-banks.md:1128-1191` |
| `SaveImage_ResetPersistentPayloadAndApplyAuthoredInitialFlags` `002EF2D0` (38 B, owner Save) | `()` | `FUN_00266D10` ("a run of ~20 subsystem resets", not read in full) and `SaveRuntime_ResetActiveImageAndRebindState` `002EF650` | `persistent-flag-banks.md:1092-1114`, `:1325-1326` |
| `SaveImage_GetPersistentPayloadBase` `002EF2B0` | `()` → `SaveImage_GetActiveBuffer()` `002EF640` `+ 0x200`; `002EF640` is `lea rax, 0x02164280` | 121 `E8` sites in 70 functions; `002EF640` 40 sites in 28 functions | `persistent-flag-banks.md:1107`, `:1116-1117`; `CONTRACT-persistent-flag-banks.md:476`, `:524-527` |
| `EventMemory_QueryDefinitionIdAbsent` `00377440` (62 B) | `(int id)` → **1 when absent**, 0 when listed | **one caller**: `ActorManager_BindLoadedDefinitionPayload` `0026C8C0` at `0026CA20` | `event-memory-at-actor-bind.md:107-121`, `:224`, `:272`; `CONTRACT-persistent-flag-banks.md:65`, `:70-71` |

#### Event memory at actor bind

| entry | callers | what it does | cite |
|---|---|---|---|
| `ActorManager_BindLoadedDefinitionPayload` `0026C8C0` | not stated in 14 | takes `esi = 0032F240(0)`; if `00377440(id)` says absent → `0025A990` (reallocate buffer A); if `00377480(id)` returns zero → `0025AA30` (reallocate buffer B); also configures fade and requested speed | `event-memory-at-actor-bind.md:62-79`, `:344-347` |
| `00377480` (S-11 `FieldRecordTable` accessor) | `0026C8C0` at `0026CA30` | bit 15 of the 3-byte record's little-endian word at `+8`/`+9`; 0 when table null or id out of bounds | `event-memory-at-actor-bind.md:52-60`, `:123-133` |
| `0025A990` / `0025AA30` (155 B each) | `0026C8C0` | free the held buffer, allocate from pool 5: `02099DD0` 1 MiB tag 13 / `02099DD8` 100 KiB tag 14 | `event-memory-at-actor-bind.md:83-95` |
| `EventMemoryList_PublishLoadedTable` `00378A50` | address-taken only, at `0037881D` in `00378540` | stores the loaded `(9, 41)` pointer into `02ADD0A8` (`mov eax, ecx` then 64-bit store) | `event-memory-at-actor-bind.md:144-147`, `:226`; `persistent-flag-banks.md:1301-1305` |

#### Authored-table publishers and the threshold variable

| entry | callers | what it does | cite |
|---|---|---|---|
| `WorldAreaField_RequestAuthoredMapTables` `00378540` (943 B) | not stated in 14 | requests kind-9 tables and installs ten-byte publishers: `(9, 0x28)` → `00378B90` → `02ADD0D0`; `(9, 0x29)` → `00378A50` → `02ADD0A8`; `(9, 0xA)` → completion `00378BA0` → `02ADD0C8` | `persistent-flag-banks.md:198-201`, `:1204-1232`, `:1329-1330` |
| `WorldAreaField_BootMapTables` `00377CC0` | `00266D10` (`persistent-flag-banks.md:1382`; `event-memory-at-actor-bind.md:370`) | **clears** the table globals ("in a run of `mov [g], rbx`", `00377D1C`; `02ADD0C8` teardown at `00377D15`) | `persistent-flag-banks.md:202`, `:1200`; `event-memory-at-actor-bind.md:62` |
| `FieldData_GetVariable0` `00265270` | 22 callers; the schedule; debug menu renderer; two achievement bodies; input `00253C70` | `(g_fieldFlags & 1) == 0` or `g_fieldVariables == NULL` → 0; else the first `u16` of the field's authored variable block | `persistent-flag-banks.md:219-230`, `:1364`, `:1370`; `CONTRACT-persistent-flag-banks.md:626-628` |
| `Resource_GetFileSizeByKindAndIndex` `0032E400` | not stated | `g_sizeTables[kind][index]` from `0x022C51F0`, guard `index < 0x400`, rounds up to 64 | `persistent-flag-banks.md:1260-1268` |

#### RNG-fed `Bank512` writers (owned elsewhere, documented here)

| entry | callers | what it does | cite |
|---|---|---|---|
| trap arming `002FA740` (477 B) | only verb `settrapresource` `0x053B` (`00355400` → `003EC630`, tail-call at `003EC679`) | walks the trap table, skips records whose `Bank512Low` flag is set, rolls the arm chance, sets bit *i* of the field mask, places a world marker `002FB560(i, x, y)`; ring of three `{fieldId, mask}` entries | `persistent-flag-banks.md:746-753`, `:1353` |
| `BattleUnit_TryTriggerNearbyAuthoredFieldAction` `002F8060` | the result "returns to `BattleUnit_RunPeriodicCombatMaintenance` (`00310FC9`–`003110BA`)"; the call edge itself is **not stated** | eligibility gate, proximity `1.3`, MT19937 75/25 pick of action id, set flag (`!= 0xFF`), post message `0046A9D0`, gather `002FB8C0`, retire marker `003EC700(i, 3)`, clear mask bit | `persistent-flag-banks.md:663-678`, `:702-719`, `:756-770` |
| `002FB8C0` | `002F8060` | gathers the four slot-map members (`0031B810`) within radius `+0x0A`; radius 0 = trigger unit alone | `persistent-flag-banks.md:761-764` |
| treasure open `002FAFD0` | one caller: end thunk `0050FAF0` of verb `btlAtelOpenTreasureMessage` `0x3037` | sets flag `+0x09` first, then gil-or-item draw (armlet-dependent pair), output triple | `persistent-flag-banks.md:830-847`, `:864-894` |
| `settrapshowstatus` `0x0547` (`00355E00` → `003EC6C0`) | script | shows or hides the sixteen marker slots `003EB720` indexes | `persistent-flag-banks.md:753-754` |

#### Bestiary (native, separate from the banks)

| entry | callers | what it does | cite |
|---|---|---|---|
| `00315A90` (thunk `00253760`) | `00306010`, on an action's execution | registers an entry: byte 0 → 1 | `event-memory-at-actor-bind.md:204` |
| `00315820` (thunk `00253750`, ~112 B) | `003171C0` on an enemy-kind defeat | `count = byte − 1` (0 if unregistered), `byte = min(count + 1, 0xFE) + 1`, only when `00315D50(id)` returns −1 | `event-memory-at-actor-bind.md:205`, `:375` |
| `00315420` (thunk `00253720`) | `00315E90`, Clan Primer menus `003154B0`, `003161A0`, `005760A0`, `00576E30` | reads `byte − 1`, or −1 when unregistered | `event-memory-at-actor-bind.md:206` |
| `00315D50` | `00315820` | walks a relative-offset chain from static `022C2550` to at most eleven `u16` ids; when listed, returns a word from `01EED130` | `event-memory-at-actor-bind.md:208-210`, `:379` |
| statistics counter `00316A50` | defeat processing, the gil setter, "among others" | "about twenty kinds" | `event-memory-at-actor-bind.md:183-185` |

#### Other functions the pages name with a role

| entry | role | cite |
|---|---|---|
| `0026A720` (verb `0x471`) | writes the saved music-track override `+0x1534`; negative arg clears `+0x1063` bit 6 and zeroes it | `persistent-flag-banks.md:456-458` |
| `002EF370` | sole store to payload `+0x1535` (raw `+0x1735`), from the options apply (`002DDB4A`, value 1) and verb `0x20D1` `debug_setscreenmode` (`0050D192`) | `persistent-flag-banks.md:461-468`; `CONTRACT-persistent-flag-banks.md:420-427` |
| `00377B60` (45 B) | flag-bank name lookup shared by `0029C530`/`002B9C70`/`002BA530` | `persistent-flag-banks.md:1399-1404` |
| `00576300` (578 B), `00570080` (295 B) | "event-memory record body" / "event-memory sibling" — role from call signatures only | `event-memory-at-actor-bind.md:336-338`, `:387-393` |

### 1.2 Inputs and outputs (data read and written, with record layouts)

#### The persistent payload (the banks' storage)

Base `= SaveImage_GetActiveBuffer() + 0x200` = fixed address `0x02164480`; length **`0x1538` = 5,432 bytes**, cleared by
one `memset` at `002EF2DB`/`002EF2E8` (`persistent-flag-banks.md:288`, `:1107-1119`; `CONTRACT-persistent-flag-banks.md:78-83`,
`:402-403`).

| payload offset | size | content | cite |
|---|---|---|---|
| `+0x1044`..`+0x105C` | 7 dwords | WorldTransition state block (field id at `+0x1044`) — owned elsewhere | `persistent-flag-banks.md:290`, `:342-343` |
| `+0x1060`..`+0x1064` | bytes | byte-flag cluster; `+0x1062` has 29 access sites; `+0x1063` bit 6 / `0x40` gates the music override | `persistent-flag-banks.md:344`, `:456-458`; `CONTRACT-persistent-flag-banks.md:413-419` |
| `+0x1164`, `+0x1364` | — | "unexplained" | `persistent-flag-banks.md:345` |
| `+0x1384` | `u8[8]` | `Bank64A`, ids `0..0x3F` | `persistent-flag-banks.md:61`, `:582` |
| `+0x138C` | `u8[8]` | `Bank64B`, ids `0..0x3F` | `persistent-flag-banks.md:62`, `:583` |
| `+0x1394`..`+0x13B3` | 32 B | gap — no accessor by any route; "reserved space … not a bank" | `persistent-flag-banks.md:505`; `CONTRACT-persistent-flag-banks.md:400-409` |
| `+0x13B4` | `u8[256]` | `Bank2048`, ids `0..0x7FF` (the NPC-name dictionary's id space) | `persistent-flag-banks.md:63`, `:370` |
| `+0x14B4` | `u8[64]` | `Bank512`, ids `0..0x1FF`; Low accessors `0..0xFF`, High add `0x100` | `persistent-flag-banks.md:64`, `:592-595` |
| `+0x14F4` | `u8[64]` | `Primary`, usable ids `2..0x1FF` | `persistent-flag-banks.md:65`, `:587` |
| `+0x1534` | `u8` | saved music-track override (verb `0x471`) | `persistent-flag-banks.md:297`, `:456-458` |
| `+0x1535` | `u8` | written (1 by options apply; any by `debug_setscreenmode`), never read | `persistent-flag-banks.md:298`, `:473-476` |
| `+0x1536`, `+0x1537` | — | no access at any width; "consistent with tail padding" | `persistent-flag-banks.md:480` |

**Bit addressing (every bank):** `byte = base + (id >> 3)`, `mask = 1 << (id & 7)`; set `|=`, clear `&= ~` — computed
with the signed-division idiom (`cdq ; and edx,7 ; add eax,edx ; and eax,7 ; sub eax,edx ; sar ecx,3`)
(`persistent-flag-banks.md:302-311`; `CONTRACT-persistent-flag-banks.md:116-126`, `:338`).

**Range guards** (upper end fails closed in all eleven; lower end differs): `QueryBank2048`, both `Bank512` queries
add `js`; `SetPrimary`, `SetBank2048`, both `Bank512` setters compare unsigned; the four `Bank64` accessors compare
signed with no `js` and accept negatives (`CONTRACT-persistent-flag-banks.md:208-221`, `:497-515`). A negative
`Bank64` id writes only when it is a multiple of 8, to bit 0 of `base + id/8` (`CONTRACT-persistent-flag-banks.md:264-286`);
no shipped path reaches a `Bank64` accessor (`CONTRACT-persistent-flag-banks.md:246-262`).

**`value` is a boolean** — any non-zero sets, zero clears; no toggle (`CONTRACT-persistent-flag-banks.md:67-68`).

#### The encoded gate id (16-bit authored value)

```
bit 14 set  : schedule(v & 0x3FFF)
else idx = v & 0x3FFF : 0 -> true, 1 -> false, < 0x200 -> Primary bit idx, else false
```

(`persistent-flag-banks.md:313-324`; `CONTRACT-persistent-flag-banks.md:339-342`.) `0xFFFF` is a "no condition"
sentinel at nine call sites; it evaluates false (`persistent-flag-banks.md:232-236`). Observed ids at the 32 call
sites: thresholds `0x4004`..`0x4011`, `0x4067`, `0xFFFF`; Primary `0x0001 0x0002 0x0054 0x005E 0x006F 0x0107`
(`persistent-flag-banks.md:238-244`; `CONTRACT-persistent-flag-banks.md:189-195`). Bit 15 of an id is not decoded
by the gate; a map-data gate word with bit 15 set is "a form this page does not read" (`persistent-flag-banks.md:380`).

#### Shipped files (all resource kind 9, all nine locale copies byte-identical unless noted)

| file | index | global | layout | consumer | cite |
|---|---|---|---|---|---|
| `mapjumpgroupinit.bin` (`FLAGDEF1`) | `0x28` = 40 | `02ADD0D0` | `char[8]` magic, `u16 count` at `+8` (53), `u16 id[count]` from `+0x0A`; 116 B. Ids: `0x0`, `0x56`, `0x65`-`0x66`, `0x70`, `0x79`-`0x7A`, `0x80`, `0xFC`, `0x108`, `0x10B`-`0x10C`, `0x11C`, `0x12C`-`0x134`, `0x136`-`0x137`, `0x13A`-`0x155`, `0x158` | `00379160` → `SetPrimary(id, 1)`; leading 0 dropped → **52** set | `persistent-flag-banks.md:23`, `:514`; `CONTRACT-persistent-flag-banks.md:430-438` |
| `eventmemorylist.bin` (`EVMEMLST` = `EVME`+`MLST`) | `0x29` = 41 | `02ADD0A8` | same header; count 8; ids `0x0000 0x0031 0x029C 0x029E 0x030E 0x0367 0x0368 0x0390`; 26 B; one copy under `common` | `00377440` membership | `event-memory-at-actor-bind.md:24`, `:241-255`; `persistent-flag-banks.md:514` |
| `mapjumpgroupflagrom.bin` (`FLAGROM1`) | `0xA` = 10 | `02ADD0C8` | `char[8]` magic (never compared), `u16 count` 152 at `+8`, `u16 offset[152]` from `+0x0A` (from file start; `0` = no schedule), then `u16` lists: bits 0-14 threshold, bit 15 on the last entry; 856 B | `00377970` | `persistent-flag-banks.md:24`, `:198-217` |
| `FileSizeTable_*.fst` | — | `0x022C51F0` | 41 kinds × 5,000 `u32`, no header | `0032E400` | `persistent-flag-banks.md:1260-1277` |

**The threshold schedule** (`00377970`): bound `index < count`, `off = offset[index]`, `off == 0` → false; then walk:
`if ((short)v < (entry & 0x7FFF)) return result; result = !result; if ((short)entry < 0) return result;` with
`v = FieldData_GetVariable0()` (`persistent-flag-banks.md:169-192`; `CONTRACT-persistent-flag-banks.md:162-170`).

#### Trap table and record (read by `002FA740` / `002F8060`)

Table `{u32 count <= 32; u32 offset[count]}` of 12-byte records, taken from `002641B0(0, 0)` script image header `+0x6C`
(`trapDataOff`), a storage-class-tagged reference (`tag = bits 24–26`, `offset = bits 0–23`), every shipped one tag 3
(`msp`) (`persistent-flag-banks.md:725`, `:736-741`). The pointer the trigger walks is `[022BE948]` (`:703`).

```
+0x00 s16 x/10   +0x02 s16 y/10   +0x04 u8 flag id (0xFF none)   +0x05 u8 arm chance %
+0x06 u16 action id 75 %   +0x08 u16 action id 25 %   +0x0A u8 radius (0 = trigger unit alone)   +0x0B u8 0
```

(`persistent-flag-banks.md:725-734`.) Proximity constant `1.29999995` at `00901B34`; divisor `10.0` at `008F8180`
(`:707-709`). The sixteen action rows a trap can name (246–261) and their recipes are tabled at `:773-780`; the
HP/MP/gil formulas are `(1 + roll % power) × (1 + roll % level)` with power from row `+0x10` and level from stats
`+0x1C2` (`:775-779`). Message rows: `0x103` → row 3, `0x104` → 1, `0x105` → 2, else 0 (`:710-714`).

#### Treasure record (read by `002FAFD0`)

```
+0x00 u8 chest index in the field's per-chest mask   +0x08 u8 flags (bit 6: gil amount random 1..N)
+0x09 u8 flag id (0xFF none, set FIRST)   +0x0B u8 gil chance %
+0x0C/+0x0E u16 item ids, normal pick (<50 / >=50)   +0x10/+0x12 u16 item ids, armlet pick (<95 / >=95)
+0x14 u16 gil amount (or N), normal   +0x16 u16 gil amount (or N), armlet
out: {kind: 1 = gil (+4 amount), 0 = item (+4 id, +6 = 1), 2 = nothing}
```

(`persistent-flag-banks.md:870-883`.) "Armlet" = party leader `003272A0` in play and layer id 25 in either effect layer
(`+0x6B` / `+0x7B` bit 1) (`:885-890`). A `0xFFFF` item id yields nothing (`:893`). Bytes `+0x01`..`+0x07`, `+0x0A`,
`+0x18`.. and the record size are **not stated**.

#### Field record table (read by `00377480`; owned by 03, contract S-11)

`02ADD100`: count `u32` at `+4`, 3-byte records from `+8`, indexed by id; `00377480` returns bit 15 of the
little-endian word at bytes `+8`/`+9` of the record (`event-memory-at-actor-bind.md:52-60`, `:125-133`, `:229`). The third
byte: "read by no accessor in that family … still open" (`:236-238`).

#### Bestiary block

512 bytes at save payload `+0xB404` (block `+0x3404` of what `002536A0` returns); one byte per Clan Primer entry id
(`.ard` class row word `+0x52`, 0–376); `0` = never encountered, else `1 + defeats`; every function bounds `id < 0x200`
(`event-memory-at-actor-bind.md:195-200`). Note `+0xB404` lies far beyond the `0x1538`-byte persistent payload of
§1.2's first table; the pages do not say which base `+0xB404` is relative to beyond "save payload" and `002536A0`.

#### Outputs

- Bank bits in the payload, therefore in the save (`persistent-flag-banks.md:404-406`, `:422`).
- Actor-definition buffers reallocated at bind (`event-memory-at-actor-bind.md:83-98`).
- Trap: a battle message, the action applied to gathered units, the marker retired, the mask bit cleared
  (`persistent-flag-banks.md:710-718`, `:766-770`).
- Treasure: the output triple (`persistent-flag-banks.md:882`); loot granted through `Inventory_GrantEncodedLootItem`
  by `0050FAF0` (`:1361`).
- Gate result consumed by the save header finalizer (`persistent-flag-banks.md:415-418`, `:626`) — **what header field
  receives it is not stated**.

### 1.3 State (globals and objects, with lifetime)

| state | lifetime as stated | cite |
|---|---|---|
| persistent payload `0x02164480`..`+0x1537` | static region of the save image; zeroed by `002EF2D0` (and the whole image `0x56690` B by `002EF650`); persists into the save; no code clears a bank wholesale except the reset `memset` | `persistent-flag-banks.md:1092-1119`, `:1017-1025`; `CONTRACT-persistent-flag-banks.md:129-130`, `:138` |
| `02ADD0D0`, `02ADD0A8`, `02ADD0C8` (table pointers, low 32 bits stored) | published at area-table request time by `00378540`'s publishers; cleared by `00377CC0`; "populated at area load" | `persistent-flag-banks.md:198-202`, `:1195-1202`; `event-memory-at-actor-bind.md:139-140` |
| `02ADD100` (`FieldRecordTable`) | owned by 03; lifetime **not stated** in 14 | `event-memory-at-actor-bind.md:54-62` |
| `g_fieldFlags`, `g_fieldVariables` | **addresses, writers and lifetime not stated** | `persistent-flag-banks.md:224-229` |
| `01F83530` (image-address base for the 32-bit pointers) | zero "at image load"; "zero for the process's life" is "supported, not proven" | `persistent-flag-banks.md:519-531` |
| trap mask ring `02EC3EA0` (3 × 12-byte `{fieldId, mask}`), count `02EC3EC8`, write index `02EC3EC4`, rotated `% 3` | written at arming; read by the trigger walk; initial value **not stated** | `persistent-flag-banks.md:750-753`, `:705-706` |
| trap table pointer `[022BE948]` | "built for the field by `002FA740`" | `persistent-flag-banks.md:703-705` |
| sixteen marker slots (`003EB720` indexes them) | **not stated** | `persistent-flag-banks.md:754`, `:1368` |
| actor buffers `02099DD0` (1 MiB, tag 13), `02099DD8` (100 KiB, tag 14) | reallocated at bind; touched only by ActorEntity and the two allocators; contents **not stated** | `event-memory-at-actor-bind.md:83-95`, `:234-235` |
| bestiary block (`+0xB404`) | in the save; initial value **not stated** | `event-memory-at-actor-bind.md:198-200` |
| `022C2550` / `01EED130` (bestiary exclusion chain) | static; meaning "(marks, story bosses) is not read here" | `event-memory-at-actor-bind.md:208-210` |

### 1.4 Order (what runs when, and what triggers it)

1. **New game / image reset.** `002EF650` (or `FUN_00266D10`) → `002EF2D0`: `memset(payload, 0, 0x1538)` then tail-jump
   to `00379160`, which sets the 52 ids — "before the first frame" (`persistent-flag-banks.md:382-383`, `:1092-1114`).
   Whether `FUN_00266D10` is "new game" is **not established** (`:1325-1326`). Precondition: the `02ADD0D0` list must
   already be published (else the applier does nothing, `:1155-1156`); **the order between `00378540`'s request and the
   reset is not stated**.
2. **Area / map tables.** `00378540` requests kind-9 tables and installs publishers; `00377CC0` clears them
   (`persistent-flag-banks.md:1200-1210`). When `00378540` runs relative to a field transition is **not stated**.
3. **Gate queries** happen whenever a caller asks; no cadence (`CONTRACT-persistent-flag-banks.md:204`). One script
   read for shape runs a per-frame loop over flag pairs (`persistent-flag-banks.md:380`).
4. **Name bit:** set when the message window opens for an actor (`persistent-flag-banks.md:385-386`, `:640`).
5. **Trap arming:** on `settrapresource` (`persistent-flag-banks.md:746-750`). **Trap trigger:** reached from
   `BattleUnit_RunPeriodicCombatMaintenance` (`:766-767`); its cadence is **not stated** in 14.
6. **Treasure:** on completion of the durative verb `btlAtelOpenTreasureMessage` (`persistent-flag-banks.md:865-867`).
7. **Actor bind:** `0026C8C0` → `00377440` → (absent) `0025A990`; → `00377480` → (zero) `0025AA30`
   (`event-memory-at-actor-bind.md:65-79`).
8. **Save:** `SaveImage_FinalizeHeaderAndChecksum` calls `gate(0x400B)`, then the payload is captured
   (`persistent-flag-banks.md:415-418`).
9. **Bestiary:** register on an action's execution against the other side (`00306010`); count on enemy-kind defeat
   (`003171C0`) (`event-memory-at-actor-bind.md:204-205`).

### 1.5 Dependencies (on other systems)

| system | what 14 needs from it | cite |
|---|---|---|
| 19 Save | the save image, active buffer `0x02164280`, `SAFH` container, header finalizer | `persistent-flag-banks.md:428-436`, `:1337` |
| 01 Script VM | the verb handlers (`setmapjumpgroupflag`, `settalknpcname`, `istreasureflag`, `settrapresource`, `btlAtelOpenTreasureMessage`, …), `00267E10` pop, script image header `+0x6C`, storage-class chooser `00265770` | `persistent-flag-banks.md:376`, `:736-748`; `CONTRACT-persistent-flag-banks.md:451-453` |
| 02 Resource | kind-9 requests `0032E620`, size tables `0032E400`, path arrays | `persistent-flag-banks.md:1213-1277` |
| 03 World/Area/Field | field id hub, `FieldData_GetVariable0`'s block, field record table S-11, `00378540` | `persistent-flag-banks.md:219-230`; `event-memory-at-actor-bind.md:54-62` |
| 04 Actor | NPC-name dictionary (`003EAC10`, `npcdic.bin`), actor bind, `.ard` class row `+0x52` | `persistent-flag-banks.md:640`; `event-memory-at-actor-bind.md:196-197` |
| 07 Combat Action / 08 Formula / 10 Status | trap gather and apply (`BattleFormula_ResolveTargetResult`/`ApplyTargetResult`), message table `0046A9D0`, action rows 246–261 and recipes, statuses | `persistent-flag-banks.md:710-783` |
| RNG | `RNG_MT19937_NextU32_Thunk` `00379CD0` | `persistent-flag-banks.md:670`, `:792`, `:1377` |
| 16 UI | map screens consume Primary gate words `+0xE`/`+0x12`; Clan Primer menus | `persistent-flag-banks.md:380`; `event-memory-at-actor-bind.md:206` |
| 18 Audio | `+0x1534` override reader | `persistent-flag-banks.md:456-460` |
| 15 Input | input arbitration calls the gate | `persistent-flag-banks.md:424-426` |
| 13 Items / 20 Achievements | loot grant, achievement counter beside the defeat count | `persistent-flag-banks.md:1361`; `event-memory-at-actor-bind.md:205` |

---

## 2. Gaps

### 2.1 Gaps the pages state themselves (still open, or live-only)

| # | gap | cite |
|---|---|---|
| S-1 | **No live observation exists** for any claim; the readiness gate needs one. Three cheap checks named (read `0x02164280 + 0x200 + 0x14F4`; step `0032A8A0` with `0x400B`; confirm the gap is zero on a fresh game). | `CONTRACT-persistent-flag-banks.md:34-35`, `:351-352`, `:364-370`, `:489` |
| S-2 | `FULL-SUBSYSTEM` parity not covered: 11 of 17 entries differentially tested; outstanding: the gate (schedule arm needs authored data), `00377970`, `00379160`, `002EF2D0`, `00377440`, `002EF2B0`. Mutation verdict `INCOMPLETE` (one `INVALID`). | `CONTRACT-persistent-flag-banks.md:580-585`, `:375-378` |
| S-3 | `STATE-TRANSITION`, `INTEGRATION`, `TIMING`, `PRESENTATION` untested; need the running game. | `CONTRACT-persistent-flag-banks.md:549-550`, `:614-615` |
| S-4 | Single-threaded access "not proven". | `CONTRACT-persistent-flag-banks.md:205-206` |
| S-5 | Which map jump each `Primary` id controls — per-script reading not done. | `persistent-flag-banks.md:376`, `:378`, `:391` |
| S-6 | The `shutoral` (airship) reading of `Bank64A`/`64B` is "an inference from a romanised identifier". | `persistent-flag-banks.md:392-393`, `:496` |
| S-7 | `+0x1535`: "its name rests only on the verb's catalog name"; a reader through a block copy or computed offset "would not be seen". | `persistent-flag-banks.md:463-464`, `:482-484` |
| S-8 | Census limit on every absence claim: a payload pointer stored and reloaded, or a bulk `memcpy`, would not be seen. | `persistent-flag-banks.md:358-359`, `:1063-1067` |
| S-9 | Whether a `0xFFFF` caller reads false as "never" or "absent" "is not asserted". | `persistent-flag-banks.md:235-236` |
| S-10 | `FUN_00266D10` not read in full; no menu path traced to it; so the "new game" trigger is not established. | `persistent-flag-banks.md:1325-1326` |
| S-11 | `0016D6A0`, `00253A80`, `00238A80` (the chain around `002EF650`) unread. | `persistent-flag-banks.md:1327-1328` |
| S-12 | Whether `00378540` registers exactly five tables (943 B, read at two sites only). | `persistent-flag-banks.md:1329-1330` |
| S-13 | The eight header bytes before each list's count are untouched by both consumers (meaning not needed, but not stated). | `persistent-flag-banks.md:1331-1332` |
| S-14 | What the two actor payload buffers hold. | `event-memory-at-actor-bind.md:234-235` |
| S-15 | The third byte of a `02ADD100` record — "still open". | `event-memory-at-actor-bind.md:236-238` |
| S-16 | Whether the two bind-time lookups concern the same kind of event. | `event-memory-at-actor-bind.md:256-257` |
| S-17 | The bestiary exclusion list's meaning ("marks, story bosses") "is not read here"; the Clan Primer functions "were not re-read". | `event-memory-at-actor-bind.md:208-210`, `:331-332` |
| S-18 | "Which achievements they serve is not read" (the two achievement bodies reading `FieldData_GetVariable0`). | `CONTRACT-persistent-flag-banks.md:626-628` |
| S-19 | `01F83530` base staying zero is "supported, not proven". | `persistent-flag-banks.md:521-524` |
| S-20 | The map-data gate words with bit 15 set: "a form this page does not read". | `persistent-flag-banks.md:380` |

### 2.2 Structural gaps found while mapping (a port needs these and no 14 page states them)

| # | gap | what shows it |
|---|---|---|
| G-1 | **The threshold schedule's input variable is not located.** `FieldData_GetVariable0` is given only as pseudo-C over `g_fieldFlags` and `g_fieldVariables`; neither global's address, writer, the meaning of `g_fieldFlags` bit 0, nor when the field variable block is loaded or replaced is stated. Without it the schedule (and every bit-14 gate id) cannot be driven. | `persistent-flag-banks.md:219-230` |
| G-2 | **Publish vs reset ordering.** `00379160` silently does nothing when `02ADD0D0` is null (`persistent-flag-banks.md:1133-1135`), and the pointer is published by an area-table request and cleared by `00377CC0` (`:1200-1202`). No page states that the list is guaranteed to be loaded when `002EF2D0` runs on a new game. | `persistent-flag-banks.md:1092-1114`, `:1195-1202` |
| G-3 | **Treasure record and per-chest mask.** The record's size and bytes `+0x01`..`+0x07`, `+0x0A` are not stated; the per-chest mask `002FB430(table, fieldId, index, 0)` — its table, layout and lifetime — is named only; the bit-6 "random 1..N" draw formula and which `+0x14`/`+0x16` applies when are given in prose without a body. | `persistent-flag-banks.md:870-883`, `:893-894` |
| G-4 | **Treasure flag half vs script check.** The native chest writer sets a `Bank512Low` bit (`persistent-flag-banks.md:836`, `:874`), while the shipped script check `istreasureflag` reads the **High** half and the Low-half verb `istreasurebattleflag` has "no shipped use" (`:369`). No page reconciles which half a chest's flag lives in from the script's side. | `persistent-flag-banks.md:369`, `:836` |
| G-5 | **Bank512 VM handlers are not mapped to accessors.** Two query handlers and four setter handlers are listed without saying which is Low/High or set/clear. | `persistent-flag-banks.md:612` |
| G-6 | **Trap trigger cadence and caller.** `002F8060`'s result "returns to `BattleUnit_RunPeriodicCombatMaintenance`", but the call edge, its frequency and which units are polled are not stated; the 342-byte body `002FA740` calls (`persistent-flag-banks.md:1353`), `002FB560` (marker placement), `003EB720` (marker slots) and the `0046A9D0` message poster are named only. | `persistent-flag-banks.md:750-754`, `:766-767`, `:1353` |
| G-7 | **Trap table header source.** The reference format (`tag = bits 24–26`) is given, but the "six-way base chooser `00265770`" and the `msp` region are delegated to 01 / 25 pages; `002641B0(0, 0)` ("manager slot 0's script image") is not described. | `persistent-flag-banks.md:736-741` |
| G-8 | **Save header use of `gate(0x400B)`.** Which header field receives the result, and what the two other `0x400B` call sites are, is not stated. | `persistent-flag-banks.md:415-418`, `:1008` |
| G-9 | **Gate caller list.** Of 32 callers, about six are named; the call sites that produce the observed id vocabulary are not listed per caller. A port of the gate itself does not need them; a port of its consumers does. | `persistent-flag-banks.md:238-244`, `:424`, `:1057-1059` |
| G-10 | **Event-memory record bodies.** `00576300` ("event-memory record body", caller `00570080`) and `00570080` ("event-memory body") are placed by call signature only; what they read and write is not described, so "event memory" as a whole is not covered by the page that bears the name. | `event-memory-at-actor-bind.md:336-338`, `:387-393` |
| G-11 | **Statistics counter.** `00316A50` has "about twenty kinds"; the kinds, storage and reset are not stated, though the page says a hunt is "a flag convention plus a counter". | `event-memory-at-actor-bind.md:183-185`, `:190` |
| G-12 | **Bestiary `00315D50` return contract.** The defeat counter runs "only when `00315D50(id)` returns −1"; the page states the listed case returns a word from `01EED130` but not that the unlisted case returns −1, nor the chain's three hops. | `event-memory-at-actor-bind.md:205`, `:208-210` |
| G-13 | **Bestiary base.** "save payload `+0xB404`" vs the persistent payload being `0x1538` bytes: the base `+0xB404` is relative to (beyond "block `+0x3404` of what `002536A0` returns") is not reconciled in 14. | `event-memory-at-actor-bind.md:198-199`; `persistent-flag-banks.md:1119` |
| G-14 | **`00377B60` fallback address is malformed**: "returns the `02EB1F0` fallback string" — seven hex digits where every other address has eight; the lookup's table global is not named. | `persistent-flag-banks.md:1399-1403` |
| G-15 | **Hunts.** Declared authored (`event-memory-at-actor-bind.md:190`), but no page names the flags or counters any hunt uses; a port of hunt behaviour needs the script reading, which is not done. | `event-memory-at-actor-bind.md:158-192` |
| G-16 | **`+0x1062`/`+0x1063` cluster** (29 access sites; bit `0x40` gates the music override) is in the payload this folder maps but its other bits are not stated. | `persistent-flag-banks.md:344`; `CONTRACT-persistent-flag-banks.md:86` |
