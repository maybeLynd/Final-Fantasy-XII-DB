# Reconstruction readiness, pass 2: 07-Combat-Action

- **System folder:** `FFXII TZA/07-Combat-Action/` (slug `07-action`)
- **Stream:** R2, for FABLE (brief `docs/cloud-briefs/re-readiness-r2.md`, part A: pass 1 mapped this system)
- **Pass 1:** `cloud-reports/re-readiness/07-action.md` (2026-10-02, cut from `main` at `c3aec14d`)
- **This pass:** 2026-10-03, against the snapshot at `b23bdddd` (synced from XIIOnline `f9d9053b9`)
- **Method:** text only. Every pass-1 gap was re-read against the current pages and `FFXII TZA/_index/OPEN-QUESTIONS.md`.
  The folder's pages were also diffed against `c3aec14d` to find what changed since pass 1. Nothing here was checked
  against the executable.

## How to read the citations

A citation `page:line` gives the path **below `FFXII TZA/07-Combat-Action/`** and the line number at `b23bdddd`.
Pages in other folders are given **below `FFXII TZA/`** and start with their folder number (`00-…`, `04-…`, `09-…`).
Register rows are cited by id, with the state cell quoted. "Not stated" means no page says it.

Verdicts (brief, part A.2): **CLOSED**, **NARROWED**, **OPEN**, **WRONG-IN-PASS-1**. Classes for OPEN and NEW gaps
(brief, Rules): **STATIC**, **RUNTIME**, **DATA**, **DOC**.

## 1. Summary

**Pass-1 gaps: 94** (§2.1: 20, §2.2: 10, §2.3: 11, §2.4: 53).

| verdict | §2.1 open items | §2.2 structural | §2.3 fields | §2.4 contradictions | total |
|---|---:|---:|---:|---:|---:|
| CLOSED | 0 | 1 | 0 | 47 | **48** |
| NARROWED | 5 | 5 | 1 | 1 | **12** |
| OPEN | 14 | 2 | 5 | 5 | **26** |
| WRONG-IN-PASS-1 | 1 | 2 | 5 | 0 | **8** |
| **total** | 20 | 10 | 11 | 53 | **94** |

The §2.4 column breaks down by group:
- A, value-changing: 17 of 17 CLOSED.
- B, counts and caller sets: 5 CLOSED, 1 NARROWED, 3 OPEN.
- C, stale claims: 22 of 22 CLOSED.
- D, banners: 3 CLOSED, 2 OPEN.

**Class of the 38 pass-1 gaps still OPEN or NARROWED**, by each gap's main residue: STATIC 27, RUNTIME 7, DOC 4, DATA 0.
One of them, §2.1-15, also has a DATA half.

**New gaps: 14.** STATIC 6, RUNTIME 1, DATA 0, DOC 7.

**Rating:** pass 1 gave **NOT YET**, with the core at MOSTLY. Pass 2 gives **NOT YET**, unchanged, with the core now
close to READY (§4).

What moved since pass 1:
- **On 2026-10-02 OPUS corrected the pages against every value-changing contradiction pass 1 listed** (A1–A17), and
  struck or annotated all 22 stale claims (C1–C22). Examples: the band-two commit, the `+0x770` latch, the combo table
  and its draw count, the `+0x01` recipe, the steal rule, and the `022C1DB8` byte.
- **New contract text arrived:**
  - the post-result events, in `CONTRACT-apply-result-to-target.md` §8a (FABLE, 2026-10-03);
  - the presentation-slot ABI, in `CONTRACT-native-command-seam.md:158-169`;
  - thirteen dated OV-42 subsections on the availability page (`Action-Availability/…:737-1457`).

  These answer the effective action id, most of the special-sequence routine `00306760`, the slot walker's path, the
  event ring's reset and the message realiser.
- **Eight pass-1 gaps were already answered at pass-1 time**, on pages outside this folder or in the register. Among
  them:
  - frame order: `00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md` and the battle-unit
    field map;
  - the 24-byte order record: `09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md`;
  - the 64-byte record's second half: GR-8;
  - `+0x760` / `+0x764`: FW-2.

  The folder still lacks pointers to these answers. Those missing pointers are counted below as DOC gaps.

What still decides the rating:
- the per-target execution step `Battle_ProcessActionTarget` (`00307300`) has no page;
- three order handlers are undecoded;
- the text engines' escape grammar is unread;
- no part of the system has live evidence.

## 2. Pass-1 gaps

