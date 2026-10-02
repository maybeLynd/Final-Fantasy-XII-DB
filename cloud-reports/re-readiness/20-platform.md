# Reconstruction readiness — `FFXII TZA/20-Platform-Online-Achievements/`

| | |
|---|---|
| Stream | R (reconstruction readiness), per [`docs/cloud-briefs/re-readiness.md`](../../docs/cloud-briefs/re-readiness.md) |
| Board task | `OPUS-CLOUD-R-READINESS-20-1002` |
| Date | 2026-10-02 |
| Snapshot | this repo's text snapshot at `34861cfd` only; no executable, Ghidra or live game was used |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every item quotes or paraphrases a page and gives its location. Text is quoted as the snapshot has it; several of these pages are being edited by other lanes. |

**Counts:** 4 pages read in full (`README.md` + 3 system pages, 1,548 lines), 7 `.tsv` files checked for layout and
counts only, 2 `.py` member headers read · **45 entry-point rows** mapped (21 Steam lifecycle, 4 award path, 20 counter
family) · **14** self-stated open gaps + **24** structural gaps · **38 contradictions**: **15 value-changing** (9 with a
favoured side settled by a dated correction: C-V3, C-V4, C-V5, C-V6, C-V7, C-V9, C-V10, C-V14, C-V15; 6 with no
favoured side: C-V1, C-V2, C-V8, C-V11, C-V12, C-V13; all 15 "page-text only - needs local check") and **23 stale /
banner** · 9 cross-checks found consistent · **Rating: MOSTLY** overall (counter update/store READY statically;
Steam path MOSTLY; evaluator modes 4–7 NOT YET because of C-V1).

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

---

## 2. Gaps

### 2.1 Gaps the pages state themselves (still open, or live-only)

| # | gap, as the page puts it | cite |
|---|---|---|
| O-1 | "Whether any caller re-issues an award that I-2 drops. The periodic checker `00315E90` is the likely candidate, and it is not read for that here." | `STM:161-162` |
| O-2 | By-id table keys: "What the keys name is not read." | `STM:168` |
| O-3 | "Still open: what `0020CCC0` does after registration." | `STM:170` |
| O-4 | "What `[02EA5368]+0x69` means (the pump's early return)." | `STM:171` |
| O-5 | "Anything live." (STM); "Evidence class: isolated original-code. Live capture: still absent." and "any runtime observation \| — \| none \| UNKNOWN" (CTR) | `STM:172`, `CTR:251`, `CTR:410`, `CTR:456` |
| O-6 | The two live checks requested from ASTRA (save block after a counter achievement; `kind == 2` held at `0x7FFF`) | `CTR:335-344` |
| O-7 | "§11 Observable behaviour — Not established." | `CTR:215-218` |
| O-8 | Award ordering: "whether it is intended is not established here" | `CTR:89` |
| O-9 | The debug menu's second number: "The format suggests the second number is a target; that is **not established**" | `CTR:60-61` (`CTR:356` and `CAT:663-667` since identify `003165C0` as the threshold lookup; the box is not updated) |
| O-10 | `SteamController_PollState`: "not read (`SD-163`)" | `CAT:165` (status line `CAT:4` says SD-163 is answered in the register; the answer is not on this page — C-S16) |
| O-11 | `ISteamUserStats` slot names "rest on the public SDK's vtable order (tier 6), not on a string in the image" | `CAT:729-730`, `CAT:353` |
| O-12 | Whether class-3 units are excluded from the bestiary tally: "Which units carry it is `SD-160`" | `CAT:339` |
| O-13 | HORIDASHI: "Which of them the achievement `ACH_SPECIAL_HORIDASHI` counts is not tied in the image" | `CAT:263-265` (partly stale — C-S13; the mode-1 value 53375 is still unexplained, G-18) |
| O-14 | `.\GameData\code_steam.txt` "a **Steam-specific authored data file**, not previously recorded" — nothing more | `CAT:543` |

### 2.2 Structural gaps found while mapping (a port needs these and no 20 page states them)

