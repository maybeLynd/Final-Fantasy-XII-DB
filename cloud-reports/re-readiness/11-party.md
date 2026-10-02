# Reconstruction readiness — `FFXII TZA/11-Party/`

| | |
|---|---|
| Stream | R (reconstruction readiness), per [`docs/cloud-briefs/re-readiness.md`](../../docs/cloud-briefs/re-readiness.md) |
| Board task | `OPUS-CLOUD-R-READINESS-11-1002` |
| Date | 2026-10-02 |
| Snapshot | this repo's text snapshot only (`df2c9f47`); no executable, Ghidra or live game was used |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every item quotes or paraphrases a page, with its location. Several 11-Party pages are being edited by other lanes; every quotation is the text as `df2c9f47` has it. |

**Counts:** _(filled in when the report is complete)_

Citation form: `page:line`. `page` is the file name inside `FFXII TZA/11-Party/`; the two pages in the subfolder
carry the `Battle-State-Block/` prefix. The ten pages:

| page | lines |
|---|---:|
| `README.md` | 46 |
| `party-roster-and-control-suppression.md` | 707 |
| `active-party-reserve-and-the-moment-the-leader-changes.md` | 664 |
| `the-five-parallel-slot-maps.md` | 376 |
| `the-setsavedata-presets-test-battle-scenarios.md` | 348 |
| `CONTRACT-party-slot-assignment.md` | 463 |
| `CONTRACT-party-focus-and-control-suppression.md` | 366 |
| `CONTRACT-the-five-parallel-slot-maps.md` | 367 |
| `Battle-State-Block/the-battle-state-block-field-map.md` | 634 |
| `Battle-State-Block/CONTRACT-battle-state-block.md` | 297 |

"Not stated" means no 11-Party page says it. Where only another category's page makes a point, the pointer is given
as a path from `FFXII TZA/`. Those pages were not audited for this report.

## Pages read

| page | status as the page states it |
|---|---|
| `README.md` | category index; "Functions \| 79" (`README.md:8`). Lists **three** of the six system pages: the SetSaveData page as "**PARTIAL, tier 1.**" (`README.md:14`), the roster page as "**DOCUMENTED, tier 1.**" (`README.md:18`) and the field map as "**DOCUMENTED, tier 1.**" (`README.md:25`). The active-party page, the slot-maps page and the four contracts are not listed. |
| `party-roster-and-control-suppression.md` | `status: AUDITED` (`:4`); `last_reviewed: 2026-09-12` (`:18`); `audit.last_pass: 2026-09-02`, `falsification-pass` (`:21`–`:22`) |
| `active-party-reserve-and-the-moment-the-leader-changes.md` | `status: AUDITED — both items that kept it PARTIAL are answered … (owner re-status 2026-10-01, OPUS; documented_rule READY)` (`:4`); `last_reviewed: 2026-09-30` (`:19`); promoted DOCUMENTED → AUDITED 2026-10-01 (`:26`) |
| `the-five-parallel-slot-maps.md` | `status: AUDITED` (`:4`); `last_reviewed: 2026-09-03` (`:18`) |
| `the-setsavedata-presets-test-battle-scenarios.md` | `status: AUDITED — the last open box … answered 2026-09-17` (`:4`); `last_reviewed: 2026-09-13` (`:19`) |
| `CONTRACT-party-slot-assignment.md` | `readiness: BEHAVIORALLY UNDERSTOOD`, `confidence: PROVEN` (`:6`–`:7`); `last_reviewed: 2026-09-11` (`:17`); `crossref_clean: false        # audit_crossrefs.py reports nothing for this document` (`:22`) |
| `CONTRACT-party-focus-and-control-suppression.md` | `readiness: CONTRACT READY`, `confidence: PROVEN` (`:6`–`:7`); `last_reviewed: 2026-09-29` (`:21`); falsification pass 1 2026-09-29, "No correction." (`:366`) |
| `CONTRACT-the-five-parallel-slot-maps.md` | `readiness: CONTRACT READY`, `confidence: PROVEN` (`:6`–`:7`); `last_reviewed: 2026-09-29` (`:19`); pass 1 corrected SM-5 and §14 (`:347`–`:367`) |
| `Battle-State-Block/the-battle-state-block-field-map.md` | `status: AUDITED`, `readiness: BEHAVIORALLY UNDERSTOOD`, `confidence: PROVEN` (`:4`, `:8`–`:9`); `last_pass_kind: authored` (`:22`); `last_reviewed: 2026-09-11` (`:17`) |
| `Battle-State-Block/CONTRACT-battle-state-block.md` | `readiness: CONTRACT READY`, `confidence: PROVEN` (`:6`–`:7`); `last_reviewed: 2026-09-29` (`:19`); pass 1 corrected §2 and BS-2/3/5 (`:278`–`:297`) |

**Member `.tsv` files.** They were used only to check layouts and counts. No item below rests on them alone.

