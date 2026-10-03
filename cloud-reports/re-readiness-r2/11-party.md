# Reconstruction readiness, pass 2: `FFXII TZA/11-Party/`

| | |
|---|---|
| Stream | R2 (reconstruction readiness, pass 2), per [`docs/cloud-briefs/re-readiness-r2.md`](../../docs/cloud-briefs/re-readiness-r2.md), part A |
| Session | FABLE r2-12 |
| Date | 2026-10-03 |
| Snapshot | this repo at `b23bdddd` (synced from XIIOnline `f9d9053b9`); pass 1 read `df2c9f47` |
| Pass 1 | [`cloud-reports/re-readiness/11-party.md`](../re-readiness/11-party.md) (2026-10-02) |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every verdict quotes a page with its `page:line` in this snapshot. No executable, Ghidra or live game was used. |

Citation form: `page:line`. A bare file name is a page in `FFXII TZA/11-Party/`; `BSB/` stands for
`FFXII TZA/11-Party/Battle-State-Block/`. Any other page is given as a path from `FFXII TZA/`. The register is
`_index/OPEN-QUESTIONS.md` (`OQ:line`).

**How the verdicts were reached.** I diffed every 11-Party page and the register between `df2c9f47` and `b23bdddd`
(253 lines added, 169 removed). I re-read each passage that a pass-1 item cites, and searched the whole snapshot for
each address a gap names. Where the answer is on a page outside 11-Party, I checked whether that text was already in
`df2c9f47` (`git show df2c9f47:<page> | grep`). If it was, the verdict is **WRONG-IN-PASS-1**: pass 1 scoped itself to
11-Party pages and missed it. If it was added since, the verdict is **CLOSED** or **NARROWED**.

## 1. Summary

**Pass-1 gaps (41: G-1 to G-22 and S-1 to S-19)**

| verdict | count | items |
|---|---:|---|
| CLOSED | 4 | G-2, S-3, S-12, S-13 |
| NARROWED | 8 | G-4, G-6, G-10, G-11, G-14, G-22, S-5, S-10 |
| OPEN | 21 | G-1, G-3, G-5, G-7, G-8, G-9, G-12, G-15, G-16, G-17, G-18, G-19, G-20, G-21, S-6, S-7, S-8, S-9, S-14, S-15, S-16 |
| WRONG-IN-PASS-1 | 8 | G-13, S-1, S-2, S-4, S-11, S-17, S-18, S-19 |

Classes of the 29 OPEN or NARROWED items: **STATIC 22**, **RUNTIME 5** (G-4, G-8, G-15, G-20, G-22),
**DATA 2** (G-11, G-21). Of the eight WRONG-IN-PASS-1 items, six leave a **DOC** residue (G-13, S-4, S-11, S-17,
S-18, S-19): the answer is on another page, and the 11-Party page has no pointer to it or still says the opposite.

**Pass-1 contradictions (54: C-V1 to C-V27 and C-B1 to C-B27).** These are not gaps in pass 1's numbering, but each
one is a choice a re-implementer would have had to make, so each gets a verdict too (§2.3, §2.4).

| | CLOSED | NARROWED | OPEN |
|---|---:|---:|---:|
| value-changing (C-V) | 25 | 2 (C-V5, C-V21) | 0 |
| stale / banner (C-B) | 23 | 2 (C-B19, C-B27) | 2 (C-B15, C-B24) |

Almost all were closed by OPUS's dated 2026-10-02 corrections, which struck or annotated the losing side in place.
**C-V19 was settled the other way from pass 1's reading:** the licence board is granted when the preset's LP word is
**not** `0xFFFF` (`the-setsavedata-presets-test-battle-scenarios.md:49`, `:122`).

**New gaps (8):** STATIC 4 (N-1, N-2, N-3, N-8), DOC 4 (N-4, N-5, N-6, N-7). None is RUNTIME or DATA. No register
row tracks any of them.

**Rating: NOT YET (unchanged), but now for one reason instead of two.** Pass 1 had two subsystems at NOT YET.
Control suppression moves to **MOSTLY**: the mask formula, the mode-1 replacement, the publication and the frame
position are all stated, on the capability-policy and world-tick pages that 11-Party points to or should point to.
The **follow formation stays NOT YET**: no page states where a follower is placed. The other five subsystems stay
MOSTLY, with fewer open items than in pass 1 (§4).

---

## 2. Pass-1 gaps

### 2.1 The gaps the pages state themselves (pass 1 §2.1, G-1 to G-22)

