# Reconstruction readiness, pass 2 — `FFXII TZA/05-Spawn-Encounter-Lifecycle/` (slug `05-spawn`)

| | |
|---|---|
| Stream | R2 (reconstruction readiness, pass 2), per [`docs/cloud-briefs/re-readiness-r2.md`](../../docs/cloud-briefs/re-readiness-r2.md), part A |
| Pass 1 | [`cloud-reports/re-readiness/05-spawn.md`](../re-readiness/05-spawn.md), snapshot `4da4b9d0`, 2026-10-02 |
| This pass | snapshot `b23bdddd` (synced from XIIOnline `f9d9053b9`), 2026-10-03 |
| Working for | FABLE |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every verdict quotes or cites a page line; no executable, Ghidra or live game was used. |

## Citation form

`ABBR:line` is a line of the page **in this snapshot** (line numbers moved since pass 1; every cite below was re-taken).
Paths are relative to `FFXII TZA/05-Spawn-Encounter-Lifecycle/` unless they start with `../`.

| abbr | page |
|---|---|
| README | `README.md` |
| SPR | `spawn-placement-and-retirement.md` |
| HT | `spawn-placement-height-and-authored-tunables.md` |
| WHY | `why-the-enemies-you-killed-come-back.md` |
| C-SP | `CONTRACT-spawn-placement.md` |
| C-GC | `CONTRACT-group-completion-and-respawn.md` |
| GC | `Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md` |
| FM | `Spawn-Record/the-spawn-keep-entry-field-map.md` |
| OQ | `../_index/OPEN-QUESTIONS.md` (the register) |
| TICK | `../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md` |
| S16 | `../25-EBP-Script-Container/Sections/section-016.md` |
| RNG | `../21-RNG-And-Determinism/rng-streams.md` |
| ENM | `../09-Combat-AI-And-Gambits/CONTRACT-enmity.md` |
| UDEF | `../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md` |
| BUFM | `../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md` |
| KIND | `../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md` |
| HEAD | `../06-Movement-And-Navigation/heading-speed-to-position-delta.md` |
| SET | `../19-Save-Load-Settings/Game-Settings-Config/the-settings-command-table.md` |
| BSB | `../11-Party/Battle-State-Block/the-battle-state-block-field-map.md` |
| CONV | `../01-Script-VM-Native-Bridge/Spawn-Verbs/the-script-to-native-calling-convention.md` |

**What changed since pass 1.** `git diff 4da4b9d0 HEAD` over the folder is +471 / −102 lines in all eight pages, almost all of
it OPUS's dated corrections of 2026-10-02 (which settle most of pass 1's §2.3 contradictions) and two new contract sections of
2026-10-03: C-SP §7a "Range retirement, the return window and the keep-bank rotation" (`C-SP:146-417`) and C-GC §10a "The
cooldown clock across a runtime reset and a load" (`C-GC:419-509`). No register row owned by this folder changed state.

**How verdicts were chosen.**
- Pass 1 scoped "not stated" to the eight pages of this folder. Where the answer was already on another page **before** pass 1
  (checked with `git show 4da4b9d0:<page>`), the item is **WRONG-IN-PASS-1** if that page answers it whole, and **NARROWED**
  if it answers part; either way the folder still lacks the pointer, which the row says.
- A "field written but left unexplained" whose page already states it is never read is **WRONG-IN-PASS-1**: a port needs the
  write, not a purpose.

## 1. Summary

| pass-1 group | items | CLOSED | NARROWED | OPEN | WRONG-IN-PASS-1 |
|---|---:|---:|---:|---:|---:|
| §2.1 open items the pages list | 14 | 0 | 3 | 11 | 0 |
| §2.2 structural gaps G1–G16 | 16 | 1 | 7 | 4 | 4 |
| §2.2 fields written but unexplained (F1–F9) | 9 | 0 | 1 | 1 | 7 |
| §2.3 A, value-changing contradictions | 18 | 17 | 1 | 0 | 0 |
| §2.3 B, counts and sizes | 5 | 3 | 0 | 2 | 0 |
| §2.3 C, stale claims, banners, names | 25 | 19 | 0 | 4 | 2 |
| **total** | **87** | **40** | **12** | **22** | **13** |

**New gaps (§3): 12** — DOC 7, STATIC 3, DATA 1, RUNTIME 1.