| file | what the snapshot holds | agrees with the pages? |
|---|---|---|
| `party-formation-slot-accesses.tsv` | 66 data rows: `00338490` 35 reads + 30 writes, `00339A60` 1 read; displacements `0x0` (11), `0x10`, `0x20`, `0x30`, `0x40`, `0x50` (10 each), `0x24` (5); route `ARRAY 0x022C7E00 stride=0x60 count=4` | yes: the base, stride and count match `party-roster-and-control-suppression.md:512`–`:513`, and `+0x24` and `+0x30/+0x40/+0x50` match `:625`–`:626` |
| `party-roster-slots-accesses.tsv` | 31 data rows in 21 functions. Writes (`w`) in **7** functions: `0025BFB0`, `00266D10` (`00266E1B`), `002695A0` (incl. an indexed `mov qword ptr [r9 + rcx*8], rdx` at `00269628`), `00269C70`, `0026AD90` (`0026ADA0`, `0026ADB9`), `0026CE60` (`0026CF13`), `0026DB30`. **No row for `00266530`.** | **no**: see C-V20 |
| `Battle-State-Block/battle-state-block-accesses.tsv` | **1,135** data rows, **215** functions, **166** distinct displacements; 683 rows / 100 functions / 105 displacements fall in `+0x8`–`+0x4747`; kinds r 710, w 282, rw 69, addr 74; highest displacement `0x7370` | **no**: see C-V21 |
| `Battle-State-Block/route-contamination-removed.tsv` | 91 data rows in 15 functions (`00307300` 33, `00311F70` 13, `00323350` 9, `0030AB40` 7, `00321B00` 5, `0030B7F0` 4, `00321850` 4, `003299B0` 4, then 2, 2, 2, 2, 2, 1, 1) | yes, exactly the per-function counts at `Battle-State-Block/the-battle-state-block-field-map.md:484`–`:485` |

---

## 1. Interface

The category holds five mechanisms that call one another:

- **The roster.** Four actor pointers at `0209A1F0`, mirrored by each record's own slot byte `+0x12`.
- **The focus (the "leader").** A packed actor handle at `022C7FE0`. It is changed by a request that a once-a-frame
  commit applies, and read through a getter that stores nothing.
- **Control suppression.** A per-call recompute from the leader's battle state, published into lock words that the
  stick consumer reads.
- **The party configuration and its four derived slot maps.** These live in the 0x7410-byte battle-state block inside
  the save image, together with the leader selector, the gambit banks and other party state.
- **The SetSaveData apply.** It rebuilds all of the above from two authored tables at area initialisation.

### 1.1 Entry points (functions, with their callers)

#### Roster

| entry | callers | what it does | cite |
|---|---|---|---|
| `PartyRoster_IsFourSlotIndex` `002647C0` | not stated | `i < 4` | `party-roster-and-control-suppression.md:49`, `:212` |
| `PartyRoster_GetActorBySlot` `00263750` | "**43 callers across five subsystems**"; named: `PartyFocus_SelectAndRequestDefaultActor` step 4, `00311E20`, script-VM `003415D0`/`00341CB0`/`00342250` | `(uint)i < 4 ? roster[i] : NULL`, unsigned (`00263753 ja`) | `CONTRACT-party-slot-assignment.md:423`, `:299`, `:404`; `Battle-State-Block/the-battle-state-block-field-map.md:193`, `:417`; `party-roster-and-control-suppression.md:454` |
| `PartyRoster_GetActorBySlotOrCurrentFocus` `00263770` | not stated | sign tested first (`00263776 js`); negative → `003590D0` then `jmp 003588B0` (the current focus); else signed `cmp ecx,4 / jge` | `CONTRACT-party-slot-assignment.md:300`–`:301`, `:404`; `party-roster-and-control-suppression.md:62`–`:74` |
| `PartyRoster_AssignActorToSlot` `00269C70` | `0050C610` (`debug_setpc`) is the only caller named; other callers not stated | eviction notice → vacate the incoming record's old slot → install → stamp `+0x12`/`+0x0F` → new occupant's notice → focus request when no focus is set | `CONTRACT-party-slot-assignment.md:115`–`:133`; `party-roster-and-control-suppression.md:97`–`:106`; `active-party-reserve-and-the-moment-the-leader-changes.md:458` |
| `ActorStorage_InitializeRecord` `00266530`, block `00266740`–`00266792` | not stated | the same protocol from a slot byte; only bytes `0x80`–`0xFE` assign (2026-09-25) | `CONTRACT-party-slot-assignment.md:135`–`:144`; `party-roster-and-control-suppression.md:142`–`:153` |
| bulk clears `002695A0`, `0026DB30` `WorldPersistence_ResetBanksForFieldTransition` | `0026DB30` ← `00266D10`; `002695A0` not stated | zero the 32 bytes; "Both call `003590E0` immediately beforehand" | `CONTRACT-party-slot-assignment.md:151`–`:152`, `:456`; `party-roster-and-control-suppression.md:150`–`:151` |
| `0025BFB0` (pending area-request consumer) | `00314020` (WorldAreaField) | reads mask `[02099ABC]`; zero → return; bit 0 → init callbacks `0026CE60(i)` for i 4..0, then the roster clear; always → unload `002628B0(i)` per set bit | `CONTRACT-party-slot-assignment.md:159`–`:186`, `:457` |
| `002681E0` (the roster-role notice) | `00269C70` (twice), `002681D0`, the focus commit's tail | kind-3 actors only: `+0x152` → a cell class stored at the movement body's `+0x80`, mirrored at `+0x153` | `party-roster-and-control-suppression.md:108`–`:123` |

#### Focus (the leader)