Each row gives:
- the pass-1 id, as `§2.1-n` for the pages' own open items, `S n` for §2.2 structural gaps, `F n` for §2.3 fields
  (in pass 1's bullet order), or `A`/`B`/`C`/`D n` for §2.4 contradictions;
- the verdict;
- the evidence, quoted;
- what is still missing, with its class.

### 2.1 Open or partly open items the pages themselves listed (pass-1 §2.1)

| id | gap (pass 1) | verdict | evidence now | still missing (class) |
|---|---|---|---|---|
| §2.1-1 | commit and target buffer: no live capture | OPEN | "**Evidence class: isolated original-code, over the whole function. Live capture: still absent.**" (`CONTRACT-commit-action.md:240`); "it still holds for the **caller**, which nothing has executed" (`:323`); "**Evidence class: isolated original-code. Live capture: still absent.**" (`CONTRACT-battle-target-buffer.md:229`) | a live capture of `0030F760` and of the target buffer; the caller of the commit executed (RUNTIME) |
| §2.1-2 | the other four contracts are native replay, not live | OPEN | seam: "replay, not live" (`CONTRACT-native-command-seam.md:189-190`); handler table: "class is native replay, not live." (`CONTRACT-battle-action-handler-table.md:159`); combo: "the evidence class is native replay, not live" (`CONTRACT-combo-continuation.md:187`); applier: "live-game reachability, and whole-system L2 acceptance" withheld (`CONTRACT-apply-result-to-target.md:432`), and the new §8a: "**Live: none.**" (`:366`) | live runs of all four (RUNTIME) |
| §2.1-3 | message-table binding has no live read (`FL-2`) | OPEN | register FL-2: "**SUPERSEDED 2026-09-26 … the file half is traced statically … The steal's ring entries are a live read carried by ASTRA-QUEUE AQ-16.**" The page agrees: "*(closed — the register row is ~~WITHDRAWN~~ SUPERSEDED, 2026-09-26.)*" (`Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:431`), and "the runtime confirmation is still owed (`FL-2`)" (`:316`) | the steal's ring entries `0x33` / `0x34` at `02EBB560`, observed live (RUNTIME; FL-2 SUPERSEDED, AQ-16) |
| §2.1-4 | the commit's callees in a live game | OPEN | "Every callee is scripted, so nothing here shows what a real cancel, a real target-buffer reset or a …" (`CONTRACT-commit-action.md:301-302`) | the callees' effects in a live game (RUNTIME) |
| §2.1-5 | whether the pending ring can hold an entry the funnel rejects | OPEN | "Whether the pending-selection ring can hold an entry that the commit funnel then rejects, and what …" (`CONTRACT-native-command-seam.md:194-195`) | the rejected-entry case and its fate (STATIC) |
| §2.1-6 | reset frequency and the enmity delegate's full effects | OPEN | "The frequency of these resets in live fights and the delegate's full effects are not established here" (`the-moment-an-action-is-committed.md:219-220`). The delegate `003220E0` is executed by EXP-151 (`:216-218`), dated 2026-09-25, so this was already true at pass 1 | the live reset frequency; the delegate's full effects (RUNTIME) |
| §2.1-7 | what a presentation slot presents; why only the special-sequence update advances `+0x696` | OPEN | "**Not claimed:** what a …" (`the-moment-an-action-is-committed.md:274-276`), unchanged. `00306760`'s dispatch and queue store are now read (`Action-Availability/battle-command-availability-and-reason-codes.md:1043-1065`), but not its `+0x695` → `+0x696` move | what a slot presents; why only `00306760` moves the handle to `+0x696`; whether a stage is skipped (STATIC; the last needs RUNTIME) |
| §2.1-8 | 13-phase machine: called bodies not read; `+0x760` / `+0x764` not named | NARROWED | **`+0x760` / `+0x764`:** named by register FW-2, ANSWERED 2026-09-12, already at pass 1: "`+0x764` (a `rand()`-seeded progress threshold that `+0x760` climbs toward by 100 per advance)". **Called bodies, now read:** phase 6's word comes from the getter `00387090`, which "returns a zero-extended WORD" (`Action-Availability/…:985-1001`); case 9's order (`:1204-1210`); `00305640` (`:1268-1282`) | the page still says "what they count was not named" (`Command-And-Action-Seam/native-command-seam.md:216-217`; new gap N3). Phase 8's callee "one call on the `+0x6B0` block" (`:206`), the preview and the target builder's 22 calls are still unread (`Action-Availability/…:1249-1250`) (STATIC) |
| §2.1-9 | presentation slot: asset kinds, codes 1 and 3, `+0x2C` upper bits | OPEN | "**Not named:** which asset kind the `+0x10` loader and the `+0x14` event table hold" (`Command-And-Action-Seam/native-command-seam.md:465`); "What codes `1` and `3` mean was not read." (`:537`); "**Still open:** … the `+0x2C` bits above bit 4, and the meanings of the 2-bit codes." (`:540`) | all three (STATIC) |
| §2.1-10 | the eight order handlers; four unnamed | NARROWED | the contract now reads "the rest is its open work *(answered in part: see Action-Dispatch/battle-action-handler-table.md - AT-3, the `0x4021` wait handler, and AT-4 with section 10, the set/clear-status runs; 2026-10-02, OPUS)*" (`CONTRACT-battle-action-handler-table.md:163-164`). `002FE840` was already described at pass 1: "**Z-14 ANSWERED 2026-09-12 (FABLE): it flips the combat stance.** Its order-table slot `01EEC460[0x14D]` is the dedicated handler `002FE840`" (`09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md:457`) | `002FE660`'s three real bodies, `002FE8D0`, `002FE910` beyond its fragment; the name column is still "—" for four handlers (`Action-Dispatch/battle-action-handler-table.md:125-129`) (STATIC) |
| §2.1-11 | the 64-byte records' surviving half | WRONG-IN-PASS-1 | register GR-8, already "**ANSWERED 2026-09-30 …: the second half, `+0x20`..`+0x3F`, is never accessed - no instruction in the image reads, writes or copies it, and `00386C10` clears exactly `+0x00`..`+0x1F`**" when pass 1 was cut | nothing for a port. The page still says "**what survives is not established here.**" (`Action-Dispatch/battle-action-handler-table.md:664`; new gap N4) |
| §2.1-12 | the cost side of the resource check is opaque | NARROWED | `00309060` is answered: "~~`FUN_00309060`~~ … *(answered for `00309060`: see using-an-item-is-an-action-that-costs-an-item.md, … the gil cost reason `0x15` compares; 2026-10-02, OPUS)*" (`Action-Availability/…:518`). The consume helper is read: "`FUN_00309110` and `00308FF0` … each get the unit and q's low 16 bits", and "It calls `00253690`, subtracts the unit's DWORD `+0xE54` in 32 bits, and passes the difference to the gil call" (`:1271-1279`) | the bodies of `003037A0`, `00309110`, `00308FF0` and `00253690` (`:518`; "The native effects of the cost, stats, gil, type-10 and final callees … are not read", `:1306`) (STATIC) |
| §2.1-13 | the frustum reason code; kind names; OV-42 | NARROWED | frustum, unchanged: "Which reason code a failed frustum test yields is not read here." (`Action-Availability/…:598`). Kinds, unchanged: "read only as calls" (`:379`). OV-42 gained thirteen dated subsections since pass 1 (`:737-1457`). Register OV-42: "**PARTLY ANSWERED 2026-09-29** … Still OPEN: a nonzero raw +5, the nonnegative override word, `003068D4` and the other producers, the interpreter transfer …" | the frustum code; the four filter predicates; the rest of OV-42 (STATIC; natural rejection RUNTIME) |
| §2.1-14 | target gathering: mask builder, wrapper callers, two of three callers | OPEN | "NOT read - the eligibility mask builder beyond its result, the three callers of the shape descriptor's wrapper, what the action state machine does around the call" (`how-an-action-gathers-its-targets.md:21-23`); "The other two were not read." (`:140`). The page's step question is answered (C6) | the mask builder; the wrapper's callers (STATIC) |
| §2.1-15 | range bands: back-off test, avoidance, §6 predicate, clearance; bit-26 pairs not tallied | OPEN | "**Not read:** the further test of the back-off arm, the avoidance manoeuvre, the predicate of section 6, and the clearance …" (`how-close-a-unit-must-stand-to-act.md:128`); "their values were not tallied here" (`:193`) | the four bodies (STATIC); the per-character bit-26 pairs (DATA) |
| §2.1-16 | combo bit-22 sweep misses whole-qword stores | OPEN | "A whole-qword store to the flag word is not covered by this sweep." (`how-a-combo-continues-and-what-it-blocks.md:188`) | a qword-store sweep (STATIC) |
| §2.1-17 | target buffer: bit-0 clearer, `+0x0C`, `02F973B8` | OPEN | "either that arm is dead-in-ship, or a clearer hides behind a route the census cannot see" (`CONTRACT-battle-target-buffer.md:366`); "`+0x0C` \| 4 \| — \| — \| **unknown span**" (`:71`); "*Not … established:* the value of `02F973B8`" (`:500`) | the clearer and `+0x0C` (STATIC); the value of `02F973B8`, which lies outside the file image (RUNTIME) |
| §2.1-18 | result record: fields written through stored pointers | OPEN | "What it cannot see: …" (`Result-Record/the-result-record-field-map.md:124`) | the pointer-routed writes (STATIC) |
| §2.1-19 | applier: nested re-entry, steal-id origin | OPEN | "* Recursive/nested applier behavior; recorded thunks leave its trigger clear." / "* Authored origin/availability of the steal IDs …" (`CONTRACT-apply-result-to-target.md:482-483`); "Nested re-entry was not …" (`:432`) | nested re-entry driven (RUNTIME); steal-id origin (DATA) |
| §2.1-20 | messages: escape grammar, class 1, category `0x12`, locomotion posts, other languages | NARROWED | the realiser and last mile are now contracted: "**Invariant I12 — the realiser reads four kind bytes of the row and hands on a fixed request.**" (`CONTRACT-apply-result-to-target.md:301-338`). Other languages: "The 100-row `ch` / `cn` / `in` / `kr` tables therefore cover every posted id. Their rows 0–99 differ from `us` only in kind bytes, not in layout." (`:345-346`) | the escape grammar ("Not traced: … the engines' escape grammar", `:370`; `Post-Result-Events/…:429-430`); "Whether class 1 ever lists a member without a unit is not read here." (`:497`); "Which menu entries carry category `0x12` is not read." (`:500`); "Which messages it posts" (`:681`) (STATIC) |

### 2.2 Structural gaps (pass-1 §2.2)

| id | gap (pass 1) | verdict | evidence now | still missing (class) |
|---|---|---|---|---|
| S1 | the per-target execution step `Battle_ProcessActionTarget` `00307300` has no page; the timeline handlers `00319F50` and `00325260` are not described | OPEN | still fragments only. The target-buffer contract adds one: "`Battle_ProcessActionTarget` ORs `0x100` into the entry's `+8` at `003075CB` when the result's flag word B bit 3, knockback, is set" (`CONTRACT-battle-target-buffer.md:281`). No page in the database has `00307300` or `00319F50` as its subject | which timeline event, in which phase, applies a hit; how many targets one event processes; the per-entry loop (STATIC) |
| S2 | frame scheduling: order of `00234520`, `00234590` and the per-unit frame; call order inside `00308610` | WRONG-IN-PASS-1 | both were stated outside the folder at pass 1 (the text is at `c3aec14d`). **Between the drivers:** "`BattleSystem_RunFieldFrameOrchestrator(slot)` `003141D4` … `ActorManager_RunFieldRuntimePass(slot)` `003141DB` the actor drive loop … `00234520(slot)` `003141E2`", and "**So the ordering is: field frame (slot 0) → actor drive loop → per unit, the lifecycle frame.**" (`00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md:103-105`, `:276`). **Inside `00308610`:** "`00308270` + `003105D0` (`003086AA`/`003086B2`), … `002FFB60` (`003086FC`), `00305AB0` + `00307BE0` (`0030874C`/`00308754`), `00253B90` (`0030877D`), `0030FA00` (`0030879F`)" (`04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md:1078-1084`) | the folder has no pointer to either (new gap N6, DOC). The two pages disagree on `00308610`'s size (new gap N1) |
| S3 | five of the eight order handlers are not decoded here | OPEN | `002FE840` was already decoded at pass 1 on the 09 page (§2.1-10). The rest are unchanged: `002FE660` "48 of the 54 ids land on `or eax, -1; ret`" (`Action-Dispatch/battle-action-handler-table.md:493`); `002FE910` "`byte[+0x6B4] == 0` selects `qword[+0x708]`, `word[rax+2]`" (`:744-745`); `002FE8D0` appears only in the table (`:128`) | `002FE660`'s three real bodies; `002FE8D0`; `002FE910`'s behaviour beyond the fragment; the return value of every handler except the wait handler (STATIC) |
| S4 | the order record's format beyond `+0` and `+2` | WRONG-IN-PASS-1 | stated at pass 1 on the 09 page: "The 24-byte order record: `+0` selector, `+2` percent, `+4` flags, three 6-byte entries" (`09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md:591`; §8g at `:1169`); "`AiOrderRecord`, 24 bytes … room for fourteen per set" (`09-Combat-AI-And-Gambits/CONTRACT-gambit-walk.md:52`) | the folder has no pointer (new gap N7, DOC) |
| S5 | the presentation side: slot walker, track resources, `00306760` and `022C2160`, phase 8, consumers of events `0x2001` / `0x2010` | NARROWED | **Slot walker:** "`0030CBE0` reads the presentation slot's u16 action id (`0030CC25`). It checks the id as class `0x14` (`0030CC32`) … and passes the pointer to `0030CE10`" (`Action-Availability/…:750-752`). **`00306760`:** "It loads the kind DWORD `022C215C` … Kinds 1..6 jump through the six entries … Only the kind-4 arm (+ 0xE8) reaches the queue store" and "Every return of the routine stores 5 to `022C2160`" (`:1045-1047`, `:1064`). **Its gate:** "`022C2160` is 0, or it is 1 with the same owner in `022C2168`" (`:793`). **Events:** register BT-4, ANSWERED 2026-09-27, already at pass 1: "`0x2010` in place of `0x2001` ready for the type-0x1A mount while turbo is on (00305080, 00303F00)" | the asset kinds of the three tracks (`Command-And-Action-Seam/native-command-seam.md:465`); phase 8's callee (`:206`); `00306760`'s kind 1, 2, 3, 5 and 6 arms; the other writers and the initial value of `022C2160` / `022C215C` (not stated in this folder) (STATIC) |
| S6 | callees named without description | NARROWED | **Now described in the folder:** `002ED2A0`: "calls `003588B0` … otherwise tail-jumps `003E6B50(record, rdx)`" (`CONTRACT-commit-action.md:552`). `00313120` "resets the buffer and appends to it at `0031325F` / `0031328C`" (`CONTRACT-battle-target-buffer.md:142`). **Already described elsewhere at pass 1:** `00310780` (`10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md:267`, `10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md:708-715`); `003065D0`, which "commit[s] the deferred-HP queue at `022C1F50`" (`08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md:245`); `00309990` (`04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md:299`); `002FFB60` (same page, the `00308610` subtree table after `:1078`); `00300060` (`16-UI/CONTRACT-ui-request-router.md:451`); `003220E0`, executed by EXP-151 (`the-moment-an-action-is-committed.md:216-218`) | `0033C9B0`; `0030DB70` beyond its record arm (`Action-Availability/…:783-789`); `00300280` beyond "the refund `00300280` adds it back" (`:502`); `003220E0`'s full effects (`the-moment-an-action-is-committed.md:219-220`) (STATIC) |
| S7 | text format engines: escape grammar unread; a line cannot be rendered | NARROWED | the realiser and last mile are contracted (I12): slot kinds from row bytes `+0`–`+2` and `+5`, the 9-entry kind map, the `0x38`-byte request to `0035B990`, and "**otherwise `0028E110(text, +0x1F, 0, 0)` is always called**" (`CONTRACT-apply-result-to-target.md:301-338`) | the escape grammar of `002B49F0` / `002B40C0` ("Not traced: … the engines' escape grammar; `00536410`'s text", `:370-371`); the style table `020BE610` and palette `0215E6C8` (`Post-Result-Events/…:429-430`) (STATIC) |
| S8 | initial values: rings, event ring and index, `02089340`, unit fields | NARROWED | **Event ring:** "The leaf `004696A0` is branch-free. It sets event `0xFFFF`, stats 0, tick 0 and word `+0x18` 0 in all ten entries, and sets the index to 0 … Its only caller is `0033A380` (`0033A3B0`), whose only caller is `00234463` in area initialisation `002342F0`" (`CONTRACT-apply-result-to-target.md:288-290`). **`02089340`:** "Area initialisation clears all three (`0023432D`, `and 0xFFFFC01E`)", for bits 7, 12 and 13 (`:264`) | the load-time value of the rings `022BEDA0` / `022BE980`; the other bits of `02089340`; the spawn values of unit `+0x6B4`, `+0x6B7`, `+0x770`, `+0x750` / `+0x754`, `+0xEA0` / `+0xEA4` / `+0xEA8` (STATIC) |
| S9 | the `022C1DB0` 12-byte per-slot row has no layout | NARROWED | word `+0` and dword `+4`: "restoring `+0xDC8` from its word `+0` and `+0xE58` from its dword `+4` (`003082AE`–`003082C0`; `00312FA0` saved them at `003130AB`–`003130C7`)" (`CONTRACT-commit-action.md:350`). Byte `+8`: "`022C1DB8` is byte `+8` of a 12-byte per-slot row at `022C1DB0`, the reserve-member slot `BattleUnit_IssueCommand` parks (`00311DA5`)" (`the-moment-an-action-is-committed.md:321`) | bytes `+2`–`+3` and `+9`–`+0xB`; a single layout table on one page (STATIC) |
| S10 | effective action id: no formula | CLOSED | "A non-null query whose BYTE `+5` is 0 selects record BYTE `+4` of the 64-byte bank at `0208D480` … A non-null O1 selects record BYTE `+0xEA9` of the bank at `0208DE80` … If that word is `0x9F` and a record was selected, the getter returns the record's WORD `+0x10` instead … Otherwise it returns the `+0x714` word itself" (`Action-Availability/…:994-1000`). The cache side: "`ResolveAndCacheEffectiveActionId` (`00387A50`) stores the pick in the source's record `+0x10` (`00387ADE`) when the committed id is `0x9F`" (`08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md:190-191`) | — |

### 2.3 Fields written but left unexplained (pass-1 §2.3)

| id | gap (pass 1) | verdict | evidence now | still missing (class) |
|---|---|---|---|---|
| F1 | target buffer entry `+0x0C`; header byte `+0x03` | OPEN | "`+0x0C` \| 4 \| — \| — \| **unknown span**, not declared padding \| no access" (`CONTRACT-battle-target-buffer.md:71`); "`+0x03` \| 1 \| — \| — \| never separately written" (`:61`) | whether `+0x0C` and `+0x03` are padding (STATIC) |
| F2 | presentation slot `+0x2C` upper bits; codes 1 and 3 | OPEN | as §2.1-9 (`Command-And-Action-Seam/native-command-seam.md:537`, `:540`) | as §2.1-9 (STATIC) |
| F3 | unit `+0x760` / `+0x764` | WRONG-IN-PASS-1 | FW-2, ANSWERED 2026-09-12: "`+0x764` (a `rand()`-seeded progress threshold that `+0x760` climbs toward by 100 per advance)" | nothing for a port. The page still lacks it (`Command-And-Action-Seam/native-command-seam.md:216-217`; new gap N3) |
| F4 | what the cancel clears: `+0x1F0` bit 5, and the masks `0xFFFFBFF75FFFCFFF` / `0xFFDFFF7F` | OPEN | "`+0x1F0` …" (`the-moment-an-action-is-committed.md:134`); "`0xFFFFBFF75FFFCFFF` and `dword[unit+4]` with `0xFFDFFF7F`" (`CONTRACT-commit-action.md:503`), unchanged | the meaning of each cleared bit (STATIC) |
| F5 | unit `+0xEA0` | WRONG-IN-PASS-1 | FW-2 named it at pass 1: "`+0xEA0` the in-flight attacker slot mask `FUN_00305230` sets on the target (`00305326`)" | still open: the teardown's compare value, "**this document does not claim it is zero.**" (`the-moment-an-action-is-committed.md:250`) (STATIC) |
| F6 | unit `+0x6C0` / `+0x6D0` from the `0x4022` precondition | WRONG-IN-PASS-1 | FW-2 at pass 1: "**Residue, a fact not a gap:** `+0x06C`, `+0x158`, `+0x6C0`, `+0x74C`, `+0x758`, `+0xB90` are write-only on every static route"; AT-6: "`0x4022` storing the distance threshold and vector at unit `+0x6D0` / `+0x6C0`" | a reader of `+0x6D0`, which neither row names (STATIC) |
| F7 | result `+0x40` / `+0x41` have no writer; `+0x30` / `+0x130` written and never read | OPEN | the writer row now says "`003900C0` the first two to clear (`+0x3E`, `+0x3F`)" (`Result-Record/the-result-record-field-map.md:151`); `+0x3E` / `+0x3F` have writers and `+0x40` / `+0x41` do not (`:86-87`) | a writer of `+0x40` / `+0x41`, or the statement that only the initialiser's `0xFF` reaches them (STATIC). `+0x30` / `+0x130` are stated facts |
| F8 | the 64-byte records' second half | WRONG-IN-PASS-1 | GR-8, ANSWERED 2026-09-30 (§2.1-11) | the page pointer (N4) |
| F9 | action row `+0x0B`, `+0x21`, `+0x0C` bits 15 / 18 / 20 | WRONG-IN-PASS-1 | not gaps at pass 1: "`+0x21` and `+0x0B` are read by nothing (AY-2, GR-5)" (`Action-Definition-Row/the-action-definition-row.md:28`); GR-5: "On rows 182-207 it repeats the matching summon row's `+0x0A` (the MP cost) … editing `+0x0B` changes nothing in play"; UQ-107: "Bits 15, 18 and 20 are authored on 24, 1 and 81 rows and read by nothing" | — |
| F10 | message row `+6` / `+7` zero on all 102 rows | NARROWED | §8a lists the row bytes the poster, filter and realiser read: `+0`–`+2` and `+5` (kinds), `+3` (filter threshold and category), `+4` bit 0 (rate limit) (`CONTRACT-apply-result-to-target.md:268`, `:273`, `:305-306`, `:327`). None of them reads `+6` / `+7` | whether anything else reads `+6` / `+7` (STATIC) |
| F11 | candidate pick: `02F973B8` outside the file image | OPEN | as §2.1-17 (`CONTRACT-battle-target-buffer.md:491`, `:500`) | the runtime value (RUNTIME) |

### 2.4 Contradictions (pass-1 §2.4)

All 17 Group A contradictions are CLOSED by dated corrections that OPUS made on 2026-10-02. In every case the page now
agrees with the side pass 1 favoured. A2, A9 and A13 were undecided in pass 1; they are now decided on the page.

**A. Value-changing**

| id | contradiction (pass 1) | verdict | evidence now |
|---|---|---|---|
| A1 | the commit's reproduction formula against its own ordering | CLOSED | the formula's lines are annotated: "`resetTargetBuffer(actor)  /* 00316CF0 */   # <- corrected 2026-10-02, OPUS - band one only (id <= 0x21E)…`"; "`+0x770` is the re-commit latch, not the stats kind byte … Missing here - the `+0x6B0` bit-1 copy … the `+0x750` clear … and the band-one propagation walk"; "`updateAttackerMask` … band one with a resolved target only" (`CONTRACT-commit-action.md:221-224`) |
| A2 | does a band-two commit update the attacker mask? | CLOSED (was undecided) | "8. **band one, with a resolved target, only:** update the target's attacker mask …" (`CONTRACT-commit-action.md:176`); "re-picks the `+0x6B0` bit-1 slot and returns 1 **without** the mask" (`:184`); "this ja accepts, it does not refuse; `0030F97A` is mov eax, 1 (committed). It skips the propagation walk and the attacker mask for ids above 0x21E" (`the-moment-an-action-is-committed.md:67`) |
| A3 | the `+0x770` re-commit latch | CLOSED | "for a unit whose stats kind byte `[+0x698]+5` is 0, a re-issued action that matches what was just cancelled keeps a non-zero `+0x770`; a kind-1 unit keeps it whatever it commits, and any other combination clears it" (`the-moment-an-action-is-committed.md:140`; also `:47`) |
| A4 | which table holds the memoised combo count | CLOSED | "`0208D480 + stats[+4] × 0x40` when the stats kind byte `+5` is 0, else `0208DE80 + unit[+0xEA9] × 0x40`" (`how-a-combo-continues-and-what-it-blocks.md:127`; also `:215`, `:314`, `:337`); `CONTRACT-combo-continuation.md:60`, `:121` |
| A5 | how many generator draws a first combo hit makes | CLOSED | "~~TWICE.~~ once or twelve times.** *(corrected 2026-10-02, OPUS: one draw at `003886FD`; a failed gate `0038871D jbe 0038887E` stops there, a passed one runs the 11-pass loop …)*" (`CONTRACT-combo-continuation.md:98`); also `:147`, `:157`, `:177`, `:268` |
| A6 | capacity of the pending action-selection ring | CLOSED | "a different ~~8-entry queue~~ 64-entry ring drained up to 8 entries per call" (`Command-And-Action-Seam/native-command-seam.md:226`); `README.md:60` |
| A7 | whether the two ring drains behave alike | CLOSED | "advance~~, same resolve-then-act loop~~ *(corrected 2026-10-02, OPUS: the drains differ - `00313CD0` pops eight entries whatever they resolve to …, `00313DB0` stops at the first entry that does not resolve …)*" (`Command-And-Action-Seam/native-command-seam.md:81`) |
| A8 | is the target buffer's `+0x01` read? | CLOSED | "**`+0x01` has a reader, on a stack instance** *(corrected 2026-10-02, OPUS: `00308813 movzx edx, byte ptr [rsi + 1]` in `003087E0` …)*" (`CONTRACT-battle-target-buffer.md:282`); "~~**The field stays UNRESOLVED on purpose.**~~ *(answered: resolved, the candidate buffer's selection recipe …)*" (`:294`) |
| A9 | where the target buffer type lives | CLOSED (was undecided) | "inline twice inside `BattleUnit` (`+0x778`, `+0xBC0`) and also as stack locals" (`CONTRACT-battle-target-buffer.md:53`); the inference built on it is struck (`:285`) |
| A10 | length of the result record's parameter arrays | CLOSED | "**Two 32-bit masks and two parameter arrays of ~~33~~ 32**" (`Result-Record/the-result-record-field-map.md:192`); `README.md:38` |
| A11 | layout of result `+0x3C`–`+0x41` | CLOSED | "six bytes, not statuses; `+0x3C`-`+0x3D` two layer effects to add (mode 2 …) and `+0x3E`-`+0x41` four to clear (mode 0 …)" (`Result-Record/the-result-record-field-map.md:173`; also `:151`) |
| A12 | width of the item field at result `+0x38` | CLOSED | "record `+0x38` (~~`u16`, `-1` = none~~ `i32`, absent when the dword is `-1`; the low word is the id)" (`applying-a-result-to-a-target.md:171`) |
| A13 | type of result `+0x11C` | CLOSED (was undecided) | "`+0x11C` \| ~~2~~ 1 \| ~~u16~~ s8 \| … *(corrected 2026-10-02, OPUS: the applier reads one byte and sign-extends it …)*" (`Result-Record/the-result-record-field-map.md:102`; also `:165`) |
| A14 | who clears the steal-availability bit | CLOSED | "the matching bit … is already clear, because `BattleFormula_ApplyResultMetadata` cleared it for every non-zero slot byte, on any target, before this loop" (`applying-a-result-to-a-target.md:124-126`); "re-cleared, a no-op" (`:170`) |
| A15 | the approach-pacing stand window | CLOSED | "the first ~~30 steps~~ `30 × [01DFE0B4]` steps of the charge, 30 at the 30 fps setting and 60 at the 60 fps one" (`how-close-a-unit-must-stand-to-act.md:115`) |
| A16 | which events `004697C0` posts | CLOSED | "\| `004697C0` \| ~~`0x06`~~ `0x05` / `0x06` / `0x07` \|" (`Post-Result-Events/the-post-result-events-and-the-battle-message-table.md:339`); `Action-Dispatch/battle-action-handler-table.md:671` |
| A17 | what the `022C1DB8` byte is | CLOSED | "The ~~posture byte~~ parked slot byte `+0x6B9` … *(corrected 2026-10-02, OPUS: not a posture …)*" (`CONTRACT-commit-action.md:294-295`; also `:350`, `:414`); `the-moment-an-action-is-committed.md:321` |