| # | short name | verdict | evidence (quote + `page:line`) | still missing / class |
|---|---|---|---|---|
| G-1 | what `+0x0F` selects | **OPEN** | "What `+0x0F`'s two values select. Two writers, no reader observed." (`CONTRACT-party-slot-assignment.md:352`); "Whether `+0x0F = 2 / 3` is the "in party / not" kind the page's suppression gate reads is not established here." (`party-roster-and-control-suppression.md:152`–`:153`). The actor-storage field map lists `+0x0F`'s writers (`04-Actor-Entity/Actor-Storage-Record/the-actor-storage-record-field-map.md:285`) but its table has no `+0x00F` row: it goes from `+0x00E` (`:105`) to `+0x010` (`:106`). | Any reader of record `+0x0F`, and what `2` / `3` select. **STATIC** |
| G-2 | `002681C0` not read | **CLOSED** (elsewhere; DOC residue) | "`002681C0` \| 9 B \| tail-jumps `00269C70(rcx, sign-extended byte +0x12 of rcx)`" (`00-Engine-Core-Runtime/ABI-Recovery/derived-call-signatures.md:359`; not in `df2c9f47`) | The 11-Party row still reads "`PartyRoster_ReapplyActorStoredSlot` \| not read" (`party-roster-and-control-suppression.md:217`). It needs the pointer. |
| G-3 | names of the two role-notice predicates | **OPEN** | "their names are the residue" (`party-roster-and-control-suppression.md:125`–`:126`). Elsewhere `00265680` appears only as a gate; for example `00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md:931` corrects its polarity at one call site. | What `00265680` and `002672B0` test, by name. **STATIC** |
| G-4 | null leader `+0x698` | **NARROWED** | Static side closed on the policy page: "Under the typed BattleUnit access census, the leader `0023B040` reads can never have a null `+0x698`." (`15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md:930`); the pass of 2026-10-01: "inside the window the re-applied unit is never the leader" (`:1043`–`:1049`). UQ-147 is **SUPERSEDED** under the runtime rule (`capability-inhibition-policy.md:784`). | The live check `FABLE-REQ-ASTRA-LEADER-STATS-NULL` (`capability-inhibition-policy.md:790`–`:791`). 11-Party still reads "Whether initialized gameplay can reach that state is not established" (`party-roster-and-control-suppression.md:183`; `CONTRACT-party-focus-and-control-suppression.md:211`–`:212`), with no pointer to the census. **RUNTIME** (+ DOC pointer) |
| G-5 | which manager slot 3 is | **OPEN** | "*Which of the five managers slot 3 is was not established here*" (`party-roster-and-control-suppression.md:651`). The mode ladder uses "manager slot 3's `+0x10` bit 0" without naming the manager (`00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md:405`). | The identity of actor-manager slot 3. **STATIC** |
| G-6 | `002695A0`; `0025BFB0`'s request bits; `0026CE60` / `002628B0` | **NARROWED** | The request bits are per-manager requests. EX-9: "the one producer `0026A5F0`, which ORs `1 << m`" (`OQ:2122`, status ANSWERED). `002695A0` was re-read: "after the two stores `002695AF`/`002695B7` it only calls and fills the 16-qword array at `0209A210`" (`CONTRACT-party-slot-assignment.md:156`). | §14 still lists "The identity of `002695A0`" as open (`CONTRACT-party-slot-assignment.md:354`). What the array `0209A210` is (N-1). What `0026CE60` and `002628B0` do natively, beyond the windows read. **STATIC** |
| G-7 | does `00263770`'s callee write the roster | **OPEN** | "The taint does not follow the address into a callee. `PartyRoster_GetActorBySlotOrCurrentFocus` (`00263770`) passes the roster to a call, and what that callee does with it is not covered here." (`CONTRACT-party-slot-assignment.md:389`–`:391`) | **STATIC** |
| G-8 | §4 staleness across a transition; slot above 3 | **OPEN** | "**§4's staleness.** After a field transition, read the four pointers …" and "Nothing static shows a caller that passes a slot above 3, so whether that path is ever taken is unknown." (`CONTRACT-party-slot-assignment.md:336`–`:338`, `:345`–`:346`) | **RUNTIME** |
| G-9 | what `003D9B80` means for a summon | **OPEN** | "What `003D9B80` resetting `record + 0x10` means for a summon, beyond the fields it writes." (`CONTRACT-party-focus-and-control-suppression.md:239`). The fields are listed on another page, and were already there at pass 1: "`003D9B80` (182 B) is the large reset the manager-map callers run: `0032B790(rcx+0x2B0)` clears the sub-record, …" (`04-Actor-Entity/Actor-Manager-Record/the-actor-manager-record-field-map.md:948`–`:953`). | What the reset means for the outgoing summon leader. The contract has no pointer to the manager-record page. **STATIC** |
| G-10 | what the five map classes mean | **NARROWED** | The heading now reads "four named, one unreached" (`active-party-reserve-and-the-moment-the-leader-changes.md:92`). The census is now "**32 sites, 31 of them passing a constant** … only `0030A804` passes a computed class" (`:97`). The `0050FD1A` family was corrected: "`0050FD15 mov edx, 3` and its siblings pass class 3" (`CONTRACT-the-five-parallel-slot-maps.md:251`). RC-18 (ANSWERED 2026-09-30): "map 1 is the engine's own follower source" (`OQ:3531`). | Class 4: "What the class byte *is* semantically … stays open" (`CONTRACT-the-five-parallel-slot-maps.md:251`–`:252`); its only site is computed at `0030A804`. **STATIC** |
| G-11 | what `01EED260` holds; `00316DF0` / `00323540` | **NARROWED** | Its role is stated: "the nine entries of the authored table at `01EED260`" (`CONTRACT-the-five-parallel-slot-maps.md:90`–`:91`), with the per-entry fill rule (`:92`–`:96`). | The nine byte values are not given; the slot-maps page still asks "what `01EED260` holds" (`the-five-parallel-slot-maps.md:200`). **DATA**. The two functions are S-9. |
| G-12 | the selector's upper byte | **OPEN** | "the upper byte of each of the nine entries is, so far, never read" (`the-five-parallel-slot-maps.md:265`–`:266`). | Whether any reader or writer gives the high byte meaning. **STATIC** |
| G-13 | `BattleUnit +0x698`: forty-record array or spawn record | **WRONG-IN-PASS-1** (DOC residue) | Resolved 2026-09-10, before pass 1: "**the unit's stats record — kind 0: the BattleSystemState element; kind 1: its SpawnKeep entry `+0x80`**" (`04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md:172`); AL-1 cites `OPUS-CONTRA-BU698` (`OQ:791`). | 11-Party still reads "**Recorded as a contradiction (`OPUS-CONTRA-BU698`), not resolved**" (`the-five-parallel-slot-maps.md:282`–`:283`). |
| G-14 | `+0x5AD0`, sixteen bytes, two known bits | **NARROWED** | The flag word's row: "bit 1 = a sequence is active …, bit 0 cleared by `00313840` with bit 1 *(corrected 2026-10-02, OPUS: …)*" (`BSB/the-battle-state-block-field-map.md:109`). The other twelve bytes have their own rows: `+0x5AD4` mode, `+0x5AD5` actor, `+0x5AD8` / `+0x5ADC` timers (`:110`–`:113`). | What bit 0 of `+0x5AD0` means (only its clear is stated), and bits 2–15. The slot-maps page still reads "Only two bits of its first word have known consumers" (`the-five-parallel-slot-maps.md:290`–`:291`). **STATIC** |
| G-15 | pooled-task-full path of a removal | **OPEN** | "*Read here and not executed: when all 32 pool slots are taken, the helper returns without the tail-jump. Map 0 is then rewritten and maps 1–4 are not …*" (`CONTRACT-the-five-parallel-slot-maps.md:157`–`:159`) | Whether play fills the pool. **RUNTIME** |
| G-16 | the scenario arm's maps 1–4 | **OPEN** | "That arm writes map 0 through `00329080` and reaches neither `00329CC0` nor the refresher `003266C0` through direct calls to depth 8. Indirect calls were not followed." (`BSB/CONTRACT-battle-state-block.md:115`–`:117`) | **STATIC** |
| G-17 | why the binder resets twice | **OPEN** | "nothing read here says why … Any difference lies in state outside the block." (`BSB/CONTRACT-battle-state-block.md:186`–`:189`) | **STATIC** |
| G-18 | the block's writer side | **OPEN** | "**writes are under-covered wherever a constructor or an index-derived writer sits outside the seeds**" (`BSB/CONTRACT-battle-state-block.md:190`–`:193`); the field map repeats the limit (`BSB/the-battle-state-block-field-map.md:58`–`:60`). | **STATIC** |
| G-19 | block `+4` bit 6 before any load | **OPEN** | "**Which writer sets it before any load is not read.**" (`BSB/the-battle-state-block-field-map.md:313`) | **STATIC** |
| G-20 | when the compatibility import fires; null `02EBF130` | **OPEN** | "It does not show when the importer's four-field test differs in real play, whether an ordinary current-format load ever reaches it with differing fields, or what the player sees" (`BSB/the-battle-state-block-field-map.md:280`–`:282`) | **RUNTIME** |
| G-21 | `+0x7A` in `00317400` | **OPEN** | "what `+0x7A` is authored as is the residue." (`BSB/the-battle-state-block-field-map.md:431`–`:432`) | The authored meaning of definition word `+0x7A`. **DATA** |
| G-22 | nothing executed | **NARROWED** (in part WRONG-IN-PASS-1) | The slot-maps banner was corrected: "the resolver is not executed, but the initialiser and both removers were — OPUS blocks 338 and 340" (`CONTRACT-the-five-parallel-slot-maps.md:222`). The suppression recompute **was** executed in isolation before pass 1: "Method B entered shipping `0023B040` at its first instruction …" (`15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md:688`–`:694`, ASTRA 2026-09-12). | Still unexecuted: the resolver `0031B9F0`, and the block's bind / reset ("**None.** No experiment executes these bodies.", `BSB/CONTRACT-battle-state-block.md:181`). The focus contract still says "Nothing executes the suppression recompute" (`CONTRACT-party-focus-and-control-suppression.md:233`), against the policy page. **RUNTIME** (+ DOC) |