| entry | callers | what it does | cite |
|---|---|---|---|
| `PartyFocus_RequestPackedActorHandle` `003594B0` (3 instructions) | 3: `00269D34` (assign), `0050C646` (`debug_setpc`), tail-jump `003265F6` (`00326500`) | `022C7FE4 = h; 022C7FF8 = 1` | `active-party-reserve-and-the-moment-the-leader-changes.md:203`–`:209`; `CONTRACT-party-focus-and-control-suppression.md:359` |
| `003594C0` (27 B, absent from the function list) | thunk `0034ED30` (`mov ecx, 2; jmp`), stored once at `01EF17C0`, the result slot of verb `0x205` `changetosummonparty` | upgrades an already-pending request to kind 2 (`cmovne`) | `CONTRACT-party-focus-and-control-suppression.md:143`–`:149`; `active-party-reserve-and-the-moment-the-leader-changes.md:271`–`:283`, `:567`–`:578` |
| `PartyFocus_CommitPendingPackedActorHandle` `00358BC0` (156 B) | only via thunk `00358BB0`, 7 callers: frame bodies `0022A770` (`0022AE3C`), `MainLoop_UpdateAndRenderFrame` `0022B8C0` (`0022BAF9`), `0022BC20` (`0022BD49`); `0026CE60` (`0026D2CF`); `0025C830` (`0025D424`); `0026C3E0` (`0026C5A3`); `0050C610` (`0050C64B`) | the change: teardown → re-read pending → store current → clear kind → resolve → tail `002681D0` | `active-party-reserve-and-the-moment-the-leader-changes.md:213`–`:231`, `:458`; `CONTRACT-party-focus-and-control-suppression.md:114`–`:134` |
| `PartyFocus_ClearCurrentActorIfEligible` `00358B40` | the commit | zeroes `022C7FE0` (`00358B6B`); outgoing actor gets `0026D6D0`, `002EC5B0(actor,0)`, `002681D0` | `active-party-reserve-and-the-moment-the-leader-changes.md:242`–`:245` |
| `PartyFocus_ResetState` `003590E0` | `002695A0`, `0026DB30` | zeroes the focus block and both lock words | `active-party-reserve-and-the-moment-the-leader-changes.md:300`; `party-roster-and-control-suppression.md:671`–`:672`; `CONTRACT-party-slot-assignment.md:151`–`:152` |
| `PartyFocus_GetCurrentPackedActorHandle` `003590D0` | 12 Presentation bodies, the audio listener update | `return [022C7FE0]` (two instructions) | `active-party-reserve-and-the-moment-the-leader-changes.md:529`, `:593`–`:597`, `:648`–`:657` |
| `BattleUnit_GetPartyLeader` `003272A0` (55 B) | 28 call sites in 25 functions; named: `00338490`, `00339A60`, `0023B040`, two spawn functions | `02089340 & 0x10` else NULL → resolve handle → BattleUnit → `u[0] & 8` else NULL | `active-party-reserve-and-the-moment-the-leader-changes.md:184`–`:198`, `:590`–`:592`; `CONTRACT-party-focus-and-control-suppression.md:101`–`:108` |
| teardown `0025A6A0` (395 B), via `0025A680` (`r8d=1`) / `0025A690` (`r8d=0`) | the commit: alternate thunk when the outgoing handle is 0 **or** kind is 2 | re-seats camera context 0 in five steps; step 5 (`003D9B80(record+0x10)`, behind-camera reset) only on the alternate path | `active-party-reserve-and-the-moment-the-leader-changes.md:446`–`:455`; `CONTRACT-party-focus-and-control-suppression.md:136`–`:141` |
| `PartyFocus_SetSecondaryPackedActorHandle` `00359410` (154 B) | `00353530`, result callback of verb `0x2B9` `setinterventioncamera` | gives camera record 2 its own context 1 seeded from the target | `active-party-reserve-and-the-moment-the-leader-changes.md:387`–`:421` |
| `PartyFocus_SetTemporaryControlledActorOverride` `003593A0` (97 B) | debug calls `0x2032`/`0x2033` only (`0050D2F0`) | `022C7FEC`; stick consumer and focus update drive that actor instead | `party-roster-and-control-suppression.md:682`–`:686`; `active-party-reserve-and-the-moment-the-leader-changes.md:381`–`:383` |
| `PartyFocus_SelectAndRequestDefaultActor` `00326500` (274 B) | tail of `00327850`; re-run by `00326620`; `003220E0` (re-key) | mode-keyed selector → unit with stats → else four map heads → else roster slot 0 → else 0 → request | `Battle-State-Block/the-battle-state-block-field-map.md:177`–`:204`, `:422`–`:427` |
| `PartyFocus_SetPreferredDefinitionSelectorAndRefresh` `00327850` (21 B) | `00313730` (sequence end), `00280B70` (roster pump) | dword store into `+0x5AA4`, tail into `00326500` | `Battle-State-Block/the-battle-state-block-field-map.md:107`, `:179`–`:181`, `:632` |
| `00327150` (117 B) | not stated | `+0x5AA4` → the unit whose stats record is `block + 8 + sel × 0x1C8` | `Battle-State-Block/the-battle-state-block-field-map.md:198`–`:200` |
| `00358EE0` (175 B, per-frame focus update) | not stated | drives `022C7FEC` or `022C7FE0`; intervention target on camera channel 1 | `party-roster-and-control-suppression.md:686`–`:690` |

#### Control suppression and the lock words

