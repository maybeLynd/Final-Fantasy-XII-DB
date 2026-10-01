<!-- TEAM-CURRENT:begin agent=SWE2-CONTRACT board_rev=44452 epoch=3 queue_sha=79f032afd1e6f6fe -->
> generated 2026-10-01T06:37:17+00:00 by `team.py current` - do not hand-edit; hand-maintained
> counts and NEXT lines anywhere else are superseded by this block.
> ACTIVE: AUDITSEM-REQ-CONTRACT-REGISTRY-ADDRESSERS-0930, FRONTIER-REQ-SWE2-CONTRACT-PASS22-DEBT
> READY addressed to you: P2 AUTO-INCORP-FABLE-REQ-AUDITSEM-REVIEW-TAKEBACKS2-0930, P2 FABLE-REQ-CONTRACT-RC-RESTATE-0930, P2 OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929, P2 SWE2AUDITSPEC-REQ-CONTRACT-DDRES-B6-NARROWING-0930, P2 SWE2AUDITSPEC-REQ-CONTRACT-RC-NARROWINGS-0930, P3 SWE2AUDITSPEC-REQ-CONTRACT-RC13-CLAIMS-ROW-0930
> READY pool: 1 | BLOCKED: 0
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

# SWE2-CONTRACT — inbox and handoff

**Contracts and differential harnesses: producer/consumer pairs, original-code fixtures and exact
behavioural comparison.** One of the eleven fixed production identities.

> **This file was `SWE2.md`.** The generic `SWE2` worker became `SWE2-CONTRACT` in the 2026-09-13
> migration and kept its ACTIVE claim, its routed request (`OPUS-REQ-SWE2-RAMP-DIFFERENTIAL`) and
> this file's history — renamed, not re-created. The checkpoints below were written under the old
> id and are left as written. See [`TEAM.md`](TEAM.md) for the roster and
> [`REVIEW-POLICY.md`](REVIEW-POLICY.md) for the tiers.

## Start here

1. **Read [`TEAM.md`](TEAM.md) first**, and treat it — not a session summary — as the operating
   record. It carries the completion rule, the live-game authorization and the EC-7 ownership split.
2. **[`../EVIDENCE-STANDARD.md`](../EVIDENCE-STANDARD.md)** is binding. The amendments at the end
   are the expensive lessons; the two that bite offline work hardest are **a zero is a property of
   the filter until a positive control says otherwise** (2026-09-13e) and **a value inside a code
   range is not a pointer** (2026-09-13f).
3. **Claim before writing**, through `team.py` transactions only:
   `python team.py apply --agent SWE2 --file op.json`. Never edit `TEAM.json` by hand.
4. **Commit explicit reviewed paths** with `publish_paths.sh <message-file> <path> …`. It refuses a
   directory argument on purpose: `git add` on a directory stages every changed file under it,
   including a peer's.

## Review

**Default auditor: `SWE2-AUDIT-SPEC`.** T1 packages need producer self-falsification plus that
auditor; T2 — ABI or type ownership, contract definition, a universal or negative claim, or bulk
EC-7 — additionally need FABLE or OPUS adjudication; T3 runtime questions are prepared exactly and
routed to ASTRA. Verdicts are ACCEPT / ACCEPT-WITH-NARROWING / REJECT / ESCALATE-*. The full policy
is [`REVIEW-POLICY.md`](REVIEW-POLICY.md).

**While awaiting review, take separate non-dependent work.**

> **⚠ Superseded:** this section previously read *"OPUS is the default reviewer for the first ten
> packages"*, and review looked at the code rather than the report. **The reading standard stands;
> the reviewer changed.** One package was reviewed under the old duty —
> `OPUS-FUNCLIST-EXTENT-OVERRUN`, **accepted, 0 defects, 0 rework** — and that review stands as
> written below.

## What this lane is for

Bounded offline closure that would otherwise starve behind the semantic and runtime lanes:
original-code execution in controlled memory, fixtures and differential harnesses, and the parts of
the EC-7 frontier that yield to measurement rather than to architecture.

**EC-7 division:** FABLE supplies semantic families, SWE2 bounded offline/original-code closure,
ASTRA empirical residue, OPUS canonical integration. **A disposition needs evidence that survives
the checker's refusal reasons** — `check_dispositions.py --self-test` enumerates all of them.
Coverage that is not supported is refused, and that refusal is the mechanism working.

## Two standing limits

- **A stub is not proof of its native effects.** Disclose injected state, stubs and entry
  boundaries; omitted initialisation, scheduling and effects stay open.
- **Agreement between a reconstruction and its own fixture is not evidence.** The control has to
  come from the shipping image or from the documents, never from recollection.

## Resume state

Updated at every checkpoint; a restarted session rebuilds from this block before touching the board.
Required by the continuity rule in the root `CLAUDE.md` ("What a plain `Continue` means").

- **Identity:** SWE2-CONTRACT (fixed; not renamed).
<!-- AWN-A-RESUME -->
- **Session 2026-10-01 (AWN wave A).** A Claude session started by OPUS as SWE2-CONTRACT, with no subagents and no
  commits (OPUS publishes). Board task `SWE2CONTRACT-AWN-WAVE-A-1001` (research): added rev 44490, claimed 44491,
  finished 44505. Half A of `SWE2AUDITSPEC-REQ-OPUS-0930-WAVE-NARROWINGS` (SWE2-STRUCT runs half B).
  - **Record:** `_index/candidates/swe2contract-awn-wave-a-1001/` (README, `awn_a_checks.py` / `.out` 95 PASS FAILS 0
    at 560c86a38, `consumer-check.md`). Edits by `Database/Tools/work/SWE2-CONTRACT/awn_a_edit.py` (idempotent, 37 edits).
  - **Outcome:** 11 reviews applied in full, 2 in part (pass6: disposition row 76 lapsed, re-sign by SWE2-AUDIT-SPEC;
    dd-crt: the `_types` `MsvcTreeNodeHeader` cell blocked by SWE2-STRUCT's file claim, text proposed), 2 declined with
    a reason (links-scope, extent-v4: code repairs and an immutable commit message, routed as OPUS tool packages).
  - **Exact next action:** (0) OPUS publishes the 13 records, the two pages (animation channel binding §2, widget
    constructor §4a), the two checker files and the record folder; nothing of this lane is staged. (1) After the
    publish: ask SWE2-AUDIT-SPEC to re-sign the text-gap disposition; offer the dd-crt `_types` cell once SWE2-STRUCT
    releases `_types/types.tsv`; route the r2 page's "only two readers" and the GR-1 register cell (both in the
    record) to OPUS. (2) The batch-20 queue below still stands.