**B. Counts, sizes and caller sets**

| id | contradiction (pass 1) | verdict | evidence now / still missing (class) |
|---|---|---|---|
| B1 | size of `0030CA80` | CLOSED | "(`BattleAction_CheckPresentationSlotReady`, 352 B *(corrected 2026-10-02, OPUS: `0030CA80`–`0030CBDF ret`, 104 instructions …)*)" (`Command-And-Action-Seam/native-command-seam.md:580`) |
| B2 | size of `003083B0` | CLOSED | "(~~307 B~~ 596 B *(corrected 2026-10-02, OPUS: `003083B0`–`00308603 ret` …)*)" (`Action-Dispatch/battle-action-handler-table.md:727`) |
| B3 | size of `002FE910` | CLOSED | "~~(~55 B)~~ (52 B *(corrected 2026-10-02 …)*)" (`Action-Dispatch/battle-action-handler-table.md:744`) |
| B4 | writers of `+0x714` | CLOSED | the pages agree on three battle-unit writers plus eight other bodies. "~~Four~~ Nine other `[reg+0x714]` writes, in eight bodies" (`Action-Dispatch/battle-action-handler-table.md:458-459`); "**at least eleven bodies** … the other ~~five~~ eight" (`CONTRACT-native-command-seam.md:121-122`) |
| B5 | sites at `+0x6B8` | CLOSED | "`+0x6B8` has ~~65~~ 64 sites image-wide" (`how-a-combo-continues-and-what-it-blocks.md:460`) |
| B6 | functions addressing the slot array: seven, eight or nine | OPEN | unchanged: "the seven functions that address the array" (`Command-And-Action-Seam/native-command-seam.md:513`); "The eight functions that reference the slot array" (`:515`); "in any of the nine functions" (`:523`). Which count is right (STATIC) |
| B7 | result-record census header: 52 offsets against 53 rows | OPEN | unchanged: "245 accesses in 39 functions over 52 offsets" (`Result-Record/the-result-record-field-map.md:14`), "52 offsets with a …" (`:31`), "reads 30 of the 52 offsets" (`:49`). The header figures do not include the `+0x010` row added 2026-09-27 (DOC) |
| B8 | the `+0x0C` bit-reader file: 23, 25 or 60 | NARROWED | the file's first comment now reads "# SUPERSEDED as a census 2026-09-27 (FABLE …): these are 23 of the 60 provenance-verified reads" (`Action-Definition-Row/members/action-row-0x0C-bit-readers.tsv:1`). Still missing: the file has 25 data rows against "23", and `Action-Definition-Row/the-action-definition-row.md:198` still opens on "23 provenance-verified reads" (DOC) |
| B9 | callers of `IssueCommand` | OPEN | sharpened since pass 1. The contract now gives "two callers only … (three call sites: `00311B20` at `00311C7B` and `00311CA6`, `003138D0` at `0031395D`)" (`CONTRACT-native-command-seam.md:66`). The post-result page still says "The issuer's other caller, `00311CD0` (five call sites), always passes slot 0" (`Post-Result-Events/…:475`). Still missing: how `00311CD0` (26 B, `Command-And-Action-Seam/native-command-seam.md:47`) reaches `00311CF0` (STATIC) |