| entry | callers | what it does | cite |
|---|---|---|---|
| `PartyControl_RecomputeSuppressionFromLeaderBattleState` `0023B040` (447 B) | `00234520` (Movement), `00234590` (WorldAreaField) | seed from `02089340 & 0x40`; gate on mode ≠ 2 / field bit 15 / leader; three-bit mask; publishes | `party-roster-and-control-suppression.md:157`–`:190`, `:475`–`:485`; `CONTRACT-party-focus-and-control-suppression.md:151`–`:172`, `:338`, `:345` |
| `0026BD40` (10 B) | `0023B040` tail | `setne [0209A2C5]` | `party-roster-and-control-suppression.md:489` |
| `00359200` (76 B) `PartyControl_SetMovementSuppressionBit` | 5 sites: `00347E14` (`setuclockstatus`), `0023B1DC`, `003071C7`, `0026CC81`..`0026CCBA`, `002628F0`..`002628F9` | `(on, bit)` into dword `022C8000`; if any bit stands, resolve the leader and tail `0026D6D0` | `party-roster-and-control-suppression.md:642`–`:651`, `:669`–`:671`, `:696`–`:699` |
| `00359250` (103 B), `003592C0`, `00359330` (97 B) | `0034E580` (`setucpcmovelockstatus`), the recompute and debug `0x2084`, `00307140` | owner bytes `022C8004`/`022C8005`/`022C8006` | `party-roster-and-control-suppression.md:662`–`:667` |
| stick consumer (window `00358D9B`..`00358E9E`) | not stated | `022C8000` ≠ 0 → speed forced to 0; OR of the four bytes: bit 0 no move, bit 1 no turn (else ≤ 0.3927 rad per call), bit 2 no heading | `party-roster-and-control-suppression.md:642`–`:660` |
| `Actor_StopRequestedMovement` `0026D6D0` (26 B) | the four setters, `00358B40` | zeroes `+0x44/+0x48/+0x4C`, tails `0026D6F0` | `party-roster-and-control-suppression.md:507` |

#### Party configuration and slot maps

| entry | callers | what it does | cite |
|---|---|---|---|
| `PartyConfiguration_CollectRuntimeRosterSelectors0To3` `0031B510` | `00359BA0` | map 3 `[0..3]` selectors; skips `0xFF` and class-`0x17` failures | `active-party-reserve-and-the-moment-the-leader-changes.md:48`–`:71`, `:377` |
| `PartyConfiguration_FindAvailableNonRosterIndex4To8` `00321100` (101 B) | `003172E0`, `003286E0` | probe of map 3 `[4..8]` at `+0x5A86` (polarity disputed: C-V11) | `active-party-reserve-and-the-moment-the-leader-changes.md:66`–`:70`; `the-five-parallel-slot-maps.md:372`–`:376` |
| `003172E0` `…AddSelector00To06ToAvailableIndex4To8` | script-VM `0034C370` | duplicate scan of map 0, then an index 4–8 via `00321100` | `active-party-reserve-and-the-moment-the-leader-changes.md:159`–`:163`; `the-five-parallel-slot-maps.md:315` |
| `003170E0` `…AddSelector07To25ToAvailablePrimaryIndex` (211 B) | not stated | duplicate scan of map 0; first `0xFF` of map 3 indices 3, 2, 1 (never 0); tail to `PartyConfiguration_SetEmptyIndexSelector` with final argument 1 | `active-party-reserve-and-the-moment-the-leader-changes.md:431`–`:438` |
| removers `00328B20` (`…00To06`), `003288F0` (`…07To25`) | `003288F0` ← `00352AF0` (verb `0x35C` `removeguestbattlemember`) | stage to `022C2580`, clear slot, release member, reconcile (0) → pooled refresh | `CONTRACT-the-five-parallel-slot-maps.md:146`–`:160`; `the-five-parallel-slot-maps.md:137`–`:149`; `active-party-reserve-and-the-moment-the-leader-changes.md:378` |
| `PartyConfiguration_ReconcileRosterFromCurrentSelectors` `003261D0` | removers, `00326110` | compacts staged selectors, writes map 0 back; argument bit 0 clear → pooled-task refresh | `CONTRACT-the-five-parallel-slot-maps.md:150`–`:156` |
| `PartyConfiguration_SetDefinitionSelectorForIndex` `00329080` | `00239960` (`(i, byte, 3)`) | writes map 0 (`00329122`) — body not described | `Battle-State-Block/the-battle-state-block-field-map.md:87`; `the-setsavedata-presets-test-battle-scenarios.md:104`–`:105` |
| `BattleSlotMap_ResolveMappedBattleSlot` `0031B9F0` (200 B) | wrappers `0031FE70`/`00320040` (swap ecx↔edx), `00320AB0` (forwards) | `(id, class)` → low byte of map *class* entry *id*; `0xFF` on bad id or class | `CONTRACT-the-five-parallel-slot-maps.md:47`–`:77`, `:288` |
| `BattleUnit_FindMappedDefinitionSelectorByIndex` `0031B810` | `00338490`, `00388D50`, `0030F275`, `002F8BB0` … | map 1 byte (`+0x5A5A + 2i`), then tail `002367A0`; `0xFF` substitute on failure | `party-roster-and-control-suppression.md:555`–`:561` |
| `BattleSlotMap_InitializeMappingClasses` `00329CC0` | `00237DF0` at `00237E41` | conditional fill of map 0 from `01EED260`, `+0x5AA4 = table[0]`, copy into maps 1–4 | `CONTRACT-the-five-parallel-slot-maps.md:86`–`:100`; `Battle-State-Block/CONTRACT-battle-state-block.md:50` |
| `BattleGroup_RefreshFourActorDefinitions` `003266C0` | `00233CF0`; pooled-task tail after a reconcile | ordered copies 0→1, 0→3, clear 1 `[4..8]`, 1→2, 1→4; then mode arms | `CONTRACT-the-five-parallel-slot-maps.md:102`–`:133`; `Battle-State-Block/CONTRACT-battle-state-block.md:264` |
| `00320890(sel)` (47 B), `0030A970(out)` (131 B), `00320800` (144 B), `00359C00`, `00359BA0` | not stated | index of a selector; filled-active mask; non-guest collector; bit masks | `Battle-State-Block/the-battle-state-block-field-map.md:154`–`:156`; `active-party-reserve-and-the-moment-the-leader-changes.md:375`–`:377` |

#### Battle-state block