### 2.2 The structural gaps pass 1 found (pass 1 §2.2, S-1 to S-19)

| # | short name | verdict | evidence (quote + `page:line`) | still missing / class |
|---|---|---|---|---|
| S-1 | the suppression mask as a formula | **WRONG-IN-PASS-1** | All of it is on the capability-policy page, which the 11-Party correction block points to ("see the policy page §10", `party-roster-and-control-suppression.md:187`). It was there at pass 1. Seed: "it is the initial value of the whole mask" (`15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md:569`–`:571`). Bits 9 and 10 of `02089340`: "Either one replaces the whole mask with all-suppressed" (`:626`–`:630`). Events: `00322600` hits make the mask all-suppressed, and any id but `0x2001` / `0x2009` / `0x2031` sets bit 1 through `00322920` (`:631`–`:644`). Statuses: "any of them **except Immobilize** also sets bit 1" (`:645`–`:651`). Combo and action: "`+0x6B7` is **combo progress** — any non-zero value makes the mask all-suppressed … bit 1 is set when the id is an action-definition id (`≤ 0x21E`) in phase 9 or later, or whenever unit flag bit 24 is set" (`:652`–`:657`). Flag 46: "unit flag **bit 46** forces all-suppressed when reached" (`:661`); this is pass 1's `0x400000000000`. | Unit flag bit 24 has no name ("registered as **SD-4**", `capability-inhibition-policy.md:665`–`:666`). |
| S-2 | the mode-1 second gate | **WRONG-IN-PASS-1** | "`003135C0` tests mode 1; `003137F0` reads the battle-state block's `+5AD5` byte, and `0031B770` finds a unit whose `+698` is the corresponding combatant record. When found, a null record or `0x80000003` status match with the field override clear replaces the mask at `0023B1B8`." (`capability-inhibition-policy.md:727`–`:731`); table row "Mode 1, selected counterpart healthy / KO \| 0 / 7" (`:725`). The counterpart is the summon's acting member (`:787`–`:789`). | Whether a healthy counterpart clears contributions the leader already set: the table shows only the default-state case. §12's "`0023B1B8 mov ebx, r14d` restores the all-ones seed on every early exit from the mode-1 block" (`:898`) is hard to reconcile with "Skipping recompute retains the seed" (`:721`). **STATIC** (a residue, not counted as OPEN) |
| S-3 | `[0208E6B8]` store; `0209A2C5`'s consumer | **CLOSED** | The store is not this function's: "the `0036FFE0` pair and the `[0208E6B8]` store at `0023B22F`–`0023B238` belong to the next function, `0023B200`, past this one's last instruction at `0023B1FA`" (`party-roster-and-control-suppression.md:484`, 2026-10-02). The consumer was already stated before pass 1: "Readers: the getter `00265460` (← `InputGameplay_ArbitrateDigitalInputAndModalState` `00254145`, the force-fight family …) and `0026DFB0` (← field entry `00268D10`)" (`15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md:622`–`:625`). | — |
| S-4 | when the recompute runs | **WRONG-IN-PASS-1** (DOC residue) | Field-frame step 8: "`002346E5` \| `PartyControl_RecomputeSuppressionFromLeaderBattleState`" (`00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md:219`). It is also the first call of the slot-0 post-step `00234520` (`:255`–`:256`). Both are mode 0 only, once per tick (`:98`–`:106`, `:207`–`:208`). Added since: the defeat cleanup calls it in the same call as `003138D0` (`15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md:798`–`:801`). | No 11-Party page cites the world-tick steps. |
| S-5 | the follow formation | **NARROWED** | Who calls the solver, and when: field-frame step 21 "`PartyFollow_SolveFormationWrapper`" and step 22 "`PartyFollow_ApplyGoal` \| only if `Navigation_HasDataset()`" (`00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md:232`–`:233`); the wrapper "calls `00338490`, then clears bit 0 of dword `022C7D04` and byte `022C7CE9`" (`:1155`). Which members: "`PartyFollow_SolveFormation` `00338490` and `PartyFollow_ApplyGoal` `003246C0` walk map-1 slots 0 to 3 through `0031B810`" (RC-18, ANSWERED 2026-09-30, `OQ:3531`). | The geometry is still unstated: spacing, ordering, and the target position each follower gets. So are slot `+0x24` and the three `movaps` vectors at `+0x30` / `+0x40` / `+0x50` ("**NOT CLAIMED**", `party-roster-and-control-suppression.md:625`–`:626`). 11-Party cites neither the world-tick steps nor RC-18. **STATIC** |
| S-6 | the refresher's per-mode values | **OPEN** | SM-5 still says only "rewrites entries of maps 1, 2 and 4 among `[0..3]`" (mode 1), "rewrites `[0..3]` of maps 1, 2 and 4" (mode 4), etc., with a value only for mode 2: "map 1 and map 4 entry 3 become `0x1A`" (`CONTRACT-the-five-parallel-slot-maps.md:117`–`:123`) | Which selector goes to which entry in modes 1, 3, 4 and 5. **STATIC** |
| S-7 | `00329080`'s body and third argument | **OPEN** | Still only a write site and a crossing name: `PartyConfiguration_SetDefinitionSelectorForIndex` (`00329080`) (`08-Combat-Formula/CONTRACT-stat-derivation.md:300`). The scenario arm passes `3` (`the-setsavedata-presets-test-battle-scenarios.md:104`–`:105`). | The body, and what argument 3 selects. **STATIC** |
| S-8 | the reconcile's compaction rule | **OPEN** | One example still: "Removing member 2 from `0..6` gives `0, 1, 3, FFFF, 4, 5, 6`, so the active part closes up." (`CONTRACT-the-five-parallel-slot-maps.md:150`–`:151`) | The general rule, and `00326110`'s full body. **STATIC** |
| S-9 | what definition activation and release do | **OPEN** | Fragments only: "`00316DF0` and `00323540` call `Inventory_GrantEncodedLootItem` `00300B80`" (`13-Rewards-Progression-Economy/CONTRACT-gil-storage-and-movement.md:278`); `00316DF0` is a caller of the level grower `0030C470` (`04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md:174`–`:177`); "grants items and increments equipment counts" (`the-five-parallel-slot-maps.md:304`). | A description of either body. **STATIC** |
| S-10 | the SetSaveData tail | **NARROWED** | `0016D6A0` is now stated: "an LP of `0xFFFF` takes `0016D6A0`, a bare `ret 0`" (`the-setsavedata-presets-test-battle-scenarios.md:49`, 2026-10-02). `002CFD10` "calls `002527B0(6, 4, 0)` then tail-jumps `0028E880`" (`:346`). | `00327870`'s body: the page gives only "`00327870(R.u8[+0xA])` selects through the state block's `+0x5A48` selectors" (`:106`) and "the formation selector step" (`:149`). `002527B0` and `0028E880` are not described. **STATIC** |
| S-11 | the licence-node row beyond byte `+7` | **WRONG-IN-PASS-1** (DOC residue) | "license node row (table 02EBF038, stride = word at +8) / +0x05 category byte -> requirement kind via 00323890 / +0x08 uint16 id[8] -> the abilities this node grants" (`12-Items-Equipment-Shops-License/license-check-what-the-board-actually-tests.md:237`–`:239`; present in `df2c9f47`) | The SetSaveData page does not point to it. Bytes `+0`–`+4` and `+6` are not stated on either page. |
| S-12 | `0035BAA0`, the one-shot leader setter | **CLOSED** (elsewhere; DOC residue) | "Field party-leader selection \| proven - D-pad Up/Down … commits via `0035BAA0`" (`16-UI/Request-Router/ui-request-router.md:77`). The body is new since pass 1: "returns without a call when `ecx` equals dword `022C8070`; otherwise calls …" (`:990`). | 11-Party names it only in the README anchors (`README.md:22`). No 11-Party page describes it or points to the router page. |
| S-13 | roster writers in the TSV that no page described | **CLOSED** | Each extra TSV write is now annotated "not a roster write - corrected 2026-10-02, OPUS: the store goes through lea [0209A210] with the index clamped to 0..15, the 16-qword array after the 32-byte roster at 0209A1F0" (`party-roster-slots-accesses.tsv`, rows `00266E1B`, `00269628`, `0026ADA0`, `0026ADB9`, `0026CF13`). The page lists the five writers (`party-roster-and-control-suppression.md:149`). | The TSV still has no row for `00266530`, the initialiser's store at `0026677C` (`party-roster-and-control-suppression.md:147`). OPUS's record routes the regeneration to SWE2-DATA (`_index/candidates/opus-party-readiness-fixes-1002/consumer-check.md:37`). |
| S-14 | the camera copy direction | **OPEN** | The contract still labels the two copies: "`00259470` … copy `02098580 -> 02097D20` … the roster state bank's push direction" and "`002593D0` … `02097D20 -> 02098580` … the restore arm" (`CONTRACT-party-focus-and-control-suppression.md:321`, `:325`). The active-party page: "`00359470` \| … all `0x860` bytes of context 0 copied over context 1"; "`0035948F` \| … context 1 copied back over context 0" (`active-party-reserve-and-the-moment-the-leader-changes.md:415`–`:416`). The contexts are "Two `0x860`-byte contexts at `02097D20`", so context 1 is `02097D20 + 0x860 = 02098580`. That makes the contract's "save" `00259470` a context 1 → 0 copy, while the active-party page's first copy is context 0 → 1. | Which helper each site calls. As written, the two pages disagree on the direction of the "save". **STATIC** |
| S-15 | the `022BE974` bracket | **OPEN** | "When `022BE974` is non-zero the bracket does nothing." (`BSB/the-battle-state-block-field-map.md:420`). No page names a writer. | What sets `022BE974`, and what it means. **STATIC** |
| S-16 | initial values | **OPEN** | No 11-Party page states the value of record `+0x12` before its first assignment, or whether the focus block and the lock words survive a save / load. The lock words are cleared by the party-focus reset `003590E0` (`party-roster-and-control-suppression.md:671`–`:672`), but when that reset runs relative to a load is not stated. | **STATIC** |
| S-17 | the wider masks' other bits | **WRONG-IN-PASS-1** (DOC residue) | "Stop, Sleep, Confuse, **Immobilize** and Berserk" for bits 3, 4, 5, 14, 27 (`15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md:645`–`:651`; present in `df2c9f47`) | PF-7 names only bit 14 (`CONTRACT-party-focus-and-control-suppression.md:154`–`:155`) and does not point to the policy page. |
| S-18 | the packed-handle encoding | **WRONG-IN-PASS-1** (DOC residue) | "~~How `ActorHandle_EncodeRegistryEntry` encodes~~ **ANSWERED 2026-09-10, §11.**" (`04-Actor-Entity/battleunit-slot-pool-and-actor-class.md:287`; §11 at `:435`) | 11-Party uses the encoder (`party-roster-and-control-suppression.md:104`) without a pointer. |
| S-19 | what `003202F0` does with record 26 | **WRONG-IN-PASS-1** (DOC residue) | "`003202F0` returns the **authored selector**: definition-row byte `+0x13` for a party member, or the equipment-descriptor-derived byte …" (`01-Script-VM-Native-Bridge/Party-Presentation-Verbs/the-party-read-in-state-machine.md:113`; UQ-51 ANSWERED 2026-09-16, `:192`) | The field map's FO-5 answer (`BSB/the-battle-state-block-field-map.md:445`–`:446`) does not point to it. |