**C. Stale "not read / open" claims**

| id | claim (pass 1) | verdict | evidence now |
|---|---|---|---|
| C1 | the README's "Not yet documented" list | CLOSED | each entry is struck with a pointer (`README.md:57-61`) |
| C2 | the availability scope note | CLOSED | "*(answered: the table was completed the same day - nineteen codes from every leg, section 10, AI-4; 2026-10-02, OPUS)*" (`Action-Availability/battle-command-availability-and-reason-codes.md:398`) |
| C3 | "AI-1 remains fully open" | CLOSED | "*(answered: AI-1, 2026-09-02 - the codes never reach a screen, §7 and §11; 2026-10-02, OPUS)*" (`Action-Availability/…:521`) |
| C4 | the per-unit pool | CLOSED | "~~with a per-unit fallback~~ checked together with the gil cost already reserved for the action in progress at `unit[0xE58]`" (`Action-Availability/…:502`; also `:505`) |
| C5 | a dated section that predates the program | CLOSED | "## SWE2-EC7-19 update (~~2026-05-15~~ 2026-09-18 …)" (`Action-Availability/…:639`) |
| C6 | when targets are gathered | CLOSED | "*(answered: after the charge - phase 4 … runs the charge progress step and phase 9 runs `Battle_BuildActionTargetSet` …)*" (`how-an-action-gathers-its-targets.md:145`) |
| C7 | is the commit executed? | CLOSED | "~~, which is unexecuted~~ *(answered: the commit is executed as shipped bytes under Unicorn, 1309 commands, 704 compared lines, 0 mismatches …)*" (`CONTRACT-the-moment-an-action-is-committed.md:159`) |
| C8 | the second shadow's readers | CLOSED | "its reader is the next commit, `0030F84E cmp di, word ptr [rbx + 0x744]` and `0030F857 cmp ebp, dword ptr [rbx + 0x740]`" (`CONTRACT-the-moment-an-action-is-committed.md:178`) |
| C9 | does the commit raise an event? | CLOSED | "does not read a script … or touch a resource; it does notify *(corrected 2026-10-02, OPUS: on a mask change `0030F975 call 00313B30` …)*" (`CONTRACT-commit-action.md:191`) |
| C10 | the commit page's "not claimed" list | CLOSED | all three are annotated as answered (`the-moment-an-action-is-committed.md:313`, `:317`, `:321`) |
| C11 | what carries the command into the funnel | CLOSED | "*(answered: `BattleUnit_SelectAndCommitNextAction` commits the issued command, `+0xBA0` id and `+0xBB8` handle, at `00305AE4`–`00305B2F` …)*" (`CONTRACT-native-command-seam.md:75`) |
| C12 | does the seam call the commit? | CLOSED | "the seam does not reach the commit; 00311CF0 records +0xBA0 / +0xBB8 only" (`Command-And-Action-Seam/native-command-seam.md:154`) |
| C13 | slot bytes `+0x1E`–`+0x1F` | CLOSED | annotated as padding at `Command-And-Action-Seam/native-command-seam.md:523` and `:540` |
| C14 | the handler-table contract's open items | CLOSED | "~~Why 18 slots are empty …~~ *(answered: AT-2, closed 2026-09-12 …)*" and "answered in part" (`CONTRACT-battle-action-handler-table.md:163-165`) |
| C15 | naming the action ids (AT-5, AT-9) | CLOSED | "*(answered: each id is named through its row's `+0x34` into bank 0 of the battle text …)*" (`Action-Dispatch/battle-action-handler-table.md:559`); "*(answered: AT-9 ANSWERED 2026-09-11 …)*" (`:563`) |
| C16 | the handler page's "not claimed" list | CLOSED | `Action-Dispatch/battle-action-handler-table.md:668`, `:671`, `:673` |
| C17 | the combo contract's stale items | CLOSED | `CONTRACT-combo-continuation.md:30`, `:142`, `:153` ("~~authored data~~ runtime state the roll writes"), `:192-194` |
| C18 | the action row's layout block | CLOSED | `+0x1E`, `+0x22` and `+0x28` are annotated (`Action-Definition-Row/the-action-definition-row.md:136-139`); "26 ~~Esper attacks~~ Quickening-family rows" (`:267`) |
| C19 | the result record's stale lines | CLOSED | "exactly 0x148 B, a stack local at every call site" (`Result-Record/the-result-record-field-map.md:158`; `:196`); `+0x08` is the gil amount (`:162`); `+0x38` is the poach reward item (`:172`); "*(answered for `0038F6F0`: step slot 163 …)*" (`:203`) |
| C20 | the status-layer modes | CLOSED | "*(answered: mode 2 sets and mode 0 clears the mutable layer `+0x68`, step 14 above …)*" (`applying-a-result-to-a-target.md:196`) |
| C21 | the target-buffer contract's stale items | CLOSED | `CONTRACT-battle-target-buffer.md:281` (the bit-8 writer), `:142` (the script verb), `:415` (bit 9 counter, bit 11 ranged critical) |
| C22 | FL-2's checkbox | CLOSED | the checkbox now reads SUPERSEDED (`Post-Result-Events/…:431`), and "~~**The row stays open**~~ *(answered: the register row closed SUPERSEDED 2026-09-26, the live read carried by ASTRA-QUEUE AQ-16 …)*" (`:437`). The two "still owed" lines (`:316`, `:541`) now name the live half only, which matches SUPERSEDED |