| entry | callers | what it does | cite |
|---|---|---|---|
| binder `00233C10` (214 B) | `00394130` (`00394222`), `00280140` | unbound: bind to active buffer `+0x4E68C`, rebase inventory, `00237DF0` **twice**; bad magic: `00237DF0` once; good magic: proceed | `Battle-State-Block/CONTRACT-battle-state-block.md:75`–`:87`, `:259`; `the-setsavedata-presets-test-battle-scenarios.md:194` |
| `BattleSystem_ResetRuntimeState` `00237DF0` (173 B) | the binder; `00239960` for set byte −2 | `0023AF50` → `002370C0`; forty stats records; `00329CC0` at `00237E41`; `00313840` | `Battle-State-Block/CONTRACT-battle-state-block.md:50`, `:274`; `the-setsavedata-presets-test-battle-scenarios.md:75`–`:76` |
| reset `002370C0` (121 B) | `0023AF50`; `00239960` at `002399E9` | memset `0x7410`, magic, map 0 = `0xFFFF`, zero `+0x5AC8`/`+0x5ACC` | `Battle-State-Block/the-battle-state-block-field-map.md:49`–`:52`; `Battle-State-Block/CONTRACT-battle-state-block.md:89`–`:108` |
| export `00234ED0` (489 B) / import `00235AF0` | `00229B40`, `005844A0` / not stated | selected bank ↔ stats record `+0x88` through the `0x6000` compatibility copy | `Battle-State-Block/the-battle-state-block-field-map.md:251`–`:277` |
| gambit banks `00326030`, `00327C40`, `003282D0` | `0023AF03`, `00328D04` (→ `resetJobs`) for `00326030` | three `0x34` banks per member; selected index at `+0x7370` | `Battle-State-Block/the-battle-state-block-field-map.md:124`–`:138`, `:403`–`:411` |
| sequence `00306760`, `00313600`, `00313840`, `00313730` | not stated | the Esper summon's state at `+0x5AD0`–`+0x5ADF` | `Battle-State-Block/the-battle-state-block-field-map.md:158`–`:166` |

#### Follow formation

| entry | callers | what it does | cite |
|---|---|---|---|
| `PartyFollow_SolveFormation` `00338490` (4,101 B) | not stated | for slots 0..3, skip no-unit / status `0x80000003` / leader; fill a keyed slot (index, position, angle in `[0, 2π)`, unit) | `party-roster-and-control-suppression.md:515`–`:529`, `:628` |
| `PartyFollow_LookupDestination` `00339A60` (390 B) | not stated | no leader / is leader / leader stats `+5 != 1` → none; else search `022C7E00`..`022C7F80` by `+0x00 == unit+0xEA9` | `party-roster-and-control-suppression.md:531`–`:542` |

#### SetSaveData

| entry | callers | what it does | cite |
|---|---|---|---|
| `btlAtelSetNextSetSaveData` `0050F810` / `…Get…` `0050F830` | verbs `302B` / `302C`; shipped `naf_b04` (set 1) and `evt_t0505` (sets 0–3) | store / read the byte `0208D455` | `the-setsavedata-presets-test-battle-scenarios.md:64`–`:70`, `:195`–`:203` |
| `00394130` (task proc) | `fsttl_newgamestart` (`705D`) via `00394640` | validate, reset or bind the save image; sets the byte | `the-setsavedata-presets-test-battle-scenarios.md:189`–`:195` |
| apply `00239960` | `BattleSystem_InitializeAreaState` `002342F0` | five-step rebuild (§1.4) | `the-setsavedata-presets-test-battle-scenarios.md:72`–`:107`; `Battle-State-Block/CONTRACT-battle-state-block.md:276` |

### 1.2 Inputs and outputs (data read and written, with record layouts)

#### The roster and its record fields

```
0209A1F0  ActorStorageRecord*[4]   image storage, never freed; 32 bytes                     CONTRACT-party-slot-assignment.md:56
ActorStorageRecord
  +0x0F  u8   2 while the record holds a slot 0..3, 3 otherwise = (slot > 3 unsigned) + 2    :63, :131-132, :280-283
  +0x12  i8   own slot, 0xFF = unassigned; read movsx then compared UNSIGNED                   :62, :66-71
  +0xC0  ptr  secondary (movement) context                                                     :64; party-roster…:112-116
secondary context
  +0x138 ptr  movement body; body +0x80 = cell class                                           party-roster…:112-116
  +0x152 u8   roster-role byte: 1 evicted / (re)init, 2 refresh variant, 0 installed, 3 dead arm  party-roster…:118-123
  +0x153 u8   mirror of the derived class; 0xFE on init                                         party-roster…:111, :120
```

Derived class (`002681E0`, kind-3 actors only): role `1` → 2; `2` → 3; `0` → 0 for the focus actor (unless `+0x0C` bit 4
and `00265680()` hold, or `002672B0()` fails → 1), 1 for every other member; **5 whenever mode 2 holds**
(`party-roster-and-control-suppression.md:118`–`:123`).

#### The focus block and the lock words

```
022C7FE0  u32  current packed handle = the leader   writers 00358C2F (commit), 00358B6B (clear), 003590FD (reset)
022C7FE4  u32  pending handle
022C7FE8  u32  secondary handle = intervention-camera subject   8 accesses, 3 writers
022C7FEC  u32  debug player-character override (no shipped script sets it)
022C7FF8  u8   request kind: 0 none, 1 normal, 2 summon
022C8000  u32  STOP word: bit 0 setuclockstatus, 1 leader battle state, 2 event lock 00307140, 3 manager slot 3 loaded
022C8004..07 u8[4]  steering owner bytes: script, leader battle state (+debug), event lock (bit 1), nobody
```