**Open and narrowed items by class** (the 34 OPEN or NARROWED pass-1 items, by what is still missing): RUNTIME 6
(§2.1 items 1–5, and 8's live half is not claimed), STATIC 17, DATA 3, DOC 8. Each row in §2 gives its class.

**Rating: NOT YET → NOT YET**, but narrower. Pass 1 rated two parts MOSTLY (the group ledger; the keep entry and bank rotation)
and placement-and-retirement NOT YET. Now **retirement** has a contract section with offsets, writers, both senses and executed
cases (C-SP §7a), and the clock's advance is stated, so three of four parts are MOSTLY. **Placement** alone keeps the system
at NOT YET: the region containment test `002374E0`, the selector's lane-and-candidate loop and the two undescribed selectors
(G2, G3, G5). See §4.

## 2. Pass-1 gaps

Ids are pass 1's: §2.1 items 1–14, §2.2 G1–G16, the §2.2 table "Fields written by documented functions but left unexplained"
(numbered F1–F9 here in pass 1's row order), and §2.3 A1–A18, B1–B5, C1–C25. "Class" is given for every OPEN and NARROWED
row (STATIC / RUNTIME / DATA / DOC); a register row is named with its state where one tracks the gap.

### 2.1 Open items the pages list (pass 1 §2.1)

| id | gap (pass 1) | verdict | evidence now | still missing | class |
|---|---|---|---|---|---|
| 1 | L-12, the area-path acceptance word | OPEN | "what that word actually holds in ordinary play — still live-only" (`SPR:1513`); "*Not established:* which values the slot holds in ordinary play. That is `L-12`'s live question" (`C-SP:103`, again `C-SP:419`). Register `L-12` **SUPERSEDED** 2026-09-26, "the static reading is complete" (`OQ:339`) | the value of the uninitialised `out_observed` stack slot in ordinary play | RUNTIME (`L-12` SUPERSEDED) |
| 2 | L-13 live residue | OPEN | "**What stays unobserved is live only:** a slot-0 field-transition autosave load with …" (`SPR:781`); "still without a carrier" (`SPR:786`); "those are live questions" (`WHY:112`). Register `L-13` **SUPERSEDED** 2026-09-27 (`OQ:340`) | a slot-0 autosave load with non-zero keep banks, and whether the requeued rotation brings the same enemies back | RUNTIME (`L-13` SUPERSEDED) |
| 3 | area-mode Y in practice | OPEN | `HT:722` (895 of 954 definitions leave the probe bit clear); `C-SP:109-111` "in area mode **`result.y` is uninitialised stack**". Register `UQ-100` **SUPERSEDED** 2026-09-26, static and data halves closed (`OQ:2814`) | the stale stack value in play | RUNTIME (`UQ-100` SUPERSEDED) |
| 4 | the modded attempt skip; no live placement evidence | OPEN | "**Whether the modded skip is reachable unmodified** **[FALSIF]**" (`C-SP:420`); "**No live evidence** for placement **[live]** — EXP-145 is original-code execution on planted …" (`C-SP:421`). C-SP §7a adds "**Live: none.**" (`C-SP:321`) | any live observation of placement or retirement | RUNTIME |
| 5 | no live capture of completion | OPEN | "completion transition: still absent" (`C-GC:577`); "EXP-019 stopped before a kill" (`C-GC:590`); evidence row "LIVE (pre-kill only)" (`C-GC:706`) | a live capture across a kill | RUNTIME |
| 6 | `waitv` width selector | OPEN | "so that arm is recorded, not attributed." (`C-GC:321`) | which `waitv` widths the group-number import uses | DATA |
| 7 | EE-8 residue | OPEN | "bits **7, 11, 12, 20** reach no direct test at any of the 29 sites" (`GC:787`); "**Bit `0x2`** has no direct test on any enumerated route" (`GC:804`). Register `EE-8` **ANSWERED** — "two bits residual" (`OQ:2072`) | a reader for row-12 bits 7, 11, 12, 20 and `02089340` bit `0x2` | STATIC (`EE-8` ANSWERED with residue) |
| 8 | body release | OPEN | "**Not established:** which tracks carry these entries (a data census of the per-action tracks), and whether any other code sets bit 34" (`GC:637-638`); "Which presentation that handle names, and what the states mean, is not claimed." (`GC:647-648`) | the track census; an image-wide bit-34 writer census; the handle's class states | DATA + STATIC |
| 9 | the window's purpose and the clock | NARROWED | Clock: "`0032A135` `inc` in `0032A100`, which runs only when the timer value `003EBA90(0)` differs from the one kept at `022C317C`" (`C-GC:436-437`). The 64 `u16` entries: "two banks of 64 `u16` counters … incremented per fresh spawn of a row with that byte `+2`" (`UDEF:248-251`, before pass 1). `WHY:180-183` is unchanged | why the window exists (a policy reason; no port effect); WHY lacks pointers to C-GC §10a and UDEF | DOC |
| 10 | threading | OPEN | "**single-threaded use is assumed, not proven**" (`C-GC:328-329`) | whether ledger writers can run concurrently | STATIC |
| 11 | bits 45/49 and bulk zeroing | OPEN | "**Not closed for bulk zeroing** — 387 sixteen-byte zero stores at displacement 0 exist and cannot be attributed to a BattleUnit statically" (`HT:882`) | whether any bulk zero clears unit bits 45/49 | STATIC |
| 12 | unread accessors; unexplained keep bytes | NARROWED | Accessors closed: "`00236030` and `00236670` — … carry it in another register form, so the dead arm is in all nine *(corrected 2026-10-02, OPUS: `00236071` … `js`, and `002366A3` … `js`)*" (`GC:964-965`). Still: "What the untouched bytes and `+0x74` are for \| **not established**" (`FM:327`) | the purpose of keep `+0x42`–`+0x4F`, `+0x7D`–`+0x7F`, `+0x248`–`+0x24F`, `+0x74`. No port effect: FM states no reader at depth 6 (`FM:325`) | STATIC (low) |
| 13 | unaudited parts of HT | OPEN | "### What this pass did not attack" … "§2e's census … the largest remaining surface" (`HT:1032-1041`); §12's list "§2a, §2b, §2c, §2f, §3, §4, §5, and the `167 zone scripts` count in §1" (`HT:1130`). HT §2c's `esi` value was corrected 2026-10-02 (`HT:189`, `HT:213`), but no audit pass was added | an independent pass over HT §2a–§2f, §3–§5 | STATIC |
| 14 | guard and metadata side effects | NARROWED | The guard's two reset paths are now split: "the call at `00233C3F` and the tail at `00233C48` on the null path, so the reset runs twice there; `00233C59` is the tail for a non-null block whose stamp is not `0x05071901`" (`WHY:244`), and its body ends at `00233CE5` (`WHY:247`); C-GC's route table agrees (`C-GC:449-451`). Still: "**Which of the guard's callees run on every call, and which only on the null path, is not read here.**" (`WHY:224-225`); the metadata wrappers' "downstream effects are not established here" (`SPR:1608`) | which battery calls (`00327F80` … `00229ED0`, `WHY:245-247`) run on which path, stated as such; the wrappers' consumer effect (`SPR:1609-1612` points to the mode ladder) | STATIC |

### 2.2 Structural gaps G1–G16 (pass 1 §2.2)

| id | gap (pass 1) | verdict | evidence now | still missing | class |
|---|---|---|---|---|---|
| G1 | the clock's source and rate | NARROWED | "The counter `0208D45C` (BSS) has exactly **two writers** in the image: `0032A135` `inc` in `0032A100`, which runs only when the timer value `003EBA90(0)` differs from the one kept at `022C317C` … and `0032A160` `mov dword [0208D45C], 0`" (`C-GC:436-438`); the same condition was already at `TICK:213` before pass 1. The inline note "a field-frame counter, not 30 Hz" (`C-GC:403`) settles A9 | how often `003EBA90(0)` changes in real time, i.e. that the counter really advances `30 × [01DFE0B8]` per second, which every seconds conversion assumes (`WHY:62`) | STATIC |
| G2 | field-data record formats for placement and mode-2 retirement | NARROWED | Already on S16 before pass 1: the `FF12POS3` record, "`+0x00 u32 type 0, 1 or 2 only`", `+0x04`/`+0x08` extents, `+0x1C` heading, stride `0x30` (`S16:88-98`); "`FieldData_GetFormat0RecordVectorByIndex` (`00320940`, returns the record's `+0x10` / `+0x14` / `+0x18` floats), `003209C0` (the whole record, `−1` / `0`)" (`S16:317-318`); region sampling for types 1 and 2 (`S16:335-345`). Mode 2's anchor is that vector: "the anchor from `00320940(unit+0x51)`" (`C-SP:209`) | the containment formula of `FieldRegion_ContainsWorldPosition` `002374E0` (HT gives only "area-mode accept test; XZ only", `HT:445`, and an anchor, `HT:1182`); the folder links to S16 nowhere | STATIC (formula) + DOC (pointer) |
| G3 | where the candidate index comes from; which lane wins | OPEN | the selector is still "for each lane 1 .. laneCount-1 … for each candidate in the lane … `remember this lane and position`" (`SPR:294-309`). C-SP §7a adds only the gate's sites (`C-SP:244-246`) | `candId`'s derivation, the candidate count per lane, why lane 0 is skipped, and which qualifying lane is returned | STATIC |
| G4 | the unit-side retirement fields | CLOSED | "its anchor index `+0x51` (`0023518A`) and threshold `+0x4C` (`0023519C`)", mode byte `+0x50` (`C-SP:170-171`); "The mode, threshold and anchor are written by `00238FC0` (verb `0x3019` `btlAtelSetDeSpawnType`). It stores the mode always (`00238FE1`), but the threshold and anchor only for mode 2" (`C-SP:182-183`); "**The opt-in bit is the drive loop's.** The loop clears record `+0x0D` bit 6 at `0025E1AD` and sets it at `0025E217`" (`C-SP:176-178`) | — (SPR §4 still lacks the offsets: new gap N7) | — |
| G5 | two of the four selectors undescribed | OPEN | `002355A0` / `002354F0` are still "another `0x250`-stride keep-bank indexer" / "same" (`HT:473-474`); FM points away: "the four selectors — the placement page" (`FM:172`), which describes two. CONV maps the verb only: "`304B` `btlAtelDecideEntryGroupByPreviousMap` → `VM_Spawn_SelectPreviousMapEntry`" (`CONV:323`) | the logic, inputs and return of `Spawn_SelectPreviousMapEntry` `002354F0` and `Spawn_PrepareRandomCandidateForCurrentEntry` `002355A0` | STATIC |
| G6 | creating the actor for a chosen entry | NARROWED | Before pass 1: "`305C` **`btlAtelSetKeepWorkGroup`** → `VM_Spawn_BindEntryAndMarkCapTracked`" (`CONV:324`), whose body FM describes: "`00239840` … lane byte `+0x57`, `+0x16`, unit flag bit 21" (`FM:163`); "`3001` **`btlAtelSetUnit`** → `VM_Spawn_ApplySelectedUnit`" (`CONV:319`) | the native body of `VM_Spawn_ApplySelectedUnit` (`btlAtelSetUnit`); `setentrygroup`; `requestreentry` | STATIC |
| G7 | teardown | NARROWED | "`00300E40` has ten call sites. The retire's `002352B1` is the only one that passes 1; the other nine pass 0" and the keep clear `00237080` runs "only when that argument is 0 (`00300F5D`–`00300F68`)" (`C-SP:236-240`) | the rest of `BattleUnit_TeardownAndDespawn`: "what the teardown's callees (`00300FC0`, `003105D0`, `00319E30`, `0023A570`) write in the keep entry" is listed as not traced (`C-SP:325`) | STATIC |
| G8 | enmity decay | WRONG-IN-PASS-1 | ENM (before pass 1): "decay \| `BattleEnmity_UpdatePeriodicDecay` (`00321530`)" (`ENM:51`); "**E-1 — One vector, two roles: byte 0 of the table *is* the decay timer.** The decay reads `movzx ecx, byte ptr [rdi]` at `0032158F` with `rdi = BKEI + 0x19`" (`ENM:69-70`) | pointer only: SPR defers to 09 (`SPR:423`) without linking ENM | DOC |
| G9 | the spawn-history counters | WRONG-IN-PASS-1 | UDEF (before pass 1): "`0208D354` holds **two banks of 64 `u16` counters** … each counter starting at 1 per area visit and incremented per fresh spawn of a row with that byte `+2` … **the only readers are this installer and the rotation**" (`UDEF:248-253`); `FB-3` **ANSWERED** — "the `+0x12` copy is read once, by `BattleUnit_RefreshActorRuntimeFromDefinition`" (`OQ:2170`) | pointer only: WHY still says "a correspondence this page has not traced" (`WHY:77-78`) | DOC |
| G10 | the RNG's exact step | WRONG-IN-PASS-1 | RNG (before pass 1): "`a = g_uSharedGameplayLcgState * 0x41C64E6D + 0x3039;`" three times (`RNG:66-68`) | pointer only (C-SP and SPR give the multiplier, not the increment) | DOC |
| G11 | angle and heading helpers | WRONG-IN-PASS-1 | HEAD (before pass 1): "`00316DA0` (74 B) computes `wrap(x0 + x1)`: adds the angles and folds into [-pi, pi]" (`HEAD:1415-1417`); "`FUN_00265200` — **33 distinct callers** … For actor class 3 it returns **`+0xA8`**" (`HEAD:999-1002`) | pointer only (`C-SP:131`, `SPR:141`) | DOC |
| G12 | order within a frame and within area init | NARROWED | Frame order (before pass 1): "**So the ordering is: field frame (slot 0) → actor drive loop → per unit, the lifecycle frame.**" (`TICK:275`). Area init: the rotation "runs after the area's reset route `00239960` (`00234349`)" (`C-SP:163`) | inside `002342F0`, whether the ledger reset `00307090` runs before or after the rotation `00233780` (`GC:215` names the reset's caller, no site) | STATIC |
| G13 | group ids above the ledger | OPEN | ledger "entries exist for groups ~~1–5~~ 1–64" (`C-GC:74`); "The **group mask is a 32-bit set of spawn-group ids**, tested as `1 << (bSpawnGroupId & 31)`" (`SPR:452`); the new interior row for `00234990` tests "bit (byte `+0xE98` of the object, mod 32)" (`GC:1178`) | a bounds check for `+0xE98` values 65–255, and how 64 ledger groups coexist with a 32-bit group mask | STATIC |
| G14 | the ground probe's dataset | NARROWED | Before pass 1: "`00232490` (90 B) is the descriptor-post wrapper `0026E3C0`, `0032BCC0` and `0032CA70` call: it builds the descriptor `{0022F8B0, rcx, ...}` … runs `0022F830(&desc)`" and `0022F830`'s bit-walk (`SET:780-804`); HT's own answer box (`HT:723-730`) | `00231900`, `00231890`, `00230B60` bodies and the navigation cell dataset format | STATIC + DATA |
| G15 | timing of the deferred completion arm | OPEN | "`003250F0` runs whenever a track ends on a unit whose guard passes (`[rcx+0x0D]&1` clear, `[rcx+0x30]` non-null)" (`C-GC:675-676`) | when the death track ends; what happens to bit 47 and the ledger flag when the guard fails | STATIC + RUNTIME |
| G16 | the rest of the spawn verb surface | NARROWED | New: "`SpawnEntry_QueryRangeReentryPending` `00236670` has one caller, verb wrapper `0050FC90` (`btlAtelGetRespawnCause`)" (`C-SP:248-249`). Before pass 1: "`3015` **`btlAtelSetCallGroup`** → `VM_SpawnEntry_SetRangeRetireInhibitTag`" (`CONV:320`); `btlAtelSetUnitType` (`0x3005`, `00510340`) "through the table `{1, 5, 3, 4}` at `01E09EE8`" (`KIND:299-301`) | native effects of `btlAtelSetDefaultLogic` and `btlAtelSetDirection` (no page outside the folder names them); no page names `btlAtelGetDeadCountNow`'s handler (presumably `00235F50` → `0050F660`, `C-GC:47`); `btlAtelSetBelong` and `btlAtelSetHpLowLimit` have pages in 09 and 08 that the folder does not link | STATIC + DOC |

### 2.3 Fields written but left unexplained (pass 1 §2.2 table)

| id | field (pass 1) | verdict | evidence now | still missing | class |
|---|---|---|---|---|---|
| F1 | keep `+0x74` | WRONG-IN-PASS-1 | "**`+0x74` is written and never read.** A reconstruction may keep it for save-image fidelity" (`FM:246`); writer and source "`00234200` (`0023429E`)", from unit `+0x160` (`FM:103`) | nothing a port needs (purpose: item 12) | — |
| F2 | `0208935C` = 5.0 | WRONG-IN-PASS-1 | "written `5.0` by `BattleStorage_InitializeWorkArrays` and **never read anywhere in the binary** — a dead tunable" (`SPR:106-107`) | — | — |
| F3 | unit flag bit 40 | OPEN | BUFM's bit table: "40 \| `SpawnEntry_ConfigureFreshLifecycleFloatMode` `0023A200` (`0023A240`, float ≠ 0) \| `0023A200` (`0023A231`, float = 0) \| \|" — the "tested by" cell is empty (`BUFM:357`) | a reader of unit bit 40, or a stated "no reader" census | STATIC |
| F4 | unit lane byte `+0x57` | NARROWED | writer `00239840` (`FM:163`); before pass 1, BUFM: "`+0x40`, `+0x57` \| read (the spawn-keep key pair) \| `0023A772`, `0023A76E` \| count only" (`BUFM:713`) | what the `0023A76E` read does with it ("count only") | STATIC |
| F5 | unit `+0x58` and table `01E09EE8` | WRONG-IN-PASS-1 | KIND (before pass 1): `btlAtelSetUnitType` "(`0x3005`, `00510340` → `BattleUnit_SetRuntimeUnitCategoryMode`) sets through the table `{1, 5, 3, 4}` at `01E09EE8` for arguments 0–3" (`KIND:299-301`) | pointer only (`FM:167`) | DOC |
| F6 | `02089344` bit 0 | WRONG-IN-PASS-1 | BSB (before pass 1): bit 12 is set in the binder `00233C10` "when `02089344` bit 0 is …", and its clear branch `00233CA6` is the "restart flag `02089344` bit 0" path (`BSB:302`, `BSB:319`) | pointer only (`SPR:3567`) | DOC |
| F7 | state `+5B04` bit 1 | WRONG-IN-PASS-1 | BSB (before pass 1): "`+0x5B04` \| 4 \| **the mode flags** — bit 0 UI, bit 1 combat / audio" (`BSB:119`) | pointer only (`SPR:1606`) | DOC |
| F8 | height-mode values 1, 2, 5, 6, 12 | WRONG-IN-PASS-1 | only bit 3 is read (`HT:714-716`); the values are fully determined by the applier (`HT:210-213`, corrected 2026-10-02) | — | — |
| F9 | ledger `flags` bits 1–7 | WRONG-IN-PASS-1 | only bit 0 is touched in the image (`GC:231-248`); a port reserves them | — | — |

### 2.4 Contradictions (pass 1 §2.3)

Every CLOSED row below is closed by a **dated correction on the page** (2026-10-02, OPUS, unless noted). They remain page text,
not executable checks; pass 1's "needs local check" applies unchanged.

| id | contradiction (pass 1) | verdict | evidence now | still missing | class |
|---|---|---|---|---|---|
| A1 | dead-mask bit: 64-bit vs sign-extended 32-bit shift | CLOSED | GC's §5 pseudocode is annotated: "`# <- corrected 2026-10-02, OPUS - a sign-extended 32-bit shift, (int64)(int32)(1u << (lane & 31)); 00306F6F mov eax, 1 / 00306F74 shl eax, cl / 00306F76 cdqe`" (`GC:392`) | — | — |
| A2 | field-table element `u16` or `i16` | CLOSED | "~~the element is **signed**~~ the element is a plain 16-bit word, read unsigned by the getter `00264D20` (`00264D3D` `movzx`) and signed by this consumer *(corrected 2026-10-02, OPUS: signedness is per reader …)*" (`C-GC:88`); GC agrees: "stores `value` as a ~~`u16`~~ 16-bit word" (`GC:468`) | — (the remaining "`u16`" wording at `GC:676`, `GC:691`, `C-GC:211`, `C-GC:293`, `C-GC:542` describes the store and is consistent) | — |
| A3 | continuous-entry match predicate | CLOSED | "~~`… && !(history[j].flags & 5) && …`~~ `history[j].flags & 2 && (history[j].flags & 5) && history[j].b_17 == live.b_17` *(corrected 2026-10-02, OPUS …)*" (`FM:203`) | — | — |
| A4 | who clears keep bits 0, 2, 7 | CLOSED | bit 0 and bit 2 rows add "`00236860` (`002368AA`) and `00237080` (`00237085`), unconditionally" and note `0023A2E0`'s mask "runs only on fresh entries" (`FM:115`, `FM:117`); bit 7: "~~nothing found does~~ `00236860` … and `00237080` … do, and `0023A2E0` (`0023A34E`) on fresh entries" (`FM:122`) | — | — |
| A5 | keep offsets in SPR §4 vs FM | CLOSED | SPR §4 diagram annotated "`+0x14` is bStealAvailabilityFlags … the field map is the authority" (`SPR:533`); §8f: "~~The per-entry field offsets in §4 stand;~~ The per-entry field offsets in §4 do not all stand" (`SPR:1110`) | — | — |
| A6 | what `0208E6A0` is | CLOSED | "~~`0208E6A0` the bank flag~~ *(corrected 2026-10-02, OPUS: `0208E6A0` is the battle-unit slot count, 32 …)*" (`FM:158`) | — | — |
| A7 | slot flag: fifth or sixth argument of `00234DA0` | CLOSED | "Its ~~sixth argument~~ fifth argument (`00234AF0`'s sixth) decides eligibility *(corrected 2026-10-02, OPUS: `00234DC3` `mov r12d, dword ptr [rsp + 0xb0]` is the first stack argument …)*" (`C-SP:503`) | — | — |
| A8 | mode-2 threshold: keep `+0x04` or unit `+0x4C` | CLOSED | FM: "*(no GFZ name)* - not the placement page's mode-2 threshold, which is the battle unit's `+0x4C` *(corrected 2026-10-02, OPUS: `0023519C` … with `rsi` = `0031B760()`, the battle unit …)*" (`FM:86`); C-SP §7a: "threshold `+0x4C` (`0023519C`)" (`C-SP:171`) | — | — |
| A9 | rate of `0208D45C`: frame counter or 30 Hz | CLOSED | "`# <- corrected 2026-10-02, OPUS - a field-frame counter, not 30 Hz; 0032A100 increments it once per 00234590 frame (0032A135), and the divisor below is 30 x [01DFE0B8] = 30 or 60`" (`C-GC:403`) | the real-time rate is G1; the "once per frame" wording is new gap N1 | — |
| A10 | does the return window survive save/load | CLOSED | "~~The return window therefore survives a save/load in both directions.~~ The field-id pair survives a save/load; the transition stamp `02089374` and the window setting `0208936C` do not" (`SPR:925`); C-SP: "**The window and the stamp are in no save.**" (`C-SP:199-200`) | — | — |
| A11 | does native code compare cooldown and elapsed | CLOSED | C-GC diagram: "`# <- corrected 2026-10-02, OPUS - not the only readers; Spawn_SelectAndPrepareAutomaticEntry reads +0x08/+0x0A/+0x0C/+0x10 directly`" (`C-GC:249`); box: "**the scripts compare with `>` and the selector natively with `>=`**" (`C-GC:390-393`); GC: "~~the only consumer~~ the script consumer compares" (`GC:738`) | — | — |
| A12 | does a mode-≠1 group post its completion | CLOSED | GC box struck: "*(corrected 2026-10-02, OPUS: arm B posts - `002EA4C5` registers the guard `002E70A0` in slot 0xC … and `003251A4` calls `00307110`, which clears bit 47 … and sets the ledger flag …)*" (`GC:509`); C-GC §7 annotated "it has one" (`C-GC:264`); GC EE-12 tail struck (`GC:835`) | — | — |
| A13 | accessor failure sentinel | CLOSED | "**Every ~~accessor~~ respawn-reader failure is `-1`** *(corrected 2026-10-02, OPUS: in the wider family `SpawnEntry_GetScriptSelection` `00236140` returns `-2` …)*" (`C-GC:333`) | — | — |
| A14 | how many ledger entries | CLOSED | "entries exist for groups ~~1–5~~ 1–64 (the authored corpus uses 1–5) *(corrected 2026-10-02, OPUS: the reset `00307090` walks `02EC13D0` to `02EC19D0` …)*" (`C-GC:74`) | — | — |
| A15 | `00235AF0`: copy on match or on difference | CLOSED | "`002EF4A0` ~~copies the matched row~~ copies the `0x6000`-byte block when any of the four compared values differs *(corrected 2026-10-02, OPUS …)*" (`SPR:3681-3682`); agrees with `SPR:3350` | — | — |
| A16 | the guard `00233C10` around `00237DF0` | CLOSED | WHY corrected to SPR's reading: "the call at `00233C3F` and the tail at `00233C48` on the null path, so the reset runs twice there; `00233C59` is the tail for a non-null block whose stamp is not `0x05071901`" (`WHY:244`); C-GC §10a's route table agrees (`C-GC:449-451`) | — (WHY's §-level summary still disagrees: new gap N2) | — |
| A17 | engine call site for handler id `0xC` | NARROWED | corrected in two places: "`call rax` on `[02CA4470]` (id 0xC) at ~~`0041DC84`/`0041DD03`/`0041CEC6`~~ `0041DC9E`/`0041DD1D`/`0041CEE3` *(corrected 2026-10-02, OPUS: the struck addresses are the `mov rax, [slot]` loads …)*" (`C-GC:368`; also `GC:834`) | the struck loads are still given as the `call rax` sites, unstruck, at `C-GC:350` ("`call rax` at `0041DC84`/`0041DD03`/`0041CEC6`"), `C-GC:671` (with `00417CC6` for id 6, corrected to `00417CDF` at `C-GC:368`) and the evidence row `C-GC:700` | DOC |
| A18 | height mode for a non-spawn-backed unit | CLOSED | "`# <- corrected 2026-10-02, OPUS - esi is 1 here (00239E33 mov esi, 1, not rewritten before 00239FA7)`" (`HT:189`); "whose ~~values are 1, 2 and 3~~ value is 1" (`HT:213`); the §4 pseudocode is annotated too (`HT:563`) | — | — |
| B1 | `0x250`-stride census, 50 vs 27 sites | CLOSED | "`# <- corrected 2026-10-02, OPUS - 27 sites in 18 functions … 10 in 0043F450`" (`HT:971`); "~~18 of its 50 sites~~ 10 of its 27 sites inside one function" (`HT:1007`) | — | — |
| B2 | function sizes `00307140`, `00312EE0` | CLOSED | "`00307140` ~~(~97 B)~~ (183 B *(corrected 2026-10-02, OPUS …)*)" (`C-GC:832`); "`00312EE0` ~~(~208 B)~~ (187 B *(corrected 2026-10-02, OPUS: `ret` at `00312F9A` …)*)" (`FM:512`) | — | — |
| B3 | the ledger TSV vs the six-function census | OPEN | `spawn-group-ledger-accesses.tsv` is unchanged since pass 1 (19 rows, three functions); GC still says "addressed by exactly six functions" (`GC:686`) | a TSV row set for `00307030`, `003070E0`, `00307110` and the flag set at `00306FE0`, or a note that the TSV is register-route only | DOC |
| B4 | 828-file counts beside the 1,114-file recount | OPEN | unchanged: "**167 zone scripts use it.**" (`HT:66`), `HT:79`, `HT:434`, `HT:675`, `HT:700`, `SPR:835` | the whole-corpus figures in place, or each line scoped to the 828-file subset | DOC |
| B5 | how many accessors carry the `js` arm | CLOSED | "carry it in another register form, so the dead arm is in all nine" (`GC:964-965`) | — | — |
| C1 | README: SPR PARTIAL | CLOSED | "~~**PARTIAL.**~~ **DOCUMENTED.**" (`README:13`) | — | — |
| C2 | README: FM DOCUMENTED | CLOSED | "~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1.**" (`README:21`) | — | — |
| C3 | README lists 2 of 7 pages | CLOSED | five pages added with their own front-matter status (`README:25-30`) | — | — |
| C4 | SPR body "raised to DOCUMENTED on 2026-09-02" | WRONG-IN-PASS-1 | already reconciled on the page at pass 1: "that raise is history … the current status is the front-matter line" (`SPR:36-37`); pass 1 said so itself | — | — |
| C5 | SPR §11 "`crossref_clean` is now false" | CLOSED | struck, "*(answered: see the front matter, `crossref_clean` true …)*" (`SPR:1556-1557`) | — | — |
| C6 | SPR `last_pass_state` "remaining caller questions open" | CLOSED | "`# <- corrected 2026-10-02, OPUS - superseded by the status line (2026-10-01); L-12 and L-13 are SUPERSEDED, section 7`" (`SPR:22`) | — | — |
| C7 | HT §10 "`status` is `DOCUMENTED`, `audit.passes` is `0`" | CLOSED | struck, "*(answered: see §11 and §12 … `status` AUDITED, `audit.passes` 1, `crossref_clean` true …)*" (`HT:872-873`) | — | — |
| C8 | SPR §2 "recorded as **L-7**" | CLOSED | "~~is recorded as **L-7**~~ is nothing at generation; a terrain probe supplies it at activation" (`SPR:176`) | — | — |
| C9 | WHY: L-13 open | CLOSED | "~~is the open question `L-13` …~~ is nothing: bank 1 is never read back and the stamp is not restored *(answered …)*" (`WHY:146`); "~~`L-13` keeps bank 1 and the timer.~~" (`WHY:176`) | — | — |
| C10 | SPR §§11–29 closing lines "remains open" | WRONG-IN-PASS-1 | each line already carried "*Reconciled 2026-09-30 (FABLE): L-12 and L-13 are SUPERSEDED since; §7*" at pass 1 (pass 1 said so); 11 such annotations stand | — | — |
| C11 | C-GC §8 "no decompiled script has confirmed it (`EE-11`)" | CLOSED | "~~no decompiled script has confirmed it~~ *(answered: see §4a and §14 item 8 - observed in 6,746 shipped calls …)*" (`C-GC:290`) | — | — |
| C12 | evidence rows "PROBABLE" for the argument order | CLOSED | C-GC row now "~~PROBABLE~~ OBSERVED" (`C-GC:703`); GC row likewise (`GC:899`) | — | — |
| C13 | GC box "No shipped script has been decompiled" | CLOSED | struck, "*(answered: see the next paragraph - `EE-11` observed in the shipped scripts 2026-09-13 …)*" (`GC:349-351`) | — | — |
| C14 | GC "whether `+0x10` is seconds \| not established" | CLOSED | the §9 row: "~~**not established**~~ yes, whole seconds - `EE-1` 2026-09-13 … ~~UNKNOWN~~ PROVEN" (`GC:885`); the §3 sentence was already annotated at pass 1 (`GC:126-127`) | — | — |
| C15 | GC §9 "no static route … PROVEN" | CLOSED | "~~… have no static route~~ *(corrected 2026-10-02, OPUS: refuted …)* … ~~PROVEN (as a negative over the listed routes)~~ REFUTED" (`GC:895`) | — | — |
| C16 | GC "row-12 bits and slot 3's reader not established"; "slot 3 is `EE-9`" | CLOSED | `GC:901` (EE-8 / EE-9 answered, "PROVEN, with the EE-8 residue"); `GC:523` "the zone script reads slot 3, by `waitv` on `scratch1`" | — | — |
| C17 | GC §5b "verified live" | CLOSED | "verified ~~live~~ statically, by the slot registration and the engine's `call rax` sites; no live verification is recorded" (`GC:614`) | — | — |
| C18 | GC heading "The reset zeroes all three fields" | CLOSED | "### The reset zeroes ~~all three fields~~ both masks and flag bit 0 only" (`GC:198`) | — | — |
| C19 | C-GC interface table split by §4a | CLOSED | "*(table header restored 2026-10-02, OPUS …)*" and a new header row (`C-GC:78-81`) | — | — |
| C20 | names saying "ticks" for seconds | OPEN | unchanged, kept knowingly: "`wRespawnCooldownTicks` ✓" (`FM:90`), and the accessor names | renaming, or a one-line "unit: seconds" beside each name on FM | DOC (low) |
| C21 | `…LethalState` vs `…LethalTransition` | OPEN | `…ProcessLethalState` at `GC:131`, `GC:428`, `GC:678`, `SPR:457`, `SPR:888`; `…ProcessLethalTransition` at `FM:87`, `FM:223` | one name | DOC |
| C22 | HT: `0043F210` "is a spawn-placement body" | CLOSED | "~~is a spawn-placement body~~ is not a spawn-placement body: its only caller is the Presentation function `0043F450`" (`HT:1186`) | — | — |
| C23 | GC: `003E6770` / `003C9250` "group-respawn body" | CLOSED | "`003C9250` (280 B) ~~is a group-respawn body~~ is not shown to be a group-respawn body" (`GC:1130`); "`003E6770` (276 B) ~~is a group-respawn body~~ is not a group-respawn body" (`GC:1139`) | — | — |
| C24 | `last_reviewed` older than the page's dated content | OPEN | unchanged stamps: GC `2026-09-12` (`GC:18`), FM `2026-09-10` (`FM:18`), C-GC `2026-09-11` (`C-GC:16`); now also C-SP `2026-09-29` (`C-SP:15`) beside its 2026-10-03 §7a, and C-GC beside its 2026-10-03 §10a | the stamps, or HT's explanation (`HT:1097-1106`) on each page | DOC (low) |
| C25 | HT §7 UQ-100 "closed — WITHDRAWN" vs "stays open" | OPEN | still "*(closed — the register row is WITHDRAWN.)*" (`HT:717`), while the register says `UQ-100` **SUPERSEDED** 2026-09-26 (`OQ:2814`) and the box body keeps the runtime half open (`HT:722`) | the box's state word made to match the register (SUPERSEDED, runtime half open) | DOC |