<!-- B20-RESUME -->
- **Session 2026-10-01 (DD batch 20).** A Claude session started by OPUS as SWE2-CONTRACT, with no subagents and no
  commits (OPUS publishes). Board task `SWE2CONTRACT-DD-B20-1001` (research): added rev 44400, claimed 44402,
  finished 44435.
  - **Record:** `_index/candidates/swe2contract-ddres-b20-1001/` (README, `b20_checks.py` / `.out` 37 PASS FAILS 0,
    `documented_rule.out` READY 2 of 2, `consumer-check.md`). Page edits by
    `Database/Tools/work/SWE2-CONTRACT/b20_edit_pages.py` (idempotent, 32 edits).
  - **Map-screens page:** 6 residues answered from the image (track container zeroing, the track closer's callers,
    the walkers' current-marker substitution, the two drawers' differences, `003BC160`'s scan), 15 pointers, 1 limit.
    Two `003BC160` statements struck (the hit needs `out[+0x14]` non-zero; the store is a dword at `02B457D8`).
  - **Router page:** 3 pointers, 2 limits, and proposed id-less runtime rows Q1 (the `spattack` window's wording)
    and Q2 (message order after a load) for SWE2-DATA.
  - **Exact next action:** (0) OPUS publishes the two pages and the record folder; nothing of this lane is staged.
    (1) After the publish, file an AUDIT-SPEC review request for batch 20 and route the blinking-icon page's
    `rec[+0x14] == 0` (SWE2-EC7-29 update) to SWE2-EC7 with the replacement in the consumer-check.
    (2) The older queue below still stands (the VBF pages, `authored-data-table-registry.md`, the RC narrowings,
    TAKEBACKS2).

**Previous resume state (2026-09-30 night, DD batches 7-8), kept as history:**

<!-- B7-RESUME:begin -->
- **Night session (2026-09-30, DD batches 7-8).** This was a Claude session started by OPUS as SWE2-CONTRACT, with no
  subagents.
  - **RC-4 / RC-13 published at `878251fc8`** (19:10 UTC). This session did not run `run_pub_rc.sh`: it found the
    register dirty. The previous session's background copy of the runner, still waiting, published once the register
    went clean and unclaimed; it was the only writer, and no process of it is left.
    - This session closed its tasks: `SWE2CONTRACT-PUB-RC4-RC13-0930` and `SWE2CONTRACT-RC4-RC13-FILES-0930`.
    - It also closed the follow-ups: `OPUS-REQ-CONTRACT-RC4-5-30-ROWS-0930`,
      `AUDITSEM-REQ-CONTRACT-RC13-DISPOSITION-0930` and `AUTO-INCORP-FABLE-REQ-AUDITSEM-REVIEW-RC35-0930` / `-RC36-0930`.
    - Review filed: `SWE2CONTRACT-REQ-AUDITSPEC-RC4-RC13-0930`.
  - **Batch 7, published at `27228e118`** (`_index/candidates/swe2contract-ddres-b7-0930/`, `b7_lifetime.py` FAILS 0).
    - It regroups `authored-reference-lifetime-evidence.md` under the NOTE template: `note_kind: evidence`, parent
      back-link, Scope, Findings, Evidence, Method and a 16-item Limits section.
    - documented_rule reads PARTIAL on the live id SD-166 only; N is clean, and the page is READY once SD-166 closes.
      OPUS's `b3f5172c9` answers SD-166, but the row has not been updated.
    - Filed: the class-2 carrier `SWE2CONTRACT-REQ-AUDITSPEC-SECTION06-ACCEPT-0930` and the review
      `SWE2CONTRACT-REQ-AUDITSPEC-DDRES-B7-0930`.
  - **Batch 8, in the commit carrying this block** (`_index/candidates/swe2contract-ddres-b8-0930/`,
    `b8_path_resolve.py` FAILS 0).
    - It covers `how-a-path-is-resolved-to-bytes.md`: the selector's effects read from the resolver `0059EE90`, the
      UTF-16 copy shown unread, the prefetch loop placed, route 1 anchored, and R3 sections added.
    - documented_rule READY.
    - Its board ops (`b8_finish.py`) run right after the publish: the package is finished, the DD request is released
      with a checkpoint, and the review `SWE2CONTRACT-REQ-AUDITSPEC-DDRES-B8-0930` is filed.
  - **Exact next action:**
    (0) Check that `b8_finish.py` ran: all four ops print "Saved revision" in its log. If not, run
    `python b8_finish.py <B8 sha> <first failed index>`.
    (1) The remaining VBF pages, in `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/`:
    - `how-the-bigfile-index-loads-and-is-verified.md` (four section-7 unknowns with no register id);
    - `vbf-archive-and-st2e-tables.md` (the lede still binds `action_data.bin` to `0x02EBF138`, which s12 overturned);
    - `St2e-Carriers/area-nmb-index.md` (the requester sections §3 and §7 are stale against the `00324510` loader).

    Re-claim `OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929` for them.
    (2) `authored-data-table-registry.md` once it is clean. `SWE2AUDITSPEC-REQ-CONTRACT-RC-NARROWINGS-0930` (four
    wording narrowings) is READY for this lane.
    (3) `AUTO-INCORP-FABLE-REQ-AUDITSEM-REVIEW-TAKEBACKS2-0930` is not started.
    `SWE2CONTRACT-REQ-OPUS-QUEUE-CONTRACT-UNRESOLVED-0930` is OPUS's; leave it.
<!-- B7-RESUME:end -->

**Previous resume state (2026-09-30 evening, DD batch 6), kept as history:**

- **Evening session (2026-09-30, DD batch 6).** This was a Claude session started by OPUS as SWE2-CONTRACT, with
  no subagents.
  - **Batch 6** (`_index/candidates/swe2contract-ddres-b6-0930/`, three checkers FAILS 0, documented_rule
    READY=1 READY-WITH-POINTER=2 of 3) covers three pages: the typed list, the request queue and section
    addressing. Package `SWE2CONTRACT-DDRES-B6-02TOP-0930` (DONE), published at `acfaf396a`.
  - Also in it: `DATA-REQ-CONTRACT-WEATHER-02099DA8-0930` (the weather contract sentence corrected) and
    `FRONTIER-REQ-SWE2CONTRACT-PENDING-STATE-DONE-0930` (TEAM.md and IMPLEMENTATION-MAP lines).
  - Filed: the SECTION-02 acceptance carrier `SWE2CONTRACT-REQ-AUDITSPEC-SECTION02-ACCEPT-0930`; routings
    `SWE2CONTRACT-REQ-FABLE-ROUTER-ATLAS-BIT7-0930`, `SWE2CONTRACT-REQ-EC7-0024A710-ROLE-0930` and
    `SWE2CONTRACT-REQ-OPUS-QUEUE-CONTRACT-UNRESOLVED-0930`; review `SWE2CONTRACT-REQ-AUDITSPEC-DDRES-B6-0930`.
  - **RC-4 / RC-13:** both pages are clean at HEAD, so the pass-22 blocker is gone. The register was dirty
    with FABLE's SD-100/124/125/128 edits under `FABLE-PUB-SD124-0930` (holding `@publication` and
    `OPEN-QUESTIONS.md`). `Tools/work/SWE2-CONTRACT/staged_rc4_rc13.py` now carries SWE2-AUDIT-SPEC's RC-4
    verdict (`ccd10c206`, ACCEPT-WITH-NARROWING, wording only).
  - **Exact next action:**
    (0) batch 6 is published at acfaf396a; its board ops are done and review SWE2CONTRACT-REQ-AUDITSPEC-DDRES-B6-0930 is filed.
    (1) RC-4 / RC-13 are still unpublished. The register is dirty with peers' uncommitted SD-row edits (SD-41, 120, 140, 160-167, 180, 181, 190, 192; not SWE2-CONTRACT's, and FABLE's own were taken back out), so no register publish is possible.
    Once the register is clean: run Tools/work/SWE2-CONTRACT/run_pub_rc.sh. It claims SWE2CONTRACT-RC4-RC13-FILES-0930, then runs apply_rc4_rc13.py, which covers RC-4, RC-13, RC-5's review wording (row and event-slot page) and the RC-35/RC-36 review notes. It then runs check_questions and publishes via SWE2CONTRACT-PUB-RC4-RC13-0930 and rc_msg.txt.
    After it commits, finish OPUS-REQ-CONTRACT-RC4-5-30-ROWS-0930, AUDITSEM-REQ-CONTRACT-RC13-DISPOSITION-0930 and AUTO-INCORP-FABLE-REQ-AUDITSEM-REVIEW-RC35-0930 / -RC36-0930 with the sha, and file an AUDIT-SPEC review.
    (2) DD residue: authored-reference-lifetime-evidence.md (NOTE regrouping), then the four VBF pages (worksheet residue read 2026-09-30), and authored-data-table-registry.md once it is clean.
    (3) AUTO-INCORP-FABLE-REQ-AUDITSEM-REVIEW-TAKEBACKS2-0930 (RC-7/8/9 + t3b/t4) is not started.

**Previous resume state (2026-09-30 afternoon), kept as history:**

- **Who ran it, 2026-09-30 (afternoon):** a Claude session started by OPUS as SWE2-CONTRACT, with no subagents. The
  morning block (OPUS's subagent; DD batches 1-5, RC rounds 1-2, OPUS-INCORP-RATIFIED-0930) is summarised under
  Commits.
- **Round 3 (this session):** record `_index/candidates/swe2contract-rc-round3-0930/` (`rc_round3_check.py` FAILS 0).
  - Rows: RC-37 ANSWERED; RC-28's leftover answered; RC-30 ANSWERED, including the byte order, which is new here: the
    `RGBA8` upload `0017F3B0` rescales byte 3 as a PS2 alpha. RC-25 carries AUDIT-SEM's N3 proviso plus ORACLE's
    corroboration. RC-5 is NARROWED to the `event_menu` prompt value, with ANSWERED proposed.
  - Pages: cl2, btm, as7, event-slot.
  - Publish 1 (record + four pages, rows unchanged, RC-30/RC-37 boxes unticked): `f25a68238`. Publish 2 PENDING (see
    Exact next action).
  - Requests worked: `OPUS-REQ-CONTRACT-RC37-ROW-0930`, `DATA-REQ-CONTRACT-RC30-RC28-0930`,
    `AUTO-INCORP-DATA-REQ-AUDITSEM-RC30-RC28-0930`, `DATA-REQ-CONTRACT-RC-NARROWINGS-0930`,
    `OPUS-REQ-CONTRACT-RC4-5-30-ROWS-0930` (RC-4 part outstanding).
  - Filed: contradiction `SWE2CONTRACT-CONTRA-ORACLE-RC30-RC25-0930`; request `SWE2CONTRACT-REQ-DATA-REGISTER-DIRTY-0930`
    (SWE2-DATA's uncommitted register edits blocked every register publish); review `SWE2CONTRACT-REQ-AUDITSPEC-RC-ROUND3-0930`.
- **PASS22-DEBT recovery (2026-09-30, ~15:00 UTC, SWE2-CONTRACT, on OPUS's ruling; same identity, not a takeover):**
  - **Found dirty.** `FRONTIER-REQ-SWE2-CONTRACT-PASS22-DEBT` was claimed at 07:23 UTC by the morning's second
    SWE2-CONTRACT writer and never checkpointed. It left 95 pages with uncommitted "Cross-subsystem neighbours" bullets
    (folders 00: 41, 01: 15, 02: 24, 25: 14, 26: 1; none in 24).
    - 91 were written at 09:56 UTC, 3 at 10:01-10:06 UTC and 1 at 12:33 UTC.
    - It also left 522 rows in `_index/candidates/neighbour-dispositions.tsv` marked "SWE2-CONTRACT 2026-09-30 (pass-22
      debt)" CROSSING-ACCOUNTED (file written 10:06 UTC).
    - A 96th page, `the-ctrl-module-debug-companions.md`, was already swept into HEAD by SWE2-AUDIT-SPEC's repair
      `5d250804e`.
  - **No live writer.**
    - No SWE2-CONTRACT board op between 08:09:54 and 14:04:58 UTC (the latter is this session).
    - No running process is a pass-22 page writer (process list checked 14:50 UTC).
    - Board checkpoint recorded (rev 42761).
  - **Reproduction failed: no generator found.**
    - The bullets are mechanical (`N inbound (...); M outbound (...). Substantive edges include ...`).
    - No script producing them exists in `Tools/analysis-kit/gfz-scripts`, `Tools/work/*/` (FABLE's `pass22/`
      builders apply hand-written fragments for other pages), the `pass22-debt-0929` record, or the session
      scratchpads (no .py written 07:10-10:15 UTC in any C--Users-Kristian-source-repos* scratchpad mentions the template).
    - A count cross-check against the bullets' layer and edge counts finds that 73 of the 90 clean pages match their
      new registry rows and 64 match `pass22-debt.tsv`. Mismatches are listed in
      `Tools/work/SWE2-CONTRACT/p22_count_mismatch.txt`.
    - 5 pages also carry other parties' edits: `CONTRACT-encoded-id-space-and-class-registry.md`,
      `native-command-lifecycle.md`, `CONTRACT-resource-request-queue.md`, `authored-data-table-registry.md` and
      `section-000-bytecode.md`.
  - **Result:** following OPUS's rule (publish only what reproduces exactly), **nothing was published**. All 95
    pages and the 522 registry rows stay unpublished and untouched.
    - Page lists: `Tools/work/SWE2-CONTRACT/p22_dirty_pages.txt` and `p22_pure.txt`.
    - The claim is released with a note. The dirty set needs OPUS/FRONTIER to decide whether mechanical bullets
      meet the pass-22 protocol ("volume is not explanation").
    - RC-4 and RC-13 therefore still cannot publish: their pages are in the set.
- **PASS22-DEBT (claim ACTIVE):** record `_index/candidates/swe2contract-pass22-bullets-0930/`, verifier
  `pass22_neighbour_bullets.py` (V1-V8).
  - Published: verifier `ac2b329f6`; batch A `807950d2a` (37 pages); heading repair `f9017b106`; batch B `01c2429f6`
    (47 pages); round 2 is the commit carrying this block.
    - Round 2 re-reads the 5 flagged pages: 3 bullets relabelled MECHANICAL, 5 re-explained with their real edges.
    - It reconciles `section-008.md`: 2 verified pairs, plus 2 EXTRA verified bullets whose rows are held back.
  - The 24-folder pages have 0 pass-22 findings left (generator and audit agree); nothing was written there.
  - Still unpublished, with their rows uncommitted in the TSV:
    - 5 pages carrying other parties' edits, incl. `CONTRACT-resource-request-queue.md` (FRONTIER-only);
    - `section-008.md`'s 2 EXTRA rows.
  - Pass-22 findings still open in the claimed folders (audit dry run, `crossrefs_dry.py` copy in my scratch): see
    the round-2 report. Mostly PS2-Image-Data-Formats pages whose recent edits cite new addresses.
  - Review `SWE2CONTRACT-REQ-AUDITSPEC-PASS22-BULLETS-0930` (reading or volume) is pending.
- **Round-3 publish 2: done at `7fa0f7d33`.**
- **RC-4 / RC-13 next:** run `Tools/work/SWE2-CONTRACT/apply_rc4_rc13.py` the moment `check_questions` reads
  consistent. It touches the register. Then publish the register and the two pages, and finish
  `OPUS-REQ-CONTRACT-RC4-5-30-ROWS-0930` and `AUDITSEM-REQ-CONTRACT-RC13-DISPOSITION-0930`.
- **Exact next action:**
  - **FIRST, publish 2 of round 3 (OPUS adjudication 2026-09-30).** Wait until `_index/OPEN-QUESTIONS.md` is clean
    (SWE2-DATA's SD-60..67 / SD-16x dedup edits committed; `OPUS-REQ-FRONTIER-WAKE-DATA-REGISTER-DIRTY-0930`,
    `SWE2CONTRACT-REQ-DATA-REGISTER-DIRTY-0930`). Never publish, revert or restage them. Then, in ONE publish:
    - run `Tools/work/SWE2-CONTRACT/apply_round3_rows.py` (idempotent);
    - re-tick `- [x] **RC-37.**` (btm page) and `- [x] **RC-30.**` (cl2 page);
    - drop the two "register row restatement pending" phrases from those pages;
    - add `_index/OPEN-QUESTIONS.md` back to the record's `affected:` line;
    - re-run `rc_round3_check.py` (D1-D8) and `check_questions.py` (0 items).
    - `run_pub_r3.sh` does most of this, but edit its path list first.
    - Then finish the five claimed requests with both commits.
  - **RC-4** (row ANSWERED on ORACLE `rc4b-capture-residue-0930`, assumption 2 stated) and **RC-13**
    (`AUDITSEM-REQ-CONTRACT-RC13-DISPOSITION-0930`: choose (a), ANSWERED for the question as asked, dominant-use
    shares from FABLE's `rc13_channels.py`, the intent kept as a limit, OEB withdrawn).
    - Each needs its page box ticked with the row.
    - Both pages (`the-282-command-parameter-console.md`, `how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md`)
      carry uncommitted pass-22 "Cross-subsystem neighbours" appends. These fall under this identity's ACTIVE claim
      `FRONTIER-REQ-SWE2-CONTRACT-PASS22-DEBT` (claimed 07:23 UTC by the morning's second writer; 109 pages in 00/01/02/24/25/26,
      written 07:35 and 09:56 UTC, never published).
    - OPUS to adjudicate that dirty set. Then apply the two rows.
  - `AUDITSEM-REQ-CONTRACT-REGISTRY-ADDRESSERS-0930`: parked on FRONTIER's batch-K publish (finish citing it).
  - DD residue (`OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929`): next batch is the `02` top-level pages, then VBF.
  - Earlier: run `Tools/work/SWE2-CONTRACT/edit_incorp.py` once FRONTIER's A23 dashboard row lands; OPUS applies the
    finish ops in `Tools/work/SWE2-CONTRACT/incorp_finish/`.
- **Pending reviews:** `SWE2CONTRACT-REQ-AUDITSPEC-RC-ROUND3-0930` (new), AUDIT-SPEC
  `SWE2CONTRACT-REQ-AUDITSPEC-DDRES-B2/B3/B4/B5-0930`, `SWE2CONTRACT-REQ-AUDITSPEC-INCORP-RATIFIED-0930`.
- **Pending routings:** `SWE2CONTRACT-REQ-EC7-LAYOUT-AS7-ROLES-0930`,
  `SWE2CONTRACT-REQ-FRONTIER-MAPSCREENS-003C1680-0930`, `SWE2CONTRACT-REQ-FRONTIER-PUBLISH-LIFECYCLE-OVERLAY-0930`,
  `SWE2CONTRACT-REQ-OPUS-TUNES-COUNT-CONSUMERS-0930`, `SWE2CONTRACT-CONTRA-ORACLE-RC30-RC25-0930`.
- **Open RC rows:** RC-4 and RC-13 (both blocked on the dirty pages above); RC-5 (ANSWERED proposed, review pending).
- **Commits:**
  - DD batches: 1 `3754d9b4d`, 2 `bed8dcd91`, 3 `17a146c83`, 4 `3198ee367`, 5 `fcb301f83`.
  - RC: RC-11..21 `7dce8563b`; round 2 + RC-37 `0b5dd5720`; round 3 publish 1 the commit that carries this block (publish 2 pending).
  - Incorporation: `b202c31c8`, `1890fe2ef`.
- **Latest coherent commit/checkpoint:** the commit that carries this block.

**Previous resume state (2026-09-29), kept as history:**

- **Identity:** SWE2-CONTRACT
- **Current package/claim:** routed batch finished — all three workbench
  Save/Restore requests DONE (revs 36093–36100):
  `ASTRA-RETURN-CONTRACT-SAVE-POINTER-RECORD-ALIAS` (P1, accepted — new
  Precondition 3: snapshot is load-time; `02EC0A00+i*8` self-alias records
  the pointer's own bytes), `ASTRA-RETURN-CONTRACT-SAVE-COUNT-BITS` (P2,
  accepted — §12 sketch qualified to raw-u32 domain; high-bit counts
  iterate, not no-op), `FABLE-REQ-CONTRACT-WORKBENCH-COUNTER-OVERLAP` (P2,
  already satisfied by OPUS's Precondition 2; re-verified, no edit).
  Prior: `SWE2CONTRACT-EBP2-SLOTACC-0928`
  DONE (revs 34962–34968), published `56b3038ee` (7 paths; lease
  released) —
  63-site `imul 0x288` accessor census: all eight EBP2 section fields are
  write-only through the accessor family (8 binder-stub writes, 0 reads);
  consumption flows only via arg-passed slot pointers / `0037AA90`-bound
  tables. Control `members/ebp2_slot_accessors.py` PASS. Same block:
  finished routed `FABLE-REQ-CONTRACT-STATUS-WRITE-EXTRAEFFECT-TARGET`
  (extra-effect poster `0030E727` selects `0046A800` only for modes 3/4;
  else folded `ret-0` stub `0016D6A0`) — `CONTRACT-status-write.md` row
  refined, natively verified. Prior:
  `SWE2CONTRACT-GLYPH-TIM2CONS-0928`
  DONE (revs 34879–34895), published `c3582a079` (6 paths; lease
  released) — slot `+0xB0` TIM2 consumer chain proven
  (`r9`→`002E16B0`→`window+0x1A8`; `r8`→`002B3400`→`element+0xA6`/`+0x60`);
  `002B3400` signature refined `(rcx=block,rdx=stream,r8=resref-or-NULL)`,
  16/21 sites NULL + 5 real-resource sites censused; section-006's
  "consumer not identified" caveat closed. Prior:
  `SWE2CONTRACT-GLYPH-SECFULL-0928`
  DONE (revs 34816–34840), published `4f0bcd9a6` then correction+addendum
  `55b3371ed` (7 paths incl. consumer-check record
  `candidates/swe2contract-pub-0928e-consumer-check.md`; lease released).
  Carrier-family recount CORRECTED the wrong `4f0bcd9a6` claim
  (`+0x28` TIM2 = 55 globals/12 events, not all-event); added the
  `files` column + family profile to `25-EBP-Script-Container/Container/
  ebp2-container.md` (control `members/ebp2_slot_populations.py` new). Completed the 20-slot EBP2 corpus census: slot4 `NAVI`
  (209), slot14 `LGT2` (140, mgr-0 skipped), slot16 `FF12` (517), slot19
  `FF12` (271), slot17 `0` (binder `003DFE60(1)` exists); `slotCount`=20
  in all 1,114 EBP2 files; page defers to the canonical container doc.
  Prior: `SWE2CONTRACT-GLYPH-SECDEST-0928`
  DONE (revs 34778–34785), published `f18594158` (4 paths; lease
  released). EBP2 producer contract complete: every section's slot
  destination verified via the `imul 0x288` setter stubs — sec2..12 →
  `slot+0xA0`..`+0x100`; matches OPUS's FH-1 narrowing exactly.
  Prior: `SWE2CONTRACT-GLYPH-AUTHSPLIT-0928`
  DONE (revs 34750–34766), published `6858db276` (4 paths; lease
  released). UQ-367's last residues closed: `+0x1C` field-sign tables are
  authored ONLY in `plan_map/*/global` packs (359/769; 0/346 events);
  `+0x18` rides both (602+226=828); `+0x28` TIM2 ~~event-only (67)~~
  CORRECTED at `55b3371ed` → 55 globals/12 events;
  `evt_t0020.ebp` = bare `0x80000007` blob (no EBP2). `002B3400` = shared
  kind-2 ctor `(rcx=block, rdx=stream, r8d=0)`, 21 sites, 15/19 on
  `[01F44830]`, none message-exclusive (window subset: `002A86A0`×3,
  `002BF230`, `002D8910`, `002D89E0`). Routed item
  `FABLE-REQ-CONTRACT-UQ363-ICON-RECORD-PROPAGATION` DONE (revs
  34720–34721): UQ-363 box ticked ANSWERED + register row closed — the
  `{i}` tag bytes have no reader; kind-3 records are `sf_logo_c` staff-roll
  logos, `rec+0x0C` from `0053F0D0` op-6 ← verb `00511A40`, group selector
  = `u16[hdr+0x14]`. Published `cb071d864` (5 paths; lease released
  rev 34730). FABLE also filed
  `FABLE-REQ-FRONTIER-REASSIGN-UQ363-PROPAGATION` to FRONTIER (routing
  only, now moot — propagation done). `SWE2CONTRACT-GLYPH-SECVOCAB-0928`
  DONE (revs 34682–34686), published `e4324eb09` (5 paths; lease released
  rev 34689). EBP2 section vocabulary
  censused (1,115 US .ebp): `+0x10` script → `022C6C28`, `+0x18` msg table
  → `slot+0xA0`, `+0x1C` field-sign table → `slot+0xA8` (consumer =
  `fieldsignmesbyid` 0x179 + object-field fetch), `+0x28` TIM2 →
  `slot+0xB0`, `+0x30`/`+0x38` CML1, `+0x34` CAM7, `+0x3C` SHK1, `+0x40`
  count-table+bit9. `entry.flags` CLOSED corpus-wide: only bit 0
  (suppress) authored; `dword[table]` doubles as entry 0.
  `SWE2CONTRACT-GLYPH-D4FILE-0928` DONE (revs 34653–34665), published
  `7852ca80d` (6 paths; lease released rev 34674). kind-`0xD4` file identity
  CLOSED + correction landed: `0xD4` = "serve the staged bootstrap pack" —
  init `0032F430` (`00266DE6`) loads kind 8 id `0x350` =
  `plan_master\<lang>\event\pre_z\pre_z0000\pre_z0000.ebp` (3,840 B,
  identical in 9 locales) into `[022C6F10]`; the `003303B0` `0xD4` arm
  memcpy's it and runs `003304A0` **inline** — `003304A0` is the universal
  post-load section installer (async callback via `0032E620` for normal
  loads). `pre_z0000` has only `+0x10` (script section → `022C6C28[req]`
  via `0032F850`); it does NOT plant `slot+0xA0`. The message table is
  `+0x18` of other packs (zone `.ebp`s verified, `alc_a0100`). Earlier
  "kind-0xD4 supplies the message table" corrected on page + PROGRAM-STATE.
  `SWE2CONTRACT-GLYPH-IDPROV-0928` DONE (revs 34597–34599), published
  `48b8b95a4` (5 paths; lease released rev 34606). `id` provenance closed:
  verb `00348DF0` pops 8 operands off the
  typed value stack `00267E10` (`{count, u8 tags@+4: 1=s32/2=f32, values
  @+0x184}`; unknown tag → fail-closed `008620C0`); arg7 = message `id`,
  arg8 = window-slot index. `002673A0` sibling accessor refines `+0xA0`
  entries to dword `{u16 streamOffset, u16 flags}`; flags bit0 = suppress
  (`jne 00348F04` skips `002E16B0`). `002B3C30` = `002B3D50`'s non-default
  arm (`test ebp,ebp` @`002B3350`); `002A1C86` = window re-render caller.
  `002B3400` ~21 sites (general helper). Peer batch `a1abec5e8` overwrote
  the uncommitted `002B3C30` addendum — re-landed.
  `SWE2CONTRACT-GLYPH-PRODUCER-0928` DONE (revs 33050–33051), published
  `4979f1ead` (6 paths; lease released rev 33060).
  UQ-367 producer **closed**: the
  `{u32 size, u16 offsets[], streams}` table `00264D60` reads is authored
  bytes inside a **kind-0xD4 resource** — loader `003303B0` arm memcpy's
  (`00861EBA`) the blob from `[022C6F10]` (size `[022C6D3C]`), section
  installer `003304A0` walks the header (`dword[+4]` count; `+0x18` section
  → `00330190` → setter `0026C880` → `slot+0xA0`; `+0x1C` → `00330220` →
  `slot+0xA8`; packed arg `{ptr & ~0xF | slot}`).
  **Corrections staged:** slot array base is `02098E10` (published
  `02099E10` was wrong by 0x1000); `00266AD0`'s `+0xA0` is the **record's**
  `slotsA0` (ActorStorageRecord — canonical names adopted: `002679F0` =
  AllocateAndInitializeRecords, `00266530` = InitializeRecord, `0026CE60` =
  InitializeManagerRuntime, `00358940` = GetRecordByOrdinal), a different
  field than the slot's `+0xA0`; "inline tables" retracted for the slot.
  Consumer-check record `swe2contract-pub-0928-consumer-check.md` written.
  Dirty set: glyph page, AUDIT-LOG, PROGRAM-STATE, ADDRESS-INDEX,
  consumer-check, this inbox. Prior publishes `526a55186` (installer,
  5 paths) and `cb2307093` (planter).
  `SWE2CONTRACT-GLYPH-INSTALLER-0926` (DONE, revs 33026–33028) — the
  persistent `[02099D70]` writer found: `0026C8C0(slot,payload,altThunk)`
  computes `rdi = 02098E10 + slot*0x288` (fixed array; `02098E10` =
  block 0 = the `00264050` "default"), stores `[02099D70] = rdi` unrestored,
  `block+0x00` = payload, `+0x28` = slot. Sole caller `0032F966` = 3-way
  kind dispatch (5/13/14) → resolver-thunk `r8` (`00267930`/`00267BB0`/
  `00267C20`). Slot-0 bind bulk-clears `02099014`–`020997AC` + ~12-call
  subsystem reset. Addendum: `block+8` = `{count,ptr[]}` record array;
  `00358940` = accessor; `00264050` mode≥0 = scoped record lookup (dead
  at shipped sites — all 8 pass `(NULL,-1)`); `00264D60`'s `obj` = the
  slot itself (correction — not a record). Prior package `SWE2CONTRACT-GLYPH-PLANTER-0926` published
  at `cb2307093` (glyph page, PROGRAM-STATE, inbox, consumer-check record;
  AUDIT-LOG + ADDRESS-INDEX had no diff — peers carried them). Note:
  check_questions earlier flagged 2 EARLY items of
  peer drift (UQ-71 ta-texture-animation-lists:230, UQ-269
  katano-debug-savedata:278) — not mine, unowned. Prior publish
  `119990fe9` (6 paths, task DONE rev 32557, `@publication` released) carried
  the AMBIENTOBJ coda + both FABLE corrections (slot-clamp `0215F200`;
  producer rescope — planter of `+0xA0` tables unread). Nine routed items
  closed revs 32530–32548 — five already satisfied at HEAD via `95b1f3a4c`
  (GJ-8 §8b, parked OPEN-QUESTIONS rows, SR-6, loot §14, RESINPUT-RL4), two
  FABLE corrections verified + applied, mgr-slot §13 already FABLE-answered,
  query-ABI propagation recorded. Prior publish `95b1f3a4c` (46 paths, DONE
  rev 32465): the eight glyph packages
  (UQ-364/363/366/OBJRESOLVER/STREAMFAM/PAGESTACK/ALIGNRES/DELIVERY), the
  01F68168 contra correction, contract closures, routed fixes, harnesses, and
  the consumer-check record
  `_index/candidates/swe2contract-pub-0926-consumer-check.md`. **Integrity
  event:** SWE2-DATA's `0cd44bd1e` clobbered AUDIT-LOG + PROGRAM-STATE from a
  stale copy (~550 lines of uncommitted 09-24..09-26 entries, multiple agents);
  my eight entries re-landed at both tails + `CLOBBER-RECOVERY-0926` note,
  `SWE2CONTRACT-NOTICE-DATA-AUDITLOG-STALEWRITE-CLOBBER` routed to SWE2-DATA.
  Two FRONTIER overlay carriers were refused by the publish guard
  (resource-input-ownership, battle-unit-built) — their hunks stay uncommitted,
  routed via `SWE2CONTRACT-REQ-FRONTIER-OVERLAY-CARRIER-PUBLISH`. Two disclosed
  FABLE hunks rode the publish (tick-frame EX-6, shop 12→11). The board revert
  resurrected 11 of my finished tasks ACTIVE — all re-finished (revs
  32469–32482).
- **Exact next action:** board poll, then routed items — **all previously
  named candidates are now closed**: GB-1 (NO ADMISSIBLE SOURCE, intent),
  GB-2 (4 = no environment class), GC-1 (dev "Display AO Only"), SR-5
  (live probe routed to ASTRA), GJ-7 (FABLE-closed), GG-1 (narrowed
  twice today — static order + float-gate domain; 50 readers + live
  gates still open but ASTRA-scoped). The §14 lane was already exhausted.
  Remaining flagged item is OPUS-owned: `initDwordAA44` store row text
  still says "no reader" while OPUS's own appended census records the
  read at `0029041D` — routed, cross-lane. Standing report: parity
  declaration problems are peer drift, not mine.
- **Pending requests/reviews:** none — `SWE2-REQ-AUDITSPEC-RAMP-REVIEW`
  and `SWE2-REQ-AUDITSPEC-STORAGE-READ-REVIEW` both returned **DONE
  ACCEPT** (reproduced independently).
- **Fallback eligible work:** `CONTRACT-save-container-transform` (round-trip
  is ORACLE-owned); no open CONTRACT-lane register rows remain — wait for
  routed items or a fresh bounded claim if one surfaces.
- **Latest coherent commit/checkpoint:** `a7898d7c1` — two routed owner-edits
  (`FABLE-NOTICE-CONTRACT-0032F240-LABEL` relabelled read-only registered-id
  lookup in steam contract + dispatch page; `FABLE-REQ-CONTRACT-AUTOSTATUS-
  325A00-RULE` guard correction, landed concurrently byte-identical via
  ORACLE's `ac3363c2a`; tasks DONE revs 38407-38408). Prior: `63e60c9ad`
  current-block refresh; `e1363a92c` resume-block correction. Prior:
  `d5869b36d` — GG-1 float-gate qualification publish (4 paths; lease
  released rev 37194); `ASTRA-RETURN-CONTRACT-STORAGE-READ-CURSOR-ALIAS`
  finished already-satisfied.
  Prior: `a68a949c1` — GG-1 narrowing
  publish (4 paths; lease released rev 36122). Prior: `c881e1130` —
  workbench Save/Restore contract refinements (5 paths; rev 36104).
  Prior: `56b3038ee` — SLOTACC census +
  extra-effect dispatch publish (7 paths; lease released rev 34968).
  Prior: `c3582a079` — TIM2 consumer
  closure publish (6 paths). Prior: `55b3371ed` — SECFULL
  correction+addendum publish (7 paths: container doc `files` column +
  family profile, `ebp2_slot_populations.py` control, glyph page TIM2
  correction, AUDIT-LOG amendment, ADDRESS-INDEX regen, resume block,
  consumer-check record). Prior: `2ad08cce6` — SECFULL resume publish;
  `4f0bcd9a6` — initial 20-slot census. Prior: `3b7f5525a` —
  group-completion §14 closed (item 9 / EE-12): all three handlers
  `003250F0`/`00325090`/`00325260` verified live — non-.pdata
  guard stubs `002E7090`/`A0`/`C0` `lea`-registered by
  `002EA320`/`002EA5F0` into `02CA4410`, dispatched by
  PresentationAuthoredCommand_Class* slots and engine track-end
  calls (`0041DC84`/`0041DD03`/`0041CEC6`). "Never posts" hazard
  refuted; §8/§15 corrected. Board tail `624bd3d41`, rev 27920.
  Prior: `48400a43e` — verb-dispatch-abi §14 closed (VA-1 dead
  space bounded; VA-2/VA-3 re-verified). Guard
  adds nothing (12→12, repaired 1 link). Board tail `c5b573b7e`,
  task DONE rev 23852, mutex released. Prior: `86f00da52` —
  save-container-transform §14 item 3 CLOSED + published: zlib
  disposition is stock 1.2.11 shared library (lenfix+distfix 0/544
  mismatches vs inffixed.h; full message census; stock entry
  shapes; inbound census reproduces FABLE's control — `0080C5A0`
  shared with loader `0019AA20`×4, `0087AF40` writer-exclusive).
  Guard initially refused on a Platform edge (`0019AA20` callee
  `0019A510`) — accounted with a Platform-SERVICE bullet in §6,
  re-run adds nothing (12→12). Board tail `bc5082e72` (one re-seed:
  EC7's `2352513bf` raced the first attempt), task DONE rev 23831,
  mutex released. Prior: `58e4c08ef` — efx §14
  item 3 narrowed + published: 4 GiB question splits into capacity
  (proven bound ~260 MiB — `0022A0B0` nine fixed backings ~256 MiB +
  arena-11 regrowth; nested arenas inside backings) and placement
  (CRT malloc, observed <2 GiB EXP-079, OS-policy only — stays
  live/ASTRA). `01F83530` zero for process life (CD-2). Guard
  initially refused on an ActorEntity edge (`0022A0B0` callee
  `002368D0`) — accounted with an ActorEntity-SERVICE crossing
  bullet, re-run adds nothing (12→12). Board tail `eca88830b`,
  publish task DONE rev 23790, mutex released. Prior: `601002f25` — efx §14
  item 2 resolved + published: rebase trigger is demand-driven
  (`003E6AA0` queues dirty `+0x294:27` + `+0x304>>27`=n from 22
  effect-side transfers; `00427DE0` delivers to `003B3C00` at
  `0042865B`; element kind `0x28` polls at `003B939F`; 2-call-site
  census total, no address occurrence). Guard initially refused on
  2 edges (`002E73C0` callers `002FE8D0`/`00303F00`) — accounted
  with a CombatAction/Party CLIENT crossing bullet, re-run adds
  nothing. Board tail `6e52abf2d`, task DONE rev 23745, mutex
  released. Prior: `4e3668536` — efx §14
  item 1 resolved + published: second object `0024D940`+`0x390` =
  the effect container (one call site `003B3C4D`; `+0x340` =
  EfxCallerTemplate context ptr, `+0x390` = own source base; CRO
  `+0x390` = `auxVec36Begin` coincidence disproven). Guard initially
  refused on a UI edge (`0024ED80` caller `0024B9B0`) — accounted
  with a UI-CLIENT crossing bullet, re-run adds nothing. Board tail
  `3063383e6`, publish task DONE rev 23706, mutex released.
  Prior: `26810a44a` (ramp §14 item 5 residual CLOSED: `+0x1C` allocator-zeroed unused dword —
  compiler-merged with `+0x20` init, never read/non-zero-written;
  `+0xD8`–`+0xDF` untouched by all bodies incl. allocator — `0xE0`
  slot tail padding; §15 claim now "every record byte has a censused
  accessor or a named disposition"; board tail `8ff895801`,
  `@publication` released rev 23643). Prior: `242c56d17`
  (`OPUS-REQ-CONTRACT-SEVEN-STATUS-WRITE-REASONS` DONE: seven
  `diff_status_write.py` CONTRACT_MAP reasons re-worded off "0030E360
  is not run" onto EXP-086's record — verdicts unchanged NOT
  EXERCISED, status_write stays NOT COVERED, contract untouched per
  scope; board tail `00494357e`, `@publication` released rev 23594).
  **SWEEP DISCLOSED:** resume commit `23219ee2f` swept five of OPUS's
  staged files (ordered-container docs, `_types/README`, `fields.tsv`,
  `types.tsv` widget-hierarchy declarations) — `git add`+`git commit`
  on the shared index instead of `publish_paths.sh`. Nothing lost or
  altered; attribution wrong. P0 notice
  `SWE2-NOTICE-SWEEP-TYPES-BATCH` filed to OPUS (rev 23603, tail
  `10abe8262`). All further commits use the private-index technique.
  Prior: `5d5516104`
  (ramp §14 item 3 residual closed: `+0x118` = handbook monster
  viewer model-open flag; `+0xAA44` = `ManagerSub0209BE80_A0D0
  +0x974` `initDwordAA44`, the `003F80D0` group's one-way ready
  dword; board tail `e0b4dfc38`, `@publication` released rev
  23564). Prior: `34ab24ed3`
  (field-runtime-pass `FRP-3` closed: `+0x10` bit 0 = the slot live
  flag — set only `0026D305` init / cleared only `00262DA8` unload;
  census widened to all byte-write forms in 58 base-takers + all 93
  `00263FF0` getter callers; five accessors fail closed on it;
  refusal 2 = not-live, "disabled" excluded by construction; §15
  PROVEN row + CONTRACT_MAP NOT EXERCISED row; board tail
  `72a419676`, `@publication` released rev 23527). Prior: `2fccc3aea`
  (V2 gate-cell census — ramp §14 item 2: `02B3F554` = +4 of
  the V2 pool's 32-byte header, a mode dword written at five
  sites, NO reader in any static form; published-but-unconsumed
  state; board tail `e072d6ded`). Prior: `760fd63b4`
  (exercise-declarations publish — OPUS-NARROWS ruling applied:
  isolated EXP evidence credits §13/§15; status-write §13+§15
  EXP-086, verb-dispatch §15 EXP-085, both map rows re-worded;
  board tail `37c3dbbd2`; four routed tasks DONE — the ruling,
  the superseded CONTRA, EOL-FLIP (this file is LF), and the
  EXP-nine-none census: all nine `contract: none` readings
  confirmed correct, per-record verdicts on the board). Prior:
  `252bc2ae7`
  (ramp consumer-map batch — §14 items 1+5: `003B62D0` channel
  map, record layout closed to `+0x1C`/`+0xD8–0xDF`/`+0x30,34`-
  reader residue; board tail `48def90e8`). Prior: `d22e22bbf`
  (two-closure batch — transform §14 item 5: `022D91F0`/`022D9210`
  are VU0 vector registers 5/7–8, oscillator second-4×4 via
  `0040DBB0`/`0040B780`; ramp §14 item 3: three tick gates
  decoded — `00358290` aux-mask bit 1, `00181DD0` singleton
  `+0x118` byte, `002E05C0` manager-flag/UI-request predicate;
  ramp contract hunk rode EC7's `be46e51ef`, disclosed; board
  tail rode FABLE's `26141406b`). Prior:
  `ade5d40fb`
  (transform-primitives §14 item 6 closed: `00397910` provably
  only a 4×4 multiply; board tail `38a32dac6`). Prior:
  `ade47bab6` (drift sweep: EY-1=Bubble, PCD-5→PCD-1..4, U-6 tick;
  board tail `e1527066b`).

## Checkpoints

Append below, newest last. Record corrected facts and remaining work, not file growth.

## Checkpoint — identity created 2026-09-13 (written by OPUS)

Nothing claimed yet. `team.py` now carries four identities and its validator prints the count rather
than asserting three; the board gained an SWE2 record with no claims and no history rewritten; and
`test_team.py` gained scenario **G**, which asserts four-way contention on one resource,
`@publication` exclusivity across all four, `@runtime` behaviour unchanged, a request addressed to
SWE2 being claimable by SWE2 alone, and owner-only closure still requiring durable references.
**9 of 9 tests pass.**


## Checkpoint — OPUS-FUNCLIST-EXTENT-OVERRUN adjudicated 2026-09-13 (SWE2)

Reproduced OPUS's strict rule exactly (36 = 23 listed + 13 unlisted; 4,468 = end minus first int3
run over the 36). The strict rule is a shape detector, not the census: plain overlap finds **29
merges**, strict sees 23, misses 6 (three no-pad adjacencies, two pad-ends-at-entry undecodable
tails, one embedded-switch-table desync). All 13 unlisted-boundary hits adjudicated **legitimate
bodies** — interior alignment pads, branch-targeted exactly, register-live, no prologue. Per-row
evidence: `_index/FUNCTION-EXTENT-ERRATA.tsv` (42 rows, `corrected_end` per merge). Instrument:
`gfz-scripts/check_extent_overruns.py`. Consumers told in PROGRAM-STATE's new section:
script_verb_shapes confirmed (8 handlers / 4 family flips, regen stays with OPUS-VERB-SHAPES-REGEN);
seven other decode-over-extent tools inherit; three extent→owner lookups misresolve the swallowed
range; program_coverage double-counts; engine_explained unaffected (citation count). functions.tsv
not hand-edited — shared generated artifact. Submitted for OPUS review.

## OPUS review — `OPUS-FUNCLIST-EXTENT-OVERRUN`, package 1 of 10: **ACCEPTED**

Reviewed against the shipping image, the errata rows and the instrument — **not against the
report**. Nothing returned for repair.

### What I re-derived rather than read

| check | result |
|---|---|
| the instrument reproduces | **yes** — 36 strict (23 listed + 13 unlisted), 29 merges (23 strict + 6 overlap-only), 13 legitimate bodies, 4,468 bytes |
| five `merge` rows' `covered_listed_entries` | **exact**, all five |
| what lies between each `corrected_end` and the next entry | **pure `cc` padding** in all five — so `corrected_end` is the last byte of the real body, not a guess |
| three `legitimate body` rows | **an internal branch really does target the boundary** in all three (`001DE5D0`, `00200BF0`, `00205B40`) — the interior-alignment-pad argument is applied correctly, not asserted |
| the merge count, independently | I censused overlapping listed bodies **before this package was submitted** and found **29 distinct outer bodies**. SWE2's plain-overlap census says **29**. Two instruments, built separately, agreeing. |

### The best thing in this package

> **"The strict rule is a shape detector, not the census."** SWE2 reproduced my rule exactly, then
> showed it **misses 6 of 29** — three no-pad adjacencies, two pad-ends-at-entry undecodable tails,
> one embedded-switch-table desync — and reported both numbers rather than the flattering one.
> That is the correct handling of an inherited instrument, and it is what I would have wanted found.

### One claim I tested because it lands on my dimension, and it holds — for a better reason

SWE2 wrote *"engine_explained unaffected (citation count)"*. I checked: **47 listed entries sit
inside swallowed ranges, and 3 are A-measured in their own right** — for example `0026A420`
swallows `0026A430`, and **`0026A430` holds its own A while the outer does not.**

**So the claim is right, and the mechanism is worth stating:** `measure_a` resolves a citation to
the **nearest preceding entry**, so an overlapped inner function keeps its own citations instead of
losing them to the body that swallowed it. *"It is a citation count"* is true but understates it —
the resolution order is what actually protects the dimension.

### Correct calls worth naming

- **`functions.tsv` not hand-edited.** It is a shared generated artefact; an errata file beside it
  is the right shape, and editing it would have been the tempting wrong move.
- **Consumers enumerated rather than assumed** — the three extent→owner lookups that misresolve a
  swallowed range are named, and `program_coverage`'s double-count is called out.

### Package 1 of 10: **0 defects, 0 rework.** Nothing to repair; close it when ready.


## Checkpoint — OPUS-REQ-SWE2-RAMP-DIFFERENTIAL harness green, gate fixture fixed 2026-09-13 (SWE2-CONTRACT)

**`diff_ramp_channels.py` runs: 483 commands, 129 compared lines, 0 mismatches** against the
shipping image under Unicorn, MSVC-built reconstruction. All six entry points driven at real
addresses — including `003B69B0`/`003B6950`, the two setters `functions.tsv` never listed
(tail-jump reached). Allocator both arms: `NOTABLE` emits the real `L/A8C00/U` extern trace;
the second `ALLOC` makes none. Exact-bit comparison throughout: record dumps, whole-table
FNV-64, float bit patterns.

**Gate fixture defect found and fixed** (answers `AUDITSPEC-REQ-CONTRACT-GATE-FIXTURE`):
the contract's `02B4052C` is the qword pointer's high dword, not a cell; the gate the tick
reads is `02B40524`. `GATE` now drives `02B40524`; `reset()` no longer leaves bit0 set;
`GATE 1` freezes all ramps / `GATE 2` does not / `ALLOC` clears it — discriminating.
Contract-text repair stays with OPUS (`AUDITSPEC-RAMP-GATE-02B40524`).

**Self-falsification:** gate-clearing mutant FAILs (2 mismatches, post-ALLOC hashes).
Literal-division mutant first SURVIVED — dyadic operands — so 8 discriminating float pairs
added (steps 3/5/7/10/13/33/100/255, e.g. `d=0x3F7FF003, s=5`: `div` gives `0x3E4CC002`,
`div+mul` gives `0x3E4CC003`); mutant now fails by exactly 1 ulp. `CONTRACT` dimension
honestly NOT COVERED — fifth-channel "no class writes it" row is PARTIAL.

Also fixed en route: PAIRBUF mapped outside the table region, page-map double-map on
`0x36C1000`, `page_up` on the end address not the size, Unicorn-2 XMM as int, driver
alloc fill `0xCD` matching the Python hook.

**Open (not claimed):** UG-1..UG-5 stand; gate's bit-1 consumer `003B6020` and writer
`003B6930` identified but unexercised. Package routed to SWE2-AUDIT-SPEC.

## `AUDITSPEC-RAMP-GATE-02B40524` — UPHELD. The gate is `02B40524`, and `02B4052C` is not a cell at all 2026-09-13 (OPUS, adjudication)

**SWE2-AUDIT-SPEC is upheld on every point I could check, and I could check all of them.** Each
positive claim reproduces byte-exact from the shipping image, and the two negatives the auditor
correctly flagged as instrumented are now **decoded** negatives with positive controls.

### Verified, byte-exact

| auditor's claim | re-derived |
|---|---|
| `003B589C mov r8d, [rip+0x278AC81]` → `02B40524` | **yes**, and `003B5890` immediately above loads the **table pointer** from `02B40528` as a `qword` |
| `or eax, r8d` / `test al, 1` at `003B58B1`–`B4` | **yes** |
| `003B620E or eax, [02B40524]` then `test al, 2` — a second consumer testing **bit 1** | **yes** |
| allocator `003B6890` clears `[02B40520]` (`003B68CB`) and `[02B40524]` (`003B68D7`) unconditionally | **yes** — both stores sit after the `jne` target, in the straight run before the `0x50`-iteration loop |
| setter `003B6930`: `gate = (gate & (arg >> 2)) \| (arg & 3)` | **yes** — `and eax,[02B40524]` at `003B6938`, `mov [02B40524], eax` at `003B6940`, 23-byte body |

### The two negatives, upgraded from instrumented to decoded

The auditor's sweep was a linear `skipdata` decode and they said so — *"a linear skipdata decode can
misalign inside data islands, so 'zero references' is an instrumented negative"*. **Re-run per body
over all 38,161 listed bodies, where misalignment cannot occur: `02B4052C` has 0 references.**
Control: the same pass finds **5** at `02B40524`, **3** at `02B40520` and **23** at `02B40528`.

**And the gap the auditor flagged as unswept is now closed.** They noted *"whether `02B4052C` is
reached by any non-RIP-relative path (movabs/absolute addressing) — not swept"*. Decoding every body
finds **855 `movabs reg, imm64` instructions** (so the detector fires) and **not one** carries an
immediate anywhere inside `.data` `[01DF0000, 02F97530)`. **No global in this image is reached by an
absolute-immediate address**, so the route does not exist to be taken.

> *One negative I will not offer as evidence:* a byte search for the literal `02B4052C` in `.text`
> returns 0 — **and so does the same search for the real gate `02B40524`**. RIP-relative code never
> embeds an absolute VA, so that search has no positive control and proves nothing. It is listed here
> only so nobody re-runs it and mistakes it for a result.

### Why the contract said `+4`, which is worth more than the correction

**`02B4052C` is not a dead cell — it is the upper dword of the 8-byte table pointer at `02B40528`**,
read as a `qword` at 23 sites including the tick's own first instruction. The contract's *"the global
gate at `[table-pointer + 4]`"* added 4 to the **pointer's address** instead of indexing the record it
points at, and landed in the middle of the pointer itself. The gate is at table-pointer **− 4**.

That also explains `UG-2`'s framing: it asks what the gate is, while `003B6930` is its setter, the
allocator clears it on every call, and `003B620E` consumes bit 1. **The question is already
answerable; it was pointed four bytes into a pointer.**

### `UG-4`, confirmed as far as my sweep reaches

`02B40520` is read at `003B5719` and written at `003B5744`, both inside `003B56D0` — consistent with
the auditor's serial/generation reading, and with the allocator zeroing it at `003B68CB`. **It is not
inert padding.** I have not re-derived the `id = (serial << 8) | index` composition or the wrap
above `0xFFFFFF`; that belongs to the repair, not to this ruling.

### Disposition

**The contract's §3 gate comment and §5 `UG-2` are wrong and must be corrected to `02B40524`.** The
file is under `SWE2-CONTRACT`'s ACTIVE claim and the same defect is inherited by
`diff_ramp_channels.py` (`GATE_AT` writes a dead address; `reset()` leaves `0xDEADBEEF` in `PRE24_AT`,
which is the real gate, permanently gating the original side). **Repair is the producer's**, routed as
`OPUS-REQ-SWE2-CONTRACT-RAMP-GATE-REPAIR`. I am not editing a claimed file, and the six verified
entry-point rows are untouched — the auditor scoped this correctly.

Landed as `a27b5cc5` (9 files via publish_paths.sh). Board: `SWE2-PUB-RAMP`,
`AUDITSPEC-REQ-CONTRACT-GATE-FIXTURE` and `OPUS-REQ-SWE2-RAMP-DIFFERENTIAL` all finished
with the commit ref; review queued as `SWE2-REQ-AUDITSPEC-RAMP-REVIEW` to SWE2-AUDIT-SPEC.

## `OPUS-REQ-SWE2-CONTRACT-RAMP-GATE-REPAIR` — half of it was already done before I queued it 2026-09-13 (OPUS)

**Your `a27b5cc5` landed before my ruling and already carries the right answer.**
`diff_ramp_channels.py` now reads `GATE_AT = 0x02B40524` with the comment *"bit0 pauses the advance,
bit1 read by 003B6020"* — which is exactly the adjudication, arrived at independently — and the
harness reports **129/129 with both mutants caught**. **The fixture half of that request is closed;
please do not redo it.**

**What is still open is the contract prose, and only two lines of it:**

- **line 73** — `# per-slot pause OR the global gate at [.. +4]`
- **line 102** — `- [ ] **What the global gate at `02B4052C` is**` (`UG-2`)

Both still point four bytes past the table pointer. `02B4052C` is **the upper dword of the 8-byte
pointer at `02B40528`**, read as a `qword` at 23 sites including the tick's own first instruction
`003B5890`; the gate is table-pointer **− 4**. And `UG-2` should not stay an open question at all:
`003B6930` is the setter (`gate = (gate & (arg >> 2)) | (arg & 3)`), the allocator `003B6890` clears
it unconditionally at `003B68D7`, and `003B620E` consumes bit 1.

Full ruling with the re-derivations and the two decoded negatives is above in this file.

## Checkpoint — storage-read differential, green and falsified 2026-09-14 (SWE2-CONTRACT)

Self-selected `CONTRACT-storage-read-completion` (19-Save-Load-Settings): three entries —
`00866A00` inner read, `00862590` wrapper, `00583C00` bounded restore. Native semantics verified
directly: the inner read null-guards cursor AND destination, `r8d==0` returns 1 via the empty loop,
bound is unsigned `cursor >= end-base`, return is boolean not count. Wrapper: `mode!=0` → `-4`
written to `02EAF8E0` and returned; else `result = inner(cursor_from_02EAF8E8, dst, n) * n`.
Restore: null parent `02CA99B8` → silent no-op; else `0x1C4*0x80 + 0x40 = 0xE240` bytes from
`[parent+0x588]` into the active image at `02164280` (getter `002EF640` = lea/ret).

Harness: 77 commands, 100 compared lines, 0 mismatches; 5 returns / 7 digests / 5 cursors.
Two harness defects fixed en route: shared-page double-map (BASE `1F44D40` and END `1F44D48` on
one page — mapped set), and a C-side double-space in `print_dest` (pure formatting).

Mutants — 4/4 killed: `m1` count-not-boolean (14 lines), `m2` restore drops the 0x40 tail
(3 boundary digests), `m3` null-guard removed (crash → all lines missing → FAIL, correct),
`m4` mode-arm skips result write (2 lines). The FileNotFoundError was my test loop quoting
`\$m.exe`, not the harness.

CONTRACT derives COVERED (5 EXERCISED / 1 OPEN QUESTION — the caller-misuse row no fixture can
answer). contract_map_sync in step; parity regenerated at 44 pilots.

## Checkpoint — FIVE-INCOMPLETE: all five contracts to template 2026-09-14 (SWE2-CONTRACT)

Claimed `OPUS-REQ-SWE2-CONTRACT-FIVE-INCOMPLETE` plus both P1 notices (finished as noted). Each
contract now carries sections 1–16 with content, not stubs — reproduction formulas carry the real
constants. Falsification passes that collided with template numbers renumbered to unnumbered
appendices (storage-read's held `## 6.`, save-container's `## 5.`, efx's `## 14.` — each noted in
place). §13 on ramp + storage-read now records the landed harnesses, and `check_gate26.py` moved:
isolated original-code 39→41, nothing-executed 4→2 (save-container + efx remain, honestly — no
execution evidence exists). readiness bumped to DIFFERENTIAL TESTED on both
(`OPUS-REQ-SWE2-CONTRACT-RAMP-READINESS` answered: DIFFERENTIAL TESTED is the rung 129/129 + killed
mutants earns). Gates green; sync in step.

## Checkpoint — PASS22-TOPDECILE: band clean, pass 22 at zero 2026-09-14 (SWE2-CONTRACT)

`audit_crossrefs.py` run 8: **1 finding total across 384 docs** — the registered `UNLISTED CODE`
census debt on `002FE7D0` (by design "reported, never dropped"), and **zero unaccounted-neighbour
findings anywhere**, band or otherwise. Band correction noted: the true request band is
00/04/16/17/99 with FABLE holding 11/13 (`FABLE-NOTICE-CONTRACT-PASS22-11-13-TAKEN`, acknowledged).

This block: appended 31 verdict rows to `neighbour-dispositions.tsv` — 19 GENUINELY-IRRELEVANT
(second-order fan-in on `00265020`/`00322C50`/`00253690`/`0031B7E0`/`00379CD0` the earlier prose
had cited), 12+5 CROSSING-ACCOUNTED on the two new FRONTIER layout-reader pages (sections written
on the pages: Presentation/Audio/CoreRT/Items/ActorEntity/CombatAction/Party/Gameplay on
battle-hud; Audio/CoreRT/Resource/Gameplay/SaveLoad/Rewards on message-windows). Those two pages
are FRONTIER's uncommitted LAYOUT-KEY-READERS work — left untracked for their publish to sweep.
check_consistency caught and fixed a 17-vs-99 caller-count disagreement on `00249C60` (the shared
Audio helper; the shared-neighbours page's 99 stands).

Peers cleared the other bands in parallel — OPUS batches through 21, FABLE folders. The top-decile
request's completion ("all 80 rows dispositioned") is met in band and exceeded globally.

## Checkpoint — ABSENCE-ANCHORS: 285 NEARBY rows dispositioned 2026-09-14 (SWE2-CONTRACT)

Claimed `FABLE-REQ-SWE2-CONTRACT-ABSENCE-ANCHORS`. The live corpus measured **285** NEARBY rows
(not the 235 of the 2026-09-13 measurement — corpus grew). Every row read against its context:

- **43 ANCHORED** — the claim's subject address put on the claim's own line. Includes the
  ABSENCE-CLAIM-CLASSIFICATION ledger rows (subject address sat unbackticked in the address
  column — backticked so the gate can bind it), plus page claims: `002AAE40` "no caller" (four
  rows across the 158/census/glyph pages), `02EAF6D8` "no writer" (x2), `01F82E48` "nothing
  reads" (x2), `01F7F5E8`/`01F7F5E0` "no consumer", `01ECB4D0` "no reader" (x2), `00392A10`
  "never called", `00379160` "uncalled" (the doc's own E9 thesis), `01F83530` "no writer",
  `022D94B0` quoted "no writer", `022D8E20` "no consumer", `02CB80C0`/`02CB80C8` "no reader",
  `02EAF930` "no consumer", `02EBF0D0` "no consumer", `00280DE0` "zero callers", `01DF0978`
  "unreferenced", `003250F0`/`00325090`/`00325260` "no caller", `02EBF178`/`02EBF188`/`02EBF198`
  (stale-checkbox rows), `0062DDE0`/`0062DFB0` "no caller context", `00684D10`/`00686280`
  "zero callers", `02B59D60` falsification-table "unreferenced" hypothesis.
- **55 SKIPPED** — `_index/AUDIT-LOG.md` (33) and `_index/OPEN-QUESTIONS.md` (12) sit under
  DATA-FMT-PS2IMG-TAIL (ACTIVE); `_index/PARITY-STATUS.md` (10) is generated from contract maps —
  hand edits would not persist.
- **187 PROSE** — per-row reasons in
  `Tools/work/swe2c/absence-anchor-dispositions.tsv`: field/bit/offset subjects, set/count
  subjects, file/format subjects, harness-coverage statements, quoted/struck claims, index and
  inbox narrative, and cases where the nearby address belongs to an adjacent statement.

Gate re-run: tested bucket **210 -> 253** (+43, exactly the anchored count). 30 anchored rows now
fire positive — the instrument finds a reference where the prose phrases an absence; each is
consistent with its page's own disclosure (operand counts reads/writes/leas uniformly, so
"no writer" claims on read-only globals fire on their readers by design). One row flagged for
adjudication: `02CB80C0`/`02CB80C8` "no reader was traced" on arm-catalogue-slice-B — the
operand fire may be a read; if so the claim needs a re-check.

Gates: `check_consistency`, `check_links`, `check_questions`, `check_stranded_absence`
(LIVE CLAIM 0) all green; `verify_doc_addresses --all` shows only pre-existing REVIEW rows.

---

## 2026-09-22c — IN FLIGHT, unpublished (lease held by FABLE-PUB-001E2AF0-FINISHED ~20+ min)

Two packages complete on disk, gates green, awaiting `@publication`:

1. **SWE2CONTRACT-COMMIT-SHADOW-NULLAPPEND-0922** — action-commit §14 fully closed:
   `+0x718` shadow census (only cancel `003105EF` reads for decisions; second shadow
   `+0x730`–`+0x747` found, readers unenumerated); null-append sole reliance
   `002FFB60` `count>0` gate at `002FFC3E`.
2. **SWE2CONTRACT-RESINPUT-RL4-0922** — resource-input-ownership RL-4 struck WITH
   CORRECTION: live borrower is `003B38B0` (`or [template+2],0x0C` at `003B3984`,
   live chain via `lea`-registered tops), NOT the EFB wrapper `0026FB90`, which is
   statically orphaned (4 route forms, 0 hits). Other 4 constructors copy.
3. **SWE2CONTRACT-COMMIT-BANDMEANING-0922** — commit-action §14 fully closed;
   band meaning was stale (handler-table page mapped it 2026-09-02).
4. **SWE2CONTRACT-WEATHER-GB3-0923** — `02099DB0` = write-only dead global
   (one accessor: store `0026DA5B` in `0026D910`; all 4 route forms negative).
   §15 row added PROVEN. **DEFERRED: OPEN-QUESTIONS GB-3 row update** — apply
   after FABLE's open-questions.md edit commits (file-claim conflict).
5. **SWE2CONTRACT-SAVEIMG-BACKUPBUF-0923** — backup buffer = dead storage:
   raw disp32 scan over ALL .text (catches non-.pdata `002EF570`) finds one
   accessor (the writer's lea), zero readers; stride tail `0x22BDD50` hosts a
   LIVE record (narrows the "padding" claim). diff_save_image.py +1 map row
   NOT EXERCISED, CONTRACT→NOT COVERED.
6. **SWE2CONTRACT-RECIPES-PREVIEWWALKER-0923** — weapon-recipes §14.1 struck:
   preview consumer = `0x3858E7` (walks `blob[0..len1)` via same step table,
   different result record); statically orphaned. NEW ROUTE FORM discovered:
   `lea reg,[rip->0x120000]` + disp32 RVA — invisible to rip/imm/qword
   censuses; found only by raw disp32 byte scan. Two table refs total.
7. **SWE2CONTRACT-SAVEPIPE-CLEARS-PADDING-0923** — save-image-pipeline §14
   fully closed: clear-caller split (`002EF650` compound ← 3 callers;
   `002EF5F0` bare ← teardown `003601D0` only); SV-5 corrected (both reach
   icall stub); backup write is the LOAD-mode arm (restore-on-failure shape,
   no reader shipped); tails split — `0x22BDD50` live record, other three
   dead slack. Buffers contract "every save"→load-mode corrected.
8. **SWE2CONTRACT-SLOTMAPS-CLASSES-0923** — slot-maps §14 closed: map 0 live,
   maps 1–4 frozen snapshots (`00329CC0` copies); literal classes {0,1,2,3},
   class 4 computed-only; `003266DB` is the sole computed-pointer write route
   (record-identity residual).
9. **Contra task** (FABLE-CONTRA-…, claimed ACTIVE): `001A9930` loads `01F81168`
   (map-art context), not `01F68168`; both doc spots corrected, gates re-run.
10. **SWE2CONTRACT-LOOT-NEAREST-CALLER-0923** — world-loot-pickup-pool §14
    "no caller" claim corrected upward: `00319850` IS called, at `003129AF`
    inside `BattleLocomotion_DecodeOrderGoal` (`00312730`) on order-goal
    opcode `0x4165` (the `>0x4035` tail switch; second-to-last internal-order
    opcode). Contract + owning page corrected; runtime reachability of order
    `0x4165` is the remaining (live) residual.
11. **SWE2CONTRACT-WORKBENCH-TW6-BQ16-0923** — shared-transform-workbench §14:
    two of three items stale, both struck. BQ-16 already answered (VU0 register
    bank — 31 regs + ACC, not matrices). TW-6's "pointer slots" already resolved
    by page BQ-17: `022D94B0`/`B4` = base of a 32×24-byte record table, written
    by indexed stores through a `lea`-taken base (`0036DE5A`/`0036DF6A` state-word
    resets, `0036E2F8` flag byte) — invisible to rip-store census. TW-6 wording
    corrected; remaining item: borrower overlap (§10).
12. **SWE2CONTRACT-WBSAVE-FOURROWS-NBOUND-0923** — save-restore §14: three of
    four struck. No caller saves a whole matrix (nine sites, ecx ∈ {1,2});
    `022D8F0C` belongs to borrower `00502280` (111 region refs) as `00501820`'s
    bit-offset parameter — §10/§15 "no relationship" corrected; N structurally
    bounded at 32 (values[32] aliases pointers[0]), unenforced. NB: `0036D930`
    is a non-.pdata body; values array overlaps a stride-0x70 table's last
    record at `02EC07D8`–`02EC0847`. Map: withdrawn claim → OPEN QUESTION,
    +1 NOT EXERCISED. PARITY-STATUS regen shows 16 problems — +2 are the peer's
    in-flight experience-and-licence rewrite, not mine.
13. **SWE2CONTRACT-ENCID-QREC08-0923** — encoded-id-space §14: "+0x08 written
    and read by nobody" corrected to write-only — `0031C5D0` stores `[rbx+8]`
    in class arms 6/10/20/21 (the `002F9860` string resolver); FY-3's zero-reader
    census stands.
14. **SWE2CONTRACT-SHOPSTOCK-THIRDCALLER-0923** — shop-stock-ladders §14 SG-6
    closed: the unaccounted `00315390` call site is `0056F482` inside `0056F470`,
    the handbook screen's pane-1 leaf helper (installed by `0056F410` via
    `003946B0`); it recomputes the rank and feeds `00394850` — a UI read, same
    recompute-not-store shape as the save header. Three callers now all named:
    `002536F0` / `00583D60` / `0056F470`. Board task added+claimed+finished
    (revs 29206–29208).
15. **SWE2CONTRACT-WORLDTICK-GETTER-0923** — world-simulation-tick §14 closed:
    `00314960` (the sole reader of `022C2548`) is the engine's reentrancy
    deferral gate — 12 call sites in 12 bodies, 8 pairing it with `001EDDA0`
    (`[01DFE0C0]!=0 || [01F82E38]==0`), 4 flagging/diverting. WT-3 unchanged
    (word still has one reader). Board task revs 29209–29211.
16. **SWE2CONTRACT-TRIGPTS-BAND-CHEST-0923** — authored-trigger-points §14:
    both items stale, both struck. `0x1B..0x27` band = the 13 Espers
    (AUDITED type-id page; `0x1A` Chocobo earns LP, Espers earn nothing);
    `002FAFD0` = the treasure-chest resolver (AF-6; sole caller the
    `btlAtelOpenTreasureMessage` end thunk `0050FAF0`, Diamond Armlet swaps
    the item pair 50/50→95/5). Board task revs 29212–29214.
17. **SWE2CONTRACT-ACHIEVE-ARMS-0923** — achievement-counters §14: two items
    closed. All eight `00315E90` mode arms decoded (dword-RVA table
    `00316098`; shared award tail `00316045` = bitmap `bts` + platform call
    `008632B0`): 0 counter≥threshold; 1/7 no-ops; 2 collect-all range loop
    `00309EC0`; 3 low-16 bitcount≥threshold; 4/5 predicates `003160C0`/
    `003161A0`; 6 chain-walk indexed lookup `00315420`. `003165C0` walk
    re-verified — FOUR word-hops (EC7-26 said three). Revs 29215–29217.
18. **SWE2CONTRACT-STOPREG-BIT41-0923** — system-stop-registry §14: 2 closed,
    1 narrowed. Bit 41's reader IS the apply's own tail (`002264D8` tests it
    in the all-slots AND → `ebp` feeds `002DF370`); reset clears it on slot
    13 only, so it = "first apply since reset" flag. Apply `00226280` is
    synchronous-only (25 edges, no frame poll) — ≥10 wrappers start without
    applying; SS-6 hazard real. Slot rest: `+0x10` = fade dword,
    `+0x14` = zeroed byte; `+0x08`/`+0x15..17` unobserved. Revs 29218–29220.
  - **`SWE2CONTRACT-HEADING-REFUSAL-0923`** — heading-speed-to-position-delta
    §14: both closed. `002E4380`'s refused `{0,0,0,1.0}` is unreachable —
    sole caller `002E50CB` (Movement_UpdateActorFrame) dominated by its own
    class-3 gate `002E5077`; `002E5085` fragment fallthrough-only. LD-2:
    class 1 = placed objects, same `[+0xB8]+0/+4/+8` read path — wider gate
    correct for a read-only query. Revs 29221–29223.
  - **`SWE2CONTRACT-SHOPSTOCK-ALLGATED-0923`** — shop-stock-ladders §14:
    both closed by `battle_pack.bin` rescan. Kind 1 ships on zero rows (dead
    arm, same `00321190` test as kind 2). **12 rows truly all-gated** (2 clan;
    21/22/26/27/43/44/48/49/51/54/55 story 500–3250) — SG-2's last-entry
    fallback observable in normal play. Page footnoted: literal ungated-last
    on 43 rows only. Revs 29224–29226.
  - **`SWE2CONTRACT-TURNLIM-BL3BL5-0923`** — battle-locomotion-turn-limiter
    §14: both closed. BL-3 bits = `locomotionFlags+0x1F0` bits 2|3|4
    (FCP slot-41 / flag 23 / non-Attack action). BL-5 pair is consumed by
    the limiter itself — `0033659D` latched direction selects `current±rate`,
    skipping wrap-delta recompute; committed-direction latch across frames,
    no outside reader. Revs 29227–29229.
  - **`SWE2CONTRACT-ACHIEVE-BITMAP2-0923`** — achievement-counters §14:
    both closed. `+0x3848..–4B` = second bitmap (kind-7 flag bank,
    `bts`/`btr` reversible) written by `00315B50` / read by `003157E7`;
    descriptor-index join done by AB-2 (`01DFE410` + TSV). Layout
    `+0x3844` award 4B + `+0x3848` flags 4B + `+0x384C` counters 0x20.
    Revs 29230–29232.
  - **`SWE2CONTRACT-ENCID-C13-GAPS-0923`** — encoded-id-space §14: two
    closed. Class13 fourth-range mismatch unreachable shipped (validator
    `00322E28` sums four null-safe descs; `02EBF078`/`+0x94` ships `0×10`
    → admitted `[0x8000,0x8200)` = the three real sub-tables). Truncation
    unreachable on offset side (all 45 offset qwords' high halves 0);
    residual = BSS base `01F83530` runtime magnitude. Gap census: 17
    disp32 candidates, 5 immediate FPs, 12 verified — zero static gap
    accesses; 191 sites tracked, sole gap read `[rax+0x5C]` diff loop
    `002CFF45`, class data-derived. Revs 29247–29250.
  - **`SWE2CONTRACT-RECINIT-SIZE-EH1-0923`** — actor-storage-record-
    initialisation §14: both closed. Record size = per-class authored
    strides from descriptor table `0x1E0C328` `{u8 class, u8, u16 stride}`
    carved align16 in one zeroed pool — class 3 = `0x6E0`/`0x670`,
    classes 0–2 = `0x2D0`–`0x3B0` (matches page EH-2's 720–1760).
    **EH-1 was already PROVEN on the page 2026-09-08** — carve loop writes
    `+0x03 = (class<<5)|(group&0x1F)` itself (`00267AFA`–`00267B13`),
    re-verified; the contract had never imported it. AR-5 spans stay open.
    Registered `SG-2` in OPEN-QUESTIONS (ANSWERED) to fix the ledger
    cross-check my shop-stock strike created. Revs 29233–29235.
  - **`SWE2CONTRACT-STATUS-GE23-0923`** — first OPEN-QUESTIONS package
    after §14 exhausted. the-thirty-two-statuses `+0x0A` amendment: GE-3
    ANSWERED — `rsi` is `0031C5D0`'s null constant (`0031C5EC`), so the
    missing-slot path reads `word [0x0A]` = guaranteed AV, reachable only
    pre-install (`02EBF118` written by shim `003847B0` → `003845F0`,
    master `+0x40`); GE-2 ANSWERED — truncation needs
    `low32(rowbase)+40·idx ≥ 2³²`, gated on `J-C` live read of `01F83530`.
    Revs 29251–29253.
  - **`SWE2CONTRACT-INPUT-GG4-0923`** — input-subsystem GG-4 ANSWERED.
    `002A3250` clears held word `02F97368` unconditionally at `002A329B`
    (qword store covers edge `6A` too) — a level clear on window
    reconfigure: `002E16B0` (message-window opener) → `002A35B0` thunk →
    `002A3250`, on the `slot+0x40 == 0xFF` arm. Revs 29254–29256.
  - **`SWE2CONTRACT-ROUTER-GH12-0923`** — ui-request-router GH-1 + GH-2
    ANSWERED. GH-1: `003F4E70` mirrors latch `02092734` into `win+0xF8` bit0
    (copy idiom `003F4FD7`), never gates/writes it — R-4 unchanged. GH-2:
    `002E15D0` = second reset (28-B leaf, all four cells), callers
    `0026A5F0` slot unload + `0026DB30` field-transition reset — producer
    census complete. Revs 29257–29259.
  - **`SWE2CONTRACT-SOUND-SR6-0923`** — sound-request SR-6 ANSWERED +
    §15a QUALIFIED resolved to PROVEN. Init `003A1434`–`003A14A6` writes
    66 nodes (`edx<0x42`): 64 pool slots + sentinels 64/65
    (`02AEF3C0`/`02AEF3D8` = used/free heads), `entry[i].+8=i` self-tag —
    the 64/66/72 reconciliation. No producer mints low-word>63: all
    handles derive from `003A0C90` (walk/alloc); globals' writers are 3
    `003A1650`-result stores + `-1`; `003A1240`'s sole caller reads a
    stored handle written only by `002E61E9`/`-1`; no stored pointer.
    Bound is data-flow, not code — latent hazard noted. Revs 29260–29262.
  - **`SWE2CONTRACT-UQ139-VERIFY-0923`** — UQ-139 closed as already-answered
    (FABLE's PROPOSED-repos2d-4, 2026-09-18). Re-ran the `01F83530` census:
    exactly 2 rip-refs (`0020E600` add / `0020E61D` sub), no lea, no shipped
    value → base=0; encode=truncate IS resolve=zero-extend. Covers all 5 §8f
    publishers (same 10-B shape, same `0032E620` chain). Also closes the
    J-C-class residual GE-2/ENCID-C13 left on this global. Revs 29263–29265.
  - **`SWE2CONTRACT-INPUT-GG23-0924`** — GG-2 + GG-3 ANSWERED. GG-2:
    `002498B0` never entered indirectly (no stored ptr/lea/FF-indirect/jcc
    image-wide; route set = the 4 enumerated, mutually exclusive under
    `0022A580`). GG-3: `002284F0` = `obj+0` handler of the lazy singleton
    widget at `01FD4948` (accessor `00228490` → factory `00244F50`; ctor
    `002465F0` stores handler at `obj+0`, default `005C5230`); created only
    from `002283AE` in `00228380`. Msg 2 sent by `00248030` — `bt [rbx+0x40],
    0x12` gates `call [rbx]` with `rdx=&00915108` (id 2), clears the bit;
    13 sites incl. `0022865C` inside `002284F0`. Revs 29268–29270. (Also
    housekeeping-finished the stale READY `ENCID-QREC08` record, 29266–7.)
    *GG-3 sender half superseded 2026-09-25 (FABLE-CONTRA-GG3): bit 18 SET
    suppresses the call; the `and` clears bit 17 (re-stamped from
    `0208ED5C`); record is `00915108`={2,0,0}. Owner half stands; FABLE
    splice-published the correction into the contract and register row.*
  - **`SWE2CONTRACT-WEATHER-GB3-0923`** — GB-3 ANSWERED: `02099DB0` is the
    only cell of the `02099DA8`..`DBC` mirror block with no accessor —
    neighbours read via getter thunks `00263E10`/`00263E20`/`00264D50` and
    `02099DB4` cmp sites; its sole access is the `0026DA5B` store. Non-rip
    blind spot bounded: only materialised bases nearby are the `02099DE8`
    bitmap (`idx≥0`) and `02099DF0`/`02099FF0` scratch banks (forward
    `slot*4`) — reaching `DB0` needs a negative index outside every
    documented domain; no `lea` targets the block. Vestigial publication.
    Revs 29272–29274 (`-0923` was a stale ACTIVE claim on the same file —
    finished with the result; duplicate `-0924` add claimed+closed
    administratively).
  - **`SWE2CONTRACT-STATUS-GE1-0924`** — GE-1 ANSWERED: bank 12 of the
    `002F9860` string pool = the group-49 `MMSG` resource =
    `listhelp_status.bin` (fst[2][49] = 3568 B, `st2e`, 32 rows
    `120000+n` — status help texts). Route: `002FA560(bank)` switch →
    `002385D0` → `00384420(01E09F68[bank], stub, "MMSG", 3, 4, 8)` → stub
    `002F7800` binds `02F973C0[12]`. The encoded-id page's "bank 12 =
    Key Items" is the packed name-word bank space — flagged, not
    reconciled. Revs 29275–29277.

Publish list when lease frees: `14-Story-Event-Quest-Hunt/persistent-flag-banks.md`,
`18-Audio/Audio-Boundary/CONTRACT-sound-request.md`, `16-UI/CONTRACT-ui-request-router.md`, `15-Input/CONTRACT-input-subsystem.md`, `10-Status-Periodic-Terminal/the-thirty-two-statuses.md`, `00-Engine-Core-Runtime/Battle-Frame/CONTRACT-world-simulation-tick.md`,
`Battle-Frame/the-world-tick-and-the-field-frame.md`,
`07-Combat-Action/CONTRACT-the-moment-an-action-is-committed.md`,
`07-Combat-Action/CONTRACT-commit-action.md`,
`02-Resource-And-Asset-Pipeline/CONTRACT-resource-input-ownership.md`,
`03-World-Area-Field/CONTRACT-weather.md`,
`19-Save-Load-Settings/CONTRACT-save-image-buffers.md`,
`08-Combat-Formula/CONTRACT-weapon-recipes.md`,
`19-Save-Load-Settings/CONTRACT-save-image-pipeline.md`,
`11-Party/CONTRACT-the-five-parallel-slot-maps.md`,
`13-Rewards-Progression-Economy/CONTRACT-world-loot-pickup-pool.md`,
`13-Rewards-Progression-Economy/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md`,
`00-Engine-Core-Runtime/CONTRACT-shared-transform-workbench.md`,
`00-Engine-Core-Runtime/CONTRACT-transform-workbench-save-restore.md`,
`00-Engine-Core-Runtime/CONTRACT-encoded-id-space-and-class-registry.md`,
`12-Items-Equipment-Shops-License/CONTRACT-shop-stock-ladders.md`,
`16-UI/Handbook/the-handbook-screen.md`,
`03-World-Area-Field/CONTRACT-authored-trigger-points.md`,
`20-Platform-Online-Achievements/CONTRACT-achievement-counters.md`,
`00-Engine-Core-Runtime/System-Stop-Registry/CONTRACT-system-stop-registry.md`,
`06-Movement-And-Navigation/CONTRACT-heading-speed-to-position-delta.md`,
`06-Movement-And-Navigation/CONTRACT-battle-locomotion-turn-limiter.md`,
`12-Items-Equipment-Shops-License/the-shop-table-and-its-stock-gates.md`,
`04-Actor-Entity/CONTRACT-actor-storage-record-initialisation.md`,
`Reconstruction/Tests/Differential/diff_save_image.py`,
`Reconstruction/Tests/Differential/diff_workbench_save.py`,
`99-Unresolved-Residual/Glyph-Run-Rendering/the-text-element-dispatch-table.md`,
`99-Unresolved-Residual/Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md`,
`_index/PROGRAM-STATE.md`, `_index/AUDIT-LOG.md`, `_index/PARITY-STATUS.md`,
this file; then finish COMMIT-SHADOW, RESINPUT-RL4, COMMIT-BANDMEANING,
WEATHER-GB3, SAVEIMG-BACKUPBUF, RECIPES-PREVIEWWALKER,
SAVEPIPE-CLEARS-PADDING, SLOTMAPS-CLASSES, LOOT-NEAREST-CALLER,
WORKBENCH-TW6-BQ16, WBSAVE-FOURROWS-NBOUND, ENC-ID-QREC08, SHOPSTOCK-THIRDCALLER,
WORLDTICK-GETTER, TRIGPTS-BAND-CHEST, ACHIEVE-ARMS, STOPREG-BIT41,
HEADING-REFUSAL, SHOPSTOCK-ALLGATED, TURNLIM-BL3BL5, ACHIEVE-BITMAP2,
RECINIT-SIZE-EH1, ENCID-C13-GAPS, STATUS-GE23, INPUT-GG4, ROUTER-GH12, SOUND-SR6, UQ139-VERIFY, INPUT-GG23, GLYPH-GJ8, GLYPH-UQ364, GLYPH-UQ363, GLYPH-UQ366, GLYPH-OBJRESOLVER, GLYPH-STREAMFAM, PUB-CONTRA + contra task, tail.
PARITY-STATUS.md: regenerated at 16 problems — the +2 are the peer's in-flight
experience-and-licence rewrite; prefer publishing AFTER that lands, else note it.
ADDRESS-INDEX.md dirty = PEER work + MY regen — do NOT publish while peer dirt
is in it.
OPEN-QUESTIONS.md now carries MY `## SG.` section at EOF (SG-2 ANSWERED) plus
MY GE-1/GE-2/GE-3 (~3444), GB-3 (~3405), GG-4 (~3475), GH-1/GH-2 (~3486), SR-6 (~3497), UQ-139 (~2907), GG-2/GG-3 (~3471), GJ-8 (~3507), UQ-364 (~3510) and UQ-363 (~3226) and UQ-366 (~3229) row flips + PROPOSED-repos2d-4 (~1353) row flips mid-file on top of pre-existing peer
dirt — check `git diff` on it at publish time and only publish if the peer's
hunks have landed first.
diff_commit_action.py left untouched deliberately (its map belongs to the sibling contract).

**Workflow adoption — FF12-WORKFLOW-MIGRATION-20260928-01 (dispatched by SWE2-FRONTIER, 2026-09-28, at next safe checkpoint).**

The user approved a completion-driven workflow migration. Preserve your current identity, active work and ownership. Read the adopted _index/workflow/COMPLETION-WORKFLOW.md and its revision at your next safe checkpoint. OPUS now owns technical migration delivery; ASTRA/SOL independent engineering verification; FABLE connected mechanism completion; FRONTIER operations, safe deployment and capacity allocation. Existing specialist roles remain. This supersedes older operative instructions assigning sole migration architecture to FRONTIER or categorically forbidding useful new tools; it does not supersede full L1+L2 requirements, independent review, safety, game-state protection or history. Do not stop useful work merely to re-plan. Respond through current checked records, self-check changes, consume review, update authorized canonical files and select the next eligible task without user relay. Honour explicit stops and limits. Report a real policy/ownership conflict instead of silently overriding it.

Read the adopted _index/workflow/COMPLETION-WORKFLOW.md, current evidence policy and checked task state. Preserve your existing lane identity, history and peer work. OPUS owns technical delivery, FRONTIER assignments/deployment, SOL independent engineering verification, FABLE completion semantics. Complete your assigned contribution through its required canonical changes and review; a request alone is not package closure. Use existing task IDs and exclusive paths; do not create a competing implementation or direct-edit TEAM. If capped or blocked, checkpoint for a supported handoff and do eligible independent work, without evading limits.

SWE2-CONTRACT: finish authorized incorporation of accepted findings into the owning contracts and pages. Prioritize review-ready packages before adding template volume. Record which exact claims, types, pages and tests depend on a correction. Preserve historical statements as superseded, not active truth. Do not infer independent acceptance from a peer's DONE routing task.

Implement only assigned bounded publication/interface checks; explicit changed-claim/consumer records and executed regression receipts matter more than strike-through keywords. Use original source evidence and the latest reviewed SN-1 identity/attribution limits, not older goal text. Track pending integration until actual files land. Provide real reviewer identities, requirement links and missing proof to the dashboard. A sparse or empty register must not hide page-local requirements or carried residue.

Self-check and record exact source/driver/input/result identities and limits. Use a qualified non-author for independent acceptance of your production. A required upstream failure or missing result is not PASS. Preserve historical receipts and relevant regressions; run impacted checks during development, broader campaigns only at governing gates. Update the actual tool/consumer path and persistent procedure so the same defect is caught next time. Use fresh preimages, supported writes, short publication claims and meaningful commits. Keep contribution DONE separate from parent acceptance and whole L1+L2 completion. Respond through the existing board and continue eligible work without user message relay; honour explicit stops and real limits.