Cites: `CONTRACT-party-focus-and-control-suppression.md:64`–`:69`, `:87`–`:91`, `:364`;
`party-roster-and-control-suppression.md:642`–`:667`, `:682`–`:690`;
`active-party-reserve-and-the-moment-the-leader-changes.md:439`–`:443`.

#### The gate words

```
02089340  bit 0x10  "the area's battle state is live" (outside it there is no leader)    active-party…:459-464
          bit 0x40  "a treasure is being opened" (suppression seed)                     party-roster…:220, :317-323
          bits 0x600 the party-down bits                                                 CONTRACT-party-focus…:74
02089344  bit 0 restart flag (binder); bits 1, 2 deferred requests folded into block +4 bits 13, 14   field-map:303; setsavedata:80-82
```

#### What the leader-side readers take from a BattleUnit and its stats record

| field | use | cite |
|---|---|---|
| BattleUnit `+0x698` | stats record pointer; null-checked twice of three loads in `0023B040` | `CONTRACT-party-focus-and-control-suppression.md:161`–`:165` |
| BattleUnit `+0x6B4`, `+0x6B7`, `+0x714` (vs `0x21E`) | action state, combo counter, action id (owned by the combo contract) | `CONTRACT-party-focus-and-control-suppression.md:167`–`:172` |
| BattleUnit `+0xEA9` | the follow lookup's key | `party-roster-and-control-suppression.md:541`–`:542` |
| BattleUnit `u[0] & 8` | leader validity | `active-party-reserve-and-the-moment-the-leader-changes.md:193` |
| stats `+0x3C`, `+0x64` | the two status words ORed and tested against `0x80000003` (gate) and `0x8800403B` / `0x8800003B` (mask bits 0, 2 / bit 1) | `CONTRACT-party-focus-and-control-suppression.md:151`–`:157`; `party-roster-and-control-suppression.md:522`, `:528`–`:529` |
| stats `+0x05` | kind byte, "0 party, 1 spawn-backed" | `party-roster-and-control-suppression.md:539` |

#### The battle-state block (0x7410 bytes, `[02EBF190]`, payload `+0x4E48C`)

| offset | field | cite |
|---|---|---|
| `+0x0000` | u32 magic `0x05071901` | `Battle-State-Block/the-battle-state-block-field-map.md:29`–`:30`, `:347` |
| `+0x0004` | u32 flags: bits 0–8 discovery (set only), 11 command fan-out, 12–14 area/script; 9, 10, 15–31 no writer | `…field-map.md:297`–`:307` |
| `+0x0008` | `BattleStatsRecord[40]`, stride `0x1C8` | `…field-map.md:66`–`:71` |
| `+0x4748`–`+0x4F9F` | inventory class regions (items 64 w, equipment 420 w, loot 512 w, magick/technick/condition/key-item/quickening bits) | `…field-map.md:220`–`:229` |
| `+0x4F84`, `+0x5004` | inventory backups A and B (`+0x534C`–`+0x57BF` unused mirror) | `…field-map.md:84`–`:85`, `:449`–`:453` |
| `+0x57C0`, `+0x57C8`–`+0x59C7` | items ever-owned bitset; loot sold tally | `…field-map.md:454`–`:455` |
| `+0x59C8` | 128 bazaar flag bytes | `…field-map.md:86` |
| `+0x5A48` | map 0: nine u16 party selectors, `0xFFFF` empty; `[0..3]` active, `[4..8]` reserve | `…field-map.md:87`; `CONTRACT-the-five-parallel-slot-maps.md:55`–`:59` |
| `+0x5A5A`, `+0x5A6C`, `+0x5A7E`, `+0x5A90` | maps 1–4, same format, derived | `…field-map.md:91`–`:106` |
| `+0x5AA4` | u32, preferred definition selector = leader (low byte; upper bytes always 0) | `…field-map.md:107`, `:373` |
| `+0x5AC8` / `+0x5ACC` | f32 + i32 walked-distance accumulator, cap 99,999,999 | `…field-map.md:108`–`:109` |
| `+0x5AD0`, `+0x5AD4`, `+0x5AD5`, `+0x5AD8`, `+0x5ADC` | summon sequence: flags, Esper row, summoner selector, timers A/B | `…field-map.md:110`–`:114`, `:166` |
| `+0x5AE0`–`+0x5AEC` | event-party word, chocobo ride time (180.0f), turbo time (10.0), last turbo argument | `…field-map.md:115`–`:118` |
| `+0x5B00`, `+0x5B0C`, `+0x5B0E` | formula echoes A (walk mod 1000), C (bank, cap 60,000), B (streak 0–17) | `…field-map.md:119`, `:122`–`:123` |
| `+0x5B04`, `+0x5B08` | mode flags (bit 0 UI, 1 combat/audio, 2 `seteventpartymode`, 3 `seteventparty2mode`); previous mode | `…field-map.md:120`–`:121` |
| `+0x5B10` | gambit banks `[40][3] × 0x34` (12 `{u16 cond, u16 action}`, `+0x30` u16 mask, `+0x32` u8 count) | `…field-map.md:124`–`:138`, `:396`–`:402` |
| `+0x7370` | i32[40] selected bank per member, to `+0x740F` | `…field-map.md:138` |

#### The follow-formation slots

`PartyFormationSlot`, `ARRAY 0x022C7E00 stride=0x60 count=4`: `+0x00` u8 slot key (`0xFF` written to all four before each
solve); a homogeneous position, an angle and a `BattleUnit*` per slot. "**NOT CLAIMED:** what the three `movaps`
vectors at slot `+0x30`, `+0x40`, `+0x50` hold, or what the second float at `+0x24` is"
(`party-roster-and-control-suppression.md:512`–`:513`, `:525`–`:526`, `:546`–`:549`, `:625`–`:626`).

