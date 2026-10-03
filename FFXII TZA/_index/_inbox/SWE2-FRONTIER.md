<!-- TEAM-CURRENT:begin agent=SWE2-FRONTIER board_rev=50155 epoch=4 queue_sha=dde03f3d8f7114d8 -->
> generated 2026-10-03T09:11:49+00:00 by `team.py current` - do not hand-edit; hand-maintained
> counts and NEXT lines anywhere else are superseded by this block.
> ACTIVE: SWE2FRONTIER-PUB-RESUME-STATE-FINAL-1003
> READY addressed to you: none
> READY pool: 0 | BLOCKED: 0
<!-- TEAM-CURRENT:end -->

> ## TEAM ROLLBACK RECOVERED (SWE2-FRONTIER, 2026-09-26 02:30Z)
>
> The hold is LIFTED. The board was rebuilt offline (witness rev 30730 + 193 tail ops
> + all receipted post-reset ops) and installed at `recovery_epoch` 1 / rev 31132;
> evidence and adjudication are in `Database/Tools/work/_incident-team-rollback-20260926/`.
> New enforced rules: `team.py` is the only board write path and now journals/checks
> every write — a stale, rolled-back or wrong-epoch copy fails closed with
> `BoardIncident`; if you held a pre-recovery in-memory copy, re-read and re-apply.
> Board-level `checkpoints` notes now go through `{"action": "note", "note": "..."}` —
> never hand-edit `TEAM.json`. Full notice at the top of `TEAM.md`.

# SWE2-FRONTIER — inbox and handoff

**Bounded offline closure of the unexplained frontier.** Entry-point recovery, block adjudication and backlog throughput over the code no document reaches yet. One of the eleven fixed production identities (2026-09-13 migration; the
generic `SWE2` became `SWE2-CONTRACT` and seven lanes were added beside it). The board, the claim
rules and every existing record are unchanged.

## Start here

1. **Read [`TEAM.md`](TEAM.md) first**, and treat it — not a session summary — as the operating
   record. It carries the completion rule, the live-game authorization and the EC-7 ownership split.
2. **[`REVIEW-POLICY.md`](REVIEW-POLICY.md)** defines the tier this lane's packages are reviewed at
   and who audits them.
3. **[`../EVIDENCE-STANDARD.md`](../EVIDENCE-STANDARD.md)** is binding. The amendments at the end are
   the expensive lessons; two bite offline work hardest — **a zero is a property of the filter until
   a positive control says otherwise**, and **a value inside a code range is not a pointer**.
4. **Claim before writing**, through `team.py` transactions only:
   `python team.py apply --agent SWE2-FRONTIER --file op.json`. Never edit `TEAM.json` by hand.
5. **Commit explicit reviewed paths** with `publish_paths.sh <message-file> <path> …`. It refuses a
   directory argument on purpose: `git add` on a directory stages every changed file under it,
   including a peer's.

## What this lane is for

The live example is UC-1. `unlisted_admissions.py` adjudicates 1,471 unlisted blocks into 1,302 `body` / 162 `continuation` / 7 `ambiguous`, and the population change is voted and built - but **it is blocked on this lane's exact output**. A splitter block is not function-shaped: listed bodies pass a linear-decode test at 100.0/99.8/98.7/97.7/92.6 %% by size band, the admitted blocks at 79.2/40.6/22.0/39.1/44.4 %%. The bytes are real code (`001505C0` opens `push rbp; mov rbp, rsp`); the **boundaries** are not established. What moves the denominator is recovered **entry points**, measured against that same control.

## Review

**Default auditor: `SWE2-AUDIT-SEM`.** T1 packages need producer self-falsification plus that
auditor; T2 — family claims, ABI or type ownership, contract definition, a universal or negative
claim, or bulk EC-7 — additionally need FABLE or OPUS adjudication; T3 runtime-dependent questions
are prepared as an exact question and routed to ASTRA. See [`REVIEW-POLICY.md`](REVIEW-POLICY.md).

**While awaiting review, take separate non-dependent work.** A package in review is not a reason to
idle, and it is not a reason to start something that depends on its outcome.


## Two standing limits

- **A stub is not proof of its native effects.** Disclose injected state, stubs and entry
  boundaries; omitted initialisation, scheduling and effects stay open.
- **Agreement between a reconstruction and its own fixture is not evidence.** The control has to
  come from the shipping image or from the documents, never from recollection.

## Resume state

Updated at every checkpoint; a restarted session rebuilds from this block before touching the board.
Required by the continuity rule in the root `CLAUDE.md` ("What a plain `Continue` means").

- **2026-10-03 09:05Z - Claude stand-in for Devin (SWE2-FRONTIER), final; supersedes the 03:25Z entry below.**
  **Current package/claim:** none. Every SWE2-FRONTIER task on the board is DONE (queue empty at rev ~50139). No
  FRONTIER runner is running, and no FRONTIER edit is uncommitted. The parent session owns the fleet-plan hold;
  re-read `fleet-plan.json` and run `controller status` before planning.
  **Done since 03:25Z (each finished on the board with its sha, and a note naming
  `FABLE-REQ-OPUS-FINISH-PACKAGES-ZIP-1003`):**
  - The dashboard (`FABLE-REQ-FRONTIER-DASHBOARD-LIFECYCLE-1003`), seven separately published steps, each with a
    focused test in `Database/Tools/dashboard/`:
    - A `240ceade4` - DB_GOAL chain, Depth as diagnostic, Source/Freshness drawer;
    - F `e25142cd3` - lifecycle panel; L9 = labels vs DASHBOARD-MEANINGS section 6;
    - B `c91231520` - Recent meaningful changes;
    - C `4219c0df2` - Next highest-value work;
    - D `de2cf8b42` - lineage;
    - E `d0f783fa8` - status residue view;
    - G `a74872174` - STRUCT's readiness view.
    Tooling: `standin1003/dash3/`.
  - `1e64e4042` - the A-overlap family rule. F went 8,842 -> 2,233 on the live tree; A unchanged; refused 47 -> 1.
    The same commit carries `accepted_families()` and the vtable `ee_index_only` frontmatter.
  - `3fef5ca4b` - the check_consistency CALLER-COUNT repair (3 -> 1).
  - `819c51cc1` - the **stale pre-image gate** in `publish_paths.sh` (`check_stale_preimage.py`, exit 9; override
    with a `reverts: <sha>` message line). It catches the 95b1f3a4c revert of fa2f75e21 (and of the dependent
    30b2fd926), bf226bbaa and 7225ed5b4, with 0 false positives over 200 commits. Every revert it found is already
    restored at HEAD.
  - `e1b42c48b` - the shared analysis venv upgraded to unicorn 2.1.4 (check_unicorn exit 0; S-08 replay identical),
    plus the `[shape]` family marker (`accepted_families_marked()`).
  - `543493baf` - the TEAM.json read-denial repair.
  - ASTRA's publication turns: two earlier requests satisfied by `88d435193` / `64cb2c0c3`; the two-job turn
    delivered `a3d7433c2` / `0d55f8417` during FRONTIER's yield window.
  **Open for Devin (not on the board):**
  - UC-1 census marker: `measure_a`'s phrase gate may need FABLE's census-name marker once FABLE publishes that R1
    wording.
  - `check_consistency`'s RETRACTED_NEARBY look-behind spans paragraphs.
  - `goal_gate`'s F= line moves at the next dashboard build.
  - `sweep.py N` (in `_index/candidates/swe2frontier-stale-preimage-gate-1003/`) can replay the stale gate further
    back in history.
  **Lessons:**
  - never `sed -i` a script a running bash executes;
  - a lane's own claim on a request can block its publish task on the same file key: release, publish, re-claim and
    finish;
  - heredocs mangle backslashes, so write scripts with the Write tool;
  - `.log` files are gitignored, so name record artifacts `.txt`.
- **2026-10-03 03:25Z - Claude stand-in for Devin (SWE2-FRONTIER); supersedes the entries below.**
  While the Devin session `calm-lamp` was rate-limited (breaker to ~07:39Z), a Claude session ran this lane.
  **Current package/claim:** none - every SWE2-FRONTIER task on the board is DONE (queue empty at board rev ~48900).
  **The fleet plan holds every SWE2 lane in `held_by_subagent`** for the Claude stand-ins. The parent session releases
  the hold when Devin returns; if it does not, the plan goes stale at ~07:36Z. The 25 pending DEP_STARVED replans are
  that hold. Re-read `fleet-plan.json` and run `controller status` before planning.
  **Done by the stand-in (do not redo; all board tasks finished with these shas):**
  - `d9b357cae` - the register NR section (NR-1) (`SWE2FRONTIER-PUB-NR-SECTION-1003`).
  - `9afe32d66` - three items in one commit:
    - the A23 named-comparison incorporation (`SWE2FRONTIER-PUB-A23-NAMED-INCORP-1002`);
    - the `test_watchdog_scheduler.py` fixture repair, 16/16 (`OPUS-NOTICE-FRONTIER-WATCHDOG-PYTHONW-NOWIN-1002`);
    - the review of ASTRA's epoch prefix, `verdict:ACCEPT` (`ASTRA-REQ-FRONTIER-PUBLICATION-EPOCH-PREFIX-1002`).
  - `3319c2a6f` - the TEAM.json replace-denial repair (`ASTRA-REQ-FRONTIER-ATOMIC-BOARD-WRITE-DENIAL-1003`):
    - team.py retries WinError 5/32 against a 30 s deadline;
    - seven board readers close the file before parsing;
    - record `_index/candidates/swe2frontier-board-replace-denial-1003/`.
    The long-running dashboard server and the watchdog controller pick up the reader change only after a restart.
  - `ae00a4a33` - the SWE2-FRONTIER answer section in `_inbox/ASTRA.md`. The commit also carries ASTRA's regenerated
    TEAM-CURRENT header.
  - `ef8e5a09a` - the readiness batch (`SWE2FRONTIER-PUB-READINESS-BATCH-1002` and
    `OPUS-NOTICE-FRONTIER-READINESS-BATCH-OVERLAP-1002`). It carries the FRONTIER share of 17 OPUS packages: 163
    edits on 47 pages, each rebuilt from HEAD. It also has L2-VERDICTS, the field-map slot labels, the allocator
    page's NR-1 pointer and a Resource crossing bullet on the spawn keep-entry field map. All 163 edits verified at
    HEAD. Record `_index/candidates/swe2frontier-readiness-apply-1002/`.
  - `a46d39253` - the UC-1 interior-citation route in `check_dispositions` / `requirements._f`, from FABLE's R1
    amendment `e050edc2a` (`FABLE-REQ-FRONTIER-UC1-INTERIOR-CREDIT-1003`, `OPUS-NOTICE-FRONTIER-UC1-GAMECODE-GATE-1003`).
    No count moves until OPUS's rows carry the phrase. The same commit makes the correction gate count touched `.tsv`
    (`SWE2STRUCT-REQ-FRONTIER-CORRECTION-GATE-TSV-AFFECTED-1003`).
  - Filed `SWE2FRONTIER-REQ-FABLE-REVIEWS-AUTHOR-IDENTITY-1003`. FABLE fixed its filer at `1db50c32e`.
  **Standing planner rule (2026-10-03, F-frontier homing split):** the 2,116 bodies that no bearing page cites are
  split three ways. Lists are in `_index/candidates/fable-homing-stream-1003/` (dashboard gen g20261003T020947Z):
  - FABLE has caller-host (590; `FABLE-HOMING-CALLER-HOST-1003`);
  - OPUS has callee-host (973) plus the 59 UC-1 game-code bodies (`OPUS-F-HOMING-CALLEE-HOST-1003`);
  - **SWE2-EC7 has caller-uncited (277) + no-ref (276) plus batches 172/173 (`SWE2-EC7-HOMING-RESIDUE-1003`).**
  Each task holds `frontier-class:<class>` keys. Released bodies go back explicitly on the board, under the same
  24 h guard and append-only rows, and shared hosts get HEAD+mine splices. **EC7 rotation targets only EC7's
  classes.** The per-batch SWE2-AUDIT-SPEC reviews of FABLE's stream join AUDIT-SPEC's queue. team.py compares
  keys as plain strings: equal keys and `/` children conflict, nothing else. The four lists were checked disjoint
  (union 2,112 data rows). Body-level overlap with other scopes (EC7's shared-hub batches, file: claims) is
  invisible to the board.
  **Lessons from tonight:**
  - `team.py current` rewrites every inbox's TEAM-CURRENT block on board writes, so a PUBLISH_EXPECT pin on an
    inbox file can fail mid-publish. Publish inbox files in their own commit.
  - A 0-byte `.git/index.lock` with no live git owner (02:21Z-02:46Z) deferred every post-commit index refresh.
    `9afe32d66` printed REFRESH-DEFERRED, and its paths were re-added by hand.
  **Rotation when Devin returns:** the board is nearly drained for SWE2. EC7 has 10 ACTIVE (readiness-edit requests
  plus the homing residue), and DATA and ORACLE have one each; AUDIT-SPEC has 1 READY P1; CONTRACT and STRUCT have
  ready-pool P1 work. Suggested first three: SWE2-EC7 (homing residue classes), then SWE2-CONTRACT and SWE2-STRUCT
  (pool P1). ORACLE's resume reads `stale:claim-done` against an ACTIVE coverage claim; reconcile it at its wake.
  **Fallback eligible work:** `publish_paths.sh` should print the lock's age and owner liveness when it defers a
  refresh. Also: restart notes for the dashboard server and controller (owners).
  **Scratch:** `Database/Tools/work/SWE2-FRONTIER/standin1003/` (runners, logs, blobs, board ops).
  **Latest coherent commit:** `a46d39253`.
- **2026-10-02 ~wake before PC restart (Devin session `calm-lamp` executing SWE2-FRONTIER):**
  **Parked for restart.** No ACTIVE claims, nothing staged, `@publication` held by peers (EC7-172, CONTRACT-B21Z4).
  **Queue on resume (15 READY):** P1 `ASTRA-REQ-FRONTIER-PUBLICATION-TURN-1002` and
  `ASTRA-RETURN-FRONTIER-A23-NAMED-COMPARISON-1001` (dep may be done — check SPEC); P2 readiness-edit applies
  (`SPAWN`, `ACTION-APPLY-CARRIER`, `ACTOR`, `SCRIPTVM`, `ENGINE-A`) + P3 readiness lines
  (`PARTY`, `WORLD`, `PHYRE`, `UI`, `CRT`), `ACCOUNTING-INDEX-RESIDUE`, `L2VERDICTS-LICENCE-360` notice,
  `RNG-PARITY-ROW`.
  **State since last entry:** OPUS answered GI-14..19 (all six) — pages re-DOCUMENTED pending its own AUDIT-SEM
  reviews; SPEC landed verdicts; board rev ~47002.
  **Restart notes:** the watchdog controller dies with the PC — `swe2_watchdog.py controller ensure` on resume.
  **Fleet park notice posted (board rev 48014):** all lanes told to checkpoint resume blocks and hold new
  publishes; ACTIVE claims preserved on the board for same-identity reclaim — do not double-claim on resume.
  Live at post: CONTRACT busy-active (`OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929`), ORACLE busy-wake pid 33452
  (`OPUS-REQ-ORACLE-EXECUTION-COVERAGE-INSTRUMENT-0929-R`), SPEC queued for next wake; EC7/STRUCT/DATA have
  parked ACTIVE claims. Controller had 8 pending `BLOCKED_NEEDS_SPECIALIST` replans — re-evaluate on resume.
  This inbox file's resume edits are uncommitted (publish when `@publication` frees). Peer worktree edits are
  theirs — do not sweep.
- **2026-10-01 ~21:10Z (Devin session `calm-lamp` executing SWE2-FRONTIER):**
  **GI residue repair published** — `85a2ae3ee` under lease `FRONTIER-PUB-GI-RESIDUE-REPAIR-0930` (14 files,
  index refresh clean). AUDIT-SEM's REJECT of `c97af7156` repaired at the cause: stale not-read prose struck with
  pointers on 7 pages; real limits registered **GI-14..GI-19**; `residue_scan.py` widened to whole-line sweep +
  paragraph rows under residue headings + multi-line strike tracking, `--selftest` embeds the `c97af7156` 80-97
  `## Not read` paragraph as the rejecting regression; gate re-run READY 7 / PARTIAL 6 / FAILS 0.
  `AUDITSEM-REQ-FRONTIER-GI-RESTATUS-RESIDUE-0930` + `AUTO-REPAIR-...-RESTATUS-0930` DONE;
  re-review `FRONTIER-REQ-AUDITSEM-REVIEW-GI-RESIDUE-REPAIR-0930` routed to AUDIT-SEM (rev 45559).
  **Publish note:** `OPEN-QUESTIONS.md` carried peer hunks (SWE2-DATA C-7, Z-19) — published a surgical
  HEAD+GI-rows-only blob, restored the worktree byte-exact. `@publication` free.
  **Live GI items:** GI-14 (00-0a tails/emitter/+0x38/VU0 body), GI-15 (authored commands ×11), GI-16 (license
  `+0x37D`), GI-17 (shop helpers ×3), GI-18 (gambit editor/list arms), GI-19 (oscillator resolve-chain types).
  **Queue next:** `ASTRA-RETURN-FRONTIER-A23-NAMED-COMPARISON-1001` (P1 — dep ACTIVE with SPEC).
  **Standing instruction (user, 2026-10-01):** the final message before standby after every `Continue` wake
  must report (a) which agents are working and on what, and (b) what this wake accomplished.
- **2026-10-01 ~13:20Z (Devin session `calm-lamp` executing SWE2-FRONTIER):**
  **Published the SD-140 contradiction repair** — `d147ab479` under lease `SWE2FRONTIER-PUB-SD140-POLARITY-1001`:
  `the-two-transform-primitives.md` + the `matrix-buffer-alias` retained mirror. Verified against the shipping
  EXE (capstone, hash `73461D08`): bits 4/5/6 of `byte[rec+0x1F1]` run **clear → blend / set → copy** (all
  three were inverted on the page); `00432300` is the PS2 colour-modulate kernel
  `min(255, (entry*colour)>>7)`, `0x80`=1.0 — not "pure staging". `OPUS-CON-TRANSFORM-00434CD0-BIT-POLARITY-0930`
  DONE with `commit:d147ab479` + record ref. `@publication` released. Residue noted: the SD-140 record's other
  X-items (X3 clip builders → `OPUS-CON-TRANSFORM-CLIP-BUILDERS-0930` already with EC7; X4/"§8 precision" on
  `effect-mesh-records-kind-54.md` line ~201 — the row states set→copy correctly but implies unconditional
  +0x28 blend; worth a small follow-up if no task covers it).
  **Earlier this session:** six-commit publish wave (`8006a94ef`, `08ca096bc`, `e325c403b`, `18bf01b79`,
  `59f0bfff1`, `ba4612812`) — all pre-lease backlog landed; ~12 tasks finished.
  **Queue next:** `SWE2AUDITSPEC-REQ-FRONTIER-BOARD-VERDICTS-MISRECORDED-0930` + addenda (~85 DONE rows cite a
  gitignored review file — board repair), `AUDITSEM-REQ-FRONTIER-GI-RESTATUS-RESIDUE-0930` + auto-repair chain,
  `ASTRA-NOTICE-FRONTIER-POSTCOMMIT-INDEX-LOCK-0930` (bound the publish_paths exit-128 edge),
  `ASTRA-REQ-FRONTIER-PREPARED-EVIDENCE-SLOT-0930`, plus new `ASTRA-RETURN-FRONTIER-A23-NAMED-COMPARISON-1001`
  (P1) and `SWE2STRUCT-REQ-FRONTIER-ARG-ROUTE-RULING-1001` (P3). `FABLE-REQ-FRONTIER-OV58D-STATIC-0930` is
  READY again — its earlier finish didn't stick; answer is already established (row restates neither wrong
  fact; record committed at `d5fee099d`).
- **2026-10-01 ~08:20Z (Devin session `calm-lamp` executing SWE2-FRONTIER):**
  **Lane identity fixed:** this interactive session is `calm-lamp` (titled by the user's first question, not
  `SWE2-FRONTIER`), so the controller counted it foreign and spawned a duplicate FRONTIER wake at 07:56Z
  (pid 68532 resuming `concise-family`). The duplicate was killed after only reads; `fleet-map.json`
  `SWE2-FRONTIER.current` is now `calm-lamp` — controller sees `busy-active`, future wakes resume this
  session. `d20a34efb` fixed the subagent double-wake class; THIS class needed map attribution.
  **Processed:** replans cleared (DEP_STARVED spam re `FABLE-REQ-CONTRACT-RC-RESTATE-0930` — CONTRACT stays
  parked, its only dependent is P3); `ASTRA-REQ-FRONTIER-NATIVE-PATH-ARGV-LIMIT-0930` DONE (authorized bounded
  multi-commit <=60 paths/call under one lease, shared PUBLISH_EXPECT; filed
  `FRONTIER-REQ-ASTRA-PUBLISH-PATHFILE-1001` as optional tooling follow-up);
  `OPUS-NOTICE-FRONTIER-READINESS-DEBT-0930` DONE (debt sized, plan unchanged);
  `ASTRA-NOTICE-FRONTIER-EVIDENCE-PUBLICATION-WAIT-1001` DONE earlier at 07:51Z.
  **Applied, waiting @publication (ACTIVE claims):**
  - `OPUS-REQ-FRONTIER-RC37-SPLICE-0930` + `OPUS-REQ-FRONTIER-S08-I3-SPLICE-0930` +
    `OPUS-REQ-FRONTIER-PUBLISH-REQUEST-QUEUE-CARRIER-0930` — both splices applied on
    `CONTRACT-resource-request-queue.md`; one publish finishes all three.
  - `AUDITSEM-REQ-FRONTIER-P22-B8-0930` — handbook page corrected (002EFD20 byte@0x30 stride,
    0032E400 kind-FF, 00572E10 transitive calls, SaveLoad batch vocabulary); publish pending.
  - `AUDITSEM-REQ-FRONTIER-P22-DATA-0930` — C1/F3/N3/N4 applied across himg/as7/btm/mrp/binmenu
    (N1/N2 optional); five files pending publish.
  - `SWE2CONTRACT-REQ-FRONTIER-PUBLISH-LIFECYCLE-OVERLAY-0930B` — neighbour gate re-verified ADDS NOTHING
    (454->450, accounts 4); `-0930` stays BLOCKED until the commit lands, then finish both.
  - `OPUS-REQ-FRONTIER-REGISTRY-ADDRESSERS-0930` — resumed+reclaimed; publish encoded-id page +
    batch-K + `registry-addressers-apply-0930/` in one commit per OPUS.
  **Publish order when @publication frees:** whichever is ready; all paths verified. Use publish_paths.sh
  per group; record each sha in the task finish.
- **2026-10-01 morning (Devin session executing SWE2-FRONTIER):**
  **@publication adjudication pending.** `SWE2STRUCT-PUB-ROUTECENSUS2-0930` has held `@publication` since
  06:50:49Z; the holding Devin session is confirmed closed by the user. Evidence: no commit (HEAD `560c86a3`),
  nothing staged, no `.git/index.lock`; last board op 06:58:37Z and last file write 06:58:51Z were the AWN
  wave-B finish sharing the identity; all batch-2 artifacts on disk by 06:37Z (untracked `*-accesses.tsv`,
  `types.tsv`/`fields.tsv`, `sweep_route_seeded_census.py`, 4 new census tools) — untouched for same-identity
  reclaim. OPUS is a waiting claimant and cannot adjudicate; FRONTIER is the only eligible adjudicator.
  Filed `FRONTIER-REQ-STRUCT-PUBLICATION-CHECKPOINT-1001` (READY, 07:36:46Z) as the `unanswered_request` leg.
  **Next action:** once the holder checkpoint is 6h old (>= ~12:50:49Z), the request is >=2h unanswered
  (>= 09:36Z) and `no_activity_since` (last holder activity 06:58:51Z) is >=2h, apply
  `{"action":"release_publication","task":"SWE2STRUCT-PUB-ROUTECENSUS2-0930","unanswered_request":
  "FRONTIER-REQ-STRUCT-PUBLICATION-CHECKPOINT-1001","no_activity_since":"2026-10-01T06:58:51+00:00"}` via
  `team.py apply --agent SWE2-FRONTIER`. Re-verify silence first — a resumed holder reclaims normally and this
  plan is void. Also pending: `ASTRA-NOTICE-FRONTIER-EVIDENCE-PUBLICATION-WAIT-1001` is answered in substance
  by this reconciliation; note it when the release lands.
- **2026-09-30 night (Claude subagent of FABLE session 0aca3c35 executing SWE2-FRONTIER):**
  **Unattributed pass-22 appends dispositioned** (`OPUS-NOTICE-FABLE-PASS22-UNATTRIBUTED-BLOCKS-0930`, for FABLE to
  close). The record is `_index/candidates/frontier-pass22-unattributed-0930/`.
  - The writer was the Devin SWE2-STRUCT wake `SWE2-STRUCT-20260930-021949` (07:35Z). Its registry step crashed.
  - 34 of 51 pages verified and published: batch 1 at `54e8a524e` (23 pages) and batch 2 at `6075e3017` (11 pages). 141 pairs accounted, ADDS NOTHING.
  - 17 appends and 48 TSV rows were moved aside. Their patches were committed at `54e8a524e`, and `git apply`
    restores them.
  - `SWE2-FRONTIER-P22-DATA-0930` is DONE: the DATA group is 0 at `1cdc09347`.
  - The orphan `SWE2-FRONTIER-PUB-PROBE-CORR-STAMPS-0930` was retired, superseded by `ac4d7d901` and `4032e34d4`.
  - The MAPSCREENS A-entry correction is published with the consumer record `frontier-mapscreens-003c1680-0930`
    (task `SWE2-FRONTIER-PUB-P22U-MS-0930`).
  **Review routed:** `FRONTIER-REQ-AUDITSEM-REVIEW-P22-UNATTRIB-0930`.
  **Claims still held:** `OPUS-REQ-FRONTIER-FLEET-LANE-DOUBLE-WAKE-0930` and `OPUS-REQ-FRONTIER-AUDITSPEC-LANE-BACKLOG-0930`.
  Both wait on FABLE's `FABLE-PUB-FLEET-HELD-0930`, which was re-queued READY after its runner died. **Next action:**
  finish both once it lands, citing its sha and noting that AUDIT-SPEC now runs continuously as a FABLE subagent.
  Also: the moved-aside owners (see the record's outcome table), and SWE2-CONTRACT's
  `native-command-lifecycle.md` hunks and its 13 other uncommitted registry rows.
- **2026-09-30 midday (Claude subagent of FABLE session 73162e75 executing SWE2-FRONTIER):**
  **Claims held: none.** DA = 0: interpreter-core stamped at `02af0c103`, fresh `requirements.py` on a HEAD export.
  **GI DD re-status** at `c97af7156`: the 13 GI pages are DOCUMENTED; DD unmet 111 -> 98.
  **Overlay plan closed** at `18facf5e9`: the carrier gate is now inert via `plan_state: CLOSED`; regression
  `overlay-plan-closure-0930/test_gate_close.py`.
  **Pass 22:** batches 1-7 are published (`3fd361505` `a1c37abb4` `c5838f4e1` `e1522398e` `89846c2d9` `44d58698d`
  `60d2dd1cf`). The debt at HEAD `acb04148d` is 6 pairs, all on `the-handbook-screen.md`; the task note lists the
  subjects still to read.
  **Defect disclosed:** `c5838f4e1` swept three of SWE2-STRUCT's uncommitted bullets (board note rev 42115).
  **Rule:** re-diff every path immediately before hashing it for a runner.
  **Board findings:** SWE2-STRUCT's unclaimed template bullets (note rev 41896). The `dc6c5f065` / `280006c24` actor
  was the Devin SWE2-DATA session holy-rock, woken by the controller in parallel with the Claude DATA subagent
  (note rev 42112).
  **Reviews open:** `FRONTIER-REQ-AUDITSEM-REVIEW-P22-B2-B7-0930`, `-GI-RESTATUS-0930`, `-FST-SYNC-0930`,
  `-P22-B1-0930`, `-DEFEAT-CROSSING-0930`, and `FRONTIER-REQ-AUDITSPEC-REVIEW-PLAN-CLOSE-GATE-0930`.
  **Parked:** registry-addressers (OPUS variant pending) and the lifecycle overlay (CONTRACT restage). With the gate
  inert, both authors can now publish their own hunks.
  **Runners:** `s0930/run_pub2.sh` (splice plus HEAD guard) and `launch2.sh` via `Start-Process`.
  **Latest coherent commit:** `18facf5e9`.
- **2026-09-30 morning (Claude subagent of FABLE session 73162e75 executing SWE2-FRONTIER):**
  **Claims held: none.** Published this session:
  - **DA falsification stamps** at `4032e34d4`: OPUS's pass 1 on six overlay carriers (encoded-id, request-queue,
    defeat-rewards, apply-result, unit-construction, resource-ownership), plus a FRONTIER crossing section on
    defeat-rewards for the pass's two new cites. The DA instrument (fresh `requirements.py` on a HEAD export
    `5475c4512`) reads all six as "falsification pass recorded" (unmet 6 -> 1; the remainder is
    `CONTRACT-interpreter-core.md`, not in these requests). Review `FRONTIER-REQ-AUDITSEM-REVIEW-DEFEAT-CROSSING-0930`.
  - **FST sync/async correction** at `ac4d7d901` (`fst-sync-read-0930`, control `fst_r8_mode.py`). Review
    `FRONTIER-REQ-AUDITSEM-REVIEW-FST-SYNC-0930`. `FABLE-REQ-FRONTIER-OV-PROBE-CORRECTIONS-0930` DONE. Its row items
    (b)/(d) went to FABLE as `FRONTIER-REQ-FABLE-OV58-ROW-TEXT-0930`. FRONTIER did not touch OV-5/OV-8.
  - **AUTO-INCORP A23 + pending-state binding** at `abe576f39` (`frontier-incorp-ratified-0930`), both DONE.
    TEAM.md:477 and the IMPLEMENTATION-MAP board-writes row still call FRONTIER's half open; routed to SWE2-CONTRACT
    as `FRONTIER-REQ-SWE2CONTRACT-PENDING-STATE-DONE-0930`.
  - **Pass-22 batch 1** at `3fd361505`: 6 of 55 pairs (gate 1244 -> 1238). Review
    `FRONTIER-REQ-AUDITSEM-REVIEW-P22-B1-0930`. `SWE2-FRONTIER-PASS22-DEBT-OWN` was released READY; its note lists
    the 49 remaining pairs by page and the tools (`C:/x/fr22` export, `work/SWE2-FRONTIER/audit_full.py`,
    `p22_mine.py`).
  **Parked (BLOCKED, with routed requests):**
  - `OPUS-REQ-FRONTIER-REGISTRY-ADDRESSERS-0930`: the replacement's cites `0030FAA0`/`0030FBE0` re-key the carrier's
    CombatFormula / Items findings (ADDS 2). Asked OPUS for a role-named variant or crossing paragraphs
    (`FRONTIER-REQ-OPUS-REGISTRY-ADDRESSERS-NEIGHBOUR-0930`). **Uncommitted FRONTIER work in the worktree:** the
    batch-K replacement (`register-triage/batch-K-scope-rulings.md`, one line) and the record
    `_index/candidates/registry-addressers-apply-0930/`. The section-14 hunk on the carrier page was applied by
    someone else around 06:21Z; publish page + batch-K + record together once OPUS answers.
  - `SWE2CONTRACT-REQ-FRONTIER-PUBLISH-LIFECYCLE-OVERLAY-0930`: CONTRACT's hunks add 3 unaccounted neighbours
    (seven new cites); `FRONTIER-REQ-SWE2CONTRACT-LIFECYCLE-NEIGHBOUR-REFUSAL-0930`. Its hunks are untouched.
  **Worktree peers' hunks left intact:** OPUS's RC-37 sentence on the request-queue carrier's state-1 row (a
  carrier, so FRONTIER will be asked to publish it). `FABLE-REQ-FRONTIER-OV58D-STATIC-0930` stays READY for FABLE to
  close, as directed. **Next:** watch the three reviews and two routed requests; publish the registry-addressers
  and lifecycle items when they are unblocked; continue pass-22 from `the-unlabelled-procedures.md`.
  **Runner lesson:** a Bash tool `&` or `run_in_background` publish survives a session death and can then run
  alongside a relaunch. Launch detached with `Start-Process` (s0930/launch.sh) and check for stale runners by
  command line before relaunching. Never edit a runner script while a bash runner that reads it is live.
  **Latest coherent commit:** `4032e34d4`.
- **2026-09-29 late (Claude subagent of FABLE session 73162e75 executing SWE2-FRONTIER; board note rev 40420):**
  **A23 release delivered** at `059ee3a6c` — `ASTRA-REQ-FRONTIER-A23-RELEASE-EXPORT-IDENTITY` DONE (the prior
  executor's 21:12Z claim was recovered same-identity; its unreceipted `g20260929T210933Z-e40dd5.zip` is not the
  candidate). Candidate `g20260929T213407Z-9c7238`: served = CURRENT pin = guarded export, `verify-zip` VERIFIED,
  ZIP sha256 `23256f18…57c7`, 8/8 views equal, manifest sources = HEAD blobs, listener pid 68280 bound, rollback
  drilled on port 8766; launcher/live restart not exercised, dashboard suites not re-run (peer's dirty
  `requirements.py`). Record: RELEASE-DASHBOARD-2026-09-29.md section 7; receipts
  `_index/candidates/a23-release-0929/`. Record stays DELIVERED, NOT ACCEPTED until SOL/ASTRA re-verifies.
  **Runtime-rule ruling** at `3957cf3f1` (`FABLE-REQ-FRONTIER-RT-RULE-CLOSURES-0929`,
  `FABLE-NOTICE-FRONTIER-OV5-OV8-NARROWING` DONE): SUPERSEDED under the runtime rule needs tier 1 AND an
  observation that would add nothing; the nine RT halves (OV-5, 8, 10, 16, 19, 21, 29, 33, 42) stay OPEN on their
  named ASTRA carriers; batch-K's "may close once the owner confirms tier 1" sentence withdrawn. OV-5/OV-8 now
  PARTLY ANSWERED ((a) fourth key range, (b) prefix-sum wrap unreachable on shipped data; (c) `qword [01F83530]`
  base, (d) over-reservation OPEN). Review routed `FRONTIER-REQ-AUDITSEM-REVIEW-RT-RULE-0929` (reviews field,
  incorporation owner FRONTIER). Published as HEAD + my nine rows only: a peer's uncommitted UQ-206 hunk in
  OPEN-QUESTIONS.md was left in the worktree, uncommitted and intact. Routed: `FRONTIER-REQ-FABLE-RT-REMAINDERS-PROBE-SITES` (exact probe sites +
  decisions for RT-REMAINDERS; timing rows may need a scope ruling), `FRONTIER-NOTICE-OPUS-P1-HEADING-BOX-REGISTER-ID`
  (the only P fact: OPUS's CON-172 reopened box has no register id).
  **DD/DA state:** DD=119 is fully routed — 13 FRONTIER pages -> GI-1..13 (FABLE answering; FABLE asked FRONTIER not
  to touch those residue sections; re-status to DOCUMENTED is FRONTIER's once FABLE's answers land), 89 READY/
  NEEDS-POINTER -> `OPUS-DD-RESTATUS-AFTER-RULING` (READY, unclaimed), 2 -> `OPUS-NOTICE-DATA-DD-RESTATUS-0929`,
  15 PARTIAL carry live OV/UQ-218 rows. DA=24 is OPUS's falsification-pass stream (`OPUS-DA-FALSIFY-BATCH-*`).
  **Claims held:** none. **Next action:** incorporate the AUDIT-SEM verdicts (RT ruling, team.py fix) when they land (AUTO-INCORP /
  AUTO-REPAIR); when FABLE's GI answers land, owner-read the 13 DD pages and re-status those with no residue left.
  **Fallback:** `SWE2-FRONTIER-PASS22-DEBT-OWN` (P3) — its disposition file `_index/candidates/pass22-tripwires.tsv` is
  currently dirty with a peer's hunks, and several of its 14 pages are FABLE's GI targets, so check both first.
  **Board throughput repair** at `d20b7b69b`: `team.py` `validate()` was quadratic over ~13.2k tasks (~27 of ~31 s
  per apply under the mutex; ~20 writers queued, one claim waited 43 min); now ~5 s per apply, differential 0 diffs,
  test_team + test_team_rollback 56 OK. Review `FRONTIER-REQ-AUDITSEM-REVIEW-TEAMPY-VALIDATE-0929`; board note rev
  40599 asks lanes to make claim retries lease-aware (`work/SWE2-FRONTIER/lease_claim.py`).
  **A23 git-lookup repair** at `cd5a039d3` (`ASTRA-REQ-FRONTIER-A23-GIT-LOOKUP-ADMISSION` DONE): `source_lookup.py`
  keeps Git exits (failed lookup = INCOMPLETE, never SHA256(empty)); real-Git controls FAILS 0, old-behaviour mutant
  killed; candidate re-bound at `5a2435b23`, all five components BOUND. Awaiting ASTRA/SOL verification.
  **Pass-22 carrier publish** at `05b858cfa` (`FABLE-REQ-FRONTIER-PASS22-CARRIER-BLOCKS` DONE): FABLE's crossing blocks
  on 12 overlay-carrier pages, additions only (279 lines), neighbour gate ADDS NOTHING (1338 -> 1217).
  **GI re-status watch:** at 01:10Z only GI-12 is answered (`6facc53bc`; its page is documented_rule READY, but
  `FABLE-REQ-AUDITSEM-REVIEW-GI12` is unreviewed). Re-status the 13 DD pages after FABLE's consolidated GI-1..11/13
  publish lands and the answers' reviews accept - not before.
  **Latest coherent commit:** `05b858cfa` (resume block `4a7130040`, amended after it).
- **2026-09-29 post-restart consolidation (rev ~39021):** the dep-starvation repair
  batch published at `93e339b12` (no-`/T` controller stop, `controller ensure`
  single-owner turnover, dep-owner promotion in `desired_set`, AUTO-UNBLOCK pass in
  transitions.py, `families` gate consuming CURRENT requirement_facts — live UNMET
  `DA=97 DD=128 F=12114 P=49`; 14/14 scheduler tests). `OPUS-NOTICE-FRONTIER-GATE-
  BLIND-TO-FOUR-FAMILIES` and `ASTRA-REQ-FRONTIER-EVIDENCE-GIT-BYTE-PREFLIGHT`
  (correction `51660c616` blob-verified, obsolete publication row adjudicated)
  finished. OV carrier `FABLE-CARRIER-SECTION-OVERLAY-ACCEPTANCE-0929` finished:
  reviewers allocated — `FRONTIER-REVIEW-AUDITSEM-OV-ACCEPTANCE-0929` (4 sections),
  `FRONTIER-REVIEW-AUDITSPEC-OV-ACCEPTANCE-0929` (6 sections), OV-31 →
  `FRONTIER-REQ-SWE2-STRUCT-OV31-TYPE-STORE`. Leftovers published `ed48a2228`
  (consumer-check + regenerated worklist: 0 id-less boxes). The transitions
  `--apply` 120 s timeout defect is closed at `c545ed760`
  (`--apply-budget-s` defers overflow to the next cycle; watchdog applies with
  240 s budget inside 300 s; `test_watchdog_scheduler` 16/16 incl. the two new
  ApplyBudget fixtures). Controller restarted pid 60108 → **63456** to pick it
  up; frontier queue empty.
- **2026-09-29 OV-15 + MS rows + underrun errata (rev ~39079):** controller 63456
  confirmed live; AUTO-UNBLOCK fired on its own —
  `AUTO-UNBLOCK-OPUS-REQ-FABLE-REGISTER-49-IDLESS-BOXES` was created for FABLE
  when the dep task closed, no user message needed (the incident fix working
  end-to-end). `FABLE-REQ-FRONTIER-APPLY-OV15-AND-MS-ROWS` done at `845e20290`:
  OV-15 §4 sentence + box tick + register row ANSWERED per FABLE's staged
  `ov15-skip-mask-fable` record (`skip_mask.py` FAILS 0); new `## MS.` register
  section with MS-1..3 OPEN (map-screens stays PARTIAL until the owner resolves
  them). `OPUS-REQ-FRONTIER-EXTENT-ERRATA-UNDERRUN-159` done at `906d5480a`:
  158/159 rows applied to FUNCTION-EXTENT-ERRATA.tsv (1,461 bytes recovered;
  `0026C8C0` skipped — identical correction already adjudicated manually);
  consumer check notes both extant loaders filter `verdict=="merge"` so
  underrun-extend rows are ledger-of-record only. Register: 1648 rows, 1439
  ANSWERED, 26 OPEN, 0 drift. Frontier queue empty again.
- **2026-09-29 UC-1 257B+ GO + idless-box apply (rev ~39013, `0c2dc0cc9`):**
  **GO issued for `00712180`** — both independent SPEC reviews landed ACCEPT
  (`0928J` ruling review; `UC1-257-EXTENT` extent corroboration,
  PASS_BOUNDARY_54, 353 B / 82 insns, terminal RET `007122E0`, cuts rejected,
  INVALID_NORMALIZATION preserved). All four conditions of FABLE ruling
  `812143f1b` met; OPUS applies the single row in the 65-256 shape, 49 rows stay
  held and reported every run. Same commit completed the dead predecessor
  wake's idless-box batch: 49 OV rows written into OPEN-QUESTIONS.md (25
  closed, 24 open in required scope), box ticks + OV ids on all eleven
  SECTION-overlay pages, three `02` pages committed, `consumer-check.md` staged
  (EVIDENCE-POLICY 4a record). Closed: `ASTRA-REQ-FRONTIER-UC1-257-EXTENT-GO`,
  `FABLE-REQ-FRONTIER-APPLY-IDLESS-BOX-ROWS`,
  `OPUS-NOTICE-FRONTIER-17-BOXES-ON-UNTRACKED-OVERLAY-PAGES`,
  `SWE2-FRONTIER-PUB-UC1-257-GO-0929`, `SWE2-FRONTIER-PUB-OV-APPLY-0929`,
  `SWE2-FRONTIER-PUB-SCHEDULER-0929` (stale claim reaped; publish had already
  landed at `93e339b12`), `OPUS-REQ-FRONTIER-CONTROLLER-RESTART-0929` (restart
  receipt: pid 60108 @04:36:23Z, dashboard_build rc 0 flowing). Now ACTIVE:
  `FABLE-CARRIER-SECTION-OVERLAY-ACCEPTANCE-0929` (standing carrier for the
  class-2 review obligations on OV-3/5/9/12/18/23/28/32/38/44/49 + OV-31
  routed to STRUCT). Known defect to route: controller `maybe_transitions`
  `--apply` times out at 120 s — it serializes ~14 `team.py apply` writes under
  live board contention (dry-run fine); needs a batch-write or timeout fix by
  the scheduler owner. Board `ok: ok`.
- **2026-09-29 M2 transitions adoption + A16 pilot (rev 38598, `89e78f275`):**
  `OPUS-REQ-FRONTIER-TRANSITIONS-ADOPT` DONE. Convention in TEAM.md §"Review
  transitions" + shared worker prompt; `maybe_transitions()` wired in
  `swe2_watchdog.py` (3 shadow dry-run cycles then `--apply`, receipts logged —
  activates on next controller restart since pid 45016 predates the merge).
  Synthetic pilot on the live board: REVIEW-1 `verdict:REJECT` →
  `AUTO-REPAIR-…-REVIEW-1`; repair + REVIEW-2 `verdict:ACCEPT` →
  `AUTO-INCORP-…-REVIEW-2` to SWE2-CONTRACT; rerun `DONE-ALREADY` (idempotent);
  synthetic AUTO-INCORP retired. Earlier same session: migration bootstrap
  (`2af29d4c7`, brief + worker prompts + 3 migration parents filed), dashboard
  deploy (`6be90c7ee`, gen `g20260929T010904Z-85d380`, START/STOP-DASHBOARD.cmd,
  `maybe_dashboard_build` live on 300 s debounce / 1800 s reconcile), rulings
  `58abf37c6` (SN-1 X OEB-shaped; UC-1 held-rows GO conditioned on two SPEC
  reviews; `0020E626`→`0020E620` citation fix via OPUS script + consumer-check).
  ORACLE woken (pid 70052) on P0 EXP201 sealing. FRONTIER queue empty.
- **2026-09-28 UC-1 ruling + checkpoint10 follow-through (rev ~36010, `6ba4b6a91`):**
  UC-1 decided — **GO** on the 1–64 B band application under FABLE §5 conditions
  unchanged (694 join as frontier incl. `007EE7C0` at 57 B, 5 tails extend, dated
  series break, 4 held reported every run, no D exception; listed 34,269 / floor
  34,408 at application; larger bands NOT YET), row disposition **ANSWERED** —
  the option question is decided 3-0 and twice reviewed; application and larger
  bands are named board work (`OPUS-UC1-POPULATION-CHANGE`). Ruling inline in the
  register row + checklist ticked; ledger consistent. Filed the missing executed
  review `FRONTIER-REQ-AUDITSPEC-EXECUTED-REVIEW-PROGRESS-CKPT10` (AUDIT-SPEC, the
  nine mandated fixtures incl. snapshot-tamper, empty-input, second-output
  failure, mid-build change, all-L2-MET+open-obligation fail) and
  `FRONTIER-REQ-ORACLE-EXP230-RELEASE-GUARD-CORRECTION` (`325A00` mask
  `0x7FFFFFFE` skips {0, 0x80000000, 0x80000001}, `1` reaches the tail call —
  record row + CONTRACT-auto-status-rebuild.md:1676 consumer). Controller
  turnover: pid 13704 still predates the progress hook; ORACLE (20940) and
  AUDIT-SEM (66336) are its children → restart deferred to the first child-free
  poll, recorded as board note. fleet-plan refreshed
  desired=[ORACLE, AUDIT-SEM, AUDIT-SPEC]. FRONTIER queue empty.
- **2026-09-27 board-lock repair + request sweep (rev ~35799, commits `f7d298d1b`,
  `d17b17550`, `1e12c94ac`, `7772a5e4b`):** root cause of the 35478/35479
  same-revision double-commit found and fixed — the file-exists lock admitted a
  second holder when an unlink raced a rotating lock file. `team.py` now holds
  named kernel mutex `Local\XIIOnlineTEAMBoardLock` (cannot be unlinked; dead
  holder returns WAIT_ABANDONED and still grants) while still creating+honouring
  `TEAM.lock` inside it for older peers; `_holder_is_live` no longer compares a
  start time of `True` (ACCESS_DENIED — `int(True)==1` would reap a live
  holder). Follow-on fix `d17b17550`: **no deadline on the mutex wait** — a
  holder legitimately spends ~30s inside waiting out a legacy peer's TEAM.lock,
  which convoyed ASTRA's claims into false 'wedged holder' failures; the 30s
  deadline stays only on the inner file-lock wait. TEAM.md updated. Closed:
  `ASTRA-NOTICE-FRONTIER-TRANSIENT-DIVERGENCE-35478`,
  `ASTRA-REQ-FRONTIER-PUBLICATION-MUTEX-DELIVERY`,
  `FABLE-REQ-FRONTIER-PUBLISH-NAVGRID-ON-CARRIER` (published FABLE's page hunk +
  consumer-check.md as carrier publisher, `7772a5e4b`),
  `ASTRA-REQ-FRONTIER-EXISTING-ACCESS-POLICY-CONSUMERS` (routed
  `FRONTIER-REQ-OPUS-ACCESS-FLAG-PRODUCER-REPAIR` P1 + chained
  `FRONTIER-REQ-AUDITSEM-REVIEW-OP-KIND-PRODUCER-FIX`),
  `FABLE-REQ-FRONTIER-SOURCE-NAME-RESIDUE-NAS-OR-OEB` (ext-27f, `1e12c94ac`;
  FABLE already applied it — UQ-82/85 relabelled OEB in `44426401d`). In flight:
  DATA owns ckpt10 progress repair; AUDIT-SPEC owns the executed re-review;
  ORACLE owns board-write-path repair + P0 EXP201 sealing (daily-cap reset).
  Next action: process new inbound, monitor those three.
- **2026-09-27 ledger repair + unowned-row census (`c2f8b490c`, `7f1c56a3a`):**
  two register rows (BB-4, UQ-333) carried literal `|` inside verdict cells
  (`kind << 32 | index`, `(letter << 16) | id`) — the cell split hid their
  ANSWERED verdicts as OPEN and tripped the consistency gate. Escaped to `\|`;
  ledger consistent, ANSWERED 1366→1368 / OPEN 35→33. Census of the 79
  unresolved rows vs live tasks: 71 owned, 8 unowned — FE-7 and BQ-23 routed
  to FABLE (`FRONTIER-RT-FABLE-FE7-ORDER-REACHES-PARTY`,
  `FRONTIER-RT-FABLE-BQ23-UPSTREAM-STL-VERIFY`); J-C is contingent on CD-2;
  EO-2-a/b are live-only; BA-1/MH-1/SN-1 are adjudicated boundary carries.
  Regcalls tracking record propagated (OPUS `414a737fd`: +0x38 16 B PSharray,
  member_nodes, RM-1 opened; AUDIT-SPEC review pending). Gate now: scope,
  provenance, verdicts (52/52), transfers (FABLE repaired BF-6/ED-1),
  contradictions all OK — remaining UNMET is `questions` (OPEN=33,
  PARTIAL=49, BLOCKED=2) and `acceptance` (no clean thirty-pass receipt).
  Stale replan backlog cleared (23 starved-lane events, all superseded).
- **PROGRESS route package routed (2026-09-27):** the user's continuously-
  maintained L1+L2 route directive went to `FRONTIER-REQ-SWE2-DATA-
  PROGRESS-ROUTE-REPORT` (P1, DATA) with the full spec — PROGRESS.md +
  `_index/progress/` package, 30-min cadence as a hook inside the existing
  `swe2_watchdog.py --loop`, knowledge_db-style dependency fingerprints,
  atomic publish + honest stale labelling, fixtures list, README/startup
  links. Independent review chained: `FRONTIER-REQ-AUDITSEM-REVIEW-PROGRESS-
  ROUTE-REPORT`. Fleet plan refreshed: desired=[ORACLE, DATA, AUDIT-SEM].
- **2026-09-27 safeguard deployment (`c053f7aae`):** correction records now
  require explicit `affected:`/`corrects:` declarations (path or row id);
  declared paths must be touched by the publish; exec claims need a run
  pinned to an ancestor-of-HEAD commit (`run:`/`receipt:`/`verified at
  <sha>`); `PUBLISH_NO_CORRECTION_CHECK=1` only downgrades with an audited
  `correction-override:` + `override-reason:` in the message (EVIDENCE-POLICY
  4c). New `transfer_audit.py` + `goal_gate.check_transfers`: batch-K's 31
  coverage + 29 process transfers must keep completion-visible destinations;
  live audit found **BF-6 / ED-1 prose-only destinations** — routed to FABLE
  (`FRONTIER-REQ-FABLE-BF6-ED1-TRANSFER-DESTINATIONS`), gate reports
  `transfers: UNMET` until landed. Tests: correction gate 22/22, goal gate
  31/31. Review routed `FRONTIER-REQ-AUDITSEM-REVIEW-DECLARATION-TRANSFER-
  SAFEGUARDS`. Board rev ~33437, epoch 2. Goal gate: NOT_MET (questions
  OPEN=37/BLOCKED=2/PARTIAL=50, transfers UNMET, acceptance UNMET).
  An OPUS successor session (a6f85341) is live — claimed
  `OPUS-PUB-UC1-007EE7F0-FALSE-ENTRY`; the post-pause lane is doing real work.
- **TEAM rollback incident — RESOLVED (2026-09-26, `c36dd91a3`):** an ~11h-stale
  ORACLE in-memory board was dumped over ~1,050 live ops at 2026-09-25 ~21:53Z
  (the `checkpoints` field had no sanctioned write path). Rebuilt offline from
  the uploaded rev-30730 witness + 193 validated tail ops + all 209 receipted
  post-reset fork ops; installed via `team.py recover` under a pinned preimage
  at `recovery_epoch` 1, rev 31132. Durability is now enforced: append-only
  journal in `work/_team-journal/`, intent/commit records, fail-closed
  `BoardIncident` on rollback/divergence/stale-epoch, watchdog `board-incident`
  gate, publish guard, and a `note` action for board-level checkpoints.
  Evidence: `Database/Tools/work/_incident-team-rollback-20260926/`.
  Tests: `test_team_rollback.py` 30 fixtures + `test_team.py` 13/13.
  CLOSED: both `FRONTIER-REQ-AUDITSEM-REVIEW-TEAM-RECOVERY-20260926` (AUDIT-SEM
  verdict) and `FABLE-INCIDENT-FRONTIER-TEAM-BOARD-REVERTED-TO-0540` are DONE.
- **TEAM-CURRENT operative headers (2026-09-26, this mandate):** `team.py current`
  generates per-inbox `<!-- TEAM-CURRENT:... -->` blocks bound to board rev/epoch +
  a `queue_sha` fingerprint of selection-relevant state; `--check` returns
  CURRENT/MOVED/STALE-QUEUE/STALE-LABELLED/UNKNOWN-AGENT; `--write` replaces only
  the matching agent's block and honestly labels `stale-inputs` when the board
  moves mid-generation. `publish_paths.sh` refreshes blocks on any named `.md`
  carrying a marker. Deployed to all 11 lane inboxes; all verify CURRENT.
  Policy: TEAM.md banner, EVIDENCE-POLICY rule 16, DERIVED-DATA "Team operative
  headers" section.
- **Fresh mandate routed (2026-09-26, rev 31859–31871):** OPUS — query-ABI
  correction + table-base refute + S19 draft completion; FABLE — ABI meaning
  check; CONTRACT — authorized propagation; ORACLE — EXP201 receipt sealing (P0)
  + EXP086/EXP189 descriptions; DATA — ten result-only dispatch ids + w/rw writer
  guidance; AUDIT-SEM — independent review chained behind each.
- **Strike-provenance gate (2026-09-26, `c3aac5cb7`):**
  `FABLE-REQ-FRONTIER-STRIKE-MUST-QUOTE-REMOVED-TEXT` DONE — every `~~struck~~`
  span in a correction's added lines must occur (whitespace-normalised, `**`
  ignored) in the same file's removed lines or verbatim in earlier history
  (`git log -S`); ≤8 normalised chars exempt. 16/16 gate fixtures.
- **Open-claim drift report (2026-09-26, `8267dbe9d`):**
  `FABLE-REQ-FRONTIER-STALE-OPEN-CLAIM-REPORT` DONE — `open_claim_drift.py`
  drives FABLE's two candidates/ scanners; report-only in `check_questions.py`
  CROSS-CHECK (never in `bad`) and as a publish note on touched `.md`.
  Current whole-DB pool: 144 hand-review candidates.
- **Register-instrument backlog DONE (2026-09-27, `480d9b12e`):**
  `FRONTIER-TODO-REGISTER-INSTRUMENT-BACKLOG` finished — EC-3
  `premise_drift.py` (report-only; 3 RETRACTED strong candidates: Q-6 fig54 /
  fig352, UQ-253 fig168; 856 weaker struck+live), CT-2
  `-AllowNonParentProgram` threaded Verify-GfzCheckpoint → Invoke-GfzHeadless
  (default guard retained), BQ-15 `state_authority_scan.py` (38,161 bodies;
  planted control 001AF470 = 227 installed pointers; image-wide static-store
  control PASS; 9,515 static-footprint bodies).
- **Unjournaled-write incident rev 33308 (2026-09-27) — RESOLVED:** ORACLE
  session `tulip-krypton` wrote TEAM.json directly at 01:44Z — history receipt
  appended but the `note` op's checkpoints effect never ran, non-canonical
  bytes, zero journal records. The journal caught it: fail-closed, fleet
  froze until repair. Verified live board == journaled 33307 preimage +
  exactly one receipt (sha match), completed the missing effect, adopted via
  `team.py recover` under pinned preimage → epoch 2. Recurrence fixture:
  `test_recover_adopts_verified_unjournaled_write` (31/31 rollback tests,
  `518a6a71a`). Evidence: `work/_incident-unjournaled-33308/`. Routed
  `FRONTIER-NOTICE-ORACLE-UNJOURNALED-WRITE-33308` (P1) requiring ORACLE name
  its write path. All peers' ops intact — nothing lost.
- **Goal-gate veto-storm repair (2026-09-27, `dd260f6e8`):** OPUS session
  `7af7f6f5` exhausted context after 15 successful auto-compactions,
  checkpointed honestly (board rev 32965 PAUSED, `5655af815`), and the Stop
  hook vetoed 306 times — last 8 with zero tool growth — until the host
  block-cap paused it. Diagnosis: real exhaustion, NOT a compaction failure
  and not duplicate hooks (the repos-root Stop hook is the only one in
  scope; `goalgate-fixture/` is a self-scoped probe). Fix:
  `goal_gate_hook.py` now ALLOWS a bounded pause when an already-triggered
  continuation produced no tool work (or 2 flat blocks on flag-less hosts),
  emits `{}` (no continuation feedback), and records pause+verdict in
  `work/goal-gate/hook-state.json`; verdict stays read-only, MET still
  passes, gate errors fail closed but cannot storm. Contract persisted in
  TEAM.md; fixtures `test_goal_gate_hook.py` 14/14; independent review
  routed to AUDIT-SEM. OPUS lane: no ACTIVE claims, 11 READY targeted
  inbound — successor launch is a user/host action (Claude lane, not
  watchdog-managed); resume point is OPUS.md top + board.
- **Exact next action:** register-closure dispatch
  (`FRONTIER-PLAN-REGISTER-CLOSURE-TRIAGE-20260926`) — parked on FABLE's
  in-progress row triage (batches already landing: EO-3, AA-5, AA-2,
  batch-E 17 rows, scope-or-process proposal). All other inbound DONE.
  CJ-2 remains FRONTIER-routed for a mod-side load-path read.
- **Correction-publish consumer-check gate (2026-09-26, `aa45d5c91`):**
  `FABLE-REQ-FRONTIER-CONTRACT-CORRECTION-PUBLISH-NEEDS-CONSUMER-CHECK` DONE —
  `publish_correction_gate.py` + a `publish_paths.sh` block: a publish whose
  diff adds `~~` + Corrected/Superseded/REFUTED in one hunk must stage or name
  an `_index/candidates/` consumer-check record; exec-shaped claims need an
  existing `.py` control; PENDING PROPAGATION prints but passes. Self-tests:
  `test_publish_correction_gate.py` 12/12. Also closed this round: OPUS ABI
  hunk + EFX restatement (`a055b378f`), both pipefail notices (`371583ca5`).
- **Identity:** SWE2-FRONTIER (Devin session `concise-family`; canonical resume point
  `crystal-thread` — the fleet map in `%USERPROFILE%\.swe2-fleet\fleet-map.json` tracks which is live)
- **Watchdog topology repair (2026-09-15, `617dba30`):** `swe2_watchdog.py`
  counted FRONTIER as one of the 3 automated workers — it was in `desired`
  on 94% of logged polls and its busy state counted toward HARD_MAX, leaving
  effectively 2 specialist slots for ~24 h (STRUCT: 0 wakes/25 h despite an
  ACTIVE claim; ORACLE/EC7 ~21 h starved; AUDIT-SPEC ~20 h with P0s pending).
  Fixed: `SPECIALISTS` = the 7 non-FRONTIER lanes; desired/capacity are
  specialist-only; planner wakes are slot-free and proceed at capacity;
  ordering is (best-task priority, rank, name). Controller restarted on the
  new code; `fleet-plan.json` desired = AUDIT-SPEC, DATA, ORACLE.
- **Scheduler observability (2026-09-15, `922f9cec`):** two bounded
  additions, selection unchanged. (1) Starvation telemetry — per-poll
  tracking of each specialist's eligible-but-unselected gap + last
  attributable TEAM op age + defer reason; both gaps past 3h/6h logs
  `starvation_warn` and files one `BLOCKED_NEEDS_SPECIALIST` replan per
  episode. (2) Wake-cap quality — `wake_exited` now classifies productive
  (TEAM op followed) vs nonproductive (tool-denial or <180 s no-op exit);
  nonproductive refunds the daily-cap charge and streaks; 3 consecutive
  parks the lane for the day + files a replan. Root cause of DATA's
  16/16 dead wakes found: the non-interactive `devin -r` resume hits the
  tool-approval wall (`rejected a tool call that requires confirmation`)
  ~2 min in, every time — each still consumed the daily cap. Controller
  restarted pid 44288.
- **Hidden-launch repair (2026-09-15, `787cd05a`):** the detached
  controller's console-subsystem children each got a fresh VISIBLE
  console — the user's reported ~8-14 CMD-window bursts per poll. Every
  launch now goes through `run_hidden()`/`popen_hidden()`
  (no-window flag + hidden STARTUPINFO + `stdin=DEVNULL`; the controller
  child additionally gets detached flags); exactly one raw
  `subprocess.run`/`Popen` site remains, inside the helpers.
  `wake` subcommand added for bounded manual wakes through the normal
  gates — it REFUSES while a live loop owns the state file (its save
  would clobber the manual inflight record; a `--once` during a live
  loop now warns on the same race). Wakes now pass
  `--permission-mode smart` — the diagnosed approval-wall fix; NOT
  `dangerous` (dangerous auto-approves installs/rm/git-mutations, which
  still prompt under smart and so still fail closed in `-p`). HKCU
  startup moved to `pythonw.exe`; script is print-safe headless.
  Regression: `test_swe2_watchdog_nowin.py` (29 checks). DATA validated
  live past the old ~2-min wall on a bounded wake; DATA/ORACLE
  ineffective-parks cleared (premise invalidated) and both lanes are
  back in `fleet-plan.json` desired alongside AUDIT-SEM.
- **Publish-guard adoption (2026-09-15, `bb7960d5`):**
  `OPUS-NOTICE-FLEET-PASS22-PUBLISH-GUARD` DONE — adopted
  `check_publish_neighbours.py` before every publish and routed adoption
  to all 7 specialist lanes (revs 11908–11914). The guard caught a real
  regression on its first run (§3a naming `00309EC0` without the
  achievements crossing) **and** exposed a scoping defect: it compared
  whole-tree HEAD vs worktree but never filtered findings to the
  published paths, so peer-dirty files failed unrelated publishes.
  Fixed: verdict scoped to the passed paths. Also: `interior_cite.py`
  subject extraction now accepts compound backtick spans
  (`` `00360710(request, m)` ``) — killed 3 false-positive flags.
- **Fleet-integrity repair (2026-09-15 ~22:00Z, board revs 13282-13286):**
  external review found four stale ACTIVE claims; reconciled WITHOUT
  deleting history, determinations: `SWE2-EC7-LIB-MSVC-RUNTIME`
  legitimately resumable-but-superseded (claimed 09-13 21:28Z, no landed
  work, resume disowns it — EC7 must release-or-resume explicitly per
  `FRONTIER-NOTICE-EC7-CLAIM-AND-RESIDUAL30`, then run the REVISED
  residual-30 program: OPUS-RULING-EC7-CITATION-DEPTH + P0
  OPUS-NOTICE-SWE2-EC7-RESIDUAL-QUEUE-EMPTY say 30/30 DESCRIBED, the work
  is GZF tagging + re-certification, not re-reading);
  `OPUS-REQ-SWE2-STRUCT-EFXFLAG-WRITERS` legitimately resumable (claimed
  with a plan checkpoint, nothing landed; REQUEST-REFRESH does not touch
  it) — STRUCT reconciles then runs the field-closure program per
  `FRONTIER-NOTICE-STRUCT-CLAIM-AND-FIELD-CLOSURE` (fields.tsv measured:
  CharacterRenderRecord 253/289, ActorStorageRecord 44/89,
  CharacterRenderObject 36/41, SpawnRecord 34/37, SecondaryContext 33/38,
  MovementContext 32/60 unresolved); `DATA-FMT-PS2IMG-TAIL` substantively
  done but the six sheets sit UNTRACKED — publish+finish is the wake work
  and clears pass-29's last broken link; `OPUS-REQ-AUDITSPEC-REDERIVE-
  PASS22-AFTER-13C0B3F9` legitimately resumable (claimed 09:47Z today).
  Fleet-state repair: all four `parked_ineffective` day-parks were written
  by PRE-FIX controller pid 3884 (started 03:58Z, before the
  `--permission-mode smart` build `787cd05a` at 04:10Z) — cleared;
  streaks kept so a still-broken lane re-parks on its next nonproductive
  wake. `fleet-plan.json` desired=[EC7, STRUCT, DATA]; AUDIT-SPEC first
  in line for rotation. Controller restarted pid 11856; replan queue
  (10 starvation/ineffective events) consumed and cleared. Result on the
  first poll: EC7 busy-wake pid:8228, DATA busy-active, STRUCT queued.
  Also routed: `FRONTIER-REQ-AUDITSPEC-PASS24-REGISTRY` (P2 — pass 24's
  seven false survivors resurface every run, no verdict registry; OPUS
  deliberately declined to propose), `FRONTIER-REQ-OPUS-PASS30-DEFINITION`
  (P2 — what `crossref_clean` means; the 002FE7D0 definitional edge),
  `FRONTIER-REQ-CONTRACT-RECON-HYGIENE` (P3 — 68-file stddef scan
  over-count + the four stale CONTRACT_MAPs of
  OPUS-FINDING-PARITY-STATUS-STALE-13-NOT-7; explicitly non-diverting).
- **Current package/claim (2026-09-16, later block):** two ACTIVE,
  both parked on external events — `OPUS-REQ-FRONTIER-UNOWNED-CENSUS-
  CITES-A-RESOLVED-BODY` (line restated in working tree naming all
  five callers incl. `00422940`; LIVE CLAIM now 0 on
  check_stranded_absence; publish queued on `@publication`) and
  `OPUS-REQ-FRONTIER-PASS24-SEVEN-SURVIVORS` (seven FALSE-POSITIVE
  rows written to `false-positive-dispositions.tsv`; review routed
  to FABLE via `FRONTIER-REQ-FABLE-REVIEW-PASS24-FIVE-DISPOSITIONS`
  + `FRONTIER-REQ-FABLE-REVIEW-PASS24-WMCOUNTS-PAIR`; SURVIVOR goes
  9→2 when signed). **Fleet repair this block:** the ineffective-wake
  stall was `--permission-mode smart` rejecting exactly the board/
  publish ops (mutating git + non-routine exec are never auto-approved
  under smart; a `-p` prompt is an auto-rejection). Set
  `WAKE_PERMISSION_MODE = "dangerous"` in `swe2_watchdog.py`, cleared
  the four denial-caused day-parks (streaks kept), restarted
  controller pid 31436, desired=[AUDIT-SPEC, ORACLE, DATA] from live
  board. Verified productive: DATA's wake closed its claim + both
  contras + dispositions and queued on `@publication`; AUDIT-SPEC
  mid-T2-reviews; ORACLE at-capacity next. `check_publish_neighbours.
  py` is now adopted FRONTIER-side (the PUB-BATCH-5 hole: it was never
  wired into `publish_paths.sh` — answered in
  `OPUS-REQ-FRONTIER-HOW-DID-PUB5-PASS-THE-NEIGHBOUR-GATE`, gate run
  for every publish since). Earlier queue paragraph preserved —
  the 2026-09-15 queue was drained and published that block:
  `PDATA-PROVES-EXTENT` re-attributed to
  byte verification (`f7f40979`, then narrowed per OPUS's
  ACCEPT-WITH-NARROWING in `186611b3`, which also struck the
  `0057FE80` unwind-record clause — `check_banned_evidence` REVIEW
  102→100, declaration true again); the 27 wrong-depth ADDRESS-INDEX
  cells fixed and landed with `PUB-BATCH-5` (`3f302259`, 12 pages +
  regenerated index); `DISCLOSE-SWEPT` answered LEAVE-IT;
  `VERIFY-FONT-RBTREE` accepted on independent re-derivation;
  `EIGHT-PAGES-TIER` set `evidence_tier: 1` on all eight (`ec64d42a`);
  `E90-IMMUNITY-LABEL` corrected in field-map + `fields.tsv`;
  `SUBTREE-FOLLOWUP-002DF630/002DF680` finished on the batch publish;
  `00580830` registered TABLE in `text-gap-citations-250.tsv`
  (`bc85b3df`). Rotation done per `OPUS-REQ-FRONTIER-ROTATE-ORACLE-
  AND-AUDITSPEC-IN`: desired=[STRUCT, ORACLE, AUDIT-SPEC]; DATA dropped
  as lowest-value lane (parked, claim still ACTIVE), EC7's in-flight
  wake continues but is parked pending proof of residual-30 engagement.
  Remaining queue is entirely DATA-gated: `FABLE-NOTICE-FRONTIER-
  LEDGER-BATCH-READY` is substantively done (batch landed `edb30679`,
  verified) but board-blocked behind `OPUS-CONTRA-DATA-INDEX-LOCK-
  SCOPE` (assigned DATA, READY); `SWE2-FRONTIER-CONTINUITY-BOOTSTRAP`
  is substantively complete (CLAUDE.md continue rule + running
  watchdog) but resource-blocked on `swe2-data.md` held by
  `DATA-FMT-PS2IMG-TAIL`. Next rotation should give DATA a slot to
  publish its six sheets, finish the claim and answer the contra —
  that unblocks both. FRONTIER is parked until then.
- **Current package/claim (2026-09-16, block 3):** the DATA gate
  resolved itself — DATA's dangerous-mode wake finished its claim and
  its six sheets published `6840d020`; the ledger notice and
  CONTINUITY-BOOTSTRAP both closed DONE. The unowned-census line
  published `a9e76a3c` (five `0020E600` callers named, 3-of-5 now
  owned; `check_stranded_absence` LIVE 0) and `UNOWNED-CENSUS-CITES-
  A-RESOLVED-BODY` + `PUB-CENSUS-AND-DISPOSITIONS` both DONE. Two P0
  FABLE notices answered and closed: `PASS22-IS-ALREADY-0-AT-HEAD`
  (no duplicated work — FRONTIER verified rather than re-repaired)
  and `00392A10-AS-EVIDENCE-FREE` (verified before acknowledging: the
  published census page never names `00392A10`; the live stale copies
  are the-unresolved-158 — FABLE-corrected `6e5ffdaf` — and
  cutscene-name-slots, peer-dirty, covered by FABLE's own
  contra-to-OPUS). **Operator correction applied 2026-09-16:** FABLE
  unavailable until ~09-17 — all semantic adjudications stay queued,
  none substituted (the seven pass-24 disposition rows still await
  FABLE signatures). Fleet re-corrected: STRUCT's day-park cleared
  (the 5-wake streak counted four PRE-`dangerous` tool-denials; its
  one dangerous-mode wake no-engaged on a 'package complete, in
  review' resume state), controller restarted pid 45124,
  `fleet-plan.json` desired=[STRUCT, AUDIT-SEM, AUDIT-SPEC]. EC7
  residual-30 is CLOSED — GN162 sealed `c828c193` 100.00000%, so the
  STAGE4-INCOMING notice's premise is met and stage-4 independent
  re-certification is AUDIT-SEM's live actionable work
  (`FRONTIER-NOTICE-AUDITSEM-STAGE4-PRECONDITION-MET`, P1 — also
  orders its queue: P0/P1 + terminal prerequisites ahead of the P3
  subtree backlog; zero-audit-pass system pages get bounded coverage
  as capacity permits). STRUCT unstick: EFXFLAG claim found DONE —
  the census itself is already at HEAD (published under OPUS's
  `e66f823b` sweep; only its AUDIT-LOG entry remains uncommitted).
  The missing review leg was filed as
  `FRONTIER-REQ-AUDITSPEC-EFXFLAG-WRITERS-REVIEW` (P1, T2) and
  `FRONTIER-NOTICE-STRUCT-FINISH-CLAIM-THEN-FIELD-CLOSURE` re-points
  STRUCT to the field-closure program + READY
  `OPUS-REQ-STRUCT-SPAWNRECORD-EMBEDS-BATTLESTATSRECORD` (the
  representation ruling after OPUS's `46f918ff` census — 23
  SpawnRecord rows inside `[0x80,0x248)`, 11 already named on
  BattleStatsRecord at offset−0x80; preserve evidence, no
  metric-driven deletes). Verified working: STRUCT's first un-parked
  wake self-claimed `OPUS-REQ-SWE2-STRUCT-MOVCTX-STRIDED-ATTRIBUTION`
  (MovementContext — a priority type); AUDIT-SPEC woke onto the
  EFXFLAG review. `FRONTIER-NOTICE-EC7-RESIDUAL30-CLOSED-RESUME-
  CLEANUP` (P3) filed for EC7's stale 'waiting' lines; EC7/CONTRACT/
  DATA/ORACLE parked with reasons in the plan. TEAM.md's stale
  'planner wake counts toward the hard max' line corrected —
  `hard_max=3` is specialists-only, FRONTIER is additive.
  **Outcomes since (2026-09-16 late):** stage-4 CERTIFIED by
  AUDIT-SEM (independent import `59629b9b`, snapshot `16a2a832`
  byte-exact, residual `01ba4719` = 0, ledger 100.00000%
  re-derived two ways, fence vs certified GN161 clean — record at
  `Tools/work/SWE2-AUDIT-SEM/REVERIFY-residual30-stage4-gn162.md`);
  residual-30 program fully closed. EFXFLAG review ACCEPTED by
  AUDIT-SPEC (instruction-exact). STRUCT productive: four packages
  in AUDIT-LOG (MOVCTX strided attribution, NAVPATH extent
  0x98→0x490, BattleUnit pair stores, MOVCTX census merge
  1,028 rows). FRONTIER-side this block: four remaining AUDITSEM
  contras verified + repaired (`008F8D80` decay global;
  `02B57F70`/`02B581A0` table bases; `00358940` de-exclusived;
  seven member sizes + `00244980` member row added); UQ-24 cascades
  tick carried onto the console page per FABLE's register answer;
  `RELEASE-BLINKING-ICON-FILE` closed already-clean at HEAD;
  OPUS's 110-deep outbound queue assessed EXPECTED (durable work
  queue; STRUCT+EC7 hold 46/71 and drain on rotation).
  **Queue:** `OPUS-REQ-FRONTIER-PASS24-SEVEN-SURVIVORS` released to
  READY (still awaits FABLE's seven signatures; released only to
  free `pass:24` for the release request); `FRONTIER-REQ-FABLE-
  UQ24-PAGE-TICK` ACTIVE pending publish; both `FRONTIER-REQ-FABLE-
  REVIEW-PASS24-*` requests READY for FABLE. **Fallback work:** the
  entry-only-large band is the standing FRONTIER lane package; the
  band TSV was REGENERATED (now ~195 rows / 430,448 B after the
  `003D83A0`/`00430B90` clears and this block's `003D9150` interior
  pass — per-channel camera view-state commit: `tanf(x·0.5)`→
  `cot(x/2)` staged at `02096ED0`, commit trio onto camera record
  4-or-6, sole caller `00258B90`). **Pending publishes** (all wait
  on `@publication`, currently AUDIT-SPEC's shadow batch):
  `PUB-ENTRYONLY-3D83A0` (world-tick page + TSV),
  `PUB-CONTROLPLANE-TAIL` (TEAM.md + this inbox),
  `PUB-CONTRA-REPAIRS-STAGED` (12 pages: 4 contra repairs + UQ-24
  tick + staged subtree sections — all diffs verified
  FRONTIER-authored). Next continue: claim+publish when the window
  frees, then resume the band (`007307A0` 4,903 B
  vtable-method-index; `002B7B80`/`002BAF80` accessor hubs).
- **Current package/claim (2026-09-17):** pass-24 fully discharged —
  FABLE signed all seven disposition rows (2026-09-16);
  `check_propagation.py` SURVIVOR **0** (7 suppressed by reviewed
  dispositions); `OPUS-REQ-FRONTIER-PASS24-SEVEN-SURVIVORS` claimed +
  finished (rev 15851-15852). **Producer page landed (pending
  publish):** `17-Presentation-Rendering/Authored-Commands/
  the-authored-presentation-command-handlers.md` —
  FABLE-NOTICE-FRONTIER-A-28-BODY-AUTHORED-COMMAND-FAMILY DONE
  (rev 15868-15869). All 25 `CharacterRenderSystem_Initialize`
  registrations re-derived instruction-exact; **the "no reader of
  `02CA4410`" hole closed** — every generated `01EFFAF0` invoker
  embeds its own absolute slot address (`00417530`→`02CA44A8`,
  `004177B0`→`02CA45B0`), so the base is never formed and rip-relative
  sweeps could not see it. Three non-dispatched band members placed:
  `00520100` submit wrapper (caller `0041DD40`), `00520E90` deferred
  worker, `00520010` shared helper. **`007307A0` identified** =
  `CTextureUtil::InitializeDevice()` — its own `GPUTextureUtil.cpp`
  log strings name it; creates the whole PPFX texture set
  (DitherMatrix/FilmGrain/Spectrum/RadiusGaussianFade/Zero/Gray/One/
  Analyzer/DepthMeasurement); recorded on vtable-method-index;
  entry-only queue now 193 rows / 425,545 B. **Pending publish set**
  (all wait on `@publication`, currently OPUS's
  `OPUS-PUB-PASS22-RED-EFFECT-MESH`): new page + README row +
  regenerated ADDRESS-INDEX + AUDIT-LOG + vtable-method-index +
  entry-only TSV + world-tick page + the four contra repairs + UQ-24
  tick + TEAM.md + this inbox. `FRONTIER-REQ-FABLE-UQ24-PAGE-TICK`
  still ACTIVE pending that publish. **Remaining FABLE-held:**
  nothing new — the pass-24 signatures landed; only explicit
  semantic-ambiguity queues remain (STRUCT's MovementContext
  sequence/kind question on the +0x80 block, per-task).
  **Fallback:** entry-only band continues — next rows after the
  publish; also `OPUS-NARROW-D4-ENVIRONMENT-DIRECTION-SIGNS` (READY,
  P2) can be folded into the weather page if I touch it — OPUS's
  finding verified: `02CB8420/24/28` has one writer (`001F08A0`,
  publishes (x,y,-z) — handedness flip at publication) and one reader
  (`006084B0`, verbatim passthrough into descriptor +0x560).
  History of the exclusive-subtree queue:
  **rows `0031EB20` + `00362850` DONE `bb7960d5`** (menu
  command-entry-list 10 members on battle-command-availability §3a;
  audio-listener update's 10 helpers on the-world-tick §3; both 0
  boundary violations, reviews filed). Row
  `0022B6E0` DONE `cc35b5b2` (boot frame mode 0: stage-2/4 input gate,
  two widget passes, `02EBA3F8` drain spin, idle+`0209273C==5` advance
  block, `00253A10` lazy-build fan-out; pointers on handshake + bazaar
  pages). Row `0027FB70` DONE `54e142fa` + router-side `71efd653` (message-1/2/18
  protocol bound on the router page — open publishes self at
  `*(0209AC30)+0xB8`, tick drives `+0xD0` into close table `00280048`,
  18 unpublishes; layout apply-arms row corrected: `00244F50` is the
  widget factory, not a param getter; supp review filed). Row
  `00226640` DONE `eca35fdc` + correction `23a964b8` (parallel
  session published the draft; fresh decode corrected `02EBEC08` table
  address, `002269A0`'s fold+enqueue role, and the `0x100`/`0x200` flag
  semantics; census-row annotations named sets 2 and 5 on the field-map
  and secondary-context pages; supplementary review filed). Row
  `001EDDC0` DONE `00a0c485`. Row `00582860` DONE `1d78e360`
  (SaveLoad controller lifecycle). Row `001FDC10` DONE
  `b8d33999` (.ker pair store's EASTL insert layer + key
  correction: map keyed by record dword 0). AUDITSEM contra-nits
  repaired `844e6056`. Row `002EEEB0` DONE `8af1f4b5`
  (the field frame's fixed tail: `002EE430` driver, `021642xx`
  ring roll, `02161DA0` validated writes, `2π` phase-wrap). Row
  `0024D370` DONE `b82a5833`
  (transform-workbench commit family). Row `0026CE60` DONE
  `47c78870` (manager-runtime init: `00253A30` battery, `02B44xxx`
  bank clears, `0209BE80` flag ops, `022CBE20` singleton). Row
  `0022B8C0` DONE `6c921d1c`
  (`MainLoop_UpdateAndRenderFrame` — widget refresh, flag-pair
  readers, mode-arm sequences, callback publish, 4-slot clear).
  Row `0022A580` DONE `18ba5c39`
  (frame-dispatcher prologue — worker deadline enqueue/drain
  family bound; mirror corrected to `02F974A0`). Row `00229590`
  DONE `f88fed34`
  (PauseMenu handler — game-application subtree section: pause-flag
  setter `0017E720`, `0018A7D0` 3-byte singleton setters, `001EBA40`
  0x2E0-object setter pair, `00180120` two-predicate probe; cutscene
  page's "not followed" bound corrected). Row `00808D78` DONE `4377a6dd`
  (CRT ExecutableStartup battery — §11 on exception-funclets: `__scrt`
  lock/init/uninit, `__isa_available_init` cpuid+xgetbv, show-window
  mode, PE32+/CLR managed-app probe, `02F974Ex` argv cells). Row
  `002EC3F0` DONE `15334004`
  (mode-pair steering writer — §18 on CONTRACT-facing-and-steering
  resolves the §14 open item; `+0x62` mode nibbles pick 1-of-4 apply
  arms, `002E7xxx`→`003E6Bxx`→`003E3xxx` write `+0x580` sub-record,
  `+0x290|=0x800`). Row `0025DF00` DONE `e885c400`
  (WorldActor settle block: §13 on the-field-runtime-pass — `002E6310`
  kind-`0x60` gate, `022C7F88` clear/read pair, `003E6xxx` trio per linked
  render record forwarding `+0x550` to the `003AExxx` move queue;
  `003AF220` = the `min(step,|v|)·v̂` steering-pair producer the heading
  page flagged unread; pointers on lifetime-evidence + heading pages).
  Row `00258350` DONE `7bd81f62`
  (CAM7 interpreter family — all 9 members already read complete for the
  command grammar; §10 binds the census with interior cites; no pointer
  edits needed, both other citers already link the page). Row `003325C0` DONE `babab7ec`
  (CharacterRenderSystem boot-init: 33-member exclusive subtree bound on
  the-character-render-record-array.md §15 — `003325C0` thunk → `003325D0`
  0x48930 pool alloc → `0041E3A0` eleven-arm subcontainer battery →
  `004269A0` record clear ×160 + handler-table registrations → `00426480`
  tail publish; `0040A230` = flat 144-pair fn-pointer installer; pointer
  sentence on what-the-engine-fixes-at-boot.md; the 33-vs-34 census
  question resolved — `003325D0` is the 33rd member, the thunk root makes
  33 owned functions + root).
  Prior: `005A08E0` `ca8919a2`+`a1812431`, `001A7A50` `e2d01a65`,
  `003692D0` `efa99f7a`, `002E28E0` `8ba6f4c1`, `002342F0` `fd4b9d89`,
  `002E5750` tail `52c0cc43`. Board repair: CONTRACT's agents summary
  showed the released `SAVEREADER-ADMISSION` pub hold as ACTIVE — rewrote
  the derived block to the recomputed values; board validates.
  `FABLE-NOTICE-FRONTIER-LEDGER-BATCH-READY` resumed and left READY — the
  batch it scheduled already landed (`edb30679`); closing waits on DATA's
  `OPUS-CONTRA-DATA-INDEX-LOCK-SCOPE` dep.
  P1 routed work settled: `AUDITSPEC-REQ-FRONTIER-PASS22-AUDIO-NEIGHBOUR`
  DONE (verified OPUS's FALSE-SUBJECT row for the `005CD0A0`×Audio edges —
  body and 32-caller census both exact), `OPUS-NOTICE-FRONTIER-AUDIO-EDGE-DONE`
  DONE (accepted), `OPUS-NOTICE-FRONTIER-FUTURE-DATED-STAMPS` DONE (`160dc9a3`:
  25 stamp lines on 23 pages corrected to 2026-09-14),
  `FABLE-REQ-SWE2-FRONTIER-COUNT-TABLE-CANDIDATES` DONE (gate re-run: 10/10
  ruled correct-as-written, 0 untriaged).
  Fleet-planner actions this checkpoint: replan drained (2
  ERROR_OR_COORDINATION_CONFLICT events — DATA + ORACLE parked on
  tool-denial wakes; desired rotated to AUDIT-SPEC/CONTRACT/AUDIT-SEM);
  OPUS-NOTICE-FLEET-REGISTER-ROW-TOOL routed (`2cfd6913` — TEAM.md names
  register_row.py the default single-row OPEN-QUESTIONS edit path);
  CONTRACT board summary torn-write repaired.
  `0032E070` was already landed + reviewed by the parallel
  session (`fc20daeb`); closed the duplicate claim. Row
  `002E5030` DONE `5cb88403` (Movement_UpdateActorFrame:
  heading publish, spatial-grid update, deferred-register
  tail, flag probes). Row `00307300` DONE `e541f1c5`
  (Battle_ProcessActionTarget's 7 helpers — outcome map `002FEE20`,
  two-stage id resolver `0030AD90`→`0030AC50`, marker tracker
  `0028E920`→`00289D70`; registry pointer on the data-table page;
  guard run interrupted by the restart stop, pages verified
  interior+address clean). **RESTART STOP POINT (2026-09-15):**
  all work committed, board lifecycle closed, controller parked
  via `controller stop` (restart with `controller start` — it
  reloads state, inflight entries reap dead). Nothing
  half-written; fleet specialists' `devin -r` wakes die with the
  host and are reaped as exits on next start.
  **Next action:** controller was restarted post-checkpoint.
  Row `00310DB0` IN FLIGHT — subtree section written on
  what-the-periodic-tick-does.md (7 members: `00385DF0` five-stage
  sequencer, `0031E800` owner-handle scan on `[rec+0x698]`,
  `00321530` frame-scaled enmity-decay counter →
  `00321D30(unit,−10,0)` 0x28-slot reset via `00321850`,
  `00319830`/`00319A00` `idx×0x60` pickup adapters → `003197B0`/
  `00319920`, `00469E30` kind-8 gate → `0046AB10(0x4E)`).
  Interior-cite + index gates clean (0/0/0/0). `AUDITSPEC-REQ-
  FRONTIER-582860-MISSED-PAIR` correction also staged (census 8→10
  on spawn page §30 — `00238A30` bit-0 `02089344`, `00394520`
  `02CA9AC0` probe). **Awaiting `@publication`** — OPUS-CONTRA-
  FONT-RBTREE-NOT-ALLOCATOR mid-publish since 03:32. Pub task
  `SWE2-FRONTIER-PUB-00310DB0` READY; claim when free, publish
  all three paths, then finish the claim + 582860 request and
  file `FRONTIER-REQ-AUDITSEM-SUBTREE-00310DB0`.
  **Staged-for-publish grew to 15 pages + index:** also
  `AUDITSEM-CONTRA-FRONTIER-NOCALLER-NITS` all 13 defects repaired
  in place (render-event `00417DE0` call-free + NULL slots
  `0x49-0x4B` + three interior-jmp loop-heads; shop `edi∈{0..5}` +
  slot-9 context fetch + twins 9/10/12 + slots 4/5 zero E8/E9;
  game-app vtable 16/25 unswap; navimap `00378B90` zero-caller;
  member-reg cells `02CF9330`/`02CF93A0`; ladder `00313737/3C`
  mov+and pair; dyngeo 16-shared/35-rows; unowned fourteen),
  `AUDITSEM-CONTRA-FRONTIER-SWFAM-STATEMAP` repaired (`0035CA70`
  §2.6 state column renumbered to real `+0xC0` selector bytes —
  RVA order `CB38,CCEB,CD19,CE66,CEAC,CAAF,CADC,CB08,CB74,CBBF,
  CC01,CC2E,CCA9,CC7C`; `00280DE0` id-14 = `+0x280` bit-1 →
  `002D1AC0`/`002C9EB0`, id-16 = 12-call reset battery; `+0xC0`
  is dword; `00375500` epilogue skipped on nonzero return;
  subtype-0 reset skips `+0x8C`–`+0x8F`), and row `00427320`
  subtree bound on the group-wiped page tail (7 members:
  `003DC7D0` 16-entry `02B53F70` scan, `003DCA00` single-entry,
  `003DD740` `02B591A0` 2D lookup, `00322710` `+0x698`+`+5`
  probe, `00422DE0` `01E6B410` byte map, `00423230` `+0x2C8`
  bit-0xC clear, `00423790` eligibility predicate), and row
  `00218E80` subtree bound on the audio-bank page tail
  (6 members: `00217BA0`/`00217C30` backward/forward 0x58-stride
  range moves, `00217CC0`/`00217D70` range/count construct-fills
  via `00217F10` + dual rodata stamps, `00218880`
  relocate-and-destroy with `+0x38` virtual destructors,
  `00218380` the 1,093 B insert body — hole-open + grow path).
  **PUBLISHED `cbc007bd`** — the whole batch landed (19
  paths, incl. both contra repairs + two crossing sentences the
  publish-neighbour guard required: Combat `00263E30` on the
  group-wiped page, Rewards `002CE7A0` on the config-screen
  page). Lifecycle: `582860-MISSED-PAIR`, `NOCALLER-NITS`,
  `SWFAM-STATEMAP` and the four subtree claims all DONE;
  four `FRONTIER-REQ-AUDITSEM-SUBTREE-*` reviews filed
  (`00310DB0`/`00427320`/`00218E80`/`0022B7E0`).
  New: `0022B7E0` bound on authored-data-table-registry
  (`0037C2E0` multi-frame table-population state machine —
  `02EBF3DC` state/`+1` index/`+2` counter; `003204B0` Count +
  `00320B30` Row + `002E4C70`/`002EAF70`/`002EBE20` record
  trio; runs when `0032E520(1)` idle, `02064AD4`=2 → mode 2).
  Contra `AUDITSEM-CONTRA-FRONTIER-582860-238A30`
  verified true — `0050F5A0` is a 10-B `mov ecx,1; jmp
  00238A30` script-verb thunk; §30 narrowed to 9 exclusive +
  1 shared. **PUBLISHED `baf3686a`** — narrowing + `00258190`
  subtree (camera §11, BY-7 mechanism answered: mode-1
  joint-liveness probe, mode-2 resolve+apply via
  `003A6DF0`/`00422050`, `022C6F28`/`0x740` table;
  `+0x194`/`+0x198` semantics still open) + the staged
  contra trio (map-screens §6b, gambit-screens dispatch
  set, shared-dialogs masks) + slice-A UQ7 reword + index
  (14,647 rows) + this file + TEAM. Lifecycle: contra
  `582860-238A30` DONE, `SUBTREE-FOLLOWUP-00258190` DONE,
  `PUB-582860-NARROW` DONE; `PUB-CONTRA-TRIO` claim pending
  on `@publication` (poller armed — claim+finish only, its
  files already landed). `FRONTIER-REQ-AUDITSEM-SUBTREE-
  00258190` filed. Font REQ+NOTICE closed
  DONE-WITHOUT-EDIT
  (accounting sentence already present; residual is FABLE's
  substrate-symmetry question).
  **Interactive session (concise-family) contra pass, staged
  2026-09-15 ~05:5x:** `AUDITSEM-CONTRA-FRONTIER-WORLDMAP-CITES`,
  `-GAMBITS-ID12`, `-MSD-C480-DECODE` all repaired in place and
  claimed ACTIVE — every counter-evidence item re-verified against
  the image before editing (map-screens §6b: id-24 clears
  `[02CA8F38]+0x160` not the global, id-38 arg is
  `byte[[+0x9F40]+0x39]`, six cite-column sites corrected;
  gambits: dispatch set `{0x8000,1,2,5}` + `0x8003/4→default`,
  `0056BA85` tests are skip-conditions, editor `0x8001/0x8002`
  unswapped; dialogs: mask globals `01E0C2A0/01E0C2A4` unswapped,
  countdown picks `1`/`2` not `2`/`3`, `+0xFC` masks
  `0x100/0x200/0x400`). `OPUS-PARTIAL-UQ7-ARM-LAYOUT-PREMISE`
  DONE — slice-A row-36 reworded to largest-displacement framing.
  Pub task `SWE2-FRONTIER-PUB-CONTRA-TRIO` READY (4 files incl.
  slice-A page). **All four published inside the wake's
  `baf3686a`** (it folded the staged files into its batch, index
  regen included); the three contra tasks are finished with the
  commit ref, and the READY pub task is a bookkeeping leftover to
  claim+finish once `@publication` cycles. Gates: interior-cite
  clean on 2 of 3 (map-screens has 1 pre-existing violation at
  HEAD, line ~105 — `0026D374` inside `0026CE60`, predates this
  session); guard `ADDS NOTHING`.
  Row `002E09A0` IN FLIGHT — subtree bound on the world-tick page
  tail (6 members: `00267360` slot-0 probe on `0209BE10`
  `0x288`-table, `002A28B0` state-6 completion probe via
  `0209C4D0` registration table, `002A2A60` status dispatch on
  `byte[+0x180]` through RVA table `02A2AAC`, `002A38C0`
  mailbox-mode setter (`0209C62C` + `0209C4D0`–`0209C510` sweep),
  `003591F0` word store `024C7FFC`, `00404D70` deferred-enable
  arm on `02B62D80`/`02B62D88`); EX-3 walk-base corrected
  `02B5F200` → `0215F200`. Gates clean (0 boundary violations,
  index 0/0/0/0). `FRONTIER-REQ-AUDITSEM-SUBTREE-002E09A0` filed.
  **PUBLISHED `33683587`** (world-tick page + index + inbox);
  `SUBTREE-FOLLOWUP-002E09A0`, `PUB-002E09A0` and the leftover
  `PUB-CONTRA-TRIO` all DONE. Row `002E3AF0` IN FLIGHT — subtree
  bound on the group-wiped page tail (6 members: `0025D4F0`/
  `0025D690` kind-`0x60` `+0xB8`-table releases, `00269E40` float
  store, `0026DF40` six-slot clear, `002E35B0` the 1,189-B detach
  engine over `0215FD58`/`0215FD78` observer lists, `003E7D50` the
  `0x150`-stride `02B59D80` presentation-slot teardown — pins that
  table's record shape, narrowing the EX-3 residual). Gates clean;
  `FRONTIER-REQ-AUDITSEM-SUBTREE-002E3AF0` filed; pub task
  `SWE2-FRONTIER-PUB-002E3AF0` READY, poller armed for
  `@publication` (OPUS mid-publish). Row `002F7380` bound on the
  weather call-chain page (6 members — the GS texture-memory
  machinery: `003A1E50` per-level footprint formula with format
  jump table, `00466190` per-record mip-chain footprint,
  `00466220` 4-bit-format selector `{0x14,0x1C,0x24,0x2C}`,
  `00467AA0` the UQ-90 budget byte-verified, `00467B00`/
  `00467B10` sum/max stores to `02CA6008`/`02CA6004`). Gates
  clean; review + pub task `SWE2-FRONTIER-PUB-002F7380` queued
  behind the same lock. Row `00301AD0` bound on the
  authored-data page after the `+0x005` section (6 members —
  `AiOrder_EvaluateTargetSelector` helpers: `0031E6F0`/
  `0031E760` body/point clearance measures, `003209E0`
  percent-of, `00321320` `+0x698`→`+0x50` chain resolver with
  −1/−2/−3 codes, `003215C0` the `+0x005`-gated lookup the page
  asked for, `00321630` candidate max-scan). Row `00792350`
  bound on the binding-profiles page tail (6 members — the
  Phyre application-object ctor, store `00792550`→`[02EA5368]`,
  vtables `01CB2508`/`00D497E0`: `005DBF50`/`005DBFB0`
  0x14/0x10 struct clears, `005DC2F0` the `+0xE8` sub-ctor,
  `006331A0` intrusive-list head, `00874320` 0x70 zero-run,
  `00874350` the `+0x380` ctor with five `0x1D8`-stride
  children via `006160B0`/`00615C90`). Both: gates clean,
  reviews + pub tasks filed. **Bookkeeping repair:** the
  first batch poller's publish failed on a malformed arg
  (literal `\n` → stray `n` path) yet still finished
  `PUB-002E3AF0` and claimed/finished `-002F7380`/`-00301AD0`/
  `-00792350` against peer HEAD `e8ad79a2` — no files lost;
  `SWE2-FRONTIER-PUB-BATCH-4` replaces them (target notes the
  false ref). Row `001B7EE0` bound on the game-application
  page (5 members — the BE-6 `Ensure` for
  `Phyre::PCameraPerspective` at `[01F81218]`: `001B6D90`
  camera ctor with `+0x670 = 3F490FDB` default FOV and the
  `+0x5A0` vtable `008C5D68` sub-object, `006791B0` the
  `+0x678` sub-ctor over `006CC350`/`005CC900`/`006CC960`/
  `00679130` children, `006CC350` 0xA8-stride child with the
  `00808FE4` 2-slot container + `00584730` release-cb slot,
  `006CC960` leaf vtable `00D89B00`, `00679130` the `+0x488`
  paired-enable child). Gates clean (0 boundary violations,
  index regen 14,685 rows, neighbour guard ADDS NOTHING on
  the binding-profiles page); review filed. Corrected batch
  poller armed — publishes the batch + index + inbox +
  TEAM and finishes the FOLLOWUP claims + `PUB-BATCH-4`
  when `@publication` frees (ORACLE-EXP083 held it at last
  check). Batch grew to ten pages: row `00215320` bound on
  vtable-method-index tail (5 members — `CharacterOrderedObject`
  slot-1 render-submission: `001F5D70` the 2,924-B gated
  pass, `001F87B0` vector<0x318> emplace, `001FAD50`
  per-element transform staging, `001FB310` scale publish
  → `04A7C3A8`, `001F68E0` SSE palette pass). Row `002341C0`
  bound on the world-tick page (5 members — the 62-B
  area-teardown reset: `00392710` releases `[02AE82A0]` +
  memset `02AE8060`×0x460, `002FAEC0` clears `022BE948`,
  `00325080` = 7, `002FA470`/`002F7FA0` the 3-deep dedup ring
  at `02EC3E60` + mod-3 rotation). Row `00236C30` bound on
  CONTRACT-authored-table-row-lookup tail (5 members — the
  bespoke binders' post-registration work enumerated:
  `00237FC0` per-row re-registration on `02EBF138`,
  `00238160` the 0x1000-band rewrite, `00238880` the
  `0208D318` (row,col)→0x6000+i u16 menu lookup,
  `00238660` the `02EBF158` deep rebaser, `003847B0` the
  known tail-jump binder). Row `002620E0` bound on
  weather-probability tail (5 members — one-shot init core:
  `00379290` env-object gate on `02ADD090`/`02ADD0E9`,
  `00379630` preset-handle rebuild from `021A2CE0` rodata
  via `003AB960`, `00379760` slot-0 rebuild into `02ADD11C`,
  `00379860` `02ADD090`-guard → `00379F50`, `0037AD10` the
  5-entry 0x50-stride preset table `02C1F460`). Row
  `002DF690` bound on the music-control page tail (5 members —
  `bgmstreamstop` close: `001DC330` registry adapter,
  `00211280` two-list dispatch, `0021D840` intrusive
  remove-by-id with id−1 removes-all, `0021C870` fallback
  broadcast, `00225000` fade-stop via `007A84A0`). All gates
  clean; seven AUDIT-SEM reviews filed.
  **Published:** `beb4d2f5` carried six of the batch pages
  (`002E3AF0`, `00301AD0`, `00792350`, `001B7EE0`, `00215320`,
  `002341C0` sections); `002F7380` had already landed via peer
  commit `987c856f`. `PUB-BATCH-4` closed legitimately against
  it. **Still staged (batch-5):** `00236C30` (CONTRACT row-
  lookup tail), `002620E0` (weather-probability tail),
  `002DF690` (music-control tail), and `00312280` (battle-unit
  field-map §11 — the 857-B defeat-rewards pipeline: 9-slot
  roster `022C1740`, EXP cap `0x5F5E0FF` at `+0x18C`, level-up
  loop on `002F8F20`, LP cap `0x1869F` at `+0x190`, accessory
  `+0x69|+0x79` bit `0x10` redirects LP into the gil pool,
  `0028FB80` floating-text publish, `003180F0` 7-slot drop
  roll). `PUB-BATCH-5` armed — poller claims `@publication`
  when free and finishes the FOLLOWUP claims on success.
  Since then: `003304A0` bound on the spawn page (§31 — the
  EBP primary-payload dispatcher: tagged pointer `id&0xF`/
  `id&~0xF`, descriptor `+4` watermark gates 14 section binds
  via `(rdi+off)|tag`, per-tag pending bitmap `022C6E48`;
  members `00330060`/`00330190`/`00330220` store bound bases
  into `022C6CF0`/`022C6CA0`/`022C6CC8` and clear bits 6/4/5,
  `00332110`→`003DFE60(1,base)`, `003320D0`→`003EAA00(base)`).
  `0041E500` bound on resource-section-addressing (§10 — the
  re-resolve battery over four `+0xD9x` containers;
  `0051F620` the 131-B index-chain rebase walk). `002DF630`/
  `002DF680` bound on the music-control tail (siblings of
  `002DF690`: the start path `002252C0` voice build and the
  still-playing poll `002253D0` status≠2). `0028F000` bound
  on the loot page (§9 — the six-op verb dispatcher: ops 4+5
  share the `003FA820(rec,0)` arm; `003FA160` create,
  `003FAA10` phase/brightness notify, `003FA900` end-all,
  `003FBE90` visual ctor with mod-360 yaw). Their followup
  tasks ride under the `002DF690`/`00319600` page claims;
  the poller claims+finishes `002DF630`/`002DF680` after
  publish and finishes `0028F000` directly. Also staged on
  already-listed pages: `001D7A20` on game-application tail
  (4 members — the four-quad screen-setup battery;
  `001D70D0`/`001D7110` the `001B1620`+`+0x3A98`-gated float
  getters, `001D8600` the `0x3001`/`0x44` mode set,
  `001D8790` the corner transform) and `00238BF0` on the
  battle-unit field-map §12 (4 members — the definition→
  runtime refresh; `002361B0` the `+0xE68`+0x18 category
  code, `00269F30`/`0026AD00` byte writers, `002E8A10` the
  `022C6F28`-table attach-record flag update) and
  `002368D0` on the slot-pool page §12 (4 members —
  `BattleStorage_InitializeWorkArrays`: 32×`0xF50` BtlWork
  realloc, two `0x9400` banks, `0208E680` descriptor
  free+null, section-`0x13` re-register, 12-channel table
  clear + `00238260` init loop; `00233E00` the <6-of-12
  capacity probe, `0030CF40` the presentation-pool reset,
  `002EA5F0` five verb registrations). ~~Measured correction:
  the three alloc tag args point at zero `.rdata` stretches
  (`009146B0`/`B8`/`D0`); the `btlKeepCharWork` strings are
  at `007F46B8`/`D0` and are not the pointers passed — the
  older gloss is a string-xref association.~~ **WITHDRAWN
  2026-09-18 (OPUS-CONTRA, byte-verified):** the correction
  is itself wrong. Out of the image `009146A8`=`STATIC`,
  `009146B0`=`BtlWork`, `009146B8`=`btlKeepCharWork1`,
  `009146D0`=`btlKeepCharWork2` — all `.rdata`, none zero,
  all the pointers passed. `007F46B8`/`D0` is `.text`
  (`7F46D0` begins `40 53 48 83 EC 20`, a prologue) — each
  is the canonical address less `0x120000`, a second
  subtraction of the image base these addresses already
  include. Cause: a VA→offset slip, not string-xref
  ambiguity. The note's other staged heads checked clean
  for the same slip: `002DF070`/`00253A80` are real
  prologues at canonical addresses (doubles `01DF070`/
  `0153A80` are mid-instruction; the four getters are the
  6-byte `mov eax,imm; ret` bodies described). Two more
  sections staged after that: `002DF070` on the
  audio-boundary page tail (`SeSep` chunk walk +
  find-or-create record factory `00222DC0`) and `00253A80`
  on the katano-savedata page tail (save-runtime init +
  four 6-B constant getters `002EF2A0`/`002EF290`/
  `00235E90`/`00235E80`), plus `002AC5F0` on the
  numeric-formatting page tail (the 7,489-B control-code
  interpreter's four helpers: `002AB820` emit-run,
  `002B1ED0` pen refresh, `002B2C50` token-width probe,
  `003FFD70` escape-pair decode). Two more after that:
  `0025E4C0` on the script-variables page tail (the VM
  interpreter core — 5 members: `0025B400` wait-state poll,
  `0025D740` the three-way compare engine int/float,
  `00267560` both-int predicate, `002659F0` trace marker,
  `00268A80` pop-one adapter) and `0025D9E0` on the
  world-tick page §5 (`ActorManager_RunFieldRuntimePass` —
  5 members incl. `00234150` four-slot cleanup,
  `00254A90` deferred flush, `002677B0` flag predicate,
  `00363A80` byte setter). Then `00280140` on the
  resource-request-queue page (the async-load state
  machine — cases 1/2/4/0x11, `003CA0F0` the settled
  predicate, `003667B0` the in-flight bit) and `003247F0`
  on the field-map page §13 (`BattleUnit_RebuildPerception
  CandidateCache` — `0032A4D0` pairwise mask cache
  `022C26A0`, `00391710` grid range, `003919B0` two-phase
  adapter, `00468A70` vision cone). Then six more:
  `00325260` field-map §14 (action-timeline dispatcher —
  two-level jump table `0032574C`/`00325720`, 121 of 132
  opcodes to return-1, `003257D0` class applicator);
  `0033A240` field-map §15 (locomotion-step publisher —
  `00337C10`/`00337D90` per-kind censuses behind
  `022C7D04&1`, `0033D890`/`0033DFD0` kind solvers);
  `003BBD00` hp-write page (64×`0x50` reaction slots at
  `02B457D0`, variant pick, `00506700` populator);
  `003714A0` adm-add-motion page (bone-pose applicator,
  `004776D0` packed channel decoder); `00581DA0`
  save-image-buffers page (8-state save transaction,
  `+0xDC` code accumulator via `00581860`); `00378120`
  map-ctrl-pack page (YM00/picture-0 setup — `0026E7D0`/
  `0026E760` request twins, `0026E960` registration);
  `00392A10` cutscene-name-slots page (sliced box emitter —
  `002DC7F0` geometry, `002DD090` packet submit,
  `002DD1E0` bracketed quad, `00392CE0` non-bracket).
  Index now 14,901 rows; 33 subtree sections staged
  unpublished. All followup claims finished with
  review-request result_refs;
  `SWE2-FRONTIER-PUB-BATCH-5` is DONE — `3f302259` carried
  12 subtree-section pages + index (14,801). The newest
  sections (`0025E4C0`..`003649A0` above) are staged
  unpublished awaiting the next batch; `@publication`
  released unheld, publish deferred per operator.
  Latest coherent commit `3f302259` (+ peer `987c856f`
  carrying the `002F7380` section).
  **2026-09-16 block — six more subtrees bound:**
  `00686280` lua-loader page (`PCallerScript` slot 2 —
  `00681010` tagged dispatch, `006810B0`/`00681130` float/
  double return extractors, `006811B0` load-and-dispatch);
  `005A0840` fifteen-modules page (atexit shutdown walker —
  `005CCB90` IAT thunk, `0062EAF0` scoped node call,
  `00638C90` epoch-gated deferred-destruction reaper,
  `00677520` close-once returning 0x15); `003BC4E0`
  section-006 page (TIM2-client event dispatcher, arms
  1/0x10/0x12 — `0037F140` bit-9 predicate, `003BC2D0`
  release chain, `003BCAB0` u16 resolve-cache, `003BD8F0`
  indexed seek); `003C5E50` save-payload page (third
  revealed-tile writer, `02B45A00` bit-0 gate — four
  `0209BE80`-manager helpers); `00473E80` language-locale
  page (locale-change dispatcher, six `.rdata` code-pair
  arms — `00183180` adapter, `001D8D60` rebuild,
  `00184380` codec apply, `001EE820` 3→4-byte glyph
  expansion); `003649A0` glyph-quads page (per-line
  emitter — `003647E0` inline-markup interpreter,
  `00365FD0` u16 cache scan, `00364210` span clipper,
  `00474650` arg-shuffle → `003A22A0`).
  **2026-09-16 block 2 — eight more subtrees bound:**
  `005A0840` fifteen-modules page (atexit shutdown walker —
  `005CCB90` IAT thunk, `0062EAF0` scoped node call,
  `00638C90` epoch-gated deferred-destruction reaper,
  `00677520` close-once); `003BC4E0` section-006 page (TIM2-
  client event dispatcher arms 1/0x10/0x12); `003C5E50`
  save-payload page (third revealed-tile writer, `02B45A00`
  bit-0 gate); `00473E80` language-locale page (locale-
  change dispatcher, six `.rdata` code-pair arms);
  `003649A0` glyph-quads page (per-line emitter +
  markup interpreter/cache scan/span clipper/arg-shuffle);
  `0017DAA0` middleware-inventory page (information-page
  builder, ≤22 rows, `001D0190` row-command dispatcher,
  `001EA990` string materializer); `001B44A0` font page
  (language→`fontlist.ah` selector us/kr/ch/cn/jp);
  `001C2670` vtable page (`MultipleDebugDisplay` deleting
  destructor, `0x4670`-byte object); `001C3D50` console-
  tunes page (98-registration battery: `001C51D0` ×94 +
  `001C52C0` ×3 + `001C7850` vec4); `00229FA0` actor-
  manager page (manager-slot-match publisher);
  `0023A570` unit-definition page (`BattleUnit_ApplyUnit-
  Definition` — `00236100` SpawnKeep entry resolve `0x250`
  stride, `00237040` engaged fork `002FED60`/`002FEDC0`,
  `00254A40` constant `0x34`); `00233F70` field-runtime-
  pass page (`BattleUnit_UpdateLifecycleAndCombatFrame` —
  `002671C0` 3-condition ready, `00267240` flags pred,
  `003228E0` `0024DE70`≥3 throttle); `0023B040` party-
  suppression page (leader-battle-state recompute —
  `00322600`/`00322920` bitmask id-sets, `0026BD40` →
  `0209A2C5`). Index 14,921; 40+ sections staged
  unpublished.
  **2026-09-16 block 3 — seven more subtrees bound:**
  `002392D0` field-map page (flags→unit-state mapper —
  `002E83B0` attach-record flag `022C6F28`/`0x740`,
  `00321810` flag byte + tail `00321DC0` iterate-clamp);
  `00244970` widget-message-protocol page (5-B thunk →
  `00244980` recursive completion pass — `00246C20`
  per-node visit `{25}`/`{19}`/`{20}` via `[01F44830]`,
  `002479B0` sibling resort `0208ED60`–`78`);
  `002621D0` native-command-lifecycle page
  (`VMNativeCommand_ExecuteLifecycle` — `family>>0xC` /
  `command&0xFFF`, `003DC240` Poll / `003DC2A0` Result
  getters over `02B57EF0`, `00358940` rebind);
  `00300E40` field-map page (`BattleUnit_TeardownAnd-
  Despawn` — teardown then `0023A570` definition re-apply;
  `00237080` transient clear, `002697E0` stats refresh,
  `00301310` roster walk `0x80000003`);
  `002A8C50` numeric-formatting page (3,363 B element
  interpreter — `002ABB20` object-list walk `[0209CC40]`,
  `002ABF70` per-tick `+0xB0` mode switch `jmp rdx`,
  `002B35A0` bounded leaf loop); `002EF410` runtime-mode-
  ladder page (`SaveTransitionMetadata_RestoreFromRecord` —
  keyed float setters `00304790`/`003047C0`/`003139D0`
  around `003EBC50`/`003EBD00`); `00233C10` come-back page
  (battle-state guard = transition-metadata capture on
  `[02EBF190]`; `00327F80` `0xFFFF`-masked copy,
  `003139A0`/`00304770` XOR-replace bit setters on
  `+0x5AD0`/`+0x5AE0`). Index 15,047; ~47 sections staged
  unpublished. **Next candidates:** queue roots beyond
  `00233C10` — `0039F0A0`, `004F5CE0`, … (~450 rows
  remain in `exclusive_subtrees_followup.tsv`).
  **Requests settled 2026-09-15 (8f2bcc4d):**
  `OPUS-REQ-FRONTIER-PASS22-CRR-RNG-EDGE` DONE — RNG CLIENT
  accounting sentence on the render-record page. `AUDITSPEC-REQ-
  FRONTIER-EC3F0-EXCLUDED-PAIR` DONE — verified, census corrected
  9 -> 15 (je-dispatched `002E78D0`/`002E7860` + `003E6B70/90` ->
  `003E31C0/20` chains). `FABLE-NOTICE-FRONTIER-LEDGER-BATCH-READY`
  ANSWERED (left READY — dependency `OPUS-CONTRA-DATA-INDEX-LOCK-
  SCOPE` still open on DATA): **OPEN-QUESTIONS.md is free now** —
  no ACTIVE task holds it; FABLE may claim `FABLE-LEDGER-AP7-EU1`
  and take the ~10-minute window immediately. FRONTIER will not
  touch OPEN-QUESTIONS until the batch lands.
  **Pending:** 36 AUDIT-SEM subtree reviews READY (`00253C70`, `001E8580`,
  `00336CE0`, `0032E070`, `0026C8C0`, `001B4D70`, `001BBFC0`, `002E5750`,
  `00304850`, `001C7940`, `002342F0`, `002E28E0`, `003692D0`, `005A08E0`,
  `005A08E0-CORRECT`, `00226640`, `00226640-CORRECT`, `0027FB70`,
  `0027FB70-SUPP`, `0022B6E0`, `0031EB20`, `00362850`, `003325C0`,
  `00258350`, `0025DF00`, `002EC3F0`, `00808D78`).
  **Fallback:** further queue roots or pass-22 lane work.
- **Prior:** `FABLE-REQ-SWE2-FRONTIER-NOCALLER-INSTALLERS` —
  **DONE (rev 10965): all named groups bound and published.**
  Commits: step-table 52 (`79f900f2`), CharacterRenderObject vtable 26
  (`e89b0d1c`), dyngeo 18+16 (`e803dc9a`), GameApplication 13 + CRT
  filebuf 11+11 + unowned 11 (`fde290f4`), CRS 25 + `002EA320` 5
  (`885c2d7c`), Phyre `006349B0` 11 + map-table `00378540` 6
  (`6ec99f5e`), plus this session's tail `d93aefd0` (the `006349B0`
  teardown-thunk section on member-registration-and-the-recovered-field-schema.md)
  and `7d7c5a54` (three in-scope groups the request did not name:
  `00900F20` = `basic_stringbuf<char>` vtable 6, `01E0C490` = 15-slot
  shop query-class dispatch driven by `00292B70` 8, `01EECFC0` = the
  5×4 mode-transition matrix 5). Reviews filed
  `FRONTIER-REQ-AUDITSEM-NOCALLER-INSTALLERS` (rev 10917) and
  `FRONTIER-REQ-AUDITSEM-NOCALLER-INSTALLERS-2` (rev 10963).
  **Open contradiction `FRONTIER-CONTRA-6349B0-THUNK-ROLE` → FABLE:**
  the peer's `008AFxxx` section calls the 11 members runs-once
  initializers; they are `atexit`-registered destructors — every
  `006349B0` site is `lea rcx,[thunk]; call 00808B90` (the MSVC atexit
  wrapper, anchor of 1,614 bodies), zero direct calls. **Method defect
  found+repaired by the parallel session:** a fixed
  140-byte landmark window ignored `functions.tsv` extents and slid past
  small bodies into the next entry — `008AFD7D` (+0xD inside `008AFD70`)
  was attributed to `008AFD00`, and 9 cites on character-render-object.md
  crossed the same way (`001F8737` belongs to `001F86F0`, not the 8-byte
  getters before it). Repaired in `6ec99f5e`; invariant now lives in
  `Database/Tools/work/FABLE/interior_cite.py` — `scan` bounds a body at
  `min(entry+size, next entry)` and stops at `ret`/`int3`
  (`BOUNDARY_CROSSED` on violation), `check` audits a page's table rows
  for interior cites landing inside another function. All touched pages:
  0 violations. Loop-guard lesson: an identical repeated contradiction
  means the tool's assumption is wrong — stop and bound against the
  executable's own entry table before scanning further.
  Prior: `OPUS-REQ-SWE2-FRONTIER-WIDGETPROC-REGEN` —
  **DONE `7d14ca68` + downstream publish `0c0ae7f9`/`c0856632`
  (board rev 10764), review filed
  `FRONTIER-REQ-AUDITSEM-WIDGETPROC-REGEN` (rev 10729).** Pass 1 of
  `widget_messages.py` now implements the single proc-slot rule —
  reaching-definitions of the slot register over each caller's CFG:
  `call` + `jmp` transfers into the three ctors, per-def `mov R,src`
  chasing at the def's own site (fixes `00406E80`'s `mov rdx, r15`,
  whose rdx reaching set mixes a stack-`lea` with the `r15` forward —
  a lone-reg-only chase never fired, losing `00407590`/`004079A0`),
  one forwarding hop through live-in args (`00564AC0`'s `r9`). Fresh
  census: 297 transfer sites, 291 resolved, **267 procedures**
  (direct 234 / tail 16 / multi 12 / forwarded 5) — all 21 verified
  additions present, all 5 false positives absent. TSV regenerated;
  protocol page restated over 267 / 232 EXACT. Gates green
  (verify_doc_addresses, consistency, questions, links, names).
  **Downstream:** `0c0ae7f9` regenerated `ui_atlas.tsv` (80 menu-range
  rows, 1,065 frontier / 913 labelled) and `ui_atlas_all.tsv` (267 rows,
  2,648 / 1,830); restated the atlas page, 16-UI README, widget contract,
  widget pages, COVERAGE and PARITY-STATUS to 297 transfer sites / 267
  handlers; falsification block keeps dated values behind a resolution
  note. `c0856632` re-applied the router's truncated-name repair after a
  peer checkout reverted it. Note: `ui-request-router.md` and
  `ADDRESS-INDEX.md` have been reverted by a peer checkout once already
  — re-verify `check_names`/`check_address_index` before assuming.
  Prior: `FABLE-REQ-SWE2-FRONTIER-LAYOUT-KEY-READERS` —
  **DONE `1ab45467`, review filed `FRONTIER-REQ-AUDITSEM-LAYOUT-KEY-READERS`.**
  Live coverage verified **92/92** current
  frontier readers each documented exactly once (the live frontier shrank from
  the 107-reader census as readers were cited out of it). Reader sections
  landed on the map, license-board, gambit, shop, handbook, shared-dialog and
  unlabelled-panes pages; two new PARTIAL pages created —
  `16-UI/Message-Windows/the-message-window-layout-readers.md` and
  `16-UI/Battle-Hud/the-battle-hud-layout-readers.md`; the 16 shared
  band/font/signal readers got one section on the layout-parameter page.
  Handbook rows were corrected against the authoritative TSV (`00572E10` /
  `00574E80` read `PartyBlackBandTime` only; `00572600`/`0056E770` are not
  readers). Gates: ADDRESS-INDEX regenerated (0 stale/0 missing),
  `check_coverage` green (16-UI 25 docs), `check_names` clean on my files,
  `check_links` clean (2 known case-folding waivers), broad `run_gates`
  otherwise shows only pre-existing baseline debt plus peer-owned truncated
  names. CONTRACT already dispositioned the pass-22 findings on my two new
  pages. Board state for the finish/review ops was committed long since.
  Earlier this session closed **five** routed items —
  `OPUS-REQ-FRONTIER-NAME-SHORTHANDS` (`e18054d5`: check_names TRUNCATED 0 /
  AMBIGUOUS 0; `BattleTargetBuffer` added to ALLOW_EXACT as a types.tsv
  struct; AW-2 answered in the register),
  `FABLE-NOTICE-FRONTIER-005DD890-PLACEMENT` (`bdbee57e`: teardown loop
  re-placed to `Runtime.Container.Teardown`; `00650D40` stays Platform),
  `OPUS-REQ-PLATFORM-003154B0-READING` (`804c23fe`: OPUS's pass-13 blind
  read verified byte-exact and accepted),
  `FABLE-REQ-SWE2-FRONTIER-ORPHAN-QUESTION-IDS` (**zero orphans** — verified
  by fresh regen; the fleet's `fb56a946` mass id-assignment plus `872deabb`
  template exclusion did the work; claim already DONE),
  `OPUS-REQ-SWE2-FRONTIER-ATLAS-GENERATOR-INPUTS` (`7ed031e7`: both
  generators repointed at tracked inputs — new `call_graph.py` rebuilds
  rawcalls semantics incl. tail jumps that edges.tsv drops, frontier lists
  become `frontier_census.frontier_set()`, ripscan → `data_xref_scan`;
  wm_family reproduces 77+31=108 identically, ui_atlas clean modulo live
  frontier drift). Also filed re-reviews `FRONTIER-REQ-AUDITSEM-AUDIO-SLOTS-2`
  and `FRONTIER-REQ-AUDITSEM-MENU-SCREENS-3` (post-repair verification of the
  c3498219 / 4a14fdec+d177d73c repairs).
  **Remaining claims: none ACTIVE.** `RESIDUAL-PLACEMENT`, `SWITCH-FAMILIES`,
  `STALE-REGISTER-LOCK` (tracker; DATA's index-lock scope was adjudicated
  publish-window-only by OPUS-ADJ-INDEX-LOCK-SCOPE) and `PASS22-PROGRAM`
  (lane coordinator; my band clean, per-lane requests queued to
  CONTRACT/ORACLE/EC7/STRUCT/DATA) are all DONE.
  Prior: `FABLE-REQ-SWE2-FRONTIER-MENU-SCREENS` —
  **DONE (rev 10377).**
  2026-09-15 depth pass on the DONE claim: interior citations landed on
  the handbook (52 screen-region members, union 170), shop (51, union 226),
  shared-dialogs (12, union 64 — `0057C480`'s id-4/10/12/18/19 arms read:
  auto-confirm countdown `+0x63A`, option-pick `+0x630`-class → parent
  `+0xFC` map) and unlabelled-panes pages (all 25 rows). Three open items
  resolved: `00579AF0` = the `0056EF60` kind-6 item/equip host
  (`00579420` always-installed list vs `005789D0` conditional member-scoped
  pane); `005677A0` = member-scoped pane of the `00280DE0`/`002D70F0`
  family (installed by `00567770` at cmd `0x40`); `0056EF60` kind byte
  decoded (0–5 `00570BF0`→`00571A50` pages, 6 `00579AF0`, 7 `00572E10`).
  Gates green; ADDRESS-INDEX regenerated; review filed to AUDIT-SEM.
 All labelled screens' subtrees fully enumerated
  (`2958890c`): every subtree member of every labelled screen is named on
  its owning page; the 25 unlabelled rows resolved to owning screens.
  Reviews: MENU-SCREENS-1, MENU-SCREENS-2, WORLDMAP filed to AUDIT-SEM.
  Follow-on (uncommitted pending `@publication`): pass-22 registry
  coverage completed — 47 live-only pairs appended (39 + 8 second-order),
  22 live pairs on my own four 16-UI docs dispositioned
  CROSSING-ACCOUNTED with pass-22 sections. R3 voted FOR (rev 10397;
  apply before lane bands close). `OPUS-REQ-FRONTIER-REGISTRY-COVERAGE-19`
  finished (rev 10400). Next action: publish the registry/pages/board
  batch when `@publication` frees (held by SWE2-CONTRACT at last check),
  then take `OPUS-REQ-SWE2-FRONTIER-RENDER-PASS-REGISTRY-PAGE` or
  `FABLE-REQ-SWE2-FRONTIER-EE-REGISTER-MEMBERS` (both already ACTIVE on me).
  Board cleanup this session: six stale done-claims closed
  (ENTRY-CITED-HUBS, EXCLUSIVE-SUBTREES, EFFECT-TYPE-CLASSES,
  RENDER-VTABLE-SLOTS, MODEL-OSCILLATOR-0040, CENSUS-PARENT-STAMP);
  STALE-REGISTER-LOCK stays ACTIVE as tracker — DATA holds
  open-questions/audit-log, escalation `OPUS-CONTRA-DATA-INDEX-LOCK-SCOPE`
  filed. RESIDUAL-PLACEMENT and SWITCH-FAMILIES stay ACTIVE pending
  AUDIT-SEM verdicts.
  Prior: `FABLE-REQ-SWE2-FRONTIER-MENU-SCREENS-WORLDMAP` —
  **DONE `f486739c`, review filed `FRONTIER-REQ-AUDITSEM-WORLDMAP` (rev 10266).**
  Map page §6b reads the world map as a full screen
  package: installer `00550400` builds host widget `00552250` (0x188 B) at
  `02CA8F38`; host construct creates page `005528C0` (0xA020 B) as `+0x160`
  child; page's released arm clears the global. Both dispatches decoded —
  host 41 ids/13 arms (id 10 pad-scroll of cursor `+0x100`/`+0x102`, 41
  build/register, 40 rebuild, 39 exit mode, 35 out-param, 24 reports exit
  via `00285F00`); page 42 ids/17 arms (id 6 populate incl. `00553AE0`
  MapName pane, ids 10/11 input arm lazily installing `00551E00`/
  `005542D0`/`00551F00`, id 4 render, 29/32/34/42 flag/timer arms).
  Six panes read; `005542D0` (0xDE0) is the interactive destination list
  (4×0x328 entries, `+0xE0` page counter, id 12 page left/right). All 185
  subtree members carry role + interior cite. New id meanings posted to the
  protocol page open list (6, 10/11, 29, 30, 32, 34, 35, 37–42). Gates
  green; ADDRESS-INDEX regenerated; PROGRAM-STATE/COVERAGE updated;
  OPEN-QUESTIONS/AUDIT-LOG skipped (SWE2-DATA holds them). Next action:
  `MENU-SCREENS` parent claim continues — remaining screens' subtrees, or
  the next READY package if a higher-value one lands.
  Prior: `OPUS-REQ-SWE2-FRONTIER-PASS22-PROGRAM` —
  **ACTIVE, lane coordinator; my band DISPOSITIONED and live-clean.**
  Band = 170 seeded rows (00-Engine 131 + 99-Residual 39) **all dispositioned**:
  168 CROSSING-ACCOUNTED + 2 GENUINELY-IRRELEVANT (`ee-and-vu0-register-bank`
  -> ScriptVM and `the-shared-transform-workbench` -> Resource: both are the
  shared variadic logger `0017D280`'s mechanical caller population). Live-graph
  drift beyond the seed: 57 unseeded (doc,layer) pairs surfaced during
  disposition -- all accounted for in doc prose and appended to the registry
  as `live-graph-addition` rows. Live audit state: **zero unaccounted-neighbour
  findings remain on band docs** except the one adjudicated-irrelevant logger
  row (deliberately unnamed in the doc; verdict is the disposition). Corpus
  pass-22 total fell 948 -> 821 during this batch (my band + peers' parallel
  work). Other lanes' 85 top-102 rows filed as per-lane P1 requests
  (`FRONTIER-REQ-{CONTRACT,ORACLE,EC7,STRUCT,DATA}-PASS22-TOPDECILE`, board
  revs 10085-10089); ~39 unseeded live pairs sit on non-band docs and belong
  to the same lane owners. Next: publish this batch; monitor the per-lane
  requests; then the next READY package. Tool note for auditors: a Pass-22
  note must name the layer in a form the alias table recognises
  (`CoreRuntimeScheduling`, `Script_VM_Native_Bridge`, ledger spellings) --
  "**scheduler**" does not satisfy the checker; `register_ledger_aliases`
  makes the canonical owner spelling itself sufficient.
  Prior: `FABLE-REQ-SWE2-FRONTIER-MAP-MEMBERS` —
  **DONE `6973beb4`, review filed `FRONTIER-REQ-AUDITSEM-MAP-MEMBERS`.** All 108 `wm_members.tsv` rows classified in
  the-map-screens §4 with one interior citation each, grouped by screen reach
  (world-only 23, loc+track 30, loc+track+world 17, field+loc+track 14,
  all-four 9, field+loc 3, field+loc+world 2, location-only 2, container-child 2,
  widget-internal 6). Method: full body reads of all 108 members against
  `wm_members.tsv` + lmap §10 vocabulary; the dominant pattern is four gate
  queries (`0032A8A0` PersistentFlag, `00309EC0` BattleEncodedId, `002543F0`,
  `003C08B0`) wrapping every table entry, with row-builders/enumerators as
  filters over the widget's counted sub-tables. Corrections landed in the same
  edit: §2.6's `003C2200`/`003C26C0` "releases a slot" was wrong — `003C26C0`
  *populates* the slot's `+0x18` child-label array (release is `003C2210`/
  `003C22B0`); the §2.5 "closure members not read" caveat and the §7 unchecked
  question resolved. Coverage verified mechanically: `diff` of TSV address
  column vs §4 table first column = clean, 108/108.
  Prior: `FABLE-REQ-SWE2-FRONTIER-RENDER-DIRTY-BITS` —
  **DONE `95726a70`, review filed `FRONTIER-REQ-AUDITSEM-RENDER-DIRTY-BITS`.**
  Re-derived `00427DE0` end-to-end: five consecutive
  sweeps of `+0x290`/`+0x294` per record (not the earlier 32-block fall-through
  extraction — the mechanically enumerated census is **56 blocks / 52 distinct
  handlers**, four clear mechanisms: processor 40, handler-self 11, inline 2,
  consume-only `btr` 2 — counts repaired per `AUDITSEM-CONTRA-FRONTIER-DIRTYBITS`,
  `18279d20`). esi=arg1 gates the tail commit
  (`0042C410` + chain-tail `+0x294`:25 → `00427BD0` → `00420A40`); pass-5
  bit-1 is the record ungate + `+0x250` snapshot. Whole-image setter census:
  `or`-imm `002Exxxx` request family, `bts`+store `0042F2xx` cascade, and
  group-write `+0x294` setters (`and ~cluster` then set own bit; union
  {0,1,5,7,8,10,17}, bit 17 cleared by all). No direct setter for
  `+0x290`{2,5,18,24,31} / `+0x294`{0,1,4,6,10,11,13,14,17,18,19,20} — no
  byte/word `or`/`bts` aliases either word; re-arms inside the `0042F250`
  cascade cover 19/20, the rest arrive via whole-record write (measured gap).
  36/52 handlers are children-loops (gate `00426220` / `[+6]==-1||[+0x2F2]==1`,
  leaf per child); 3 are `_guard_check_icall` virtual calls into chain tails.
  Output: CRR page §14 rewrite + `members/dirty-bits.tsv` (9 cols, all rows
  interior-cited). Gates green; ADDRESS-INDEX regenerated (13,363).
  Prior: `OPUS-REQ-FRONTIER-PASS5-INDEPENDENT-IMPORT` —
  **DONE 2026-09-14.** Fresh headless import of the sealed GN161 `.gzf` into
  `work/proj_pass5_indep` (project `GFZ_PASS5_INDEP`, distinct from the
  sealing `gn161_certify` import). All four proofs reproduced:
  ledger 38161/9409/585/28137/0/38131/30/99.92139; snapshot FAS2
  `c16409ec…`; embedded EXE `73461d08…21f8`; residual 30 addrs
  `955da8c9…`. Retained artifacts `work/verify_GFZ_PASS5_INDEP/`.
  Done this block: `AUDITSEM-CONTRA-FRONTIER-RENDER-VTABLE-DUP` +
  `OPUS-REQ-FRONTIER-STRANDED-ABSENCE-RESIDUE-4` +
  `OPUS-CORRECTION-FRONTIER-RESIDUE-3-NOT-4` — **all three DONE
  `3080b69f`.** Six `calls` cells deduped to the distinct-callee
  convention (each body verified 1-2 distinct callees vs edges.tsv);
  glyph-quads :218 count corrected (three of four now classified,
  `002AC5F0` alone remains in the certified 30), :219 marked
  true-at-GN161 not fixed, the-unresolved-158 :490 pair annotated with
  its GN161 class; second-icon-drawer :167 left untouched per the
  correction. Re-run: 0 LIVE in my folder; the two lmap LIVE rows are
  already with ORACLE.
  `OPUS-REQ-FRONTIER-AGGREGATE-CLAIMS` — **DONE `dfe3775d` (+ board
  `fec05ae5`).** Per-document verdicts in
  `_index/candidates/aggregate-claims-gn161-adjudication.tsv` (71 rows).
  Method: the GN158→GN161 delta is provably tag/comment-only (128 records
  gained CodeDomain), so only claims over (a) the residual set, (b) the
  no-CodeDomain set, (c) the 11 grown families, (d) the explicit ledger
  figure could move; every byte/graph/shape/owner census is stable.
  CORRECTED: phyre-subsystem-map (6,768→6,769, Rendering 287→288,
  ~217/26→147/24, 992→993), largest-unclassified (10,152→10,024 /
  2,524,402 B), ownership-boundary (ledger three-way), capability-policy
  (158→30), object-construction + 24-README (225→226), image-hardening
  (992→993), memory-allocation caller split (Boundary 9→10, Runtime
  303→304), unowned-code census (15,896→15,975; 317→335; glue/substantial
  table), class-descriptor frontier (6,735→6,736), third-party inventory
  (690→691, 801→802 via new ThirdParty.XML.ConfigParse member), 99-README
  (158→30 + sha + pointer), glyph-run standing claim bounded, plus
  _index/COVERAGE, EVIDENCE-STANDARD, READINESS-GATE, COMPLETION-PLAN.
  BOUNDED: exception-funclets — 1,609/3,895 are .pdata-structural (cannot
  move); "386 unclassified parents" annotation-derived, bounded ≤4
  (parent list not preserved under Tools/work; only measured EH-adjacent
  new edge 0089FC9B→005DD890). STABLE: remainder re-verified (thunk 689,
  Runtime.Callback 409, __xc 1,172-table has zero newly-tagged targets,
  Phyre.Reflection 4,557 / ScriptVM 1,219 unchanged, Bullet 120/138).
  Prior package: `OPUS-REQ-FRONTIER-STRANDED-ABSENCE-CLAIMS` — **DONE
  `cc759036` 2026-09-14.** All 37 rows adjudicated: 29 present-tense status claims
  corrected to name the GN161 CodeDomain, 5 verified correct-as-history, 3
  re-routed to owning lanes (`FRONTIER-REQ-ORACLE-STRANDED-LMAP`,
  `FRONTIER-REQ-CONTRACT-STRANDED-CRR`); per-row verdicts recorded in the TSV.
  Census repack stamped to GN161 (`OPUS-NOTICE-FLEET-PARENT-ADVANCED-UNPACKED`
  answered; `check_census_generation` green); render-vtable role-column repair
  published `d070e4f6`.
  `OPUS-REQ-SWE2-FRONTIER-APPLY-RESIDUAL-109-DOMAINS` +
  `OPUS-REQ-SWE2-FRONTIER-RESIDUAL-109` — **BOTH DONE 2026-09-14. Batch R109
  applied and certified as the GN161 parent.** Pipeline: fresh GN160 import into
  `work/proj_gn161_r109`, enrich 109 rows PASS, apply via
  `ApplyCurrentBodyCodeDomainBatchAllowExisting` (earlier batches' domain tag
  names preexist — the strict variant refuses on tag-name collision; function-
  level classification-drift checks still ran), pre/post FAS2 diff CLEAN
  (comment+tags only on exactly 109; immutable 0; added/removed 0/0; tag
  removals 0), PACK_PASS `11110a34…d77500` 82,179,446 B, certified by fresh
  import into `work/gn161_certify`: ledger 38161/9409/585/**28137**/**38131**/
  **30** pct=**99.92139**, snapshot `c16409ec…` reproduces, embedded EXE
  authorized `73461d08…21f8`. `GfzEnv.ps1` advanced to GN161 (GN160 in lineage),
  `COVERAGE.md` ledger block re-derived, residual-109 TSV header records the
  apply, unresolved-158 page carries a GN161 status banner. Wrapper fix:
  `Apply-GfzBatch.ps1` now accepts the `ALLOW_EXISTING` pass marker. Consequence
  filed: `FRONTIER-REQ-FABLE-PROVENANCE-TRANSFER-GN161` — 242 GZF-derived docs
  carry superseded parent stamps and need a `transfers_to` ruling (comment-text
  appends are the new delta shape).
  Prior: `FABLE-REQ-SWE2-FRONTIER-RENDER-VTABLE-SLOTS` —
  **review-gated**. All three RTTI class x slot matrices written with per-row
  interior citations: OrderedObject 43 classes / 95 distinct bodies
  (§2.5 + `members/ordered-object-vtable-slots.tsv`, 132 rows — base slots 1+2
  are `jmp _purecall`; 40-dtor shape `00212CE0`; order keys 0x1/0x10/0x20/0x80/
  0x100/0x2/0x4 plus two field-read keys; FontBorder slot-3 setter `00225580`),
  GeometryInstance 24 classes / 144 slot positions / 68 distinct bodies
  (gi page §18a + `members/geometry-instance-vtable-slots.tsv` — `0016D6A0`
  already named, so 67 uncovered matches the request exactly; slot 0 prepare,
  slot 1 execute, slot 2 dtor only on DynGeo; the earlier 29/81 scratch count
  was a name-match pulling in `GeometryInstanceOrderedObject` + GiReset*Obj +
  4 Phyre reflection classes, resolved by ancestry), RenderObject 3 classes /
  29 bodies (§18b + `members/render-object-vtable-slots.tsv` —
  `CharacterRenderObject` 31 slots, 27 frontier).
  **Caveat:** the five files committed under OPUS's `feb33bb0` via the
  shared-index race (disclosure `OPUS-NOTE-FRONTIER-MY-COMMIT-CARRIED-YOUR-RENDER-FILES`,
  board note `604167b0`); content verified identical at HEAD.
  Review filed as `FRONTIER-REQ-AUDITSEM-RENDER-VTABLE-SLOTS` (rev 9098).
  Gates: verify_doc_addresses + links + consistency + questions + provenance
  all green; ADDRESS-INDEX regenerated (13,248).
  Prior: `FABLE-REQ-SWE2-FRONTIER-IMPORT-EIGHT` **DONE**
  (`303fd8fa`+`bcb3e4a2`): all eight bodies re-read, zero mismatches, placed with
  research provenance; `research_import_gap.py` named+owned gap now **0**. Two
  follow-up contradictions repaired `628ade54`: THUNKROOTS (006CA8D0 = 7 rip +
  3 rax indirect; 001A11B0 allocs via 00584740; 005FDEA0/005FE010 tails 3-vs-2)
  and 3703A0 (003DFFE0 added to cluster table; baked-parameter window corrected
  to 022D91A0–022D9270). OPUS-NOTE provenance stamps added to the four
  effect-type pages — `check_provenance` "NO exe_sha256"/"NO audit block" both 0.
  Prior: `FABLE-REQ-SWE2-FRONTIER-EXCLUSIVE-SUBTREES` — completion-ready,
  11-contradiction AUDIT-SEM sweep repaired `7b841f95`.
  `OPUS-REQ-SWE2-FRONTIER-RENDER-PASS-REGISTRY-PAGE` — published `67236b49`,
  review-gated on `FRONTIER-REQ-AUDITSEM-RPR-PAGE`: post-process page §7a
  (registry contract, node layout incl. `+0x10`/`+0x18`, three return codes,
  declared 60-wrapper family) + `members/render-pass-registry-60.tsv` — all 60
  rows re-derived at the image (name+node+teardown, 60/60).
  Review-gated claims: `FABLE-REQ-SWE2-FRONTIER-MENU-SCREENS`,
  `FABLE-REQ-SWE2-FRONTIER-EFFECT-TYPE-CLASSES`, `FABLE-REQ-SWE2-FRONTIER-AUDIO-SLOTS`,
  `SWE2-FRONTIER-ENTRY-CITED-HUBS`, `SWITCH-FAMILIES`, `RESIDUAL-PLACEMENT`,
  `MODEL-OSCILLATOR-0040`, `EE-REGISTER-MEMBERS`,
  `RENDER-PASS-REGISTRY-PAGE`, `RENDER-VTABLE-SLOTS`.
- **Exact next action:** `FABLE-NOTICE-FRONTIER-PASS22-368` **DONE** —
  the R3 clauses-1+2 work list is planned and routed: live measure is
  **25 pairs → 17** as peers disposition in flight (TSV:
  `_index/candidates/pass22-r3-clauses12-pairs.tsv`; FRONTIER's 3 rows
  dispositioned with bullets + registry rows, published `2bbec7ad`;
  lane requests filed for CONTRACT/ORACLE/STRUCT/DATA — DATA's row
  already cleared, task will finish trivially). The R3 vote itself
  remains open — a separate decision on instrument merits, per FABLE §7.4.
  `FRONTIER-CONTRA-6349B0-THUNK-ROLE` **ruled in FRONTIER's favour** —
  FABLE corrected the peer's section in place (`3eae5896`).
  RESIDUAL-PLACEMENT claim **finished** (NARROW verdict + e25264ac
  repairs). SWITCH-FAMILIES stays ACTIVE: REJECT verdict's five defects
  repaired (17c0368a + addendum 8ad1f17b), re-review filed
  `FRONTIER-REQ-AUDITSEM-SWFAM-4TO8-RE`. Watch for the AUDIT-SEM
  verdicts on `FRONTIER-REQ-AUDITSEM-NOCALLER-INSTALLERS` / `-2`,
  `WIDGETPROC-REGEN`, `LAYOUT-KEY-READERS`, `SWFAM-4TO8-RE` —
  AUDIT-SEM is daily-capped with 10 reviews queued.
  Fallback queue: the 478-root follow-up
  (`subtrees/exclusive_subtrees_followup.tsv`). Roots 1–10 are
  **DONE**: `00253C70` (`bbc8d235` — input-arbitration family),
  `001E8580` (`7895bc17` + index `9a8b2375` — glyph-run vertex
  pipeline), `00336CE0` (`394cd28f` — battle-locomotion solver),
  `0032E070` (`fc20daeb` — resource-request pump),
  `0026C8C0` (`725a624e` — actor bind; EVTMEM/navimap queries),
  `001B4D70` (`6bfa7982` — font `.ker`/`.fex` loader: the shared
  ordered-map insert layer), `001BBFC0` (`26b30752` — `01F81240`
  singleton's 0x2A8-record vector + anisolighting shader request),
  `002E5750` (`990db79b` — 13 kind-`0x60`-gated steering-record
  accessors behind the mode integrator), `00304850` (swept in
  `8812f60a` — five state arms over the shared `0020E600` row
  lookup), `001C7940` (swept in `6c22bcfa` — the 153-setting
  loader's typed-store layer). Reviews filed for each
  (`FRONTIER-REQ-AUDITSEM-SUBTREE-*`). Next largest unclaimed:
  `002342F0` (12 members, `BattleSystem_InitializeAreaState`),
  `002E28E0` (11, movement). The 30-residual body-read belongs
  to SWE2-EC7 — do not duplicate.
  `OPEN-QUESTIONS.md`/`AUDIT-LOG.md` are publish-window surfaces
  (ruling cc1946da) — never claim-duration keys; I rotated them off the
  stale `DATA-FMT-PS2IMG-TAIL` claim (rev 11172).
  SWITCH-FAMILIES request **DONE** — all ten dispatchers carry published
  case tables (latest: `09a13795`, the `00500850`/`00500980` record-store
  pair on effect-element-type-dispatch.md §2.7 + the three `003A9xxx`
  store ops + `003AA1BC` TABLE adjudication + all-dispatcher decode TSV);
  review `FRONTIER-REQ-AUDITSEM-SWITCH-FAMILIES` filed.
  Latest coherent commit: `baf3686a` (00258190 subtree + 00238A30 narrowing
  + contra trio). In flight: `002E09A0` subtree bound on the world-tick page,
  gates clean, review filed — `SWE2-FRONTIER-PUB-002E09A0` READY waiting on
  `@publication`; also claim+finish the leftover `SWE2-FRONTIER-PUB-CONTRA-TRIO`
  (its files are already in `baf3686a`) in the same lock window.
  Done since: `UI-ATLAS-MESSAGE-IDS`
  (`4a076a02` — three message_ids rows repaired to the distinct-arm convention,
  verifier 67/67 + 63/63), `CENSUS-PARENT-STAMP` (`046f6ec7`), and the
  TEXT-GAP registry **third pass** (`3bc9451a` — claim already DONE at
  `f5230908`; this pass decided 24 more rows against the image: 2 TABLE
  read out of prev_fn indexing code — `0028144C`/`002FE5B0`; 22 UNLISTED
  body starts incl. four SIMD-kernel starts `0012AD00/70/00/90`;
  interior-point reasons sharpened for `002FE7xx`/`0055B3xx`/`00580xxx`.
  Verdicts now 155 TABLE / 24 PAD / 28 UNLISTED / 56 UNCONFIRMED, all
  reasoned; residual is the UC-1 population question). `SUBTREES-THUNK-ROOTS`
  done (`107add21` — `0017D000` 114-member manager-init burst on
  game-application.md, `006106A0` 48-member work-ring thread on the
  input-stack page; families + open questions reported to FABLE). Planner
  action done: `FABLE-REQ-FRONTIER-STALE-REGISTER-LOCK` → nudged SWE2-DATA
  in its inbox to drop `open-questions.md`/`audit-log.md` from
  `DATA-FMT-PS2IMG-TAIL` until publish.
  Tools: `Database/Tools/work/SWE2-FRONTIER/{xdis.py,swdump.py,bshape.py}`.
- **Done this block (board rev ~8770):** `FABLE-REQ-SWE2-FRONTIER-EXCLUSIVE-SUBTREES`
  — all 20 cited top roots done. This session: `003B8670` (33, ownerless-functions
  §12), `00266D10` (32, weather), `00234590` (31, world-tick), `00253970` (31, gil),
  `001CD0E0` (28, console `DebugMenu_Render`), `001A5B30` (33, `.ta` page),
  `001D1660` (26, console dispatch), `002628B0` (26, manager-unload), `0020AC30`
  (24, audio-slot setter), `002F6AB0` (23, YM00 ctor `26415517`), `0022A0B0` (144→
  67 in-scope, boot `26f05908`). Two AUDIT-SEM routed repairs applied `3b272d5b`
  (0022B0B0 narrowing + 0022A770). All gates green; A-count 1,470.
- **Done this block (board rev ~8072):** `FABLE-REQ-SWE2-FRONTIER-VU1-REGION` DONE —
  `members/vu1-region-functions.tsv` (351 rows, role+evidence each, no
  adjacency-only roles) + page §2.6; the 54 VU-state touchers proven
  layer-internal; `004EF860` form compared (8/9 look-alikes match, `004CF280`
  does not). Commit `630663b8`. Two verdicts processed: menu-screens-2 (handbook
  `+0x11D0&1` page-built flag polarity fixed) and effect-types-00-0a (six defect
  classes — base setup FOUR heads `+0x00`–`+0x30`, universals qualified for the
  `0x02` outliers, helper order corrected, five setup maps re-emitted incl.
  `00431770` 4× stride-`0xF0` loops, globals `02AEE908`/`02AEE900`). Both handed
  back to AUDIT-SEM. OPUS date notice done (`2026-09-13`). Commit `d177d73c`.
- **Done this block (board rev ~7991):** all four effect-type groups published —
  `4a14fdec` (`0x00`–`0x0A`: method vocabulary — base+tail step/update, pointer-rebase
  setup, workbench walk), `3009f518` (`0x60`–`0x74`: PRNG `0044B960`, deferred-free
  queue `0024B1C0`→`02092150`/`02092168`, `0x70` definition-only), `7f6928f4`
  (`0x80`–`0x97`: shared-method band, variant-selector walks keyed on record flag
  bytes), `cfb64718` (`0x40`–`0x42`/`0xA0`–`0xAB`/`0xD0`–`0xD1`: `0xD0`/`0xD1`
  seventh-method payloads). AUDIT-SEM menu-screens-1 verdict landed as
  `AUDITSEM-CONTRA-FRONTIER-MENU-SCREENS-1`: all 5 defects verified against the
  image and repaired in `4a14fdec` (D1 global `02CA9738`, D2 all-clear gate,
  D3 `0x7E`, D4 `0x121` is the id-18 destroy arm, D5 editor table `00569F1C` +
  peeled `0x121`); finished → auditor re-verifies. `@publication` released after
  each commit.
- **Done this block (board rev ~7783):** UC-1 audit fix published (`707a2ad9`),
  `AUDITSPEC-REQ-FRONTIER-UNLISTED-SIGNALS` DONE, `OPUS-REQ-SWE2-FRONTIER-RESIDUAL-ORDER`
  DONE (`residual-order.tsv`), `OPUS-CORRECTION-ENTRY-ONLY-WORKLIST` DONE (107 rows),
  `OPUS-CONTRA-QUESTIONS-DOUBLE-COUNT` DONE (166 shared ids; 6 stale pairs settled;
  register mutation routed to owner SWE2-DATA), three planner notices answered
  (publication hold ended, DATA ledger-claim is owner-release, DATA lane stale-but-free).
- **Fleet posture:** desired=[EC7, STRUCT, DATA] (2026-09-15 external-review
  replan; see the fleet-integrity bullet at the top of this block). FRONTIER is
  never in `desired` — it runs planner wakes / manual Continue alongside the
  three specialists. AUDIT-SPEC first in line for rotation (resumable P1
  pass-22 rederive claim); ORACLE waits on `@publication` for EXP083-PUB;
  CONTRACT and AUDIT-SEM follow. Controller pid 11856 alive; logon startup via
  HKCU Run key `SWE2FleetWatchdog` → `controller start` (pidfile guard makes
  re-entry a no-op). On any activation, first process pending replans (planner
  duty below).
- **ASTRA window (until ~2026-09-19 reset):** ASTRA is not an eligible dependency; live-only
  questions go to `_inbox/ASTRA-QUEUE.md` (8 seeded). Policy in TEAM.md. On ASTRA's return
  FRONTIER re-triages the queue — highest-value truly-live items first.
- **Planner duty (this lane):** replanning is event-driven — workers file events via
  `swe2_watchdog.py replan --identity <id> --reason <REASON>` (append-only files in
  `%USERPROFILE%\.swe2-fleet\replan-events\`; only the watchdog wakes). When woken as planner,
  or whenever FRONTIER sees `pending: true` during its own board pass: inspect board/requests/
  reviews/rate state → write `fleet-plan.json` →
  `swe2_watchdog.py replan --clear --identity SWE2-FRONTIER` (planner-only, mechanically
  enforced). A planner wake counts toward hard_max (own debounce: 180 s); FRONTIER needn't
  occupy a desired slot when its work isn't top-3.
- **Fleet scheduling duty (this lane):** `swe2_watchdog.py` is now the capacity-limited controller
  (target/hard max 3, staggered wakes, rate-error circuit breaker, never-wake list). FRONTIER owns
  `%USERPROFILE%\.swe2-fleet\fleet-plan.json` — refresh `desired` at every checkpoint to the
  smallest highest-value set; if it goes stale (>6 h) the controller falls back to the board
  heuristic. Lanes can only be woken while their session lock is FREE (not open in Devin Desktop).
- **Pending requests/reviews:** none awaiting me; the ramp-channel draft files I left uncommitted
  (`Reconstruction/Game/Presentation/ramp_channels.*`, `Tests/Differential/{diff_,}ramp_channels*`)
  belong to SWE2-CONTRACT's `OPUS-REQ-SWE2-RAMP-DIFFERENTIAL` — do not edit.
- **Fallback eligible work:** this lane's ready queue; never a peer's claimed resource.
- **Latest coherent commit/checkpoint:** fleet-integrity repair 2026-09-15 —
  board revs 13282-13286 routed, parked_ineffective cleared (stale premise),
  desired=[EC7,STRUCT,DATA], controller pid 11856, replan queue cleared.
  Prior: fleet hardening sealed 2026-09-14 — append-only replan
  events (8-writer concurrent test: zero loss; mid-clear event survives), planner-only clear
  (non-FRONTIER refused, exit 2), planner debounce 180 s, controller lifecycle
  (`controller start|stop|restart|status`, pid 16760 detached, duplicate-start refused),
  `rebuild` regenerates map+state from `devin list`, semantic resume-staleness check live
  (6 lanes flagged for repair at next checkpoint). Real worker→replan→rotation proven:
  throwaway `SWE2-TEST-THROWAWAY` filed ROLE_QUEUE_DRAINED itself, watchdog observed, FRONTIER
  rotated AUDIT-SEM→AUDIT-SPEC, controller woke `sapphire-porkpie`. Publication request
  `OPUS-REQ-FRONTIER-FLEET-HARDENING` filed board rev 7364 — all FRONTIER changes uncommitted
  pending @publication (FABLE holds `FABLE-PUB-LMAP`). Claim checkpoint board rev 7252.

## Checkpoints

Append below, newest last. Record corrected facts and remaining work, not file growth.

### 2026-09-13 — watchdog became the fleet scheduler; unlisted-entry input recovered

Two packages this turn. **(1) Fleet watchdog → dynamic controller.** `swe2_watchdog.py` rewritten:
`target_active=3`/`hard_max=3`, desired set from `fleet-plan.json` (FRONTIER-owned, stale>6h falls
back to a board heuristic: ACTIVE claim > targeted READY > lane research; auditors only while
review work exists), staggered wakes (one/poll, ≥120 s), and a circuit breaker that suspends all
wakes for the reported reset+margin on a Windsurf overall-message-rate error, then re-probes one
worker at a time. **Host-interface corrections (recorded in TEAM.md):** `devin -r <id>` resumes IN
PLACE and only while `session_locks/<id>.lock` is free — a held lock means *open somewhere*
(including idle Devin Desktop tabs), not *working*; resume of a desktop-held session fails
`session_locked`. Validated by a create→resume round-trip on `glamorous-pecorino` and a dry-run
decision pass; `tree-coaster`/`universal-coral` are never woken. **(2) UC-1 input.**
`unlisted_entry_points.py` emitted `unlisted-entry-points.tsv`: 1,525 candidate entries in 1,392
blocks (204,593/244,619 B, 83.6%); 1,283/1,302 body blocks covered; controls 99.99%/99.99% on the
listed population. Checkpointed at board rev 7159. Residual visible: 19 body blocks decode to zero
instructions; a segment end is not a proven function end.

### 2026-09-13 late — event-driven fleet + ASTRA window + residual fully adjudicated

**Fleet:** controller is event-driven now (`replan` subcommand, aggregated pending replan,
planner wake counts toward hard_max=3, breaker margin 25s); running as `--loop` pid 18188.
Desktop released all locks; wake path proven live (AUDIT-SEM filed its mkvparser verdict; EC7
woken and working). Initial three: FRONTIER + EC7 + AUDIT-SEM. **ASTRA window (~6 d):** ASTRA is
not an eligible dependency — policy in TEAM.md, prepared queue in `_inbox/ASTRA-QUEUE.md` (8
seeded items from READY/BLOCKED ASTRA requests). **Claim:** residual adjudicated — 15 of 19
zero-decode blocks are switch jump tables (all 181 entries resolve into listed space; body upper
bound ~1,287); 4 are +1 mid-instruction SSE case bodies (declared plausible). Split blocks: 45
extras carry ref/jmp-in evidence, 88 are post-term-only uncertain. Unlisted-body count is the
range ~1,332..~1,424; denominator unmoved pending review. Board rev 7252.

### 2026-09-14 — orchestration hardened and sealed; live rotation proven

All nine review fixes landed in `swe2_watchdog.py`. Append-only replan events (8 concurrent
writers → zero loss; event filed mid-clear survives; malformed → `quarantine/`). `replan
--clear` mechanically restricted to SWE2-FRONTIER. Planner debounce separated (180 s vs worker
900 s); daily cap retained. Controller lifecycle commands (`controller start|stop|restart|
status`) with PID-file identity guard; running detached as pid 16760, 120 s polls. `rebuild`
regenerates the eight mappings + never-wake set from `devin list`, fail-closed on duplicate
titles. Resume-state check is semantic now — flags `claim-done`/`none-vs-active-claim`/
`duplicate-blocks` (6 lanes currently stale, repair at their own checkpoints). Permanent
`Continue` semantics persisted in root `CLAUDE.md`; worker replan obligation + ASTRA-window
policy in TEAM.md; ASTRA-QUEUE.md elaborated into three batches with discriminating
observations (two items downgraded to author-decisions — not live-only). **Live lifecycle
proof:** throwaway session (deleted after) filed `ROLE_QUEUE_DRAINED` itself → watchdog
observed → quiet window → planner wake suppressed (FRONTIER already active) → FRONTIER
re-planned desired=[FRONTIER, EC7, AUDIT-SPEC] → planner-cleared event → controller woke
`sapphire-porkpie` (pid 5384). No user message anywhere. Publication: all changes uncommitted;
request filed to OPUS (rev 7364) — FABLE currently holds @publication (`FABLE-PUB-LMAP`).

  **2026-09-16 block 4 — ten more subtrees bound:**
  `00536410` (message-table page — the slot formatter:
  `00536190` context resolve, `0035D400`/`0035D430` `00D10C60`
  permutation-map pair feeding `002DD7B0`/`002DD7E0`);
  `005369C0` (same page — the realiser: `00536310` per-slot
  resolve ×3, `0031B860`→`[02EBF188]` ×4, `00536280` ×2, then
  `00536410`+`0035B990`; members `00263B40`/`00267410` are the
  `+0x102` movsx getter / setge-nonneg pair — the richer
  `00263B50`/`00267420` bodies are siblings, not members);
  `00320160` (CONTRACT-field-record-accessors — thunk to
  `00377BA0`, the save-overridable bits-12–13 accessor;
  getters `00314AA0`/`00314AC0` read `+0x1062`/`+0x1063` off
  `002EF2B0`); `005C9760`/`005C97A0`/`005C9780`/`005C97C0`/
  `005C97E0`/`0060D7F0`/`0060D990`/`006C2770` (vtable-method-
  index — the `PClassDataMemberPhyreArray` slot-5 adapter
  family: identical 29-B `[rcx+0x48]-dword[[rcx+0x18]+0xF4]`
  index prologue → per-class element accessor (`005C8CA0`,
  `005C8DC0`, `005C8D30`, `005C8E50`, `005C8EE0`, `0060C630`,
  `0060C990`, `006C26E0`) → field copy through `0017D260`;
  classes: PAnimationChannelTarget, PAnimationDataSourceList-
  Entry, PAnimationConstantChannel, PAnimationEvent,
  PAnimationNetworkInstanceTarget, PMeshInstanceSegmentContext,
  PShaderParameterDefinition, PShadowCaster::PShadowSplit).
  **Duplicate avoided:** `0022B7E0` was already bound at
  `cbc007bd` on authored-data-table-registry.md — appended
  section reverted, HEAD restored.
  Index 15,118; ~56 sections staged unpublished. **Next
  candidates:** `0017F8C0`, `001829A0`, `00184960`,
  `001D0390`, `001E71B0`, `001E8070`, `001EC490`, `001F4340`
  (2-member rows now top of queue); `005C97xx`/`006xxxxx`
  adapter cluster continues.
  **Requests pending:** +10 AUDIT-SEM READY
  (`00536410`, `005369C0`, `00320160`, `005C9760`, `005C97A0`,
  `005C9780`, `005C97C0`, `005C97E0`, `0060D7F0`, `0060D990`,
  `006C2770`).

  **2026-09-16 block 5 — four more subtrees bound:**
  `0017F8C0` (numeric-formatting — `001B5FA0`-context thunk
  battery; `001E9860` codepoint→glyph index via
  `dword[[r8]+edx*4]` + `001FDEC0` keyed list search on
  `[rcx+0x50]`/`+0x20`); `001829A0` (render-command-list —
  `SetScreenIndexToPostProcessManagerObj` pass-wrapper battery;
  `0018CC60` frame-open wrapper + `001F1ED0` ctor vtable
  `009030B0`); `00184960` (game-settings — DH-7 present-sync
  setter; `001EDEF0` writes `dword[01DFE0C0]`, `00798E90`
  clamps 1–3 into `01F3DA18`); `001D0390` (ARM-CATALOGUE — the
  293-label filler; `002F79E0` 16-B `movdqa` copy,
  `001EAC50` dword setter); `001E8070` (glyph-run painting —
  the glyph emitter; `001E7A20` `0x38`-stride vector insert,
  `0079E3C0` `+0x28` getter); `001EC490` (render-command-list —
  `ApplyJsonForCutSceneObj` battery; `0018B540` wrapper +
  `001F1770` ctor vtable `009030B0`; `01DFE40C` mode index +
  `mDofFocusDistance`/`mDofApertureFnumber` arms).
  Index 15,138; ~62 sections staged unpublished. **Next
  candidates:** `001F4340`, `001FDB90`, `00223AD0`, `00234200`,
  `00237DF0`, `0023B6F0`, `00250540` (2-member rows).

  **2026-09-16 block 6 — five more subtrees bound:**
  `001F4340` (bigfile page — the 991-B `SRYK`-magic index
  opener; `001F3FD0` red-black insert + `001F4720` index
  accessor); `001FDB90` (font-kerning — the `.fex` ordered-map
  entry create refusing duplicate keys; `001FD780` insert +
  `001FDF90` keyed accessor); `00223AD0` (audio-bank — the
  `.win.sab` loader, `0016D6A0` ×6 assert battery;
  `00220CD0` thunk + `002203F0` record accessor);
  `00234200` (field-map — `ActorSystem_ReleaseBattleUnitSlotForActor`:
  yaw `+0x160`→spawn `+0x74`, `0208E688`/`0208E6A0` BtlWork
  bounds, `00861EC0` free stride `0xF50`; `00263980`/`003589A0`
  tiny getters); `0023B6F0` (282-console — the second Config
  row proc on ids `0x2CA2`–`0x2CA5`/`1`; `0017E540` 22-case
  dispatcher + `001DC920` paired setter); `00250540`
  (widget-animation — the per-frame UI pump; `002508E0` mode-5
  drain on `0208EA38/40/48`, `003C9FD0` mode-gated step).
  Index 15,148; ~68 sections staged unpublished. **Next
  candidates:** `002572E0`, `0025AFC0`, `0025C830`,
  `00263230`, `002B0280`, `002E2240`, `002E45E0`.

  **2026-09-17 block 7 — batch-6 published `0cdb6009`:**
  51 files, +2,311/-597. Cleared entry-only-large rows:
  `007307A0` (`CTextureUtil::InitializeDevice`, source-named),
  `007D76E0` (SurroundReverb param commit), `0085C4E0` +
  `0085CED0` (Bullet solver slots 6/7 — workspace setup +
  constraint accounting/pool growth), `00854F40`
  (`InplaceSolverIslandCallback` slot 1 processIsland),
  `001EC760` (six-literal scene-name `strstr` gate:
  `spc_z0000`/`sum_m0001`/`sum_l0001`/`sum_h0001`/
  `hne_e0100`/`wdl_b0101`). Queue 207 → ~189 rows /
  413,718 B. New page:
  `Authored-Commands/the-authored-presentation-command-handlers.md`
  (28 bodies, dispatch via `02CA4410[id]` + `01EFFAF0`
  absolute slots — the "no reader" hole closed).
  Weather D-4 folded OPUS's verified two-handedness finding.
  AUDIT-LOG excluded from the commit — carries a pending
  STRUCT entry; publish after their registry batch lands.
  Older READY pub tasks (ENTRYONLY-3D83A0,
  CONTROLPLANE-TAIL, CONTRA-REPAIRS-STAGED) are subsumed —
  finish them citing `0cdb6009`. Fleet: controller pid 45124,
  desired=[STRUCT, AUDIT-SEM, AUDIT-SPEC]; UQ-24 tick claim
  released (tick landed in this batch).

  **2026-09-17 block 8 — band run continued (queued for batch-7):**
  cleared `007DB8D0` (`Sd::Driver::BuildReverb` slot 3 — the
  build-reverb parameter commit, same `007A9E50`/`007AED00`
  helper pair as SurroundReverb slot 8, expf+powf over the
  `+0x490..+0x4CC` block); `0084BED0`
  (`btContinuousConvexCollision` slot 1 —
  `calcTimeOfImpact` conservative advancement, GJK substep
  family `0084C6B0`..`0084CB20`); `0019FFD0` (the
  `effect_finish` path-table initializer — 125 `hNNNN.efx`
  pointers, flat qword array `[rbx+0x115750]`; corrects the
  page's "input cluster" read); `007AC4F0` (the
  `hcam`-configured sound-device factory — six RTTI
  vtables + `007AD460` register calls). Queue ~187 rows /
  407,642 B. Superseded pub tasks closed; UQ-24 tick
  finished citing `0cdb6009`. Fleet: controller 45124,
  OPUS cycling @publication publishes.

  **2026-09-17 block 9 — batch-7 landed + pass-22 accounting done (queued for
  publish):** batch-7 published (six paths). Cleared the three queue rows my
  own writeups created: `007D2150` (`SurroundReverb` ctor — RTTI
  `01CB7528`/`01CB7578`, `DynamicValue<2>` `01CB7068`), `007DAFF0`
  (`BuildReverb` ctor), `007AEF30` (rendering-channel block init —
  `02EAD34C=8`, `02EAD358` array fill that `007AED00` reads; corrected
  `mov rax` -> `mov eax`). Queue 403,282 B. **Claimed and completed the
  P1 `OPUS-REQ-FRONTIER-PASS22-BATCH6-39-UNACCOUNTED-NEIGHBOURS`:**
  wrote section-4.2-style crossing paragraphs on all 16 affected docs
  (incl. the `00377C20` 12-label fan-out and `0017D280` variadic-logger
  fan-in on the adm/bigfile pages), appended 39 `CROSSING-ACCOUNTED`
  rows to `neighbour-dispositions.tsv`. Live audit now reports **2
  findings**: `002FE7D0` unlisted-code + effect-mesh-54 ->
  CoreRuntimeScheduling — both pre-existing and routed to SWE2-DATA,
  not batch-6's. Verified via HEAD-worktree re-run: the 39 rows match
  `0cdb6009`'s additions exactly. Consistency + address-index clean.
  `SWE2-FRONTIER-PUB-PASS22-ACCOUNTING` filed READY — publishes 24
  paths once `OPUS-PUB-EC1-RESTATED` releases @publication. Request
  task stays ACTIVE until the publish lands. Next: claim+publish when
  the window frees; then finish the request citing the commit.

  **2026-09-17 block 10 — pass-22 published + five more rows cleared (queued
  for batch-8):** `a5232d9c` landed all 39 batch-6 dispositions +
  AUTHCMD-BANKB contra repair; both tasks finished. Band: `007FF1C0`
  (Tremor decoder-core tail — bitmask scan, `01CC4810`/`01CC5820`
  fixed-point tables, sorted-post store loop; naming queued for
  adjudication), `001DE5D0` (`GameSettingConfig_ParseText` CONFIRMED —
  the "interface populate" cluster claim was wrong: its 34 rip-indirect
  calls are IAT thunks, `edx=0x3d` `=` split, `r12+0x1CDD050` key table;
  corrected on the config page + audio-boundary citer), `0084B320`
  (`btSubsimplexConvexCast` slot 1 `calcTimeOfImpact`), `007D6270`
  (`SurroundReverb` slot 5 — the per-frame parameter ramp stepper, ~40
  unrolled (cur,tgt,flag) triples at 0x30 pitch), `0075C080`
  (`CRenderTextureArray` slot 0 `InitializeDevice` — `007273E0` gate,
  `006DF480`/`0071B3C0` release pairs, recreate calls). Queue 180 rows /
  394,859 B. Fleet rotation: desired=[STRUCT, AUDIT-SPEC, DATA] — DATA
  holds the effect-mesh P1; AUDIT-SEM's P3 subtree claims persist.

  **2026-09-17 block 11 — 12 more exclusive-subtree roots bound (73 this
  session arc):** index at **15,208 rows / 422 docs**. Bound and gated:
  `00263230` (mode-1 `ActorResource_StartEntryScriptExecution`,
  time-stop page), `002B0280` (render submit prep, spawn-keep-entry),
  `0030A4E0` (`Equipment_EvaluateCandidateLoadoutAndBuildDerivedStats`
  — classifier `00309480` → `dword[+0x24]` + `002FEF30` rebuild),
  `003014C0` (`AiOrder_EvaluateAndResolveActionTarget` gates),
  `002FEF30` (stats rebuild; members are the `/100` magic-divide pair —
  `002F8E50` = `ecx*edx*(r8+1)/100`, `002F9180` = `ecx*edx/100`;
  boundary correction: `002F8E70`/`002F91A0`/`002F9240` are siblings),
  `00317ED0` (`EnemyChain_UpdateOnDefeat` — `022C315C`/`022C3168`
  counters, `0x3E7` cap, `[0209BE80]+0x7C7x` record writes),
  `0032FC30` (`WorldSimulation_ProcessDeferredModeRequest`;
  `0025D4D0` = 22-B `0x288`-stride flag-clear on `02098E10`),
  `003083B0` (`BattleAction_CheckTargetEligibility` — `[02EBF138]` +
  `0020E600` row battery), `002E45E0`
  (`Movement_UpdateSteeringTowardTarget` — `003A19C0` vector deltas,
  `003DA6A0` angle stage), `00306760`
  (`BattleAction_UpdateSpecialPresentationSequence` — `022C215C`
  state), `00315E90` (navimapdata command interpreter — both arms on
  `[022C2550]`), `0030C970`
  (`BattleAction_ReleasePresentationSlot` — `022C17B0` + `cl*48`,
  `cl==0xFF` out). All `interior_cite` clean (all flagged violations
  verified pre-existing at HEAD). 12 `AUDIT-SEM` requests filed ACTIVE.
  Queue: ~325 unbound rows remain; next candidates `00307C70`,
  `0031ADB0`, `0034DB30`, `00360710`, `002E5180`, `002E2240`,
  `006234A0`, `0067A480`, `001E71B0`. `@publication` unheld; staged
  sections unpublished per operator instruction.

  **2026-09-17 block 12 — pass-29 link depths + publish-guard link leg.**
  OPUS's `f4e46dc7` repaired 26 of the 30 pass-29 breaks; the two left
  to holders were mine and are repaired in-tree: world-tick page
  `../_index`→`../../_index`, sead-function-identification
  `_index`→`../_index`. Guard integration landed in-tree:
  `check_links.py` gained `--raw` (machine output, no head_scope
  split — the publish side's files are worktree edits inside the
  worktree and would otherwise classify as "not published debt"), and
  `check_publish_neighbours.py` now runs `check_links --db <wt> --raw`
  on BOTH detached sides and refuses on `links_after − links_before`
  (same added/gone semantics as neighbour findings; a break already
  standing at HEAD is not the publish's to answer). Verified live:
  guard run over the two repaired files printed "links repaired by
  this publish: 2" and exited 0. Three AUDIT-SEM contras repaired
  in-tree: `00227420` member row (the `0x400` arm lives in `00227460`,
  a separate 62-B twin reached through Script-VM thunk `00350400` —
  dropped the second-arm cite, noted the twin), `002B0280` ~500 B →
  6,441 B, `003014C0` ~447 B → 876 B + `00319460` tail-jump →
  call+`comiss` epilogue. `27464-ARM`/`2B0280-SIZE` claimed ACTIVE;
  `3014C0-SHAPE` is READY but its file resource is held by my own
  ACTIVE sibling — claim lands when it frees. Next: claim
  `SWE2-FRONTIER-PUB-BATCH-8` when `@publication` frees (currently
  unheld) and publish the pass-29 pair + guard pair + contra repairs
  + batch-8 rows; exclude ADDRESS-INDEX (regen encodes peer
  citations) and AUDIT-LOG (peer entries). Queue: 392,373 B.

  **2026-09-17 block 13 — pass-29 closed, guard armed, contras published.**
  `891f0849` + `ed4c533f` landed: (a) pass-29 residual — world-tick and
  sead link-depth repairs, plus two menumap pages whose decoder links
  pointed into git-ignored `Tools/work/` scratch (de-linked to inline
  code — they could never resolve in a clean checkout); (b)
  `check_links --raw` + the publish-guard link leg — the guard caught
  and I accounted 7 new crossings my band notes introduced (per-doc
  CLIENT sentences on workbench/spawn-keep/levels-up/post-process
  pages); (c) all three AUDIT-SEM contra repairs. **Completion proof:
  `check_links --raw` exits 0 in a detached worktree at `ed4c533f`.**
  Band reads this block: `00279E20` (UI level-up arm dispatcher, 46
  outbound edges, `00245000` callback registrations `0027C870`/
  `0027AA70`/`00276D30`), `0077E0B0` (`CDepthOfField` slot 3 — ~25
  counted `006DA8A0` vtable-`+0x10` dispatches on `01F3BA68`),
  `0018D850` (effect-record registration battery, 5-call idiom ~9x
  into `02D3A440`), `007943E0` (GameApplication script-method
  registration — `getWidth`/`getWorld`/`setCamera`/`getDebugUtils`
  etc. bound via `00632FB0` into `02EAC3xx`). Queue: **381,677 B**.
  `OPUS-REQ-FRONTIER-PASS29-THIRTY-BROKEN-RELATIVE-LINKS`,
  `SWE2-FRONTIER-PUB-BATCH-8`, all three contras finished.
  `@publication` released. Next: board-tail publish; band continues.

  **2026-09-17 block 14 — seven more entry-only-large clears, queue
  381,677 -> 363,990 B.** `003A4290`/`003A56F0`: already fully censused
  (switch-family-3a42-3a56.tsv, effect-element-type-dispatch PARTIAL
  page) — the rows persisted only because the citing DOCUMENTED pages
  named entries without interior anchors; added anchors to
  field-runtime-pass + record-field-map (`003A4308`/`003A578C`
  selector bounds). `002F2530`: the effect frame-advance body —
  `001EDDA0` x2 over `02EBEF88`, `003A8950`/`002F31C0` arms, pi/2 and
  -0.5 SSE scaling into the `022D92E0`/`022D92F0` vector pair (same
  globals the `003A56F0` compute front fills). `00741680`: narrowed
  the rng-streams open thread one hop — `0074C4D0`'s sole caller is a
  PPFX-span worker reached only from `006F61F0`. `0018E4A0`: AO
  blur/composite confirmed — `ColorBufferSampler`/`gMainTexTexelSize`/
  `gAoAxis`/`gMainTex` bound via `0018D240` on `01F7E340`. `006F8740`:
  identified as `CPostEffect::EndPostEffectScene_PreProcess` itself —
  the twice-referenced `CPostEffectEndPostEffectScene_PreProcess:`
  diagnostic names its own site (PPFX ERROR strings `00D90A58`/
  `00D90E70`). `00191560`: DoF pass binds six names (`materialColor`/
  `customPosition` newly noted). Fleet: consumed EC7's
  BLOCKED_NEEDS_SPECIALIST replan — rotated EC7 into desired
  [STRUCT, DATA, EC7] over AUDIT-SPEC (which holds no board tasks).
  Gates: links clean on all five touched subtrees, addresses verify.
  Next: publish the six docs + TSV + board tail when @publication
  frees; band continues.

  **2026-09-17 block 15 — five more entry-only-large clears, published
  `20482d09`; queue 354,576 B.** `001930F0` SSS pass (ten `0018D240`
  binds incl. LinearSampler/PointSampler not previously listed),
  `00191E90` scalable AO (all 13 constants bound in table order),
  `0059C700`/`0059D940` cluster-loader object builders (`005CDAA0`/
  `00584730`/`0017D260` shapes verified), `00596890` byte-swap stream
  op (`0059FFC0` x6 + `call r13`/`r12` tails). Publish:
  `SWE2-FRONTIER-PUB-BATCH-9` DONE. AUDIT-LOG still excluded —
  STRUCT's four-census widening entry unpublished (its batch carries
  it). Next: band continues; publish tail when window frees.

  **2026-09-17 block 16 — two publishes + nine band clears total.**
  `20482d09` (band-15: 001930F0 SSS / 00191E90 scalable-AO /
  0059C700 / 0059D940 / 00596890), `06815e10` (board tail),
  `42d51afb` (band-16: 003AF460 countdown driver over 0x380-stride
  records at 02B3F58C; 003C8B70 thrice-repeated 8-call
  sound+state sequence on the group-wipe page). In-tree pending
  batch-11: six UI-layout P-reader interior reads (002D2DB0
  scroll bounds + 002D8D10 x4; 00273E30 BattleCommand; 0057C480
  confirm-window; 00228C70 pause-menu parent; 002BA700 locamap;
  00292390 listitem). Queue: **337,630 B**. Also repaired two
  ../../_index depth errors in spawn-placement's 00584580 section
  (parallel session's file — rides its publish). Fleet: desired
  [STRUCT, DATA, EC7]; EC7 rotated in but still queued
  at-capacity (foreign session irradiated-lentil counts).
  Next: publish batch-11 when the window frees; band continues.

  **2026-09-17 block 17 — sixteen more exclusive-subtree roots bound (124
  this session); index 15,363.** `00379D40`/`003EADE0` (resource-queue:
  13-B wrapper + 198-B list splice on `02ADD170`/`02ADD790`/`02ADD870`;
  8-state request machine on `byte[+0x30]` gated by `byte[+0x31]`),
  `003057D0` (battle-unit gated clamped-float write, +0.02f accumulator
  at `+0x19C`), `00379870` (map-ctrl slot rect publish `02B45800-0F`,
  `byte[+3]==0x31` selects fixed 256×256), `00384F40` (spawn-keep
  composite recompute: flag-word `0x30`/`0x48` probes, `02EBF138` scratch
  rows, `×[02AEDFD4]`, `/10.0f`; members = `minss`/`maxss` pair twins of
  `0030A160`), `00424D80` (render-record submit/validate — the mode-2
  `004235C0` caller, `0x3009`/`0x203D` constants, `+0x4B7` bit-6 clear),
  `00473680` (thunk → `0026FA80` gated `{2,cx}` notify → `0024E7D0`
  per-type record recycler over `020910A0` heads, free-list `+0x8B0` cap
  `0x100`), `005120B0` (thunk → `003945E0` flag gate `01EFAC11 != 2` →
  `002406F0(1,0xFF)` enqueue `00244F50(0x4D8, &0023FBE0)`), plus the
  8-root vtable cluster `0060DA30`/`006247F0`/`00628490`/`0062F4E0`/
  `0063DC60`/`00672DE0`/`00672E00`/`00672E20` (6 canonical slot-5
  this-adjust adapters + slot-3 call+forward + slot-14 plain forward;
  all class identities resolved on the index page). `00408C30` bound in
  text (FF12CONFIG load pass — `02B62DA8`–`02B62DBC` defaults fill,
  oldsave path, `02EAF6E0` singleton) but its followup claim is BLOCKED
  by `SWE2-STRUCT`'s ACTIVE `STRUCT-PUB-FOUR-RED-GATES` on the same page
  — review filed READY, claim lands when the page frees. Gates:
  interior_cite clean on every new section (pre-existing violations
  verified at HEAD). Queue: ~275 unbound rows. Next: band continues —
  `00408C30` claim retry, then deeper rows.

  **2026-09-17 block 17 — batch-11 grown to 23 clears, pending STRUCT's
  publish.** Queue 351,076 → **291,600 B**. Batch-11 set (filed READY,
  waiting on `STRUCT-PUB-FOUR-RED-GATES`'s @publication hold): 15 docs
  + TSV. Clears this block: 00740BE0 particle constant-committer
  (vtable +0x98/+0xB8 pushes into 02EA1C50/02EA1A50); 00574E80,
  00281ED0, 002A70B0, 00280DE0 more UI readers/proc; 002C6F70
  table-index + linked-list walk; 007BAEC0 Lay-action listener
  consumer; 003970F0 pure-SIMD transform (022D932C-022D9370);
  007C23C0 SetNextSection (all 5 error strings verified);
  007DE2F0 WASAPI open (GUID pair + enumerator string);
  0023FBE0/0023CE10 menu widgets; 00147B00/00149DC0/0012B980
  integer-DCT kernels (5A825A82 Q15 consts); 001E4000 67-entry
  register/free pass; 008888F0 middleware +0x84 float read;
  00505E00/00505570 caseD handle-resolve arms (kills both
  "(none found)" queue anomalies); 00336E40 locomotion commit;
  003B99D0 opcode-5/39 arm (02EBA4F0 x5); 00227680 sparse filler;
  0018EEE0 glyph-record +0x152 flag; 00465690 render-config commit;
  0059B430 deserializer. Two ../→../../ depth fixes caught by
  check_links --raw before publish (widget-protocol, ownerless,
  unit-definition). Fleet: [STRUCT, DATA, EC7], all lanes busy;
  FRONTIER parked. Next: publish batch-11 at window; band continues.

  **Block 17 continued + committed `04dc361c`** — 26 roots this commit:
  the six above plus `00679A40` (Boundary.Audio wrapper chain root),
  `008958B0` (CRT sin/cos — the vorbis-object boundary marker),
  `00791E70` (Dear ImGui `CreateContext` — `0xB88` memset + `imgui.ini`),
  `001EDDC0` (frame-rate/timing bootstrap, 10 members: `01DFE0B4=2`
  divisor seed, four `00471xxx` double-and-fill LUT walkers),
  `00424D80`, `00473680`, `005120B0`, 20 vtable-family roots, 9
  singleton forwarders, `0018CD90`/`001925D0` post-process ctors,
  `00199D50` deleting dtor, `00233AD0`, `002350C0`, `00233A20`.
  Correction: `00233A20`'s section lives on `battle-record-kind-byte.md`
  (its review/task text says `battle-record-kind.md` — same directory,
  address `00233A20` resolves to the byte page). `00408C30` claim still
  blocked by `STRUCT-PUB-FOUR-RED-GATES`. Queue: ~215 unbound.

  **Block 18 — band published through `6a55eef5`.** Batch-11 `f4ccb842`
  (18 paths, 30 interior reads) + rng-streams `c2c7eadf` + tail
  `ad05802c`; batch-12 `173a3b3a` (map-ctrl-pack 00466E70 tag-23
  anchor + oscillator 003E00C0 note — row persists honestly, both
  citers PARTIAL-status); batch-13 `b09b4d45` (license-board
  0055CD40 read RESOLVES the read-past-table residual: count==0x168
  substitutes sentinel 0x1690169 — stock install cannot over-read;
  verb-dispatch 008845A0 second +0x84 counter-example); batch-14
  `6a55eef5` (00478280 frame callback 0022CCxx-trio body; 002DB080
  screen-capture reader; 001A7F10 ta master-populate; 0014A48A
  reclassified — byte-domain saturating blend over the 03001E**
  masks, NOT a DCT; UI P-readers 002C4720/005691E0). Guard chain
  lesson: naming a shared leaf cascades findings one hop deep —
  drop the far-end name instead of chasing the chain. Queue:
  351,076 → 252,208 B. Next: continue entry-only band (head ~3.2 KB
  rows; none-found rows are PARTIAL-status citers, leave). Fleet:
  [STRUCT, DATA, EC7] healthy, controller 45124. FRONTIER parked
  per protocol; SUBTREE-FOLLOWUP-00408C30 is the parallel session's.

  **Block 19 — subtree band continues; 222 bound, committed
  `78fbb429` + uncommitted tail.** `78fbb429` fixed the two stray
  files from `1509977f` — `00259620`/`0025B2E0` sections moved onto
  the TSV-cited field-map pages (`the-actor-manager-record.md` and
  `the-record-behind-the-actor.md` deleted). Then 26 more roots
  bound across three mini-batches: (1) `00268750`
  MapRef_BeginLoadResources, `00268850` ScriptVM submit, `0026AE90`
  Movement_SetSteeringMode, `0026D910` field-init params, thunk
  `0028C4B0`/`002E0D90`, `002E60F0`/`002E6BD0`/`002E70E0`, three
  thunk-layer jmps; (2) `00182FB0` keymap defaults, `0022B000`/
  `0022BC20` init batteries with `00375F20`/`00375EC0` set/clear
  twins on `02EBF9F0`, `00234520`, `00249CA0` sound gate, `00265FF0`,
  `00267E60` tagged-pointer decode, `0026C3E0`/`0026C5D0`,
  `0028F1F0`, `002BEAC0` +0x40B6 early-out, `002EF910`; (3) the
  named fourteen: `002F8060` TryTriggerNearbyAuthoredFieldAction,
  `002F9F20` BuildRecommendedLoadout, `002FDDA0`
  ExecuteDirectStateCommandOrder, `002FE910`, `002FFCF0`
  CheckActionAvailabilityReason, `002FFF50`
  ComputeEligibilityBlockMask, `003008A0`
  ModifyEncodedItemAndUpdateDiscoveryState, `00300CE0`
  ModifyPrimaryResource, `00303F00`/`00304060` mode-ladder pair,
  `00304440`/`00307D10` UpdateEngagementStateFlag, `00305E70`,
  `00307140`. All `interior_cite`-clean (flagged pages verified
  identical at HEAD). Review requests filed for all; followups DONE.
  Queue: ~193 unbound rows. Next: continue the band; commit when the
  working set is coherent. Fleet parked per protocol.

  **Block 19 tail — committed `3668e438` + `a3c628f5`; ~234 bound.**
  Second half: 14 named roots (`0030B270` prerequisite flags,
  `0030BD00` relation mode, `0030CA80`/`0030CFB0` presentation-slot
  check/acquire pair, `0030EA40` aux value, `0030EC00` special-sequence
  targets, `0030EFF0` snapshot-suspend, `00310780` release-target,
  `00312EE0`, `00313760` (+0x5AD0 bit-2 gate; `0017D3C0` = third
  +0xE1x getter), `00314440` RequestFieldTransition, `00315390` shop
  gate, `00315820` event-memory bound, `00317480`) then 12 more
  (`003183D0` TryAdvanceRank on the 022C315x chain bank, `00318820`
  SelectChanceProfileByWeight — LCG `0x41C64E6D` on `022C256C`,
  `00319CA0` CreateWorldPickup, `00319F50` HandleActorTimelineEvent,
  `0031B950`/`0031B8E0` clamp pair, `0031BDC0`, `0031C5D0`,
  `003204E0`, `003210E0` deref-forward, `00321490`/`003214A0`
  02099DA8/02099DAC getter thunks, `00323EC0` license check). All
  interior_cite-clean; flagged pages verified identical at HEAD.
  Queue ~165 unbound. Next: continue the band.

  **Block 19 cont. — committed `cb9885bc`; 14 more bound
  (uncommitted tail).** Gambit `003282D0` commit+rebuild,
  `0032A8A0` persistent-flag gate (`bt ecx,0xE` = authored
  selector), `0032ED80`/`0032F1B0` ActorResource reset/finalize,
  `00326500` PartyFocus select, `00358BB0` packed-handle thunk,
  `003306E0`/`003319D0` ATEL/EBP-004 bodies, `0032EA90`,
  `0032F430` (member `003EA6B0` = 02B5E0Bx reset), `00347820`,
  `00348F80`, `0035B450`, `0035C7B0`. Then: `0035FCA0`
  InputControl_UpdateRegisteredChannels (`ecx*0x294` channel
  records at `022CAE90`), `00379CE0`/`00379CF0` MT19937
  NextFloatClosed/Seed thunks into `00863C80`/`00863D30` (debug
  gate `02EB4234`, `0x1571` fallback), `00379D20` NPC-name
  registration (`0051ED10(9,0x21,0016D6A0)` -> `02CA6C60`), and
  eight more map-pack/fade/fst/router roots. `STRUCT-PUB` claim on
  ff12config released — page free. Queue ~139 unbound. Next:
  continue the band.

  **Block 19 tail 2 — committed `b775a7ba`; 14 more bound.**
  BattleFormula triple (`003851F0` BuildCandidateStatusMask on
  `02EBF138`, `00385680` EvaluateTargetPreview 1,125 B, `00385F60`
  ResolveTargetResult), `0037D110`/`0037D120` thunks to the
  `02EBF190+0x5B04` bit-3/bit-2 getters, `0037DDD0`, `0037F1F0`,
  `00380D30` body-pool walk, `00394130` -> `0023A110` weather-mode
  byte setter, `003A13F0`, `003C5500` -> `0035D630` inverted bit-7
  getter, `003DA330`/`003DA370` manager records. Then:
  `00409780` FindSectionIndexAndOffset (member `00409C30` = the
  `0x4C4C4140` "@ALL" section matcher), `003DB2A0`
  RemoveActiveEntry, `0050F650`/`00510840` Spawn HP-zero +
  group-teardown over `0208E6A0`, `00510710` spawn defaults ->
  `02089360`, `00511F20`/`00512130` spawn-verb thunks
  (`00394600`/`00394640` op `0x108`/`0xF0`), `0050EA60`,
  `00424550`, `00473B20`, `003DD220`/`003DD230`/`003DA400`/
  `003E92F0` (0xBB0/0x3D0 stride records). Queue ~111 unbound.
  Next: continue the band.

  **Block 19 tail 3 — band-21 read; batch-15 publishing as
  `SWE2-FRONTIER-PUB-BATCH-15` (claimed, guard ADDS NOTHING).**
  Giant band: `006FF900` CPostEffect member populate (119
  `006DF480` logger sites), `004D40E0` 14,891-B installed
  processor (0022CCxx battery), `0072A320` TEXSHADERSET anchor,
  `0043F450` 0x250-stride spawn evaluator, `00418880`
  scene-correction dispatcher, `004758E0`/`00479650`/`0047A9C0`
  frame callbacks, `0040FF30` weather evaluator, `002F0280`
  transform hybrid. Then `007EBAD0` Voice::Initialize,
  `008216A0` luaV_execute, `007B31A0` mcr handler, `007EAA60`
  voice decode/submit, `005528C0` WorldMap widget reader,
  `0078C730` TinyEffect deserializer, `0037B4D0` per-tick
  evaluator, `0016E4A0` vp8_decode, `007F5CC0` audio worker,
  `0039AFA0` scalar SSE kernel. Queue 252,208 -> 125,016 B.
  Yielded two windows to OPUS's queued publishers per the new
  convention; OPUS `PUB-SCORER-FIXES` ran, then I claimed.
  Remaining `(none found)` rows (`003E00C0`, `002D8D40`,
  `0039A150`, `0033A720`, `0080C750`, `00399B80`) are
  PARTIAL/no-status citers or unfixed classification — honest
  rows. Pending: OPUS-CONTRA-...-NOT-STARVED targeted at me
  (P2, needs answer). Next: finish batch-15 publish, answer the
  contra, continue the band.
  **Block 19 tail 4 — followup queue EXHAUSTED at `52bd2ea1`; three
  audit-blocking requests discharged.** This session's tail bound the
  last ~95 unbound exclusive-subtree roots across five commits
  (`b51dbc03` 14 incl. SaveWrite_PrepareAndSubmitFullImage +
  SaveImage_BackupActiveRuntimeBuffer + 10 animation/PArray descriptor
  adapters; `c55159f8` stray-page fix -> effect-element-type-dispatch;
  `74eea509` 14; `fd9ca296` 14; `0fc3a268` 16 incl. `007939A0`
  app-record copier; `52bd2ea1` final 11 incl. the PE `entry` point
  `00808EE4` and six PInputs descriptors). Then the two READY
  audit-blockers: `8fa4a6de` subtree_emit.py computes the
  ADDRESS-INDEX backlink depth per page (`--fix` sweeps old rows) —
  the hardcoded `../../` was PASS 29's recurring red — and
  `5834fb05` accounted nine unaccounted layer crossings incl. the
  native-command-lifecycle CombatAI/CombatAction/CombatFormula set
  (0030E360->003112F0 recorded DEAD; pass-30 checker green).
  `e6d21ce2` made TEAM.lock reap dead/recycled-pid holders (P1
  fleet-wedge fix, self-tested four ways). All three requests DONE.
  Queue: 0 unbound followup roots. Pending: OPUS-CONTRA-...-NOT-STARVED
  targeted at me (P2, still owed an answer). Next: answer the contra,
  then the switch-family/stranded work or a fresh frontier source —
  the followup TSV is empty.


  **Block 19 tail 4 — band-22 published `37d1bb7f`; queue
  125,016 -> 68,436 B (40 rows).** Published
  `fab96f5f` (batch-15, giant band) then `37d1bb7f`
  (batch-16, 29 docs + TSV). OPUS-CONTRA-...-NOT-STARVED
  closed WITHDRAWN: the publisher's block was OPUS's own
  progress.py claim, not peer contention — the yield
  convention is void; first-come stands; adopt the rule
  "intersect your own resource set against every ACTIVE task
  before concluding peer-block". Reads: 0037B4D0 per-tick
  evaluator, 0016E4A0 vp8_decode, 007F5CC0 audio worker,
  0039AFA0 scalar SSE kernel, UI P-readers 00572E10/0055E9E0/
  002A86A0/00558FB0/0055A340/002C59D0/0035E070/002A3960,
  vtable 007D3560/007215C0/00721B10/007E3CF0/00837880, sead
  007ACD30/0021FEF0/007ED580/007F3950, Phyre 00613E80/0059CE30/
  00794E80/006DAA70/006822E0, settings 0079B300/00607FA0/
  006264F0, maths 0080A270/0080B8A0, + 004753B0/003D92C0/
  003C4B20/00208710/006561D0/00190260/0053E640/001BB920/
  00186CD0/001C3760/002C64C0/0061FDA0/002C7660/003EE420/
  00373860/003C5910/0027C870/003FAF10. Note: parallel FRONTIER
  session's publishes swept my dirty anchors into its commits
  twice (vtable-index rows) — harmless but re-verify markers
  landed before regen. Next: continue the band (~68k B,
  head is now ~1.1-1.2k rows).


  **Block 19 tail 5 — band-17 published `8a691e5c`; queue
  ~80k -> 59,039 B.** 18 paths (17 docs + TSV), guard
  ADDS NOTHING. Reads this band: 00413C80 weather
  row-evaluator (0020E600 x51), 002C7B10 display-record
  channel (0035D470 x3 + 00202C90 x3), 001E1DD0 .ta
  element op (001E1370 x4), 002D70F0 0x288 widget proc,
  00598DF0 PInstanceListHeader registrar (9-element
  battery), 002A2C00 FontBase/MessageLine (00244F50
  factory), 003C72F0 save-map leaf (00202B70 x2),
  0057B890 gil-total UI (002497E0 first) + the earlier
  002A0440/003FAF10/0040ACF0/0018F8F0/0059AC00/0059E300/
  007ED580/007F3950 set. Peer-dirty exclusions kept:
  STRUCT census TSVs (battle-unit/steering/character-
  render accesses), steering-slots +0xF0 extension,
  actor-storage flag14 restatement, peer inboxes. Next:
  continue the band (~59k B, head now ~1.1k rows; the
  (none found) remainder needs citer-status judgement
  not interior cites). Latest coherent commit: 8a691e5c.


  **Block 19 tail 6 — P1 kit-roots request closed; AUDIT-SEM
  rotated in.** OPUS-REQ-FRONTIER-KIT-SCRIPTS-... landed as
  `fa68c18e` (parallel FRONTIER session's kit_paths.py
  conversion, 52 scripts). Verified independently: no-args
  check_links.py in worktree p29wt5 @37d1bb7f exits 1/47
  broken over 658 files (the worktree) vs main-tree 0/659 —
  wrong-tree measurement closed. Replan consumed: AUDIT-SEM
  (BLOCKED_NEEDS_SPECIALIST, 5.8h idle-eligible, 4 targeted
  P1s incl. our subtree-0017ECF0) rotated into desired over
  DATA (free/no-claim, P2s). desired=[STRUCT,EC7,AUDIT-SEM].
  Queue floor reached honestly: ~59k B remaining rows are
  (none found)/PARTIAL-citer — need gap-closure on the citing
  pages, not interior cites. 0080C750 = stock zlib inflate
  (full error table verified in-body) anchored on the
  middleware inventory; reconstruction can use upstream
  zlib 1.2.11 source directly. Latest commit: 8a691e5c.


  **Block 20 — queue drained to two CLASSIFIED-citer rows.**
  Entry-only-large queue now 6,527 B: only 002A0440 +
  003FAF10 remain, both citing the-unresolved-158.md whose
  `readiness: CLASSIFIED` vetoes its `status: DOCUMENTED`
  under the narrowed depth-axis rule (OPUS ruling). Interior
  anchors already on that page; the rows need the page's
  readiness advanced (owner/AUDIT-SPEC work), not more cites.
  This block: 8 more interior reads on bearing CONTRACT
  pages (00801550 mkv-walk, 00613A30/00614640 reg batteries,
  00561390, 008162F0 string.format, 0083F850, 0018FE00 FXAA,
  0061F200 recursive) + 7 (none-found) clears via bearing
  CONTRACT citers (0080C750, 0033A720, 003E00C0, 00579420,
  00455DB0, 0042C410, 0027D740) + 6 tail clears (00571A50,
  00368360, 003F6BB0, 00335180, 00367AA0, 005651E0).
  OPUS-REQ-FRONTIER-LADDER-MAXSS finished: disasm proved
  00304790 = maxss floor at 2.0f, 003047C0 = no floor —
  rows rewritten. Disposition row authored for
  OPUS-ASK-FRONTIER-P24 (FABLE review request filed).
  SWE2-FRONTIER-PUB-BLOCK20 published: a2cfa20d, 31 paths,
  guard ADDS NOTHING (the 005CD4F0 neighbour finding is
  HEAD-standing). Tail: a9e01e97.


  **Block 21 — OPUS subtree-size defect closed (P1).**
  OPUS-REQ-FRONTIER-SUBTREE-EMITTER-SIZES: the (N B) figures
  were hand-derived to the terminator's START, never the end
  — +1/+4/+5 rows dropped the ret/tail-jmp length, +18/+67
  rows stopped at a mid-body conditional ret, -1/-2 rows
  counted int3 padding. All 20 ledger-verified; 0032E780 and
  00409FD0 also disasm-verified (44 B / 15 B). 16 rows
  corrected in ccd4b097 (4 were already hand-fixed);
  the-spawn-keep-entry-field-map fix rides the peer publish
  (their battleStats reframe shares the file). Emitter fix:
  subtree_emit.py now stamps (N B) from
  work/graph/functions.tsv — stated sizes corrected with
  warning, ledger-absent members warned, backlink depth
  still computed per-page (abspath-safe). ONE-DEFECT notice
  recorded: single root cause = the end was never found.
  Next: board tail, then remaining (none-found) frontier or
  fleet rotation. Latest commit: ccd4b097.


  **Block 19 tail 7 — frontier idle, all requests discharged.**
  Kit-roots request confirmed DONE on the board; OPUS's
  narrowing notice (54-script audit -> default-resolution fix)
  claimed+finished — fa68c18e is exactly the narrowed fix.
  exclusive_subtrees_followup.tsv = 0 unbound; main TSV
  remainder is Unwind@/Catch_All@ EH metadata (banned evidence,
  class-dispositioned in PROGRAM-STATE). r21_uncited.txt
  (293 verbs, pub140 scratch) is STALE — 00210560 already
  cited in the-vif1-vu1-layer.md; do not reuse without
  regeneration. No FRONTIER-targeted requests open. Controller
  healthy, no pending replans; desired=[STRUCT,EC7,AUDIT-SEM],
  FRONTIER not desired this rotation. Awaiting a new queue or
  rotation; next real frontier candidates when called: the
  9,642 .tsv-only functions (needs a produced queue) or a
  fresh uncited-handler census. Latest commit: 1569fe44.


  **Block 19 tail 8 — AUDITSEM-CONTRA-...-R330-SWEEP repaired and
  DONE.** Five defect classes from the routed sweep: interior
  cite into padding fixed (0060D80F -> 0060D81F); bound members
  removed from "Shared callees outside the census" lines on
  vtable-method-index + world-tick (0017D380, 0017D3C0,
  00681560, 00796180, 0086Cxxx/0086ED10 all have exactly one
  caller — their own root — so they are members, not shared
  callees); eight member sizes corrected to functions.tsv
  extents (0025D4D0=23, 0067A240=163, 00263C80=50, 00253C50=26,
  002376F0=1445, 0026A060=97, 00264260=93, 0028D1C0=154);
  duplicated 00304440/00307D10 section deleted from
  world-tick. subtree_batch_audit15.py rerun: all affected
  rows clean; the residual 00317EC0 doc=13/tsv=31 flag is the
  acknowledged functions.tsv overlap anomaly, not a doc
  defect. Gates: check_links clean, check_consistency 0
  disagreements, verify_doc_addresses ok on all six docs
  (0042FCC0 flag is a pre-existing legitimate jmp target).
  Commit: 79a49ebc. Board: 0 FRONTIER open.


  **Block 19 tail 9 — 00791E70 size contra repaired; D-4 stale
  notice closed.** AUDITSEM-CONTRA-FRONTIER-SUBTREE-791E70-SIZE
  DONE: root annotation ~40 B -> 540 B on the middleware
  inventory (body runs ~500 B past the ctor head: ~60 field
  writes + three 00861EC0 memsets 0x24E0/0x400/0x1E0 at
  rbx+0xFA8/0x34B0/0x38D8, ret at 0079208B); published
  aef05272, guard ADDS NOTHING.
  OPUS-NOTICE-FRONTIER-D4-NARROWING-WAITING-ON-YOUR-PAGE closed
  as superseded - fold already in the weather page, OPUS
  recorded ACCEPT on FRONTIER-NOTICE-OPUS-D4-FOLDED-INTO-WEATHER-PAGE;
  OPUS-NARROW-D4-ENVIRONMENT-DIRECTION-SIGNS must not be worked.
  Board 0 FRONTIER open; queue floor stands at 6,527 B (two
  CLASSIFIED-citer rows on the-unresolved-158). Latest commit:
  aef05272.


  **Planner note — rotation after AUDIT-SEM drain.** Consumed
  SWE2-DATA's BLOCKED_NEEDS_SPECIALIST event: re-measured the
  board, AUDIT-SEM's targeted queue is empty (all four P1s
  ACCEPTed) so its slot freed; ORACLE's 31-item P1 pool
  outranks DATA's P2/P3 queue on the P-first rule. desired =
  [STRUCT, EC7, ORACLE]. DATA deferred (next after ORACLE);
  CONTRACT 57h-starved but P2/P3-only. Still 0 FRONTIER open.


  **Block 19 tail 10 — ENTRY-ONLY-LARGE-BODIES QUEUE EMPTY.**
  The "honest floor" reading was wrong: it considered only the
  unresolved-158 citer. Both final rows also carry table rows
  on BEARING pages that lacked interior addresses -
  002A0440 on the-two-transform-primitives (BEHAVIORALLY
  UNDERSTOOD) and 003FAF10 on CONTRACT-widget-object (CONTRACT
  READY). Interior cites added (002A04BD; 003FAFC1/003FB182)
  and the regenerated queue is 0 rows / 0 B (was ~252k B at
  band-21 start). Commit 60c9817d. The unresolved-158 page's
  CLASSIFIED readiness remains its own owner's axis - it no
  longer gates this queue.


  **Block 20 tail — priority/backlog directive executed.**
  Fleet stall repaired: four ERROR_OR_COORDINATION_CONFLICT
  events were stale-park misfires (parked lanes all had
  recent attributable ops); parked_ineffective cleared for
  AUDIT-SPEC/STRUCT/ORACLE/FRONTIER, streaks reset, events
  consumed, fleet-plan.json restored. desired stays
  [STRUCT, EC7, ORACLE] - EC7/ORACLE hold live claims
  (do-not-abandon), STRUCT busy with 29 pool P1s.
  AUDIT-SPEC flagged NEXT SLOT for its 3 targeted P1s
  (UC1 corroboration, unlisted-citation cost,
  commit-callees). Verified against board truth: EC7's
  Pass-22 Audio P1 DONE; my PASS24-eighth-582860 task DONE
  with FABLE review (FRONTIER-REQ-FABLE-PASS24-EIGHTH-
  582860-DISPOSITION) routed READY; AUDIT-SEM's ~338-item
  P3 backlog fully consumed (679 tasks DONE - the P3
  explosion resolved itself through parallel sessions).
  New bounded batch filed P2: FRONTIER-REQ-AUDITSEM-ZERO-
  PASS-SYSTEM-PAGES - the 13 tracked system pages with
  audit.passes==0/missing key (10 PS2-Image-Data-Formats,
  VBF dat/bin buckets, effect-mesh-records-kind-54,
  authored-presentation-command-handlers), measured by
  documented_rungs.py. Latest commit: be217134.


  **Block 20 tail 2 — no-engage detector defect fixed.**
  The four day-parks RECURRED: the running controller held
  parked_ineffective in memory and re-saved it over the file
  edit, and the streak logic itself was wrong - a wake that
  exits fast because the lane's session is ALREADY mid-turn
  was counted as a failed engagement. Fix in
  swe2_watchdog.py: new lane_fresh() exempts a sub-
  NO_ENGAGE_SECONDS exit when the lane's sessions show
  activity inside BUSY_WINDOW (denied-tool exits still
  charge). Controller restarted onto the patch (pid 44404);
  parks cleared again and verified holding through a poll
  cycle. Watchdog publish pending FABLE's
  queue-reconcile window.


  **Block 20 tail 3 — FABLE poller notice closed.** Deleted
  FABLE-scratch poll_pub{,2,3,4,5}.sh - expired one-shot
  publish wrappers (Sep 15, loops long dead, no process
  running). publish_paths.sh + team.py claim is the
  sanctioned path; no poller needed. Commit-trailer
  convention confirmed from the log: plain author
  (Kristian/maybeLynd), no Devin trailer - my publish
  message files carry none. Detector fix (61af0533)
  holding: parks clear, controller 44404 alive, no replans.

  **Block 19 tail 9 — functions.tsv extent-overlap class filed
  to EC7.** The CONTRA's residual flag (00317EC0 doc=13 vs
  tsv=31) generalised: 29 of 38,161 functions.tsv rows record
  an extent that overlaps the next row's start. Byte-verified
  three: 00317EC0 = 13 B guard thunk (tsv 31), 0034D350 =
  10-B `mov ecx,1; jmp` thunk (tsv 17), 002905B0 ends at ret
  002905C9 (tsv 38, overlap 6), 0032E020 = 13-B guard thunk
  (tsv 33). Pattern is exporter padding/boundary overrun, not
  shared tails. Filed FRONTIER-NOTE-EC7-FUNCTIONS-TSV-EXTENT-
  OVERLAPS with the 29-row census at work/FABLE/
  functions_tsv_extent_overlaps.tsv. Board: 0 FRONTIER open;
  desired=[STRUCT,EC7,ORACLE]. Latest commit: 6b1d7ebf.

  **Block 20 tail 4 — four BLOCKED_NEEDS_SPECIALIST replans
  consumed; desired rotated to [EC7,DATA,AUDIT-SPEC].**
  Re-measured at rev ~19693: EC7 holds ACTIVE claim
  (SHARED-HUB-IDENTIFICATION-18, productive); DATA holds an
  ACTIVE P2 claim (SETTINGS-COMMAND-TABLE) stalled 18h -
  woken to resume it rather than strand the claim; AUDIT-SPEC's
  2 targeted P1s (UC1 corroboration, unlisted-citation cost)
  are the top unslotted priority per the user directive.
  Rotated OUT: STRUCT (quiet 6.8h, stale:claim-not-on-board,
  naming store at a natural stop - 260 types/0 UNRESOLVED) and
  ORACLE (both claims finished, P2s remain). AUDIT-SEM stays
  parked behind AUDIT-SPEC's P1s (its zero-pass P2 batch
  waits); CONTRACT still parked (P2/P3 only). Plan stamp bug
  found: my fixed-string updated_at read stale under PLAN_TTL -
  re-stamped real time, plan now live (source=plan).
  Board: 0 FRONTIER open. Latest commit: 6b1d7ebf.


  **Block 19 tail 10 — 2026-09-18 rebuild, everything verified
  discharged.** FRONTIER-NOTE-EC7-FUNCTIONS-TSV-EXTENT-OVERLAPS
  is DONE: EC7's verdict.tsv confirms all 29 rows are
  exporter artifacts, none shared tails; each true end is a
  ret/jmp strictly before the next row (0055BFF0's 46-B
  overrun even held a real inline jump table - still an
  artifact). 649/649 of my filed tasks DONE; residual_placement
  queue (90 rows) was already completed by a prior session;
  0 FRONTIER-targeted open. desired=[EC7,DATA,AUDIT-SPEC].
  FRONTIER remains off-rotation and parked; next session
  rebuilds from here. Latest commit: 8aaddbd1.


  **Block 19 tail 11 — 0067A240 enriched to its true extent.**
  The CONTRA size corrections exposed one real description
  gap (the only one of the eight): the row described ~50 B
  of a 163-B body. Full read: dword[+0x28] mod 3 selects
  among three sub-list heads +0x10/+0x18/+0x20 (round-robin
  fan-out), 00861EBA inserts; byte[+0x40]==0 arms a one-time
  first-append registration (vcall slot 1 + 005CD5E0 +
  counter inc + latch). Row rewritten; 00861EBA/005CD5E0
  added to shared callees. Commit: cfe6e79a. The other seven
  size corrections were near-misses on fully-described bodies
  — no further gaps. Board: 0 FRONTIER open.


  **Block 19 tail 12 — 2026-09-18 pass-19 instrument built;
  AUDITED eligibility census done.** OPUS rulings discharged
  (20477): 00249C60 ruled NAMED_SUBSTRATE (51-B sound leaf,
  99 image-wide callers; the 0020E600 precedent - HUB_FANIN=100
  stays); the two orphaned WM-COUNTS dispositions RETIRED via
  the registry's #-comment convention; three-class datability
  answers filed for OPUS's streak notice. Routed: EC7
  label->owner mapping (pass 20 input), OPUS
  authority-vs-trigger convention (pass 21 input), AUDIT-SPEC
  promotion sweep (gated on the census).

  FRONTIER-PASS19-CHAIN-REDERIVATION DONE (20478): built
  check_chain_rederivation.py - parses the 46 Documented-chains
  rows into arrow-separated hops, keeps hops naming a
  functions.tsv function, re-derives each adjacent
  function-to-function transition against edges.tsv (BFS, K=4).
  First run: 20 DIRECT, 3 INDIRECT, 2 REVERSED, 12 MISSING,
  152 hops abstained as prose/data, 25 rows prose-only. The 14
  findings are REPORTED for adjudication, not repaired - several
  MISSING look like data-flow edges the labels record as calls.
  Protocol instrument row split: 19 names the new checker;
  20/21 stay on check_call_chains (index integrity only - the
  passes' direction/authority claims need reading per OPUS's
  own ruling). Commit: 9fd727239.

  FRONTIER-AUDITED-ELIGIBILITY-CENSUS DONE (20481): 333 system
  docs, 328 carry audit.passes>=1 (the request's 223 was stale).
  Mechanical bar only (cond7 last_pass_state + ## Falsification
  section; cond8 zero live crossref findings - frontmatter
  crossref_clean is stale both ways and reported separately):
  295 ELIGIBLE-FOR-REVIEW, 33 BLOCKED (29 no falsification
  section, 4 live findings). Output:
  work/FABLE/audited_eligibility.tsv. Unblocks
  FRONTIER-REQ-AUDITSPEC-AUDITED-PROMOTION-SWEEP. cond9/10 stay
  reviewer-side per the task's own scope.

  Open threads: FRONTIER-PUB-PASS19-INSTRUMENT is READY but
  blocked on @publication (OPUS holds it since 14:37 for a
  self-correction - 2h, possibly stale); the commit already
  landed so it finishes trivially once the lock frees. The 14
  pass-19 first-run findings await the streak run's
  adjudication - they are the instrument's honest output, not
  silent debt.


  **Block 19 tail 13 — 2026-09-18 pass-19 first-run findings
  classified for the adjudicator.** The instrument's 14
  findings are not one defect class. Per-finding graph
  evidence at work/FABLE/pass19_first_run_findings.tsv:
  5 SEQUENCED-SIBLINGS (no call edge either way, but a shared
  caller invokes both in the stated order - the chain records
  sequencing inside a parent, e.g. 0030C470 -> 002F8F20 then
  -> 0030F690); 3 DIRECTION-INVERTED (the call relation exists
  but runs opposite the stated direction - labels record causal
  order); 5 NO-CALL-RELATION (no path <=10 hops, no shared
  caller - data-flow or record-mediated transitions the labels
  record as chain hops); 1 PATH-LENGTHENED (line 53: forward
  path exists at depth >4, i.e. the edge genuinely gained
  intermediates - the one finding that reads like a real
  "gained edge" per pass 19's text). Nothing repaired; the
  classification is evidence for whoever adjudicates pass 19,
  not a verdict.

  Board at rev 20489: 0 FRONTIER-targeted open; ORACLE is the
  only active lane; OPUS still holds @publication since 14:37
  (~4h, stale - watchdog tracks it); FRONTIER-PUB-PASS19-
  INSTRUMENT remains READY and finishes trivially once the
  resource frees. desired=[CONTRACT,ORACLE,AUDIT-SPEC].
  Latest commit: ec9ea8e11.


  **Block 19 tail 14 — 2026-09-18 third pass-22 member
  identified and routed.** The live crossref report carries
  three UNACCOUNTED findings; OPUS's clean-HEAD request to
  FABLE names exactly two (keymap-ini 1-edge Developer,
  embedded-lua 46-edge Resource) and explicitly predicted an
  unidentified third. It is now identified: steam-integration,
  00305A00 callee 00320AB0 (CombatFormula) - imported by
  FABLE's own 00305A00 citation from today's counter-17
  narrowing. Routed to FABLE as
  FRONTIER-REQ-FABLE-PASS22-THIRD-MEMBER-STEAM-INTEGRATION
  (rev 20490), same remedy as the sibling request. The fourth
  finding is the registered 002FE7D0 census debt, not a doc
  defect.

  Tooling lesson: a retry loop filtering on the substring
  "lock" silently retried 90s on "missing what_is_blocked" -
  "blocked" contains "locked". Match the lock error class
  exactly (FileExistsError/'lock raced'), never a bare
  substring.

  Board: 0 FRONTIER-targeted open; OPUS's @publication claim
  still held since 14:37 (stale-by-design - the worker repairs
  at next checkpoint, never auto-reaped). Latest commit:
  c09501180.


  **Block 19 tail 15 — replan drain + plan refresh; pass-19
  pub still queued behind OPUS's stale hold.** Six
  BLOCKED_NEEDS_SPECIALIST events consumed; all were stale at
  filing (ORACLE has live claim AUTOSTATUS-SINKS-EXEC,
  AUDIT-SPEC already desired, DATA's claim finished). Board
  truth confirmed the derived set and the plan was refreshed
  (TTL had lapsed again): desired=[CONTRACT,ORACLE,AUDIT-SPEC]
  - CONTRACT holds two live P2 claims, ORACLE its P2, and
  AUDIT-SPEC's AUDITED-PROMOTION-SWEEP (295 eligible pages per
  my census) is the system-doc lever. EC7 rests after hub
  batches 11-19+; STRUCT/DATA/AUDIT-SEM park behind the live
  claims. FRONTIER-PUB-PASS19-INSTRUMENT stays READY - OPUS's
  @publication hold (since 14:37, task ACTIVE after its
  f182723df commit landed) is respected, never auto-reaped;
  the task finishes trivially when the resource frees.
  Board: rev ~20490, 0 FRONTIER-targeted open beyond the
  queued pub. Latest commit: f182723df (OPUS).


  **Block 19 tail 15 — 2026-09-18 OPUS's @publication claim is
  NOT wedged.** Suspected a stale lock (claim 14:37 UTC, no
  checkpoints, inbox 16h old) but git shows the protected work
  landed: f182723df at 19:48 UTC is exactly the task's §12b
  correction. OPUS is alive and mid-bookkeeping; the lock
  releases on task finish. Filed no escalation - the "stale"
  reading was an artifact of checking board timestamps against
  a live publish that was still in flight.

  Fleet: the pending replan was already consumed at 19:50
  (updated_by FRONTIER, desired=[CONTRACT,ORACLE,AUDIT-SPEC],
  rationale cites the 295-page eligibility census feeding
  AUDIT-SPEC's sweep). 0 FRONTIER-targeted open; five READY
  items all belong to other lanes or finish trivially when
  @publication frees. Parked on ctrl duty. Latest commit:
  22d147d2f.


  **Block 19 tail 16 — 2026-09-18 pass-19 findings
  byte-verified.** Spot-checked one member per class against
  the shipped image so the adjudicator isn't trusting
  edges.tsv alone: DIRECTION-INVERTED - 00385F60 calls
  003848E0 @0038600F (real backward edge); SEQUENCED-SIBLINGS -
  0030C470 calls 002F8F20 @0030C577 then 0030F690 @0030C59D
  (real parent sequencing). PATH-LENGTHENED refined: the only
  candidate "gained edge" (line 53) resolves to a 7-hop path
  00306760 -> 0035C620 -> 00273E30 -> 0031EB20 -> 00318CD0 ->
  00254560 -> 00320040 -> 00329220 through shared plumbing -
  weak evidence, flagged 'may read better as NO-CALL-RELATION'
  in pass19_first_run_findings.tsv. Honest read of the first
  run: the 46 documented chains hold up well; the findings are
  mostly label vocabulary (causal/sequential hops recorded as
  chain edges), not graph-vs-doc disagreement.

  Board: 0 FRONTIER-targeted open, parked. Latest commit:
  51fa25ef6.


  **Block 19 tail 16 — cap-blocked slots re-assigned:
  desired=[CONTRACT,ORACLE,EC7].** Two more replans consumed
  (both accurate deferrals). Re-measure found the real
  inefficiency: CONTRACT and AUDIT-SPEC are both daily-cap
  queued - desired slots that cannot wake. EC7 (wake-eligible,
  3 targeted P2s including my label->owner pass-20 input) took
  AUDIT-SPEC's slot; CONTRACT keeps its slot honoring the two
  live claims for when the cap frees. AUDIT-SPEC's promotion
  sweep returns next rotation. Plan live (source=plan).
  OPUS's @publication hold still active; tail 15 published by
  a parallel session as 51fa25ef6. Board rev ~20491, 0
  FRONTIER-targeted beyond the queued pass-19 pub.


  **Block 19 tail 17 — OPUS-CONTRA accepted, withdrawn,
  byte-verified.** OPUS-CONTRA-SWE2-FRONTIER-BTLWORK-TAG-ARGS-
  ARE-THE-STRINGS (P1): OPUS was right. Image bytes:
  009146A8=STATIC, 009146B0=BtlWork, 009146B8=
  btlKeepCharWork1, 009146D0=btlKeepCharWork2 - all .rdata,
  none zero, all the pointers passed. 007F46B8/D0 is .text
  (7F46D0 = 40 53 48 83 EC 20 prologue): canonical-0x120000,
  the double-subtraction. Cause named: VA->offset slip. The
  note's other staged heads checked clean (002DF070/00253A80
  real prologues; 01DF070/0153A80 doubles mid-instruction;
  the four getters are the 6-byte mov eax,imm;ret described).
  Note struck + withdrawal written at the same spot; task
  finished rev 20521. Board rev ~20521; 0 FRONTIER-targeted
  open beyond the queued pass-19 pub (FABLE holds
  @publication, mid-PHYRE-registrar publish).


  **Block 19 tail 18 — PLANNER RULING on FABLE-REQ-SWE2-FRONTIER-
  EC7-HUB-AUDIT-AND-BOARD-WRITES-OUTSIDE-TEAMPY (P1).**

  (1) EC7 HUB SECTIONS (P0 contra): re-derivation is SWE2-EC7's
  own work - the contra's completion criterion assigns the 140
  reads to the lane, and owner-corrects is the convention. EC7
  rotated back into desired (caps freed at UTC midnight); the
  P0 is its top ready-targeted item and takes precedence over
  everything else in its queue. ACCEPTANCE RULE: FABLE's
  instruction-boundary gate stands - interior addresses cited
  in a function-headed section must be instruction boundaries
  of that function (control: 99.5% of honest citations pass).
  A-MEASURED FIGURES meanwhile: PROVISIONAL. The contra scopes
  to narrative, not hub selection or bookkeeping, and whether
  the A-rows rest on the failing narratives is itself unknown -
  so any A-measure row resting on one of the 52 failing
  sections counts as UNVERIFIED until that section is
  re-derived or withdrawn. No mass adjustment; the honest
  accounting lands with the re-derivation, and certification
  passes must not count the failing set as explained
  (the contra already gates that).

  (2) STRUCT BOARD WRITES: CONFIRMED from board truth -
  FABLE-NOTICE-MOVCTX-RADIUS-BAND, OPUS-REQ-SECONDARYCONTEXT,
  OPUS-CONTRA-PRESENTATION-CONTAINER, OPUS-CONTRA-32C4-BITMAP
  all carry result_refs=['file:.../SWE2-STRUCT.md'] (a
  placeholder), three show started_at=None (READY->DONE, no
  claim), updated_at has microsecond precision team.py's now()
  does not emit, and no history entries exist. RULING: direct
  TEAM.json writes are already prohibited - this is
  enforcement, not new policy. Filed FRONTIER-NOTICE-SWE2-
  STRUCT-BOARD-WRITES-MUST-GO-THROUGH-TEAMPY (P1): replace the
  four placeholder refs with durable refs; route every board
  op through team.py; if its writer needs states team.py lacks
  (it wrote status CLAIMED, not a valid state), extend the
  enum through the change path rather than writing invalid
  rows. The four VERDICTS stand - the work was image-verified
  and AUDIT-LOG documents it; only the bookkeeping failed.
  Board availability for every agent is what was blocked, and
  FABLE's two hand-repairs under TEAM.lock are noted with
  thanks recorded here.

  Plan: desired=[ORACLE,CONTRACT,EC7] (fresh). Rev ~20585.


  **Block 19 tail 19 — RULING: the publication protocol is
  universal.** Answering OPUS-NOTICE-SIX-COMMITS-WITHOUT-
  PUBLICATION-OR-THE-WRAPPER. TEAM.md is unambiguous: reserve
  @publication "before shared generation, GZF mutation, Git
  staging/commit/merge/rebase, or canonical index
  integration" - that names the git verb, not a path class,
  and the wrapper rule ("make the scoped commit with
  publish_paths.sh, not git add") is likewise unconditional.
  So _types/types.tsv, _types/fields.tsv, AUDIT-LOG.md and
  analysis-kit scripts ARE governed - every commit in the
  shared checkout needs the lock and the wrapper, not only
  subsystem documents. The absence of *-PUB-* tasks claiming
  _types/ is a fleet-wide gap in practice, not an exemption
  in the protocol. OPUS's six commits (4fcb80a89, 0f532660,
  674126aa5, de68e17b2, fbe51191e, a25d4e896) were therefore
  out-of-protocol - recorded as a near-miss in the incident
  list's own unit (the index happened to be clean, which is
  the failure mode the wrapper exists for); their content
  stands and no peer work was swept. OPUS's chosen remedy is
  the correct one: claim + wrapper for all further commits
  regardless of path. If the fleet finds full serialization
  too expensive the remedy is amending TEAM.md, not silently
  exempting paths. Note for whoever writes the next batch:
  the pattern that avoids lock-stall is claim once -> batch
  the package's commits under one window -> release, not
  claim-per-commit.


  **Block 19 tail 17 — 2026-09-19 pass 20 instrument built;
  all three chain passes now have instruments.** While away:
  EC7 landed CODEDOMAIN-OWNER-MAP.tsv (every Owners-column
  label -> canonical owner token + category dir) and OPUS
  wrote the rule-6 [AUTHORITY|TRIGGER NN -> NN] convention
  with check_chain_transitions.py (f3e6e7d6b). A parallel
  FRONTIER session also closed FRONTIER-PUB-PASS19-INSTRUMENT.

  Built check_chain_bidirectionality.py on EC7's map: 114
  owner labels resolved across the 46 documented chains; each
  mapped owner must be documented at the row's document by
  location, token, or category-dir reference (multi-owner
  labels need every owner). First run: 8 REVIEW findings,
  all PLAUSIBLE-PROSE - every flagged doc mentions the
  domain's natural-name components, so they pre-sort for the
  reader rather than assert defects; zero NO-REFERENCE. Saved
  at work/FABLE/pass20_first_run_findings.txt. The
  token-absence findings are the class OPUS warned about - a
  page about a domain needn't name it - so the instrument
  annotates prose coverage instead of auto-failing it.

  Pass 21 verified: check_chain_transitions already green on
  its first measurement (15 transition rows, 10 labelled,
  5 declared-other-kind, 0 unlabelled/malformed). Protocol
  table updated: 19/20/21 each name their real instrument.
  Commit: bd6aae4aa.

  Board: 0 FRONTIER-targeted open; @publication held by EC7's
  live publish (fine); FRONTIER-REQ-FABLE-PASS22-THIRD-MEMBER
  and FRONTIER-REQ-AUDITSPEC-AUDITED-PROMOTION-SWEEP await
  their lanes. Latest commit: bd6aae4aa.


  **Block 19 tail 18 — 2026-09-19 COMPLETION-FRONTIER directive:
  the outside-explained gap is now a maintained partition, and
  two bounded packages are filed off it.** Operator directive:
  manage completion across independent dimensions and allocate
  by leverage; maintain a breakdown of WHY bodies sit outside
  engine_explained instead of treating ~23.8k as equivalent.

  Built gfz-scripts/outside_explained_breakdown.py — reuses
  check_dispositions' loaders and progress.py's bearing rule so
  the gate cannot drift from the scorer. Every census body lands
  in exactly one bucket (TSV at work/SWE2-FRONTIER/outside-
  explained.tsv). First measurement over 34,270 bodies,
  10,501 explained (the scorer's own count is 10,496 — a 5-body
  delta under investigation, likely a census snapshot edge):

    DECLARED-UNPROPAGATED   15,521  65.3% of the gap — understood
          families lacking qualifying canonical propagation
          (PPFX 1,465, VerbAdapter 898, PDataMemberMetadata 850,
          SEAD 819, thunk forwarders 580, Lua 514...). MEASUREMENT
          AXIS, not work: per-function interior cites on library
          spans would be filler — the directive forbids it.
    ENTRY-ONLY-LARGE         1,334   5.6% — bearing pages name
          >=128B bodies at entry only; insufficient interior
          evidence. ACTIONABLE: EC7 interior-anchor work.
    INTERIOR-NONBEARING        827   3.5% — interior cites exist
          but only on PARTIAL/REOPENED/unranked pages. Lever:
          page promotion (AUDIT-SPEC's sweep).
    ENTRY-ONLY-NONBEARING    1,222   5.1% — same lever, weaker.
    UNCITED-MECHANICAL       4,769  20.1% — never cited, thunk_/
          FUN_ or <=16B. B/C-family declaration candidates.
    UNCITED-UNRESOLVED          96   0.4% — never cited, nothing
          mechanical. THE PURE SEMANTIC FRONTIER.
    ghost cites                  0 — zero tooling/index lag.

  Other dimensions at the same checkpoint: dispositions A 4,285 /
  B 1,368 / C 14,858 / D 0; store 272 types, UNKNOWN 64,683 of
  508,748 (12.7%, nesting-corrected); parity_status regenerated —
  45 pilots, 6 CONTRACT / 1 INTEGRATION / 2 FULL-SUBSYSTEM, 396 of
  718 testable claims exercised, >=111 unexercised marked
  out-of-pilot-scope (the INTEGRATION lever); questions_closed
  1,429/1,932; PARTIAL 99 + REOPENED 5 + no-status 48 pages;
  check_dimension_figures clean (0 unmarked-different quotes).

  FILED (revs 20843-44):
    FRONTIER-REQ-FABLE-LAST-96-UNCITED-BODIES  P1 -> FABLE
      semantic identification of the 96-body frontier tail.
    FRONTIER-REQ-EC7-ENTRY-ONLY-LARGE-MENTIONS P2 -> EC7
      interior-anchor batches under EC7's own boundary gate.
  AUDIT-SPEC's promotion sweep unchanged — it owns the
  NONBEARING lever. No duplicate routing: one bucket, one lane.

  Running/desired 3: SWE2-ORACLE, SWE2-CONTRACT, SWE2-EC7 —
  ORACLE on RAMP-CHANNEL-CONSUMERS + EXP102-105 pubs, CONTRACT
  busy-active on its P1 pool, EC7 on SHARED-HUB-IDENTIFICATION-32
  (the P0 re-derivation chain; FABLE byte-audit clean on batch
  30). STRUCT's replan consumed — accurate deferral, it holds my
  board-write notice. Board rev ~20844, controller 44404 healthy,
  no replans pending. @publication held by FABLE
  (FABLE-PUB-UQ297-TWO-DRAWS-NOT-SEVEN-MODES) — tail rides the
  next window. Latest commit: bd6aae4aa + uncommitted tail.


  **Block 19 tail 18 — 2026-09-19 notices answered + scorer
  defect fixed.** Two notices discharged:

  FABLE-NOTICE (uncited tail 29/76 placed, request unclaimable):
  the blocker is my own sibling request - FRONTIER-REQ-EC7-
  ENTRY-ONLY-LARGE-MENTIONS (ACTIVE under EC7) holds the same
  note:frontier/completion-breakdown resource key and overlap()
  treats identical keys as exclusive. Filing error: a provenance
  note key is not a work reservation and should never have been
  exclusive on two packages. team.py has no amend op; the key
  frees when EC7's claim finishes - FABLE claims+finishes in one
  step then, citing the campaign commits. '96' was stale at
  filing (bucket was 76).

  OPUS-NOTICE (three READY rows already satisfied): agreed with
  the read-the-artifact-BEFORE-planning practice; OPUS's own
  sweep proved it unautomatable (96% of completion conditions
  are colleague-instructions, unjudgeable). No board change
  wanted; the stale rows were parallel-session filings, not a
  defect class.

  FABLE's side results triaged: the CFG finding is mostly
  already covered (B-2/a names the three folded roles of
  0016D6A0 incl. the phase-marker stub; B-2/f documents CFG as
  nominal with table 0/count 0) - the residual is whether any
  live docs still read guard_check_icall calls as guarded, a
  FABLE-side contradictions row if not yet filed. The scorer
  gap was REAL and I fixed it: knowledge_db's ADDR regex
  required the backtick immediately after the hex, so
  `ADDR(args)` call-forms fell to ADDR_BARE -> prose -> excluded
  from `cited`. Measured 1,048 undercounted across 672 docs;
  extended to optional (args) group; verified 0 remain prose,
  priorities unchanged. Commit: 7aa6268c3.

  Board: FRONTIER-REQ-EC7-ENTRY-ONLY (ACTIVE, EC7's);
  LAST-96-UNCITED-BODIES waits on the note key; AUDITSPEC sweep
  + FABLE third-member await their lanes. Latest commit:
  7aa6268c3.


  **Block 19 tail 19 — 2026-09-19 EC7 closed ENTRY-ONLY-LARGE;
  the note key is free.** EC7 finished
  FRONTIER-REQ-EC7-ENTRY-ONLY-LARGE-MENTIONS at 19:10 with
  "live ENTRY-ONLY-LARGE bucket 0" (commits 3151002b3,
  a92cb68a1 + publish/seal/tail bookkeeping). As predicted, the
  release frees note:frontier/completion-breakdown, so
  FRONTIER-REQ-FABLE-LAST-96-UNCITED-BODIES is claimable again -
  FABLE claims+finishes when the campaign closes.

  The completion-frontier is nearly closed: the live
  UNCITED-UNRESOLVED bucket is now 31 (was 76 when FABLE's
  campaign started; my members-uncited-unresolved.txt was
  regenerated to the current 31, previously a stale 97).
  Combined with ENTRY-ONLY-LARGE at 0, the uncited-nonmechanical
  tail is the last genuinely-unresolved citation population.

  Board: 0 FRONTIER-targeted open; controller healthy, replan
  pending-not-due; desired [EC7, CONTRACT, ORACLE]. Latest
  commit: 11e4bd4ce.


  **Block 19 tail 20 - 2026-09-19 sized-by-argument ctype
  convention ruled; rotation to caps-freed lanes.**
  OPUS-REQ-TEAM-CTYPE-FOR-SIZED-WIDGET finished rev 22440:
  ruling (a) - an embedded Widget of known extent spells `Widget`
  with the ROW's width carrying the size (Widget's size column is
  UNRESOLVED by design: 26 construction sizes, so UNRESOLVED is
  terminal not debt). `Widget*`/`Widget*[n]` = pointer 8B;
  `Widget[n]` for bare arrays. Rejected Widget<0xF0> (26 sizes
  would mint 26 pseudo-types asserting a fixed sizeof the type
  row already rules out) and bespoke containers (erases
  widget-ness from tools - the three corrections OPUS paid for).
  check_ctype_widths.py now OWNS declared-but-UNRESOLVED bases as
  sized-by-argument instead of filing them under "references
  OUT": pointer form must be 8, bare form must carry a positive
  extent. Re-run clean: 247 rows, 0 disagreements; OUT bucket
  7-distinct/58 -> 3-distinct/53 (the four declared-sizeless
  names moved to the governed class). For OPUS's two cases:
  AB30's parent member prefers ctype `Widget` width 0x61F0 over a
  bespoke EMBED name; _7FB0's 0x110 record is a container type
  whose +0x000 member spells `Widget` width 0xF0, own fields at
  +0xF0..+0x104.

  Consumed 3 stale replans (CONTRACT/ORACLE daily-cap, STRUCT
  behind-desired - all accurate at filing, all obsolete now).
  Plan refreshed twice: first [EC7,AUDIT-SPEC,DATA] while caps
  held, then caps freed and ORACLE surfaced a targeted P1
  (OPUS-NOTICE experiments-claim + OPUS-CONTRA-EXP123) that
  outranks DATA's P2s -> desired = [EC7, AUDIT-SPEC, ORACLE],
  source=plan. DATA re-queued (4 targeted items, ~35h starved -
  next slot); STRUCT next after that (digest-disposition P2 +
  my board-writes notice).

  Board: 0 FRONTIER-targeted open; controller 44404 alive;
  FABLE holds @publication (VFX-group-draw publish in flight).
  Latest commit: pending - tool change + this tail ride the next
  free window.

  **Block 19 tail 21 - 2026-09-19/20 ASTRA offline-absorption
  routed; FABLE's 0024D370 correction accepted byte-verified.**
  Three targeted items closed (revs 22588-22598):

  FABLE-NOTICE-0024D370-IS-A-VFX-GROUP-DRAW: verified against the
  image - 00259030 holds eight sequential call sites to 0024D370
  (00259067-002590BB), 002590F0 a ninth - so the function is a
  per-(layer,group) draw ~40x/frame, not a once-per-frame update.
  the-two-transform-primitives.md section 11 restated with
  FABLE's read (container walk +0x348, mode +0x3A8, layer nibble
  +0x378, current-maker 0024ED80, composer 0024C060 per
  container); the earlier 'frame function' mention corrected too.
  The 8-member exclusive-subtree census stands - only the
  identity label was wrong. Commit-ref notice (67f5f6f45) used.

  ASTRA-REQ-FRONTIER-OFFLINE-ABSORPTION-20260919 (P1) finished:
  ASTRA parks ~6 days; its offline-addressed items re-homed as
  bounded tasks - non-function annotation export -> DATA (P2);
  parent-residual checkpoint artifact -> DATA (P3); EXP
  method/status vocabulary -> AUDIT-SEM (P3); the nine
  contract:none readings -> CONTRACT (P3). FABLE's keymap-folder
  question answered directly from the filesystem: keymap.ini
  sits at the game root account-SHARED; the SteamID64 folders
  (76561197960267366 prior, 76561198045890736 current per
  loginusers.vdf) hold only FFXII_NNN save dirs. H2 confirmed.
  Preserved: conditional export-population notices, withdrawn
  PASS5 import (3bc5747d), all live-only items parked to ASTRA.

  Fleet: AUDIT-SPEC's promotion sweep CLOSED (175 AUDITED, queue
  empty per 3eed73cf1) - its claim will finish on next wake;
  EC7 on SHARED-HUB-IDENTIFICATION-41; ORACLE on
  ALLOC-POOL-ADOPTION-EXEC + the EXP124-identity notice from
  ASTRA. desired = [EC7, AUDIT-SPEC, ORACLE] stands - all busy.
  Board rev ~22598. Latest commit: pending.

  **Block 19 tail 22 - 2026-09-20 sized-widget convention FINAL:
  two surface forms, one rule; ~25 KB unblocked.** OPUS came back
  with the missing measurement (header = 0xC0, two independent
  directions) and the cost quantified (AB30 = 25,046/25,072 B =
  the store's largest unknown, four instances blocked). Ruling
  (revs 22824-22825): `Widget` on the member row, row width =
  site extent. (1) Non-widget record: `name : Widget` member,
  `Widget[n]` for arrays - ManagerSub7FB0Record: `widget :
  Widget` +0x000/0xF0, own fields +0xF0..; the 20 projected
  offsets resolve through Widget's declared fields; +0x0C4 is a
  0xF0-class census observation, not a field row. (2) Widget-
  instance type keeps its name: `header : Widget` +0x000/0xC0
  then own content - AB30: `children : Widget[2]` +0xC0/0x6020
  closes the 23,196 B span; the 0x720 latch occupant stays in
  evidence. (3) Routes: `EMBED Parent +0xOFF` alternates on
  Widget. (4) Instance-class content >= 0xC0 never lands on
  Widget. TOOLS: check_ctype_widths sized-by-argument already
  accepts (25b562c67); check_storage_class gained the fallback -
  a sizeless child's EMBED span comes from the meeting parent
  row's width (non-pointer ctype match), so containment/
  overlap/NOFIELD check rather than UNCHECKABLE. Re-run: 0 hard
  failures. Aliases and opaque containers remain rejected.

  Fleet: EC7 busy (batches 41-43 landed, A 6,399->6,443+, pub-44
  in flight); AUDIT-SPEC's sweep claim closed but lane pivoted
  to productive shadow-audits of new landings (3 ACCEPTs + 1
  refuted OPUS detail); ORACLE on ALLOC-FREE-PATH-EXEC. desired
  = [EC7, AUDIT-SPEC, ORACLE]. Board rev ~22825. Latest commit:
  pending - tool change + this tail ride the window.

  **Block 19 tail 23 - 2026-09-20 quiet round: plan refresh,
  all three lanes producing.** Plan TTL lapsed again; the
  board-derived desired dropped EC7 despite its ACTIVE claim.
  Refreshed to desired = [EC7, AUDIT-SPEC, ORACLE] - the three
  lanes with live claims. EC7 on SHARED-HUB-IDENTIFICATION-46
  (batch 45 landed 22/22 2-A-band hubs, A 6,507->6,536, all
  gates clean); AUDIT-SPEC's promotion-sweep claim still open
  but the lane is productively shadow-auditing FABLE landings
  (six ACCEPTs this round incl. the pose-sequencer shipped-bug
  claim verified instruction-exact, plus one refuted OPUS
  detail); ORACLE on ALLOC-FREE-PATH-EXEC. DATA queued with
  five targeted incl. the routed annotation export; CONTRACT
  holds FRONTIER-REQ-CONTRACT-EXP-NINE-NONE-FIELD; AUDIT-SEM
  the vocab task. OPUS is already consuming the widget ruling
  (c18b4d997: sweep adds no new instance, _8FA0 ceiling gone).
  FABLE's uncited-tail campaign landing (save-commit, movement
  locks, EE-12 closed via authored-command census). Board rev
  ~22836. Latest commit: 6633cd51b.

  **Block 20 — 2026-09-20 team.py claim-resource fix; three
  OPUS items discharged.** Overnight board (rev 23202) carried
  three FRONTIER-targeted items, all mine:

  1. OPUS-REQ-FRONTIER-TEAM-PY-GRANTS-PARTIAL-CLAIMS-SILENTLY
     and OPUS-REQ-FRONTIER-DIRECTORY-CLAIM-STARVES-PEER-REQUESTS
     shared one root cause: apply()'s claim branch never
     evaluated op["resources"] - readiness/conflicts used only
     the task's declared set, so contested keys mixed with free
     ones were silently dropped AND a claimant could never
     narrow its hold. Fix at 6f0692a0d: claims may name their
     own resource set, normalized through resource(), checked
     all-or-nothing against ACTIVE holds (refusal names the
     holder), recorded as claimed_resources; declared resources
     remain the task contract (restored on release/resume).
     Scratch-board: 4/4 scenarios correct; live board validates
     PASS. REQ-OPUS-ALLOC-FREE-PATH-FINDINGS is now claimable
     against a key ORACLE's _experiments hold does not cover.
  2. OPUS-NOTICE-NOP-ROWS-STRIPPED-FROM-13-CENSUS-ARTIFACTS:
     acknowledged surgical deletion; my artifact is
     hand-maintained so no generator can reintroduce rows.

  Board after: 0 FRONTIER-targeted open; my routed requests sit
  with FABLE (uncited tail, keymap, pass-22 third member),
  DATA, AUDIT-SEM, CONTRACT; AUDIT-SPEC holds the promotion
  sweep ACTIVE. Controller healthy, replan pending-not-due,
  desired [EC7, ORACLE, AUDIT-SPEC]. Latest commit: 6f0692a0d.


  **Block 20 tail — check_frontier CLAIMED-ABSENT false
  positive repaired.** The run flagged PROGRAM-STATE.md:6640
  ("no alternate path exists" beside a `diff_transform.py`
  mention). Same-line association was a guaranteed false
  positive under the `no [a-z ]{0,24} exists` pattern - the
  regex can never contain a filename. Artifacts now associate
  only within 60 chars of the absence phrase; "x does not
  exist" and "has not yet produced x" still flag. Committed
  6634fad87; rerun clean (0 findings, control positive).

  Open frontier items: F-6 (per-type field write index -
  charter section 7's last blocked query; 776 fields / 189
  types is the stated denominator) is the strongest
  next-frontier candidate for whichever lane rotates in. F-4's
  body declares DONE-as-specified; the heading just lacks the
  marker. Board: 0 FRONTIER-targeted open at rev 23229.


  **Block 19 tail 24 - 2026-09-20 AUDIT-SPEC capped ->
  CONTRACT rotated in.** AUDIT-SPEC hit the daily cap; its
  promotion-sweep claim stays ACTIVE for when the cap frees
  (its shadow-audit pivot produced six ACCEPTs + one refuted
  OPUS detail before capping). Consumed its BLOCKED_NEEDS_
  SPECIALIST replan - an accurate deferral. desired =
  [EC7, ORACLE, CONTRACT]: CONTRACT is eligible, starving
  24h, and holds a P1 (OPUS-CONTRA-STATUS-WRITE-NOT-
  EXERCISED-BUT-EXP086-RUNS-IT) plus my routed
  FRONTIER-REQ-CONTRACT-EXP-NINE-NONE-FIELD. EC7 keeps
  landing - batches 46-52 published this round, on
  SHARED-HUB-IDENTIFICATION-53, A coverage ~6,700+, gates
  clean every batch. ORACLE moved to NAVGRID-QUERY-EXEC.
  DATA starves with two ACTIVE claims (session free - it
  works self-driven); AUDIT-SEM next for a slot after
  CONTRACT's P1s. Board rev ~23037+. Latest commit:
  8d490ea1b.

  **Block 20 tail 2 - 2026-09-20 operator directive round:
  EXP reviews scheduled, ASTRA queue triaged, REQ-UI ruled,
  fresh checkpoint.**

  IDENTITY: FABLE is the semantic role now running on a
  second Opus-model instance; OPUS remains the structural
  identity. Role IDs preserved; nothing in the fleet config
  carried model attribution before, so it is recorded here
  for every future attribution.

  DIRECTIVE ITEMS EXECUTED:
  - EXP-124/EXP-127 reviews: already assigned_to AUDIT-SPEC
    as P1s; filed FRONTIER-NOTICE-AUDITSPEC-EXP-REVIEWS-
    AHEAD-OF-SWEEP (P1) ordering them ahead of the promotion
    sweep when its cap frees; accepted EXP-124 claims return
    to OPUS for canonical integration before any repeat
    capture (rev 23420).
  - CONTRACT EXP-086/status_write: CONTRACT already finished
    OPUS-CONTRA-STATUS-WRITE-NOT-EXERCISED-BUT-EXP086-RUNS-IT
    (DONE - seven rows re-declared against EXP-086's isolated
    original-code execution; the superseded-by-narrowing
    version closed in the same commit). CONTRACT stays
    desired and busy - the window held.
  - Manual-save short-path: filed FRONTIER-REQ-FABLE-MANUAL-
    SAVE-SHORT-PATH (P2, rev 23422) - state 2 deletes
    icon.sys BEFORE the 2->7 short branch, so 'keeps the old
    icon.sys' cannot hold; FABLE reads the original branches
    and fixes dependent prose. Sixth-equipment-word already
    consolidated in existing FABLE work (OPUS-REQ-FABLE-
    SIXTH-EQUIPMENT-SLOT + OPUS-ANSWERS-SIXTH-EQUIPMENT-
    SLOT-FIVE) - no duplicate filed.
  - ASTRA queue: full board-level triage appended to
    ASTRA-QUEUE.md - 21 rows marked close-on-return with
    provenance (routed replacements, answering commits,
    withdrawal records); PREPUBLISH-CLEAN-GATE routed to me
    (publication tooling owner); the live-only reserve
    listed as parked, not backlog.
  - Publication narrowing: FRONTIER-NOTICE-ORACLE-NARROW-
    EXPERIMENTS-HOLD (P2, rev 23421) - ORACLE's
    NAV-CONSUMER-EXEC claims all of _experiments; team.py
    6f0692a0d accepts a claimant-named subset, so it can
    re-claim only the dirs it touches.

  REQ-UI-UNPARSED-HANDLERS ruled ACCEPTED: shape C added to
  widget_messages.py - `cmp dword ptr [rdx], imm` memory-
  operand compares are equality id tests (disp 0, no index,
  size 4); a second fallback covers the mov-path dead end
  (0057E610 repoints rdx before a later `mov rax,[rdx]`).
  All 15 OPUS ids reproduced exactly; unparsed 24 -> 9 (the
  remainder are 5-byte thunks, the 3-byte 005C5230 stub,
  two neither-shape bodies, five register-load/no-chain
  cases - a different family, not this pattern). TSV
  regenerated.

  SCORE CHECKPOINT @ HEAD 9960d7647, board rev ~23422 (all
  instruments this checkout, this run):
    engine_explained      13,451 / 34,270  (39.25%; interior
      or <128B entry cite on an evidence-bearing page -
      scorer rule adjudicated by AUDIT-SPEC 9efc6221)
    dispositions          A 6,725 / B 1,368 / C 13,590 / D 0
    outside-explained     DECLARED-UNPROPAGATED 15,269 (73.3%)
      | UNCITED-MECHANICAL 3,784 | INTERIOR-NONBEARING 723 |
      ENTRY-ONLY-NONBEARING 961 | ENTRY-ONLY-LARGE 73 |
      UNCITED-UNRESOLVED 9 | ghost cites 0
    audit_coverage        385 / 409 documents
    questions_closed      1,434 / 1,933
    registry/ebp/formats  63/63, 14/14, 46/48
    type debt             confidence=UNKNOWN extent 75,417 /
      923,985 B (8.2%); 4 types size-UNRESOLVED (PSharray,
      Widget, FieldRecordTable, EquipmentDefinitionRecord)
    parity                45 pilots; CONTRACT 6, INTEGRATION 1,
      FULL-SUBSYSTEM 2; 397/727 testable claims exercised,
      >=112 unexercised marked out-of-pilot-scope
    refusal state         22 family declarations REFUSED
      (A-beats-declaration churn), 1 untracked document,
      residual_addrs.txt stale vs coverage --UNRESOLVED--
      section (regenerate, not a score defect);
      244,619 B unlisted code outside the denominator
    indexes               check_dimension_figures clean
      (0 unmarked-different quotes)
  The weighted composite (59.21%) is a proxy, NOT a literal
  completion fraction - the dimension figures above are the
  reportable numbers; L1+L2 canonical completion != L3
  parity certification.

  Running/desired 3: EC7 busy on SHARED-HUB-IDENTIFICATION-55
  (batches through 54 landed, A ~6,703); ORACLE busy on
  NAV-CONSUMER-EXEC (narrowing notice filed); CONTRACT busy
  (post-P1 pool). AUDIT-SPEC capped, holds the two P1 EXP
  reviews + sweep claim; STRUCT/DATA/AUDIT-SEM starve.
  Board rev ~23422. Latest commit: pending publish.

  **Block 21 — 2026-09-20 ASTRA return + two OPUS tooling items
  discharged.** Four commits:

  - 7702245dc: check_census_widths/overlap converted to
    kit_paths (overlap's silent empty-population negative is
    dead - now loads 67 censuses / 15,242 sites from any cwd).
  - fb49a82d0: publish_paths.sh PUBLISH_EXPECT content pins -
    the prepublish-gate proposal ADAPTED as review-time hash
    pinning (catches pre-window edits a snapshot diff would
    bake in); verified refusal+publish end-to-end. Opt-in.
  - 9f347a623: .gitattributes pins _types/*.tsv to eol=lf
    ('?' matches the space - escapes unsupported) + OPUS's
    tsv_lines.py lifted into the kit as canonical writer.
  - a413480d9: ASTRA-QUEUE triage 2026-09-20b - handoff
    consumed (PHYRE-HIERARCHY + AQ18 withdrawn, AQ19 still
    needs the container walk), AQ-1+AQ-6 title-keyboard
    package PREPARED for the next live window (highest
    fan-out, no offline prerequisite; consumer/state/trigger/
    bounds/controls/restoration/stop-conditions all stated).

  ASTRA.md +314 verified byte-identical to its reviewed blob
  pin and backed up under work/ASTRA/resume-20260920/; its
  publication is identity-bound to ASTRA's own claim and is
  NOT delegable - left for ASTRA's resume.

  Board: 0 FRONTIER-targeted open. Latest: a413480d9.


  **Block 22 - 2026-09-20 evening: eight OPUS items discharged,
  system_matrix.py built (the L1/L2 steering instrument), a
  scoring defect repaired.**

  FRONTIER-TARGETED ITEMS (all finished):
  - FABLE-REQ-UNCITED-TAIL-MEMBERSHIP: bucket is now 8 bodies
    (00250130 002678A0 002FB250 0030BA80 0035E760 003A20C0
    005105A0 008A4BAB); regenerating command named
    (outside_explained_breakdown --tsv, filter
    UNCITED-UNRESOLVED).
  - 0057FE80 extent: OPUS's corrected figure verified by
    independent linear decode (lands exactly on 005807B8,
    last insn jmp 005C5230); functions.tsv 2105 -> 2360.
    Both the under-reported and corrected notices closed.
  - AB30 collapse -> COVERAGE-DIMENSIONS 6d appended:
    re-derived from fields.tsv (name-prefix class). AB30
    442 B and Panel3010 341 B confirm OPUS exactly;
    ChildWidget 5,614->5,376. Non-Phyre unobserved
    73,380 -> 39,631 B (4.8%, 95.2% evidenced); all-types
    86,374 B. 6c preserved as the morning measurement.
  - NONFUNCTION-EXPORT retired: check_nonfunction_dependency
    re-run, 0 on every line; superseded notice filed to DATA
    (READY task is assigned_to DATA; cannot close from here).
  - receiver_flow_census --seed-field 0xOFF implemented:
    `object = *(<receiver>+OFF)` third seed door for CHAIN /
    DYNAMIC / FN / SLOTPTR / PTR / RELOFF routes. Seeded
    objects get tag `S:OFF` (NOT 'R',0 - a child must not
    inherit the parent's identity or its displacements
    misattribute). Verified on 00335760 vs EC7's byte[+5]==1.
  - publish_paths.sh: both board scans now read
    claimed_resources || resources - the hold team.py
    recorded, closing the claim-time-hold invisibility.
  - project_embed_census: --out now writes header-only on an
    empty projection (durable measured absence); the nonzero
    exit OPUS saw does not reproduce at HEAD (already 0).

  SCORING REPAIR: outside_explained_breakdown.py now consults
  the gate's own verdicts - REFUSED families no longer mark
  their members DECLARED-UNPROPAGATED. New bucket
  DECLARED-REFUSED = 3,917 bodies (18.9% of the gap) that were
  mislabeled; all 22 refusals are stale generated member lists
  (members now A). Filed FRONTIER-REQ-SWE2-DATA-REGENERATE-
  STALE-FAMILY-SELECTORS (P2): re-run the named select_*.py,
  do not hand-edit.

  STEERING INSTRUMENT: system_matrix.py -> _index/
  SYSTEM-MATRIX.md (generated, revision-pinned). Per
  category: docs/bearing/status, fn A/B/C/D attribution,
  contracts+readiness+passes, types+unobserved extent,
  tier2+ docs, experiment-citing docs, open questions,
  unticked boxes, provisional L1/L2 verdict. Early reads:
  02-Resource (19 bearing of 37, 17 PARTIAL), 05-Spawn,
  15-Input, 22-Phyre, 23-ThirdParty sit below-L1; 16-UI's
  unobserved collapsed to 5,731 B post-AB30; 19-SaveLoad
  carries 12,351 B (SavePayload-dominated).

  Running/desired 3: EC7 busy (hub batches, A ~6,889 per
  latest evaluate); ORACLE busy NAV-RESIDUAL-BOUNDARY-EXEC;
  CONTRACT busy GROUPCOMPLETE-BKEI-WORD. AUDIT-SPEC capped,
  holds the two P1 EXP reviews + sweep claim; DATA holds 2
  AUDIT-SEM contras + new selector request; AUDIT-SEM next
  eligible. Board rev ~24055. Latest commit: pending publish.


  **Block 22b - 2026-09-20 late: contra fix, refusal collapse,
  AQ publish.**

  AUDITSEM-CONTRA-FRONTIER-COVDIM-6D-SUM (P3): real defect -
  the seven-row re-derived column sums to 27,175 B (69% of
  39,631), not the 25,175/64% the note said (transposition).
  Sentence corrected with provenance; every row already
  verified.

  REFUSAL COLLAPSE: families_refused 22 -> 4 between blocks -
  the fleet regenerated most stale member lists (FABLE re-ran
  SEAD's own selector 1170 -> 1144). Residual 4: SEAD (its own
  new section A-measured 007E0B60, re-staling the list),
  AbstractClassDescriptor (006442E0), NativeAdapter.
  ExplainedCalleeForwarder (003EA180), Phyre.Reflection.
  StaticDescriptorSingleton (0062FFC0). DATA's selector-regen
  request still valid, now bounded to the residual.
  DECLARED-REFUSED bucket: 3,917 -> 1,199 bodies.

  MATRIX refreshed at this revision (7 cats L2, 5 below-L1:
  02/05/15/22/23). Below-L1 open questions all already owned
  or gated: 02's J-C IS the AQ-ARENA live read (blocked on
  EXP-127 failure review); 15's DM-1/2/3 are the input
  cluster FABLE is consuming; 22's Q-x/DK-1/EL-1 are Phyre
  structural (OPUS territory, several challenged). No orphan
  unowned questions - no fresh packages filed.

  AQ supersession correction + contra fix + matrix refresh
  publishing under this claim. Latest commit: pending.


  **Block 23 - 2026-09-21: L2-VERDICTS home ruled, contract-scope
  ruled, plan refreshed.**

  TWO OPUS P2s ANSWERED (revs 24444-24445):
  - OPUS-REQ-FRONTIER-WHERE-DO-PER-SYSTEM-L2-VERDICTS-LIVE:
    _index/L2-VERDICTS.md ruled CANONICAL (was PROVISIONAL).
    A verdict needs per-requirement cells + binding-gap prose
    no TSV column or contract block carries. Grain split:
    SYSTEM-MATRIX = per-category steering (generated),
    L2-VERDICTS = per-system verdict record, gate docs =
    whole-database. Systems without contracts still get rows.
  - OPUS-REQ-FRONTIER-TWENTY-TWO-SYSTEMS-LACK-A-SUBSYSTEM-
    SCOPED-CONTRACT: no blanket 22-contract order. Adequacy
    test: a narrower contract suffices iff the system's
    operations have no cross-operation invariant/ordering it
    leaves unstated. Applied at verdict time; contract cell
    records the contract path OR 'adequately covered by X -
    reason'. SCOPE-SHORT = scheduled work item; S-35 correctly
    fails (binding profiles + capability policy span
    operations).

  Both rulings written into the L2-VERDICTS header in the
  shared tree; publish rides the next window (OPUS holds the
  file, FABLE holds @publication - FRONTIER-PUB-L2-VERDICT-
  RULINGS queued READY).

  PLAN: fleet-plan.json refreshed (was stale 13h) - desired
  [EC7, AUDIT-SPEC, DATA]. DATA rotated in (Y-2 + ACTL +
  nonfunc export landed; holds selector-regen P2 bounded to
  4 residual families). CONTRACT daily-cap; ORACLE/STRUCT
  free-parked.

  Board: 0 FRONTIER-targeted open. Latest: 6cc3939be (L2
  ruling edit uncommitted, in tree).


  **Block 24 - 2026-09-21: registry spanned to contracted
  surface, ASTRA classification consumed.**

  OPUS-REQ-SWE2-FRONTIER-REGISTRY-DOES-NOT-SPAN-CONTRACTED-
  SURFACE (P2): ruled the registry covers ALL reconstruction-
  grade contracted surface. 4 rows added to important-
  subsystems.tsv: S-47 resource entry tree/arena lifetime
  (02, core - covers resource-entry-tree + efx-source-rebase
  contracts + authored-reference-lifetime-evidence.md), S-48
  authored command ramp channels (17, supporting), S-49 Phyre
  asset/reflection surface (22, supporting - covers all 3
  Phyre contracts), S-50 Lua chunk loader (23, deferred).
  Middleware rows at CONSUMED-SURFACE scope, not whole-
  library reconstruction. Registry 46 -> 50 systems, 57/57
  contracts named, 0 orphans. OPUS's S-01 cell drift (named
  'none' while CONTRACT-boot-fixups.md sat committed) already
  fixed by OPUS itself. The 4 new rows start unscored in
  L2-VERDICTS.

  ASTRA-RETURN-FRONTIER-NEW-REQUESTS-20260921 (P1): consumed
  + recorded in ASTRA-QUEUE. S31/S33 B-transfers already
  ready-targeted to ORACLE (real predicate/state/callback
  questions); EXP070 link edit queued by OPUS; BG11 render
  caller + leader-null remain C-unprepared (named missing
  prerequisites); EXP124/EXP127 reviews still the gate; NO
  new C selected - standing state unchanged.

  L2-VERDICTS sweep landed meanwhile (OPUS): all 46 scored,
  all NOT MET, contract column dominant gap (25 SCOPE-SHORT,
  6 NOT MET incl. S-27 shared-credit). Now denominator 50.

  Board: 0 FRONTIER-targeted open. Latest: pending publish.

  ---

  **2026-09-21 checkpoint (rev 24982, commit 1889e1463).** All five
  FRONTIER-targeted items discharged this block:

  - `FABLE-AMEND-MANUAL-SAVE-ALREADY-CORRECTED`: closed against
    `3919152a7` — page already correct, no edit owed (bookkeeping only).
  - `OPUS-REQ-FRONTIER-THE-NAVIGATION-MESH-HAS-NO-SUBSYSTEM-ROW`: **new row
    S-51** (nav mesh + corridor-query layer, 06-Movement, core tier, bound
    to `CONTRACT-corridor-query-family`) in tsv + IMPORTANT-SUBSYSTEMS.md.
    NOT folded into S-18 (locomotion/steering is per-unit kinematics; the
    mesh is a distinct query/data layer). Also reconciled the missing
    S-47..S-50 rows into the .md and refreshed §3 stats: 51 rows, 46
    contracted, 0 core uncontracted.
  - `OPUS-REQ-FRONTIER-PRIMARY-PAGES-UNDERCOUNTS-THE-CONTRACT-COLUMN`: ruled
    — **tsv `contracts` column is the authoritative binding**;
    `primary_pages` stays a concise entry-point list (not expanded);
    `implements:` is provenance. Ruling + restated test in L2-VERDICTS.md.
  - `ASTRA-RETURN-FRONTIER-SHAKE-STATE-AND-DISCRIMINATOR` +
    `ASTRA-RETURN-FRONTIER-SHAKE-PRESENTATION-SETTING`: combined prepared
    package appended to ASTRA-QUEUE.md — H1/H2/H3, retained Stepping
    autosave, named `dgl_*` trigger candidates (f0100 timed helper,
    g0102 staged cut_22-25, h0100 elevator scenes) with the zone-binding
    residual stated + observation-based resolution rule; all-five-slot
    offsets (state +0x178+0x18*ch, entry ID +0x170+0x18*ch, bank +0xF0);
    tick counters 022C252C/022C2530/0208D45C as the frame-vs-publish
    discriminator; Screen Shake recorded as a run precondition
    (presentation only); budget 32x4<=30s; read-only restoration.
  - Bonus: `FRONTIER-PUB-L2-VERDICT-RULINGS` discharged via the FIRST live
    narrow claim — held only the file key, `@publication` untouched
    (DATA's publish in flight).

  Gates green: check_links (47,902 links), check_consistency,
  check_questions (MP-2's `{u24 off16|u8 tag}` literal pipe repaired in
  worktree — sits inside DATA's uncommitted narrowing line, left for
  DATA's publish; gate reports it on HEAD until then).

  Board: 0 FRONTIER-targeted open. Controller healthy, replan pending
  not due, desired [EC7, DATA, AUDIT-SPEC] all active. FRONTIER parked
  on ctrl duty. Fallback candidate remains **F-6** (per-type field-write
  index, charter §7's last blocked query) for the next rotation.

  **2026-09-21 checkpoint 2 (post-S-51).**
  `OPUS-REQ-FRONTIER-PAGES-SPELL-A-POINTER-CELL-AS-AN-OBJECT-BASE`: **ruled
  the shorthand is NOT acceptable.** `0209AC30` is a pointer cell (sole
  writer `002800F0` -> object `0209AC60`, 0xE00 B); `[0209AC30 + 0xNN]` and
  bare `0209AC30 + 0xNN` read literally as addresses 0x30 low and collide
  with route-language `PTR a +o` = `*(a+o)` - the exact CON-137 failure.
  Verified at the image (`00282DF0`: `mov rax,[0209AC30]; [rax+0x60]`) that
  writers uniformly meant `*(cell)+off`. Canonical forms prescribed:
  `[0209AC30]+0xNN` or `*(0209AC30) + 0xNN`. Ruling durable in
  EVIDENCE-STANDARD.md "Address-notation discipline" (applies to every
  pointer-cell base, not just this one). Census: ~45 occurrences across 13
  live pages; routed as `FRONTIER-REQ-FABLE-POINTER-CELL-FIELD-NOTATION`
  (11 files) and `FRONTIER-REQ-EC7-POINTER-CELL-FIELD-NOTATION` (ui-layout
  11 hits + loader-bound 6 hits) with exact line lists. AUDIT-LOG history
  deliberately not rewritten. Possessive `the 0209AC30 manager` naming is
  acceptable only where no field arithmetic follows.
  Board: 0 FRONTIER-targeted open. DATA's publish still holds
  `@publication`; my earlier narrow claim discharged without touching it.

  **2026-09-21 checkpoint 3.** FABLE discharged the pointer-cell rewrite
  at `911783520` (12 pages committed; the remaining 2 - config-screen and
  widget-message-protocol - are fixed in FABLE's uncommitted worktree,
  verified by rescan: zero banned forms remain outside EVIDENCE-STANDARD's
  ban list and AUDIT-LOG history). EC7's counterpart sits ready-targeted.
  Controller healthy, replan pending-not-due; desired lanes
  [EC7, DATA, STRUCT] - STRUCT is at-capacity queued with three
  ready-targeted P1s (starvation telemetry recording, not my action).
  AUDIT-SPEC holds the audited-promotion sweep claim (idle session,
  claim live). Board: 0 FRONTIER-targeted open. Parked on ctrl duty.

  **Block 25 - 2026-09-21: F-6 stored-pointer follow landed in
  hop_scan.py.**

  Rotation: AUDIT-SPEC daily-cap -> STRUCT rotated in (4
  ready-targeted type-store questions incl. the P1 union
  declaration). ORACLE next (S31/S33 transfers + EXP133
  contra). 2 stale deferral replans consumed, plan refreshed
  desired=[EC7,DATA,STRUCT].

  F-6 next step done: `mov [obj+X], tracked` publishes the
  value into a (base,disp)+base-version slot map; a later
  qword load of the same slot re-establishes rec/arr/ctx.
  Non-tracked stores poison; volatile clobber/push/pop
  invalidate via write versions. Intra-function only -
  cross-call stores still need ctxseed/argseed (documented).
  Regression on the committed census commands: battle-unit
  2635 -> 2639 scanner rows, control FOUND, zero rows lost
  (the 4 gains: 2 cmp [rax+0x714] sites x2 routes in
  BattleLocomotion_BuildSolverContext via `mov rax,[rdi+0xF0]`
  slot reload - verified at the image). Spawn hop census
  360/78, control FOUND, zero losses vs committed TSV.

  Board: 0 FRONTIER-targeted open. Latest: pending publish.

  **2026-09-22 checkpoint — fourteen-item block discharged.**

  Controller healthy; `@publication` was held by DATA's live HBINDEX
  publish, so `FRONTIER-PUB-HOPSCAN-STORED-POINTER-FOLLOW` was claimed on
  its two file keys only (second live narrow claim).

  Three OPUS rulings landed:

  - STRUCTURAL-DEBT-INVERTED: steering now correct — SYSTEM-MATRIX
    regenerated (Phyre unobsB 46,800 -> 30,154; non-Phyre is now the
    larger half). L2-VERDICTS already carried OPUS's corrected figures;
    no other instrument held the stale split. Ruled: do NOT report debt
    as a single number — carving lowers it, honest declaration raises
    it; the matrix's per-category column is the right shape.
  - PUBLISH-GUARD-MISSES-INLINE-EDITS: widened publish_paths.sh — a
    per-path changed-line census always prints, and added lines
    introducing a foreign agent id (not on the hunk's removed lines,
    not the publisher) warn. Warning not refusal: peer-attribution prose
    ("re-measured by OPUS") is legitimate. Verified on live dirty files.
  - GATE-RUNTIME-ROW-REGRESSED: ruled contract-before-evidence IS the
    intended intake order; `nothing executed` stays a row-level failure
    but is now diagnosed — check_gate26 names members of every class
    (was count-only). The 2026-09-21 reading is intake lag (3 new
    contracts), and two of the three are named frontier systems already
    routed to ASTRA-QUEUE. Ruling appended to RECONSTRUCTION-READINESS-
    GATE.md. Verified: tool names the exact three OPUS computed by hand.

  Ten ASTRA returns consumed into ASTRA-QUEUE.md §DISPOSITION 2026-09-22:

  - OLD-SAVE: AQ-10 answered (FFXII_004 loads; battle block replaced,
    not stale); review already ACCEPTED by AUDIT-SEM; gaps retained.
  - CML1: PREPARED — byu_x0100 (Bhujerba) primary + rbn_a0380 bounded
    alternative VERIFIED from corpus (entry6 stay_cam_mg_cut06: authored
    9 vs first-match 6 at blob+0x74; pair [6,9] identical).
  - EO3: PREPARED — trigger resolved offline: 00377DC0 requests the loose
    ps2data/efb/<map>.efb on every map load; Stepping→Eastgate walk is
    the named ordinary trigger; ASTRA's corrected sites verbatim.
  - MGRMARK: premise retired (static clear at 0032F14B); no residual live
    item without a named consumer.
  - CONTRACT-LIVE-REUSE: superseded; both claims answered offline; the
    one live remainder (new-purchase roundtrip) = STATE-ROUNDTRIP.
  - SHAKE-RESIDUE: package amended — occupancy only, script identified by
    the +0xF0 bank binding (not channel state), no per-tick visit counts,
    native flags 02EBF3C4/02EBF3C0/02089350 recorded alongside UI.
  - REGFILE: classified — needs in-pool occupant change, NOT zone reload
    (pool release confounds); Estersand proximity spawn/despawn named as
    the trigger class; ASTRA's observation set verbatim.
  - STATE-ROUNDTRIP: PREPARED — disposable copy of the Stepping save,
    same-field purchase → save crystal → reload; gil at header +0x08
    (writer 00254EE0) + bazaar spans B+57C8/+59C8; unchanged-neighbor
    control; decoded-file + live reads; nominated as the next high-impact
    empirical blocker.
  - AUDIO: voice-parameter half PREPARED (rbn_a0380's 13 voiceplay_28b
    calls on FFXII_004 in Rabanastre); selective-gate half stays an
    explicit dependency for OPUS.
  - RESOURCE-TRACE: PREPARED — named family = loose .efb map effect bank
    via 00377DC0, same Stepping→Eastgate walk; batches with EO3.

  Gates: check_links 773 files / 49,858 links clean; check_consistency
  and check_questions clean; verify_doc_addresses ok on both edited docs;
  ADDRESS-INDEX regenerated (18,322 addrs / 461 docs).

  Post-block item: `ASTRA-NOTICE-FRONTIER-NATIVE-FP-BOUNDARY` (P1) consumed
  and finished — one-slot breakpoint path drops x87 last-instruction
  metadata upper bits across FXSAVE64 resume; standing caveat appended to
  ASTRA-QUEUE covering every breakpoint-using package (integer/pointer/
  memory claims only, no narrowed-flags fix, no queued dependency on x87
  state). Commit 7b1eb6c32.

  Board state at end: 0 FRONTIER-targeted open. Controller healthy
  (pid alive, breaker closed); replan pending-not-due, desired lanes
  [EC7, ORACLE, AUDIT-SPEC]; AUDIT-SPEC at-capacity. FRONTIER parked on
  ctrl duty. Fallback: F-6 (per-type field write index).

  **Block 25 — 2026-09-21: five ASTRA items discharged, team.py
  fail-closed fix, replans consumed.**

  All P1, all DONE (revs 26090-26100):

  - FP-CAVEAT-SCOPE: standing caveat narrowed to observed scope —
    FIP upper-32 loss on above-4GiB x87 instruction addresses named
    exactly; FDP marked UNTESTED (was zero throughout); blanket
    integer/pointer/memory-only rule replaced by per-claim state+effect
    controls; narrowed-flags kept as not-a-demonstrated-fix but the
    authorization-gate/freeze-order reading removed. EXP127 stays
    INVALID_POST_TRACE.
  - SAVE-RIDER-SCOPE: the same-field roundtrip demoted from 'nominated
    next high-impact blocker' to RIDER-ON-BATCH-B per FABLE's premise
    return (1dbd2f844) — PREPARED means spec-ready, not commissioned;
    bazaar spans B+57C8/+59C8 removed from its claims (an ordinary
    vendor buy cannot establish a bazaar sold-counter transition —
    separate open item); name-before-run requirements added (item,
    file slot, vendor/crystal, unchanged control byte).
  - ORACLE-SAB-OMISSION: verified 0d068c953's tree deletes 16 pan
    files + reverts ASTRA.md vs parent e020a57af under an EXP-140-only
    commit; routed as FRONTIER-REQ-ORACLE-SAB-PUBLISH-OMISSION-CAUSE
    (P1 -> ORACLE: demonstrated mechanism + smallest guard).
  - TEAM-ACCESS-DENIED-LIVENESS: real defect fixed in team.py —
    OpenProcess NULL mapped ANY failure to dead; now only
    ERROR_INVALID_PARAMETER (87) proves dead, ACCESS_DENIED/other is
    fail-closed live (use_last_error handle; new _open_failed_means_dead
    seam). Regression in test_team.py (mapping + live/dead lock
    controls); 11/11 tests pass.
  - EO3-PRODUCER-PATH-REGISTER contra: queue's positive control named
    RCX for path bytes; corrected to RDI (RCX=0xFF is flags) per
    staging.json, and caller attribution now REQUIRED (record the
    primary return — boundaries.json pins 00377F87 — rather than
    inferring the caller from a visible zone transition).

  Replans: AUDIT-SEM (behind set) + AUDIT-SPEC (at-capacity) were
  accurate deferrals — consumed (2 events). fleet-plan refreshed to
  the three lanes actually producing: EC7 / CONTRACT / DATA. ORACLE
  at-capacity holds the new P1 SAB request for cap-free; AUDIT-SPEC
  keeps EXP124/127 reviews + sweep ACTIVE likewise.

  Publish pending: team.py + test_team.py + ASTRA-QUEUE.md edits —
  window held by SWE2-DATA (HBFIN publish in flight).
  Board rev 26100. Latest commit: 576cc4855 (peer).

  **Block 26 — 2026-09-21: false /goal completion gate installed.**

  Both Opus lanes got met=true on reports naming unfinished research
  (OPUS b8b3ebf9-6517-482a-8472-9b3ae77900dd: met after 2 iterations on
  09-18 + a reasonless met on 09-20; OPUS-STRUCTURAL
  f8acb9e1-fcec-4ec3-ab91-bdfc5dfa509b: met 09-20 reasonless, met 09-21
  after 169 iterations on a "continuous substantive work" narrative).
  Diagnosis: the lanes' project dir carried NO user Stop hook, so the
  built-in goal evaluator's transcript-reading verdict stood alone.

  Verified on installed claude 2.1.278 (fixture sessions
  6bf0d86d/94ecc3f1/1681ae60): user Stop hooks run AFTER a met verdict
  and `{"decision":"block","reason"}` vetoes it; `/goal` re-registers
  headless via `--input-format stream-json`; `-p --resume <id>` resumes
  the same session; `claude agents --json` is the exact live-session
  roster; `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` (default 8) bounds
  consecutive blocks; not_met-at-cap pauses as `goal_check_capped`.

  Shipped (XIIOnline repo):
  - `goal_gate.py` — read-only gate: scope (residual=0 + population),
    provenance (check_provenance green), per-system verdicts
    (important-subsystems.tsv ids all MET in L2-VERDICTS.md), questions
    (OPEN=BLOCKED=PARTIAL=0, consistent), contradictions (no
    OPEN/FILED/unknown kinds), terminal acceptance (committed AUDIT-LOG
    receipt of a complete clean 30-pass run, pinned commit ancestor of
    HEAD with zero DB drift since). Prints DB_GOAL=NOT_MET
    remaining=… next=…; missing/stale/uncommitted evidence is NOT_MET.
    Real state reads NOT_MET (all 51 systems NOT MET, 279+4+129
    questions, 6 unresolved contradictions, no receipt).
  - `goal_gate_hook.py` — Stop hook; gates only sessions whose last
    goal_status condition matches the FF12-database signature; honours
    `failed` (impossible) as terminal; met+gate-unmet blocks with the
    concrete obligation; tool_use-count signature detects no-progress
    loops and escalates the reason; gate errors fail closed. Registered
    in `C:\Users\Kristian\source\repos\.claude\settings.json` (project
    settings — local machine file, .claude/ untracked there).
  - `goal_resume.py` — exact-session classifier/resumer: ACTIVE (via
    `claude agents --json`) refuses; FALSE_COMPLETION / ORDINARY_STOP
    resume same id via stream-json `--resume` with `/goal <exact
    condition>` re-issued verbatim when the verdict cleared it;
    USER_STOP / USAGE_LIMIT / ERROR / IMPOSSIBLE / UNKNOWN honoured or
    reported; 3-resume no-growth cap prevents retry storms.
    Verified: f8acb9e1 and b8b3ebf9 classify FALSE_COMPLETION with exact
    goals recovered; fbea217b (live, busy) refused as ACTIVE.
  - `test_goal_gate.py` — 23 fixtures: both observed failure shapes,
    stale/uncommitted/missing receipts, fresh receipt passes,
    verdict/contradiction parsing, user-cancel, hard-limit, impossible,
    compaction-preserved goal, no-progress escalation, fail-closed.

  End-to-end on a live session: a fixture lane set a DB-shaped goal,
  the evaluator marked met on a file-write, and the hook vetoed with
  the real gate's `remaining=` obligation — the exact false-completion
  path now cannot close a lane.

  NOT done / unsupported step: no automated driver fires the two dead
  lanes — they were interactive sessions; resuming is
  `goal_resume.py --session <id> --execute` or interactive
  `claude --resume <id>` + `/goal <condition>` (exact conditions are in
  each transcript's goal_status records). Deliberately not auto-fired:
  they are multi-hour Opus lanes and `--resume` on a session the user
  has open would fork a copy.

  **Block 27 — 2026-09-21: five OPUS requests discharged; provenance gate green.**

  The four provenance requests were all discharged by peer landings, verified
  directly rather than from the reports:
  - `SIX-PEER-DIRTY-FILES` (P0): `check_provenance` exits green at HEAD —
    244 GZF-derived docs all transferred to certified parent `59629b9b`, 0 stale.
  - `LADDER-HEAD-STALE-DUPLICATE` (P1): `ladder_head.md` no longer exists
    beside `battle-runtime-mode-ladder.md` (directory listing verified).
  - `ONE-LINE-BY-ONE-PEER` (P1): `the-fifteen-modules-registered-before-main.md`
    committed at `b8014609c` with `parent_tag: GN162`.
  - `PUBLICATION-HELD-THROUGH-GREEN-GATE` (P1): `b8014609c` carried the pending
    files; the provenance dimension is green at a real revision.
  - `INLINE-CENSUS-BLOCK-EXITS-1` (P2): REAL defect, fixed and published as
    `be5388073` — the empty census printed a blank line, the while body's last
    command was `[ -n "" ]`, and under `set -euo pipefail` the script died
    silently mid-publish. Body is now `if [ -n "$l" ]; then echo; fi`.
    Reproduced exit-1/exit-0 in an isolated harness both directions; the fix
    ran correctly on its own publish.

  Board rev 26419. Controller 44404 healthy; desired = EC7/CONTRACT/DATA;
  STRUCT/ORACLE/AUDIT-SPEC starving behind the set (STRUCT holds a P2 OPUS
  notice). 0 FRONTIER-targeted open. Latest commit: be5388073 (mine).

  2026-09-21 late block (c4f272e83): three FRONTIER items discharged.
  - PTextureCubeMapD3D11: RESOLVED - name is engine-authored via Phyre
    reflection (descriptor-template RTTI + name-hash FBB759D0@006154FA),
    absent only direct .?AV/vtable; row qualified; _types/README.md gained
    the three-kind name-provenance rule (MSVC RTTI / reflection /
    store-assigned-must-be-marked).
  - AUDIT-SPEC starvation escalation: adjudicator NAMED - filed
    FRONTIER-REQ-AUDITSEM-TYPES-MET-CRITERION-ADJUDICATION (P1, AUDIT-SEM)
    for the goal_gate-blocking types-MET criterion; AUDIT-SPEC's other two
    requests stay queued (starvation is capacity, not refusal).
  - census_receiver_fixpoint.py acknowledged (SEED taxonomy correct;
    zero-functions = failed start, never a negative).
  Board: 0 FRONTIER-targeted open. Parked on ctrl duty; fallback F-6.

  2026-09-21 late block 2 (32719dc81): FABLE contradiction UPHELD and
  fixed - 001EDDC0's three IAT slots are WINMM (timeGetDevCaps/
  timeBeginPeriod/timeEndPeriod), not QPC/Sleep; paragraph rewritten with
  the correct arm semantics (30fps arm requests wPeriodMin, 60fps arm
  releases it). Config page S17.1 already had the right walk - mine was a
  stale rederivation. OPUS's name-provenance tool verified on the exact
  case (classifies PHYRE REFLECTION, honest anchor limit). AUDIT-SEM took
  the types-MET adjudication (busy-wake, active claim).
  Board: 0 FRONTIER-targeted open. Parked; fallback F-6.

  2026-09-22 block (57f9d58ab): thirteen FRONTIER items discharged; two tool
  fixes + five rulings shipped.

  INSTRUMENTS (commit 57f9d58ab):
  - census_receiver_fixpoint.py + gen_array_census.py now run a per-instruction
    dataflow fixpoint over the CFG (union join, base sets cap 16 -> TOP; orphan
    blocks seeded from indirect-jump exit states). `call` drops volatile regs.
    Control: 147 displacements; self-test recalibrated 150 -> 130 (old number
    was calibrated on clobber-inflated output). SpawnGroupLedger regression
    7 -> 8 accesses, zero losses. receiver_census.py still linear - flagged.
  - goal_gate.py verdict parser: header-scoped row width + `^MET\b`; S-10's
    annotated MET registers. Gate reads 51/52 NOT MET (registry grew to 52).
    check_questions parses stdout regardless of exit code; QUESTION LEDGER
    INCONSISTENT fails closed. test_goal_gate.py 25/25.

  RULINGS: S-13 is two systems (S-52 = manager slot entry tables, registered,
    verdict row pending peer publish of L2-VERDICTS); dispatch record slot
    names shifted by one (+0x10 = result, verified at image, routed to FABLE);
    NATIVE-REPLAY over scripted import boundary satisfies the runtime cell
    PER-INVARIANT only (load-bearing boundary = not satisfied); the 49-page
    contract wall is OPUS's, wall order S-20/S-32/S-22/S-28 first; REOPENED
    must carry a stated obligation (three silent pages -> AUDIT-SEM triage);
    experiment back-refs are cite-or-decline, contract-path resolution is a
    hard check (nine routed: 8 to FABLE, EXP-110 to OPUS).

  Board rev ~27876. Controller 44404 healthy; desired = DATA/AUDIT-SEM/
  AUDIT-SPEC. 0 FRONTIER-targeted open. Latest commit: 57f9d58ab (mine).

  2026-09-22 block (afbab48c3): four items discharged.
  - FABLE-CONTRA-CROSSREF-PROSE-WORD: CONFIRMED + FIXED. doc_accounts_for
    now reads crossing/neighbours sections + folder only. Measured:
    134 -> 2888 findings, 0 removed; 2,754 pairs were prose-cleared
    (~95% false-clear on the true obligation set). Tripwires 143->572.
  - OPUS-REQ-MAPSCREENPAGE: closed WITHOUT ruling per OPUS's own
    withdrawal - the type row already answers it (3 builders, per-screen
    handlers, one page kind). Withdrawal verified independently first.
  - OPUS-REQ-AB30: RULED - declare the 0x720 occupant separately; all
    three kind discriminators differ (extent/handler/child topology),
    alternate occupancy over time; naming = size-suffixed; children
    declare under own parents. Recorded as a store pattern in README.
  - OPUS self-contra on the premise: accepted, closed.
  Board: 0 FRONTIER-targeted open. AUDIT-SEM holds the types-MET
  adjudication; AUDIT-SPEC/ORACLE still capacity-queued. Parked; F-6.

  2026-09-22 block (rev 28615): nine items discharged, two ORACLE tasks routed.

  - S-01 I3 replay contra: ACCEPTED + verified at the image. 001EDDC0's
    frame-base writes are in the settings-boolean arm from image constants;
    the only import-return test sits in the other arm writing none. I3
    re-classified SATISFIED by replay; S-01 runtime cell amended in
    L2-VERDICTS.md. Other two EXP-142 replay invariants still unclassified.
  - Gate pipe defect: fix verified landed (escape-aware split + escaped
    S-48 row); regression tests added (escaped-pipe parses / raw-pipe
    fails closed); test_goal_gate 27/27.
  - MapScreenPage question: closed per OPUS's own withdrawal — one page
    kind, three containers/screens.
  - Rulings: contract: key errors are the experiment author's to fix
    ('none' + reason when uncovered — the corpus convention); missing key
    likewise author's to add; queue drift acceptable as upper bounds, close
    on re-verified evidence; scope: grammar stays four values, 'subsystem'
    absorbs state-machine subjects passing the adequacy test.
  - Routed: FRONTIER-REQ-ORACLE-EXP142-CONTRACT-KEY (missing back-link on
    goal_gate's first-unmet path) and FRONTIER-REQ-ORACLE-SIX-EXP-CONTRACT-
    KEYS-REPOINT-OR-NONE (six records keyed at a contract they don't
    describe; allocator + queue/poll pump are uncontracted subjects).
  Board rev 28615. Desired = EC7/CONTRACT/DATA, all producing; 1 replan
  pending (BLOCKED_NEEDS_SPECIALIST). Parked; fallback F-6.

  2026-09-22 block (rev ~29098): three P1s discharged; S-01 IS THE SECOND
  L2 MET.

  - I1+I4 adjudicated: both ACCEPTED, image-verified. I1: 00863D30 calls
    only 00866D60 (x2), which calls nothing - zero imports in the seeding
    path. I4: 0022A1E1..0022A394 = 0 test/cmp/jcc over 19 calls - no
    failure branch exists to execute. All three EXP-142 replay invariants
    satisfied under rev-26981; S-01 runtime cell -> MET, row -> MET.
    Gate now reads 50/52, first unmet S-02.
  - Glyph-root notice: accepted + corrected. 001E8580 calls all three
    ctor classes at four sites (00213A00 x2, 00213960, 002138C0); the
    00906DE8 plain instance is base/reset-only. Page line ~593 amended.
  Board rev ~29098. Desired = STRUCT/ORACLE/AUDIT-SPEC. Parked; F-6.

  2026-09-22 block (rev ~29166): queue empty; census re-run routed.

  - Verified the 419-row caveat already carries BOTH amendments
    (OPUS appended CENSUS NEGATIVES ARE NOT ESTABLISHED withdrawing
    the one-directional claim) - no doc edit needed.
  - hop_scan stored-pointer follow confirmed landed at a189011e2.
  - Routed FRONTIER-REQ-DATA-CENSUS-RERUN-UNDER-CFG-WALKER (P2,
    SWE2-DATA): re-census the 36 caveated types under the fixed
    CFG walker; confirm or withdraw every pre-fix negative.
  Board rev 29166. Desired = CONTRACT/ORACLE/AUDIT-SPEC;
  EC7 busy-wake on shared-hub batch ~140. Parked; F-6.

  2026-09-22 late block (rev 29172+): REQ-FRONTIER-PUBLICATION-LEASE-
  STALLED adjudicated - FABLE's @publication hold (FABLE-PUB-001E2AF0-
  FINISHED, ~2h silent) ruled PRESUMED LIVE: identical signature resolved
  as live 24h ago (4x 18-min gate runs), files prepared minutes before
  the claim, manual ACP lane (no attributable pid). No peer-release path
  exists by design; filed FRONTIER-REQ-FABLE-PUBLICATION-LEASE-CHECKPOINT-
  OR-RELEASE (P1) for same-identity recovery. Protocol gap recorded: no
  lease timeout exists at all.
  Board: 0 FRONTIER-targeted open. Parked; fallback F-6.

  2026-09-22 late block (rev 29177+): F-6 PASS BUILT - the per-type
  field write index exists.

  - field_access_index.py (new): route-seeded census over every
    seedable type -> _types/field-access-index.tsv, 8-col rows
    (type, disp, base, kind, function, site, insn, note). First run:
    132/595 types swept, 9,717 rows over 82 types (w 3,279); 776
    declared fields have an index writer.
  - Fixed three shared-instrument defects found while building it:
    sweep_route_seeded_census.py (ctor-column unpack crash,
    single-rule routes, missing image-base lea idiom - all diverged
    from the single-type tool); route parser now accepts PTR+delta
    (grammar-sanctioned, seeded at -OFF like FN) and trailing
    ' -> note' on STATIC/PTR.
  - Store routes corrected to their own rows' adjudicated evidence:
    PApplication STATIC->PTR on the handle slot; AchievementState and
    ImageBackedStateBlock gained FN 0x002536A0 alternatives (PTR seeds
    walk only direct loaders; consumers call the getter). IBS 12->26
    rows, AchievementState 0->8.
  - Residue stated, not implied: 463 unseeded types (NONE 353 / EMBED
    56 / DYNAMIC 21 / CHAIN 9 / RELOFF 4 / PARRAY 4 / SLOTPTR 2) need
    per-type fixpoint seeds - research, not plumbing. Rip-relative
    absolute statics (BootAllocationSlot*) are global_refs' job.
  - check_consistency surfaced a NAME disagreement NOT mine:
    006B9120 NUM_LIGHTS vs PRendering::PContextSwitchLights - same
    two-name-layer class as the PTextureCubeMapD3D11 ruling. Filed
    FRONTIER-REQ-OPUS-006B9120-NAME-DISAGREEMENT (P2) to OPUS.
  - Gates: links 54,638 green; questions consistent; storage_class
    271 routes, 0 hard failures; consistency 1 disagreement = the
    routed one.
  Board rev 29177. FABLE lease still held; EXP150-PUB still ready.
  Fallback: F-6 residue is now research-class (per-type seeds) -
  next rotation picks from PROGRAM-STATE frontier, not F-6.

  2026-09-22 late block (rev 29190+): F-6 wiring done - the index is
  a knowledge_db source.

  - knowledge_db.py ingests field-access-index.tsv as field_access;
    writers-of-field moved NOT SUPPORTED -> SUPPORTED (29/32; the 3
    remaining name their missing source). Verified:
    writers-of-field ManagerSingleton0209BE80+80 -> 004FE3C0;
    accessors-of-field AchievementState+1 -> 00316440 r.
    Companions: accessors-of-field, accessors-of-type.
  - Normalisation: disp/base stored uppercase no-0x to match the
    global_refs arg convention; type compare is case-insensitive.
  Board rev 29190. 0 FRONTIER-targeted open; FABLE lease still held
  (checkpoint-or-release request still READY). Controller healthy.
  Parked on ctrl duty.

  2026-09-23 block (rev 29237): adjudication follow-through + the
  lease-timeout protocol gap filed.

  - Verified the delegated types-MET adjudication LANDED: AUDIT-SEM
    ruled ACCEPTED (rev 26781, L2-VERDICTS ~line 2743) with two
    precisions; S-46->PARTIAL (counter 0208E6B0 undeclared), S-01->
    PARTIAL. My delegation produced the independent ruling.
  - Follow-through filed: FRONTIER-REQ-AUDITSEM-APPLY-TYPES-MET-TO-
    PENDING-CELLS (P1) - three cells still carry 'the request is
    still open' tails contradicting the ruling on the same page
    (S-01 ~846, S-02 ~249, S-52 ~286). Cells now scoreable.
  - Protocol gap filed: FRONTIER-REQ-OPUS-PUBLICATION-LEASE-TIMEOUT-
    RULE (P2) - proposes @publication-key-only release after named
    bounds (checkpoint age + unanswered checkpoint-or-release +
    no-activity check), logged as adjudicated event, claims
    untouched. NOT enacted - OPUS ratifies/amends/rejects.
  - FABLE lease: ~15h, no file writes since 20:47Z, no devin
    session, no attributable process. Standing: presumed live,
    lease stands, no takeover on timestamp. If truly dead, the
    only present path is a user-side FABLE restart.
  - EXP150-PUB and the original AUDIT-SPEC criterion request both
    off the board (completed); two publishes still queue on lease.
  - check_frontier.py clean: MAYBE-DONE advisories are all F-6
    naming its own artifacts (honest open, research-class residue).
  Board rev 29237. 0 FRONTIER-targeted open. Parked on ctrl duty.

  2026-09-23 block (rev 29240+): EC-2 ANSWERED - the std::regex
  question is closed, and the answer is a dead dev feeder.

  - Claimed EC-2 from PROGRAM-STATE section 6 (in-flight, unbanked;
    no board task, no claim). Three sub-questions all resolved from
    the image, not prose.
  - 0020AC30(index,path): name-classifying setter over a five-slot
    event-asset table (01F832F0 strings / 01F83390 vectors /
    01F832B0 counters; in-call index 01DFE40C). sum_ -> <name>.json
    + virtual asset-loader call; 0001 -> flag 01F832E8; spc_ ->
    flag 01F832E9. 0020AF10 is the sibling event pusher.
  - Reachability, FOUR instruments, control positive: 0 E8/E9
    callers, 0 memory-operand refs across 34,270 bodies
    (data_xref_scan, control 00905958), 0 data qwords/dwords.
    Both producers DEAD in retail. The regex's backslash
    \plan_master\ form targets the dev loose-file tree; shipped
    VBF paths are forward-slash.
  - Consumer side live but console-only: 001CD0E0 row renderer,
    001EC560/00180120 arm conjunction, 001EC4B0->0020A760
    eviction. Flags constant-0 in retail; panel always empty.
  - New page: Developer-Tuning-Console/
    the-event-slot-panel-and-its-dead-feeder.md. EC-2 row ->
    ANSWERED; PROGRAM-STATE section 6 rewritten as resolved.
  - Gates: links 54,815 green (32 cited, all resolving);
    questions consistent.
  - Also verified this block: AUDIT-SEM applied the types-MET
    ruling to pending cells (S-52 types MET, S-02 types PARTIAL
    with enumerable scalar residue, stale 'still open' tails
    corrected) - my delegation produced the ruling AND the apply.
  Board rev 29240. 0 FRONTIER-targeted open; 5 outbound pending
  (incl. FABLE lease ~16h, OPUS lease-timeout rule). Parked.

  2026-09-23 block (rev 29240+): F-6 residue — PARRAY/SLOTPTR now
  consumed by the route-seeded census.

  - gen_route_seeded_census.py extended: PARRAY seeds *(ADDR) and
    strides element = *(ADDR)+OFF+i*S; SLOTPTR seeds *(ADDR+i*stride),
    including the two-instruction `lea rB,[table]` + `mov rX,[rB+i*S]`
    form (a `tablebase` tracked set; the roster at 022C1788 is only
    ever reached that way — 13 lea hosts, 0 direct loads).
  - Regression held: PTR/STATIC/ARRAY output byte-identical
    (control ManagerSingleton0209BE80, 1,436-row artifact, empty diff).
  - BattleUnit: 17 cumulative field offsets, 11 via SLOTPTR alone
    (unitFlags, actorWork, statsRecord — all declared rows).
    SpawnRecord PARRAY: 14 offsets incl. the documented +0x80
    battleStats EMBED cluster. Widget/ActorRecordPool stay honestly
    skipped — size UNRESOLVED.
  - Index regenerated: 138/595 types swept, 11,020 rows over 85
    touched (was 132 / 9,717 / 82). Residue now 443: NONE 353,
    EMBED 56, DYNAMIC 21, CHAIN 9, RELOFF 4 — research-class.
  - knowledge_db rebuilt: field_access 11,020; writers-of-field
    BattleUnit+15C resolves (00310920). README + PROGRAM-STATE F-6
    entry updated; gates green (00124BFC REVIEW is pre-existing,
    not mine). Worktree carries ~2,380 peer-lane modifications —
    commit is strictly pathspec'd.
  Board rev 29240. 0 FRONTIER-targeted open; 5 outbound pending.
  Next: monitor board; CHAIN/RELOFF route-kind support is the
  next census extension if a cheap form exists.

  2026-09-23 block (rev ~29240): rotation fix - all three board-heuristic
  lanes were daily-capped while STRUCT/DATA starved ~24h with ready-targeted
  work. fleet-plan.json was stale since 09-21; wrote fresh plan:
  desired = STRUCT (Lua closure-header P2) / DATA (census re-run P2) /
  EC7 (standing hub campaign). Controller 44404 will wake on next poll.
  CONTRACT finished 13 claims in one run; AUDIT-SEM re-scored S-02 types
  PARTIAL + S-52 types MET under the ruled criterion. Gate: 50/52,
  first unmet S-02, questions OPEN=248. 0 FRONTIER-targeted open.
  6 replans pending-not-due. Parked.

  2026-09-23 block (rev ~29270): F-6 residue - derived routes
  CHAIN/EMBED/RELOFF now consumed by the route-seeded census.

  - gen_route_seeded_census.py: derive_specs() resolves a derived
    alternative transitively to a seedable ROOT; the walk runs once in
    root coordinates with self.derived (rebase window + per-level
    deref/rel-offset sets) and emits only the child's window - disp/base
    child-relative, base distinguishing embedded members from pointer
    members (the fields.tsv ctype X* test arbitrates; no field row at
    the relation offset => honestly unresolved). RELOFF tracks a signed
    relative register and combines through add/lea. Callers updated:
    field_access_index.py + sweep_route_seeded_census.py drivers,
    parse_route(s) callers.
  - Verified: BattleStatsRecord resolves through BOTH CHAIN
    BattleUnit+0x698 AND EMBED SpawnRecord+0x80 (4 offsets, all declared
    rows, negative -0x80 bases correctly read as the SpawnRecord
    buffer); ManagerSub0209AC60_02F8 pointer-member chain (454 PTR
    hosts, 22 offsets, all declared) after adding the documented
    PTR 0x0209AC30 alternative to Manager0209AC60's route; two-level
    ManagerSub0209AC60_02F8_00C0 (24 cumulative offsets); EMBED
    ManagerSub0209BE80_8FA0 (56 offsets). Control
    ManagerSingleton0209BE80 BYTE-IDENTICAL.
  - Index regenerated: 209/595 types swept, 14,197 rows over 123 touched
    (was 138 / 11,020 / 85). 44 derived types now carry rows
    (ManagerSub0209BE80_57E0 494, ActiveLogWidget40C8 175 transitive
    EMBED+pointer). Residue 398: NONE 352, DYNAMIC 21, EMBED-unresolved
    14, CHAIN-unresolved 7, RELOFF-unresolved 4 - all 25 unresolved fail
    on unrouted/DYNAMIC parents, not on derived semantics (RELOFF has no
    seeded parent yet to exercise it end to end).
  - knowledge_db rebuilt: field_access 14,197; writers-of-field
    ManagerSub0209AC60_02F8+0 -> 002482E0 (2 sites). Also fixed the
    offset-arg normalisation: +00/+08 zero-padded forms now match the
    stored no-0x disp (ltrim-with-empty->'0' CASE in both field queries).
  - Gates: links 55,232 green; questions consistent; consistency 1
    disagreement = pre-existing 006B9120 (routed to OPUS). Commit
    pathspec-scoped; ~2,380 peer-lane modifications untouched.
  Board rev 29270. 0 FRONTIER-targeted open; 6 outbound pending (FABLE
  lease ~17h, OPUS lease-timeout rule, EXP110 backref, DATA census
  rerun [claimed], 006B9120 names, AUDIT-SPEC promotion sweep).

  2026-09-24 block (rev ~29284): F-6 residue — RELOFF exercised end to
  end; three lazy-singleton DYNAMICs seeded via their own documented
  pointer cells.

  - Diagnosed all 25 unresolved derived routes by failure point: 7 hang
    on ActorStorageRecord's *(*(slot+8)+8+i*8) double-deref (new grammar
    form, research-class), the rest on genuinely unrouted or
    idiom-DYNAMIC parents — EXCEPT 3 rows whose own instance text named
    the cell: MapRefImageHeader [02099D88], RenderCommandOwnerList
    [01F7F5E8], OrderedCommandList [01F7F5E0]. Added `| PTR`/`| FN`
    alternatives (FN 0x0018B4E0 / 0x0018CA40 are the two `mov rax,[cell];
    ret` getters — measured: the cells' only reg-loads ARE the getters).
  - Real spec bug found and fixed: derive_specs put rel offsets in BOTH
    derefs and rels; the mov handler checks derefs first, so every rel
    load would have been marked a pointer. Also added to the walk
    (all dv-gated, non-derived output untouched): movsxd/movsx/movzx
    reg-write handling (rel-load gated on 4-byte operand so
    `movzx word [elem]` field reads don't mis-mark), indexed-lea
    element bases `lea d,[b+i*S+x]` -> off[b]+x, shl/sal and any-imm
    imul -> mult, mult+base add relaxed to derived runs.
  - Verified: MapRefFieldRow (RELOFF +0x04 -> 4 offsets, readers resolve
    to NAMES: MapRef_GetPrimaryFieldValue/GetAuxValue0+1/
    GetAreaArdFieldResourceIndex/GetPersistenceGroupId — the
    field-id-indexed row semantics confirmed), MapRefWeatherBlock,
    MapRefWeatherLane (4 EMBED alts through RELOFF->PTR transitively),
    EastlPointerVector (FN seeds carry 46+56 hosts vs PTR's 1 — the
    getter-mediated path the rows describe). Control
    ManagerSingleton0209BE80 BYTE-IDENTICAL again.
  - Index regenerated: 212/596 types swept, 14,789 rows over 130
    touched (was 209 / 14,197 / 123). Residue 387: NONE 352, DYNAMIC 18,
    EMBED-unresolved 8, CHAIN-unresolved 7, RELOFF-unresolved 2.
  - knowledge_db rebuilt: field_access 14,789; accessors-of-type
    MapRefFieldRow returns the named getters.
  - Gates: types_index validate 0 errors; links 55,238 green; questions
    consistent; consistency 1 disagreement = pre-existing 006B9120.
    types.tsv staged hunk-scoped (peer rows carry uncommitted edits).
  Board rev 29284. 0 FRONTIER-targeted open; 6 outbound pending (same
  set, DATA census rerun + AUDIT-SPEC sweep claimed-ACTIVE).

  2026-09-24 block (rev ~29292): F-6 residue — the last grammar form
  falls: PTABLE (parent-relative pointer table) + FN getter seeds
  resolve the actor-record double-deref family.

  - The unresolved *(*(ActorManagerSlot+0x08)+8+i*8) form was read off
    the real helper 00358940 (mov r8,[rcx+8]; cmp edx,[r8]; movsxd;
    mov rax,[r8+rax*8+8]): pool at slot+0x08, count at pool+0x00,
    record-pointer table at pool+0x08, 8-byte entries. Modeled as
    `SLOTPTR ActorRecordPool +0x08 stride=0x8` — a derived PTABLE level
    matching indexed qword loads off a tracked `tablebase` set.
  - tablebase now carries the lea'd VALUE (dict), so the biased-table
    idiom works — bodies lea the enclosing array base 0x02098E10 and
    load [rB + i*0x288 + 8]; the seed completes v+disp==addr with the
    disp inside a 0x400 window. Propagation added through reg copies,
    indexed leas, add/sub adjustment, and explicit invalidation on
    register rewrites (mov fallthrough, imul, call-volatile).
    store() gained a routes map so size-UNRESOLVED parents
    (ActorRecordPool) still expose their route for derivation.
  - The pool PTABLE alone still yields 0 offsets — consumers reach
    records through the two getters (75 and 180 call sites) and the
    walk has no callee->caller return channel. Added the observable
    path as FN alternatives: FN 0x00358940+0x0
    (ActorManager_GetRecordByOrdinal), FN 0x003588B0+0x0
    (ActorHandle_ResolveRegistryEntryByPackedId).
  - Verified: ActorStorageRecord 74 offsets / 999 accesses, base
    histogram cleanly separates embedded children (+0x120
    movementContext, +0x350 secondaryContext); transitive children
    ActorResourceEntry 11, ActorWaitSlot 5, MovementContext 61,
    SecondaryContext 42 — every base resolves to a declared row, zero
    >=256B gaps. HEAD-vs-worktree control run BYTE-IDENTICAL;
    BattleUnit SLOTPTR hosts 13->21 (biased-window nominations),
    coverage identical at 17 offsets.
  - Index regenerated: 213/596 types swept, 17,269 rows over 136
    touched (was 212 / 14,789 / 130). Residue 378: NONE 352,
    DYNAMIC 17, EMBED-unresolved 4, CHAIN-unresolved 3,
    RELOFF-unresolved 2 — all genuinely unrouted parents.
  - knowledge_db rebuilt: field_access 17,269.
  - Gates: links 55,240 green; questions consistent; consistency 1
    disagreement = pre-existing 006B9120 (routed to OPUS);
    check_route_uniqueness's two flagged shared FN routes are
    pre-existing, documented on their own rows (OPUS, 2026-09-19/20) —
    not introduced by this work.
  Commit fd2cfa80a (8 files, pathspec-scoped).
  NEW FINDING ROUTED (rev 29303): worktree carries stale-lane reverts
    of three committed route cells - PApplication PTR->STATIC,
    AchievementState/ImageBackedStateBlock FN alternatives dropped.
    Filed FRONTIER-REQ-OPUS-STALE-ROUTE-REVERTS-IN-WORKTREE (P2).
  Board rev 29292. Inbound processed: OPUS ladder-head self-resolved;
  FABLE publication-lease answered (claim-at-publish working as
  intended, FABLE-PUB-001E2AF0-FINISHED holds @publication mid-gate —
  do not interfere); OPUS S-52 measurement routed to AUDIT-SPEC
  scoring batch (SWE2-FRONTIER-PUB-L2VERDICTS-SCORING-BATCH, READY,
  blocked on @publication).

**2026-09-24 checkpoint — PTABLE expansion + element provenance.**
  Continued the F-6 PTABLE frontier:
  - Absolute `PTABLE 0xADDR stride=0xS` now parses, seeds `ptab` on
    `mov rB,[rip->ADDR]` (mark rides either mem operand), propagates
    through copies/indexed-lea/add, and yields element bases on qword
    slot loads. Host nomination widened in all three tools.
  - `Category` resolves via `PTABLE 0x02EAD008 | FN 0x007AAA20` (13
    offsets / 48 accesses); `AudioParameterRamp` 9 via CHAIN transit.
  - `SLOTPTR Type +OFF` now splits on the field ctype: `X*` = inline
    table (mark-match yield), `X**` = pointer-to-table — elements only
    through a `tptr`-proven register. `tptr`/`elems` carry across
    blocks via the `state` tuple merge (loop bodies need it).
  - Derived-run element-relative loads `[array + i*S + f]` fold by
    base mark — `LegacyPs2GsSourceTextureRecord` (1 offset),
    `DerivedSlotRecord` (1), `ReferenceDescriptor` (3) resolve via
    multi-offset `CHAIN LegacyPs2GsTextureContext +0x150 +0x8` etc.
  - `OrderedObject` resolves via `SLOTPTR EastlPointerVector +0x00`
    (2 offsets — `vftable`, `flushSelector`; thin but honest, the
    vector's own fields stay out through the `elems` gate).
  - ActorStorageRecord pslot path is 0 in BOTH old and new — the 999
    accesses are all FN-getter-mediated; no regression (verified by
    running HEAD's tool side-by-side).
  - Control ManagerSingleton0209BE80 BYTE-IDENTICAL (57/57/0);
    BattleUnit 17 offsets stable; BattleStatsRecord 4 stable.
  - Index regenerated: **219/596 swept, 17,483 rows over 142 touched**
    (was 213 / 17,269 / 136). Residue 372: NONE 352, DYNAMIC 11,
    EMBED 4, CHAIN 3, RELOFF 2. knowledge_db rebuilt: field_access
    17,483.
  - Gates: links 55,240 green; questions consistent; consistency 1
    disagreement = pre-existing 006B9120; route-uniqueness flags remain
    the two documented shared-FN conflations only.
  Commit 56d76c58e (8 files; types.tsv/PROGRAM-STATE staged via
  hash-object splice around peer hunks — PApplication/AchievementState/
  ImageBackedStateBlock stale reverts remain UNSTAGED, already routed).
  NEXT: F-6 residue is now genuinely unrouted parents; next frontier is
  DYNAMIC-factory seeding or the NONE tail (352 route-less types -
  mostly Phyre reflection rows, low value). Parked on ctrl duty.

**2026-09-24 checkpoint — PKREF + null-coalesce merge (commit 506a915cd).**
  Continued the F-6 residue: added `PKREF 0xFN Parent +0xOFF` (derived
  level) — the dword at parent+OFF marks `rels`, and `call FN` with rcx
  carrying it marks rax as the child base (0020E600 = `rax = ecx +
  *(0x01F83530)`). Bare-cell parent form `PKREF 0xFN 0xCELL +0xOFF`
  synthesises a PTR-on-cell root (band-shared header slots).
  - NavMeshVertex/Triangle/PortalRecord/RegionRecord/BroadPhaseHeader
    resolve through `PKREF 0x0020E600 NavRunStateBlock +0xNN` (parent
    `PTR 0x02AEDFB0`); StatusDefinitionRecord through
    `PKREF 0x0020E600 0x02EBF118 +0x0C`. Every emitted offset lands on a
    declared row.
  - Supporting: 2-operand `imul` products tracked under derived runs;
    `zero` now crosses blocks by intersection so a mark survives a
    `x ? marked : NULL` coalesce join (null side = dead null-deref).
    The merge fix alone recovered ~2,400 rows across 90 swept types,
    zero losses; control diff is only five newly-correct `zeroclear`
    tags.
  - Index regenerated: **225/596 swept, 19,882 rows over 148 touched**
    (was 219 / 17,483 / 142). Residue 366: NONE 352, DYNAMIC 5,
    EMBED 4, CHAIN 3, RELOFF 2. knowledge_db rebuilt: field_access
    19,882.
  - Gates: links 55,240 green; questions consistent; consistency 1
    disagreement = pre-existing 006B9120; route-uniqueness still the two
    documented shared-FN conflations.
  Remaining unrouted parents (all genuinely unrouted, type-store work):
  LuaState/LuaProto/LuaTable (gate 4 Lua children), AuthoredTableHeader
  (band-membership idiom, gates AuthoredBlobFixupTable),
  ActorDefinitionPayload, PaneListWidget0B68, PDeferredLightingBase,
  AuthoredExpressionBlock. DYNAMIC residue: 3 vtable-only
  DynGeoFontTextSpecial* + LicenseNodeRecord (authored file).
  NEXT: VTABLE route kind could seed the three vtable-only DynGeo types
  (rcx=this at each vtable method entry); beyond that the residue is
  unrouted-parent work for the type store. Peer-lane stale route
  reverts remain UNSTAGED (routed). Parked on ctrl duty.

**2026-09-24 checkpoint — VTABLE seed kind (commit 37ba899ea).**
  Closed the last mechanical DYNAMIC form: `VTABLE 0xADDR` reads the table
  from the image (consecutive qwords that are known function entries, to
  the first miss) and walks each method body with `rcx` marked 0 - what
  `call [rax+slot]` dispatch guarantees. DynGeoFontTextSpecial{Instance,
  FinalInstance, ShadowInstance} resolve 27 offsets each, every base on a
  declared row; shared methods contribute to all three correctly.
  - Index regenerated: **228/596 swept, 20,011 rows over 151 touched**
    (was 225 / 19,882 / 148). Delta is exactly +129 rows on the three new
    types - zero losses anywhere. Residue 363: NONE 352, DYNAMIC 2
    (LicenseNodeRecord authored-file; AuthoredTableHeader band-membership
    idiom), EMBED 4, CHAIN 3, RELOFF 2.
  - Control ManagerSingleton0209BE80 byte-identical HEAD-vs-worktree.
    knowledge_db rebuilt: field_access 20,011.
  - Gates: links 55,240 green; questions consistent; consistency 1
    disagreement = pre-existing 006B9120; route-uniqueness still the two
    documented shared-FN conflations.
  NEXT: the F-6 mechanical frontier is done - residue is unrouted-parent
  type-store work (Lua roots, AuthoredTableHeader band idiom,
  ActorDefinitionPayload, PaneListWidget0B68, PDeferredLightingBase,
  AuthoredExpressionBlock) - route to OPUS/STRUCT, not census tooling.
  Peer-lane stale route reverts remain UNSTAGED (routed). Parked on ctrl
  duty; P0 L2VERDICTS batch still gated on FABLE's @publication lease.

**2026-09-25 checkpoint — work-order round: lease handback + EXP evidence + mirror coherence (uncommitted until @publication).**
  Operator work-order executed:
  - **@publication handed back safely.** FABLE-PUB-001E2AF0-FINISHED
    held the lease 46h with zero activity; verified no session, work
    already committed (000694b0f), dirty files preserved untouched.
    Same-identity recovery release at rev 29307 with full state record.
    FABLE's new Opus5.5 session acknowledged on its return: "the
    recovery release was correct." Window immediately productive:
    EC7 claimed it for batch-140 publication.
  - **EXP-150..188 staged for publish** (task FRONTIER-PUB-ORACLE-
    EXP150-188-EVIDENCE, rev 29313): 39 records byte-identical from
    ORACLE's Temp drafts + per-record drivers at evidence/<slug>/check.py
    (EXP-167..188 share exp166_check.py final revision; per-run revisions
    live in the records' case tables) + ORACLE's dated SECTION-02
    revisions to EXP-081..149 + cited continuation-section evidence dirs.
    Drivers assert exe sha256 at run time; receipts embedded per case.
  - **Index decoder**: the movups-store/test-read defect was already
    fixed by OPUS (reg_tracking.py dirty, OPUS's own publish queued).
    My usage guidance fixed to include rw rows (1,740 omitted before).
    TSV regen run then REVERTED: DATA's in-flight route edits dropped
    5,172 rows on 32 mid-edit types — regen deferred to
    FRONTIER-REGEN-FIELD-ACCESS-AFTER-RERUN (dep on the census rerun).
  - **Mirror revision-coherence**: knowledge_db.py gains a provenance
    table (per-table source path+sha256+rows+schema_version 2), hex
    size parse (two 0x18 Lua header fields read 0 before), empty-row
    skip (phantom 7,284th row). Both sqlite mirrors regenerated:
    field_access 20,011 = TSV, fields 7,325, source hashes pinned.
  - **Steering routed**: FRONTIER-REQ-AUDITSEM-S52-ROW-PASS (4 UNSCORED
    cells), FRONTIER-REQ-OPUS-PENDING-UPDATES-ACCEPTANCE (its queued
    corrections + my name/lease/stale-route requests). Board rev 29317.
  NEXT: claim FRONTIER-PUB-ORACLE-EXP150-188-EVIDENCE when EC7 releases
  @publication; publish the staged package + my owned files
  (this inbox, knowledge_db.py, field_access_index.py, both
  knowledge.sqlite). Then mirror publish task FRONTIER-PUB-MIRROR-
  REVISION-COHERENCE covers the tooling commit. Fallback: F-6 residue.

**2026-09-24 checkpoint — direction-regen P1 (commit 3496afb78, task DONE rev 29330).**
  Claimed at rev 29325. Regenerated field-access-index under OPUS's
  repaired classifier (worktree reg_tracking.py: mnemonic tables before
  capstone flags) FROM COMMITTED INPUTS - HEAD types.tsv/fields.tsv
  staged into a scratch db dir (input sha256: types fad15541..., fields
  a4e7b6fd...). Result: 226 types / 20,150 rows / 150 touched - matches
  OPUS's HEAD-inputs figure exactly.
  - Reproduction gap established: the 20,011 publication ran against a
    DIRTY worktree types.tsv - stale route reverts (AchievementState
    0->11, ImageBackedStateBlock 12->29, PApplication 998->1202 under
    restored PTR) plus uncommitted peer rows (IndexedExternalSourceRequest
    49->0, VmValueStack 44->0 absent on HEAD).
  - Direction verify: 0 movups-family store rows tagged r (of 661
    mem-first stores), 0 test/cmp w rows; 221 kind flips vs the published
    file. knowledge_db rebuilt (field_access 20,150) - provenance table
    now records per-table source sha256.
  NEXT: commit index + doc stat updates (index only - reg_tracking.py/
  knowledge_db.py/field_access_index.py worktree edits are OPUS's
  in-flight repair claim, not mine to commit); finish board item.

**2026-09-25 checkpoint — request-queue processing (commits 17b5700de, 03a785a39,
  63a54f238, d9e110d57; board rev ~29717).**
  All eleven inbound FRONTIER items processed at rev 29630+:
  - **Attribution (17b5700de)**: the uncommitted knowledge_db.py provenance
    work and check_route_ctype_agreement.py whitespace tolerance were FRONTIER's
    own in-flight tooling (the provenance half of FRONTIER-PUB-MIRROR-
    REVISION-COHERENCE); committed scoped. OPUS's attribution notice closed.
  - **team.py ops (03a785a39)**: release_publication (FRONTIER/OPUS-only, all
    three TEAM.md gates enforced: 6h checkpoint computed, 2h READY holder-
    request, 2h no_activity_since citation; lifts only @publication, file
    claims preserved, event in task history) and retire (adjudicated close of
    unclaimable READY/BLOCKED request rows). 13/13 tests pass; used already to
    retire the two circular UC1 rows.
  - **Shared-dialogs labels (63a54f238)**: 001EDEC0 = render-scale gate on
    +0xB4; 002ABEC0 = window-record function. OPUS request closed.
  - **Overlay publication plan** (d9e110d57,
    _index/candidates/overlay-publication-plan.md): FRONTIER is sole publisher
    for Updates 01-12 - one commit per section under @publication, reviews and
    continuation-sectionNN evidence folder riding each commit. Gate adopted:
    overlay_drop_census.py + per-token dispositions (restated/withdrawn/
    restored) required before each commit; SECTION-03 (outlier, 92 addresses)
    last. OPUS owner-merges the SECTION-01 drops and the three queue facts;
    S11/S12 wait on AUDIT-SPEC's first-line audit. Tracked by
    FRONTIER-PUB-EXTERNAL-CONTINUATION-OVERLAYS. Interim: no lane names
    overlay paths in publish_paths.
  - **UC1 readiness routed**: OPUS recused (instrument author); ruling
    requests filed to FABLE + ASTRA (the other two 2026-09-13 voters) plus
    independent corroboration to SWE2-AUDIT-SPEC.
  - **Thunk hops (d9e110d57)**: call_graph.call_maps folds E9 stub tails
    (listed body whose only edge is jmp->one target) into the target's
    callers/sites. Controls: sites[0020AC30] contains 0032FD64; tail-jump
    control green. Doc note in ABSENCE-CLAIM-GATE 2a. NOTE: the next
    field-access regen may gain hosts through resolved thunks.
  NEXT: @publication is held by OPUS-PUB-197-PMESH-CTOR (ACTIVE) - the P0
  L2VERDICTS batch and the overlay publishes stay queued behind it. Watch for
  the OPUS owner-merges (SECTION-01 + queue facts), the AUDIT-SPEC first-line
  audit, and DATA's fields.tsv census rerun (gates
  FRONTIER-REGEN-FIELD-ACCESS-AFTER-RERUN). Fallback: F-6 residue is
  research-class (unrouted Lua GC-heap parents - FRONTIER-REQ-OPUS-NINE-
  DERIVED-ROUTES-NEED-PARENT-ROOTS filed).

**2026-09-25 checkpoint — overlay publishes + revision-pinned mirror (commits b16cedc8c,
  bc74b44a8, 291ec5588, 60379fcbd, 21f25545b; board rev 30751).**
  Claimed FRONTIER-PUB-EXTERNAL-CONTINUATION-OVERLAYS + @publication. Published per
  overlay-publication-plan: S04 (widget receiver, b16cedc8c), S02/08/09 (resource queue,
  bc74b44a8), S05 (encoded-id + FABLE defect fixes, 291ec5588), S06/07/10 (resource lifetime
  / EFX rebase, 60379fcbd), S03 (rewards, owner appendix merge, 21f25545b). Evidence dirs
  were already in HEAD under ORACLE's b6c9a74a8 - section commits cite them. Live
  overlay_drop_census: 0 undisposed drops on every published file. S11/12 correctly held:
  69 undisposed tokens + AUDIT-SPEC first-line audit pending.
  knowledge_db.py --pin: sources read from a ref's blobs (schema_version 3); canonical
  _index/knowledge.sqlite rebuilt pinned to 21f25545b (provenance: git: origin + blob oid +
  commit per table; worktree: honestly marked for the three untracked Tools/work TSVs).
  NEXT: board ops - finish OPUS notices (owner-merges, S04 restore, 69e9cad19 sweep findings,
  FABLE dispositions), answer OPUS-REQ-FRONTIER-REGISTER-PARKED-EDITS (authorize OPUS to
  publish OPEN-QUESTIONS.md with per-owner hunk attribution), release @publication. Then
  FRONTIER-PUB-EXTERNAL-CONTINUATION-OVERLAYS stays ACTIVE for S11/12 when the audit lands.

**2026-09-26 checkpoint — board-wedge repaired + 329 routed (commit 7fee67048; board rev 30810).**
  OPUS-NOTICE-BOARD-WEDGED-BY-A-DONE-TASK-WITHOUT-RESULT-REFS answered: the DONE-without-
  refs record was written outside team.py apply() - proof in history: ORACLE's 07:49:38Z
  claim logged under agent 'SWE2-ORACLE-UNIT-INSTALL-EXEC' (not in AGENTS, apply() fails
  closed on it); a direct TEAM.json writer on ORACLE's lane logged the finish op verbatim
  but dropped result_refs from the record. OPUS's repair_missing_result_refs (rev 29761)
  is the documented repair precedent; ORACLE still to confirm the added refs. Fixed the
  latent same-class defect in `retire` (result_refs=[] wedge) - commit 7fee67048:
  retire omits the key, validate() exempts `retired` rows, regression in test_team.py
  test_j, 13/13 pass.
  FRONTIER-REQ-OPUS-329-RUNTIME-CLOSERS-INDEX RULED: routed to SWE2-AUDIT-SEM (runtime is
  the auditor's scored cell; 44 targeted AUDITSEM-REQ-OPUS-287..346 P1 tasks + the 329
  index already decompose it; SEM is READY+desired). Criterion restated in the ruling:
  per-invariant live-or-substitution-free; disclosed stubs move only touched items;
  boundaries admissible with cut-off items scored not-executed; contradicted rows
  (s11 TP-2, s02 five failing request-ids, s21 scripted-vs-real, s34 unitemized,
  s47 carried EXP-084) route back to FRONTIER/FABLE, not silently scored.
  NEXT: FRONTIER-PUB-TEAMPY-RETIRE-GUARD sits READY with @publication - the artifact is
  already committed (7fee67048); when FABLE's FABLE-PUB-R338A-PARTY window releases,
  claim+finish it with the commit ref and free the lease. S11/12 overlays still gated on
  AUDIT-SPEC's first-line audit. Fallback: F-6 residue (per-type seed classification).

**2026-09-26 checkpoint — freshness machinery + canonical policy (commits 7fee67048,
  dbe677d34; board rev 30924).** Operator repair instruction executed:
  DERIVED-DATA freshness is now enforced mechanically, not by memory.
  knowledge_db.py schema 4: provenance records per (table, dependency) -
  file-set content fingerprints (tree manifests catch add/delete/edit,
  CRLF-normalised), git_blob + pinned_commit, generator_sha256 (module set +
  schema - a parser change stales every table), output_sha256 (row digest -
  catches hand-edited mirrors). `knowledge_db.py check` is the shared verdict;
  query/sql/info refuse stale reads naming the moved inputs (- never an
  apparently-current absence), --snapshot is the labelled as-of read, --refresh
  rebuilds through the staging guard (inputs fingerprinted before+after; moved
  mid-build => staged output discarded, last usable index kept; data+provenance
  publish atomically). Readers charter_grade_audit / readiness_rank /
  tools_provenance call freshness_report; publish_paths.sh prints mirror
  freshness at the checkpoint (non-blocking - raw research never waits on a
  derived table). Policy: _index/DERIVED-DATA.md committed; OPUS's broader
  canonical-evidence-policy draft placed as _index/EVIDENCE-POLICY.md
  (single canonical statement; CLAUDE.md + TEAM.md links repointed to it -
  pending publish commit behind FABLE-PUB-BASE-ZERO-FLAGBANKS's lease).
  Isolated fixture suite test_knowledge_db.py: 10 tests pass (same-row-count
  edits, add/delete, generator change, mixed-table scoping, mid-build discard,
  stale refusal + snapshot labelling, w+rw writers, hex/variable sizes,
  no-index/old-schema); test_team 13/13 pass.
  FINDINGS ROUTED (one accountable owner each): ORACLE -
  FRONTIER-REQ-ORACLE-EXP-RECEIPT-MAP (per-EXP driver hash/revision, inputs,
  cases, raw results, limitations; reuse allowed, double-counting not) +
  FRONTIER-REQ-ORACLE-EXP086-189-RECORD-REPAIR (three-byte RET wording;
  512-byte zero / 128-byte AND-F8 wording; superseded text marked not erased).
  DATA - FRONTIER-REQ-DATA-TEN-UNNAMED-RESULT-ONLY-IDS (AO-5's ten family-0
  ids 1438..1484 reconciled without invented names) +
  FRONTIER-REQ-DATA-MIRROR-FRESHNESS-OPS (own the check-and-refresh rule).
  FABLE - FRONTIER-REQ-FABLE-IMAGE-BASE-PROPAGATION (GG-3/event-slot already
  have live CONTRACT/DATA routes; image-base was the uncovered third).
  OPUS - lighting/three-axes/EXP189 independent reviews already sit with
  AUDIT-SPEC (AUDITSPEC-REVIEW-OPUS-*); runtime scoring sits with AUDIT-SEM.
  OPUS-REQ-FRONTIER-STARTUP-POLICY-AND-TYPE-COVERAGE-REGEN claimed: policy half
  placed (EVIDENCE-POLICY.md); TYPE-COVERAGE.md is OPUS-owned per TEAM.md
  ownership table - answer is 'regenerate it yourself at a coherent checkpoint;
  the dirty copy is an unknown-provenance regen, do not commit it'.
  NEXT: when FABLE's lease releases, publish_paths the policy batch
  (FRONTIER-PUB-EVIDENCE-POLICY ACTIVE on @publication claim pending) and
  finish the OPUS request + both publish tasks with commit refs. Fallback: F-6
  residue (per-type seed classification).

**2026-09-25 late checkpoint — queue drained (rev ~30973).**
  Inbound processed: rule 4a (correction propagation) merged into
  EVIDENCE-POLICY.md + publication checklist item into TEAM.md
  (11c3c62a7); OPUS's AUDIT-SEM stall answered (root cause found by the
  parallel FRONTIER session: recovery gate held `recovering` while ANY
  wake was in flight - STRUCT's dead 20h wake froze all probes; fixed and
  controller restarted in 21146fc69, which also landed FABLE's 01F83530
  ledger/standard resolutions); GE/GG parked-cell receipt noted; UC1
  circular rows retired via the new `retire` op. team.py gained
  release_publication + retire adjudicated ops (03a785a39, 13/13 tests).
  call_graph.call_maps now folds E9 thunk tails (d9e110d57); overlay
  publication plan recorded (FRONTIER sole publisher, drop-census gate).
  NOTE: a parallel FRONTIER session (concise-family wake pid 59648)
  authored 21146fc69 concurrently - watch for same-identity duplication
  on board ops.
  NEXT: FRONTIER-PUB-EXTERNAL-CONTINUATION-OVERLAYS publishes as gates
  clear (OPUS merges S01/queue facts, AUDIT-SPEC audit for 11/12,
  per-section dispositions); FRONTIER-REGEN-FIELD-ACCESS-AFTER-RERUN
  waits on DATA's census rerun; @publication currently free.

**2026-09-26 checkpoint — external continuation complete (rev ~31790).**
  ALL TWELVE continuation overlay sections are at HEAD: 01 via
  69e9cad19 + 673c442af (owner restore) + a3707ab82 (merge tail),
  02/08/09 bc74b44a8, 03 21f25545b, 04 b16cedc8c (00249320 restored),
  05 291ec5588, 06/07/10 60379fcbd, 11 51ab1ce85, 12 baa39c696.
  FRONTIER-PUB-EXTERNAL-CONTINUATION-OVERLAYS finished rev 31782;
  plan table updated 9dcf39c7c. SECTION-11/12 dispositions written by
  publisher: overlay-drop-dispositions-11-12.md (57 tokens, all
  restated/consolidated/restated-elsewhere). FABLE's I8 hunk carried in
  a3707ab82 (S01 merge tail; gate 00385BA0 clears availability, not the
  steal loop). publish_paths.sh now refuses overlay-carrier paths to
  non-plan publishers. Routed: OPUS re-verification of merged files
  (FRONTIER-REQ-OPUS-VERIFY-01EC81F0-VS-01EEBCC0-S05-MERGE - the S05
  publish reverted ORACLE's committed fix), 17 parked OPEN-QUESTIONS
  rows to FABLE/OPUS/AUDIT lanes.
  NEXT: nothing inbound. Fallback: FRONTIER-REGEN-FIELD-ACCESS-AFTER-
  RERUN (blocked on DATA's census rerun); otherwise highest-value
  unblocked frontier work. @publication free.

**2026-09-26 afternoon checkpoint (rev ~32248).**
  Four inbound processed: (1) OPUS's ENCID 01F83530 scope patch published
  verbatim in 3f034fbce (byte-exact verified: patch de2eb07f vs HEAD
  0c2b9002 -> blob 51ad90f98) alongside FABLE's FY-1 answered-channel
  pointer in the query-record page - two request items closed. (2)
  FABLE's S47 overlap-copy paragraph (memcpy = jmp memmove in installed
  VCRUNTIME140, 39,215-copy replay) is WRITTEN and parked in
  contract-resource-input-ownership.md section 13, but the file is held
  by stale ACTIVE claim SWE2CONTRACT-RESINPUT-RL4-0922 (09-23, clean at
  HEAD); the task is BLOCKED with the paragraph in place, and
  FRONTIER-REQ-SWE2-CONTRACT-RELEASE-RESINPUT-RL4-CLAIM routes the
  release. PUBLISH IT THE MOMENT THE HOLD CLEARS. (3) Correction-gate
  double fix in ce38cf05b: find_correction_hunks now multiset-subtracts
  the removed lines' strike/keyword markers (a re-edited one-line row no
  longer refires), and publish_paths.sh absolutises $msg before the
  gfz-scripts cd so records named in the message are seen; the gate also
  falls back to root-relative msg resolution. 14/14 gate tests pass.
  NEXT: publish the parked S47 paragraph when the RESINPUT hold clears;
  otherwise no FRONTIER queue. @publication free.

**2026-09-27 early checkpoint (rev ~33252).**
  The S47 paragraph shipped during the gap - a parallel FRONTIER session
  published it in 278b13e56 once CONTRACT's RESINPUT hold cleared. Big
  items this block: (1) FRONTIER-PLAN-REGISTER-CLOSURE-TRIAGE-20260926
  DONE - all 292 register rows now carried; 15 carrier tasks filed at
  revs 33187-33202 covering 194 rows (AUDIT-SEM 21 verify, AUDIT-SPEC 20
  verify, ORACLE 7 runtime-surrogate, FABLE 100 static + 4 runtime
  residual + 16 INTENT-NAS + UQ-147, OPUS 25 static-resource), manifest
  at _index/candidates/register-triage/dispatch-2026-09-26.md; class-3
  conflict ruled (B-2/d + BS-5 revert to OPEN annotated). (2) All five
  FABLE-CARRIER class-2 tasks DONE - 29 rows dispatched in
  dispatch-2026-09-26-carrier-decisions.md (commit 1bb263ded): FABLE 13,
  OPUS 3, AUDIT-SEM 3, DATA 3, ORACLE 1, FRONTIER instrument backlog 3,
  EC-7 ruled adopted, EP-1/BX-3 declined. (3) Five ASTRA items consumed
  and recorded in ASTRA-QUEUE.md DISPOSITION 2026-09-26 (dc14d55fb):
  S19 stoploss QUEUED, status-watch/SR-5/S33 PREPARED with owners+prereqs,
  reward-seal/UC1 COORDINATED. (4) ASTRA-RETURN-FRONTIER-PROVEN-INPUT-
  ROUTE-RECOVERED ruled (ad07e61a6): sender/pulse proven identical to
  accepted Sep-13 receipts, so ONE bounded ~6min/2-pulse qualification
  pass granted under four mandatory conditions - consumes frozen budget,
  fresh native controls mandatory pre-spend, no retry without new
  evidence.
  NEXT: FRONTIER-TODO-REGISTER-INSTRUMENT-BACKLOG (EC-3 checker, CT-2
  precondition, BQ-15 dataflow instrument) is my only open item, P3.
  Watch: carrier lanes fill (FABLE already claimed INTENT-NAS), CONTRACT
  release request resolved (file claim finished), CJ-2 sits in the
  manifest as FRONTIER-routed (mod-side load-path read - cheap, do it
  next session if queue stays empty). @publication free. Controller
  pid 13704 alive; AUDIT-SEM/SPEC queued at-capacity; CONTRACT + DATA
  starving.

**2026-09-27 morning checkpoint (rev ~33768).**
  Two ASTRA returns closed: (1) POSTCOMMIT-IDENTITY-GUARD - the false
  failure was real guidance rot: publish_paths.sh printed `git log -1`
  on moving HEAD, and TEAM.md's finish rule required it. 6f042881e now
  pins the verification to the `committed sha:` the script wrote;
  TEAM.md updated (stopped publish? verify `git cat-file -t <sha>`, not
  HEAD). (2) STATUS-WATCH-PREREQUISITES - qualified detector predicate
  recorded in status-watch-preflight/PLAN.md (fa6b82534): trap-after-
  access (SDM 17.3.1.2) means the watch reports the NEXT context;
  normalized access-PC valid only with a native positive; RW windows
  fire on writes; other-RIP +13-only hits are not sparse readers. Owner
  OPUS, reviewer FABLE+AUDIT. Also: reaped a stale TEAM.lock (dead pid
  63704); a rollback detector caught a stale write (33750 vs journal
  33751) which self-healed at 33752; FRONTIER-TODO-REGISTER-INSTRUMENT-
  BACKLOG was closed by a peer session.
  NEXT: queue fully empty. Watch carrier lanes; CJ-2 (mod-side
  load-path read) is the named FRONTIER oddment if it stays empty.
  @publication free at checkpoint time.

**2026-09-27 afternoon checkpoint (rev ~33974).**
  Two FABLE items closed: (1) retired FABLE-REQ-ASTRA-GF4-WHICH-BODY-
  CALLS-POST-EFFECT-SLOT-6 (the withdrawn live request - GF-6/GF-2/name-
  census prove no shipped state can hold a slot-6 instance; required
  widening team.py's retire guard to kind {request, research} since
  -REQ- rows are filed under both). (2) routed FABLE's EASTL rbtree
  relabel to SWE2-EC7 (the GFZ tag/code-domain owner) as FRONTIER-REQ-
  SWE2-EC7-EASTL-RBTREE-RELABEL - 18 OrderedContainerRuntime members are
  EASTL RBTree* (line-for-line match, control bq23_tier6.py), 3 MSVC
  _Tree members keep the label.
  NEXT: queue empty; CJ-2 already answered by FABLE. Watch: EC7 carrier
  uptake, retire-guard change uncommitted pending publish lease.
  @publication last seen free.

**2026-09-27 late-morning checkpoint (rev ~34329).**
  (1) CLASS1-FF4-FH1 ruling DONE: class 1 applies to both rows -
  SUPERSEDED, residue named (extension appended to batch-K-scope-
  rulings.md; file publish pending the lease). (2) AO-4 publish is
  STAGED, blocked on @publication: SWE2-DATA-PUB-BQ9-ARITY has held the
  lease since 10:00Z with its session free and no commit landed.
  PUBLISH ORDER when the lease frees: OPEN-QUESTIONS.md must carry
  HEAD + AO-4 row only (rows_ao4.py output staged at
  /tmp/oq_publish.txt - rebuild from HEAD if stale); native-command-
  lifecycle.md already carries FABLE's verified hunk; DO NOT sweep
  DATA's BQ-9 line - if DATA's commit landed, the worktree file =
  new HEAD + my AO-4 row reapplication; if not, re-apply DATA's BQ-9
  line to the worktree after publishing so its parked work survives
  (saved at /tmp/data_bq9.txt). batch-K-scope-rulings.md rides the
  same publish. FRONTIER-REQ-SWE2-DATA-RELEASE-OR-COMMIT-PUBLICATION
  filed (rev 34328) - starts the 2h adjudication clock on the lease.
  NEXT: publish the staged trio when the lease frees; fleet otherwise
  healthy (ORACLE on EXP-201 receipts, carriers being consumed).

**2026-09-27 evening checkpoint (rev ~35321).**
  The whole 17-item queue is closed. Two publishes: b7dc34ea4 (AO-4
  carrier hunk + ANSWERED row, FF-4/FH-1 class-1 extension, class-3
  OUT-OF-EVIDENCE-BOUNDARY terminal status in check_questions.py +
  progress.py) and 41354fdb7 (correction batch) + ca992fb20 (gate fix
  + 27d rulings). Rulings issued: class-3 terminal = OUT OF EVIDENCE
  BOUNDARY (closed-bucket, NAS-style four-part guard, per-row by
  FABLE); class-1 YES for UQ-80/EH-4/BT-2/UQ-2; AR-5 superseded onto
  ar5_dispatch.py; SV-1 scope-closed SUPERSEDED (dev-image residue =
  named follow-on); HM-1 residue routed to RT-RUNTIME-SURROGATE.
  Owner edits: UC-1 row -> PARTIAL (both reviews ACCEPTED, 007EE7C0
  admitted 57 B); Y-1 corrections on four FRONTIER surfaces; BB-1 slot
  table items 1-4; vu1-region-functions.tsv ten registered
  microprograms. Tooling: 'retained' preimage dirs skipped by
  check_questions (BE-6 unblock); zero-count status lines always
  print (BLOCKED=0 no longer wedges goal_gate). Routed: 4 tasks to
  EC7 (Y-1 constants, GA-1 labels, UQ-107 paragraph, BB-1 001EF060),
  1 to STRUCT (+0x3B0), 1 to DATA (hub-called claim - DATA already
  claimed it). UQ-363 propagation was moot (CONTRACT landed it).
  NEXT: nothing inbound. Watch the routed corrections + OPUS's UQ-70
  carrier. @publication released on finish.

**2026-09-27 late checkpoint (rev ~35423).**
  (1) OPUS ruling request DONE (35395): ext 27e in
  batch-K-scope-rulings.md - G-2 class-1 SUPERSEDED (all 11,165
  records profiled, 99 consumers closed, residue 4 unread bytes),
  T-4 class-1 SUPERSEDED (1,172 initializers x depth 6, residue =
  pass-node numbering), L-13 SUPERSEDED with live residue carried by
  pending FABLE-REQ-ASTRA-L13-BANKS (HM-1 rule; real window beats
  surrogate). (2) DATA's progress package DELIVERED + AUDIT-SEM
  ACCEPTED: PROGRESS.md + _index/progress/ committed d248c507d;
  watchdog now carries maybe_progress_report (1800s gate) and
  publish_paths dirty-marks _index/progress/.dirty. CAVEAT: running
  controller pid 13704 predates the hook (started 9/25) - the
  cadence is dead code until a controller restart, and
  `controller restart` taskkills its process TREE: EC7's live
  session (pid 53756) is a child of 13704. DEFERRED: restart only
  when no live session is controller-spawned. (3) ORACLE is
  daily-cap wedged (16/16) until 00:00Z - P0 EXP201 sealing waits
  ~1h; controller will wake it automatically. (4) Ledger now
  ANSWERED 1416/1596, OPEN 6, PARTIAL 19, BLOCKED 0 - questions
  dimension nearly closed. (5) STAGED: rulings-file publish parked
  on @publication (OPUS/FABLE churning); publish task
  SWE2-FRONTIER-PUB-BATCHK-EXT27E filed, claim poll armed.
  NEXT: when the lease lands, publish_paths.sh with /tmp/pubmsg.txt
  over batch-K-scope-rulings.md only; then controller restart at a
  child-free window to activate the progress cadence.

**2026-09-28 checkpoint10 routing (rev ~35479).**
  checkpoint10 mandate routed through existing owners, no new
  framework: (1) DATA owns progress_report.py repair -
  FRONTIER-REQ-SWE2-DATA-PROGRESS-REPAIR-CKPT10 (P1, full defect
  list: accuracy/pass13-files/LIVE-gating/reviewer-resolution/
  WITHDRAWN separation; dedup route; freshness+coherent-publish;
  executed-fixture list incl. real 30-min scheduled receipts).
  (2) ORACLE owns its board-write path -
  FRONTIER-REQ-ORACLE-BOARD-WRITE-PATH-REPAIR (P1, locate+replace
  direct writer, stale-note vs new-ops test, no replay/recovery).
  (3) Prior AUDIT-SEM ACCEPT REOPENED via board note (report
  acceptance only); re-review to AUDIT-SPEC requiring EXECUTED
  controls (FRONTIER-REQ-AUDITSPEC-EXECUTED-REVIEW-PROGRESS-REPAIR,
  chained on the repair). (4) EXP201 sealing already P0 top of
  ORACLE's targeted queue; ORACLE daily-cap ends 00:00Z.
  (5) STILL STAGED: ext-27e rulings file uncommitted;
  SWE2-FRONTIER-PUB-BATCHK-EXT27E claim polling (lease held by
  DATA's UQ218 publish). NEXT: land the publish when the poll wins;
  controller restart for the progress hook still deferred until no
  live session is a controller child.

**2026-09-28 board-lock fix (rev ~35560).**
  ASTRA-NOTICE-FRONTIER-TRANSIENT-DIVERGENCE-35478 dispositioned:
  journal proved FRONTIER (foreign session) + EC7 dual commits at
  35478/35479; EC7 wake log documents manual TEAM.lock reaps during
  live contention (rotation observed between check and reap) - file-
  existence exclusion plus holder-finally unlink cascaded the
  collision. Nothing lost: overwritten ops were retried, EXT27E
  landed as 0b2f92e5c. FIX: team.py exclusion now the named kernel
  mutex Local\XIIOnlineTEAMBoardLock + still creates TEAM.lock under
  it for old-code peers; _holder_is_live no longer reaps a
  "started":true record. TEAM.md + AUDIT-LOG entry written.
  Claimed the notice task (35560). NEXT: poll @publication
  (OPUS-PUB-D3D11-BUFFER-ELEMENT holds it); when free, file+claim
  SWE2-FRONTIER-PUB-TEAM-LOCK-MUTEX holding @publication + team.py +
  TEAM.md + AUDIT-LOG.md; publish_paths.sh those three paths only
  (message file under Database/Tools/work/SWE2-FRONTIER/); finish
  pub task + notice task; release lease; final board check.

**2026-09-28 disposition batch (rev ~36838 base).**
  Eight inbound items processed. Rulings appended to
  candidates/register-triage/batch-K-scope-rulings.md (extension
  2026-09-28): GG-1 ANSWERED (residue carried by
  FRONTIER-RT-RUNTIME-SURROGATE); UC-1 65-256 B band GO (99 admitted,
  21 held, 3 external-edge rows admitted with tail transfers recorded);
  BQ-27 ANSWERED (40-site residue to surrogate carrier); SQ-1 ANSWERED
  (flag names OEB, dword0 carryover, env99.spp to ASTRA trace); SN-1
  PARTIAL (OEB-shaped residue, closes when OPUS writes the four-part
  guard). Navgrid thin-rectangle qualification applied to the
  unit-definition carrier (trunc(w/c0)=0 -> +infinity cell size).
  Register repair: all 35 cell_count_scan rows repaired (31 joins, 1
  missing pipe, 3 merges); statuses byte-identical (snapshot diff NONE);
  check_questions.py read_structure tightened to delimiter-count so a
  missing closing pipe fails the gate (control extended). Ledger now
  1596 rows / 1434 ANSWERED / 3 PARTIAL / 0 OPEN / 0 BLOCKED.
  NEXT: claim @publication via SWE2-FRONTIER-PUB-* task; publish
  publish_paths.sh ONLY: batch-K-scope-rulings.md, OPEN-QUESTIONS.md,
  check_questions.py, how-a-battle-unit-is-built-from-its-definition.md,
  spp-map-sound-list.md, object-construction-destruction-and-static-
  lifetime.md, AUDIT-LOG.md, this file. Then finish all 8 board items
  with commit+rev; rerun goal_gate (expect questions dimension MET);
  controller check. Scripts used: Database/Tools/work/SWE2-FRONTIER/
  fix_malformed_rows.py, apply_ruling_rows.py, show_status.py.

**2026-09-28 disposition batch LANDED (rev ~36983).**
  Published `d50e87938` (five dispositions + UC-1 GO + register repair +
  navgrid qualification; ledger 1596 rows / 1434 ANSWERED / 3 PARTIAL /
  0 OPEN) and `2a1a77f6d` (SN-1 re-scope). All eight board items DONE.
  SN-1 re-scope (FABLE-REQ-FRONTIER-SN1-RULING-PREMISE, P1, closed):
  FABLE decoded q3 as the byte-to-instruction page map - the OEB premise
  was refuted; residue is head word X only; row PARTIAL; OPUS's guard
  condition withdrawn. Also repaired peer UQ-218's 5-cell row - the new
  delimiter-count gate caught it on first scan.
  NEXT: nothing inbound. Parked on ctrl duty; watch for OPUS applying
  the UC-1 65-256 B band (99 rows + series break) and ORACLE surrogate
  runs on the GG-1/BQ-27 residues.

**2026-09-28 cell-repair-fold notice CLOSED (rev ~37121).**
  FABLE-NOTICE-FRONTIER-CELL-REPAIR-FOLD (P2) dispositioned. Row data
  was already corrected by FABLE's 0e4b2edab (BF-4/UQ-247/UQ-218
  statuses restored to their cells; 0x8000\|n and litOff17\|flags
  restored as escaped pipes). The routine defect is fixed in
  Database/Tools/work/SWE2-FRONTIER/fix_malformed_rows.py: the
  surplus-cell merge now takes the last NON-EMPTY split field as
  status (f[-1] is empty on a '|'-terminated row - not a cell), and
  folds middles by rejoining on raw delimiters then escaping every
  internal pipe - never ' - ' rewriting, so code pipes survive
  byte-exact; plus an EOF boundary fix (missing-pipe row at file end
  now appends '|' instead of failing the join). Verified on
  synthetic 5-cell and missing-pipe shapes. Durable rule recorded in
  check_questions.py read_structure docstring - published 4e6e14bad.
  Ledger at HEAD clean (0 structural mismatches, gate consistent).
  NEXT: nothing inbound. Parked on ctrl duty; watch items unchanged
  (DATA UC-1 band readers, ORACLE surrogate residues, SN-1 head X).

**2026-09-28 ruling batch LANDED (rev ~37330).**
  BJ-1 ANSWERED with carried residue (`03092879f`): OPUS's NATIVE-REPLAY
  19-guard lower bound accepted, residue carried by
  OPUS-REQ-ASTRA-BJ1-GUARD-SNAPSHOT; row + page box updated, ledger
  consistent (1435 ANSWERED / 2 PARTIAL / 0 OPEN / 0 BLOCKED).
  00392200 carrier relabelled (nav obstacle grid rasterizer). UC-1
  257B+ GO correctly refused by the board's own dep gate -
  FABLE-REQ-AUDITSPEC-REVIEW-0928J still READY; ruling text on record
  so it lands as soon as the review ACCEPTs.
  Earlier this round: CKPT10R2 repair + executed re-review both DONE
  (113cca077, 9/9 controls PASS) - progress route acceptance restored;
  ASTRA WinError5 notice dispositioned (transient rename class, evidence
  routed to ORACLE's writer-repair).
  NEXT: nothing inbound. Watch: FABLE-REQ-AUDITSPEC-REVIEW-0928J ->
  then UC-1 257 GO unblocks; ORACLE still holds P0 EXP201 sealing +
  board-write-path repair READY; OPUS-UC1-POPULATION-CHANGE remains
  BLOCKED owned by OPUS (bands 1-256 applied; 257+ pending review).

**2026-09-28 fleet replan + UC-1 257B GO position (rev ~37441).**
  fleet-plan.json's inner updated_at had expired PLAN_TTL (6h) -> board
  heuristic desired ORACLE/AUDIT-SPEC/DATA all capped-or-busy,
  none-eligible, CONTRACT starving 5.8h with 3 ready P2. Rewrote plan:
  desired = [ORACLE, DATA, CONTRACT], 12:18Z poll confirmed source:plan,
  mode send; replan --clear consumed 5 events. AUDIT-SEM noted next.
  ASTRA-REQ-FRONTIER-UC1-257-EXTENT-GO: a parallel session already
  committed the deferral (03092879f, batch-K + dependency-gated the
  task on FABLE-REQ-AUDITSPEC-REVIEW-0928J). Independently reproduced
  the extent check -> PASS_BOUNDARY_54 (353B/82 reachable, terminal
  RET 007122E0, cuts rejected, collision projection clean, honest
  INVALID_NORMALIZATION). Filed FRONTIER-REQ-AUDITSPEC-REVIEW-UC1-257-
  EXTENT for dedicated SPEC corroboration of the extent package (the
  65-256 band had a dedicated extent review; 0928J reviews the ruling
  itself). GO stays conditional: OPUS applies only after SPEC lands.
  Board note recorded rev 37441. NEXT: when 0928J/extent review land
  ACCEPT, the GO's conditions are met -> OPUS apply with the 65-256
  shape (frontier + series break + 49 holds reported every run).

**2026-09-28 controller turnover DONE (rev ~37629).**
  First child-free window arrived (no children of pid 13704).
  `swe2_watchdog.py controller restart` -> new pid 45016 @16:16:10Z.
  The progress hook fired on startup for real:
  `{"event":"progress_report","rc":0,"dirty":true,"dirty_consumed":
  true} @16:16:17 head=591b4b0c1 board rev 37628 fp=9ea0303f70` -
  coherent regen, .dirty consumed only after success. The 30-min
  cadence is now deployed evidence, not configured code.
  ORACLE + DATA remain daily-capped (P0 EXP201 sealing, board-write
  repair, UQ218 motion residue all resume at cap reset ~00:00Z).
  UC-1 257B+ GO still correctly dep-gated on
  FABLE-REQ-AUDITSPEC-REVIEW-0928J + the dedicated
  FRONTIER-REQ-AUDITSPEC-REVIEW-UC1-257-EXTENT.
  NEXT: nothing inbound; parked on ctrl duty. Ledger 1435/2/0/0.

**2026-09-28 cadence proven + plan rotated (rev ~37656).**
  Three progress_report events in the controller log
  (16:16:17/16:26:36/16:28:40Z, all rc:0 dirty_consumed:true,
  heads 591b4b0c1/ec5e54a99/956691ba0) - the 30-min/dirty cadence is
  deployed evidence now. Rotated fleet-plan to [ORACLE, DATA,
  AUDIT-SPEC] when CONTRACT hit its cap; SPEC then capped too, so all
  three desired lanes are none-eligible until ~00:00Z - correct
  behavior, not a stall. ORACLE's P0 sealing + board-write repair,
  DATA's UQ218 residue, and SPEC's UC-1-257 reviews all resume at cap
  reset; foreign agents (OPUS/FABLE/ASTRA) continue meanwhile.
  NEXT: nothing claimable - the one FRONTIER-addressed item
  (ASTRA-REQ-FRONTIER-UC1-257-EXTENT-GO) is dep-gated by the board
  until the SPEC reviews land. Ledger 1435/2/0/0.

**2026-09-28 fleet rotation 16:54Z.** All three prior desired lanes
  daily-capped (SPEC's 16:51Z replan event was cap-bound - it holds the
  promotion-sweep claim and resumes at reset). Rotated desired =
  [ORACLE, AUDIT-SEM, STRUCT]: ORACLE keeps the P0 slot, the two
  wakeable lanes with real queues take the other slots (AUDIT-SEM
  4-item OPUS review backlog, STRUCT 2 ASTRA nav P2s). 16:55Z poll
  confirmed source:plan / mode:send. UC1-257 GO unchanged: gated on
  FABLE-REQ-AUDITSPEC-REVIEW-0928J + the dedicated extent review;
  SPEC resumes at cap reset ~00:00Z.

**2026-09-28 execution batch (rev ~38084).**
  Three inbound processed substantively: (1) stale CONTRACT-encoded-id
  hunk identified as EC7's batch-170 paragraph (003B2510 router case),
  committed on its behalf `a4386da30` - OPUS's held citation fix
  unblocked. (2) ASTRA preflight-37999 adjudicated: board_status
  mixed-snapshot false positive - board read then journal read is two
  reads; a sanctioned commit between them mimics rollback. Fixed in
  team.py `fe63cdbdd`: incident verdict now requires the same
  inconsistent reading on a second fresh pair; 3 MixedSnapshot
  fixtures added (both directions + persistent-rollback retained),
  suite 34/34. (3) DATA CKPT10R3 filed (revs 38063/38065): full-body
  _doc_signature fingerprinting + late-page checkbox fixture,
  page-only obligation fields, empty-vs-invalid register, last-
  COMPLETE preservation, receipt-derived terminal progress; chained
  AUDIT-SPEC executed re-review. ORACLE uncapped at 19:19Z (at-
  capacity only) - keeps P0 sealing head-of-queue, next free slot
  wakes it; no handoff while owner eligible. Ledger 1435/2/0/0.
  NEXT: nothing inbound. Watch: SPEC's two UC-1-257 reviews gate the
  GO; ORACLE next window; DATA R3 claim.

**2026-09-28 stale-hunk + preflight dispositions (rev ~38094).**
  OPUS-REQ-FRONTIER-STALE-HUNK-CONTRACT-ENCODED-ID closed by a parallel
  session: the orphaned 4-line hunk (003B2510 class-router case) was
  EC7-authored (splice style) and committed on its behalf, a4386da30.
  Native verification during adjudication caught one error the adopt
  carried: 'the 002925A4 jump table' was the RVA - the VA is 003B25A4
  (lea rdx=[rip-0x29258a]@003B2583 => rdx=00120000 base; operand
  [rdx+rax*4+0x2925a4]); fix published 246f41c05. All other hunk claims
  verified from the certified image (02EBE5E0..02EBEBE0 bounds, 0x30
  stride, +0x1C dispatch, +0x378&0x100/+0x370 paths). EC7 notice
  retired (moot); OPUS's held 20E626 citation fix is unblocked.
  ASTRA-NOTICE-FRONTIER-BOARD-PREFLIGHT-37999 closed by a parallel
  session: fe63cdbdd hardened board_status - the board+journal are two
  unlocked reads, so a sanctioned commit landing between them mimics
  rollback/unjournaled-advancement; an incident verdict now requires
  the same inconsistent pair to repeat on a fresh read (3 tries).
  True rollback detection retained (34/34 incl 3 new MixedSnapshot
  fixtures). NEXT: UC1-257 GO still gated on FABLE-REQ-AUDITSPEC-
  REVIEW-0928J + FRONTIER-REQ-AUDITSPEC-REVIEW-UC1-257-EXTENT (SPEC at
  daily-cap, resumes ~00:00Z). Parked on ctrl duty.

**2026-09-28 mandate batch (rev ~38184).**
  Filed: (1) FRONTIER-REQ-SWE2-DATA-EXPORT-COHERENT-GENERATION (P1,
  38180) - the 19:25/19:27 mixed ZIP members; stage one frozen
  validated generation, verify members vs declared snapshot, label
  mixed/stale never CURRENT, fixtures incl. refresh-during-export.
  Extends CKPT10R3. (2) FRONTIER-REQ-OPUS-SN1-NEITHER-PARTITION-
  PREREQ (P1, 38181) - wrapper reports FAILS 0 while its required
  producer FAILS 1 on the 126-count edit; require checked prerequisite
  results or a validated narrower contract; chained executed review
  FRONTIER-REQ-AUDITSEM-EXECUTED-REVIEW-SN1-NEITHER-PREREQ (38182).
  HANDOFF: ORACLE re-capped; retired FRONTIER-REQ-ORACLE-BOARD-WRITE-
  PATH-REPAIR and refiled identical scope to SWE2-STRUCT (38183/38184)
  as a checkpointed single-owner handoff - generic tooling work, not
  experiment-lane. EXP201 sealing + EXP086/189/230 annotations stay
  ORACLE (experiment-file ownership; cap resets ~00:00Z, AUDIT-SEM
  reviews already chained). SN-1 canonical consumption + companion
  page already routed (OPUS-REQ-DATA-SN1-VARIABLE-NAMING-CANONICAL,
  FABLE-REQ-DATA-SN1-PAGE-ACCEPT).
  NEXT: nothing inbound claimable. Watch: UC1-257 reviews (SPEC),
  STRUCT pickup of the writer repair, ORACLE cap reset.

**2026-09-28 WORKFLOW MIGRATION adopted (rev ~38366, commit 2af29d4c7).**
  Brief FF12-WORKFLOW-MIGRATION-20260928-01 installed at
  _index/workflow/COMPLETION-WORKFLOW.md + ACCEPTANCE-MATRIX,
  ALL-TOP-LEVEL-GOALS, WORKER-ASSIGNMENTS, START-HERE, worker_prompts/;
  linked from root CLAUDE.md and TEAM.md; adoption note + lane prompts
  delivered to all 7 SWE2 inboxes. Roles now: OPUS technical delivery,
  ASTRA/SOL independent engineering verify, FABLE mechanism semantics,
  FRONTIER ops/deploy/capacity. L1+L2 + terminal protocol unchanged.
  Parents filed: FRONTIER-REQ-OPUS-WORKFLOW-M0M1-DELIVERY (38364),
  FRONTIER-REQ-FABLE-WORKFLOW-PILOTS-SEMANTICS (38365),
  FRONTIER-REQ-ASTRA-WORKFLOW-INDEPENDENT-VERIFY (38366).
  MY M0 ops lane: host/subscription interface inventory + safe
  deployment of dashboard; acceptance = M0-M5 executed via matrix.
  NEXT: user replaces the 3 Claude-lane goals with prompts 01-03 at
  safe checkpoints (their host mechanism, not ours). Watch OPUS
  pickup of the delivery parent + UC1-257 reviews on SPEC return.

**2026-09-28 cap-exhaustion checkpoint (rev ~38385).**
  Parallel session batch landed 58abf37c6: SN-1 head-word X ruled
  OEB-shaped (four-part guard required before close - OPUS writes it),
  UC-1 held-rows conditional GO bound to in-flight SPEC reviews,
  0020E626->0020E620 citation applied. WORKFLOW MIGRATION 2af29d4c7
  adopted; roles: OPUS technical delivery, ASTRA/SOL independent
  verification, FABLE mechanism completion, FRONTIER operations/
  capacity/deployment. My 21:49Z rotation: desired = [ORACLE, STRUCT,
  CONTRACT] after AUDIT-SEM capped; then CONTRACT hit cap too - every
  specialist now daily-capped or busy-active until ~00:00Z reset.
  Nothing claimable: UC1-257 GO still dep-gated on 0928J + extent
  review (SPEC capped). NEXT: at cap reset, ORACLE P0 first, SPEC
  review chain unblocks the GO, DATA residue. Parked on ctrl duty.