| # | missing | why a port needs it | where the gap shows |
|---|---|---|---|
| G-1 | **Which evaluator arm each mode 4–7 reaches.** The two pages decode the eight-arm table at `00316098` differently (C-V1). | Decides whether Cartographer (id 15, mode 5), Scrivener (id 16, mode 6) and the ten `MONSTER` marks (ids 20–29, mode 7) can ever be awarded, and by which test. | `CAT:662` vs `CTR:354-363` |
| G-2 | **The updater's trigger-path test and fire body.** CTR §7 says mode 0 fires "unconditionally"; CAT and CTR's own claim table say it compares (C-V2). The comparison operator (`>=`? `==`?), which source wins when `003165C0` and `+0x04` are both non-zero, and what `Fire(id)` in the §12 formula does (it is never defined) are not stated. | Ids 5, 8, 18 (Wayfarer, Exemplar, The Unrelenting) and 19 (Collector) are kind 0 and fire only here. | `CTR:139-143`, `CTR:229-230`, `CAT:578-588`, `CTR:407-408` |
| G-3 | **What calls the periodic sweep `00316930`, and how often.** | Decides when evaluator-only achievements (modes 2, 5, 6, 7) fire, and whether "awarded on the *next* update" (`CTR:86-87`) is ever corrected sooner. | `CAT:297`, `CAT:331`, `CAT:662` (caller never named) |
| G-4 | Descriptor byte `+0x03`; the per-id values of `+0x01` (the offset byte) as a table. | A port that builds its own descriptor table needs all eight bytes; the offsets are only implied by the listing order of `CTR:445-449`. | `CAT:566` (fields `+0x00`, `+0x02`, `+0x04` only), `CTR:100-102` |
| G-5 | How `00316760` produces the values for ids 5 and 8 ("special-cases 5 and 8 at `00316787`/`0031678C`"). | Wayfarer (50,000 steps) and Exemplar (average level 50) compare against these values. | `CAT:693-694` |
| G-6 | The exploration predicate's bitmap: "the handbook's hop-1 bitmap (`[022C2550]+8`, bit `n` at `+4+(n>>3)`)" — whether `+8` is the blob position before hop 1 (the member TSV says hop 1 lands at `+0x3C`) is not stated, nor the bitmap's length. `00255120` / `00255060` semantics are 03's. | Cartographer's test. | `CAT:662`, `CAT:170` |
| G-7 | The bestiary-completion predicate's keyed-record format (type 0 / type 1, the `word & 0xFFF` key at `[022C2550]`). | Scrivener's test. | `CAT:662`, `CAT:169` |
| G-8 | Mode 2's "packed word pair `[lo,hi)`": which half is `lo`; the meaning of `00309EC0`'s answer. The three shipped values are printed only as signed dwords (`810627072`, `1075331072`, `-1071661038`). | Ids 9, 10, 12 (Runeweaver, Jack-of-All-Trades, High Summoner). | `CTR:358`, `CAT:617-620`, `CAT:662` |
| G-9 | What the load-time normaliser `00316810` changes. | A loaded save must be normalised the same way; the member TSV shows it reads descriptor bytes `+0x00`/`+0x01` six times. | `CAT:331` |
| G-10 | The new-game initial contents of save `+0x3844`..`+0x386B` (and who writes them). | A fresh game's counters and award bits. | not stated on any of the four pages |
| G-11 | The kind-7 flag bitmap at `+0x3848`: who calls `00315B50`/`003157E7` with `cl == 7`, and what the 30 flags mean. | Reversible save state with no named consumer. | `CTR:377-386` |
| G-12 | `003154B0`'s callers, and what categories 0–4 (count/base tables at `0x00D10640`/`0x00D10630`, bitset `+0x32CC`) and 6 represent. | A query into achievement state (category 7) with no named consumer. | `CAT:169` |
| G-13 | The 1101 handler in full: whether the achieved count is recounted during the refresh (it is "reset"), what happens to entry 0's local byte (only entries 1…n−1 are refreshed), what a non-matching game id or `result != 1` does, and whether `+0x10`/`+0x90` are overwritten (C-V12). | Session state after receipt. | `STM:104-109`, `CAT:288-289` |
| G-14 | Start-up step 1: what the context's `+0x18` is and what sets it before `007980A0` ("If the context's `+0x18` is already set, skip to step 3"). | Whether `SteamAPI_Init` can be skipped. | `STM:59-60` |
| G-15 | Who calls `008653B0` and `0020CD80` (and when), and who reads the listener's `+0x80` / `+0x88`. | Shutdown and connection-lifecycle behaviour. | `CAT:289`, `STM:121-124` |
| G-16 | How `startscene` arguments map to the by-id table's `{key1, key2}` (34,125 `startscene` rows in the member census, no page maps them). | Which story scenes award entries 31–38. | `STM:99-100`, `STM:163-168` |
| G-17 | The amounts some feeders pass: counter 17's `(byte [+0x1C2] - byte [+0x88]) x word [[+0xE78]] + word [[+0xE70]]` (fields not described); counter 18's value from `0028F0C0` (also stored at block `+0x7C78`); counter 13's "row index" (how it lands at or above the mode-3 bias `0xE2`). | The counters' inputs. | `CAT:331`, `CAT:318-319`, `CAT:316-317`, `CTR:185-187` |
| G-18 | Counter 19 (Collector, mode 1, threshold 53375) fires when `0056D370`'s "record's word `+8`" equals 53375 on a purchase; what that record and value are is not stated. | Collector's condition. | `CAT:319-320`, `CAT:331`, `CTR:145` |
| G-19 | `008632B0`'s return value when the manager is null, and whether any caller uses `0020CE60`'s 1 / 0. | Caller behaviour. | `STM:91`, `STM:94-98` |
| G-20 | "`007A0C60` matches the Steam language against `japanese`, `english`, `french` and the rest (this page's `Language` finding)" — the page has no `Language` section; the result's consumer is not stated. | Locale selection. | `CAT:288` |
| G-21 | `code_steam.txt`'s contents and reader. | Authored Steam data. | `CAT:543` |
| G-22 | `00315390` (one of the "twenty achievement-counter bodies", `CAT:288`) appears in the unlinked `achievement-state-accesses.tsv` reading the `+0x3844` route at `base+0x24` (`+0x3868`, counter 17); CAT's displacement-scan list (`CAT:331`) does not name it. Pointer only. | A possible extra reader of counter 17. | `CAT:331`; member TSV row `00315390 … 003153A4 0x24 r` |
| G-23 | What `003162E0` and `00316440` decide before calling `008632B0` (the TSV shows `00316440` reading `+0x3845`). | Two award callers with no stated condition. | `STM:89-90`, `STM:192` |
| G-24 | Thread and frame relation between gameplay counter updates and the window pump. | I-2's "lost award" window depends on when 1101 arrives relative to the first awards. | `STM:84-85`, `STM:126-130` |