#### The camera contexts the focus teardown and the secondary handle write

Two `0x860`-byte contexts at `02097D20`: `+0x10` the behind-camera object, `0xB0` pose blocks at `+0x6F0` / `+0x7A0`,
blend factor `+0x850`, dword `+0x854`. Camera-record stack `02097300`: eight `0x110` records, `+0xF4` = the context
index (`active-party-reserve-and-the-moment-the-leader-changes.md:405`–`:416`). The install `0025A180` copies the
movement body's placement record `+0x30`..`+0xDF` into `+0x7A0` and sets word `+0x690 = 4` (`:451`, `:457`;
`CONTRACT-party-focus-and-control-suppression.md:310`).

#### The SetSaveData tables

```
0208D455  i8  pending set: -1 none, n >= 0 apply once, -2 reset only; copied to 0208D456 when applied
ScenarioRow (02EBF030, 50 x 208, rows at file 0x29300):
  +0x00 u8 slot[9] ; +0x09 u8 (no reader) ; +0x0A u8 selector -> 00327870 ; +0x0B u8, +0x0C u16 (no reader) ;
  +0x0E u16 gil ; +0x10 u16 item[64] ; +0x90 u8 count[64]
PartyPresetRow (02EBF028, 226 x 44, rows at file 0x26C00):
  +0 u8 scenario ; +1 u8 battleSlot ; +2 u8 level ; +3 u8 -> record +0x20 (rank) ; +4 u16 equip[5] ;
  +0xE u16 gambitPreset (0x5000+row) ; +0x10..+0x1F zero ; +0x20 u16 lp ; +0x22..+0x27 zero ; +0x28 u8 mpPercent
```

Cites: `the-setsavedata-presets-test-battle-scenarios.md:46`, `:111`–`:123`, `:155`–`:161`, `:206`, `:244`–`:250`.

#### Outputs

| output | written by | consumed by | cite |
|---|---|---|---|
| `0209A2C5` | `0026BD40` from `0023B040` | not stated | `party-roster-and-control-suppression.md:484`–`:485`, `:489` |
| `022C8000` bit 1, `022C8005` | `0023B040` via `00359200` / `003592C0` | the stick consumer | `party-roster-and-control-suppression.md:185`, `:649`, `:665` |
| `[0208E6B8]` | `0023B040` (`0023B22F`–`0023B238`) | **not stated** (meaning not stated) | `party-roster-and-control-suppression.md:483` |
| movement body `+0x80` cell class | `002681E0` | placement resolver `00380D30` | `party-roster-and-control-suppression.md:112`–`:116` |
| render record `word[[022C6F28]+0x4882C]` | Presentation readers of the focus (`0` → `-1`) | Presentation | `active-party-reserve-and-the-moment-the-leader-changes.md:652`–`:656` |
| camera contexts 0 / 1, record 2 `+0xF4` | the teardown, `00359410` | the camera | `active-party-reserve-and-the-moment-the-leader-changes.md:410`–`:421` |

### 1.3 State (globals and objects, with lifetime)

| state | lifetime and initial value | cite |
|---|---|---|
| roster `0209A1F0` | image storage, never freed; zeroed by `002695A0`, `0026DB30` (field transition) and `0025BFB0`'s bit-0 arm; **the bulk clears touch no record**, so records keep their slot | `CONTRACT-party-slot-assignment.md:56`, `:90`–`:95`, `:151`, `:196`–`:197` |
| record `+0x12` / `+0x0F` | per record; initial value of `+0x12` before any assignment **not stated** | `CONTRACT-party-slot-assignment.md:62`–`:63` |
| focus block `022C7FE0`–`022C7FF8` | static; zeroed by `003590E0`; whether it is saved: **not stated** | `active-party-reserve-and-the-moment-the-leader-changes.md:300` |
| lock words `022C8000`–`022C8007` | static; cleared by `003590E0` | `party-roster-and-control-suppression.md:671`–`:672` |
| battle-state block | inside the save image (static buffer `02164280`, size `0x56690`), at `+0x4E68C`; saved whole; reset when unbound or on bad magic | `the-five-parallel-slot-maps.md:215`–`:230`; `Battle-State-Block/CONTRACT-battle-state-block.md:70`–`:87` |
| compatibility copy | first `0x6000` bytes at buffer `+0x2200`, written on world-transition capture and save prep | `Battle-State-Block/the-battle-state-block-field-map.md:239`–`:262` |
| staging pair `022C2580`/`022C2590` | 18-byte copy of map 0 during removal | `the-five-parallel-slot-maps.md:141`–`:144`; `CONTRACT-the-five-parallel-slot-maps.md:148` |
| pooled-task pool | 32 entries, bitmask `022BE7C0` | `CONTRACT-the-five-parallel-slot-maps.md:154` |
| formation slots `022C7E00` | rewritten each solve (`0xFF` keys first) | `party-roster-and-control-suppression.md:547`–`:549` |
| pending set byte `0208D455` | set by verb or `00394130`; initialised at `00236A04`; carried across field transitions in the snapshot record | `the-setsavedata-presets-test-battle-scenarios.md:64`–`:70` |

### 1.4 Order (what runs when, and what triggers it)