### 2.3 Pass-1 value-changing contradictions (pass 1 §3.1, C-V1 to C-V27)

A contradiction is **CLOSED** when its losing side is now struck or annotated in place by a dated correction, so a
reader of either page reaches the same value. Unless stated otherwise, every correction quoted is "*(corrected
2026-10-02, OPUS: …)*".

| # | verdict | evidence (`page:line`) | residue |
|---|---|---|---|
| C-V1 out-of-range slot install | CLOSED (side B) | §10 now: "step 2 is skipped, step 5 still stores past the array … while `roster[slot]`, past the four entries, points at it" (`CONTRACT-party-slot-assignment.md:205`–`:207`); evidence row corrected (`:366`) | — |
| C-V2 the displaced occupant | CLOSED (B) | "the occupant it displaces keeps its `+0x12` and `+0x0F` while `roster[slot]` names the newcomer" (`party-roster-and-control-suppression.md:138`); call chain annotated (`:284`) | — |
| C-V3 init-path slot bytes | CLOSED (B) | "in `0x80`–`0xFE` *(corrected … `0026673E jns` skips the block for a byte without bit 7 …)*" (`party-roster-and-control-suppression.md:143`); "only `0x80`–`0xFE` assign" (`CONTRACT-party-slot-assignment.md:44`) | — |
| C-V4 `+0x0F` in the reproduction code | CLOSED (B) | "`/* <- corrected 2026-10-02, OPUS - 00269CD9 also stores prev->+0x0F = 3 */`" and the tail comment (`CONTRACT-party-slot-assignment.md:250`, `:255`) | — |
| C-V5 maps 1–4 written after the copy | **NARROWED** | Struck on all three body pages: `the-five-parallel-slot-maps.md:122`, `:181`; `active-party-reserve-and-the-moment-the-leader-changes.md:118`, `:133`; `CONTRACT-the-five-parallel-slot-maps.md:246` | Two unstruck statements of side A remain in the contract's §14: "class 0 is the live map and classes 1–4 are four frozen snapshots of it." (`CONTRACT-the-five-parallel-slot-maps.md:236`–`:237`) and "structurally classes 1–4 read the same frozen bytes" (`:252`). Both contradict SM-5 and the same section's `:229`. **DOC** |
| C-V6 refresher arms | CLOSED (B) | "Modes 3 and 5 restore map 4 …" (`the-five-parallel-slot-maps.md:133`); field-map row annotated (`BSB/the-battle-state-block-field-map.md:90`) | — |
| C-V7 writers of map 0 | CLOSED (B) | "Map 0 is written by the reset's `0xFFFF` loop (`00237107`), the initialiser `00329CC0` and `00329080`" (`the-five-parallel-slot-maps.md:185`); `active-party-reserve-and-the-moment-the-leader-changes.md:127` | — |
| C-V8 source table address | CLOSED (B) | "~~`0x01EC9260`~~ `01EED260`" (`CONTRACT-the-five-parallel-slot-maps.md:239`, evidence `:286`) | — |
| C-V9 `003266DB` | CLOSED (B) | "`003266DB` is `mov qword ptr [rsp + 0x68], r12` inside `003266C0`" (`CONTRACT-the-five-parallel-slot-maps.md:274`, `:286`) | — |
| C-V10 the class census | CLOSED (a re-count; neither side) | "**32 sites, 31 of them passing a constant**" (`active-party-reserve-and-the-moment-the-leader-changes.md:97`); class 0 has two callers (`:101`, `:107`); class 3 "**24 sites**" (`:103`); contract evidence "24 constant sites, and class 4's one computed site is `0030A804`, of 32" (`CONTRACT-the-five-parallel-slot-maps.md:287`) | — |
| C-V11 `00321100`'s polarity | CLOSED (B) | "is `0xFF`, or whose class-`0x17` check fails, returns *(corrected … `0032113D je 0x321158` …)*" (`the-five-parallel-slot-maps.md:376`) | — |
| C-V12 map-1 immediate scan | CLOSED (a re-count) | both pages now: 6 of map 1, 3 of map 3, no write through a map 1–4 base (`active-party-reserve-and-the-moment-the-leader-changes.md:127`; `the-five-parallel-slot-maps.md:171`, `:175`) | — |
| C-V13 guest placement | CLOSED (B) | "the first free roster index of 3, 2, 1, never 0" (`active-party-reserve-and-the-moment-the-leader-changes.md:321`) | — |
| C-V14 leader-handle writers | CLOSED (B) | "~~four in reality~~ and three in reality" (`active-party-reserve-and-the-moment-the-leader-changes.md:498`) | — |
| C-V15 kind-byte sites | CLOSED (B) | "two more sites, seven in all" (`active-party-reserve-and-the-moment-the-leader-changes.md:268`); the extra store is `003594D3` (`CONTRACT-party-focus-and-control-suppression.md:94`) | — |
| C-V16 getter call sites | CLOSED (B) | "twenty-eight call sites in twenty-five functions" (`active-party-reserve-and-the-moment-the-leader-changes.md:32`) | — |
| C-V17 what reaches `0209A2C5` | CLOSED (A) | "publishes ~~`ebx & 1`~~ the inverse of bit 1 of `ebx`" (`party-roster-and-control-suppression.md:484`) | — |
| C-V18 `00359200`'s targets | CLOSED (B) | "`dword[022C8000]`" and "`003588B0(dword[022C7FE0])`" in the note itself (`party-roster-and-control-suppression.md:501`, `:503`) | — |
| C-V19 when presets grant the licence board | CLOSED (**A**, not B) | "an LP of `0xFFFF` takes `0016D6A0`, a bare `ret 0`" and the board loop "runs when LP is NOT `0xFFFF`" (`the-setsavedata-presets-test-battle-scenarios.md:49`); "any value but `0xFFFF` grants the board's per-slot mask, for battle slots ≤ 6" (`:122`); formula annotated (`:159`, `:161`) | The step text's "otherwise" carries no slot bound (N-7) |
| C-V20 roster writer set | CLOSED | the four extra TSV writes annotated "not a roster write" (`party-roster-slots-accesses.tsv`); five writers listed (`party-roster-and-control-suppression.md:149`) | No TSV row for `00266530` (S-13) |
| C-V21 size of the access table | **NARROWED** | Corrected in the body: "1,135 rows, 215 functions, 166 offsets" (`BSB/the-battle-state-block-field-map.md:467`); the records range "683 accesses in 100 functions … 105 offsets" (`:67`–`:68`) | The front matter still says "1,145 accesses in 217 functions over 165 offsets" (`BSB/the-battle-state-block-field-map.md:12`–`:13`). **DOC** |
| C-V22 `+0x5AD0` bits `00313840` clears | CLOSED (B) | "bit 0 cleared by `00313840` with bit 1" (`BSB/the-battle-state-block-field-map.md:109`); "bits 0 and 1" (`:162`) | — |
| C-V23 end of the gambit banks | CLOSED (B) | "`+0x5B10`–~~`+0x7373`~~`+0x736F`" (`BSB/the-battle-state-block-field-map.md:144`) | — |
| C-V24 block `+0x57C8` | CLOSED (B) | "class 7's second region, the descriptors themselves being static at `01EEBCC0`" (`BSB/the-battle-state-block-field-map.md:53`); layout annotated (`:350`); contract BS-1 (`BSB/CONTRACT-battle-state-block.md:72`) | — |
| C-V25 MP percentage | CLOSED (B) | "(100 in 220 rows, 80 in four and 70 in two …)" (`the-setsavedata-presets-test-battle-scenarios.md:123`); `:185` | — |
| C-V26 block size | CLOSED (B) | "**Size: `0x7410`, measured**" (`the-five-parallel-slot-maps.md:241`); limits struck (`:288`) | — |
| C-V27 resolver class-0 arm | CLOSED (B) | "~~`0031B9F0`~~ `0031BAAA`" (`the-five-parallel-slot-maps.md:258`) | — |