---

## 3. Contradictions (statements a re-implementer would have to choose between)

Each item quotes both sides with `page:line`. **Value-changing** items (3.1) would change what a port computes or
stores; every one is **page-text only - needs local check** (this session cannot see the executable). A favoured side
is named only where a dated correction on the pages settles it, and even then the byte check is still owed. **Stale /
banner** items (3.2) change no value: an "open / not read" claim another page or later section answers, a banner that
disagrees with front matter, or a corrected claim repeated unstruck.

### 3.1 Value-changing — page-text only - needs local check

**C-V1 — Which arm of `00315E90`'s jump table each mode 4–7 reaches.** *No favoured side.*

- CAT (dated "ANSWERED 2026-09-17 (FABLE)"): "**1, 4** → nothing (arms at the return label); … **5** → `003160C0()`:
  every navigation-map entry flagged … is visited …; **6** → `003161A0()`: every id below `0x200` satisfies its
  bestiary requirement …; **7** → the threshold (0–9) indexes the `u16` id list at the handbook's third hop
  (`00316014`–`00316037`), and that monster's defeat count `00315420(id)` must be above 0." (`CAT:662`). Also "the
  exploration check, achievement mode 5" (`CAT:170`) and "the checker's mode-7 arm (`00315FFA`) indexes the
  descriptor's threshold (0–9) into the `u16` monster-id list" (`CAT:297`).
- CTR (dated "CLOSED 2026-09-23 (SWE2-CONTRACT): all eight arms decoded"): "| 1 | `0031607D` | **no-op** — the epilogue
  itself |", "| 4 | `00315FDC` | predicate `003160C0()` → award if true |", "| 5 | `00315FEB` | predicate `003161A0()` →
  award if true |", "| 6 | `00315FFA` | walks the `022C2550` word-offset chain (same shape as `003165C0`), bounds-checks
  descriptor `+4` against `word[rax+2]`, fetches `word[rcx + rdx*2 + 4]` and calls `00315420` on it — award if `> 0` |",
  "| 7 | `0031607D` | **no-op** — shares mode 1's epilogue |" (`CTR:357-363`).