- **Leader change.** A request (`003594B0`) stores the pending handle and kind 1. `changetosummonparty` may then upgrade
  it to kind 2. The commit runs "once a frame, from whichever of the three mode frame bodies runs, so a read of the
  leader after that call sees the new one and a read before it the old"
  (`active-party-reserve-and-the-moment-the-leader-changes.md:253`–`:254`, `:458`). Within the commit the order is
  fixed: `00358C24` re-read pending → `00358C2F` store → `00358C35` clear kind → `00358C3C` resolve → `00358C52`
  tail-call (`CONTRACT-party-focus-and-control-suppression.md:128`–`:134`). A commit that changes nothing still runs
  the store and the push (PF-4, `:123`–`:126`). The only synchronous path is `debug_setpc` (PF-3, `:114`–`:121`).
  Where the commit falls relative to the other steps of those frame bodies: **not stated**.
- **Assignment.** The eviction notice runs first, then the vacate, install, stamp, the new occupant's notice, and a
  focus request when no focus is set (`CONTRACT-party-slot-assignment.md:115`–`:133`;
  `party-roster-and-control-suppression.md:97`–`:106`).
- **Suppression.** Recomputed by `0023B040` on calls from `00234520` and `00234590`. When those run within a frame is
  **not stated**; the roster page's own chain begins "leader battle state changes" (`party-roster-and-control-suppression.md:274`).
  Inside it: the seed, the mode-2 / bit-15 / leader gate, the leader's contributions, then "**A later mode-1 gate**
  (`003135C0`) can replace the whole mask" (`:189`–`:190`), then publish. The setters stop the actor on the frame a
  lock is set (`:669`–`:671`).
- **Removal.** Stage → release → reconcile(0) → pooled task → refresher, in one call; maps 1–4 stay stale only when the
  32-entry pool is full (`CONTRACT-the-five-parallel-slot-maps.md:147`–`:160`).
- **Bind and reset.** The binder runs on load / new-game (`00394130`); unbound: `00237DF0` twice; bad magic: once
  (`Battle-State-Block/CONTRACT-battle-state-block.md:75`–`:87`).
- **Area initialisation.** `002342F0` → `00239960`. If the set byte is ≥ 0 and within the table: reset (`002370C0`,
  keeping flag bits 12–14) → forty stats records → gil, clear inventory, 64 items → every preset row of that scenario
  → nine formation selectors via `00329080(i, byte, 3)` → `00327870(R.u8[+0xA])` → `002CFD10(−1)`
  (`the-setsavedata-presets-test-battle-scenarios.md:72`–`:107`).
- **The summon sequence.** Started by `00313600` and ended by `00313840` (UI) or `00313730` (end and prefer). The field
  frame's steps 15 and 20 read it (`Battle-State-Block/the-battle-state-block-field-map.md:160`–`:166`).
- **Focus default selection.** Runs at the tail of every `+0x5AA4` write (`00327850`) and every handle re-key (`003220E0`)
  (`Battle-State-Block/the-battle-state-block-field-map.md:179`–`:204`).

### 1.5 Dependencies (on other systems)

| system | what 11-Party uses from it | cite |
|---|---|---|
| Battle runtime mode ladder (00) | `0030D9A0` mode 0..5; mode 2 = chocobo ride, mode 3 = field bit 15, tested first | `party-roster-and-control-suppression.md:223`, `:414`–`:418` |
| Field record table (03) | `FieldData_GetActiveFieldRecordBit15`; `00377C70` (bits 4–6 of the field record's third byte, mode 3's focus selector) | `party-roster-and-control-suppression.md:200`–`:206`; `Battle-State-Block/the-battle-state-block-field-map.md:434`–`:438` |
| Actor registry and pool (04) | packed handles, `ActorHandle_ResolveRegistryEntryByPackedId`, `002367A0`, `0031B770`, manager slots, `0026CE60` / `002628B0` | `active-party-reserve-and-the-moment-the-leader-changes.md:188`–`:194`; `party-roster-and-control-suppression.md:563`–`:585` |
| Movement (06) | the movement body and its cell class, `0026D6D0`, the placement resolver `00380D30` | `party-roster-and-control-suppression.md:112`–`:116`, `:507` |
| Combat action (07) | the combo fields read by suppression | `CONTRACT-party-focus-and-control-suppression.md:167`–`:172` |
| Combat formula / stats (08) | `BattleStatsRecord` layout, `BattleStats_InitializeDefinitionRecord`, `BattleEncodedId_IsValidForClass` class `0x17` | `Battle-State-Block/the-battle-state-block-field-map.md:66`–`:71`; `CONTRACT-the-five-parallel-slot-maps.md:79`–`:84` |
| Gambits (09) | the bank format and rebuild | `Battle-State-Block/the-battle-state-block-field-map.md:396`–`:411` |
| Status (10) | the meaning of bits 0, 1, 31 (KO, Stone, X-Zone) | `party-roster-and-control-suppression.md:332` |
| Items (12) | inventory class descriptors at `01EEBCC0`, rebaser `0030B6A0` | `Battle-State-Block/the-battle-state-block-field-map.md:216`–`:236` |
| Input (15) | the full suppression mask contributions are deferred to "the policy page §10" | `party-roster-and-control-suppression.md:184`–`:187` |
| Camera (17) | the two camera contexts and the record stack | `active-party-reserve-and-the-moment-the-leader-changes.md:405`–`:421` |
| Save image (19) | the static buffer, `SaveImage_GetActiveBuffer` `002EF640`, the transition record | `the-five-parallel-slot-maps.md:215`–`:247` |
| Script VM (01) | verbs `changetosummonparty`, `setinterventioncamera`, `setuclockstatus`, `setucpcmovelockstatus`, `removeguestbattlemember`, `btlAtelSetNextSetSaveData`, `debug_setpc` | sections above |