### 2.4 Pass-1 stale and banner items (pass 1 §3.2, C-B1 to C-B27)

| # | verdict | evidence (`page:line`) | residue |
|---|---|---|---|
| C-B1 README statuses and index | CLOSED | three statuses corrected to AUDITED (`README.md:14`, `:18`, `:25`); six omitted pages added (`:30`–`:36`) | — |
| C-B2 "not read" key-address rows | CLOSED | `party-roster-and-control-suppression.md:215`, `:221`, `:222`, `:224`, `:225` | `002E8100` is still "not read" there (N-5) |
| C-B3 mode 2 | CLOSED | `party-roster-and-control-suppression.md:422`; `CONTRACT-party-focus-and-control-suppression.md:243` | — |
| C-B4 the sketch's null arm | CLOSED | "`// <- corrected 2026-10-02, OPUS - not an all-suppressed arm …`" (`party-roster-and-control-suppression.md:166`) | — |
| C-B5 O-5 wording | CLOSED | "~~they do,~~ they do not" (`active-party-reserve-and-the-moment-the-leader-changes.md:35`) | — |
| C-B6 classes 2 and 4 "unreached" | CLOSED | `active-party-reserve-and-the-moment-the-leader-changes.md:92`, `:145`–`:147` | — |
| C-B7 "what the classes are" | CLOSED | pointer under the heading (`the-five-parallel-slot-maps.md:103`); limit struck (`:295`) | — |
| C-B8 "manager record" | CLOSED | `CONTRACT-party-focus-and-control-suppression.md:176`–`:177`, `:272` | — |
| C-B9 the blend | CLOSED | "*(answered: it is a blend — `00259510` is the family's spherical interpolate …)*" (`CONTRACT-party-focus-and-control-suppression.md:242`) | — |
| C-B10 the secondary handle | CLOSED (in the contract) | `CONTRACT-party-focus-and-control-suppression.md:244` | The roster page still says the camera side "was not read" (N-4) |
| C-B11 when the commit runs | CLOSED | `CONTRACT-party-focus-and-control-suppression.md:285` | — |
| C-B12 `+0x152` and `002681E0` | CLOSED | `CONTRACT-party-slot-assignment.md:353` | — |
| C-B13 the assigner's tail | CLOSED | `CONTRACT-party-slot-assignment.md:132` | — |
| C-B14 the other two bulk clears | CLOSED | `CONTRACT-party-slot-assignment.md:156` | — |
| C-B15 front-matter dates and flags | **OPEN** | unchanged: `last_reviewed: 2026-09-11` and "`crossref_clean: false        # audit_crossrefs.py reports nothing for this document`" (`CONTRACT-party-slot-assignment.md:16`, `:21`); `last_reviewed: 2026-09-11`, `last_pass_kind: authored` (`BSB/the-battle-state-block-field-map.md:16`, `:21`) | **DOC** |
| C-B16 "no experiment" banner | CLOSED | `CONTRACT-the-five-parallel-slot-maps.md:222` | — |
| C-B17 the binder's reset "never read" | CLOSED | `BSB/CONTRACT-battle-state-block.md:227` | — |
| C-B18 BS-5 on SM-7 | CLOSED | `BSB/CONTRACT-battle-state-block.md:123` | — |
| C-B19 SetSaveData as shipped behaviour | **NARROWED** | the shipped half is answered: "two shipped scripts call it" (`the-setsavedata-presets-test-battle-scenarios.md:56`) | The script-corpus count still differs: "two of the 1,115 `us` scripts" (`the-setsavedata-presets-test-battle-scenarios.md:195`) against "the 1,114 decompiled scripts" (`active-party-reserve-and-the-moment-the-leader-changes.md:283`, `:401`; `party-roster-and-control-suppression.md:674`). **DOC** |
| C-B20 ledger box | CLOSED | `the-setsavedata-presets-test-battle-scenarios.md:189` | — |
| C-B21 "inventory temporary snapshot" | CLOSED | `BSB/the-battle-state-block-field-map.md:32`, `:139`, `:349` | — |
| C-B22 `00310DB0` as "the leader-change path" | CLOSED | `active-party-reserve-and-the-moment-the-leader-changes.md:636`, `:644` | — |
| C-B23 the incoming leader's push | CLOSED | `active-party-reserve-and-the-moment-the-leader-changes.md:250`; `CONTRACT-party-focus-and-control-suppression.md:125` | — |
| C-B24 the debug override's verb number | **OPEN** | unchanged: "`result(0x32)` of the default dispatch table" (`active-party-reserve-and-the-moment-the-leader-changes.md:381`–`:382`) against "`0x2032 debug_setdebugpc`" (`party-roster-and-control-suppression.md:684`) | Whether table index `0x32` is call `0x2032`. **DOC** |
| C-B25 "the active party is three" | CLOSED | `party-roster-and-control-suppression.md:383` | — |
| C-B26 `00311E20`'s position read | CLOSED | `BSB/CONTRACT-battle-state-block.md:269` | — |
| C-B27 what `+0x5AA4` is | **NARROWED** | the layout row and the slot-maps page now name the leader (`CONTRACT-the-five-parallel-slot-maps.md:59`; `the-five-parallel-slot-maps.md:110`) | SM-8's own text still reads "It is a `u32` holding the source table's first byte." with no pointer (`CONTRACT-the-five-parallel-slot-maps.md:161`–`:162`). **DOC** |
