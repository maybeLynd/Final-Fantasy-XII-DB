---
system: Steam integration and the achievement catalogue
category: 20-Platform-Online-Achievements
status: DOCUMENTED — every register row it names is closed (owner re-status 2026-09-30, OPUS): SD-160, SD-161, SD-162 and SD-163 ANSWERED; AB-6, AB-8 and UQ-272 SUPERSEDED, their residue moved as those rows state — the unnamed Platform functions (AB-6) and the Trial Mode relation (AB-8): counter 17 is fed natively (FABLE 2026-09-30, accepted by SWE2-AUDIT-SEM); the register word is pending, and AB-6 is SUPERSEDED (2026-09-26, FABLE); the networking question UQ-272 is SUPERSEDED as a duplicate of AB-3 (answered 2026-09-17: fetched, never called); YUGOU (AB-2, Mist Walker) and what modes 5/6/7 test (UQ-273) answered 2026-09-17; UQ-274's id-31 note corrected 2026-09-29 (FABLE, GI-2); since answered in the register: SD-160 (free-target type 3), SD-161 answered 2026-09-30 (no code writes the licence counter negative; a save file's bytes are data), SD-162 (the Trial stage awards' clear path), SD-163 (the controller poll) (status line current 2026-09-30, SWE2-DATA)
owner_layer: PrimaryOwner:PlatformOnlineAchievements
evidence_tier: 2
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 17 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 1
  last_pass: 2026-09-02
  last_pass_state: falsification-pass
  crossref_clean: false
  reopened_count: 1
---

# Steam integration and the achievement catalogue

> The complete list of **41 achievement identifiers** is in the executable, in the developers' own
> naming — and a few of them still carry romanized Japanese from the original internal build.

~~**PARTIAL.**~~ **DOCUMENTED.** *(corrected 2026-10-02, OPUS: the front matter says `status: DOCUMENTED`, owner re-status 2026-09-30)* The identifiers and Steam interface versions are authored strings (tier 2) and are
exact. ~~The 59 platform functions are unnamed and none was read.~~ *(answered: see §7 and §10 — the counter, checker, award and receipt code is read; 2026-10-02, OPUS)*

## 1. What the player sees

The achievement list. All 41 of them, and the game carries their internal names: not the display
titles you see on Steam, but the tags the developers typed — `ACH_EVENT_DEFEAT_VAYNE`,
`ACH_COUNT_STEP`, `ACH_MASTER_LICENSE`.

The list reveals the *shape* of what FFXII tracks about you. Eleven achievements are pure
counters — steps walked, gil earned, gil spent, enemies killed, items stolen, spells cast,
techniques used, chains built. The game is quietly counting all of that, all the time.

## 2. Native mechanism

### The catalogue — 41 identifiers in eight families

**`ACH_COUNT_*` — cumulative counters (11):**

```
ACH_COUNT_CHAIN     ACH_COUNT_FIGHT     ACH_COUNT_GET_GIL   ACH_COUNT_KILL
ACH_COUNT_MAGIC     ACH_COUNT_SCORE     ACH_COUNT_SELL_EVITEM
ACH_COUNT_STEAL     ACH_COUNT_STEP      ACH_COUNT_TECH      ACH_COUNT_USE_GIL
```

Gil is counted **twice and separately** — `GET_GIL` and `USE_GIL` — so earning and spending are
independent running totals.

**`ACH_SPECIAL_*` — a numbered series (11):**

```
ACH_SPECIAL_HORIDASHI
ACH_SPECIAL_MONSTER01 .. ACH_SPECIAL_MONSTER10
```

A flat, zero-padded run of ten plus one outlier.

**`ACH_EVENT_*` — story milestones (8):**

```
ACH_EVENT_FINISH_REX            ACH_EVENT_RETURN_RABANASTRE
ACH_EVENT_FIRST_HUNT            ACH_EVENT_SAVE_ASHE
ACH_EVENT_DEFEAT_VOSSLER        ACH_EVENT_DEFEAT_JUDGE_BERGAN
ACH_EVENT_DEFEAT_CID            ACH_EVENT_DEFEAT_VAYNE
```

These are in rough story order, and every one names a character or place from the game.

**`ACH_MASTER_*` (4), `ACH_COMPLETE_*` (3), `ACH_TRIAL_*` (2), and two single-member families — `ACH_CHAMPION_*` and `ACH_LEVEL_*`:**

```
ACH_MASTER_LICENSE   ACH_MASTER_MAGIC   ACH_MASTER_SUMMON   ACH_MASTER_TECH
ACH_COMPLETE_MAP     ACH_COMPLETE_MONSTER   ACH_COMPLETE_YUGOU
ACH_TRIAL_MODE_50    ACH_TRIAL_MODE_100
ACH_CHAMPION_IVALICE ACH_LEVEL_AVERAGE
```

~~`ACH_TRIAL_MODE_50` and `_100` are **Zodiac Age-specific** — Trial Mode did not exist in the~~
~~original release, so these identifiers postdate the 2006 game.~~ *(Struck 2026-09-30, SWE2-DATA: a claim about the 2006 release, which nothing in this image or corpus can check. What the image shows is that the Trial Mode stage scripts `tri_*` award indices 39 and 40 (the script-award section below).)*

### Romanized Japanese in the identifiers

Two names are not English:

| Identifier | Romanization | Note |
|---|---|---|
| `ACH_SPECIAL_HORIDASHI` | *horidashi* | from 掘り出し(物), "a dug-up find" / bargain |
| `ACH_COMPLETE_YUGOU` | *yūgō* | 融合, "fusion" / "merge" |

These are internal build names that survived localisation. ~~**What each corresponds to in the
shipped game is not established here** — `horidashi` is suggestive of the Bazaar, and `yūgō` of
some completion set, but neither is proven.~~ **BOTH ANSWERED — `AB-2` is closed, and the second
half was answered by a table on this page's own subject that this page had not found.**

- **`YUGOU` is the achievement the player sees as *Mist Walker*.** Re-read from the image here:
  the achievement manager's record array is static at `01DFE410`, **41 records of `0x198`
  bytes**, each `{qword counter id at +0x00, tag pointer at +0x08, inline Steam title at
  +0x10}`. **Record 19 (`01E00258`) is `{13, ACH_COMPLETE_YUGOU, "Mist Walker"}`** — counter
  and title read as bytes, and the tag pointer `00906060` resolves in `.rdata` to the literal
  string `ACH_COMPLETE_YUGOU`. Record 0 is `{0, ACH_CHAMPION_IVALICE, "Champion of Ivalice"}`
  and record 40 `{40, ACH_TRIAL_MODE_100, "Imperator"}`, so the stride and the bound check out
  at both ends. **So the tag never needed a translation: the shipped name is in the binary,
  sixteen bytes after the tag pointer.**
- **`HORIDASHI` is the bazaar's script-unlocked stock** — FABLE, 2026-09-15, cited rather than
  re-derived: the verb `sethoridashi` (`0x2F7`, handler `0034C710` → `0032AB50(good, 1)`) sets
  availability only for bazaar rows whose `+0x14` carries bit 1, and exactly seven of the 128
  rows do — the *Forgotten Grimoire* set, which is exactly the seven ids the shipped scripts
  pass.

Recorded as **AB-2**, now **ANSWERED**; the register row carries both halves.

`ACH_COUNT_SELL_EVITEM` follows the same pattern in abbreviated form.

### Steam interface versions

The binary requests **21** named Steam interfaces at pinned versions (corrected 2026-09-02, §9 — the list below was already complete and exact; only the stated number was wrong):

```
SteamClient017                            STEAMUSERSTATS_INTERFACE_VERSION011
SteamUser019                              STEAMAPPS_INTERFACE_VERSION008
SteamFriends015                           STEAMREMOTESTORAGE_INTERFACE_VERSION014
SteamUtils009                             STEAMSCREENSHOTS_INTERFACE_VERSION003
SteamMatchMaking009                       STEAMHTTP_INTERFACE_VERSION002
SteamMatchMakingServers002                STEAMUNIFIEDMESSAGES_INTERFACE_VERSION001
SteamNetworking005                        STEAMUGC_INTERFACE_VERSION010
SteamController005                        STEAMAPPLIST_INTERFACE_VERSION001
                                          STEAMMUSIC_INTERFACE_VERSION001
                                          STEAMMUSICREMOTE_INTERFACE_VERSION001
                                          STEAMHTMLSURFACE_INTERFACE_VERSION_003
                                          STEAMINVENTORY_INTERFACE_V002
                                          STEAMVIDEO_INTERFACE_V002
```

Plus `steam_api64.dll`, `SteamInternal_ContextInit`, `SteamInternal_CreateInterface`, and **seven
`SteamAPI_*` symbols in total** — `Init`, `RestartAppIfNecessary`, `RunCallbacks`,
`RegisterCallback`, `UnregisterCallback`, `GetHSteamPipe`, `GetHSteamUser`.

**Two of these matter for multiplayer work and must be read carefully.** `SteamNetworking005` and
`SteamMatchMaking009` are present *as interface-version strings*. That is what the standard
Steamworks SDK header emits for every interface it can describe — **their presence does not show
that FFXII uses networking or matchmaking.** It shows the SDK was linked. See **AB-3**.

`SteamController005` is different: the binary also carries the runtime messages
`SteamController Connected` / `SteamController Disconnected` and a named function
`SteamController_PollState` (1,124 bytes), which is real usage. *(Added 2026-09-19, FABLE: where the Steam controller
object is built, and the action set `Global` with its eighteen action names, is on
[how a gamepad becomes a controller object](../15-Input/how-a-gamepad-becomes-a-controller-object.md).)*

## 3. Key addresses

| Address | Name | Size | Verified |
|---|---|---:|---|
| `007A1CD0` | `SteamController_PollState` | 1,124 B | ~~not read~~ (`SD-163`) *(answered: see the register row SD-163, ANSWERED 2026-09-30 — it reads 16 buttons and two sticks and drives the rumble; record `_index/candidates/sd163-steamcontroller-poll-0930/`; 2026-10-02, OPUS)* |
| `001F3AE0` | *(Platform-owned)* | 809 B | ~~not read~~ read 2026-09-17 (FABLE): the SDK context fetcher that fills the twenty interface slots (§7, AB-3) |
| `0020C940` | *(Platform-owned)* | 470 B | ~~not read~~ the 1101 `UserStatsReceived` handler: it refreshes every entry from Steam and awards entry 0 when all others are achieved ([the Steam contract](CONTRACT-steam-integration-subsystem.md) §6; `pf_steam_checks.py` S1) |
| `0020CB50` | *(Platform-owned)* | 334 B | ~~not read~~ the by-id award body ([the Steam contract](CONTRACT-steam-integration-subsystem.md) §5) |
| `003154B0` | *(Platform-owned)* — a **(category, index) condition query**: `category < 5` bounds `index` against the int16 count/base tables at image `0x00D10640`/`0x00D10630` (`003154CF`/`003154E8`) and tests bit `base+index` of the bitset at `+0x32CC` of the `002536A0` singleton (`003154FD`); `category == 6` (`index < 0x200`) walks the keyed-record table at `[022C2550]` matching `word & 0xFFF` (`00315533`–`0031557B`); `category == 7` tests bit `index` (`< 0x1E`) of a second bitset at `+0x3844` (`003155F4`–`00315612`); all other categories return 0 | 367 B | read 2026-09-14 (pass-13 blind read, verified by FRONTIER) |
| `003160C0` | *(Platform-owned)* — calls `WorldTransition_GetActiveOrPendingFieldId` | — | ~~not read~~ the exploration check, achievement mode 5: every flagged navigation map visited (§7, AB-4's FG-1 correction) |

**59 functions carry the `PlatformOnlineAchievements` owner**, and all but
`SteamController_PollState` are unnamed. ~~That is the honest state of this category: the *data* is~~
~~recovered, the *code* is not.~~ *(Corrected 2026-09-30, SWE2-DATA: the achievement path's code is read — the counter updater, checker and award (§10), the SDK context (§7, AB-3), and the receipt handlers ([the Steam contract](CONTRACT-steam-integration-subsystem.md)). The unnamed set's population is AB-6, SUPERSEDED.)*

## 4. Data structures and formulas

```
Achievement identifier grammar
  ACH_<FAMILY>_<SPECIFIC>

  FAMILY      count  meaning
  COUNT         11   cumulative running totals
  SPECIAL       11   HORIDASHI + MONSTER01..MONSTER10
  EVENT          8   story milestones
  MASTER         4   LICENSE / MAGIC / SUMMON / TECH
  COMPLETE       3   MAP / MONSTER / YUGOU
  TRIAL          2   MODE_50 / MODE_100          (Zodiac Age only)   <- corrected 2026-10-02, OPUS - 'Zodiac Age only' is struck in section 2 (2026-09-30): a claim about the 2006 release that this image cannot check
  CHAMPION       1   IVALICE
  LEVEL          1   AVERAGE
                ---
  total         41
```

No formula is asserted. ~~Nothing here states the *threshold* for any counter achievement — those~~
~~numbers were not found in this pass and are **AB-1**.~~ *(Corrected 2026-09-30, SWE2-DATA: AB-1 is answered. The targets are the `menuhandbook.bin` overrides tabled in §10, compared locally by the checker.)*

## 5. Call chain

```
game start
  -> SteamAPI_Init
     -> request SteamClient017, SteamUser019, STEAMUSERSTATS_INTERFACE_VERSION011, ...

gameplay
  -> counters advance (steps, kills, gil, steals, chains, ...)
  -> story milestones reached
     -> (unread) platform code sets the matching ACH_* identifier   <- corrected 2026-10-02, OPUS - read: 00316A50 -> 00315E90 -> 008632B0 -> 0020CE60 (see the note below)

controller
  -> SteamController_PollState (007A1CD0)
     -> "SteamController Connected" / "Disconnected"
```

*(Corrected 2026-09-30, SWE2-DATA: the `(unread)` step is read. A counter event calls the updater `00316A50(index, amount)`, which accumulates or compares and then calls the checker `00315E90`. A met condition sets the fired bit at `+0x3844` and calls the notifier `008632B0`. The notifier records the unlock locally and, once stats are received, calls `SetAchievement` and `StoreStats` (§10, UQ-275). Scripts award by index through `unkCall_5ad` (the script-award section below), and the two receipt handlers award entry 0 (`pf_steam_checks.py` S1, S2).)*

**Upstream:** gameplay systems that move the counters — Rewards for gil, Combat for kills, Movement
for steps.
**Downstream:** the Steam User Stats interface.

**Do not confuse with:** the persistent flag banks. Story achievements and story flags plainly
overlap in subject (`ACH_EVENT_DEFEAT_VAYNE` versus a story bit), ~~but **no connection between them~~
~~has been read**. They may share storage or be entirely independent.~~ **AB-4** *(answered 2026-09-12, FABLE: separate state. Achievements keep their own fired bitmap at block `+0x3844`, §7; reconciled 2026-09-30, SWE2-DATA)*.

## 6. Modding notes

- **41 achievement identifiers, in the developers' own naming**, are in the EXE and can be matched
  against the Steam display names.
- **The counter set tells you what the game tracks continuously**: steps, kills, gil in, gil out,
  steals, magic, techniques, chains, fights, score, loot sales. Those totals exist in memory and
  ~~almost certainly~~ in the save payload *(AB-5: payload `+0x8000`, §7; corrected 2026-09-30, SWE2-DATA)* — a promising lead for mapping more of **V-1**.
- **Gil earned and gil spent are separate counters**, not one net figure.
- **`SteamNetworking005` and `SteamMatchMaking009` being present proves nothing about multiplayer
  support.** They are SDK interface strings. Do not cite them as evidence FFXII has networking.
- **`SteamController` support is real** — a named poll function plus connect/disconnect messages.
- **XIIOnline:** achievements are per-account Steam state and must never be driven from a peer. If a
  shared session advances counters on multiple clients, the same achievement will unlock repeatedly
  or inconsistently. Whatever the project does with progression, achievement writes belong to the
  local player's own Steam session only.

## 7. What is not known

- [x] ~~The threshold values for the 11 counter achievements.~~ **AB-1 — the negative of §10 stands (reconciled 2026-09-12, FABLE):** the accumulate path never reads a threshold and the ~~twelve~~ eleven *(corrected 2026-10-02, OPUS: eleven type bytes at `00D10460` are non-zero, indices 0–4, 6, 7, 11, 13, 14, 17)* accumulating descriptors carry 0 (index 13's `16` is a mode-3 bit index), so the counter targets are not in `FFXII_TZA.exe`; ~~the notifier `008632B0` hands the running value on, and the comparison lives on the Steam side.~~
      **MECHANISM CORRECTED 2026-09-17 (FABLE); the negative stands, the last clause does not.** The targets are indeed not in the executable - they are in `menuhandbook.bin`, which `003165C0` reads per index (`UQ-274`). But the comparison is LOCAL: the checker `00315E90`'s mode-0 arm (`00315F19`) compares the counter (`00316760`) against that override and fires the notifier itself; the notifier (`UQ-275`) then unlocks by name. *The running value is handed to Steam, where the target lives* is therefore wrong on both counts - nothing hands a value on, and the target lives in the handbook. A consequence that DATA can test: any counter index whose handbook bit is clear would compare against the authored 0 and fire at the first check, so the handbook mask must cover all eleven.
- [x] What `HORIDASHI` and `YUGOU` refer to in the shipped game. **AB-2.**
  *Half answered 2026-09-15 (FABLE) — `HORIDASHI` is named by the shipped data; ~~`YUGOU` is not~~.* *(answered: YUGOU too — record 19 at `01E00258` is *Mist Walker*, the 2026-09-17 answer below; 2026-10-02, OPUS)*
  - **HORIDASHI is the bazaar's script-unlocked stock.** Three script verbs carry the name: `ishoridashi` (`0x2F5`),
    `clearhoridashi` (`0x2F6`) and `sethoridashi` (`0x2F7`,
    [the verb table](../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv)).
    - `sethoridashi`'s handler `0034C710` pops an id and tail-calls `0032AB50(good, 1)`. That is the script entry the
      [bazaar contract](../12-Items-Equipment-Shops-License/CONTRACT-bazaar-unlock-and-purchase.md) records: it sets
      availability only for bazaar rows whose `+0x14` bit 1 is set.
    - **Exactly seven of the 128 bazaar rows** (battle pack directory `+0xE8`) carry that bit: `0x63`–`0x66` and
      `0x7C`–`0x7E`, all named *Forgotten Grimoire*.
    - **They are exactly the seven ids the shipped scripts pass** (`0xD063`–`0xD066`, `0xD07C`–`0xD07E`; 135 calls in
      the decompiled `us` corpus).
    - Six of the seven sit behind a per-location visit counter: `g_com_counter_for_horidasi[n]` increments beside a menu
      open (`openfullscreenmenu_48d(2, 51)`, saturating at 255). On reaching 100 (`0xD066`), 30 (`0xD064`), 25
      (`0xD07C`), 15 (`0xD07E`), 40 (`0xD065`) or 20 (`0xD07D`), it calls `sethoridashi` once, guarded by a bit of
      `g_com_check_for_horidasi`.
    - `0xD063` is set once, after a dialogue line, in an `rbn` script.
    - `0xD066` appears in 22 area scripts; the others in 5–6 each.
    - So *horidashi* (掘り出し物, a find or bargain) names these seven unlockable Grimoire packages. Which of them the
      achievement `ACH_SPECIAL_HORIDASHI` counts is not tied in the image: ~~the achievement names have no index binding~~ *(answered: the names do have one — record 17 at `01DFFF28` is `{19, ACH_SPECIAL_HORIDASHI, "Collector"}`, the 2026-09-17 answer below; 2026-10-02, OPUS)*
      (§ above).
  - ~~**YUGOU stays open.**~~ *(answered: see the 2026-09-17 answer below — record 19 at `01E00258`; 2026-10-02, OPUS)* Its only occurrence in the image is the string `ACH_COMPLETE_YUGOU` (file offset `0x7E4E6D`). No
    script uses the name, and `horidashi.bin` (named in the image's test-battle paths) is not in the local extract.
      ***ANSWERED 2026-09-17 (FABLE): YUGOU is the achievement the player sees as *Mist Walker*, and the image says so in a table this page had not found.** The achievement manager's record array is static: 41 records of `0x198` bytes at `01DFE410`, one per `ACH_` tag, each `{qword counter id at +0x00, tag pointer at +0x08, inline Steam title at +0x10}` (the unlock body's `[manager+8] + index * 0x198` of UQ-275 indexes exactly this array; its `+0x190` unlocked byte sits at the record's end). Record 19 is `{13, ACH_COMPLETE_YUGOU, "Mist Walker"}` (`01E00258`). The counter ids are [the contract page](CONTRACT-achievement-counters.md)'s save-layout ids: 0..4 (`COUNT_FIGHT`, `MAGIC`, `TECH`, `STEAL`, `KILL`), 5 `STEP`, 6 `GET_GIL`, 7 `USE_GIL`, 8 `LEVEL_AVERAGE`, 9..12 the `MASTER_*` four, 13 `COMPLETE_YUGOU`, 14 `SELL_EVITEM`, 15 `COMPLETE_MAP`, 16 `COMPLETE_MONSTER`, 17 `COUNT_SCORE`, 18 `COUNT_CHAIN`, 19 `HORIDASHI`, 20..29 the ten `MONSTER` marks, 31..38 the eight `EVENT` milestones, 39 and 40 the two `TRIAL` tiers, and record 0 `CHAMPION_IVALICE` with id 0 beside `COUNT_FIGHT`. So the counter this page's §10 found fired per Esper-attack row, index 13 with threshold 16, is Mist Walker's: *yugo*, fusion, is the developers' word for the Mist family, and the achievement counts Esper attacks. The whole table, with every title, is [`members/achievement-descriptors.tsv`](members/achievement-descriptors.tsv). Static; the records read from the file image.*
- [x] ~~**UQ-272.** Whether `SteamNetworking` / `SteamMatchMaking` are actually called, or only linked. **AB-3 —~~
      directly relevant to the multiplayer project.**
      **Narrowed 2026-09-14 (FABLE): the interfaces are fetched once, and no use of them was found.**
      - **The fetch.** The Steam context initialiser, reached through `SteamInternal_ContextInit` (IAT `008C3190`), asks the Steam client for every interface in the SDK's list. It loads each version string (`SteamMatchMaking009` at `00903578`, `SteamNetworking005` at `009035F8`, and the others in `00903548`–`009036E8`) and stores the result in a context slot. MatchMaking goes to `+0x20` and Networking to `+0x40`; MatchMakingServers to `+0x38` and user stats to `+0x28`. This is the SDK's context boilerplate, so the fetch alone says nothing about use.
      - **The uses.** Every `.text` call through `SteamInternal_ContextInit` was scanned for the context slot read in the next seven instructions. The slots read are:
        - `+0x28` user stats, 17 sites (the achievement path this page documents);
        - `+0x08` user, 4;
        - `+0x18`, 2;
        - `+0x30`, 1;
        - `+0x68` controller, 1.
        **`+0x20` and `+0x40` are never read.**
      - **Not excluded:** a consumer that keeps the context pointer and reads the slot later, or reaches an interface by another route. The result is linked and initialised, with no call found.
      ***ANSWERED 2026-09-17 (FABLE): only linked. The two interfaces are fetched into a context nothing keeps, and their slots are read nowhere.** The SDK context is one static record at `01DFE0D0` (the once-only `Init` wrapper `001F3E10` zeroes its twenty slots and tail-calls the fetcher `001F3AE0`, which fills them: matchmaking into `+0x20` from `SteamMatchMaking009`, networking into `+0x40` from `SteamNetworking005`; those version strings have no other reader). The context is reached only through `SteamInternal_ContextInit` (IAT `008C3190`), which returns its address: all 25 call sites in the image were classified, and every one consumes the returned pointer in place, with a slot read or compare (`+0x28` user stats, `+0x08` user, `+0x18`, `+0x30`, `+0x68`) or a second `ContextInit` call; none stores it to memory or another register, so the 2026-09-14 residual, a consumer that keeps the pointer, does not exist. No instruction reads the record's `+0x30` or `+0x50` (context `+0x20`/`+0x40`) by absolute address either. So the networking and matchmaking interfaces are obtained at start-up and never called in the shipped executable; a multiplayer build gets nothing from them but the fetch. Static, every site read.*
- [x] ~~Whether achievements read the persistent flag banks or keep separate state.~~ **AB-4 ANSWERED 2026-09-12 (FABLE): separate state, inside the save image.** The updater keeps the fired bitmap at block `+0x3844` (§10; payload `+0xB844`) and ~~the counters in the entry table at payload `+0x8224`~~ **reads the entry table at payload `+0x8224` — corrected 2026-09-12 (FABLE, FG-1): those entries are the navigation maps' revealed-tile bitmaps, and the exploration check `003160C0` consumes them (popcount `00255060` on the live map, `00255120` per listed map), it does not keep counters there** (AB-5, [the save-payload field map](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md)); no persistent-flag-bank accessor is called on either path.
- [x] ~~Where the running counters live — very likely the save payload.~~ **AB-5** — ANSWERED 2026-09-10:
  inside the save image at payload `+0x8000` — `00253970` points `020927C0` at the active buffer `+0x8200`
  (`00253985`–`00253990`); the entry table at `+0x8224`, the fired bitmap at `+0xB844`
  ([the save-payload field map](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md)).
- [x] What the 58 unnamed Platform-owned functions do. **AB-6.**
      ***NARROWED 2026-09-17 (FABLE): the unnamed set is 59 today, and what each body calls sorts it into five groups; the per-body listing is [`members/platform-unnamed-functions.tsv`](members/platform-unnamed-functions.tsv).** The census pairs every Platform-owned `FUN_` body with its imports (the edge list's external callees), its named callees and the strings its `lea` operands reach. *Twenty* are the achievement-counter bodies `00315390`..`00316C60`, which [the counters contract](CONTRACT-achievement-counters.md) and this page already read under their addresses (the bestiary byte `00315420`, the category tester `003154B0`, ~~the counter updater `00315E90`~~ the evaluator `00315E90` *(corrected 2026-10-02, OPUS: the updater is `00316A50`; `00315E90` writes no counter)*, `003165C0`, `003166F0`, `00316760`, `00316A50`, `00316BF0`); they call `FieldData_GetVariable0`, `BattleEncodedId_DispatchQueryMode0Value` and `WorldTransition_GetActiveOrPendingFieldId` and import nothing. *Sixteen* are Steam API bodies: `001F3AE0` (809 B) acquires the `SteamClient017`, `SteamUser019` and `SteamFriends015` interfaces through `SteamInternal_ContextInit`; `0020C730`, `008653B0` and `008655E0` register callbacks and `0020CD80`, `00865490` and `00865660` unregister them; `0020C940` ~~prints `name` and `desc` through `OutputDebugStringA`~~ copies the `name` and `desc` display attributes into each entry's `+0x10` and `+0x90` and prints one fixed line through `OutputDebugStringA` *(corrected 2026-10-02, OPUS: slot `+0x60`, then `001CCAC0` (`__stdio_common_vsprintf`, format `%s`) at `0020C940+0xC4` / `+0xDA` and `+0xFE` / `+0x117`; the one `OutputDebugStringA` call, `0020C940+0x34`, prints "Received stats and achievements from Steam")*; `007A0C60` matches the Steam language against `japanese`, `english`, `french` and the rest (this page's `Language` finding); the others are `SteamInternal_ContextInit` wrappers. *Two*, `0079FA00` and `00862A40`, build a folder path with `SHGetFolderPathW`, `GetFileAttributesW` and `CreateDirectoryW` (the `%s%s%s` save-folder pattern). *Three* are miscellaneous: `007A0810` a guarded static initialiser, `008655A0` a debug print, `0020CD30` a 77-byte body ~~with nothing to name it~~ *(answered: it creates the achievement manager — allocates `0x80` bytes, calls `0020C730` and stores `01F83450`, CONTRACT-steam-integration-subsystem.md §3; 2026-10-02, OPUS)*. *Eighteen* are bare stubs of at most 60 bytes with no import, callee or string (`0020C840`..`0020CE00`, `00862A20`, `00863240`..`008632B0`, `00865540`..`00865590`, `008B7DB0`), the shape of the Steam callback objects' vtable arms. What remains unnamed is those eighteen and the bodies of the sixteen beyond their imports. Static; census only.*
      **Narrowed 2026-09-18 (FABLE): the Steam callback objects name their events, and nine of the eighteen bare stubs with them.* Each register body installs a `CCallback<Owner, Event>` vtable whose RTTI names both: `0020C730` registers `CSteamAchievements` for `UserStatsReceived_t` (id `0x44D`, vtable `00906360`), `UserStatsStored_t` (`0x44E`, `009063A0`) and `UserAchievementStored_t` (`0x44F`, `009063E0`) through `steam_api64.dll!SteamAPI_RegisterCallback` (`008C3180`); `008653B0` registers `SteamCallbacksListener` for `SteamServersConnected_t` (`0x65`, `01CCFBE0`), `SteamServersDisconnected_t` (`0x67`, `01CCFC20`), `SteamServerConnectFailure_t` (`0x66`, `01CCFC60`) and `SteamShutdown_t` (`0x2C0`, `01CCFC80`); `008655E0` registers `CSteamManager` for `GameOverlayActivated_t` (`0x14B`, `01CCFCA0`); `0020CD80`, `00865490` and `00865660` unregister the same objects through `SteamAPI_UnregisterCallback` (`008C3178`). Every one of the eight vtables shares slots 0 and 1, `00865550` (`Run`: tail-jump through `[this]+8`) and `00865540` (`Run` with the call-result form: loads `this+0x10` and tail-jumps `[this+0x18]`), and the per-event handler is the function pointer each registration stores beside the object — so the handlers are named: `0020C940` `OnUserStatsReceived` (~~the `name` / `desc` debug print~~ the `name` / `desc` copy into each entry *(corrected 2026-10-02, OPUS: `0020C940+0xDA` and `+0x117`, see the AB-6 note above)*), `0020CB20` `OnUserStatsStored`, `0020C8C0` `OnUserAchievementStored`, `00865560` `OnServersConnected`, `00865570` `OnServersDisconnected` **and** `OnServerConnectFailure` (one body registered twice: `inc [this+0x88]`, `[this+0x80] = 1`), `00865590` `OnSteamShutdown` (clears both), `008655A0` `OnGameOverlayActivated`. Slot 2 is `GetCallbackSizeBytes`: `0020C8A0` returns `0x18` (`UserStatsReceived_t`), `0020C8B0` `0x98` (`UserAchievementStored_t`), `0053DD10` returns 1 for the three one-byte events, `001F2880`, `0016EE70` and `00314F20` are the folded size stubs of the other three. That names `00865540`, `00865550`, `00865560`, `00865570`, `00865590`, `0020C8A0`, `0020C8B0` and `0020CB20` of the eighteen bare stubs and gives `008655A0` its event. Static: the RTTI of the eight installed vtables and the register bodies.*
      *SUPERSEDED 2026-09-26 (FABLE, Claude Opus 5.5) under FRONTIER's class-1 ruling: a population-coverage statement; the population is carried by 20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md. See the register row.*
- [x] ~~What `ACH_SPECIAL_MONSTER01..10` are (rare marks? Espers?).~~ **AB-7 closed 2026-09-12
      (FABLE): not in the image.** ~~The updater's seven callers fire indices 0–4, 6, 7, 11, 13, 18 and~~
      ~~19 only (kills, steals, magicks, technicks, gil in / out, licence points)~~ The updater's nine call sites, three direct and six through the thunk `00253770`, fire indices 0–4, 6, 7, 11, 13, 14, 17, 18 and 19 *(corrected 2026-10-02, OPUS: `retool.py callers 00316A50 00253770`; 14 at `0056D370+0x126`, 17 at `002E2380+0x2` and `00317090+0x43`)* and none passes 20–29,
      so ~~the ten mode-7 descriptors have **no producer in the shipped executable**; what monsters the~~
      ~~names meant is authoring history the binary does not carry, and a reconstruction needs only the~~
      ~~fact that nothing ever raises them~~ the updater is not the ten mode-7 descriptors' producer; the checker's mode-7 arm is *(corrected 2026-10-02, OPUS: the evaluator's jump-table load `00315E90+0x7C` reads eight targets: modes 1 and 4 `00315E90+0x1ED` (the return), 5 `00315E90+0x14C`, 6 `00315E90+0x15B`, 7 `00315E90+0x16A`; the sweep `00316930` runs the checker for ids 0–29 at `00316930+0x109`, see the 2026-09-17 answer below)*. **AB-7.**
      **REOPENED AND ANSWERED 2026-09-17 (FABLE) - the 2026-09-12 closure was wrong: a producer exists, and it is not the updater.** The closure reasoned from the updater's callers alone. The periodic sweep `00316930` calls the checker `00315E90` for every index 0–29 (`00316A36`–`00316A43`), and the checker's mode-7 arm (`00315FFA`) indexes the descriptor's threshold (0–9) into the `u16` monster-id list at `menuhandbook.bin`'s third hop from `[022C2550]+8` and awards when that monster's bestiary defeat count (`00315420`: save `+0x3404` byte minus one) is above 0. So `ACH_SPECIAL_MONSTER01..10` fire on defeating the ten monsters the handbook lists, in list order, and their identities are a DATA read of that record (routed), not authoring history. The count-and-shape match of §10 (ten mode-7 descriptors, ten names) stands; what was wrong was *nothing ever raises them*. See `UQ-273`.

      **List read 2026-09-18 (SWE2-DATA), `us` `menuhandbook.bin`:** the hop-3 record lands at blob
      `+0xDC` and carries `u16 count = 11` at `+2` - **eleven** `u16` bestiary ids at `+4`, not ten.
      In list order: `0x00F8, 0x00FB, 0x00FD, 0x00F0, 0x00FA, 0x00E6, 0x0104, 0x0121, 0x010F,
      0x0111, 0x0103`. The ten mode-7 descriptors (indices 20-29) carry thresholds `0`-`9`, so only
      the first ten entries are reachable through the checker: `ACH_SPECIAL_MONSTER01` tests list
      entry 0 (`0x00F8`) through `ACH_SPECIAL_MONSTER10` at entry 9 (`0x0111`); entry 10 (`0x0103`)
      is shipped but never indexed. Naming the ids is a separate decode: the `hctg` index
      `menuhandbook_monster.bin` plus the per-entry `menuhandbook_monsterNNN.dat` pages carry the
      names in section-002 text (page `000` decodes to *Cactus*), ~~but the bestiary-id -> page map~~
      ~~inside `hctg` is not yet read.~~ *(Answered by reconciliation 2026-09-30, SWE2-DATA: [the handbook page](../16-UI/Handbook/the-handbook-screen.md) decodes the list as Trickster, Gilgamesh, Behemoth King, Fafnir, Carrot, Deathgaze, Yiazmat, Hell Wyrm, Ultima, Zodiark and Shadowseer. The first ten are `ACH_SPECIAL_MONSTER01`..`10`.)*
      *Narrowed 2026-09-12 (FABLE) — the updater's callers enumerated.* `00316A50` is reached directly
      from three sites and through one thunk (`00253770`) from ~~four~~ six more *(corrected 2026-10-02, OPUS: the thunk's callers are `0028F0C0`, `002E2380`, `00305640`, `003112F0`, `00317090` and `003171C0`, as the counter-17 census below says)*, and **no caller passes an
      index in 20–29**: `GameState_SetGil` fires **6** with the gil gained and **7** with the gil spent
      (`00254EF8`–`00254F02`); `BattleUnit_ProcessDefeatRewardsAndLoot` fires **11** with the licence
      points awarded (`00312496`) and, through `003171C0`, **4** (amount 1) for every enemy-kind
      defeat (`003171DF`–`003171E7`); `BattleFormula_ApplyTargetResult` fires **3** (amount 1) as it
      clears a stolen-loot bit (`00311468`–`00311475`); `BattleAction_ConsumeExecutionResources` fires
      **0 / 1 / 2** (amount 1) for a party unit's action whose row `+0x1E` is 0 (Attack), 1 (the 81
      magicks) or 2 (the 24 technicks), and **13** with the row index for `+0x1E == 10` (the sixteen
      Esper-attack rows, `00305744`–`003057A5`, [the action definition row](../07-Combat-Action/Action-Definition-Row/the-action-definition-row.md)); `0028F0C0` fires **18** with a value it
      also stores at block `+0x7C78`; `0056D370` fires **19** (mode 1, threshold 53375) with a word
      from its record's `+8` *(and **14** on a sale - corrected 2026-09-30, OPUS; see the counter-17 census below)*. ~~So kills, steals, magicks, technicks, gil in, gil out and licence~~
      ~~points are the counters this build advances natively, and the ten mode-7 descriptors have no~~
      ~~producer in the image — either the Steam side unlocks them from stats, or they are dead.~~ The stored counters this build advances natively are attacks, magicks, technicks, steals, kills, gil in, gil out, licence points, Esper attacks (13), sales (14) and the score (17), and the ten mode-7 descriptors are produced by the checker's mode-7 arm, not by Steam *(corrected 2026-10-02, OPUS: the updater's nine sites above; the evaluator's jump-table load `00315E90+0x7C` reads eight targets: modes 1 and 4 `00315E90+0x1ED` (the return), 5 `00315E90+0x14C`, 6 `00315E90+0x15B`, 7 `00315E90+0x16A`)*.
- [x] Whether `ACH_COUNT_SCORE` relates to Trial Mode. **AB-8.** *(closed — the register row is ~~WITHDRAWN~~ **SUPERSEDED** 2026-09-26; the register word corrected 2026-09-30, SWE2-DATA.)* *(Corrected 2026-09-30, SWE2-DATA, per SWE2-AUDIT-SEM's batch-4 review C9 (`_index/candidates/auditsem-review-dd-owner-read-4-0930/REVIEW.md`): the row now carries FABLE's correction that the SUPERSEDED disposition rests on a false static premise. Counter 17 is fed natively (once per defeat, and by the `addclanpoint` verb), accepted in `auditsem-review-ab8-0930`. The register word is pending with the register owner, so SUPERSEDED is not the current summary.)*
      *Narrowed 2026-09-12 (FABLE):* no native caller of the updater is Trial Mode's; the only
      counter with a non-zero threshold, index 13 (`16`), is fired by
      `BattleAction_ConsumeExecutionResources` with the row index of an Esper-attack row (`+0x1E ==
      10`). If the count-and-shape match of §10 holds, `ACH_COUNT_SCORE` would sit in that list by
      order only; ~~nothing in the image ties the name to an index~~ *(answered: the record array at `01DFE410` ties it, see the 2026-09-17 note below; 2026-10-02, OPUS)*, and nothing Trial-Mode-shaped
      raises any counter. Live-only discriminator: whether a Trial stage clear advances any stat.
      ***NARROWED 2026-09-17 (FABLE): the tag-to-index tie is now proved, and it moves `ACH_COUNT_SCORE` off index 13.** The static descriptor array at `01DFE410` (AB-2, [`members/achievement-descriptors.tsv`](members/achievement-descriptors.tsv)) gives `ACH_COUNT_SCORE` counter id 17 and the title *Record Breaker*; counter 17 is one of the four int32 counters in [the contract](CONTRACT-achievement-counters.md)'s save layout (with 11, 6 and 7), and index 13, the Esper-attack counter with threshold 16, is `ACH_COMPLETE_YUGOU`, *Mist Walker*. So the count-and-shape placement above is withdrawn: nothing Esper-shaped feeds the score. What feeds counter 17 is not found by an immediate scan of the updater's call sites (no site passes 17 directly, so it goes through a wrapper or a computed id), and whether a Trial stage clear advances it stays the live discriminator.*
      *Narrowed 2026-09-18 (FABLE): ~~every route into the counter block is enumerated, and none of them feeds counter 17.~~* The block lives at `record + 0x384C` of the save record `002536A0` returns (`003166F0`, `00316705`; the fired bitmask at `+0x3844`), and a whole-image scan for any memory operand with displacement `+0x3844` .. `+0x386B` finds it touched only by the accessor family that forms that address — `003162E0`, `003166F0`, `00316810`, `00316BF0`, `00316C60` — and by the fire-bit readers; no other body indexes a counter by offset. **~~The store path~~ The evaluate-and-award path takes the id only** *(corrected 2026-10-02, OPUS: `00315E90` is the checker; the store is `00316BF0`, CONTRACT-achievement-counters.md §2)*: `00315E90` overwrites `edx` at `00315EBA`, so it carries no amount, and it has two callers, the re-check loop `00316930` over ids 0 .. 29 (`00316A36`–`00316A43`) and `AchievementCounter_UpdateAndMaybeFire` `00316A50`. ~~**The three sites of `00316A50` pass 6, 7, 11 and 19, never 17**~~ *(corrected 2026-09-30, FABLE: these are the three DIRECT sites; six more reach `00316A50` by tail jump through the thunk `00253770`, and two of them pass 17 - see the correction below)*: `GameState_SetGil` passes 6 or 7 by the sign of the gil delta (`00254EF8`, `00254F00`), `BattleUnit_ProcessDefeatRewardsAndLoot` passes 11 with ~~the 99,999-clamped total it keeps at `+0x190`~~ the licence points just awarded, while the 99,999-clamped total goes only to `+0x190` *(corrected 2026-10-02, OPUS: `mov edx, esi` at `00312280+0x204`, `esi` being the increment added at `00312280+0x201`)* (`00312475`–`00312496`), and `0056D370` passes 19 with a record's word `+8` as the amount (`0056D4CC`–`0056D4D2`, ~~gated on `[+0xE4] & 0x3FC0 == 0x2C0`~~) *(Corrected 2026-09-30, OPUS, on SWE2-STRUCT's DD batch 11, [`swe2struct-ddres-b11-0930`](../_index/candidates/swe2struct-ddres-b11-0930/README.md) S1-S2: the `0x2C0` test guards only the `0030B630` unlock call (`0056D4AC`-`0056D4C0`), so every purchase passes 19; the same driver's sale arm passes **14** with the quantity sold `+0xDC` when `[+0xE4] & 0x3FC0 == 0x1C0` (`0056D483`-`0056D498`, `cl = 0xE`, then the shared call at `0056D4D2`).)*. The two remaining accessors are not feeders either: `00316810` is the load-time normaliser, called once from `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` (`00584398`), and `00316C60` is the developer console's 99,999 max helper, called once from the max-LP arm `00305A00` (`00305A96`). The name itself closes the last door: `ACH_COUNT_SCORE` (`00905F80`) is referenced by exactly one qword in the image, the static record `01DFF268` (slot 9), whose `0x198` bytes hold the counter id `0x11`, that name pointer and the inline title *Record Breaker* and no code pointer, so there is no per-achievement evaluator. ~~**So no native body advances counter 17 with an amount in this build.**~~ Either the score is never fed (the achievement would then be unreachable through the counter mechanism) or it arrives by a route this image cannot show — a Steam-side stat or a code path outside the function list — and that is exactly what the live discriminator decides: whether a Trial stage clear moves the counter at `+0x3868`. Static: the displacement scan, the six accessor bodies and their callers, the record bytes. *Corrected 2026-09-30 (FABLE, Claude Opus 5.5; AB-8; `_index/candidates/ab8-counter17-fable-0930/`, `ab8_counter17.py`, FAILS 0):* **counter 17 IS fed, by two native bodies**, both through the 5-byte thunk `00253770` (`jmp 00316A50`), which the 2026-09-18 census did not follow. `00317090` passes `ecx = 0x11` (`003170D3`) with the amount `(byte [+0x1C2] - byte [+0x88]) x word [[+0xE78]] + word [[+0xE70]]` (`003170AA`-`003170D1`) and is reached once per defeat from `BattleUnit_ProcessDefeatRewardsAndLoot` `00312280` (`003125BC`); the 12-byte wrapper `002E2380` (`002E2382`) passes 17 with its caller's amount and is called only by the handler `003403E0` of script verb `0x4DC` `addclanpoint`. So `ACH_COUNT_SCORE` (*Record Breaker*) accumulates the per-defeat award and the scripts' `addclanpoint` amounts: native code advances it, so the page's 'never fed' reading is withdrawn. The other four thunk sites pass 18 (`0028F0C0`), 3 (`003112F0`, `lea ecx, [rdx + 2]` at `00311472`), 4 (`003171C0`, `003171E4`) and 13, 2, 1 or 0 (`00305640`, `00305785`-`003057A0`); none passes 17. The live discriminator named above is withdrawn: what moves the counter is static. Control: the census's three direct feeders are found by the same raw-index read.

> **Crossing into ActorEntity — FINAL-AUDIT pass 22 (FABLE, 2026-09-14).** `003171C0`, the wrapper that fires
> counter 4 in the AB-7 note, does one more thing after the fire. If the unit's `+0x698` record still has byte `+5` = 1,
> it asks the actor layer for the class nibble of the unit's actor `[unit+0x10]`. The query goes through
> `ActorRuntime_GetClassNibble` (`00263C20`, `actor[0x0E] & 0x0F`;
> [the slot pool and actor class](../04-Actor-Entity/battleunit-slot-pool-and-actor-class.md)). It **skips class 3**.
> Otherwise it passes the word at `[[unit+0xE68]+0x52]`, unless that word is `0xFFFF`, to `00315820` through the thunk
> `00253750` (`003171EC`–`0031721F`). ~~What class 3 is and what `00315820` records are not read here.~~ *(Reconciled 2026-09-30, SWE2-DATA: `00315820` counts a defeat in the bestiary tally at save `+0x3404` ([actor-bind event memory](../14-Story-Event-Quest-Hunt/event-memory-at-actor-bind.md)). Class 3 is free-target type 3 (AL-3), the value `btlAtelSetUnitType` argument 2 selects. Which units carry it is `SD-160`.)*

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| 41 achievement identifiers | authored strings extracted from the authorized EXE by pattern `ACH_[A-Z0-9_]+` | 2 |
| The ~~seven-family~~ eight-family taxonomy *(corrected 2026-09-30, SWE2-DATA, per §9)* | the identifiers' own naming | 2 |
| Gil earned and spent are separate | distinct `ACH_COUNT_GET_GIL` and `ACH_COUNT_USE_GIL` | 2 |
| Trial Mode achievements exist | `ACH_TRIAL_MODE_50` / `_100` | 2 |
| ~~23~~ 21 Steam interface versions *(corrected 2026-09-30, SWE2-DATA, per §9)* | authored interface-version strings | 2 |
| SteamController is genuinely used | `SteamController_PollState` (named, 1,124 B) plus connect/disconnect strings | 3 |
| 59 Platform-owned functions | GFZ owner census | 3 |
| the counter targets live in `menuhandbook.bin` and are compared locally *(rows added 2026-09-30, SWE2-DATA)* | §10, UQ-274; the checker `00315E90` | 1 |
| an unlock is recorded locally, then sent by `SetAchievement` and `StoreStats` | §10, UQ-275 | 1 (6 for the slot names) |
| networking and matchmaking are fetched and never used | §7, AB-3 | 1 |
| the achievement records and their Steam titles | `01DFE410`, §2, AB-2 | 1 |
| entry 0 is awarded by the two receipt handlers | [`pf_steam_checks.py`](../_index/candidates/dd-data-4-0930/pf_steam_checks.py) S1, S2 | 1 |
| the chain achievement compares the passed value; kind-4 sums never go below 0 | S3–S5, C | 1 |

### The claim I am specifically not making

`SteamNetworking005` and `SteamMatchMaking009` appear in the binary. It would be easy — and wrong —
to present that as evidence that FFXII: The Zodiac Age has latent multiplayer or networking support,
which is exactly the claim this project would most like to be true.

**Every Steamworks title contains these strings.** The SDK's interface-accessor headers reference
each interface by versioned name, and the linker keeps the string whether or not the accessor is
ever called. The correct test is whether any code path reaches the accessor, and that requires
reading the platform functions~~ — none of which were read here~~. *(answered: see §7, AB-3 — every `SteamInternal_ContextInit` site was read and the matchmaking and networking slots are read nowhere; 2026-10-02, OPUS)*

~~Recorded as **AB-3, OPEN**, not as a finding.~~ *Superseded 2026-09-26 (FABLE, Claude Opus 5.5): **AB-3** was answered on 2026-09-17. The two interfaces are only linked: they are fetched into a context nothing keeps, and their slots are read nowhere.*

### Why tier 2 and why the code section is empty

~~Everything load-bearing here is an authored string. That is strong evidence for *what the names~~
~~are*, and no evidence at all for *what the code does*. All 59 platform functions are unnamed and~~
~~unread, so §3 lists sizes and nothing else, and §5's call chain marks the achievement-setting step~~
~~as `(unread)` rather than describing it.~~ *(Corrected 2026-09-30, SWE2-DATA: written before the reads in §7 and §10. The award path is now tier 1, in the rows added above, and §3 and §5 say so. The identifier strings remain the tier-2 part.)*

The Japanese glosses in §2 are the weakest thing on this page — a romanization plus a dictionary
meaning, with the in-game referent explicitly unproven.

## 8b. Reopened 2026-09-02 - AB-3: two methods tried, both inconclusive

The question was whether `SteamNetworking005` and `SteamMatchMaking009` are actually used or merely
linked. ~~**It is still open**, but the search space is now much better defined.~~ *(Superseded by reconciliation 2026-09-30, SWE2-DATA: AB-3 was answered 2026-09-17 — only linked, §7. This section stays as the record of two failed methods.)*

### What the import table proves

`steam_api64.dll` is a genuine import, with exactly **nine** functions:

```
SteamAPI_Init                    SteamAPI_RunCallbacks
SteamAPI_RestartAppIfNecessary   SteamAPI_RegisterCallback
SteamAPI_GetHSteamUser           SteamAPI_UnregisterCallback
SteamAPI_GetHSteamPipe           SteamInternal_CreateInterface
                                 SteamInternal_ContextInit
```

**Every interface is acquired through the two generic accessors** - `SteamInternal_CreateInterface`
and `SteamInternal_ContextInit`. There is no per-interface import. So the import table is
**structurally incapable** of answering which interfaces the game uses: networking and user-stats
go through exactly the same two entry points.

### Two failed methods, recorded so they are not repeated

**Method 1 - RIP-relative LEA scan.** Scanning `.text` for `48 8D /r` references to the interface
version strings returned **zero hits for every interface**, including
`STEAMUSERSTATS_INTERFACE_VERSION011`.

Achievements demonstrably work in the retail game, so the user-stats interface *must* be acquired.
A test that reports "not referenced" for a known-positive is broken. **Rejected.**

**Method 2 - absolute pointer search.** Searching the whole image for 8-byte pointers to those
string addresses returned **zero** as well - again including the known-positive.

Both results are consistent with the Steamworks SDK's accessor pattern, where the version string
reaches `SteamInternal_ContextInit` through a static context structure populated at runtime rather
than through a compiled-in reference the file can show.

### What this does establish

The strings sit at `0x9035B0` (`STEAMUSERSTATS`), `0x903578` (`SteamMatchMaking009`), `0x9035F8`
(`SteamNetworking005`) and `0x903548` (`SteamUser019`) - a contiguous `.rdata` table, exactly as the
SDK header emits them.

**Answering AB-3 requires reading the accessor call sites**, not a static string search. The
positive control for any future attempt is fixed: whatever method is used must find
`STEAMUSERSTATS_INTERFACE_VERSION011`, because achievements work. If it does not, the method is
wrong.

**The original caution stands and is now better founded:** nothing yet shows FFXII uses Steam
networking or matchmaking, and the import table shows it *cannot* be inferred from linkage.

## 9. Related

- [`../14-Story-Event-Quest-Hunt/persistent-flag-banks.md`](../14-Story-Event-Quest-Hunt/persistent-flag-banks.md) — story bits, which overlap in subject with `ACH_EVENT_*` ~~but are not yet connected to it~~ *(answered: see §7, AB-4 — separate state, the fired bitmap at block `+0x3844`; 2026-10-02, OPUS)*
- [`../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md`](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md) — where the counters ~~most likely~~ live *(answered: see §7, AB-5 — inside the save image at payload `+0x8000`, the block at `+0xB844`; 2026-10-02, OPUS)*
- [`../13-Rewards-Progression-Economy/experience-and-license-point-award.md`](../13-Rewards-Progression-Economy/experience-and-license-point-award.md) — gil, which two counters track
- [`../23-Third-Party-Libraries/third-party-middleware-inventory.md`](../23-Third-Party-Libraries/third-party-middleware-inventory.md) — the other linked third-party surfaces

## 9. Falsification pass 2026-09-02

**Attack chosen.** Everything load-bearing here is a **count over authored strings** — 41
identifiers, seven families, 23 interfaces — and every one is reproducible from the image. All were
recounted by exhaustive enumeration, printing complete lists rather than samples.

### SURVIVED exactly: 41 achievement identifiers

A scan for `ACH_[A-Z0-9_]+` returns **41 distinct identifiers**, matching the headline to the unit,
and the seven listed groups account for all 41 with nothing left over.

### CORRECTED: eight families, not seven

Grouping by prefix gives **eight**: `COUNT` 11, `SPECIAL` 11, `EVENT` 8, `MASTER` 4, `COMPLETE` 3,
`TRIAL` 2, `CHAMPION` 1, `LEVEL` 1. The document's own prose says *"and **two** singletons"*, so the
heading's "seven" contradicts the body — the two singletons are two families, not one. Counts are
unaffected: `11+11+8+4+3+2+1+1 = 41`.

### CORRECTED: 21 interfaces, not 23 — but the list was already right

This is the reverse of the defect found in
[`../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`](../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md)
§9, where a correct total sat over wrong rows. **Here the rows are right and the total is wrong.**

An exhaustive enumeration of every printable string in the image containing "steam" (49 in total)
yields exactly **21** interface-version strings — 8 short-form `SteamXxx###` and 13 long-form
`STEAM*_INTERFACE_*`. That is precisely the set the document lists. The inflation came from a
**stray trailing line**, `STEAMHTMLSURFACE / STEAMVIDEO / STEAMINVENTORY`, which repeated three
entries already present two lines above. It has been removed.

**A note on instrument, because it nearly produced a wrong finding.** The first regex used here
returned 18, then 19. It missed `STEAMHTMLSURFACE_INTERFACE_VERSION_003` (an underscore before the
digits) and both `_INTERFACE_V002` forms (`STEAMINVENTORY`, `STEAMVIDEO`), which use `V` rather than
`VERSION`. Had 18 been reported against the documented 23, the "missing" five would have been an
artefact of the pattern. **Only the exhaustive enumeration was trustworthy**, per the evidence
standard's rule on truncated and over-specific instruments.

### CORRECTED: seven `SteamAPI_*` symbols in total, not "Init plus seven"

The text read *"`SteamAPI_Init` and seven `SteamAPI_*` symbols"*, implying eight. There are **seven
in total, one of which is `Init`**: `Init`, `RestartAppIfNecessary`, `RunCallbacks`,
`RegisterCallback`, `UnregisterCallback`, `GetHSteamPipe`, `GetHSteamUser`. Two further symbols
exist but are not `SteamAPI_*` — `SteamInternal_ContextInit` and `SteamInternal_CreateInterface`.

### STRENGTHENED: the multiplayer caution now has positive evidence

§2 warns that `SteamNetworking005` and `SteamMatchMaking009` are *"present as interface-version
strings"* and that this **does not show usage**, because the Steamworks header emits a version
string for every interface it can describe. That was a careful negative resting on an absence.

The string enumeration supplies the missing positive side. The binary carries **RTTI class names for
concrete Steam callback registrations**, and they are specific:

```
CCallback<CSteamAchievements, UserAchievementStored_t>
CCallback<CSteamAchievements, UserStatsReceived_t>
CCallback<CSteamAchievements, UserStatsStored_t>
CCallback<CSteamManager,      GameOverlayActivated_t>
CCallback<SteamCallbacksListener, SteamServersConnected_t>
CCallback<SteamCallbacksListener, SteamServersDisconnected_t>
CCallback<SteamCallbacksListener, SteamServerConnectFailure_t>
CCallback<SteamCallbacksListener, SteamShutdown_t>
```

**Eight callback registrations exist: three for achievements, one for the overlay, four for
connection lifecycle — and none for matchmaking, lobbies, or P2P networking.** A game that used
`ISteamMatchmaking` or `ISteamNetworking` would need callbacks for lobby and session events, and
there are none. The caution is no longer an argument from silence: the callbacks the binary *does*
register show what it actually uses, and multiplayer is not among it.

### The callback count is confirmed a second way

The RTTI names above are one line of evidence. The **import table** is another, and it agrees
exactly. Counting `FF 15` call sites through each `steam_api64` import slot:

| Import | Call sites | Calling functions |
|---|---:|---:|
| `SteamAPI_RegisterCallback` | **8** | 3 |
| `SteamAPI_UnregisterCallback` | **8** | 3 |
| `SteamInternal_ContextInit` | 25 | 11 |
| `SteamAPI_GetHSteamPipe` | 2 | 2 |
| `SteamAPI_Init`, `RunCallbacks`, `RestartAppIfNecessary`, `GetHSteamUser`, `SteamInternal_CreateInterface` | 1 each | 1 each |

**Eight registrations, eight unregistrations, eight RTTI `CCallback<>` classes.** The numbers match
across two independent instruments — mangled type names in `.rdata`, and call sites through the
import table — and both say the same thing: this game registers callbacks for **achievements, the
overlay and connection lifecycle, and nothing else**. Had matchmaking or P2P networking been used,
a ninth registration would have to exist somewhere, and there is none.

*(These call sites are invisible to the function call graph, which records direct calls only; they
were recovered with `analysis-kit/gfz-scripts/iat_xrefs.py`.)*

Supporting runtime messages, all authored strings:

```
Received stats and achievements from Steam      Stored Achievement for Steam
Stored stats for Steam                          Steam overlay now active / inactive
Creating new Steam Controller                   SteamController Connected / Disconnected
```

### Also found

- `.\GameData\code_steam.txt` — a **Steam-specific authored data file**, not previously recorded.
- `PInputDevicePadSteamController@PFramework@Phyre` — the Steam Controller is wired in as a
  **PhyreEngine input device class**, which is why `SteamController005` is real usage where the
  networking interfaces are not.
- `SteamController_PollState` (`007A1CD0`, **1,124 bytes** — size confirmed) is a **GFZ working
  name**, not an authored string. The document calls it "a named function", which is accurate, but
  it is not evidence of the same kind as the quoted strings around it.

## 10. `00316A50` opened — the counter updater, and the table behind the catalogue

`00316A50` (411 B) was on the *leaned on and never opened* cut, cited by four documents — **none of
them this one.** It is the function that updates every counter in this catalogue, and it carries two
parallel authored tables.

**Extent checked**: 104 instructions, ends `ret` at `00316BEA`, no `jmp` leaves the extent.

### Signature and tables

`00316A50(index /*cl*/, amount /*edx*/)` — **`cmp cl, 0x1E ; jae return`, so the index space is 0–29,
thirty entries.** Two tables, both in `.rdata` and therefore **present in the shipped image**:

| table | address | stride | contents |
|---|---|---:|---|
| descriptors | **`00D10460`** | 8 | `+0x00` type, `+0x02` mode, `+0x04` threshold |
| ids | **`00D10550`** | 4 | one dword per entry, passed to the notifier |

**The thirty ids are distinct and span `0x01`–`0x1E`** — a dense 1-based identifier space.

### Two paths, and only one of them reads the threshold

```asm
00316A81  cmp byte ptr [table + i*8], 0
00316A8A  jne  accumulate            ; type != 0
```

**Type `0` — the trigger path.** The mode at `+0x02` selects the test: mode `0` compares the amount
against the threshold (or against a value from `003165C0` when that returns non-zero), mode `1`
requires an **exact match**. On success it sets a bit and notifies:

```asm
00316AC3  call 0x2536a0
00316ACB  movzx ebx, byte ptr [rax + rdi + 0x3844]
00316AD3  bts   ebx, esi
00316ADB  mov   byte ptr [rax + rdi + 0x3844], bl    ; a 30-bit bitmap at +0x3844
00316AEA  call  0x8632b0                              ; notify, with the id from the second table
```

> **There is a dedicated 30-bit "already fired" bitmap at `+0x3844`** of the block `002536A0` returns —
> **separate storage, indexed by the same 0–29 index.** That bears directly on **AB-4**: achievements
> keep their own bit here, whatever else they read.

**Type `2` or `4` — the accumulate path**, which **never reads `+0x04` at all**:

| type | saturation |
|---:|---|
| `2` | add, clamped to **`0x7FFF`**, and clamped **up to 0** if the result goes negative |
| `4` | add, clamped to **`0x7FFFFFFF`**, and clamped **up to 0** if the result goes negative *(corrected 2026-10-02, OPUS: the kind-4 arm's `jl` at `00316A50+0x162` reaches the same `add ebx, edi` / `jns` / `xor ebx, ebx` as kind 2, `00316A50+0x14D`..`+0x151`)* |

Mode `3` on that path does `bts value, (amount - 0xE2)` — **a bitfield counter whose bit index is the
amount minus 226**.

### The table, in full

```
 i type mode  threshold        id        i type mode  threshold        id
 0   2    0            0  0x00000001    15   0    5            0  0x00000012
 1   2    0            0  0x00000002    16   0    6            0  0x0000000E
 2   2    0            0  0x00000003    17   4    0            0  0x00000009
 3   2    0            0  0x00000004    18   0    0            0  0x00000006
 4   2    0            0  0x00000005    19   0    1        53375  0x00000011
 5   0    0            0  0x00000007    20   0    7            0  0x00000016
 6   4    0            0  0x00000008    21   0    7            1  0x00000018
 7   4    0            0  0x0000000A    22   0    7            2  0x00000019
 8   0    0            0  0x0000000C    23   0    7            3  0x00000015
 9   0    2    810627072  0x0000000F    24   0    7            4  0x00000017
10   0    2   1075331072  0x00000010    25   0    7            5  0x00000014
11   4    0            0  0x0000000D    26   0    7            6  0x0000001A
12   0    2  -1071661038  0x0000001E    27   0    7            7  0x0000001B
13   2    3           16  0x00000013    28   0    7            8  0x0000001C
14   2    0            0  0x0000000B    29   0    7            9  0x0000001D
```

### Two correspondences with the catalogue above — by count and shape, not by name

**Eleven entries carry a numeric type** (`2` ×7, `4` ×4): indices 0–4, 6, 7, 11, 13, 14, 17. Section 2
lists **eleven `ACH_COUNT_*` cumulative counters.**

**Ten entries share mode `7` with thresholds `0`–`9`**: indices 20–29. Section 2 lists
**`ACH_SPECIAL_MONSTER01 .. MONSTER10`** — *"a flat, zero-padded run of ten"*.

> **~~Eleven accumulating entries against eleven counter names, and~~ ten parameterised entries against ten
> numbered names.** Both are **count-and-shape matches, not identifications** — no string in this table
> ties an index to a name, and ~~**this document should not treat the correspondence as a mapping until~~
> ~~one is found.**~~ *(corrected 2026-10-02, OPUS: the mapping is found, and it breaks the first match: the record array at `01DFE410` (AB-2) binds the eleven accumulating indices to nine `ACH_COUNT_*` tags plus `ACH_MASTER_LICENSE` (11) and `ACH_COMPLETE_YUGOU` (13), while `ACH_COUNT_STEP` (5) and `ACH_COUNT_CHAIN` (18) have type 0 at `00D10460`, no stored counter; the ten mode-7 entries are `ACH_SPECIAL_MONSTER01`..`10`)* It is stated because two independent runs of the same length and shape is worth
> recording, and because it makes **AB-7** a much narrower question: the ten differ only by a `0`–`9`
> parameter passed to one shared mode.

### AB-1 answered, and the answer is a negative

> **The eleven counter achievements have no threshold in this table.** The accumulate path never reads
> `+0x04`, and every numeric-type entry's threshold field is `0` except index 13, whose `16` is a
> **bit index** for mode 3 rather than a target.

**So whatever decides that a counter has "reached" its goal is not here.** That closes AB-1 as posed
~~and reopens it as *"who compares a counter against a target"*.~~ *(answered: see §7's AB-1 note and the UQ-273 / UQ-274 answers below — the checker `00315E90` compares each counter against the `menuhandbook.bin` override; 2026-10-02, OPUS)*

### A type caution on three thresholds

Indices 9, 10 and 12 carry mode `2` with thresholds `810627072`, `1075331072` and `-1071661038`. Read
as `float`, two of them are plausible (`2.379`, `-2.496`) and **one is not** (`7.6e-10`). ~~**The field is~~
~~compared with a signed-integer `cmp` in the code**, so either these are large integers or they are~~
~~float bit patterns compared as integers — **which is order-preserving only while both operands are~~
~~non-negative, and one of the three has its sign bit set.** The type is **not established** and no~~
~~reading is asserted here.~~ The field is two `u16`s: the evaluator's mode-2 arm takes the low half as `lo` and the high half as `hi`, and awards when every encoded id in `[lo, hi)` answers non-zero to `00309EC0` — `0x3000`–`0x3051` (index 9), `0x4000`–`0x4018` (index 10) and `0xC012`–`0xC01F` (index 12); nothing compares the dword whole *(corrected 2026-10-02, OPUS: `00315E90+0xB6` loads it, `+0xC0` `sar eax, 0x10` and `+0xC3` `movzx edi, ax` take `hi`, `+0xC6` `movzx ebx, cx` takes `lo`, `+0xC9` compares them unsigned, and `+0xD6` calls `00309EC0`; the UQ-273 answer below reads it the same way)*.

### What is not established

- [x] ~~**UQ-273.** What modes `5`, `6` and `7` test — each appears here without an accompanying comparison this
      function performs.~~
      **ANSWERED 2026-09-17 (FABLE): they are tested, but not by the updater - by the checker `00315E90`, whose jump table has an arm per mode.** The updater's type-0 path handles modes 0 and 1 itself and RETURNS for any other mode (`00316A9D cmp ecx, 1 / jne 00316BD1`), which is why 5, 6 and 7 appeared there without a comparison. `00315E90(index)` - called after every accumulate (`00316BC1`) and by the periodic sweep `00316930` for **all thirty indices** (`00316A36`–`00316A43`) - reads the mode byte at `+2`, `cmp eax, 7 / ja`, and dispatches through the table at `00316098`: **0** → value ≥ threshold, the threshold being `003165C0`'s handbook override when non-zero, else `+4`; **1, 4** → nothing (arms at the return label); **2** → the threshold is two `u16`s, and every encoded id in `[lo, hi)` must answer non-zero to `00309EC0` (`BattleEncodedId_DispatchQueryMode0Value`); **3** → the popcount of the 16-bit value ≥ the override or 16; **5** → `003160C0()`: every navigation-map entry flagged in the handbook's hop-1 bitmap (`[022C2550]+8`, bit `n` at `+4+(n>>3)`) is visited (`00255120(n)`), the current field tested by `00255060(…, 0x20)` instead; **6** → `003161A0()`: every id below `0x200` satisfies its bestiary requirement - a keyed record if the handbook lists one (type 0: `FieldData_GetVariable0` ≥ the record's value; type 1: another entry's defeat count above 0), else its own defeat count `00315420(id)` above 0; **7** → the threshold (0–9) indexes the `u16` id list at the handbook's third hop (`00316014`–`00316037`), and that monster's defeat count `00315420(id)` must be above 0. `00315420` is the bestiary byte at save `+0x3404` minus one, as the unlabelled-panes page reads it. On success every arm sets the fired bit at `+0x3844` and calls the notifier with the id-table entry. Static; the jump table's eight targets were decoded from the image and every arm read. **What the ten mode-7 monsters ARE is the handbook's hop-3 list - a DATA read of `menuhandbook.bin`, not done here.**
- [x] ~~**UQ-274.** What `003165C0` returns for mode `0`, which overrides the authored threshold when non-zero.~~ **Answered 2026-09-14 (FABLE):** `003165C0(id)` is a sparse per-achievement lookup into **`menuhandbook.bin`** (kind 7, id `0xC8`). Its loader `003158B0` frees the previous copy and stores the new one at `022C2550` (`003158F8`–`003158FD`). The body (`003165C0`–`0031666B`) does three things:
      1. It follows a chain of relative offsets from blob `+8`: each hop adds the `u16` found at the current position, four hops in all, using 32-bit arithmetic. That reaches a record `R`.
      2. It returns 0 when the blob is absent, a hop sums to 0, `id >= 0x20`, or bit `id` of `R+4` is clear.
      3. Otherwise it counts the set bits of `R+4` below `id` and returns the dword at `R + 8 + 4 × rank`.
      So the mode-0 override is the handbook file's packed per-id value, present only for ids whose bit is set. ~~What the handbook's values mean to the player is not read here.~~ *(Answered by the record read below, reconciled 2026-09-30, SWE2-DATA: they are the achievement targets, for example 300 attacks for Assault Striker, and the handbook's statue descriptions state the same numbers ([the handbook page](../16-UI/Handbook/the-handbook-screen.md)).)*

      **Record read 2026-09-18 (SWE2-DATA), `us` `menuhandbook.bin`:** hop 4 lands at blob `+0xF8`.
      The record there is `u16 0x0040, u16 0x000E`, mask `R+4 = 0x800661FF`, and fourteen dwords at
      `R+8` that fill the file exactly (`R+8+0x38 = 0x138`, the file size). The mask's set bits are
      `{0-8, 13, 14, 17, 18, 31}` - fourteen, matching the dword count. By `003165C0`'s rank rule
      (k-th set bit -> k-th dword), the shipped overrides are:

      | counter id | counter (achievement record) | mode | override |
      |---:|---|---:|---:|
      | 0 | `ACH_COUNT_FIGHT` (Assault Striker) | 0 | 300 |
      | 1 | `ACH_COUNT_MAGIC` (Spellslinger) | 0 | 200 |
      | 2 | `ACH_COUNT_TECH` (Premier Prestidigitator) | 0 | 100 |
      | 3 | `ACH_COUNT_STEAL` (Master Thief) | 0 | 50 |
      | 4 | `ACH_COUNT_KILL` (Blood Dancer) | 0 | 500 |
      | 5 | `ACH_COUNT_STEP` (Wayfarer) | 0 | 50000 |
      | 6 | `ACH_COUNT_GET_GIL` (Plunderer) | 0 | 100000 |
      | 7 | `ACH_COUNT_USE_GIL` (Spendthrift) | 0 | 1000000 |
      | 8 | `ACH_LEVEL_AVERAGE` (Exemplar) | 0 | 50 |
      | 13 | `ACH_COMPLETE_YUGOU` (Mist Walker) | 3 | 8 |
      | 14 | `ACH_COUNT_SELL_EVITEM` (Privateer) | 0 | 1000 |
      | 17 | `ACH_COUNT_SCORE` (Record Breaker) | 0 | 500000 |
      | 18 | `ACH_COUNT_CHAIN` (The Unrelenting) | 0 | 50 |
      | 31 | `ACH_EVENT_FINISH_REX` (For the Homeland) | - | 16 |

      (Counter ids from `members/achievement-descriptors.tsv`; modes from the descriptor table at
      `00D10460` read out of `.rdata`.) Ids 5, 8 and 18 carry `kind = 0` - no save field - so
      `003166F0` returns `-1` and `00316760` resolves them itself (it special-cases 5 and 8 at
      `00316787`/`0031678C`; ~~how id 18's chain count reaches the compare is the consumer side,~~
      ~~not read here~~ *(read 2026-09-30, SWE2-DATA: for id 18, `00316760` returns -1, so the checker's compare never passes. The updater's kind-0 arm compares the value `0028F0C0` passes (§7, AB-7 note) against the override 50 and fires on it, `pf_steam_checks.py` S3–S5)*). Id 13 is mode 3, and its arm (`00315F87`) does consume `003165C0`: Mist
      Walker fires when the 16-bit counter's popcount reaches **8**, not the default 16. Id 31 is
      ~~dead through the engine~~ out of every achievement check's range *(corrected 2026-10-02, OPUS: `003165B0` has callers outside the achievement code, `00572920+0x9E` among them; see the 2026-09-29 correction below)* - the checker refuses `id >= 0x1F` and the updater `id >= 0x1E` - so
      ~~its override ships unread.~~ **Corrected 2026-09-29 (FABLE, GI-2):** no achievement check reads
      its override, but the value is read: the Sky Pirate's Den layout `00572920` calls `003165C0`
      (through the `003165B0` thunk, `005729BE`) with the index of each `0xFF`-keyed `hodr` record,
      and for record 31 the returned 16 is the key of the statue its extra sprite belongs to
      (Ba'Gamnan, record 16, drawn beside it); record 30 has no mask bit and anchors to key 0
      ([the handbook page](../16-UI/Handbook/the-handbook-screen.md#the-sky-pirates-den-and-the-two-data-files-decoded-2026-09-29-fable-gi-2);
      check in `_index/candidates/gi-0929-dialogs/gi2_hcom_hodr.py`).

      **AB-1 test, result:** the prediction was that the mask must cover every counter index
      `{0-4, 6, 7, 11, 13, 14, 17}` - eleven ids. The shipped mask covers ten of them and **leaves
      index 11 clear**. With the descriptor modes read, the picture tightens: the mode-0 ids are
      `{0-8, 11, 14, 17, 18}` (thirteen) and the mask covers every one **except 11**
      (`ACH_MASTER_LICENSE`'s licence counter). For it `003165C0` returns 0, so the mode-0 arm
      falls back to descriptor `+4` = 0 and the check becomes a signed `counter >= 0` on the dword
      at save `+0x384C+0x10` (`kind 4`, so a real stored field): Conqueror fires exactly when that
      field is non-negative. ~~Whether the producer ever leaves it negative is not read here.~~ *(2026-09-30, SWE2-DATA: the updater cannot, because its kind-4 arm clamps a negative sum to 0 (`pf_steam_checks.py` C). Whether any other writer stores that field is `SD-161`: answered 2026-09-30 — no code writes it negative; the load paths copy a save file's or backup's bytes, which is data (OPUS addendum; [record](../_index/candidates/sd161-counter11-writers-0930/README.md)).)*
- [x] ~~Which block `002536A0` returns, and whether `+0x3844` lives in the save payload~~ (**AB-5**) —
  ANSWERED 2026-09-10: `002536A0` returns `*(020927C0)`, which `00253970` sets to the active save buffer
  `+0x8200` (`00253985`–`00253990`) — payload `+0x8000` — so `+0x3844` is payload `+0xB844`, in the image.
- [x] ~~**UQ-275.** Whether the notifier `008632B0` is the Steam call or a queue in front of it.~~ **Answered 2026-09-14
  (FABLE): it is the Steam call, with no queue.** `008632B0(index)` (44 B) fetches the achievement manager singleton
  `[01F83450]` through an 8-byte getter. If the manager exists it tail-jumps into the 137-byte unlock body with
  `(manager, index)` (`008632B8`–`008632D1`). That body:
  1. Indexes a `0x198`-byte record at `[manager+8] + index × 0x198`. If its byte `+0x190` is already set it returns 1.
     Otherwise it sets `+0x190 = 1` and clears `+0x194` (`0020CE67`–`0020CE82`).
  2. Only when the manager's byte `+0x18` is set, calls `SteamInternal_ContextInit` (IAT `008C3190`) and takes context
     slot `+0x28`. That is the user-stats interface UQ-272 counts 17 uses of.
  3. Calls its vtable `+0x38` with the record's `+0x08` pointer as the argument, then tail-jumps its vtable `+0x50`
     (`0020CE9B`–`0020CED2`).

  In the Steamworks `ISteamUserStats` layout those slots are 7 and 10, `SetAchievement(name)` and `StoreStats()`. That
  identification rests on the public SDK's vtable order (tier 6), not on a string in the image. So an unlock is recorded
  in the local `0x198` record and sent to Steam in the same call. Without Steam (`+0x18` clear) only the local record
  changes, and the call returns 0.

## Crossings into other layers — FINAL-AUDIT pass 22 (OPUS, 2026-09-18)

**CombatAI — SERVICE.** `AiOrder_EvaluateTargetSelector` (`00301AD0`), owned by that layer, calls
this page's `BattleEncodedId_DispatchQueryMode0Value` (`00309EC0`) at **`003032E4`**. The callee
answers `0xFFFF` in, `-1` out immediately (`00309EC0`–`00309ED1`), so the selector is asking it a
question about an encoded id. **The crossing is that the AI layer consults this shared query, not
that this page owns anything in CombatAI** — the same helper is accounted the same way from
[the licence-board screen page](../16-UI/License-Board-View/the-license-board-screen-widgets.md).

## Which achievements the scripts award directly, and who awards entry 0 (2026-09-25, FABLE, Claude Opus 5.5)

The native award path is laid out in [the Steam integration contract](CONTRACT-steam-integration-subsystem.md). Its by-index entry `008632B0` is reached, besides the counter bodies, by the script verb **`unkCall_5ad`** (call `0x5AD`, handler `00352250`, one int). A census of every shipped `.ebp` ([`members/script_award_verb_census.py`](members/script_award_verb_census.py)) finds only three indices ever passed:

| index | descriptor | title | where | sites |
|---:|---|---|---|---:|
| 39 | `ACH_TRIAL_MODE_50` | Judge Magister | Trial Mode stage scripts `tri_*` | ~~900~~ 900 code copies (100 files × 9 languages); 9 live, `tri_j05` only *(corrected 2026-10-01, SWE2-DATA, `SD-162`)* |
| 40 | `ACH_TRIAL_MODE_100` | Imperator | Trial Mode stage scripts `tri_*` | ~~900~~ 900 code copies; 9 live, `tri_t05` only *(corrected 2026-10-01, SWE2-DATA, `SD-162`)* |
| 33 | `ACH_EVENT_RETURN_RABANASTRE` | A Traitor Redeemed | `slm_a01` | 9 |

**So Trial Mode awards its two achievements from its own stage scripts, by index, bypassing the counter updater**, and `ACH_COUNT_SCORE` is not among the script-awarded indices (**AB-8** narrowed).

**Descriptor slot 0 is `ACH_CHAMPION_IVALICE`, *Champion of Ivalice*.** No script or counter awards it. The Steam receipt handlers `0020C940` (callback 1101) and `0020C8C0` (1103) award it themselves when every other entry is achieved.

*Static and corpus. ~~Whether a given stage's call site is reached on a stage clear is not established here~~
(`SD-162` answered 2026-10-01, SWE2-ORACLE — all 1,800 sites sit after the `waitv` group-completion post in the shared
director code; each is live in exactly one stage file under its `nowmap()` guard — index 39 live only in `tri_j05`
(stage 50, `nowmap()==0x4CF` after the tenth-stage set), index 40 only in `tri_t05` (stage 100, `nowmap()==0x51F`);
18 live sites, 1,782 statically excluded; record [`sd162-trial-award-path-0930`](../_index/candidates/sd162-trial-award-path-0930/README.md), `sd162_award_path.py` FAILS 0).*

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Script_VM_Native_Bridge — CLIENT (FABLE, Claude Opus 5.5, 2026-09-25).** The script verb `unkCall_5ad` (call `0x5AD`, handler `00352250`) tail-jumps the by-index award entry `008632B0`. Trial Mode and `slm_a01` scripts award achievements 39, 40 and 33 through it (the section above). The script layer decides when; this layer transports the award to Steam.

**CoreRuntimeScheduling — CLIENT.** `FUN_0022a0b0`, owned by that layer, calls `00253970` on this page. That caller is a startup sequence that WRITES the globals the small scheduling getters read - `[02064AA4]`, `[01E02814]` and `[01E0281C]`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — CLIENT (12 edges through 5 of this page's functions).** The UI layer reaches this page at `00263C20`, `0028F0C0`, `00253970`, `003158B0` and 1 more. `FUN_002c7660` is the worked example, read in full - it is a 1,190-byte routine in a `0xD8`-byte frame with a stack cookie and one preserved SSE register; **4 of the 12 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Resource — CLIENT (8 edges, all eight neighbour bodies read).** Three functions cited here reach
the resource layer, and what they reach is that layer's **table lifecycle** rather than any asset.

`0022A0B0` — the startup sequence above — accounts for five of the eight. Two of them are the same
lookup asked twice: `00379E90` and `00259DF0` each load a literal pair into `ecx`/`edx` and call
`0032E400`, and both arrive with **class 9** (`lea ecx, [rdx+2]` from `edx = 7`, and
`lea ecx, [rdx+6]` from `edx = 3`), so they are two entries of one table, not two tables. The other
three are a global set, a global clear and a teardown: `002DF9A0` parks `01E461F0` into
`[0215F000]`; `0032EAE0` is a single instruction, `mov qword [022C51E0], 0 / ret`; `00379D20` runs
`003EAC40` then `00473D20` and tail-jumps to `003EAB60`.

`00253970` reaches the two initialisers. `002494A0` is lazy: it does nothing if `[0208F578]` is
already set, and otherwise points it at `02090910` and zeroes `0x780` bytes. `0024A660` is
unconditional — it zeroes `0x1208` bytes at `0208F580`, which is the table the resource layer's name
lookup walks. And `003158B0` calls `00249180`, which builds an entry through `00249210`, stores the
caller's pointer at `[entry+0x10]` and hands back `[entry+8]`.

So the crossing is that this page's startup and catalogue code initialises, populates and tears down
resource tables. It is a client of that lifecycle; it owns none of it. Read from the shipping bytes
2026-09-14 (OPUS).

**Presentation — CLIENT (4 edges, all four bodies read).** Two of the four are the startup sequence
loading model assets: `0022A0B0` calls `AddMotion_LoadHighModelReplace` and
`AddMotion_LoadSkeletonMapping`, both stack-cookie-guarded loaders. The other two arrive from the
other direction and land on the lookup named above: `003B2310` and `003B53C0` both call `0032E400`.
`003B2310` is gated — if `byte[02EBEBE4]` is set it writes `1` into `[rcx+0x1C]` and returns 1
without looking anything up. `003B53C0` resets four globals (`byte[02B40518]` masked with `0xFC`,
`dword[02B4050C]` to `-1`, `word[02B40508]` and `byte[02B4050A]` to zero) and then asks for
**class 9** — `lea ecx, [rdx-0x21]` with `edx = 0x2A` — the same class this page's own startup asks
for. So the table is shared with the presentation layer rather than owned here. Read from the shipping bytes 2026-09-14 (OPUS).

**RNG_Random_Selection — CLIENT (1 edge, body read).** `0022A0B0` calls `RNG_MT19937_Seed`, which is
five bytes: `jmp 00863D30`, onto the CRT's Mersenne Twister seed. Startup seeds the generator; that
is the whole of the relationship. Read from the shipping bytes 2026-09-14 (OPUS).
- **Audio - CLIENT (115 edges).** `0000001B`, `0000000D`, `00000011` are also called by bodies filed to audio: `007DE120`, `007DE8D0`, `007DDC20` (+110 more) - shared machinery across the layer boundary, no shared ownership.
- **CombatAction - CLIENT (4 edges).** `00309EC0`, `00263C20`, `00320AB0` are also called by bodies filed to combat action: `0030AB40`, `00317BC0`, `00317C80` (+1 more) - shared machinery across the layer boundary, no shared ownership.
- **CombatFormula - SERVICE (1 edge).** `00305A00` reaches bodies filed to combat formula: `00320AB0` - shared machinery across the layer boundary, no shared ownership.
- **Gameplay - CLIENT and SERVICE (3 edges).** `00309EC0` is also called by bodies filed to gameplay: `0031C5D0`; `00315E90`, `00320AB0` reach bodies filed to gameplay: `00309EC0`, `0031B9F0` - shared machinery across the layer boundary, no shared ownership.
- **Input - CLIENT and SERVICE (11 edges).** `0053DD10`, `00000007`, `0000000B` are also called by bodies filed to input: `00862C70`, `00797910`, `007A3110` (+4 more); `00253970`, `007A1CD0` reach bodies filed to input: `00249840`, `0035FF60`, `007A15A0` - shared machinery across the layer boundary, no shared ownership.
- **Movement - CLIENT (2 edges).** `00263C20` is also called by bodies filed to movement: `00335760`, `00338490` - shared machinery across the layer boundary, no shared ownership.
- **Party - CLIENT (1 edge).** `00320AB0` is also called by bodies filed to party: `00304180` - shared machinery across the layer boundary, no shared ownership.
- **Rewards_Progression_Economy - CLIENT and SERVICE (6 edges).** `00316A50`, `00320AB0`, `003171C0` are also called by bodies filed to rewards/progression: `00312280`, `00254EE0`, `002F8BB0`; `0056D370` reaches bodies filed to rewards/progression: `00253690` - shared machinery across the layer boundary, no shared ownership.
- **Status_Periodic_Terminal - CLIENT (1 edge).** `00320AB0` is also called by bodies filed to status/periodic terminal: `00310DB0` - shared machinery across the layer boundary, no shared ownership.
- **World - CLIENT (1 edge).** `0032E400` is also called by bodies filed to world: `00378540` - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT and SERVICE (12 edges).** `0032E400`, `00255060`, `00255120` are also called by bodies filed to world area: `00576A50`, `00268750`, `003319D0` (+4 more); `003154B0`, `003160C0`, `003161A0` reach bodies filed to world area: `00265270`, `003148F0` - shared machinery across the layer boundary, no shared ownership.
## Crossing accounted 2026-09-19 (FABLE): CombatFormula

**CombatFormula - SERVICE.** The developer console's max-LP arm `00305A00` on this page calls
`BattleStats_GetByMappedBattleSlot` `00320AB0`, owned by the CombatFormula layer (49 B, read whole): it resolves a
mapped battle slot, refuses one above `0x27`, and returns `state block + 8 + slot x 0x1C8` - a battle stats record. The
arm calls it in a loop and keeps up to nine record pointers, the records it then writes LP into. Nothing about
achievements crosses; the crossing is that getter.

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../_index/candidates/opus-steam-integration-and-achievement-catalo-ee-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `007DDC20` | 176 B | calls `AcquireSRWLockExclusive` (`008C2308`) on `rcx`+0x90; with `n` = dword [rcx+0x84]: when `n` is at least 4 (signed) calls `ReleaseSRWLockExclusive` (`008C22F8`) on `rcx`+0x90 and returns 0x80004005; otherwise stores `edx` at dword [rcx+0x74+4k] with `k` = (dword [rcx+0x88] + `n`) signed remainder 4, increments dword +0x84, calls `ReleaseSRWLockExclusive` on `rcx`+0x90 and `SetEvent` (`008C2198`) on qword [rcx+0x48]; returns 0 when that is non-zero, else `e` = `GetLastError` (`008C20A8`), returning (`e` AND 0xFFFF) OR 0x80070000 when `e` is greater than 0 (signed) and `e` otherwise | `007DDC42`, `007DDC5A`, `007DDC86`, `007DDC9A`, `007DDCA4` |
