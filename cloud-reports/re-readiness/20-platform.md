# Reconstruction readiness — `FFXII TZA/20-Platform-Online-Achievements/`

| | |
|---|---|
| Stream | R (reconstruction readiness), per [`docs/cloud-briefs/re-readiness.md`](../../docs/cloud-briefs/re-readiness.md) |
| Board task | `OPUS-CLOUD-R-READINESS-20-1002` |
| Date | 2026-10-02 |
| Snapshot | this repo's text snapshot at `34861cfd` only; no executable, Ghidra or live game was used |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every item quotes or paraphrases a page and gives its location. Text is quoted as the snapshot has it; several of these pages are being edited by other lanes. |

**Counts:** _(filled in with the rating section)_

Citation form: `page:line`, where `page` is the file name inside `FFXII TZA/20-Platform-Online-Achievements/`. The
pages, with the short names used below:

- `README.md` (28 lines) — **README**
- `steam-integration-and-achievement-catalogue.md` (812 lines) — **CAT**
- `CONTRACT-achievement-counters.md` (487 lines) — **CTR**
- `CONTRACT-steam-integration-subsystem.md` (221 lines) — **STM**

"Not stated" means none of these four pages says it. Where another category's page is the only place a point is made,
the pointer is given as the 20 page cites it; that other page was not audited for this report.

## Pages read

| page | status as the page states it |
|---|---|
| README | category index; `Functions \| 59` (`README.md:8`); lists one system, CAT, as "**PARTIAL, tier 2.** All **41 achievement identifiers** in the developers' own naming, in seven families, plus 23 Steam interface versions" (`README.md:13-15`); does not list either contract |
| CAT | `status: DOCUMENTED — every register row it names is closed (owner re-status 2026-09-30, OPUS)` (`CAT:4`); `evidence_tier: 2` (`CAT:6`); `last_reviewed: 2026-09-02` (`CAT:19`); `audit.passes: 1`, `last_pass: 2026-09-02` (`CAT:21-22`); `reopened_count: 1` (`CAT:25`); body banner "**PARTIAL.**" (`CAT:33`) |
| CTR | `readiness: BEHAVIORALLY UNDERSTOOD` (`CTR:6`); `confidence: PROVEN` (`CTR:7`); `entries: ["00316A50", "003166F0", "00315E90", "003165C0"]` (`CTR:9`); `last_reviewed: 2026-09-11` (`CTR:17`); `audit.passes: 1`, `last_pass: 2026-09-12` (`CTR:19-20`); `crossref_clean: false` (`CTR:22`) |
| STM | `readiness: CONTRACT READY   # the lifecycle, the award path and the failure behaviour are STATIC; nothing here was observed live` (`STM:6`); `confidence: PROVEN` (`STM:7`); 11 `entries` (`STM:10`); `last_reviewed: 2026-09-29` (`STM:20`); `audit.passes: 1`, `last_pass_kind: falsification` (`STM:23-25`) |

Member files, checked for layout and counts only (no item below rests on a member file alone):