**D. Status banners**

| id | item (pass 1) | verdict | evidence now / still missing (class) |
|---|---|---|---|
| D1 | the README's statuses disagree with the pages | CLOSED | `README.md:19`, `:23`, `:30`, `:36`, each "*(corrected 2026-10-02, OPUS: the page's front matter says …)*" |
| D2 | the README lists six of eleven pages and no contracts | CLOSED | "*(2026-10-02, OPUS: the twelve pages below were missing from this list …)*" (`README.md:40`), followed by the list at `:42-53` |
| D3 | the availability banner and body disagree | CLOSED | "~~**PARTIAL.**~~ **AUDITED.** *(corrected 2026-10-02, OPUS …)*" (`Action-Availability/…:32`) |
| D4 | "Pending first review" after the review | OPEN | unchanged: "… action state machine does around the call. Pending first review" (`how-an-action-gathers-its-targets.md:23`); "… pending first review  promoted: 2026-10-01 DOCUMENTED -> AUDITED" (`how-close-a-unit-must-stand-to-act.md:24`) (DOC) |
| D5 | review flags | OPEN | `crossref_clean: false` remains on six contracts and the combo page (`CONTRACT-commit-action.md:21`, `CONTRACT-the-moment-an-action-is-committed.md:23`, `CONTRACT-native-command-seam.md:23`, `CONTRACT-battle-action-handler-table.md:23`, `CONTRACT-combo-continuation.md:23`, `CONTRACT-battle-target-buffer.md:21`, `how-a-combo-continues-and-what-it-blocks.md:25`). Peer review is still pending on the applier pair (`applying-a-result-to-a-target.md:26`; `CONTRACT-apply-result-to-target.md:13`) (DOC) |