- The two agree on modes 0, 2 and 3 (arms `00315F19`, `00315F46`, `00315F87`: `CTR:356-359`, `CAT:244`, `CAT:696`) and
  on the bodies behind the arms; they disagree by one position for modes 4–7. The descriptor table uses modes 5 (id
  15), 6 (id 16) and 7 (ids 20–29) and no mode 4 (`CAT:608-622`). Under CTR's table, the ten `MONSTER` marks (mode 7)
  never fire, Cartographer (mode 5) runs the bestiary predicate and Scrivener (mode 6) runs the monster-list arm.
  Neither page strikes the other; CAT's later reconciliations (2026-09-30, `CAT:308`) keep mode 7 = monster list, and
  the member file `menuhandbook-achievement-records.tsv` labels descriptors 20–29 "mode 7" with "`003165C0 /
  00315FFA`" as the walker. **Local check:** the eight dwords at `00316098` and the index arithmetic before
  `00315F0C`–`00315F17`.

**C-V2 — The updater's trigger path, mode 0: unconditional fire or a threshold compare.** *No favoured side* (the
weight of the pages is on "compare", but nothing strikes CTR §7).

- CTR §7: "| `0` | fire unconditionally through `003165C0` (`00316A99` → `00316AF4`) |" (`CTR:141`); §12: "`if (d->mode
  == 0)                    Fire(id);`" (`CTR:229`); §15a: "Of the nineteen trigger descriptors, one is mode 1 … and three
  are mode 0" (`CTR:145`).
- CTR's own claim table: "when the id has no counter, submode 0 fires on a threshold and submode 1 on an exact match |
  `00316AF4` against `00316AA6`. Executed at, below and above the threshold" and "the fire lookup supplies the threshold
  when it is non-zero | `00316AF8` then `00316B01`" (`CTR:407-408`); CAT: "mode `0` compares the amount against the
  threshold (or against a value from `003165C0` when that returns non-zero)" (`CAT:578-579`); CAT (read 2026-09-30,
  SWE2-DATA): "The updater's kind-0 arm compares the value `0028F0C0` passes … against the override 50 and fires on it"
  (`CAT:696`).
- Affects ids 5, 8, 18 (the three mode-0 trigger descriptors). **Local check:** `00316A99`–`00316B01`.

**C-V3 — CTR §12 reproduction formula: the store target, and the missing evaluate.** *Favoured: the 2026-09-12
correction* (`00316BF0` stores; `00315E90` evaluates first).

- CTR §7/§12: "`Store(id, result)                      00316BBD -> 00315E90`" (`CTR:182`); "`Store(id, v);
  /* 00315E90 */`" (`CTR:245`); the formula calls no evaluate step.
- CTR box, "**CORRECTED 2026-09-12 (`OPUS-ACHIEVE-ISOLATED`)**": "The store is **`00316BF0`**" (`CTR:78`); "`00316BC1 call
  00315E90`, then `00316BCC call 00316BF0` with the new value" (`CTR:83-84`); claim row "the store is 00316BF0, not
  00315E90" (`CTR:409`).
- The formula also omits the trigger path's award-bit set and notify (`CAT:582-587`) behind `Fire(id)`.

**C-V4 — Negative-sum clamp on the accumulate path.** *Favoured: clamp to 0 on kinds 2 and 4, none on the fall-through*
(the 2026-09-12 run, "What the run established that reading had put in the wrong row", `CTR:285`, re-checked
2026-09-30 by `pf_steam_checks.py` C, `CAT:714`).

- CTR §12: "`if (d->kind == 2) v = (amount > 0x7FFF     - v) ? 0x7FFF     : v + amount;`" / "`else if (d->kind == 4) v =
  (amount > 0x7FFFFFFF - v) ? 0x7FFFFFFF : v + amount;`" — no lower clamp (`CTR:237-238`); CAT §10: "| `4` | add, clamped
  to **`0x7FFFFFFF`** |" against "| `2` | add, clamped to **`0x7FFF`**, and clamped **up to 0** if the result goes
  negative |" (`CAT:598-599`).
- CTR: "Kinds 2 and 4 reach `add ebx, edi / jns` and clamp a negative sum to zero; the fall-through arm adds and does
  not." (`CTR:293-294`); claim row "a sum that goes negative is clamped to zero on kinds 2 and 4 but NOT on the
  fall-through" (`CTR:405`); CAT: "the updater cannot, because its kind-4 arm clamps a negative sum to 0" (`CAT:714`);
  "kind-4 sums never go below 0" (`CAT:357`).

**C-V5 — `003165C0`'s hop count.** *Favoured: four* (dated 2026-09-23 correction).

- CTR SWE2-EC7-26 (2026-09-18): "resolves the `022C2550` root through three word-relative offset hops" (`CTR:472-473`).
- CTR §14 (2026-09-23): "the walk is **four** word-relative hops … The EC7 note says "three" hops; the verified count is
  four (`003165DA`/`003165E3`/`003165EC`/`003165F5`)" (`CTR:366-370`); CAT: "four hops in all" (`CAT:664`).

**C-V6 — The id bound "before anything else".** *Favoured: CTR's 2026-09-25 correction* (evaluator `< 0x1F`; update and
store `< 0x1E`).

- CTR §4 lead sentence, unstruck: "**The id is bounded at 30 before anything else happens**, in all three entry points"
  (`CTR:106`).
- Same paragraph, "*Corrected 2026-09-25*": "The evaluator `00315E90`'s own first instruction bounds the id at **31**"
  (`CTR:108-110`); EXP-089 box: "`00315E90  cmp cl, 0x1f / jae     evaluate  accepts id < 0x1F   (0..30)`" (`CTR:154`);
  and "`003166F0` and `00316BF0` both call `002536A0` at their very first instruction, *before* any range or kind test"
  (`CTR:298-299`), which contradicts "before anything else happens" for the read and the store.

**C-V7 — The set of updater feeders.** *Favoured: the 2026-09-30 corrections* (three direct sites plus six thunk
sites; ids 0–4, 6, 7, 11, 13, 14, 17, 18, 19).

- CAT AB-7 (2026-09-12), unstruck: "The updater's seven callers fire indices 0–4, 6, 7, 11, 13, 18 and 19 only"
  (`CAT:292-293`); "`00316A50` is reached directly from three sites and through one thunk (`00253770`) from four more"
  (`CAT:309-310`); "So kills, steals, magicks, technicks, gil in, gil out and licence points are the counters this
  build advances natively" (`CAT:320-321`).
- CAT (corrected 2026-09-30, FABLE): "these are the three DIRECT sites; six more reach `00316A50` by tail jump through
  the thunk `00253770`, and two of them pass 17" (`CAT:331`); OPUS 2026-09-30: "the same driver's sale arm passes
  **14** with the quantity sold" (`CAT:331`, also `CAT:320`).

**C-V8 — The amount `BattleUnit_ProcessDefeatRewardsAndLoot` passes for counter 11.** *No favoured side.*

- CAT (2026-09-12): "fires **11** with the licence points awarded (`00312496`)" (`CAT:312-313`).
- CAT (2026-09-18): "passes 11 with the 99,999-clamped total it keeps at `+0x190` (`00312475`–`00312496`)" (`CAT:331`).
- A per-award delta and a running total give different kind-4 sums under mode 0 (`CAT:610-618`, id 11 is kind 4 mode
  0). **Local check:** `00312475`–`00312496`.

**C-V9 — Whether the ten `MONSTER` marks have a producer.** *Favoured: a producer exists* (CAT's dated "REOPENED AND
ANSWERED 2026-09-17 (FABLE) - the 2026-09-12 closure was wrong"), **subject to C-V1**.

- CAT, unstruck: "so the ten mode-7 descriptors have **no producer in the shipped executable**" (`CAT:294`); "a
  reconstruction needs only the fact that nothing ever raises them" (`CAT:295-296`); "the ten mode-7 descriptors have
  no producer in the image — either the Steam side unlocks them from stats, or they are dead" (`CAT:321-322`).
- CAT: "**REOPENED AND ANSWERED 2026-09-17 (FABLE) - the 2026-09-12 closure was wrong: a producer exists, and it is not
  the updater.**" (`CAT:297`). If CTR's arm table (C-V1) is right, mode 7 is a no-op and the 2026-09-12 conclusion
  returns by another route.

**C-V10 — Whether descriptor `+0x04` is read outside mode 1, and its type for mode 2.** *Favoured: it is read (modes 0,
2, and the monster-list arm), as a `u16` pair for mode 2* (CAT "ANSWERED 2026-09-17", CTR "CLOSED 2026-09-23").

- CTR §3: "`threshold` is compared **only on mode 1**" (`CTR:102`); CTR §7: "the rest carry modes 2, 5, 6 and 7 and
  therefore **never fire through this function**. That is why their `+0x04` values look arbitrary: nothing reads them."
  (`CTR:145-147`); CAT §10: "The type is **not established** and no reading is asserted here." (`CAT:651-656`).
- CTR §14: mode 0 "threshold = `003165C0(id)`, falling back to descriptor `+4` when 0"; mode 2 "descriptor `+4` is a
  packed word pair `[lo,hi)`" (`CTR:356-358`); CAT: "**2** → the threshold is two `u16`s" (`CAT:662`); mode-7/6 arm
  indexes the list with it (`CAT:662`, `CTR:362`).

**C-V11 — The extent of by-id row 6's walk.** *No favoured side.*

- STM: "when the matched row is index 6, `0020CB50` also walks entry offsets `0x3168`–`0x3C90`, which is entries
  **31–37**" (`STM:166`).
- `0x3168 / 0x198 = 31` and `0x3C90 / 0x198 = 38` exactly, so "`0x3168`–`0x3C90`" names entries 31–38 if the end is
  inclusive; STM's falsification table: "the seven by-id rows map to entries 31–38" (`STM:216`) against the row list
  "31, 32, 34, 35, 36, 37 and 38" (`STM:164-165`). Whether entry 38 is in the walk (it is row 6's own entry) and whether
  the walk includes 33 (not a by-id row; awarded by `slm_a01`, `CAT:751`) both follow from the bound. **Local check:**
  the loop bound in `0020CB50`.

**C-V12 — What the 1101 handler does with `"name"` / `"desc"`.** *No favoured side.*

- STM: "copies the display attributes `"name"` / `"desc"` (slot `+0x60`)" (`STM:106-107`); entry layout "`+0x10` display
  name (`0x80`), `+0x90` description (`0x100`)" (`STM:54`).
- CAT AB-6 census: "`0020C940` prints `name` and `desc` through `OutputDebugStringA`" (`CAT:288`); "`0020C940`
  `OnUserStatsReceived` (the `name` / `desc` debug print)" (`CAT:289`); and the title at `+0x10` is described as static
  "inline Steam title" read from the file image (`CAT:108-115`).
- Whether `+0x10`/`+0x90` are overwritten at runtime. **Local check:** `0020C940` after the slot `+0x60` call.

**C-V13 — How many descriptors accumulate.** *No dated correction; the page's own table counts eleven.*

- CAT AB-1: "the twelve accumulating descriptors carry 0 (index 13's `16` is a mode-3 bit index)" (`CAT:243`).
- CAT §10: "**Eleven entries carry a numeric type** (`2` ×7, `4` ×4): indices 0–4, 6, 7, 11, 13, 14, 17" (`CAT:627`);
  CTR §15a: "**So 11 of 30 ids carry a counter and 19 do not.**" (`CTR:442`); the table `CAT:608-622` shows eleven.

**C-V14 — How many Trial Mode award sites are live.** *Favoured: 9 live per index* (CAT, "corrected 2026-10-01,
SWE2-DATA, `SD-162`").

- STM: "**39** `ACH_TRIAL_MODE_50` (*Judge Magister*) and **40** `ACH_TRIAL_MODE_100` (*Imperator*) are passed by the
  Trial Mode stage scripts `tri_*`, 900 sites each (100 per locale)" (`STM:190`).
- CAT: "~~900~~ 900 code copies (100 files × 9 languages); 9 live, `tri_j05` only" and "9 live, `tri_t05` only"
  (`CAT:749-750`); "18 live sites, 1,782 statically excluded" (`CAT:761`). The member census (no live column) agrees
  with the 900/900/9 totals only.

**C-V15 — Which achievements have a stored counter.** *Favoured: the AB-2 binding (2026-09-17) and the record read
(2026-09-18)* — `ACH_COUNT_STEP` and `ACH_COUNT_CHAIN` have no save counter; `ACH_MASTER_LICENSE` and
`ACH_COMPLETE_YUGOU` do.

- CAT §1: "Eleven achievements are pure counters — steps walked, gil earned, gil spent, enemies killed, items stolen,
  spells cast, techniques used, chains built." (`CAT:42-44`); §10: "**Eleven entries carry a numeric type** … Section 2
  lists **eleven `ACH_COUNT_*` cumulative counters.**" (`CAT:627-628`); §6: "Those totals exist in memory and ~~almost
  certainly~~ in the save payload" (`CAT:229-231`).
- CAT: "Ids 5, 8 and 18 carry `kind = 0` - no save field" (`CAT:693`); the counter-id list "5 `STEP` … 18
  `COUNT_CHAIN`" (`CAT:268`); member `achievement-descriptors.tsv` slots 6/7 (counter ids 18/5). Numeric-type ids 11 and
  13 are `ACH_MASTER_LICENSE` and `ACH_COMPLETE_YUGOU` (`CAT:268`, `CAT:330`).

### 3.2 Stale "open / not read" claims, corrected claims repeated unstruck, and banner disagreements

| # | stale side (quoted) | answering / correcting side (quoted) |
|---|---|---|
| C-S1 | README: "**PARTIAL, tier 2.**" (`README.md:14`); CAT body: "**PARTIAL.** … The 59 platform functions are unnamed and none was read." (`CAT:33-34`) | CAT front matter: "status: DOCUMENTED — every register row it names is closed (owner re-status 2026-09-30, OPUS)" (`CAT:4`); "the achievement path's code is read" (`CAT:174`) |
| C-S2 | README: "in seven families" (`README.md:14-15`) | CAT: "41 identifiers in eight families" (`CAT:48`); "The ~~seven-family~~ eight-family taxonomy *(corrected 2026-09-30 …)*" (`CAT:346`) |
| C-S3 | README: "plus 23 Steam interface versions" (`README.md:15`) | CAT: "The binary requests **21** named Steam interfaces … (corrected 2026-09-02, §9" (`CAT:128`); "~~23~~ 21 Steam interface versions" (`CAT:349`) |
| C-S4 | CAT §4 grammar: "`TRIAL          2   MODE_50 / MODE_100          (Zodiac Age only)`" (`CAT:188`) | "~~`ACH_TRIAL_MODE_50` and `_100` are **Zodiac Age-specific**~~ … *(Struck 2026-09-30, SWE2-DATA: a claim about the 2006 release, which nothing in this image or corpus can check.*" (`CAT:90-91`) |
| C-S5 | "What the 58 unnamed Platform-owned functions do." (`CAT:287`); "**59 functions carry the `PlatformOnlineAchievements` owner**, and all but `SteamController_PollState` are unnamed" (`CAT:172-173`, i.e. 58 unnamed) | "the unnamed set is 59 today" (`CAT:288`); member TSV has 59 rows; `README.md:8` "Functions \| 59" |
| C-S6 | AB-6 census: "`0020CD30` a 77-byte body with nothing to name it" (`CAT:288`) | STM (2026-09-25): "Create the manager, `0020CD30` (`0079812D`). It allocates `0x80` bytes and calls `0020C730` …" (`STM:62-63`) |
| C-S7 | `00315E90` named as "the counter updater `00315E90`" (`CAT:288`), "**The store path takes the id only**: `00315E90`" (`CAT:331`), "`00315E90`'s store dispatches on the mode byte" (`CTR:33`), "the periodic checker `00315E90`" (`STM:89-90`, `STM:161`, `STM:194`), "Downstream: the Steam User Stats interface, reached through the store's mode arms." (`CTR:128`) | CTR box (CORRECTED 2026-09-12): "`00315E90` is not the store" (`CTR:63`), the updater is `00316A50` (`CTR:48`); the periodic sweep is `00316930` (`CAT:662`). The behaviour each side describes agrees (id only, no store); only the names are stale |
| C-S8 | CTR scope note: "`00315E90`'s store dispatches … and `003165C0` walks a relative-offset chain at `022C2550`; **neither is specified** — they are named and bounded, and each arm's behaviour is open." (`CTR:33-35`); debug-menu box: "`003165C0` stays unspecified, as the scope note says" (`CTR:61`) | CTR §14: "**CLOSED 2026-09-23 (SWE2-CONTRACT): all eight arms decoded.**" (`CTR:349`) and "`003165C0`'s chain walk … **CLOSED 2026-09-23**" (`CTR:364-365`) |
| C-S9 | "The correct test is whether any code path reaches the accessor, and that requires reading the platform functions — none of which were read here." (`CAT:367-368`) | "*Superseded 2026-09-26 …: **AB-3** was answered on 2026-09-17.*" (`CAT:370`); "**ANSWERED 2026-09-17 (FABLE): only linked.**" (`CAT:281`) |
| C-S10 | §9 Related: "story bits, which overlap in subject with `ACH_EVENT_*` but are not yet connected to it" (`CAT:436`) | "**AB-4** *(answered 2026-09-12, FABLE: separate state.*" (`CAT:223`); "**AB-4 ANSWERED 2026-09-12 (FABLE): separate state, inside the save image.**" (`CAT:282`) |
| C-S11 | §9 Related: "where the counters most likely live" (`CAT:437`) | "**AB-5** — ANSWERED 2026-09-10: inside the save image at payload `+0x8000`" (`CAT:283-286`) |
| C-S12 | "*Half answered 2026-09-15 (FABLE) — `HORIDASHI` is named by the shipped data; `YUGOU` is not.*" (`CAT:246`); "**YUGOU stays open.**" (`CAT:266`) | "***ANSWERED 2026-09-17 (FABLE): YUGOU is the achievement the player sees as *Mist Walker*" (`CAT:268`); "**BOTH ANSWERED — `AB-2` is closed**" (`CAT:104`) |
| C-S13 | "Which of them the achievement `ACH_SPECIAL_HORIDASHI` counts is not tied in the image: the achievement names have no index binding" (`CAT:263-265`) | the record array binds every tag to a counter id, "19 `HORIDASHI`" (`CAT:268`); member TSV slot 17 `counter_id 19` |
| C-S14 | "nothing in the image ties the name to an index" (`CAT:327-328`); "no string in this table ties an index to a name, and **this document should not treat the correspondence as a mapping until one is found.**" (`CAT:634-636`) | "***NARROWED 2026-09-17 (FABLE): the tag-to-index tie is now proved**" (`CAT:330`); `CAT:268` |
| C-S15 | "**So whatever decides that a counter has "reached" its goal is not here.** That closes AB-1 as posed and reopens it as *"who compares a counter against a target"*." (`CAT:646-647`) | "*(Corrected 2026-09-30, SWE2-DATA: AB-1 is answered. The targets are the `menuhandbook.bin` overrides tabled in §10, compared locally by the checker.)*" (`CAT:196`); `CAT:244` |
| C-S16 | Key-address row: "`SteamController_PollState` \| 1,124 B \| not read (`SD-163`)" (`CAT:165`) | status line: "since answered in the register: … SD-163 (the controller poll)" (`CAT:4`) — the answer itself is not on the page |
| C-S17 | status line: "AB-6, AB-8 and UQ-272 SUPERSEDED" (`CAT:4`); AB-8 row: "the register row is ~~WITHDRAWN~~ **SUPERSEDED** 2026-09-26" (`CAT:323`) | same row: "The register word is pending with the register owner, so SUPERSEDED is not the current summary." (`CAT:323`) |
| C-S18 | CAT front matter: "`evidence_tier: 2`" (`CAT:6`), "`last_reviewed: 2026-09-02`" (`CAT:19`), "`last_pass: 2026-09-02`" (`CAT:22`) | body corrections dated up to 2026-10-01 (`CAT:749`); "The award path is now tier 1" (`CAT:377`) |
| C-S19 | CTR front matter: "`entries: ["00316A50", "003166F0", "00315E90", "003165C0"]`" (`CTR:9`) | CTR §2 lists the store `00316BF0` as an interface entry ("**Missing from this contract until 2026-09-12**", `CTR:51`) |
| C-S20 | CAT: "Id 31 is dead through the engine" (`CAT:697-698`, the following clause struck); member `menuhandbook-achievement-records.tsv` last comment: "id 31 is out of range for every caller (checker id<0x1F, updater id<0x1E) — dead data." | "**Corrected 2026-09-29 (FABLE, GI-2):** no achievement check reads its override, but the value is read: the Sky Pirate's Den layout `00572920` calls `003165C0`" (`CAT:699-700`) |
| C-S21 | CTR §13: "the eleven counters' widths and offsets in §3 can be confirmed" (`CTR:337-338`) | §3 (`CTR:93-102`) gives no per-counter widths or offsets; they are in §15a (`CTR:436-454`) |
| C-S22 | §5 call chain: "`-> (unread) platform code sets the matching ACH_* identifier`" (`CAT:208`) | "*(Corrected 2026-09-30, SWE2-DATA: the `(unread)` step is read.*" (`CAT:215`) — annotated, not struck |
| C-S23 | STM §9: "Whether any caller re-issues an award that I-2 drops. The periodic checker `00315E90` is the likely candidate, and it is not read for that here." (`STM:161-162`) | CAT reads the checker and the sweep (`CAT:662`) and CTR states the checker "**returns if it is already set**" (`CTR:68-69`); neither page draws the I-2 conclusion, so O-1 stays open — listed here only because "not read" is stale |

### 3.3 Checked and found consistent (not contradictions)

- Record addresses: `01DFE410 + 9×0x198 = 01DFF268` (`CAT:331`, slot 9 `ACH_COUNT_SCORE`) and `+ 19×0x198 = 01E00258`
  (`CAT:110`); both match the member TSV.
- Award-id table vs record slots: counter 13 → `0x13` (slot 19, YUGOU), 17 → `0x09` (slot 9), 11 → `0x0D` (slot 13,
  MASTER_LICENSE), 20 → `0x16` (slot 22, MONSTER01), 25 → `0x14` (slot 20, MONSTER06) (`CAT:608-622` against the member
  TSV); no award id is 0, consistent with I-4 / W4 (`STM:139-141`, `STM:216`).
- Table addresses: `0x120000 + 0x1F6098 = 0x316098` (`CTR:34` vs `CTR:50`); `0x120000 + 0xBF0550 = 0xD10550 =
  0xD10460 + 30×8` (`CTR:351-352`, `CTR:255`, `CTR:158-160`, `CAT:567`).
- Save block: `4 + 4 + 0x20 = 40` bytes (`CTR:98`, `CTR:384-385`); counter 17 at `+0x3868 = +0x384C + 0x1C`
  (`CAT:331`, `CTR:448`); id 11 at `+0x384C+0x10` (`CAT:713`, `CTR:448`).
- Callback ids: `0x44D`/`0x44E`/`0x44F` = 1101/1102/1103 and `0x14B` = 331 (`CAT:289`, `STM:65-70`); `0x91640` = 595520
  (`STM:71`).
- Imports: nine `steam_api64.dll` imports (`CAT:389-397`, `STM:14-15`); one `RunCallbacks` site (`CAT:522`, `STM:217`).
- Handbook: hop 3 at `+0xDC`, hop 4 at `+0xF8`, record end `0xF8 + 8 + 0x38 = 0x138` (`CAT:299-300`, `CAT:669-671`,
  member TSV).
- Script census totals 900 / 900 / 9 (`STM:190`, `CAT:749-751`, member TSV).
- Mode-3 evaluator default 16 / override 8 for id 13 (`CTR:359`, `CAT:662`, `CAT:696-697`).

---

## 4. Rating

**MOSTLY** overall — named gaps, with one structural hole in the evaluator.

| part | rating | why |
|---|---|---|
| Counter update / read / store (`00316A50` accumulate path, `003166F0`, `00316BF0`), descriptor and award-id tables, save block layout | **READY** (statically) | the tables are fully dumped (`CAT:606-622`, `CTR:436-454`); widths, saturation, mode-3 bitset, the two bounds and the evaluate-before-store order are stated and were run under Unicorn with "0 mismatches" (`CTR:261`). Use the favoured sides of C-V3, C-V4, C-V6 rather than the CTR §12 formula as written. New-game contents (G-10) and the load normaliser (G-9) are missing. |
| Updater trigger path (kind 0: ids 5, 8, 18, 19, …) | **MOSTLY** | C-V2 (unconditional vs compare) and G-2 (operator, fire body), G-5 (ids 5 and 8), G-18 (53375) |
| Evaluator `00315E90` modes 0–3, handbook overrides and monster list | **MOSTLY** | arms 0/2/3 agree across pages and the `menuhandbook.bin` values are decoded (`CAT:669-690`, `CAT:299-308`); G-8 (mode-2 pair order) |
| Evaluator modes 4–7 and the sweep | **NOT YET** | the two pages disagree on which arm each mode reaches (C-V1), which decides whether Cartographer, Scrivener and the ten `MONSTER` marks can fire; the sweep's scheduler is not stated (G-3); predicate record formats are summaries only (G-6, G-7) |
| Steam lifecycle, pump, award path, receipt handlers | **MOSTLY** | STM states the order, the null-manager rule and invariants I-1…I-6 with falsification (`STM:114-148`, `STM:205-221`); open: `0020CCC0` (O-3), `[02EA5368]+0x69` (O-4), by-id keys and the `startscene` mapping (O-2, G-16), the row-6 walk end (C-V11), the 1101 details (C-V12, G-13), listener/shutdown wiring (G-15) |
| Script award verbs | **MOSTLY** | indices and live sites are stated (`CAT:745-761`); the `startscene` → by-id mapping is not (G-16) |
| Networking / matchmaking | **READY** (as a negative) | "fetched once … never called in the shipped executable" (`CAT:281`); nothing to port beyond the fetch |