| file | what was checked |
|---|---|
| `members/achievement-descriptors.tsv` | 4 comment lines, header `slot record counter_id tag title other_strings`, **41 data rows** (slots 0-40), records `01DFE410` + slot×`0x198`. Agrees with `CAT:107-112` (slot 19 = `{13, ACH_COMPLETE_YUGOU, "Mist Walker"}`, slot 0 and slot 40) and with the counter-id list at `CAT:268`. Slots 0 and 1 both carry `counter_id 0`. |
| `members/menuhandbook-achievement-records.tsv` | 11 `monster_list` rows (slots 0-10) and 14 `override_id` rows; values agree with `CAT:299-304` and the override table `CAT:675-690`. Its comment calls the hop walker "`003165C0 / 00315FFA`" and labels descriptors 20-29 "mode 7" (see C-V1). Its last comment still reads "id 31 ... — dead data" (see C-S20). |
| `members/platform-unnamed-functions.tsv` | header `entry size imports named_callees strings` and **59 data rows** — agrees with `CAT:288` ("59 today") and `README.md:8` |
| `members/script-award-verb-census.tsv` | header `file pc verb opcode status args_push_order`, 35,934 data rows: **34,125 `startscene`** and **1,809 `unkCall_5ad`** (900 × `PUSHII:39`, 900 × `PUSHII:40`, 9 × `PUSHII:33`) — agrees with `STM:190` and `CAT:749-751`. It has no live/dead column; the "9 live" figure of `CAT:749-750` is not derivable from it. |
| `achievement-descriptor-accesses.tsv` (16 rows), `achievement-state-accesses.tsv` (8 rows), `image-backed-state-block-accesses.tsv` (32 rows) | **No page in the folder links these three files.** The state file has a row for `00315390` reading `base+0x24` from the `+0x3844` route (i.e. `+0x3868`, counter 17's dword per `CAT:331`); CAT's displacement-scan list at `CAT:331` does not name `00315390`. Pointer only (see G-22). |
| `members/*.py` | header comments only; not run |

---

## 1. Interface

The folder documents two layers that meet at one function, `008632B0`:

- **The achievement counter family** (CTR, CAT §10): a 30-entry authored descriptor table in `.rdata` decides, per
  counter id, whether a gameplay event is a trigger or an increment, the counter's width and save offset, and which
  completion test runs. State lives in a 40-byte block of the save image.
- **Steam integration** (STM, CAT §2/§7/§8b): one start-up handshake, one per-window-pump callback service, a 41-record
  achievement manager, and the award path to `SetAchievement` / `StoreStats`. Without Steam, awards are local only
  and the by-index path is off.

### 1.1 Entry points (functions, with their callers)

#### Steam lifecycle

| function | role as stated | callers as stated | cite |
|---|---|---|---|
| `007980A0` | application start-up; owns the Steam handshake order | "the application start-up" (CoreRuntimeScheduling); caller not stated | `STM:57-75`, `STM:181-182` |
| `001F3E10` | "the once-only `Init` wrapper", zeroes the context's twenty slots and tail-calls `001F3AE0`; also named "init callback" of the context | reached through `SteamInternal_ContextInit` (IAT `008C3190`) | `STM:52`, `CAT:281` |
| `001F3AE0` (809 B) | SDK context fetcher, fills the interface slots | `001F3E10` | `CAT:166`, `CAT:281`, `CAT:288` |
| `0020CD30` | creates the manager (`0x80` B), calls `0020C730`, stores to `01F83450` | `007980A0` at `0079812D`, only after a successful `SteamAPI_Init` | `STM:62-63`, `STM:116-117` |
| `0020C730` | registers callbacks 1101/1102/1103 on `CSteamAchievements`; then one user-stats call (slot `+0x48`, "the stats request") and `0020CCC0` | `0020CD30` | `STM:62-69`, `CAT:289` |
| `008655E0` | registers callback 331 `GameOverlayActivated` on `CSteamManager` | start-up step 3 (`STM:69-70`) | `STM:69-70`, `CAT:289` |
| `008653B0` | registers `SteamCallbacksListener` for `SteamServersConnected_t` (`0x65`), `SteamServersDisconnected_t` (`0x67`), `SteamServerConnectFailure_t` (`0x66`), `SteamShutdown_t` (`0x2C0`) | **not stated** | `CAT:289` |
| `0020CD80` | the manager's destructor: frees the `0x80` bytes, stores 0 to `01F83450` (`0020CDED`); unregisters | **not stated** | `STM:121-124`, `CAT:289` |
| `00865490`, `00865660` | unregister the other callback objects | not stated | `CAT:288-289` |
| `007A3110` | **the pump**: slot 0 of Phyre `PWindowWin32Base` / `PWindow` vtables; early return 9 if `[02EA5368]+0x69`; else `SteamAPI_RunCallbacks` (`007A312E`) then `InputBackend_UpdateResolvedDeviceState` | no direct caller; "Phyre's window loop drives it" | `STM:77-85`, `STM:187-188` |
| `0020C940` | 1101 `OnUserStatsReceived` | Steam via the pump | `STM:104-109`, `CAT:167`, `CAT:289` |
| `0020CB20` | 1102 `OnUserStatsStored` — logs only | Steam via the pump | `STM:112`, `CAT:289` |
| `0020C8C0` | 1103 `OnUserAchievementStored` | Steam via the pump | `STM:110-111`, `CAT:289` |
| `0020CE10` | sends entry 0's award; tests `+0x18` only | the 1103 handler `0020C8C0` (its one caller) | `STM:111`, `STM:134-137` |
| `00865560`, `00865570`, `00865590` | `OnServersConnected`; `OnServersDisconnected` **and** `OnServerConnectFailure` (one body: `inc [this+0x88]`, `[this+0x80] = 1`); `OnSteamShutdown` ("clears both") | Steam via the pump | `CAT:289` |
| `008655A0` | `OnGameOverlayActivated` (a debug print) | Steam via the pump | `CAT:288-289` |
| `00865540`, `00865550` | shared `CCallback` vtable slots 0/1 (`Run` forms) | Steam | `CAT:289` |
| `0020C8A0`, `0020C8B0`, `0053DD10`, `001F2880`, `0016EE70`, `00314F20` | `GetCallbackSizeBytes` slot-2 stubs | Steam | `CAT:289` |
| `007A0C60` | matches the Steam language against `japanese`, `english`, `french`, … | not stated | `CAT:288` |
| `007A1CD0` `SteamController_PollState` (1,124 B) | controller poll | not stated | `CAT:155-159`, `CAT:165` |
| `0079FA00`, `00862A40` | build a save-folder path (`SHGetFolderPathW` …) | not stated | `CAT:288` |

#### Award path

| function | role as stated | callers as stated | cite |
|---|---|---|---|
| `008632B0(index)` (44 B) | by-index award thunk: fetches manager via `0020CE00` (`mov rax, [01F83450]`), returns if null, tail-jumps `0020CE60(manager, index)` | `00316A50` (twice), `00315E90`, `003162E0`, `00316440`, `00352250` | `STM:89-92`, `CAT:718-721` |
| `0020CE60` (137 B) | unlock body: if `+0x190` set return 1 (no Steam call); else set `+0x190 = 1`, `+0x194 = 0`; if manager `+0x18`, `SetAchievement(entry+0x08)` (slot `+0x38`) then tail-jump `StoreStats` (slot `+0x50`); else return 0 | `008632B0` | `STM:93-98`, `CAT:722-732` |
| `00352250` | handler of script verb `unkCall_5ad` (call `0x5AD`, one int); tail-jumps `008632B0` | script VM | `STM:190`, `CAT:745`, `CAT:765` |
| `0034C9A0` → `00863240` → `0020CB50` (334 B) | by-id award: handler of `startscene` (call `0x11B`); table at `00906290` of seven 12-byte rows `{key1, key2, entry}`; same `SetAchievement`/`StoreStats` pair; row 6 also walks entries 31–37 | script VM | `STM:99-100`, `STM:163-168`, `STM:196` |

#### Counter family

| function | role as stated | callers as stated | cite |
|---|---|---|---|
| `00316A50` `AchievementCounter_UpdateAndMaybeFire(cl=id, edx=amount)` (411 B) | id bound `< 0x1E`; trigger path (`kind == 0`) or accumulate path; calls evaluate `00315E90` (`00316BC1`) then store `00316BF0` (`00316BCC`) | **direct:** `GameState_SetGil` (6/7, `00254EF8`, `00254F00`), `BattleUnit_ProcessDefeatRewardsAndLoot` (11, `00312496`), `0056D370` (19 on purchase, 14 on sale, `0056D4D2`); **through thunk `00253770`:** `00317090` (17, `003170D3`), `002E2380` (17, from `003403E0` = verb `0x4DC` `addclanpoint`), `0028F0C0` (18), `003112F0` (3), `003171C0` (4), `00305640` (13/2/1/0) | `CTR:48`, `CTR:83-84`, `CAT:561`, `CAT:331` |
| `00315E90(cl=id)` | evaluate-and-award: bound `cl < 0x1F`; tests the award bit for id `< 0x1E`; dispatches on descriptor `+0x02` through the eight-arm table at `00316098`; shared award tail `00316045`; writes no counter, never reads `edx` | `00316A50` at `00316BC1`; the periodic sweep `00316930` for ids 0–29 | `CTR:50`, `CTR:63-79`, `CTR:349-363`, `CAT:331`, `CAT:662` |
| `00316930` | periodic re-check loop over ids 0..29 (`00316A36`–`00316A43`) | **not stated** | `CAT:297`, `CAT:331`, `CAT:662` |
| `00316BF0(cl=id, edx=value)` | the store: validates id, reads `kind`, writes a word (kind 2) or dword (kind 4) | `00316A50` at `00316BCC` | `CTR:51`, `CTR:77-79` |
| `003166F0(cl=id)` | the read: returns the counter in `eax`, `-1` on rejection; calls `002536A0` first; tests `>= 0x1F` (`0031670B`) and `>= 0x1E` (`00316711`) | `00316A50` (`00316B55`); `00316760`; `DebugMenu_Render` (ids 0–4, 11) | `CTR:49`, `CTR:54-61`, `CTR:189-192`, `CTR:297-300` |
| `00316760` | the evaluator's counter source: calls `003166F0`; special-cases ids 5 and 8 (`00316787`/`0031678C`); returns `-1` for id 18 | `00315E90` arms | `CTR:84-85`, `CAT:693-696` |
| `003165C0(cl=id)` (172 B) | handbook override lookup: four word-relative hops from `[022C2550]+8`, rejects `cl >= 0x20`, needs bit `id` of `R+4`, returns `dword[R + 8 + 4×rank]`; 0 on any miss | `00315E90` arms 0 and 3; `00316A50` trigger path; `DebugMenu_Render`; Sky Pirate's Den layout `00572920` through thunk `003165B0` | `CTR:364-370`, `CAT:663-667`, `CAT:699-705` |
| `003158B0` | `menuhandbook.bin` loader (kind 7, id `0xC8`): frees the previous copy, stores the new one at `022C2550` | not stated | `CAT:663` |
| `003160C0` | exploration predicate (calls `WorldTransition_GetActiveOrPendingFieldId`, `00255120`, `00255060`) | `00315E90` (arm number disputed, C-V1) | `CAT:170`, `CAT:662`, `CTR:360` |
| `003161A0` | bestiary-completion predicate | `00315E90` (arm number disputed, C-V1) | `CAT:662`, `CTR:361` |
| `00315420` | bestiary defeat count: save `+0x3404` byte minus one | `00315E90` monster arm(s) | `CAT:297`, `CAT:662` |
| `00315820` | counts a defeat in the bestiary tally at save `+0x3404` | `003171C0` via thunk `00253750` | `CAT:333-339` |
| `003154B0` (367 B) | `(category, index)` condition query (categories `< 5`, 6, 7) | not stated | `CAT:169` |
| `00315B50` (`cl==7` arm) / `003157E7` (`cl==7` arm) | write / read the kind-7 flag bitmap at `+0x3848` | not stated | `CTR:377-386` |
| `00316810` | load-time normaliser | `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` (`00584398`) | `CAT:331` |
| `00316C60` | developer console's 99,999 max helper | max-LP arm `00305A00` (`00305A96`) | `CAT:331`, `CAT:806-812` |
| `003162E0`, `00316440` | callers of `008632B0`; `003162E0` and `00316760` call the slot getter `00282DD0` (`*(0209AC30) + 0x408 + id×0xC0`) | `00316440` is called from `00305640` | `STM:89-90`, `STM:192`, `CTR:480-487` |
| `00309EC0` `BattleEncodedId_DispatchQueryMode0Value` | the mode-2 arm's per-id query (`0xFFFF` in → `-1` out) | `00315E90` mode-2 arm; also CombatAI `003032E4` | `CAT:662`, `CAT:736-741` |
| `00253970` | points `020927C0` at the active save buffer `+0x8200` | `FUN_0022a0b0` start-up sequence | `CAT:284-285`, `CAT:767` |
| `002536A0` | returns `*(020927C0)`, the save block | the counter accessors | `CAT:715-717` |

### 1.2 Inputs and outputs (data read and written, with record layouts)

#### Descriptor table `00D10460` (`.rdata`, read-only, 30 × 8 B)

| offset | field | cite |
|---|---|---|
| `+0x00` | `kind` = counter width in bytes on the accumulate path (0 = no counter / trigger, 2 = signed word, 4 = signed dword) | `CTR:100-101`, `CTR:403`, `CAT:566` |
| `+0x01` | the counter's byte offset inside the `+0x384C` block | `CTR:101`, `CTR:129-131` |
| `+0x02` | `mode` | `CTR:101-102`, `CAT:566` |
| `+0x03` | **not stated** | — |
| `+0x04` | `threshold` (dword; meaning depends on mode — see C-V10) | `CAT:566`, `CTR:356-362` |

Full per-index `kind`/`mode`/`threshold`/award-id dump at `CAT:606-622`. The `+0x01` offset byte is not tabled per id; the
packed layout is given at `CTR:445-449` (seven `int16` for ids 0–4, 13, 14 at `+0x00`..`+0x0C`, two alignment bytes,
four `int32` for ids 11, 6, 7, 17 at `+0x10`..`+0x1C`). The id-to-slot order inside each run is implied by listing
order; `CAT:713` places id 11 at `+0x10` and `CAT:331` places id 17 at `+0x3868` (= `+0x384C+0x1C`).

#### Award-id table `00D10550` (`.rdata`, 30 × dword)

"one dword per entry, passed to the notifier" (`CAT:567`); "The thirty ids are distinct and span `0x01`–`0x1E`"
(`CAT:569`); the evaluator's award tail reads it as `[r15 + r14*4 + 0xBF0550]` (`CTR:351-352`). Values at `CAT:608-622`.

#### Achievement manager (heap, `0x80` B, pointer at `01F83450`)

`+0x00` game id (compared with each callback's `+0x00`), `+0x08` entry array (stride `0x198`), `+0x10` count (41),
`+0x14` achieved count, `+0x18` "stats received" flag (`STM:53`).

#### Achievement record (static array at `01DFE410`, 41 × `0x198` B)

`+0x00` qword counter id, `+0x08` tag pointer (API name), `+0x10` inline Steam title / display name (`0x80`), `+0x90`
description (`0x100`), `+0x190` achieved byte, `+0x194` a dword cleared on award (`STM:54`, `CAT:108-112`, `CAT:268`).
Slot-by-slot table: `members/achievement-descriptors.tsv` (cited at `CAT:268`, `CTR:375`, `STM:160`).

#### By-id table `00906290`

Seven 12-byte rows `{key1, key2, entry}`, entries 31, 32, 34, 35, 36, 37, 38; "What the keys name is not read"
(`STM:164-168`).

#### Save-image achievement block (`AchievementState`, 40 B)

`002536A0` returns `*(020927C0)` = active save buffer `+0x8200` = payload `+0x8000`, so `+0x3844` is payload `+0xB844`
(`CAT:715-717`).

| block offset | size | content | writers | cite |
|---|---|---|---|---|
| `+0x3844` | 4 B | award ("fired") bitmap, ids 0–29, `bts`-only | `00316A50` trigger path (`00316AC3`–`00316ADB`); evaluator award tail `00316045` | `CTR:98`, `CTR:350-351`, `CAT:583-591` |
| `+0x3848` | 4 B | kind-7 flag bitmap, `bts`/`btr` | `00315B50` `cl==7` arm | `CTR:98`, `CTR:377-386` |
| `+0x384C` | `0x20` | counter block (11 counters, layout above) | `00316BF0` | `CTR:98`, `CTR:431-454` |

Other save offsets the pages use: `+0x3404` bestiary bytes (`CAT:297`, `CAT:662`); `+0x32CC` bitset of the `002536A0`
singleton (category query, `CAT:169`); `+0x7C78` (value `0028F0C0` also stores, `CAT:318-319`).

#### `menuhandbook.bin` (kind 7, id `0xC8`, `us` copy 312 bytes) at `[022C2550]`

Hop chain from blob `+8`, `pos += u16[pos]`, four hops: hop 1 → `+0x3C`, hop 2 → `+0x7C`, hop 3 → `+0xDC`, hop 4 → `+0xF8`
(member TSV header, agreeing with `CAT:299-300`, `CAT:669`). Hop 3: `u16 count = 11` at `+2`, eleven `u16` bestiary ids
at `+4` (`CAT:299-304`). Hop 4: `u16 0x0040, u16 0x000E`, mask `0x800661FF` at `+4`, fourteen dwords at `+8`
(`CAT:669-673`); override table `CAT:675-690`. The mode-5 arm's "hop-1 bitmap" (`CAT:662`) — its exact location is
ambiguous (G-6).

#### Steam SDK context `01DFE0D0`

Twenty interface slots; `+0x08` user, `+0x20` matchmaking, `+0x28` user stats, `+0x38` matchmaking servers, `+0x40`
networking, `+0x68` controller; `+0x18` and `+0x30` read but unnamed (`CAT:272-279`, `CAT:281`). STM says "If the
context's `+0x18` is already set, skip to step 3" (`STM:59-60`).

#### Outputs

- To Steam: `SetAchievement(entry.name)` (slot `+0x38`), `StoreStats` (slot `+0x50`), `GetAchievement` (slot `+0x30`),
  display-attribute read (slot `+0x60`), stats request (slot `+0x48`) — slot names rest on SDK vtable order, "tier 6"
  (`CAT:729-730`, `STM:69`, `STM:96-97`, `STM:106-107`).
- To the save image: the 40-byte block above.
- Process exit: `exit(1)` if `SteamAPI_RestartAppIfNecessary(0x91640)` returns true (`STM:71-72`).
- Debug output: `OutputDebugStringA` in `0020C940` (`CAT:288`); the strings at `CAT:535-539`.

### 1.3 State (globals and objects, with lifetime)

| state | lifetime as stated | initial value | cite |
|---|---|---|---|
| Steam context `01DFE0D0` | static record; zeroed by `001F3E10` once, filled by `001F3AE0` | zeroed slots | `CAT:281` |
| manager pointer `01F83450` | set by `0020CD30` after a successful `SteamAPI_Init`; set to 0 by `0020CD80` | null without Steam | `STM:116-124` |
| manager `+0x18` stats-received | set by the 1101 handler on a matching game id with result 1 | not stated (presumably 0 after allocation — **not stated**) | `STM:104-105` |
| manager `+0x14` achieved count | reset by 1101, incremented by 1103 | not stated | `STM:105`, `STM:110` |
| records `01DFE410` `+0x190`/`+0x194` | per session: set by the unlock body, overwritten by 1101 from Steam for entries 1…n−1 | static image value not stated | `STM:94-95`, `STM:106-107` |
| descriptor / award-id / by-id tables | `.rdata`, never written | image | `CTR:121`, `CTR:196-197` |
| save block `+0x3844`..`+0x386B` | save image; copied in by the load paths; normalised by `00316810` at load | **new-game value not stated** | `CAT:331`, `CAT:714` |
| `[022C2550]` handbook blob | replaced by `003158B0` (frees the previous copy) | when it is first loaded: not stated | `CAT:663` |
| `[02EA5368]+0x69` | the pump's early-return byte | "What `[02EA5368]+0x69` means" is open | `STM:80`, `STM:171` |
| `SteamCallbacksListener` `+0x80` / `+0x88` | set/incremented on disconnect/connect-failure, cleared on shutdown | not stated | `CAT:289` |

### 1.4 Order (what runs when, and what triggers it)

1. **Start-up (`007980A0`)**: `SteamInternal_ContextInit(01DFE0D0)` (`00798116`) → if context `+0x18` already set skip
   to 3 → `SteamAPI_Init` (`00798123`; on failure go to 4) → `0020CD30` (manager, three callbacks, stats request,
   `0020CCC0`) → `008655E0` (callback 331) → always `SteamAPI_RestartAppIfNecessary(0x91640)` (`0079813C`), `exit(1)` on
   true (`0079814B`). "Init runs **before** the relaunch check, the reverse of the usual SDK order" (`STM:57-75`). The
   same body runs the settings loaders `001DE050`/`001DED50` (`STM:198`). Where `008653B0` and the `0022A0B0` start-up
   sequence (`00253970`, handbook loader) fall relative to these steps: not stated.
2. **Every window pump (`007A3110`)**: `SteamAPI_RunCallbacks` then the input backend update, unless `[02EA5368]+0x69`
   (`STM:77-85`). All Steam callbacks run here (I-5, `STM:143-145`). Which thread / how often relative to the game
   frame: "once per window pump, on that thread" — the frame rate of that pump is not stated.
3. **On a counter event**: `00316A50(id, amount)`: bound → trigger path (fires through `008632B0` and sets the award bit)
   or accumulate path: read `003166F0` → add/bitset by kind and mode → evaluate `00315E90` → store `00316BF0`
   (`CTR:83-87`, `CTR:168-170`). "an achievement whose counter crosses its threshold is awarded on the *next* update
   rather than the one that crossed it" (`CTR:86-87`).
4. **Periodic**: `00316930` calls `00315E90` for ids 0–29 (`CAT:662`). What schedules it: **not stated**.
5. **Award**: `008632B0` → `0020CE60`; before 1101 the award is local only and 1101 later overwrites it from Steam
   ("so an award made before the stats arrive is lost unless the game issues it again", I-2, `STM:126-130`).
6. **Receipt**: 1101 → refresh entries 1…n−1, award entry 0 if all others achieved; 1103 → count, award entry 0 at n−1
   through `0020CE10`; 1102 → log (`STM:102-112`).
7. **Save load**: `00316810` from `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` (`CAT:331`).

### 1.5 Dependencies (on other systems)

| system | dependency | cite |
|---|---|---|
| 00 CoreRuntimeScheduling | owns `007980A0`; `0022A0B0` calls `00253970` | `STM:181-182`, `CAT:767` |
| 15 Input | co-scheduled in the pump | `STM:184-185` |
| 22 Phyre | `PWindow` slot 0 drives the pump; Steam Controller is a Phyre input device class | `STM:187-188`, `CAT:544-546` |
| 01 Script VM | `unkCall_5ad` (0x5AD) awards by index; `startscene` (0x11B) awards by id; `addclanpoint` (0x4DC) feeds counter 17; `sethoridashi` (0x2F7) | `STM:190`, `CAT:331`, `CAT:116-120` |
| 25 EBP | the `tri_*`, `slm_a01` scripts that award 39/40/33 | `CAT:747-761` |
| 07/08 Combat | `00305640`, `00312280`, `003112F0`, `003171C0`, `00317090` feed counters; `00316440` called from `00305640` | `STM:192`, `CAT:309-331` |
| 13 Rewards / economy | `GameState_SetGil`, `0056D370`, `00254EE0`, `00312280` | `STM:200-203`, `CAT:311`, `CAT:331` |
| 19 Save | block pointer `020927C0`, load normaliser, payload map | `CAT:282-286`, `CAT:715-717` |
| 16 UI (Handbook) | `menuhandbook.bin` targets and monster list; Sky Pirate's Den reads id 31's override | `CAT:308`, `CAT:667`, `CAT:699-705` |
| 14 Story (bestiary) | `00315820`, `00315420`, save `+0x3404` | `CAT:339`, `CAT:662` |
| 04 Actor | `ActorRuntime_GetClassNibble` from `003171C0`; `0032F240` from `startscene` | `CAT:333-339`, `STM:196` |
| 03 World | `WorldTransition_GetActiveOrPendingFieldId`, `00255120`, `00255060` (exploration predicate) | `CAT:170`, `CAT:662` |
| Presentation (debug menu) | `DebugMenu_Render` reads ids 0–4, 11 | `CTR:54-61` |
| 12 Shops (bazaar) | `sethoridashi` → `0032AB50` | `CAT:116-120`, `CAT:250-252` |
| Steamworks (`steam_api64.dll`) | nine imports (`CAT:389-397`) | `CAT:389-397` |
