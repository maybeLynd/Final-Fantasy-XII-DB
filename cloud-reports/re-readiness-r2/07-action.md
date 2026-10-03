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
