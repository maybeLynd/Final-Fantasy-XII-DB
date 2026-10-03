<!-- TEAM-CURRENT:begin agent=SWE2-AUDIT-SEM board_rev=50160 epoch=4 queue_sha=7b4c8087fee07ee1 -->
> generated 2026-10-03T09:12:45+00:00 by `team.py current` - do not hand-edit; hand-maintained
> counts and NEXT lines anywhere else are superseded by this block.
> ACTIVE: AUDITSEM-PUB-STANDIN3-1003
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

# SWE2-AUDIT-SEM — inbox and handoff

**Independent auditor - semantic packages.** Default auditor for FRONTIER, DATA and semantic-family EC-7. One of the eleven fixed production identities (2026-09-13 migration; the
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
   `python team.py apply --agent SWE2-AUDIT-SEM --file op.json`. Never edit `TEAM.json` by hand.
5. **Commit explicit reviewed paths** with `publish_paths.sh <message-file> <path> …`. It refuses a
   directory argument on purpose: `git add` on a directory stages every changed file under it,
   including a peer's.

## What this lane is for

**Inspect the evidence, the original code, the tests and the database diff - never the producer's summary.** A package that reproduces its own numbers has proved only that it is deterministic. Return one of ACCEPT / ACCEPT-WITH-NARROWING / REJECT / ESCALATE-FABLE / ESCALATE-OPUS / ESCALATE-ASTRA, with the exact defect named when it is not an accept. **The producer repairs its own package**; the auditor does not silently redo the work.


## Two standing limits

- **A stub is not proof of its native effects.** Disclose injected state, stubs and entry
  boundaries; omitted initialisation, scheduling and effects stay open.
- **Agreement between a reconstruction and its own fixture is not evidence.** The control has to
  come from the shipping image or from the documents, never from recollection.

## Resume state

Updated at every checkpoint; a restarted session rebuilds from this block before touching the board.
Required by the continuity rule in the root `CLAUDE.md` ("What a plain `Continue` means").

- **Identity:** SWE2-AUDIT-SEM
- **CHECKPOINT 2026-10-03 09:15Z (Claude stand-in for Devin): four more items DONE. Supersedes the "next action" below.**
  - `2f1259752`: `OPUS-REQ-AUDITSEM-S49-REREVIEW-1003`, ACCEPT-WITH-NARROWING. D1 is repaired: `02CF8260` is declared, and a raw
    `.text` scan finds its 29 references. One narrowing: contract §8's code snippet (line 234) still says "CFG path". 15 more
    undeclared S-49 addresses were routed to the L2 expansion census.
  - `c858f27ff`: `OPUS-REQ-AUDITSEM-L1-VERDICT-ITEMS-1003`, ACCEPT. S-45's registry row now lists the steam contract.
    S-25 p2, S-29 p1 and S-38 p2 are SCOPE-SHORT. This lane authored those cells, so the wordings were routed to the
    expansion re-score, and AUDIT-SPEC (non-author) concurred in `78595090d`.
  - `b7a084d4a` + `ab6665a77`: `AUDITSPEC-REQ-SWE2-AUDIT-SEM-L2EXP-REPAIRS-1003`. This repairs the lane's own cells after
    AUDIT-SPEC's independent census (`78595090d`). Types cells MET→PARTIAL (L2→NOT MET) for S-09, S-10, S-14, S-16, S-17,
    S-22, S-25, S-31, S-36, S-39 and S-45, with S-28 also re-scored PARTIAL for `02097D20`. Each returns to MET when OPUS's
    declarations land (`AUDITSPEC-REQ-OPUS-L2EXP-REPAIRS-1003`). **Note:** `b7a084d4a` also carried 11 of SWE2-DATA's
    runtime-row edits from the shared worktree (record `4207b4a16`); `ab6665a77` documents it. goal_gate reads 16/52 NOT MET.
  - **Current package/claim:** none. **Next action:** re-score the 11 types cells to MET as OPUS's declarations land
    (check with `types_census2.py` in `auditspec-l2-expansion-1003/`). Always diff `L2-VERDICTS.md` before publishing
    it, because other lanes edit it too.
- **CHECKPOINT 2026-10-03 06:45Z (Claude stand-in for Devin): L2-MET risk sample DONE, published `bcbf43096`.**
  This supersedes the "nothing done" line below. User task (audit follow-up package §6): a stand-in audited six MET
  systems. Verdicts: S-02, S-13, S-28, S-43 ACCEPT-WITH-NARROWING; S-36 and S-49 REJECT. Record:
  `_index/candidates/auditsem-l2-sample-1003/README.md`. It recommends expanding the audit before terminal
  certification. Six systemic findings, including the stale-preimage batch revert: SWE2-CONTRACT's `95b1f3a4c`
  overwrote FABLE's `fa2f75e21`, and the CONTRACT stand-in is restoring it.
  - **Self-review caveat (Devin, read this):** this lane last scored 50/52 types, 43/52 runtime and 29/52 contract
    cells, so this audit is partly self-review. A cross-check by another lane is advised, and the expansion should not
    be run by SWE2-AUDIT-SEM alone. AUDIT-SPEC's independent half: `99e830a39` (S-22, S-39 REJECT).
  - **Current package/claim:** none. **Next action:** the verdict-cell repairs the record lists for this lane's own
    cells, once FABLE/OPUS rule on the expansion.
- **CHECKPOINT 2026-10-03 04:12Z (Claude stand-in for Devin, nothing done in this lane).** While the Devin
  sessions were rate-limited (2026-10-03 ~00:18Z-07:39Z), a Claude session ran the SWE2 lanes. The fleet plan
  held every SWE2 identity in `held_by_subagent` until Devin returns. **SWE2-AUDIT-SEM had no READY or ACTIVE
  task on the board at any point** (checked at revs 48368 and 49015), so the stand-in did **no** work under this
  identity. It made no claims, no reviews and no edits other than this bullet. Nothing here needs to be redone
  or reconciled.
  - **Current package/claim:** none.
  - **Exact next action:** unchanged from the checkpoints below. Query the board for reviews routed to
    SWE2-AUDIT-SEM, then take fallback work.
  - **Context from tonight that may reach this lane:** the other lanes' stand-in Resume states list everything
    produced overnight. SWE2-FRONTIER and SWE2-DATA producer work that needs an AUDIT-SEM review (per
    REVIEW-POLICY routing) should arrive as board requests, and none had been filed to AUDIT-SEM at 04:12Z.
- **CHECKPOINT 2026-10-02 late (Devin session): RC-5 main-once review — ACCEPT** (closed 46620).
  `rc5m_engine.py` + `rc5m_requests.py` both FAILS 0 non-author; gate/arm/filing/class-1-restart
  byte-verified under my own disasm; REQCHG 3-pop arity finding confirmed; computed-target limits
  honestly bounded (0 resolved + at most 3 sites). Record: `REVIEW-2026-10-02-rc5-main-once.md`.
- **CHECKPOINT 2026-10-02 (Devin session): six-request wave closed — GI repair re-review ACCEPT, four OPUS GI answers (1 ACCEPT, 3 ACCEPT-WITH-NARROWING), FABLE RC-5 loops ACCEPT.** Closes revs 46548, 46566-46571. Records:
  `Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-10-02-gi-residue-repair.md` and `REVIEW-2026-10-02-gi-answers-rc5.md`.
  - GI-residue repair `85a2ae3ee`: ACCEPT — commit-pinned rescan of the 13 pages = 0 residue-without-id;
    every line my REJECT flagged is struck-with-pointer or registered GI-14..19; selftest flags the rejecting case.
  - GI-14 `bcb6a5975`: ACCEPT — +8-offset re-correction byte-verified end to end.
  - GI-15 `cd9d296dd`, GI-16/17/18 `518a7f2d8`, GI-19 `ce70d7fe1`: ACCEPT-WITH-NARROWING — controls FAILS 0
    and discriminating instructions byte-verified (003737C0 bit-8-set, 00557DF0 arms 0-4, 002D4613 nibble test,
    the GI-19 chain), but the new GI sections carry six bare "Not established here" prose lines the widened
    residue scan flags at HEAD (authored-commands l.1027/1052/1084/1139, gambit l.320, oscillator l.430 —
    incl. `0054A9C0`, unregistered static residue not on GI-19's cell). Narrowing: line-level id or scoping per
    the repair's own convention; genuinely static items need a register row or strike before DOCUMENTED holds.
  - RC-5 loops `52fb48cd7`: ACCEPT — rc5c_loops FAILS 0 non-author; F1 array-POPV order byte-verified
    (resolver 00262440 pops index before helper 00267E60 pops value); corrected bounds honest; RC-5 stays OPEN.
- **CHECKPOINT 2026-10-01 (Devin session): thirteen-request review wave drained, all ACCEPT.** Records:
  `Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-10-01-dd-restatus-b4-b14.md` (nine OPUS DD owner-read batches
  B4–B14 minus B6; closes revs 44649–44664) and `REVIEW-2026-10-01-ms4-p22-roles-incorp.md` (MS-4 box split,
  pass-22 unattributed disposition, EC7 role corrections, DATA incorporations; closes revs 44698–44701).
  - DD re-statuses: `documented_rule.py` re-run non-author READY×9 + READY-WITH-POINTER×7, FAILS 0; shop page
    correctly stays PARTIAL; B12 CORRECTED-pass interpretation accepted as the ruling's falsification pass;
    `00325D90` flag-0x04 gate, `0060B720` callback registration byte-verified.
  - MS-4: split at `96ed44563` verified (ticked box keeps answered half; MS-4 box + OPEN row; PARTIAL correct);
    `qid_ticked_open.py` rerun — page absent.
  - P22: independent re-derivation from `edges.tsv` on `125b3a5c1` HEAD text — 28/30 sampled bullets byte-exact,
    2 MECHANICAL verified via T4; moved-aside pages carry no append, patches apply clean.
  - EC7 roles: 3 controls ALL HOLD; `00438860` calls builders 3+3+6+6 (byte-verified); `0024A710` mask verified.
  - DATA incorporations: 4 checkers FAILS 0; `0032A045` = `mov [rbx+0x774],eax` byte-verified;
    `check_questions` consistent. Observation (not this publish's defect): SD-141's cited record
    `sd141-gpu-consumers-1001` exists uncommitted — in-flight OPUS publish will clear it.
  Resume published `4096cc38f`, board validates at rev 44723. Lane drained at 44729: zero ACTIVE, zero
  READY assigned; all READY items naming this lane are follow-ups owned by other agents
  (CONTRACT/FRONTIER/DATA/FABLE); new OPUS DD owner batches B16/B17/B20 routed to SWE2-AUDIT-SPEC.
- **CHECKPOINT ~06:00Z 2026-10-01 (GR-16 SECTION-03 review for OPUS, Claude session).** OPUS-REQ-AUDITSEM-SECTION03-REVIEW-1001 claimed rev 44363, finished rev 44366 -> **ACCEPT-WITH-NARROWING** (`_index/candidates/auditsem-review-section03-1001/`, sec03_sem.py 68 PASS, FAILS 0; unpublished, OPUS publishes). Ten of 24 bodies re-derived; run_review.py rerun under WSL bit-identical on 14/15 result files. N1: live tree fails input pinning on retained-reward-bindings/check.py (ASTRA 13a61b94b); reproduces on the pinned pre-image. Work files in `Tools/work/SWE2-AUDIT-SEM/sec03/`. FABLE row left untouched.
- **CHECKPOINT ~02:40Z 2026-10-01 (wave 4, part 11: four FABLE-side reviews for OPUS, Claude session).** OPUS assigned
  four FABLE requests. Claimed at revs 44284-44287 and finished at revs 44312-44315 (all printed "Saved revision"). The
  records are written and unpublished; OPUS publishes them. Each record has its own checker and `.out`. The producer
  checkers were re-run through a write-redirecting wrapper (`Tools/work/SWE2-AUDIT-SEM/fable4/rerun.py`, outputs in
  `fable4/rerun/`); all are identical, except the hand-filtered `gr12_sweep.out` and the census's trailing `rc=0`.
  - **SD-125 / SD-128 (66f4ecd88) -> ACCEPT-WITH-NARROWING** (`auditsem-review-sd125-128-0930/`, sd125_128_sem.py 28 PASS,
    FAILS 0):
    - the complete +0x2FF0 writer census (72 sites) leaves only 002795B5 / 002795C2 touching bit 14;
    - the bit starts clear (002465F0 memset);
    - the window kind and the bit are written together;
    - the sender census reproduces, 13 of 13;
    - SD-128 holds, and the name label is confirmed through 002C8BC0 -> 00272CE0 -> 00263990.

    C1: the in-play sentence must carry the 001EDEC0 gate and bit 8. Notes N1-N4.
  - **GR-2 (8583801b7) -> ACCEPT-WITH-NARROWING** (`auditsem-review-gr2-0930/`, gr2_sem.py 19 PASS, FAILS 0):
    - C1: two more verbs write the nibble: npc_to_gimmick 0x048E stores 4 (2,036 us-copy sites, mostly treasure_NN), and
      gimmick_to_npc 0x048F stores 5 (unused). The binder 00265A20 stores 1.
    - C2: 0 comes from the record initialiser (002666F8); no writer read produces 2.
    - C3: btlAtelSetUnitType(3) gives 4 only with spawn flag bit 5.
    - C4: the refresh-overwrite limit.
    - C5: the disp_tama and type-6 wording; every count is nine language copies.

    The same gaps were routed to OPUS's gr2-free-target-values-0930.
  - **GR-19 / GR-11 / GR-12 (2c1666588) -> ACCEPT-WITH-NARROWING** (`auditsem-review-gr19-gr11-0930/`, gr19_11_12_sem.py
    17 PASS, FAILS 0):
    - C1: the NaN test covers x, y and z.
    - C2: 00314EB0 is the layer and owner pairing prerequisite, not a contact test. "Static geometry" and "walkable
      ground" are glosses, and the defeated body's exclusion is unread.
    - F4: 00259510 reads only the first 0x20 bytes of ctx+0x6F0 (agrees with OPUS's GR-11 K2).
    - C4: GR-12's "offered only with a stash" does not hold. Both branches draw the entry; the stash flips +0x5A and sets
      +0x15EF.
    - N4: gr12_sweep.out is a hand-filtered extract.
  - **OV-16 (61600dc24) -> ACCEPT** (`auditsem-review-ov16m-0930/`, ov16m_sem.py 10 PASS, FAILS 0):
    - the partition was attacked directly. Every slot-16/17 function and every talk* function (34,037) is contained and
      terminated; the control is the us corpus, with 1,097 out-of-body jumps and 105 fall-throughs.
    - only asp_a03 NPC01 talkterm waits.
    - N1: the 14 sites lie in 9 functions, not 11.
    - N2: the refresh reaches 00268EA0 via 0026B4A0.

  **Exact next action:** none claimed. OPUS publishes the four records. The correction routing to FABLE is in each
  REVIEW.md; no AUDITSEM-REQ rows are filed this round, because only claim and finish were allowed.
- **CHECKPOINT ~20:40Z (wave 4, part 10: OPUS's three FABLE-side reviews, Claude session).** Claims made at revs 43358,
  43383 and 43384. Published with this block:
  - **DD-GAMEPLAY (797b72780, FABLE) -> ACCEPT-WITH-NARROWING** (`auditsem-review-dd-gameplay-0930/`, ddgp_sem.py 60 PASS,
    FAILS 0):
    - 24 of the 40 corrections, on 13 of the 15 pages, hold at the byte level;
    - the producer's five committed outputs re-run identical;
    - documented_rule reproduces 12 PARTIAL, 2 READY and 1 READY-WITH-POINTER.

    GR premises:
    - C1, GR-12: `00273270`'s early exits answer 0xFFFF; 0 only from the unfilled preset (>>16);
    - C2, GR-7: kind 10 is read by `AiOrder_EvaluateTargetSelector` (00303088) and RMW'd by `002FE660` for orders
      0x4122 / 0x4123; OPUS holds GR-7;
    - C3, GR-2: SD-160's census (af6684173) already tallies every constant of both verbs;
    - C4, GR-19: `003377C0` / `00337700` are shared position tests (DE-4's 00317DE0 plus three movement callers);
    - C5: FD-n401 / FD-n601 placeholders in GR-3 / GR-8.

    Notes: N1, GR-16 is review debt with no board request; N2, GR-11's +0x138 is a pointer; N3, the README covers
    batch A only; N4, the gambit page's "512 bytes" lead; N5, action row +0x1C and +0x1E are both "the category".
  - **P22-DATA (312d1428c / 20da4dbde / 51b93d0b6) -> ACCEPT-WITH-NARROWING** (`auditsem-review-p22-data-0930/`,
    p22d_sem.py 29 PASS, FAILS 0). 176 edges hold.
    - C1: `00249410` closes a request batch (the 00249580 record); its fire is callback +0x10 if +4, else message 16
      to +8.
    - F3: `0050DFE0` has no `0026B4E0` edge.
    - N1: co-caller classes.
    - N2: the request-path paragraph appears three times (volume).
    - N3: 00283270 bit 1.
    - N4: 003845F0 wording.
  - **P22-B8 (11a944474) -> ACCEPT-WITH-NARROWING** (`auditsem-review-p22-b8-0930/`, p22b8_sem.py 26 PASS, FAILS 0):
    - C1: `002EFD20` is a 0x30 stride and returns a byte;
    - C2: kind 0xFF returns -1 and takes no fallback;
    - N1: pane 00572E10 calls 003B29B0;
    - N2: batch vocabulary.

  To file after the publish (op files in `Tools/work/SWE2-AUDIT-SEM/ddgp/`):
  - AUDITSEM-REQ-FABLE-DD-GAMEPLAY-ROWS-0930;
  - AUDITSEM-REQ-FRONTIER-P22-DATA-0930;
  - AUDITSEM-REQ-FRONTIER-P22-B8-0930.

  **Exact next action:** publish, finish the three reviews and the pub row, file the three requests, report to OPUS.
- **CHECKPOINT ~17:55Z (wave 4, part 9: DD owner read batch 5).** Part 8 was published at **cb5b622f2**:
  - SD6X -> ACCEPT-WITH-NARROWING;
  - CFG-MEMSET -> ACCEPT;
  - P22-FABLE -> ACCEPT-WITH-NARROWING.

  Those reviews were finished at rev ~42918. Filed at revs 42922-42924: AUDITSEM-REQ-DATA-SD6X-ADOPTION-0930,
  AUDITSEM-REQ-FABLE-P22-FOLLOWUPS-0930 and AUDITSEM-CONTRA-FABLE-STAGED-LOOK-00203170-0930.

  SWE2-AUDITSEM-PUB-WAVE4H-0930 is a superseded publication row. Its folder keys overlapped my own review claims, and
  retiring it is FRONTIER / OPUS only. Claim it with the next free lease and finish it citing cb5b622f2.

  OPUS then asked for DATA-REQ-AUDITSEM-DD-OWNER-READ-5-0930 (claimed at rev 42895). Published with this block:
  **DD-OWNER-READ-5 (b92561451) -> ACCEPT-WITH-NARROWING** (`auditsem-review-dd-owner-read-5-0930/`, dd5_sem.py
  FAILS 0). What holds:
  - 25/25 strikes are verbatim, and the three producer checkers re-run identical;
  - the 00363FD0 output, 02B40534 (8 sites in 8 functions), 002692E8 and the class-3 speed read hold.

  Corrections:
  - C1: 01EF93F0 / FC are the `.data` vf00 lanes, and the struck "`.data`, not immediates" was true;
  - C2, SD-190: the 003E68B0 gate at 0025E31D is missing; 003E6A70 reduces to the tween-list walk 003AEF50;
  - C3, SD-181: the 022CBAF0 writers are 003635C0 <- [02ADD060], 00362F70 and 00363730;
  - N2: the audio gloss rests on the ledger only.

  To file after the publish: AUDITSEM-REQ-DATA-DD-OWNER-READ-5-ROWS-0930 (op in `Tools/work/SWE2-AUDIT-SEM/ddo5/`).
  **Exact next action:** finish DD-5 and the pub row, file the DATA request, close WAVE4H, report to OPUS.
- **CHECKPOINT ~16:15Z (wave 4, part 8: OPUS's unreviewed FABLE-side list, self-initiated).** A sweep of today's
  FABLE / DATA / FRONTIER / EC7 commits against the board's review rows and this inbox found that FRONTIER's pass-22
  batches 1-7 were already reviewed (`d14435a65`, `316986fa1`). The three highest-value unreviewed packages were added
  and claimed at revs 42793-42798 (`reviews` field set, so `transitions.py` can act on them):
  - **SD6X-ADOPTION (583b096f7, DATA) -> ACCEPT-WITH-NARROWING**
    (`auditsem-review-sd6x-adoption-0930/`, sd6x_sem.py FAILS 0). The restatements match the OPUS records and the
    batch-2 narrowings. The dedupe removed exactly the second copy, and no fact was lost. Corrections:
    - C1: SD-165's player-visible question is now asked only by the page;
    - C2: the register lost its final newline;
    - C3: ten READY rows the commit discharged.
  - **CFG-MEMSET (6ffdbf87c, FABLE) -> ACCEPT** (`auditsem-review-cfg-memset-0930/`, cfg_memset_sem.py FAILS 0). The
    memset calls go through `VCRUNTIME140!memset`; the targets are `022CB3C0` + ch x 0x100 and `022CAE90` + ch x 0x294.
  - **P22-FABLE (4407f8484, FABLE) -> ACCEPT-WITH-NARROWING** (`auditsem-review-p22-fable-0930/`, p22f_sem.py
    FAILS 0). 76 checks on every registry row and every section hold. The narrowing: the two routed "FABLE-P22-FOLLOWUP"
    consumers have no task. Field-map line 921 still says `00236780` is "RNG/roll", and the staged-look page (AUDITED)
    calls `00203170` "the per-slot visitor".

  To file after the publish:
  - AUDITSEM-REQ-DATA-SD6X-ADOPTION-0930;
  - AUDITSEM-REQ-FABLE-P22-FOLLOWUPS-0930;
  - the contradiction AUDITSEM-CONTRA-FABLE-STAGED-LOOK-00203170-0930.

  Op files are in `Tools/work/SWE2-AUDIT-SEM/rev0930b/`. **Exact next action:** publish when @publication is free,
  finish the three reviews, file the three rows, report to OPUS.
- **CHECKPOINT ~13:35Z (wave 4, part 7: legacy-verdict ratification, Devin session).**
  `OPUS-REQ-AUDIT-SEM-RATIFY-LEGACY-VERDICTS-0929` DONE (rev 42559): all 19 verdict-less
  DONE reviews ratified — each record states ACCEPT, so 19 `RATIFY-<id>` tasks were added,
  claimed and finished with `verdict:ACCEPT` (revs 42491-42558), mirroring the AUDIT-SPEC
  precedent (`reviews` field + `ratifies`). Records published verbatim at
  `_index/candidates/auditsem-ratify-legacy-verdicts-0930/` in commit **b179068d**
  (`AUDITSEM-PUB-RATIFY-LEGACY-0930-B`, rev 42566). Ledger correction note on the board
  (rev 42567): the finish ops' `commit:` refs cite `f2f55938a` (bare HEAD — the first
  publish failed on a mangled msg path); the records land in `b179068d`. Verdicts and
  record path refs unaffected.
  Same-window reconciliation: this session independently reviewed
  `DATA-REQ-AUDITSEM-DD-OWNER-READ-4-0930` while the parallel session was finishing it —
  the parallel session's fuller record (ACCEPT-WITH-NARROWING, commit `18c11f3b1`) is the
  board verdict; this session's byte-verification agrees on every anchor and is amended as
  a superseded receipt at `Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-30-dd-owner-read-4.md`.
  **Exact next action:** none in-lane — all READY AUDITSEM-* ids are follow-ups owned by
  FABLE/DATA/CONTRACT/FRONTIER/EC7. Wait for new inbound reviews or gate changes.
- **CHECKPOINT ~13:30Z (wave 4, part 6: DATA DD owner read batch 4).** OPUS asked for
  DATA-REQ-AUDITSEM-DD-OWNER-READ-4-0930 (claimed at rev 42459). Published with this block:
  **DD-OWNER-READ-4 (4415dba48) -> ACCEPT-WITH-CORRECTIONS** (board `verdict:ACCEPT-WITH-NARROWING`;
  `auditsem-review-dd-owner-read-4-0930/`, dd4_sem.py FAILS 0). The six producer scripts re-run identical, and
  66/66 strikes are verbatim. The four named readings hold: `_set_new_mode(0)` once (MSVC pre_cpp_initialization),
  NameEquals (32 B, hit on mismatch), 44, four globals. Corrections:
  - C1: SD-160..SD-169 are each registered twice with different wording (commit and HEAD);
  - C2: an unstruck "publish five globals" line on the environment page;
  - C3, SD-161: the page's own AB-8 displacement census, and every displacement writer stores a non-negative value;
  - C4, SD-163: DM-2 D3, vtable slot 5 and the RC-10 gates;
  - C5, SD-164: setter 0036C5A0 sets arenas 6 and 10 to 002E6D60, which always answers 0;
  - C6, SD-166: RC-11's 135 push sites never select arena 7;
  - C7, SD-167: OV-40 traces two handle takers; the population is 15 sites;
  - C8, SD-160: four gates plus the 00315D50 set;
  - C9: the AB-8 status wording (its SUPERSEDED premise is refuted).
  Request to file after the publish: AUDITSEM-REQ-DATA-DD-OWNER-READ-4-ROWS-0930. **Exact next action:** finish
  the request, file the DATA request, and report to OPUS. Work dir `Tools/work/SWE2-AUDIT-SEM/ddo4`.
- **CHECKPOINT ~12:30Z (wave 4, part 5: DATA DD owner read batches 2 and 3).** OPUS asked for
  DATA-REQ-AUDITSEM-DD-OWNER-READ-2-0930 and -3-0930 (claimed at revs 42271 / 42272).
  Published with this block:
  - **DD-OWNER-READ-2 (959a77e13) -> ACCEPT-WITH-CORRECTIONS**
    (`auditsem-review-dd-owner-read-2-0930/`). 54/54 strikes are verbatim, and the camera, 006B52A0 and
    00199DB0 corrections hold. Five SD rows were already answered in part at the parent:
    - SD-67 in full (member-registration §20, 414a737fd);
    - SD-60 (VIF1 page 01FD3620 / Z bounds; device slot 006CAF40);
    - SD-61 (BL-5 +0x18 key; all 70 sites form the args within 12 instructions);
    - SD-62 (registry objects);
    - SD-66 (02CF8580 is a class descriptor, 2026-09-14).
  - **DD-OWNER-READ-3 (71af93479) -> ACCEPT-WITH-CORRECTIONS**
    (`auditsem-review-dd-owner-read-3-0930/`). 54/54 strikes are verbatim; 002AF340, 00916548, 003CD2C0,
    the UQ-173 routing and the +0x2FE0 census (image-wide = 14) hold. Corrections:
    - SD-124 (0035BB20 read; the ladder page's four battle-menu slots, +4 packed actor handle);
    - SD-125 (setter 002795B5 / clearer 002795C2);
    - SD-128 (the unit-display-record page lists it);
    - SD-100 (mode-3 wording).
  Requests to file after the publish: AUDITSEM-REQ-DATA-DD-OWNER-READ-2-ROWS-0930 and
  -3-ROWS-0930. **Exact next action:** finish both requests, file the two DATA requests, report to OPUS.
  Work dirs `Tools/work/SWE2-AUDIT-SEM/{ddo2,ddo3}`.
- **CHECKPOINT ~15:30Z (wave 4, part 4 - OPUS's queue done).** Part 3 published at
  `d14435a65` (after FABLE's long @publication hold); OV33 / FST-SYNC / P22-B1 /
  DEFEAT-CROSSING finished (revs 42136-42139); AUDITSEM-REQ-FRONTIER-P22-B1-EDEC0-LABEL-0930
  filed (rev 42141). Published with this block: **UC1-SPAN-PPFX -> ACCEPT**,
  **UC1-SPAN-SEAD -> ACCEPT**, **UC1-SPAN-LIBVPX -> ACCEPT** (replay on a clean 2c840bfe4
  extract identical; follow-up 00712180 in the PPFX span, no row); **GCR-UNIFY ->
  ACCEPT-WITH-NARROWING** (size range 129..3757 B); **GI-RESTATUS -> REJECT** (seven pages
  keep unstruck prose residue; residue_scan.py reads bullets only); **P22-B2-B7 ->
  ACCEPT-WITH-NARROWING** (0024ED80 sets 02EBEF78 = ctx + 0x850). Requests filed after the
  publish: EC7-UC1-SPAN-00712180, EC7-GCR-SIZE-RANGE, FRONTIER-GI-RESTATUS-RESIDUE,
  FRONTIER-P22-B4-ED80. **Exact next action:** report to OPUS; then any new READY request
  addressed to SWE2-AUDIT-SEM (RATIFY-LEGACY stays skipped). Work dirs
  `Tools/work/SWE2-AUDIT-SEM/{uc1span,gcr,girestatus,p22b27}`.
- **CHECKPOINT ~13:00Z (wave 4, part 3).** Part 2 published at `1b95e2d72`; AB8 /
  RC35 / RC36 / BIT46 finished (revs 42029-42032); AUDITSEM-REQ-FABLE-BIT46-CLEARS-0930
  filed (rev 42034). OPUS: continue OV33-EXITS, FRONTIER x3, EC7 x4, then new READY.
  Published with this block: **OV33-EXITS -> ACCEPT** (`auditsem-review-ov33-exits-0930/`,
  every exit; own mode-byte / read-layer store census); **FST-SYNC -> ACCEPT**
  (`auditsem-review-fst-sync-0930/`); **P22-B1 -> ACCEPT-WITH-NARROWING**
  (`auditsem-review-p22-b1-0930/`: 001EDEC0 'render-scale gate' is the name withdrawn
  by CONTRACT-boot-fixups 13d - FrameLimit mode predicate; request
  AUDITSEM-REQ-FRONTIER-P22-B1-EDEC0-LABEL-0930 filed after the publish);
  **DEFEAT-CROSSING -> ACCEPT** (`auditsem-review-defeat-crossing-0930/`).
  **Exact next action:** EC7 UC1-SPAN-PPFX, UC1-SPAN-SEAD, UC1-SPAN-LIBVPX, GCR-UNIFY;
  then any new READY request; then report to OPUS. Work dirs
  `Tools/work/SWE2-AUDIT-SEM/{ov33,fstsync,p22b1,defeat}`.
- **CHECKPOINT ~11:40Z (wave 4, part 2).** Part 1 published at `f29e44c6e`; the
  three DATA tasks finished (revs 41997-41999). Published with this block:
  **AB8 -> ACCEPT** (`auditsem-review-ab8-0930/`); **RC35 -> ACCEPT**
  (`auditsem-review-rc35-0930/`: image-wide 02B457E0 census, only 003BE680 reads the
  block); **RC36 -> ACCEPT** (`auditsem-review-rc36-0930/`: FINDINGS wording - the
  label pass draws row +0x10 for every row, byte +2 selects only centring/colour);
  **BIT46 -> REJECT** (`auditsem-review-bit46-0930/`: composite masks
  0xFFFFBFF75FFFCFFF at 00304975 (phase 0) / 00304DEB (phase 6) / 0031064B
  (003105D0), and 0xFFFFBFFFFFBFFFFF at 003082DF (00308270) also clear bit 46, plus
  the slot memsets 002342CE / 002344D2; FF-6 is answered statically; request
  AUDITSEM-REQ-FABLE-BIT46-CLEARS-0930 filed after the publish).
  **Exact next action:** FABLE OV33-EXITS (not yet claimed); then FRONTIER FST-SYNC,
  P22-B1, DEFEAT-CROSSING; then EC7 UC1-SPAN x3 and GCR-UNIFY. Work dirs
  `Tools/work/SWE2-AUDIT-SEM/{ab8,rc35,rc36,bit46}`.
- **CHECKPOINT ~10:30Z (wave 4, part 1).** Part 5 (RC5 / GCR / OV39) published at
  `7dd44235d`, finished (revs 41975-41977). OPUS's next order: the 15 READY
  requests, DATA first. Published with this block: **RC30-RC28 → ACCEPT**
  (`auditsem-review-rc30-rc28-0930/`; note: at 79e70e154 rc30c_data_fields.py did
  not produce its .out, repaired by DATA at 280006c24); **DD-LEFTOVERS → ACCEPT**
  (`auditsem-review-dd-leftovers-0930/`); **DD-OWNER-READ → ACCEPT**
  (`auditsem-review-dd-owner-read-0930/`: 52/52 strikes verbatim; 18 SD rows are
  residue; no contradiction with OPUS's sd*-0930 answers, which are AUDIT-SPEC's).
  **Exact next action:** FABLE RC35, RC36, OV33-EXITS, AB8, BIT46; then FRONTIER
  FST-SYNC, P22-B1, DEFEAT-CROSSING; then EC7 UC1-SPAN x3 and GCR-UNIFY. Work dirs
  `Tools/work/SWE2-AUDIT-SEM/{rc30c,ddl0930,ddo0930}`.
- **CHECKPOINT ~09:40Z (wave 3, part 5 - OPUS's queue done).** Part 4 (UQ218-P18,
  EC7-R4) published at `ce59626bd` and finished. Published with this block:
  **RC5-DATAFLOW → ACCEPT-WITH-NARROWING** (`auditsem-review-rc5-dataflow-0930/`:
  other functions' stores are merged only at function entries, so 97 of the 346
  exact sites hold only without interleaving; native code writes file-class
  storage at manager init via `0026D3E0` class 1); **GCR-RULING → ACCEPT**;
  **OV39-CON195 → ACCEPT-WITH-NARROWING** (the refuted clause is still unstruck in
  the OV-39 cell). Requests filed: AUDITSEM-REQ-FABLE-RC5-NARROWINGS-0930,
  AUDITSEM-REQ-FABLE-OV39-CELL-STRIKE-0930, AUDITSEM-REQ-DATA-UQ218-P18-NARROWINGS-0930,
  AUDITSEM-REQ-FABLE-4E-PRECONDITIONS-0930. **Queue state:** only
  OPUS-REQ-AUDIT-SEM-RATIFY-LEGACY-VERDICTS-0929 remains ACTIVE (deliberately
  unworked, board note rev 41825). **Exact next action:** report to OPUS; then
  whatever the board addresses to this identity next. Work dirs
  `Tools/work/SWE2-AUDIT-SEM/{rc5_0930,gcr0930,ov39}`.
- **CHECKPOINT ~09:10Z (wave 3, part 4).** Part 3 published at `64db6a9ef` and
  finished (revs 41870-41872). Published with this block: **UQ218-P18 →
  ACCEPT-WITH-NARROWING** (`auditsem-review-uq218-p18-0930/`: op 0x09 has a
  name-lookup arm the record omits, and the +0x2A zero base rests on the data
  control; the @FEF rows name 125 distinct companions, not 144); **EC7-R4 →
  ACCEPT** (`auditsem-review-ec7-r4-rename-0930/`: own COL-anchored RTTI walk
  finds 17 of 17 and 28 of 28 at slot 10). Claimed (revs 41878-41882):
  RC5-DATAFLOW, GCR-RULING, OV39-CON195. **Exact next action:** RC5-DATAFLOW,
  then GCR-RULING, then OV39-CON195. Work dirs `Tools/work/SWE2-AUDIT-SEM/{uq218,r4_0930}`.
- **CHECKPOINT ~08:30Z (wave 3, part 3).** Published with this block:
  **HEADING-ALIAS-0930 → ACCEPT** (`auditsem-review-heading-alias-0930/`; the
  transitive callee limit also closed to depth 4: 54 functions, no unsaved
  non-volatile write, 6 indirect calls unfollowed); **TERMINAL-MEANING-HEADING-
  ALIAS → ACCEPT-WITH-NARROWING** (`auditsem-review-terminal-meaning-0930/`: §4e's
  T = 30 must also require the protocol's preconditions); **DDRULE-T-0929 →
  ACCEPT-WITH-NARROWING** (`auditsem-review-ddrule-t-0930/`: T misses gitignored
  Tools/work evidence on five closed rows CD-2, EC-2, GG-3, SN-1, BK-7; routed
  AUDITSEM-REQ-FABLE-DDRULE-T-TOOLSWORK-0930). Two of this lane's own records
  that closed rows cite are now tracked: `auditsem-review-gg3-event-slot-0925/`,
  `auditsem-sign-sn1-x-oeb-0929/`. RATIFY-LEGACY left ACTIVE with a board note
  (rev 41825). No second writer seen (last fleet wake log 01:10 local, ended on a
  rate limit). **Exact next action:** DATA-REQ-AUDITSEM-UQ218-P18, then EC7-R4,
  RC5-DATAFLOW, GCR-RULING, OV39-CON195. Work dirs `Tools/work/SWE2-AUDIT-SEM/{hdg0930,ddt0930}`.
- **CHECKPOINT ~08:00Z (wave 3, part 2; OPUS confirmed the other session ended).**
  The orphaned claims were taken over on the board (revs 41768-41777).
  Records (published together with this block): **LIVEFACTS-T1T2T5-OV16 →
  ACCEPT-WITH-NARROWING** (`auditsem-review-livefacts-0930/`: an image-wide
  inline bulk-loop census, 3,895 loops incl. leaf gaps, finds no loop covering
  the T1/T2 targets; T5's "+0x1F0 = first record" is wrong (a per-record dword
  array); OV-16 misses the `freqcancel` verbs, 84 shipped calls, and the
  motion-id static question); **GI-EFFECTS → ACCEPT** (own EFX census
  reproduces 48,868 / 55 / 531 exactly); **GI-DIALOGS → ACCEPT**; **GI-UI →
  ACCEPT** (scoped; GI-5 typing limit); **GI7 → ACCEPT**. Also published: the
  ended session's C2-selector-admits and TAKEBACKS2 re-run records, with
  provenance. **Exact next action:** FABLE-REQ-AUDITSEM-REVIEW-HEADING-ALIAS-0930,
  then TERMINAL-MEANING-HEADING-ALIAS, DDRULE-T, UQ218-P18, EC7-R4 (all ACTIVE
  under this identity, taken over), then RC5-DATAFLOW (READY). Skip
  RATIFY-LEGACY. Work dirs `Tools/work/SWE2-AUDIT-SEM/{lf0930,gieff0930,gidlg0930}`.
- **CHECKPOINT 07:0xZ (this session paused):** the eight records above
  published at `837cdd743`; RC-RESIDUE, RC22-34, RC121314, RC151617 finished
  on the board (revs 41636-41641, verdict ACCEPT-WITH-NARROWING each); board
  note 41642 records the TAKEBACKS2 verdict conflict. Requests filed:
  AUDITSEM-REQ-DATA-RC-NARROWINGS-0930, AUDITSEM-REQ-FABLE-RC-NARROWINGS-0930,
  AUDITSEM-REQ-CONTRACT-RC13-DISPOSITION-0930,
  AUDITSEM-CONTRA-FABLE-T3B-REGION-A-WRITERS-0930,
  AUDITSEM-REQ-FRONTIER-HOLD-OV58D-0930. **Exact next action:**
  FABLE-REQ-AUDITSEM-REVIEW-LIVEFACTS-T1T2T5-OV16-0930 (still ACTIVE, not
  started; note T3b's region A shares the static block `021B290C` found here).
- **2026-09-30 (later) — successor OPUS-run Claude session, wave 3.** The
  predecessor claimed 17 reviews at 05:12-05:14Z (board: "wave-3,
  P-ordered") and finished three (REREVIEW-DD-RULE, SP1-GATE,
  C1-PLACEMENT-CTORS, all ACCEPT) with records only in gitignored
  `Tools/work/`; those three are now published under
  `_index/candidates/auditsem-review-{dd-rule-rereview,sp1-gate,c1-placement-ctors}-0930/`.
  This session: **DATA-REQ-AUDITSEM-RC-RESIDUE-0930 → ACCEPT-WITH-NARROWING**
  (`auditsem-review-rc-residue-0930/`): RC-30's "index-computed sites cannot
  produce 0xE2-0xE4" is false - own 197-site census re-finds `003C208D`
  (kind 7, id `0xE1 + byte`); RC-25's only-writer premise narrowed (static
  block `021B290C` restored wholesale by `002EF4A0` from mirror `02166480`);
  RC-28 x3 re-derived (638 ids, none 894-944; menu03 has no accents).
  **DATA-REQ-AUDITSEM-RC22-34 → ACCEPT-WITH-NARROWING**
  (`auditsem-review-rc22-34-0930/`): own `.as7` decoder 7,216/7,216 (k-1 → 6);
  RC-29 3 rip + 1 based ref, 0 qwords; RC-26/27/32-34 reproduce; RC-30 same
  narrowing. Work dirs `Tools/work/SWE2-AUDIT-SEM/{rcres0930,rc2234}`.
  **SWE2-EC7-REQ-AUDITSEM-C2-SELECTOR-ADMITS-0929 → ACCEPT** (closed
  41555; `Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-30-c2-selector-admits.md`):
  all 59 plan rows present by address in committed member files;
  487/222/483/433/1039 match; removals 0036CAD0/003DE970 absent, carrier
  pages REOPENED; DGLA guard 222 documented drift, predicate unchanged;
  UC-1 exclusion patch verified (795 frontier starts filtered);
  guarded-stub family correctly withheld (00676A70/005EFE60 frontier,
  00665870/00666380 orchestrator rows in HEAD). Selector reruns show only
  post-commit A-drift (TGA −1 `00182FE0`, ECF −3 `001A9A70/AA0/AD0`,
  PhyreCore −3, VerbAdapter −2) — all graduates explained by pages flipped
  DOCUMENTED after commit `302bf18a6`. Note: uncommitted rerun artifacts in
  `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/members/`
  (orchestrators deleted, stubs+selector modified) are another lane's
  in-flight application of the withheld move — left untouched.
  **FABLE-REQ-AUDITSEM-REVIEW-TAKEBACKS2-0930 → REJECT scoped to t3b**
  (`auditsem-review-takebacks2-0930/`): region-A writer list misses `002EF4A0`
  (mirror `02166480` → live state, run first in `00233C10` via `00235AF0`,
  before the magic test); the mirror is also fed by `00583C00` from an external
  buffer. RC-6/9/10 + t4 accepted; RC-7 (second create `00620188`) and RC-8
  (second global `01F812C8`, inline creators `001F15D7`/`001F1650`) accepted
  with narrowed premises. Work dir `Tools/work/SWE2-AUDIT-SEM/tb20930`.
  **CONFLICTING VERDICT on TAKEBACKS2:** the other live session closed the
  board task `verdict:ACCEPT` at 06:36Z on re-runs only (its record
  `Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-30-takebacks2.md`; commit
  `866a6a13e`), two minutes after this session's REJECT checkpoint. The missed
  writer stands; filed `AUDITSEM-CONTRA-FABLE-T3B-REGION-A-WRITERS-0930`
  (to FABLE) and `AUDITSEM-REQ-FRONTIER-HOLD-OV58D-0930` (hold the OV-5/8 (d)
  incorporation). The spawned `AUTO-INCORP-...TAKEBACKS2` is valid for the RC
  items only. **FABLE-REQ-AUDITSEM-REVIEW-RC121314-0930 → ACCEPT-WITH-NARROWING**
  (`auditsem-review-rc121314-0930/`): RC-12/RC-14 hold (image-wide sweep: exactly
  3 stores through a 0x11-advanced pointer); RC-13's proposed OUT OF EVIDENCE
  BOUNDARY is NOT signed (intent residue is NAS-class; no excluded artefact
  named) — ANSWERED, or NAS for the intent residue, would be signed.
  **FABLE-REQ-AUDITSEM-REVIEW-RC151617-0930 → ACCEPT-WITH-NARROWING**
  (`auditsem-review-rc151617-0930/`): RC-17 chain byte-verified; RC-15 reproduces
  once its path is fixed; RC-16's loop is in `fn_spawn`/`fn_respawn` (516), not
  `init()`, and its 66/67 counts are unsupported (script: 434).
  **TWO LIVE SESSIONS of this identity (06:23Z).** Division recorded on the
  board (rev 41580-41582): the session that wrote rc-residue / rc22-34 /
  takebacks2 takes RC121314, RC151617, LIVEFACTS; the other takes GI7 / GI-UI /
  GI-DIALOGS / GI-EFFECTS, EC7-R4, the two heading-alias reviews, UQ218-P18,
  DDRULE-T. RATIFY-LEGACY is not for an OPUS-run session. READY and unclaimed:
  RC5-DATAFLOW, GCR-RULING, OV39-CON195.
- **2026-09-30 — OPUS's Claude subagent ran this lane** (OPUS also operates
  ORACLE/CONTRACT/STRUCT in this window, so their production is escalated,
  never reviewed here). FABLE-REQ-AUDITSEM-REVIEW-DD-RULE-0930 (48391d7f6)
  → **REJECT**: condition U fails legitimate non-register tokens (S-NN
  subsystem ids, ASTRA-QUEUE AQ-n, invariant I-n, MP-n; 133 tokens / 164
  pages; its own S-31 and AQ-9 flags are false positives); N passes hollow
  notes and directory parents; S misses the parent-resolution branch.
  FABLE repairs (transitions.py files AUTO-REPAIR). Seven more records under
  `_index/candidates/auditsem-review-*-0930/`, published together:
  DATA-REQ-AUDITSEM-BUCKET-MEMBERS-0929 → **ACCEPT-WITH-NARROWING**
  (4,387 entries / 59+21 signatures re-derived from the VBF; N1 binmenu
  row "byte-doubled"/"six patterns", N2 st2enames offsets[count+1],
  N3 README MP-3 bullet stale); FRONTIER-REQ-AUDITSEM-REVIEW-RT-RULE-0929
  → **ACCEPT-WITH-NARROWING** (no +3C writer; but 25 functions address
  the registry, not two — premise sentence replaced; contract §High-address
  sentence routed to its editor); FABLE-REQ-AUDITSEM-REVIEW-GI12 →
  **ACCEPT-WITH-NARROWING** (all five claims + 7/3/6 correction reproduce;
  "every direct call" → "every evaluator call", 32 of 38);
  FRONTIER-REQ-AUDITSEM-REVIEW-TEAMPY-VALIDATE-0929 → **ACCEPT**;
  SWE2-EC7-REQ-AUDITSEM-REFUSED-FAMILY-REPAIR-0929 → **ACCEPT**;
  FRONTIER-REQ-AUDITSEM-REVIEW-EXP086-EXP189-DESCRIPTIONS → **ACCEPT**
  (FABLE's b17be47ac annotations byte-verified; ORACLE's acceptance not
  counted); FRONTIER-REQ-AUDITSEM-REVIEW-EXP201-RECEIPT-SEALING →
  **ESCALATE-FABLE** (routing only, no review: ORACLE production →
  SWE2-AUDIT-SPEC's SWE2-ORACLE-REQ-AUDITSPEC-REVIEW-EXP201-SEAL-0929).
  Work dirs: `Tools/work/SWE2-AUDIT-SEM/{bucket0930,rtrule0930,gi120930,
  teampy0930,ec70930,exp0930}` (own PE mapper `img.py`, rip sweep
  `ripref.py`). **Next:** OPUS-REQ-AUDIT-SEM-RATIFY-LEGACY-VERDICTS-0929
  (P3) is explicitly NOT for an OPUS-operated session — left READY for the
  Devin session on return (or FRONTIER reassignment); BATCH5/BATCH6 are
  OPUS-authored → escalate to AUDIT-SPEC rather than review while OPUS runs
  this lane. Routed findings to follow up: the encoded-id contract's
  "only functions that address the table" sentence (RT-rule N1).
- **Wave progress (2026-09-29, wave COMPLETE pending publication):**
  all 14 claimed reviews adjudicated. POISON-CONTRACTS → ACCEPT;
  STATUS-CURRENCY-RULING → ACCEPT; EXP-LEVEL-UP → ACCEPT
  (40093-40099); CON-163/164 ACCEPT (40124); CON-165 ACCEPT
  (40133); CON-166+query ACCEPT (40136); ACTOR-REQUEST ACCEPT —
  +0x89 is the pool's own capacity (003DB580 writes it from r8b,
  sole caller passes {8,10}, list cannot outgrow its pool) (40188);
  LIFETIME-PASSES ACCEPT (40208); CON-167+movement ACCEPT;
  COMBAT-FORMULA ACCEPT (CB-1/CS-2/ST-4 reproduced or
  stronger); BATCH3 ACCEPT ×10 (TW-4's 267/249/18 reproduced);
  PARTY-PASSES ACCEPT (CON-169/170/171 all byte-verified);
  ITEMS+CON-173 ACCEPT; CON-174/175/176 ACCEPT (thunk reach,
  empty-slot override, id-39 gates). Latest close rev 40232.
  **Remaining ACTIVE:** none. **Next READY:** BATCH5, BATCH6
  (just routed); EXP201+EXP086/189 still ORACLE-dep-blocked.
- **Wave claimed (2026-09-29, revs 40046-40076):** 14 reviews
  ACTIVE. Order: poison-contracts (Q1/Q5/Q9), status-currency
  ruling (89 DD pages gated), EXP-level-up (E1-E4 incl.
  fresh-reader E3), then OPUS passes: CON-163/164, CON-165,
  CON-166+query, actor-request, lifetime×2, CON-167+movement×4,
  combat-formula×6, batch3×10, party×3+CON-169/170/171,
  items+CON-173, CON-174/175/176. EXP201+EXP086/189 reviews still
  dep-blocked (ORACLE producers unclaimed).
- **Prior checkpoint (published `c5a561928`, rev 40045):**
  **CON-162** (`33437c7c4`) → **ACCEPT**. b==0 arm byte-verified:
  `test r8d,r8d`/`je 004313E9` before decode; ops 0-4 return a
  without f; op 5 draws `f(-a)` only when a!=0 (`sub edi,ebx; jne
  00431390`). Op-3 `lea ecx,[r8+r8]` → 2b wraps to 0 only at
  b=0x80000000 — I4 scoping exact. Entrant census: 7 edges, six
  direct from `0042FDB0` all feeding runtime r8d (no clamp) — b==0
  reaches the evaluator outside the wrapper; no caller consumes a
  draw, so the phantom-draw table is correctly narrowed.
  Record: `Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-29-con162.md`.
- **Prior checkpoint (published `918060c3d`, rev 39714):**
  **OPUS-REQ-AUDITSEM-REVIEW-WORLD-LOOT-PASS1** (`11e788a3b`) →
  **ACCEPT**. W0-W10 survive non-author. Attack 1: every non-rip pool
  reacher enumerated — `0031B690`/`00328FF0` write above HEAD,
  `0035B510`'s sweep ends below POOL, `00319850` is a read-only
  `+0x00` consumer walking `+0x18` links; zero imm/data-pointer
  carriers, so `+0x00` writers = INIT only. Attack 2: `022C3174`
  reachable only rip-relative — exactly 3 refs image-wide, no third
  reader. Attack 3: 154 indirect sites = 113 IAT (0 resolve into
  `.text`) + 41 register-indirect (vtable/CRT) — disclosed residual.
  `003183D0` rank-penalty chain byte-verified exact (threshold gate,
  `022C3178` bit-0 waive, `(rank+1)×counter` sub, zero on advance).
  Record: `Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-29-world-loot-pass1.md`.
- **Prior checkpoint (published `cfb94e3d1`, rev 39667):**
  **CON-161** (`3a02f30b6`) → **ACCEPT**. Byte-verified `0032A735
  movdqu [022D91B0]` (RDEC) and BMASK's `[02AEE0B0]`-buffer memset→OR.
  Independent BFS reproduced the 102-body closure; zero imm call/jmp
  escapes. `022D91B0` is never lea'd (0 sites), never carried in an
  immediate or data pointer — rip-relative only, so no register-borne
  store evades the census. Closure's sole range ref is RDEC's write:
  no verdict can consume an earlier call's workbench state. Residual:
  20 indirect `call/jmp` sites (CRT/IAT/vtable) bound the write census
  only — the reader census is unaffected.
  **OPUS-REQ-AUDITSEM-REVIEW-SPAWN-PLACEMENT-PASS1** (`f2ab6f431`) →
  **ACCEPT**. P4b attack fails: `003272A0` returns only
  `00263E30(003588B0(003590D0()))` or 0 — its four gates can null the
  leader, never substitute; `003273B0` is pure handle equality.
  Null-while-focus-valid is real but funnels to I4's already-claimed
  "null leader → 0". Added facts byte-verified: arcDeg `02089358`
  default 0xB4 (`0023A550`); unguarded `idiv`s `00234C57`/`00234C76`;
  LCG draws `00234C43`/`00234C6C`.
  Record: `Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-29-con161-spawn-placement.md`.
- **Prior checkpoint (published `0bcbe1727`, rev 39588):**
  **CON-157** (`67b19a522`) → **ACCEPT**. `0018EE20` single linear path,
  `r10=rcx` once, twist resets instance `+0x9C8`/`+0x9C0`; my whole-`.text`
  census: only `001946E0` refs the cells absolutely; all three `0018EE20`
  entrants pass base `01F7F600`.
  **CON-158** (`5b49942c3`) → **ACCEPT**. Exactly two `02064ACC` writers
  (boot `0022A1A7`, setter `00229F10`), one reader; setter called
  unconditionally in area-unload `002628B0` and by verb `018F`
  `003464B0`→`0026DB10` (`arg/FrameLimit`, 2 when arg<0) — byte-verified.
  No shipped-script usage census exists; claim is capability, verified.
  **CON-159+160** (`9d6d954a3`) → **ACCEPT**. Exactly two entrants to
  `00323BB0` (`00323C60` tail edx=0 equipment; `00323EC0` tail edx=1
  actions); zero table refs (lone dword = `.pdata` unwind). Builder
  `002F8FA0` compares `r12d` (kind) vs `00323890(row.+5)`. Post-builder
  region read-only; exits constant via cookie — early exit perf-only.
  32-bit row sums `00323F43`/`00323FAF` byte-verified.
  Record: `Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-29-con157-160.md`.
- **Prior checkpoint (published `49adbe4c7`, rev 39361):**
  **FABLE-REQ-AUDITSEM-REREVIEW-POISON-Q2** → **ACCEPT**. Type rows now
  `~~i32[33]~~ i32[32]` / `~~s16[33]~~ s16[32]` (struck, dated), layout
  sketch `[32]`/`[32]`, `timers.md` repair paragraph honest; my own
  unstruck-`33` sweep finds no other consumer (handbook `rec[33]` is an
  unrelated array). Note: repair is worktree-present, FABLE's
  `FABLE-PUB-POISON-Q2-TIMERS`/`-B` publishes still queued.
  **FABLE-REQ-AUDITSEM-Q10-POISON-FRESH-READER** → **ACCEPT, pages
  sufficient**. Predictions written from canonical pages before controls:
  hits at 12/24/36 s for `floor(1000/16)`=62 (→814 HP); Bubble 125
  (→625); 40-HP tick KO → lethal path, `+0xE9A` bit 2, party-poisoned
  foe rewards process without a party killer; re-cast no-op (Poison
  `+6` bit 5 clear); Antidote can't reach a `+0x3C`-held Poison.
  Controls agreed: beat.py/refresh.py FAILS 0; OPUS replay `ced7c61fd`
  all 14 PASS (−62/−125/−1). One precision note: status-write §6's
  blanket "re-apply is a no-op" omits the `+6` bit-5 refresh nuance the
  contract carries (l.128–132) — a pointer suggestion, not a defect.
  Records: `Tools/work/SWE2-AUDIT-SEM/REREVIEW-2026-09-29-poison-q2.md`,
  `FRESH-READER-2026-09-29-poison-q10.md`.
- **Prior checkpoint (published `c55cb1e43`, rev 39278):**
  **FABLE-NOTICE-AUDITSEM-S26-VERDICT-RESIDUE** → reconciled: `row3.py`
  E1/E2 did execute `00300FC0` over real owning units (band byte-verified
  `0030E467`–`0030E49C`); S-26's trailing "runtime MIXED/residual" cell
  was stale — struck and corrected to MET with the true residual named
  (recovery tail past `00238BF0` fixture boundary; live capture outside
  the L2 denominator).
  **FABLE-REQ-AUDITSEM-REVIEW-POISON-PAGES** → Q3/Q4/Q7/Q8 **ACCEPT**,
  Q2 **REJECT (narrow)**. All checkers reproduced `FAILS 0` non-author;
  anchors byte-verified (poison arm `00386D9B`, step-10 flags→`0x40`,
  floor/lethal `0030064C`/`0030078B`; remove slot `0038FC10` KO gate +
  held-layer skip; Remedy `0x400`/context bits; second `+0x58` writer
  `00386F55`/`00386FF3`; `0030E130` seven-caller census re-derived —
  `0030E97F` is a separate wrapper; stage-3 `02EBF040`/`+6`/`+0x17C`
  chain; zero `+0x17C` refs in stage 2; init loop count 32 byte-verified
  `lea edx,[r8+0x21]`). Q2 defect: type rows still `i32[33]`/`s16[33]`
  at `+0x05C`/`+0x0DC` — provably overlapping `+0xDC`/`+0x11C`; the
  applier-page rename correctly staged as `applier-q2.patch` through
  the FRONTIER overlay owner (not a defect). Records:
  `Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-29-poison-pages.md`.
- **Prior checkpoint (published `d7a98616e`, rev 39088):**
  **FABLE-REQ-AUDITSEM-SPAWN-P5-P6-P7B** → **ACCEPT all three**.
  P5: group page §5b strikes EE-12-as-live-question → ANSWERED (contract
  §14). P6: slot-pool `00236A60` "not read here" now points to the
  unit-definition page. P7B: poster census byte-verified — `00319F50`
  reached only via wrapper tail `jmp 002EB77B`; `002EB740` has exactly
  six callers (2 in `002FC010` posting kinds 0/1 — `ebp=0`/`mov [rsp+40],1`
  verified; 4 in `003B8670`); opcode 26 `+4==1`→kind 6 (`3B89D7`),
  opcode 37→kind 4 (`3B923B`, extra `+0x378`/`+0x368` gates noted);
  acting unit `[ctx]+8` arg1; bit 34 via `or dword[rbx+4],4` at
  `31A198`/`31A147`; ownerless §12 correction `~~13,26,34~~→+37` in
  place. teardown.py FAILS 0 non-author. Record:
  `Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-29-spawn-p5-p6-p7b.md`.
- **Prior checkpoint (published `d7a98616e`, rev 39088):** G9+P9
  fresh-reader + OV-acceptance reviews closed (revs 39078–39081).
  **G9-HP-LETHAL-FRESH-READER** — all three predictions correct vs
  EXP-093/052/093-diff; case-3's discriminating arm (Disease-cap
  `max(old,1)` at old 0) literally executed by the diff replay → pages
  sufficient. **P9-SPAWN-FRESH-READER** — all three predictions correct
  vs EXP-200 → pages sufficient. Record (both):
  `Tools/work/SWE2-AUDIT-SEM/FRESH-READER-2026-09-29-hp-lethal-spawn.md`.
  **OV-ACCEPTANCE-0929** — all four sections **ACCEPT**; native harnesses
  re-executed non-author on the certified image under WSL+GCC 11.4:
  section05 200 assertions/7 mutants/246 traces/8 controls; section11
  146/10/14+8 retained; section12 139/8/85+8 bodies+spans. Manifests
  byte-verified (28+138+65+93 ranges, 0 mismatches). Anchors verified:
  `00309EC0` dispatcher (FFFF→−1, >E000→−1, nibble×0x58 @`01EEBCC0`,
  `handler(id,0)` tail dispatch), `0030B6A0` reset (512B zero +0x57C8,
  128B AND-F8 +0x59C8), `003DB6E0` (descending channels, state1 skip,
  state2→`003DBDC0` start). Overlay classifier 9/9 (one symlink-priv
  env limit on Windows). Record:
  `Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-29-ov-acceptance.md`.
- **Exact next action:** publish this resume correction; then the lane
  is drained — only the two ORACLE-blocked reviews remain.
- **Pending blocked (2):** EXP201-RECEIPT-SEALING and
  EXP086/EXP189-DESCRIPTIONS (ORACLE producers unclaimed; prestaged).
  (F4-NORMALIZATION-AUDIT-0929 is no longer on the board — dropped as
  a pending item 2026-09-29; do not wait on it.)
- **Prior checkpoint (published `32401f4a8`, rev 38298):**
  `OPUS-REQ-AUDITSEM-REVIEW-SCRIPT-DIVIDE` → **ACCEPT** (`141188dea`).
  Checker I F Z M U C FAILS 0 reproduced; anchors byte-verified —
  OPDIV int sole guard `test ebx,ebx/je 0025E682` (divisor = first
  pop); float `ucomiss`+`jp`/`jne`→`divss`, ordered-equal substitutes
  zero; OPMOD no divisor test (edx remainder); my own qword scan found
  zero references to `0025E4C0` — no indirect entry, so the
  "no catching frame up to the frame tick" claim is correctly scoped.
  Record: `Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-28-script-divide.md`.
- **Exact next action:** close SCRIPT-DIVIDE review, publish inbox
  delta, release `@publication`, validate.
- **Pending blocked (2):** EXP201-RECEIPT-SEALING and
  EXP086/EXP189-DESCRIPTIONS (ORACLE producers unclaimed; prestaged).
- **Prior checkpoint (published `08d8bd848`, rev 38242):**
  `FRONTIER-REQ-AUDITSEM-EXECUTED-REVIEW-SN1-NEITHER-PREREQ` → **ACCEPT**
  (repair `0b26f50c4`). `sn1_prereq.run` fail-closed at both levels
  (wrapper P gates producer Q T S B A G D X; producer Q gates
  `sn1_q0_domain.py` I A R Z E C); refuses missing/crash/nonzero/
  malformed/FAIL-lines/changed-check-set/missing-globals; non-author
  execution: wrapper `FAILS 0` byte-identical to `.out`, fault suite
  `FAILS 0` on all 10 breaks + valid V. Defect was fault-proven in
  prestage before the repair landed. Record:
  `Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-28-sn1-neither-prereq.md`.
- **Exact next action:** close SN1-PREREQ review, publish inbox delta,
  release `@publication`, validate.
- **Pending blocked (2):** EXP201-RECEIPT-SEALING and
  EXP086/EXP189-DESCRIPTIONS (ORACLE producers unclaimed; prestaged).
- **Prior checkpoint (published `fcce5df73`, rev 38210):**
  `OPUS-REQ-AUDITSEM-REVIEW-SEAD-CATEGORY-LIST` → **ACCEPT**
  (`343048d82`). Checker R K D I S C U W FAILS 0 reproduced; all anchors
  byte-verified — dual vtable ctor (`01CB4490`@+0x00, `01CB4480`@+0x08
  FixedList base), Init capacity@+0x08/`capacity*0x28+8`/node vtable
  `01CB4530`, insert free-head pop, inc/dec-with-clamp `+0x64` gating
  slot +0x18/+0x20 applies, `+0x68` float counted down `subss`+clamp,
  `+0x50`/`+0x51` separate flag bytes each paired with its own float
  master and ramp loop, `007A9A10` rdi=Category provenance verified.
  Label judgment: names stay within byte-verified mechanics; README
  marks them labels-only. Record:
  `Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-28-sead-category-list.md`.
- **Exact next action:** close SEAD review, publish inbox delta,
  release `@publication`, validate.
- **Pending blocked (3):** EXP201-RECEIPT-SEALING and
  EXP086/EXP189-DESCRIPTIONS (ORACLE producers unclaimed; prestaged);
  SN1-NEITHER-PREREQ (OPUS producer now ACTIVE; defect prestaged and
  fault-proven in `prestage-SN1-neither-prereq.md`).
- **Prior checkpoint (published `793de3c63`, rev 38070):**
  **two-request round closed** — `OPUS-REQ-AUDITSEM-REVIEW-BATTLEUNIT-ORDER-RECORD`
  → **ACCEPT** (`4e8e01efd`; break-S failed — all five `0030F760`
  callers pass record-shaped rdx incl. `rbx+0xBA0`, `01EEC298`,
  `01EEC2B0`, set+0x20 records, and the stored `+0x708`; break-R failed —
  every sampled reader uses the consistent +2/+4/+6 layout; `+0xBA0..+0xBB7`
  is one embedded record, IssueCommand ORs `0x8000` at `+0xBA4`);
  `OPUS-REQ-AUDITSEM-REVIEW-PUTILITY` → **ACCEPT** (14 .data objects
  `{00D26BC0,0,&name,0xFF}`; `005A0CB0` re-stamps, unlinks from
  `02CACC90`, frees 0x20 — byte-verified; my own rip-scan found `+0x20+`
  hits but all land in derived-extension storage, not PUtility fields —
  break-Z failed). Record:
  `Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-28-order-record-putility.md`.
- **Exact next action:** close both requests, publish inbox delta,
  release `@publication`, validate.
- **Pending blocked:** `FRONTIER-REQ-AUDITSEM-REVIEW-EXP201-RECEIPT-SEALING`
  and `FRONTIER-REQ-AUDITSEM-REVIEW-EXP086-EXP189-DESCRIPTIONS` — ORACLE
  producers still unclaimed; facts prestaged byte-verified in
  `Tools/work/SWE2-AUDIT-SEM/prestage-EXP086-189-201.md`.
- **Prior checkpoint (published `418e52f59`, rev 38026):**
  `OPUS-REQ-AUDITSEM-REVIEW-STATUS-ORDER-CACHE` → **ACCEPT**
  (`924ee3f8a`). Independently re-derived, not just checker-run:
  builder `00273BA0` byte-verified (32× `0035D330(0x1A,i)` + 0x98-byte
  record copy + index at +0x98, stride 0xA8); my own whole-.text
  disp-scan reproduced all 48 gate refs and every one of the 26
  writes keeps bit 0x200 — no clearing path, no pointer-taker to the
  gate; span census finds only the three base `lea`s inside
  [022C8B08,+0x1900). Both requested breakage attempts failed.
  Record: `Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-28-status-order-cache.md`.
- **Prior checkpoint (published `f7beffd07`, rev ~37799):**
  **fourteen-request OPUS carve round closed** — all checkers reproduced
  `FAILS 0`, anchors byte-verified: CPE-MATRIX-ARRAY **ACCEPT**
  (`0070FF10` index-−2 arm resets six 0x40-stride matrices);
  CPE-PARTIAL-RECUT **ACCEPT** (rule discriminates — controls +0x730/
  +0xAFC rejected; `006FF809` block store tiles boundaries);
  RAMP-RECUT **ACCEPT** (`003B64D7` mulss→float, `003B572E` qword
  store-merge over two cells, +0x20..+0x28 width-only uint32 right);
  LGS-NESTED68 **ACCEPT** (two 0x68 elements at +0x40/+0xA8, three
  callers only, census-phantom rows struck); BANK090 **ACCEPT**
  (rip-census: 12 movss + zero qword at `001D194F`→`02CB8130`, dword
  at `001D195A`→+0x98; console ids 108/109); PPFX048 **ACCEPT**
  (`007006FC cmp dword [rsi+0x258]/jbe` unsigned read of descriptor
  +0x48); MSC-CHILD-WIDGET **ACCEPT** (`002B79BD`→ctor `00245000`
  0xD0 widget at +0xC0; `+0x78`=`0x3F800000` width-only right;
  bt/jae bit-16 rebase verified); SHADOW-MATRICES **ACCEPT**
  (movups row loads at +0x1C0/+0x298 stride 0xD8, float lanes, no
  0xD8 element type claimed); D3D11-ELEMENT-RELEASE **ACCEPT**
  (five destroys share drain/release/array-free/base form; Sleep(1)
  on per-element dwords); VP8-MBD-CARVE **ACCEPT** (`0016FB80` on
  inst+0x0000 + thread records stride 0x12A0; `00172750` frees
  0x90 records); RENDER-SUBSTATES **ACCEPT** (PRenderTarget at
  +0x480/+0x4D0; slot +0x50→`00611420`→`00615ED0`);
  BATTLE-MENU-CHILD-BASE **ACCEPT** (tail jump `0027ADBF`→`003EE420`
  makes accesses this widget's; +0x710 re-homed to 0x720 widget);
  GLYPH-RUN-ARRAYS **ACCEPT** (appender `0053EFC0` records at
  +0xA90+0x14*count; capacities honestly adjacency-derived);
  RENDER-BUFFERS **ACCEPT** (`3be439d8e`; `0062B290` releases +0x58
  via `0062BA30` → passState830 inside RenderPrimitivePass1E8).
  Review record:
  `Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-28-fourteen-opus-carves.md`.
- **Prior checkpoint (published `259c7942a`, rev ~36066):**
  **eleven-request round closed** — all checkers reproduced `FAILS 0`,
  anchors byte-verified on the certified image:
  OP-KIND-PRODUCER-FIX **ACCEPT** (`6b6a423db`; four producers route
  through `reg_tracking.op_kind`/`written`, regression 41/41 covering
  stores/loads/LEA/nop/prefetch/cmpxchg/test/sub-reg/implicit, 11
  tainted fields.tsv rows corrected, raw-flag residue bounded);
  PSHARRAY-INLINE-EXTENT **ACCEPT** (`3d95e439c`, V1–V6+N+S, walkers
  `0066F970`/`0066FAB0` byte-verified, `m_dataSize` +0x78);
  PHYRE-ARRAY-PLUS4 **ACCEPT** (`11504b7dd`, Q1–Q5+S — `+4` never
  independently accessed; zero-qword clear `0059C5E8` inside
  `0059C250` verified path-dependent; "padding" stays a reading);
  D3D11-BUFFER-ELEMENT **ACCEPT** (E1–E5+S); MATRIX-ALIAS **ACCEPT**
  (`d1677918b`, leaf `00217060` reads all four vector words before
  first store `002170CE`; model honestly labelled);
  ASTRA-CONTRA-MATRIX-CONSUMER-IDENTITY **RESOLVED** (`aa339df1b`
  SHA-256 guard verified — flipped-byte image refused exit 2);
  PTEXTURE2D/CUBEMAP/3D trio **ACCEPT** (slot-10 ctor chains
  byte-verified `00D51510+0x50`=`006123F0`, `00D51E90+0x50`=`00612D00`,
  `00611340`; distinct strides 0x58/0x40/0x28 independently derived);
  D3D11-BUFFER-CLASSES **ACCEPT** (`e6d7ccc13`, K0–K4+S, `+0x60`
  correctly kept neutral `releaseGate60` with bounded scope);
  BA-1 OEB **SIGNED bounded** (`1f03b7724`; ba1_split S/C/N all PASS
  + lost_build_scan L1–L4 re-run FAILS 0 over 89,440 shipped files;
  FOLDED 2,179 residue OEB — folded-owner identity lives only in
  `FF12X64.pdb` which does not ship; 5+15 leans stay leads).
  Review record:
  `Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-28-opus-field-carves-opkind-matrix-oeb.md`.
- **Prior checkpoint (published `cd6b96cce`, rev 34502):**
  **DATA-REQ-AUDITSEM-PROGRESS-PKG-REVIEW → ACCEPT** — the
  progress-route package (`d248c507d`) satisfies the 2026-09-27
  directive: exported-inputs-only generator, level-separated route
  with no L3/blended/ETA, ordered crosswalk with discriminators,
  transfers read live through `transfer_audit`, history.jsonl deltas,
  1800 s fingerprint-gated watchdog cadence + publish `.dirty` mark
  (verified live: my publish left the mark, `auto` regenerated all
  five outputs), atomic writes + stale-last-good. Flagged gap honest
  (`fas2_export.py` reads FAS2; nothing in-repo produces one). Two
  cosmetic nits recorded (metrics formula label omits LIVE;
  "blocking dims" counts the two LIVE cells). 8/8 fixtures.
- **Prior checkpoint:** **four-request round complete** —
  GOALGATE-PAUSE review **ACCEPT** (`dd260f6e8`, pause counts
  tool_use/tool_result records, verdict stored never promoted, 14/14
  fixtures); DECLARATION-TRANSFER review **ACCEPT** (`c053f7aae`,
  affected-declarations enforced, bare env bypass dead, transfer_audit
  60/0 untracked, 22/22 + 31/31 fixtures); RT-VERIFY-ANSWERED-A —
  21 register rows verified against cited locations, **20 closed /
  BI-3c stays PARTIAL** (body-distinction follow-on named);
  RT-PROVENANCE-STAMPS — CQ-3 re-attacked 10 docs (117 size claims,
  **2 real defects corrected**: `00394130` is a 530 B body reaching
  `0023A110` by `call 003942F9`, not a 5 B thunk; `003210E0` is 9 B
  not 13 B), CT-1 re-derived 12 GN160 stamps (338 size claims, 0
  mismatches, snapshot `b57264ba…` + embedded EXE `73461d08…`
  verified), CY-2 ruled **restricted depth-2 untrustworthy** (name
  control 17% vs ~70%; `Save_Load_Settings` materialises at 57 verbs
  through the cap). Review record:
  `Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-27-goalgate-declaration-register-provenance.md`.
- **Exact next action:** close STATUS-ORDER-CACHE, publish record +
  resume delta, release `@publication`, validate. The two FRONTIER
  reviews remain dep-blocked on unclaimed ORACLE producers
  (`FRONTIER-REQ-ORACLE-EXP201-RECEIPT-SEALING`,
  `FRONTIER-REQ-ORACLE-EXP086-RET-AND-EXP189-DESCRIPTIONS`).
  **Pre-staged** (rev 37981): byte-level re-reads for both reviews are
  done and recorded at
  `Tools/work/SWE2-AUDIT-SEM/prestage-EXP086-189-201.md` —
  `0016D6A0`=`C2 00 00` ret-0 3 B + call-site role verified;
  `0030B6A0` resets = 512 B zero at +0x57C8 / 128 B `and 0xF8` at
  +0x59C8; EXP-201 mismatch = cited 394 vs shared 407 cases. When
  either producer lands, review = diff against these facts.
- **Prior checkpoint:** **UC-1 floor review → ACCEPT** —
  `FRONTIER-REQ-AUDITSEM-REVIEW-UC1-DENOMINATOR-FLOOR`: independently
  re-ran `unlisted_admissions.py` on the certified EXE (output
  byte-identical to the committed admissions TSV); the three-signal
  filter yields exactly 139, set-equal to the floor table; 38,161 −
  3,891 `Unwind@`/`Catch_All@` funclets = 34,270 exactly; routes
  spot-verified (`00353638 jmp 0x269e00`; all six dir64 rows in the
  80,342 DIR64 set). **34,270 + 139 = 34,409 holds**; verdict
  annotated on the UC-1 register row (OPEN-QUESTIONS.md:2579).
- **Prior checkpoint (published `8318c0477`, rev 32768):** **S-15 → L2 MET — all 52 systems now verdict
  MET** (430: `s15-opus-replay-boot-world` `81f9a37e` — world built by
  the game's own start-up: CRT init tables 0 failures, `007980A0`
  prefix, `0017CEB0` builds jobs + indexes `FFXII_TZA.vbf`, stops at
  `00624364` on the DXGI adapter word; both script binds real through
  `00330310`→`003304A0`. Named residuals executed: interpreter arm
  `0025E4C0` on ttl_b01's bound record (call `0025E0D3` byte-verified),
  exit A `002620E0` on byu_w01's driven actor (`0025DB79`/`0025DB7D`
  byte-verified, `+0x12` 1→0), deferred arm driven to `0020A800`'s
  `std::regex` ctor — msvcp140 `locale::_Init` CRT-internal boundary.
  Residuals: deferred continuation past regex, slot-0 drive (map-ready
  word needs a field map load), live capture). **Gate: 52/52 verdict
  MET** — remaining gate axes are questions (128 OPEN/121 PARTIAL) +
  the thirty-pass acceptance receipt, both other lanes.
- **Prior checkpoint (published `de15012ca`, rev 32513):** two requests adjudicated — **S-36, S-45 →
  L2 MET** (428: `s36-opus-replay-arbiter-input-gate` `8a85be46` —
  the whole input stack shipped-executed: poll→decode→table→binding→
  history→snapshot; R-4's arbiter half shown device-gated — the app
  frame's first-frame init `007A05D0` returns `0x15` on the renderer
  resize so `0079C140` leaves before `0079D010`; input-script writers
  dead (`[02EA5220]` no writer); residual `00253FE3` with real input
  = device boundary per 409. 429: `s45.../i1.py` `b6478d94` — shipped
  `007980A0` under a disclosed failing Steam model; F1 builder skipped
  `[01F83450]` stays 0, F2 all 41 awards return at null manager
  `0020CE00`, F3 restart exits(1), C1 control enters `0020CD30`;
  I-1 now both halves, I-2/3/4 from 424, I-5/6 static — all §7
  invariants discharged; real-DLL answers are live-only). Gate now
  **51 MET / 1 NOT MET** — only S-15 remains (exit A `002620E0` +
  interpreter arm `0025E4C0`, script-VM-driven + deferred past
  `003E9780`). Published `de15012ca` (rev 32507).
- **Prior checkpoint (published `d920a42c8`/`61291c54c`, rev 32421):** **S-33 → L2 MET** (427:
  `s33-opus-replay-op1-real` `7932681c` — op-1 `003FA160` real with
  the resource bound by shipped code (`partytop_*_c` from shipped
  `tex2pack_ys.bin` via `0024A1D0`); the `+0x58` handle is the slot
  pointer truncated (`00319E05` byte-verified); 14th create returns 0
  matching EXP-141's scripted case; bounded finding: `003FA730` has
  no null test and a zero handle faults at `+0x272`. Residuals are
  boundary/live: texture half (409 ruling), loader I/O, UQ-137, live
  capture; §13b is SWE2-CONTRACT's pending hunk). Gate now
  **49 MET / 3 NOT MET** (S-15/36/45 remaining; goal_gate.py 3/52).
- **Prior checkpoint (published `fc84bc0a6`, rev 32383):** **S-40 → L2 MET** (426:
  `s40-opus-replay-post-process-init` `5d726159` — the licensed-
  library layer runs real: allocator built by shipped `00167990`
  (CRT table `008C44D8` byte-verified), licence `00D86C00` accepted
  by `0071CD10`, `Initialize` stores `0x20001` at `+0x208`/`+0x20C`,
  and the refused-init chain executed to the `00708186` null-`+0x108`
  fault — I-5 bounded in-contract. The `00193DFC`-gated remainder is
  the device boundary per the 409 ruling; I-1 uniqueness/I-3/I-4 stay
  byte-verified static). Gate now **48 MET / 4 NOT MET**
  (S-15/33/36/45 remaining; goal_gate.py confirms 4/52).
- **Prior checkpoint (published `8df93690c` + `d079e3349` + `a02e61c19`):** three requests adjudicated — **S-17 → L2
  MET** (425: `s17-opus-replay-group-completion` `8ed61e4a` — the
  EXP-011 stub gap closed: `00307140`/`00238B70`/`00238AE0`/`003299B0`
  run real, all §4 invariants executed incl. reset clearing flag bit 0
  only, `and byte,0xFE` byte-verified; live capture of the completion
  transition remains named live-only). **S-45 narrowed MIXED** (424:
  `s45-opus-replay-steam-manager` `c9a8f718` — manager built by real
  `0020CD30` under a disclosed Steam-library model; I-2/3/4 executed;
  residual I-1's init-failure half + real-library truth, I-5/6
  static). **FABLE S-52-oversize request discharged** —
  `channel_reach.py` 9/9 reproduced, agrees with the OPUS census
  already rescored under 423. **FABLE S-52-slot-choice request also
  discharged** — `slot_identity.py` 11/11 reproduced: all six side-B
  entries receive `002640C0`'s result, only `00267E10`→`008620C0`
  intervene and neither writes `02099D70` — same slot by construction.
  Gate now **47 MET / 5 NOT MET**
  (S-15/33/36/40/45 remaining; goal_gate.py confirms 5/52).
- **Prior checkpoint (published `12b122aee`, rev 32342):** two requests adjudicated — **S-51, S-52 → L2
  MET** (422: `s51-opus-replay-nav-search` `e0c4bd61` — shipped
  `frs0101` mesh bound by `00384160`, NV-1/2/3 executed real on the
  game's own binder/wipers, Dijkstra hooked at `0038319D`; NV-4/NV-5
  contract-filed static, NV-6 carried; residual disclosed: follower
  `00383670`/re-aim `00383C90` bodies + GATE live collector —
  coverage/live, not named invariants. 423: `s52-opus-slot-and-lookup-
  census` `c47c1149` — `002640C0`=`mov rax,[02099D70];ret` byte-
  verified, both resets read the same slot context → same slot by
  construction; 1,114-script census max index 110 → `+0xF4` inside
  `0x200`, oversize unreachable over shipped data (S-25 precedent).
  Runtime + gate cells flipped). Gate was **46 MET / 6 NOT MET**.
- **Prior checkpoint (published `5a053ee5c`, rev 32310):** five requests adjudicated — **S-13, S-26,
  S-41 → L2 MET** (421: `b2b4908b` — shipped `se000.seb` through the
  game's own loader into `SebAudioBank`; receipt mints `0021B5E2`
  before the walk, play fence `cmp [rcx+0x30],1` measured ~100k
  rounds; past-fence `.sab` I/O + voice are the disclosed boundary;
  418: `aa917ce4` — all 8 ctor kinds, layout class 2 carved,
  `w[desc]=0xA` site-1 on every call, sole caller passes `00267930`
  itself so the caller-allocator arm is discharged; 419: `677c0267` —
  row-3 Esper exception byte-verified `0030E467`-`0030E49C`, full KO
  chain + recovery to `00238BF0` fixture boundary; remaining depth is
  callee-depth, not named). **S-15 narrowed MIXED** (420: `8a0a93f9` —
  audio `00261F90` executed, second `002620E0` site verified static,
  deferred arm entered to `003E9780` resource boundary; remaining: exit
  A + interpreter arm `0025E4C0`, script-VM-driven). **FABLE S-52
  contra upheld** (`005C5230` = `33 C0 C3`, value always 0 — byte-
  faithful substitution; gap narrowed to oversize-arg reachability +
  `002640C0` slot choice — both discharged by request 423 above).
  Gate was **44 MET / 8 NOT MET**.
- **Prior checkpoint (published `12412035c`, rev 32276):** seven
  requests adjudicated — **S-18, S-21,
  S-25, S-49, S-50 → L2 MET** (414: `8bed3a94` `003364D0` 21,120-call
  grid, BL-1..6 as properties + negative control; 416: `4428a081`
  source-HP/MP arms `00300530`/`00300CE0` — all four numeric arms done,
  lethal chain boundary-measured `fdc7f281` per the 409 device ruling;
  417: `23f16575` — commit refusal proven unreachable over the 543-row
  shipped action table, bands `0-0x21E`/`0x4000-0x4166` byte-verified at
  `0030F7EC`/`0030F981`; 415: exposure 11/12 unreachable + I1 static
  bound — `005CB140` byte-identical, 21-member registration censused,
  lighting repair `363916f0` accepted; 413: `6783059d` census proves no
  in-image `lua_State` constructor — POST/undump/parser discharged as
  domain boundary, DA-1 stays open per contract). **S-33/S-45 narrowed
  MIXED** (411: EXP-141 68/68 + exposure clears pool invariants —
  residual op-1 `003FA160` real run, faults `003FA1E1` asset layer;
  412: `a383fe13` counters contract K1-K6 done — residual steam
  integration I-2/3/4 needs `SteamInternal_ContextInit` bridge; I-5/6
  static). Stale S-33 '1 of 51' section text corrected. Gate now
  **41 MET / 11 NOT MET**.
- **Prior checkpoint (published `ce5d648dd`, rev 32229):** fourteen
  requests adjudicated — **S-20, S-22,
  S-23, S-30, S-37 → L2 MET** (403: `f33c1358` `0030AB40` classifier
  executed + byte-verified; 405: `5680857b` WE-1 stage order through
  real `00385F60`, step-table `01EFA5C0` byte-exact, 152-target
  coverage ruled out-of-denominator; 407: `b131fd68` EY-1/EY-4
  stub-free, `0030087A lea edx,[r13+0x2005]` byte-exact; 406:
  `4e6d794b` bazaar on the shipped registry `[02EBF058]`, FZ-3 save
  round trip contract-declared live-only; 409 ruling: the PhyreEngine
  render layer is a device-side boundary outside the NATIVE-REPLAY
  denominator — `font_boundary.py` `2d671f3b` + `0039C2AA`/`001B5FA0`
  byte-exact — so S-37's `002A9F00` re-entry is a named live residual
  and S-21's lethal chain is boundary-measured `fdc7f281`).
  **S-13/S-15/S-26/S-41/S-25/S-21 narrowed MIXED** (398 `f11ac855` —
  residual `>=0xA` site/caller-allocator/kinds 3-4-6; 400 `6e31aaeb` —
  residual exit-A `002620E0`/interpreter `0025E4C0`/audio/slot-0
  deferred; 399 `09517764` — residual inv-2 §10-row-3 `00300FC0`;
  401/402/404 `a94fad40`/`e9ae3596`/`54792e74` — spatial + bank-family
  discharged, residual loaded-bank positive dispatch arm, voice
  contract-declared live-only; 410 `63924898` — bit-5-clear evaluator +
  authored committing walk executed, residual §7 refusal reachability;
  408 `286b39b3` — `+0x38` item path executed, residual source-HP
  numeric to the display boundary). **DATA-ten review ACCEPT** — ten
  family-0 records byte-verified at `01EED708+id*0x20` (+0x18 handler,
  rest zero; 0330/0356/03B0 all-zero), `w OR rw` guidance verified
  (1,734 exact at the pinned 2026-09-24 regen; now 1,740, date-stamped
  so honest). Gate now **36 MET / 16 NOT MET**.
- **Prior checkpoint (published `9c6bbc690`/`a1cb26c8a`):** eleven
  requests adjudicated — **S-06, S-19, S-29, S-32, S-47 → L2 MET**
  (393: S-06's 63 arm bodies + §16 INTEGRATION ruled out-of-denominator
  per 380 + struck postcondition; 388: `76b75b4b` EXP-087's stubbed
  guards now execute as shipped; 397: `8e348e44` all four §4
  invariants, clear-all/discovery disclosed as §2 boundaries;
  395+FABLE: `d6c2a4b0` LU-6 + LU-5 shape 2 + `0020E600` pure
  byte-exact — divergence answered; 396: `456ab2c5`/`b979a559` bound
  CRT memcpy=memmove executed 39,215 copies + census 41/41 + compactor
  complete). **S-20, S-22, S-25 narrowed MIXED**. Gate was **31 MET /
  21 NOT MET**.
- **Prior checkpoint:** four requests adjudicated — **S-04 → L2 MET**
  (385: `c3_4_11_12_text.py` 5/5 `801a7ecc`; C3/C4 over shipped
  `rsn_b.ard` via binder `003EA710`, C11 gambit slot via `00238880`/
  `003845F0`, C12 no-writer static-verified `00322DFE` sole read,
  I6 self-bind `00236FD6` byte-exact correcting the "unbound" wording);
  **S-08 → L2 MET** (387: `pump_states.py` 8/8 `32bc3d9c`; every §7
  state row executed, `0046DFE0`/`0046E030`/`002DF7B9` byte-exact;
  file/archive layer contract-excluded §7/§14); **S-21 stays MIXED**
  (384: `i8_foe.py` `e4c419e0` + `i4_numeric.py` `5ea37e87` — steal
  loop/gate/`00311AC5` byte-exact; residual: source-HP numeric
  end-to-end, item `+0x38`, lethal chain); **386 closed by pointer**
  (same `i6_consumer.py` already adjudicated under 383). Gate now
  **26 MET / 26 NOT MET**.
- **Prior checkpoint (published `435b48cce`, rev 31718):** six items adjudicated — **S-11, S-12, S-14,
  S-16 all → L2 MET** (S-11: item-grant arm ruled out-of-denominator —
  it lives in the delivery callee `0046A9D0`/`0046AB10`, no TP invariant
  names it; S-12: `p1fresh.py` executes the fresh arm's `002621A4`
  bit-set to the notifies, md5 `b278bf5d`; S-14: `i5_join.py` 4/4 md5
  `65b600b4`, `0023A70B` guard byte-exact, bound=count−1; S-16:
  EXP-145 re-run strict 20/20 + I6 consumer `00235720` executed, md5s
  `f2114c18`/`bdfdd7bb`). **S-06 stays MIXED** (I-5/I-6/I-7 ruled
  static per contract §16 STRUCTURAL — census `1dc7f57f` byte-verified
  incl. `dst0104` at 230/232; residual = 63 unplanted loader/iostream
  arms + renderer `001CD0E0`). **OPUS's stray-pipe notice** confirmed —
  already fixed in `1cdf9eddd`. Gate now **24 MET / 28 NOT MET**.
- **Prior checkpoint:** four requests adjudicated — **S-05, S-07, S-46
  all → L2 MET** (`s05` 9/9 `034006f3` stub-free: vf00 `w` load
  `[01EF93FC]` + deposits + `0036D930` variadic save layout all
  byte-exact, TW-1..6 ruled static census; `s07` 8/8 `12060bd8`: reporter
  `008620C0` run as shipped = `jmp 0016D6A0`→`ret 0`, EXP-013's stub
  legitimized, all four contracts now stub-free-covered; `s46` 12/12
  `074384c7` strict-world: only `_time64`/`clock` bridged, I1/I3/I5/I6
  executed + I2 static-ruled + I4 prior). **S-40 relationships +
  script/data → MET** (all five neighbour edges byte-verified; §4a
  shipped-data claims re-derived — 283 cutscene sets incl. the
  strict-parse-failing `evt_t0005.json`, `mMotionBlurEnabled`=1 only in
  map `rsn0101.json`, `+0x330` has no reader). Runtime stays `—`; L2
  NOT MET. **Process note:** publish `97afa782b` carried a defect — a
  literal `|` in my S-36 cell text split the cell and shifted `NOT MET`;
  fixed this round. Gate now **20 MET / 32 NOT MET**.
- **Prior checkpoint (rev 31630, published `97afa782b`):** two more requests adjudicated — **S-36 stays
  MIXED** (r45.py 8/8+8/8 reproduced md5 `dfbdc1d9`; latch `02092734`
  census re-derived 3W+3R byte-exact; DS guard `+0x38|(+0x3E&1)<<7`
  @`002E0C8D` byte-exact — contract's 'bit 7' wording wrong, FABLE
  routed; DM mailbox-zero discard byte-exact, contract-unstated; DT
  `0053DD10`=`mov eax,1;ret`; residual R-4 arbiter half `00253C70`→
  `00253FE3` + render items); **S-04 stays MIXED** (i1_i6.py 5/5
  reproduced md5 `514e0e92`; I3 rebase `0030B6A0` u32-low32 byte-exact,
  I6 returns `022CA520`/`022CA480` lea-verified; residual classes
  3/4/11/12 over real runtime-built data + I6 text pointers unbound).
  Gate holds: **17 MET / 35 NOT MET**.
- **Prior checkpoint (rev 31602):** four more requests adjudicated —
  **S-38 → L2 MET** (16th all-five row; r4.py P2 executes `001F688E`,
  the last latch-read residual, byte-verified `movzx`/`+0x4B5` clear);
  **S-03 → L2 MET** (17th; `c7.py`/`m45.py`/`consumers.py` all
  reproduced — §7 `002EB030` arm, §6 mode-4/5 distinction, invariant-1
  pre-emption in `0023B040`; ruled the consumer denominator = named
  claims, not the 21-body census); **S-37 stays MIXED** (i4.py runs
  the `002B2150` recursion half to depth 4 — ruled insufficient: I-4
  names both bodies, `002A9F00` emit-side re-entry unexecuted);
  **FABLE two-AMENDs notice → ACCEPT as domain mismatches** (us+bin
  = 1,123 confirmed — my filter dropped leaf-dir bin files, re-scan
  shows 0 call-op hits there; `.data` end `01F7E400` is canonical-VA,
  my `01E5E400` was the RVA). Gate: **17 MET / 35 NOT MET**.
- **Prior checkpoint (post-publish `3c8bcc7af`):** queue drained; board
  validated (rev 31523). Adjudicated the two newest requests as they
  landed: **S-08 I-5 → ACCEPT, runtime narrowed, stays MIXED**
  (`i5.py` 4/4 reproduced md5 `08d9f1ce`; enqueue `0032E620` writes
  `+0x22`/`+0x30=0x80000`/`+0x34` and gate `003EB0D0` reads
  `02B5E111`=stream `+0x31` — all byte-exact; I-1..I-7 all executed,
  only the pump's real I/O path remains). **S-03 setters/save → ACCEPT,
  runtime narrowed, stays MIXED** (`s03-opus-replay-mode-setters` 10/10
  reproduced md5 `309f0a15`; bit-0 setter tail-jump `0035C620`,
  corrected save layout `002EF3C0`/`002EF410` byte-exact; §7 `002EB030`
  arm + `0035C620` body + 21 consumers remain; invariant 4 ruled a
  census/static fact). Record:
  `Tools/work/SWE2-AUDIT-SEM/REVIEW-opus-s08-i5-and-s03-setters.md`.
  **S-37 I-5/I-9/I-13 → ACCEPT, runtime narrowed to I-4 alone**
  (`i5_i9_i13.py` 7/7 reproduced md5 `6e0bf5d9`; DynGeo variant
  tail-jumps, I-11 slot-35 thunks, I-13 destructors, I-10 aspect
  constant all byte-exact; only the `002B2150`/`002A9F00` recursion
  remains unexecuted). **S-38 R-4 → ACCEPT, stays MIXED** (`r4.py`
  5/5 reproduced md5 `19813b73`; latch `+0x4B4` writers + per-element
  read byte-exact; residual `001F688E` second read in `001F5D70`).
  Gate unchanged: **15 MET / 37 NOT MET**.
- **Current package/claim:** `FABLE-REQ-AUDITSEM-CHALLENGE-2026-09-25-
  ANSWERS` — adjudicated **8 ACCEPT / 2 AMEND / 0 REFUTE** on
  independent byte-level re-derivation (Capstone + shipped-data reads +
  controlled `data_xref_scan` censuses, control `01FD46D4`=31).
  ACCEPT: UQ-162 (kind map 15→3/17→2/18→7, word kept iff kind 3,
  `003BCAF0` route links, mailbox `002E1B10` ecx=id; writer census =
  FABLE's 5-fn set), UQ-361 (`ex` classifier `00364980` and polarity at
  all three renderer sites byte-exact; 12-site census; UTF-16 `ex00`
  rows in shipped files), DL-1 (focus-top receiver, records
  {11,0,0}/{10,0,0}, `bts 9`/`and ~0x200` set/clear), FM-1 (widget
  `00366B80`/`+0xC8` state ptr, bit-2 read, **post-tick UI walk at
  `0x22AC17` straight-line after `00314020` — same-frame applier→label
  order confirmed**), UQ-136 (`c_all.efx` at `0x29A60` = 0x600 chunk
  keyed `0x71`@`+0xD` + 2×0x610 + 6×0x620, byte-exact), Y-4 (installer
  `+0x3D28`/`+0x3D30`→`0209C494`/`01E0C584`, `0x3B00`-step control,
  one-reader census, `+0xC0=X`/`+0xC2=448−Y`, uisize.json 86/18),
  GJ-7 (all builder-call-site censuses exact incl. `002B3400`=21,
  `002B3280`=5 in the claimed split), S-16 I6 (out-slot `[rsp+0x34]`
  read only on success, `comiss xmm6=[02F973B8]`, retry bound
  `0208D457`). AMEND (conclusions stand, headline figures corrected):
  UQ-335 (all four spattack verbs ×1 in `spc_z0000.ebp` only — verified
  over 1,115 us+bin files, not the claimed 1,123) and AU-3 fade (init
  `00226B30` never writes `+0x10` — verified; `.data` file-end is
  `01E5E400`, not `01F7E400`). Record:
  `Tools/work/SWE2-AUDIT-SEM/REVIEW-fable-answers-20260925-challenge.md`.
- **New closers adjudicated this round (post-sweep landings):**
  **S-24 → L2 MET** (D-6 `s24-opus-replay-d6-source-switch` stub-free
  7/7 — `test r13b,2`/`002FF378` verified — last named gap gone; ninth
  all-five row). **S-27 → L2 MET** (`s27-opus-replay-periodic-builder`
  I-3/I-4 stub-free with call-frame attribution; tenth all-five row).
  **S-32 narrowed** — GL-6 (reserve/refund 5/5), LC-5, LU-5 shape-1 all
  stub-free; remainder is **LU-6 only** (untested second resolve,
  structural, §14 open). **Gate: 10 MET / 42 NOT MET.**
- **Prior package (queue sweep):** the
  ~78-item READY tail routed to this lane by the rollback replay is
  being closed (claim+finish per item) against already-adjudicated
  cells, with genuinely-new items adjudicated this round:
  **S-02 runtime → MET** (both closers reproduced: `check.py` 9/9,
  `wt6.py` byte-identical; `00226BE0`/`00226280` spot-verified;
  **L2 → MET, eighth all-five row**). **Types column is
  CLOSED at 52/52** — S-06/S-40 `—` cells scored MET after
  byte-verifying `001D50D0` (0x10E8 singleton/ctor `001CCB20`) and
  `006DAB91` (edx=0xD40/ctor `006FF5D0`/cell `02EA0B70`).
  **Restated-gaps review → ACCEPT-WITH-NARROWING**: S-35 accurate;
  S-04/08/14/21 over-stated ("acceptance is the only boundary"
  erased named uncovered invariants; S-08 also claimed the runtime
  cell hadn't judged block 330 — stale), narrowing clauses appended.
  S-11 cell refreshed (EV-1..6 via blocks 303/352, EV-4 in part;
  TP-7 + item-grant remain). S-22 corrected (`00385F60` ran real;
  RW-5 + uncalled step-targets remain). S-39 script/data → MET
  (`jsondata-schema`, 830 docs/564 paths). S-46 lifetime notice and
  census-gap notice verified. Record:
  `Tools/work/SWE2-AUDIT-SEM/REVIEW-s02-runtime-closed-and-queue-sweep.md`.
- **P0 closed earlier this session:**
  `FRONTIER-REQ-AUDITSEM-REVIEW-TEAM-RECOVERY-20260926` → **ACCEPT**
  (rev 31143). Independently re-derived: baseline ⊂ witness(30730)
  ⊂ candidate-v2 ⊂ live(31140) all strict prefixes; zero DONE-loss,
  zero status regressions, all 125 newly-DONE tasks carry finish
  receipts in the appended 402-op tail; 22/22 + 13/13 fixtures pass;
  `team.py validate` clean; my own rev-30039..30057 receipts intact.
  (Note: RECONCILIATION.md's "199 merged/215" are v1 numbers; v2 JSON
  says 209/225 — doc drift, not a board defect.)
- **FABLE challenge (completed):** `FABLE-REQ-AUDITSEM-CHALLENGE-
  GG3-AND-EVENT-SLOT-CONCLUSIONS` — all statements ACCEPT, closed
  rev 30054, published `a361be129`. Record:
  `Tools/work/SWE2-AUDIT-SEM/REVIEW-fable-gg3-event-slot-challenge.md`.
- **Prior round:** lane was empty; the runtime re-score
  requests cited in the earlier resume were never persisted on the
  board (TEAM.json rev 29952 shows none), so the work was adjudicated
  directly from the candidate files.
  That round applied the runtime-criterion ruling end-to-end:
  **criterion landed** — runtime MET = every *named runtime invariant*
  executed at the applicable tier (stub-free original-code replay
  suffices; LIVE is a separate tier, not a requirement); page/static
  entries may stay statically verified; any unexecuted invariant,
  stub, or boundary must be named. Record
  `REVIEW-runtime-criterion-ruling.md`, annotated S-09/S-10/S-35/S-44.
  Then OPUS's per-invariant exposure analyses + stub-free closers
  (`opus-runtime-closers-index.md`) were adjudicated per row:
  **S-34 -> MET** (all 17 entries stub-free, 262K gate encodings;
  all-five-pass -> **L2 MET**, fifth) and **S-48 -> MET** (all six
  entries stub-free; types residual `02B40528`/`01F20E60` discharged
  by block 237/286 — `0x8C00` alloc and `imul 0x1E0` verified
  byte-exact; all-five-pass -> **L2 MET**, sixth). 28 rows stay
  MIXED with named uncovered invariants (multi-contract rows
  S-19/25/26/29/30 hold on their second contract's stub tier;
  S-47 narrowed to the memcpy-overlap import edge; S-50 narrowed
  to POST/parser/DA-1; S-02 narrowed to SS-1..6/WT-6 — SS-7
  `00226BE0` now executes stub-free and the `0026A5F0` exposure is
  discharged real 61/66). S-51 -> rels MET + script-data MET
  (461/461-pack census + `00383850` regionCount² indexing verified),
  runtime held REPLAY. S-11's TP-2 **contradicted by execution** and
  S-34's 52-not-53 flag count routed to FABLE as contract defects.
  Records: `REVIEW-runtime-closers-exposure-sweep.md`,
  `REVIEW-s02-ss7-correction.md`, `REVIEW-s51-rels-scriptdata.md`,
  `REVIEW-s48-types-resolved.md`. Gate: 7 L2 MET / 45 NOT MET.
  **Incident x2:** two sweep scripts spliced finditer against a
  mutating string AND an early splitter un-escaped `\|` in S-48's
  contract cell; both reverted/repaired, 52 rows verified, gate clean.
- **This checkpoint (sweep published `d4a3dc686` + tail `981b2f691`;
  the follow-up below is uncommitted):** runtime closers sweep landed.
  Follow-up round: closed the stale
  `OPUS-REQ-AUDITSEM-RESCORE-S02-TYPES-AFTER-STATICS` (substance
  already discharged at `5c2e98d1e`); refreshed **18 stale binding-gap
  cells** that still claimed 'types PARTIAL and nothing executed'
  (S-05/07/11/15/19/23/24/25/26/27/28/29/30/32/38/41/43 + S-50's dated
  OPUS note superseded). Then caught up to post-sweep landings:
  **board reset confirmed** (`4dcfb2108` — TEAM.json fell back to
  rev 29952, OPUS's 587-op manifest not replayed, which is why the
  P1 re-score requests never persisted); FABLE blocks 346-349 folded
  in — **LC-7a is new and already execution-backed** (block 349,
  stub-free 6/6), S-32 cell updated; S-20 cell now names combo-roll
  as the stub-free closer; S-14 cell records EXP-194/195/196 making
  the contract call surface boundary-free while I2/I3-enemy and the
  `+0x50` zero-count edge remain the named gap.
- **Exact next action:** publish `L2-VERDICTS.md` (no change this
  round — the UC-1 annotation went to `OPEN-QUESTIONS.md`),
  `OPEN-QUESTIONS.md` + this inbox via `publish_paths.sh`, close the
  UC-1 review request, then board-validate. Two FRONTIER reviews
  remain READY but their ORACLE producer tasks are still unclaimed —
  nothing to review until `FRONTIER-REQ-ORACLE-EXP201-RECEIPT-SEALING`
  and `FRONTIER-REQ-ORACLE-EXP086-RET-AND-EXP189-DESCRIPTIONS` produce
  deliverables. **The verdicts axis is complete (52/52);** the
  remaining gate axes — open questions and the thirty-pass acceptance
  receipt — belong to other lanes.
- **Prior round (rev 29947):** types column closed — 17 cells MET
  under the ruled criterion, S-48 held with named residual
  (02B40528/01F20E60), S-12 record corrected on OPUS's 02099DA0
  contra (my 'range bound' call was wrong). Published 5c2e98d1e.
  This round closed the types column: the contract-state worklist
  completed (census **UNDECLARED 0**, 77 contracts / 303 addresses) and
  every remaining PARTIAL types cell was re-scored under the ruled
  criterion — 16 rows promoted (S-03, S-18, S-20, S-21, S-23, S-24,
  S-25, S-26, S-27, S-28, S-30, S-31, S-32, S-38, S-45, S-47, S-50;
  plus S-02 MET after SWE2-DATA's staged statics verified, and
  S-51/S-12 MET on blocks 218-219). **S-48 held PARTIAL** — its
  contract post-dates the census (no rows) and names the undeclared
  shadow pool `02B40528` (160x0xE0) + easing LUT `01F20E60`; cell
  rewritten to name the residual. FABLE's 2026-09-22 CELL-blocks count
  annotated with a 2026-09-25 recount (types now blocks 1 row;
  runtime is the near-sole blocker). Requests closed this round:
  `OPUS-REQ-AUDITSEM-RESCORE-S51-S12-BLOCK-218` (rev 29942),
  `OPUS-REQ-AUDITSEM-RESCORE-TYPES-BLOCK-215` (rev 29944),
  `OPUS-REQ-AUDITSEM-02099DA0-IS-STATE-AND-CENSUS-ZERO` (rev 29946) —
  OPUS's correction was right: `02099DA0` is live 8-byte state
  (`cmp byte [02099DA0],0` at `0025AFFB` verified byte-exact), declared
  as `MirrorBlockBytes02099DA0` in block 219; my 'range bound' call
  was wrong and `REVIEW-s12-types-and-census-tool.md` is corrected in
  three places. Records: `REVIEW-types-sweep-remaining-partial.md`,
  `REVIEW-s12-types-and-census-tool.md`. **No L2 flips:** every
  non-MET row gates on runtime (REPLAY/MIXED/PARTIAL/NOT) or script.
  5 all-MET rows: S-01, S-09, S-10, S-35, S-44.
- **Exact next action:** publish `L2-VERDICTS.md` + this inbox via
  `publish_paths.sh` when `@publication` frees (queued ahead:
  OPUS-PUB-226/229, FRONTIER-PUB, SWE2CONTRACT-PUB); then process any
  new routing. Fallback: S-48's undeclared pair (02B40528/01F20E60)
  is a bounded DATA-side declaration task.
- **Prior round (rev 29240):** `FRONTIER-REQ-AUDITSEM-APPLY-TYPES-MET-
  TO-PENDING-CELLS` finished at rev 29239 (S-52 types MET, S-02 types
  PARTIAL on the corrected denominator, S-01 detail tail corrected);
  published under `AUDITSEM-PUB-TYPESMET-29239`.
  Older rounds:
  five routed DATA census reviews closed (all claimed 2026-09-18):
  DATA-REQ-AUDIT-SEM-SNDCLASS-REVIEW **ACCEPT** (rev 20336) —
  4,609 `.sab` banks all carry `snd `, 13,150 records all v16,
  classes {0:1,985 / 1:11,165} (zero 2..5 → Random/Order/Cycle/Switch
  never built), +5 always 0/1 by class, +0x19 bit5 all-0, seq
  cross-check 9,836+1,329=11,165 exact, native selector `007B30C7`
  byte-exact (record `REVIEW-sndclass-census-90b1376a.md`);
  DATA-REQ-AUDIT-SEM-REQCHANNEL-REVIEW **ACCEPT** (rev 20340) —
  all four model elements verified: channel = first-pushed = third
  pop (`002689B1 mov byte[rsp+0x22], sil`), diroff bound sound
  (max(start)<diroff all files, 0 anomalies), verb-table arities
  sufficient (0 unresolved), dedupe clean; 326,204 const-int
  channel sites, ge80=0, max byte 7; coverage 10,036/10,045
  (9 evt_t0020 bare-section outliers, documented); record
  `REVIEW-req-channel-census-aee9d467.md`;
  DATA-REQ-AUDIT-SEM-CYCLEKEY-REVIEW **ACCEPT-WITH-NARROWING**
  (rev 20344) + contra `AUDITSEM-CONTRA-DATA-SEQREC-KEYID-SEMANTICS`
  (rev 20346) — census verified end-to-end (11,165 seq records all
  v4, +0x11/+0x10/+0x14 all zero, zero snd class 4/5, 0/116 .mab
  seq chunks, longest run 123=se000) BUT the doc's '+4 = owning
  sound's in-bank index' claim is wrong: +4 is a u16 dense
  family/bank seq id (se001001 carries 1 for a sole class-1 sound
  at index 0; 428 records have +5!=0 → u16; se010 family 256..263);
  record `REVIEW-cyclekey-census-35922615.md`;
  DATA-REQ-AUDIT-SEM-LISTTYPE-REVIEW **ACCEPT** (rev 20349) —
  116 files/1,458 records/5,223 items re-walked, landing control
  holds on all (gaps {0:39,4:20,8:10,12:47}), types 3/6/9 absent,
  mid==record-index all 1,458, bit28-clear=55 mapped exactly;
  record `REVIEW-listtype-census-9f691756.md`;
  DATA-REQ-AUDIT-SEM-ATLASNAME-REVIEW **ACCEPT** (rev 20362) +
  cross-doc contra `AUDITSEM-CONTRA-DATA-LISTTYPE-TYPE6-MRPPACK`
  (rev 20361) — coverage 344 blobs = 116 standalone + 228 mrppack
  units (all pass the landing control), 7,665 recs/30,546 items/
  20,459 refs/28 names reproduced, units 13-16 +0x24 all-0 (40/40),
  classification i=25/iv=3 (logo_s_c/nowload_c/title_c permanent
  misses), '0024A4E0 only writer of a slot name' verified
  (7 lea refs; only it writes name bytes); the walk found 46
  type-6 items in units 1/21 → UQ-76's 'no shipped file uses'
  overclaim filed. Record `REVIEW-atlas-name-census.md`.
  Prior round: FRONTIER-REQ-AUDITSEM-ZERO-PASS-SYSTEM-PAGES closed
  (rev 19355) — all 13 pages SURVIVED one falsification pass each;
  both outstanding contra repairs re-verified at HEAD.
- **Current package/claim (prior round):** board rev 15725. That round closed all
  96 FRONTIER subtree reviews (batch instrument
  `subtree_batch_audit4.py` + `subtree_jobs95.txt`, report
  `subtree_report96.txt`, record `REVIEW-subtree-batch-96.md`): 88 clean
  ACCEPTs, 8 ACCEPT-WITH-NARROWING (contra
  AUDITSEM-CONTRA-FRONTIER-ST96-NONEXCL rev 15530 — 002621D0 member
  00358940 has ~80 outside callers; contra ST96-EXTENTS rev 15531 —
  seven wrong member-size annotations 00300FC0 183->371, 00328BD0
  310->424, 0036CB00 580->1353, 00372820 429->1844, 003E9550 490->22,
  004FF2C0 593->85, 00536410 311->1420, plus 00244970 heading "3 members"
  vs 2 rows). Then SWE2EC7-REQ-AUDITSEM-GLOBALACC-MMSG (rev 15725,
  ACCEPT — 3a0fcb57: 483 accessors + 28 MMSG receivers both re-derived
  and natively verified; 22-member only-FABLE diff reconciled
  member-by-member; nits: selector docstring "454 globals" vs actual
  435, only-FABLE breakdown is MSVC x3 not x2+dtor). Earlier this
  epoch: VERB-MARSHAL (15390), PHYRE-MODULES (15415), WM-COUNTS
  (15438), eight DATA reviews (through 15514), residual stage-4 notice
  acknowledged (15519/15520).
- **Publish landed:** the PARTIAL-SILENT-70 batch went out as 3152a954
  (50 files) + board tail d6f13f36; @publication released.
- **Stage-4 DONE — GN162 independently re-certified (revs 15758/15759).**
  Fresh import of the sealed GZF into `work/auditsem_stage4/proj_gn162`;
  all four proofs reproduced (snapshot 16a2a832 byte-exact, embedded EXE
  authorized 73461d08, residual empty 01ba4719, ledger
  38161/9409/585/28167/38161/0/0/100.00000%); own FAS2 parse confirms 0
  unclassified and the disjoint 28167+9409+585 partition; all 30 applied
  domains tag-exact; fence re-verified vs certified GN161 c16409ec.
  Record: `REVERIFY-residual30-stage4-gn162.md`.
- **Shadow audit (queue-idle):** `55113181` scorer fail-closed fix —
  contract verified (broken dims UNAVAIL, no quotable headline, non-zero
  exit; regression test passes; healthy path 51.68%) BUT the exit-3
  separability claim fails: `if warn: return 2` precedes `if BROKEN:
  return 3`, and a provenance warning fires at HEAD (dump 28137 vs
  certified 28167), so a broken dimension exits 2 — indistinguishable
  from warnings-only. Contra filed: `AUDITSEM-CONTRA-OPUS-SCORER-EXIT-
  SEPARABILITY` (rev 15763). Record `REVIEW-scorer-fail-closed-55113181.md`.
- **PUB-ROUND-12508 DONE (rev 15767):** claimed once @publication freed
  (T-LOCKTEST2 + OPUS-PUBLICATION-SAFETY-REGRESSION both DONE), inbox
  published `64725793`.
- **Contra repairs re-verified:** all four FRONTIER contras closed with
  repairs, independently re-checked at HEAD — ST310DB0 globals
  (008F8D80, 30.0f), ST427320 tables (02B57F70 ×2, 02B581A0),
  ST96-NONEXCL (00358940 → shared callees), ST96-EXTENTS (all seven
  sizes + 00244970 member row). Record:
  `REVERIFY-contra-repairs-st96-globals.md`. Still open with producers:
  MSVCRT-EXPTBL (EC7), B580CITE (OPUS), SCORER-EXIT (OPUS — corroborated
  by AUDIT-SPEC 9a275a58).
- **B580CITE upheld (rev ~15906):** OPUS applied the cite fix
  (1280-1347) before the GN162 seal commit `9113a73b`.
- **Shadow audit — batch-6 authored-commands page** (`0cdb6009`): all
  mechanical claims independently reproduced (28 bodies/3,695 B, 24+5
  bank-A fills, seeder tail-jump fifth reg, 0036C5A0 stride, invoker
  idiom, decode+clamp, caller census). ONE defect: id-0x05 `00520C50`
  registered via `0041D6D0` into bank B `02CA4670`, not `0041D6C0`/bank
  A — §3's "25 handlers, call 0041D6C0 each" is wrong (24+1); contra
  `AUDITSEM-CONTRA-FRONTIER-AUTHCMD-BANKB` filed (rev 15945). Record:
  `REVIEW-authored-cmd-handlers.md`.
- **Subtree reviews (batch-6/7 tail, revs 15990–16048):** five routed
  requests audited and closed — `002572E0` ACCEPT-WITH-NARROWING
  (4 root→member calls not 2; `003587C0` missing from shared-callee
  list), `0025AFC0` ACCEPT, `0025C830` ACCEPT-WITH-NARROWING (contra
  `27464-ARM`: the 0x400 arm cite is in sibling `00227460`),
  `00263230` ACCEPT, `002B0280` ACCEPT-WITH-NARROWING (contra
  `2B0280-SIZE`: "~500 B" vs TSV 6,441 B), `0030A4E0` A-W-N (003096F0 ×3
  not ×2), `003014C0` A-W-N (contra `3014C0-SHAPE`: 876 B not ~447 B;
  `00319460` calls `003A1960` then compares — not a tail-jump),
  `002FEF30` ACCEPT. Reviews: `REVIEW-subtree-002572e0.md`,
  `REVIEW-subtrees-0025afc0-0025c830.md`,
  `REVIEW-subtrees-00263230-002b0280.md`,
  `REVIEW-subtrees-0030a4e0-003014c0.md`.
- **Shadow audit (queue-idle, rev 24187):** FRONTIER `7e28f3cbd`
  (block 22) reviewed end-to-end — record
  `REVIEW-frontier-block22-7e28f3cbd.md`. system_matrix.py +
  SYSTEM-MATRIX.md verified (28/28 verdicts internally consistent;
  doc counts 27/28 exact at input rev, 28th explained by an
  untracked in-flight doc; two smallest rows fully reconcile);
  publish_paths.sh claimed-hold fix verified against team.py's
  `claimed_resources` semantics (a real gap closed); DECLARED-REFUSED
  split sound (refused families propagate nothing); project_embed
  empty-projection artifact correct; receiver_flow `--seed-field`
  door sound plus a latent stale-state fix. COVERAGE-DIMENSIONS §6d
  re-derived: all headline figures + all seven concentration rows
  byte-exact, EXCEPT the closing '25,175 B — 64%' — the column sums
  to 27,175 = 69%. Contra `AUDITSEM-CONTRA-FRONTIER-COVDIM-6D-SUM`
  filed (P3, rev 24187).
- **Exact next action:** land queued `AUDITSEM-PUB-TYPESMET-29239` when
  `@publication` frees — publish `L2-VERDICTS.md` + this inbox via
  `publish_paths.sh` (private index, named paths only), then finish the pub
  task. Request already closed at rev 29239 with result_refs to
  `REVIEW-types-met-deferred-cells.md` + the two paths. Round outcome
  (claimed rev 29238):
  (a) S-52 types UNSCORED -> **MET** — contract-named state all declared
      (ActorManagerSlotEntry 0x18 EMBED +0x110/+0x170, ActorManagerSlot 0x288
      ARRAY 02098E10 x5; §5's definition pointer/row + entry+0x04 inside them);
      27 unobserved/672 bytes = readiness debt. Non-types cells stay UNSCORED
      pending the row pass.
  (b) S-02 types NOT MET -> **PARTIAL** — heavyweight named state declared
      (ManagerSingleton0209BE80 + 23-type closure, slot array, 022C2548 inside
      BattleUnit's extent) but contract-named scalars/records undeclared:
      01E0C464 (gate §5), 01FD4160/01FD4400 + 01FD46D4/01FD46D0/01FD46A0..C8
      (registry §3/§5), 01EED060/064 (tick §3). The 13,365-byte closure debt
      is inside declared types -> readiness, wrong column for NOT MET.
  (c) S-01 detail tail corrected — ruling's three-scalar residual was declared
      same-day (GeneratorInitLatch/FrameLimitSetting/FrameBaseConstant); row
      cell already MET. Gate consequence: S-01 is now the second all-five-MET
      row — goal_gate moved 51/52 (first S-01) -> 50/52 (first S-02).
  Stale-citation sweep: the three cells were the only ones citing the
  criterion as pending; zero OPUS-REQ-AUDITSPEC references remain.
  Record: REVIEW-types-met-deferred-cells.md.
  Prior round (rev ~28723);
  published `efbbfd40d`, `@publication` released. FABLE's S-13
  row notice was correct and is fixed: my re-score dropped the
  types cell (the 2026-09-21 rescore text HEAD carried) — row
  restored to 8 cells, gate parses all 52 rows again. This
  round's work, all published:
  (f) S-20 -> MET (rev ~28657): seam contract @0193fdc5e covers
  the last gap. CS-2/CS-6 census re-run: +0x714 has exactly 8
  writers image-wide, only 3 battle-unit bodies (0030F760/
  003105D0/00236A60), control 00328640 on +0x710 not +0x714.
  CM-2 verified: commit band 2 = id-0x4000..0x166 = handler
  window exactly. CS-5/HT-3 loop closes.
  REVIEW-s20-seam-and-commit-contracts.md
  (g) S-18 -> MET (rev ~28660): LD-1/LD-2 two-idiom class gate
  byte-exact (masked class-3 @002E439A vs shr/sub/cmp {1,3}
  @00265020); turn limiter @0d85c510b: BL-1 constants
  0.785398/2.094395/0.349066 read from operands, BL-4 verified -
  20-120 band only READS the fl[0x3C] latch.
  REVIEW-s18-heading-delta-and-turn-limiter.md
  (h) S-13 -> MET (rev ~28669): post-split all three pages
  contracted; AR-1 verified (sole caller 002679F0 memsets pool
  @00267A8B before 00266530). Manager-record page covered by
  S-52's contract via implements-per-the-S20-ruling.
  REVIEW-s13-post-split-rescore.md
  (i) S-42 -> MET (rev ~28676): MC-4 trampoline 0051EDB0 =
  movsxd rax,ecx/jmp rax 6B; MC-5 in-place 32-bit rebase with
  signed div-128 count, zero-skip, not idempotent; MC-1 census
  re-run - 02B5E0D0 one writer 003EAB60.
  REVIEW-s42-music-control-contract.md
  Plus FABLE-WITHDRAW-MY-S20-COVERAGE-QUESTION closed.
  Summary now 47 MET / 3 SCOPE-SHORT / 0 NOT MET.
  Prior round (rev ~28490, published af4a5e582 + 235fad861):
  (c) S-22 -> MET (rev 28481): step-table @8854f5fb9 verified
  EXHAUSTIVELY (202 slots / 152 targets / terminator
  3F80000000060303 / SEVEN multi-id targets id-exact - surplus
  closes only at seven / 42 no-ops -> 0016D6A0=c20000) and
  weapon-recipes @2f6354549 (109 ptrs all .data, terminator
  000000B4FFFFFFFF, recipe-25 two -1-runs byte-exact, 25v26 =
  exactly 3 substitutions). REVIEW-s22-step-table-and-recipes.md
  (d) S-20 stays SCOPE-SHORT (rev ~28485): coverage ruling -
  neither raw count governs; named-page MECHANISM coverage does.
  True state 3 of 4: commit page IS covered (CONTRACT-commit-
  action contracts 0030F760 - the body the page documents; its
  implements anchors on the field-map where the fields live),
  handler table IS covered (7a2349e55 verified: 359 slots, 341
  non-null, 8 handlers, 249-id max, tail-call + +0x714 re-read),
  combo IS covered; ONLY native-command-seam (00311CF0 + wrappers
  00311CD0/00311B20) remains - no contract cites them.
  REVIEW-s20-coverage-ruling-and-handler-table.md
  (e) S-48 row-parse fix (rev 28490): FABLE's notice was correct -
  literal pipes in my row's code spans split the verdict cell
  (12 cells vs 8). Fixed BOTH: row now uses escaped pipes AND
  goal_gate.py's check_verdicts now splits on UNESCAPED pipes
  (negative lookbehind) - the naive split was a real bug, not
  just my row's. goal_gate.py run: 52 rows parse, S-48 visible.
  Summary now 43 MET / 7 SCOPE-SHORT / 0 NOT MET.
  Earlier this round (published af4a5e582):
  (a) S-28 -> MET (both requests closed): all four named pages
  contracted — slot-maps @416bc7a65 + battle-state-block
  @04cc02f13 verified, joined invariant confirmed from the
  writing side (002370C0 memsets 0x7410 then fills ONLY map 0
  +0x5A48..+0x5A59 with 0xFFFF; magic 0x5071901 rewritten;
  refresh copies map0->1 then map0->3 BEFORE clearing map1's
  tail — one-qword store @00326728).
  REVIEW-s28-slotmaps-battlestate.md
  (b) S-48 -> MET (rev 28470): scope key repaired to `subsystem`
  @3981ee43d, confirmed via knowledge_db.frontmatter (real
  parser, not grep). Substance byte-verified: setter 003B69B0
  (identity guard, steps==0 cancels in-flight ramp, byte
  counter, one-division delta), advance 003B5890 (0xA0 recs,
  gates [+0x40]&1 and ([+0x41]|[02B40524])&1, order 0,2,1,3,
  0x43, counter decremented only past both gates), gate writer
  003B6930 exact. REVIEW-s48-ramp-channels-3981ee43d.md
  Summary now 42 MET / 8 SCOPE-SHORT / 0 NOT MET.
  Prior round (rev ~28290, published 714451774 + 0569c11fe):
  twelve routed items closed:
  (a) S-11 -> MET: environment-variant contract @af0187f96
  byte-verified (EV-1 tail jmp w/ zeroed args, EV-2 cmovg clamp,
  EV-3 first-writer-wins latch, EV-5 band, EV-6 global census);
  all three pages contracted. REVIEW-s11-env-variant-af0187f96.md
  (b) S-20 stays SCOPE-SHORT: combo-continuation contract
  @0d5168cb2 VERIFIED (CB-1 width census 7/1-word and 64/4-byte
  exact, CB-3 two draws + branch past them, CB-4 nibble compare)
  but command seam + handler table uncontracted.
  REVIEW-s20-combo-continuation-0d5168cb2.md
  (c) S-22 stays SCOPE-SHORT: env-scaling contract @361c6b228
  VERIFIED (WE-4 three tests, WE-3 7-byte getters ->02099DA8/AC,
  WE-1 +0x13 mask); step table + recipes uncontracted.
  REVIEW-s22-env-scaling-361c6b228.md
  (d) S-28 stays SCOPE-SHORT: party-focus contract @017665504
  VERIFIED (022C7FE0 census 18/3W/1-install/0 lea; unlisted
  003594C0 confirmed; masks differ by bit 14 exactly); two pages
  still uncontracted. REVIEW-s28-party-focus-017665504.md
  (e) S-29 -> MET @5ea0cc557 (slot bits 7..5 of +0x07, bt/jb
  FORBIDDEN mask, +0x05 bypass, asymmetric partner test).
  REVIEW-s29-equipment-compat-5ea0cc557.md
  (f) S-30 -> MET @aae8061db (sole caller, pointer-identity match,
  last-entry fallback, count-closed/ptr-open, kind-2 zeroes elem).
  REVIEW-s30-shop-ladders-aae8061db.md
  (g) S-32 -> MET: all five pages now contracted (three added
  post-request); LC census 022C256C exact 17/8R/9W; GL/DR/LU
  spot-verified. REVIEW-s32-loot-chain-and-four-pages.md
  (h) S-41 -> MET: spatial-source @1afaa62de + bank/controller
  @d87f2ada5 verified (slot-34 postcondition, +0xE0 audibility,
  12 vtables, banks uniform 11 slots/52B dtor, controllers
  7/8/8/8/8/7 + 9B add+0x20 thunks).
  REVIEW-s41-audio-family-1afaa62de-d87f2ada5.md
  (i) S-47 -> MET @56b232843 (bit tests both sites, borrow stores,
  template or 0xc, 02F97340 census 60/45R/15W exact).
  REVIEW-s47-resource-ownership-56b232843.md
  (j) S-51 -> MET @5bc6b3b4b (different invalidation sets 3v2
  callers, 1.414 literal not sqrt2, 0030A130 no multiply).
  REVIEW-s51-navigation-5bc6b3b4b.md
  (k) S-02 -> MET: all three pages contracted (tick contract
  2a5eb4ff9 landed post-request); SS-1 zero bitset reads in 952B
  body + WT-3 census/single-ret + WT-5 immediates all verified.
  REVIEW-s02-tick-and-stop-registry.md (not yet written - the
  finish note carries the evidence)
  (l) FRONTIER REOPENED triage closed: all three pages have real
  obligations (vbf needs a pass over s2/3/4/7/10; file-schema needs
  crossref_clean cleared + s3b pass; middleware owes the EASTL doc
  + YEBIS read + scope-inheritance check per s11 'Still owed').
  TRIAGE-reopened-pages-2026-09-22.md
  TOOLING: linear whole-.text md.disasm aborts silently at the
  first undecodable byte without skipdata - returned 0 on a known-
  positive target. Per-function disasm over functions.tsv extents
  with skipdata=True is the correct sweep shape.
  Summary now 40 MET / 11 SCOPE-SHORT / 0 NOT MET.
  Earlier round (published 714451774):
  (1) S-09 .ard binder RETURNED (rev ~27799->closed ~27800,
  CONTRACT-ard-area-binder.md @32f49dc12) — AB-7 verified FALSE:
  `003EA820` holds FIFTEEN setter calls in THREE groups of five
  (003EA8AD-D5, 003EA8E5-90D, 003EA9B7-9DF), each preceded by
  call 003DCF00 (three such calls: 003EA8A4/8DC/9AE), and every
  group CLEARS categories 0..4 (edx=0) — the contract's 'ten calls
  in two groups of five around two calls' and its 'two directions'
  reading are both contradicted. The third group is in-body (ends
  before the tail jmp @003EA9F7). Record:
  REVIEW-s09-binder-32f49dc12.md. Row stays SCOPE-SHORT.
  (2) S-05 contract -> MET (rev ~27813,
  CONTRACT-shared-transform-workbench.md @e4681372a) — TW-1/TW-2/
  TW-3/TW-4/TW-6 byte-verified: region past .data SizeOfRawData
  (0x1F7E400), 46 distinct 16B-wide addresses all 16-aligned,
  003970A0's contiguous 4-row/64B copy, census EXACT (267 touchers/
  249 writers/18 read-only -> 16 pointer-slot + 00501820@+0xF0C +
  003970A0 sole matrix consumer), no rip-store to 022D94B0/4B4.
  Record: REVIEW-s05-contract-e4681372a.md.
  (3) S-11 contract VERIFIED but cell stays SCOPE-SHORT (rev ~27818,
  CONTRACT-authored-trigger-points.md @963fa2583) — TP-1 constants
  (10.0f, 1.2999999523162842f), TP-3/TP-5/TP-6 sites all byte-exact;
  TP-7's 'exactly two' independently rebuilt (66 RNG callers x 18
  flag callers = {002F8060,002FAFD0} only). Same ruling as S-07/
  S-09: the field-environment-variant page is still uncontracted.
  Record: REVIEW-s11-trigger-points-963fa2583.md.
  Summary now 32 MET / 18 SCOPE-SHORT / 0 NOT MET.
  Prior: S-43 contract -> MET (rev ~27746, CONTRACT-save-image-pipeline.md
  @a53b868f0 — all 6 invariants: 3x 0x566C0 gaps, both copies carry
  the post-jne 16B tail so 0xACD*0x80+0x10=0x56690 exact, six
  0x56690 sites in two layers, backup 022676C0 exactly one ref vs
  4/2/3 = read by nothing, guarded-vs-unguarded clears, handle-
  before-copy tail-call). TOOLING: C7 /0 store-immediate modrm
  filter undercounted the immediate sweep (3/6) — /0 is the reg
  FIELD, not the modrm byte range.
  S-09 contract stays SCOPE-SHORT (rev ~27750): contract verified
  (RA-4 sign-extended-offset confirmed, RA-3 both pairs, RA-5
  02B62E10, RA-1 single magic site) but the .ard binder is the
  gap's other NAMED half — per the S-07 ruling the cell needs
  every named part contracted.
  Prior: FABLE's close-out reply answered DONE (rev ~27689): both 002498B0
  contras verified applied at HEAD (four-site census incl. the
  00249C4D tail-jump; 'arms are ALTERNATIVES' wording) — BUT the
  board model only lets the ASSIGNEE finish a contradiction task,
  so both remain READY for FABLE to self-close (claim+finish); my
  finish attempts were refused by team.py. Nothing is short on the
  evidence side.
  Prior: both repair re-scores closed: S-19 contract -> MET (FABLE
  428db07d5 — refusal 6 'non-zero AND equal' verified vs
  test al,al/je @00314FFE/00315000; P-7's three arms verified
  eax=3/4/1 with the +0xED/+0xEE splits exact) and S-27 contract
  -> MET (FABLE 428db07d5 — sec1/sec7 prose now consistent with
  the byte-verified 50fb65cf8 core; THE BOARD'S LAST NOT MET
  CLEARS). Summary now 30 MET / 20 SCOPE-SHORT / 0 NOT MET.
  Prior: three FABLE re-scores closed — S-38 contract -> MET
  (rev 27645,
  CONTRACT-character-render-object.md @75041c609 — all 7 invariants:
  3x 0x668 sites, 2 vtable refs, 13 writes @+0x4B4 of which exactly
  2 byte-width = the one-way latch, 17 byte reads in 16 fns, 105
  insns/48 movups/0 bwd jumps, not-ready publish returns @001FB13A
  before every store) and S-07 contract -> MET via BOTH halves
  (interpreter core @22f7e359c — 100/100 in-body, 92 distinct, 3
  shared groups exact, V-5's flagged band re-derived len[0x47]=1/
  len[0x48]=3, all 21 sub-r14 cancels carry the same length lookup;
  lifecycle @fb3117aea — rep stosq+4 overwrites at slots 0/3/5/7,
  N-3 shifted row, tbl+32*count resolves 00342560/00510970/NULL,
  all 1960 fourth slots NULL). Criterion answer for FABLE: the cell
  moves only when every NAMED part of the gap is contracted.
  Summary now 28 MET / 21 SCOPE-SHORT / 1 NOT MET.
  TOOLING CAVEAT: a 20KB function-extent cap undercounts
  displacement sweeps (11/13 at +0x4B4) — uncapped gives 13.
  Prior: S-25 contract -> MET (rev 27588, CONTRACT-enmity.md @5c27a0920 —
  all eight invariants byte-verified: byte0 of BKEI+0x19 is the decay
  timer @0032158F vs table[id+1] reads @00321906; cmp byte[+5],1
  foe-gate at all three sites; three calls from 003216E0 with the
  third param negated @0032174B; -10/interval decay held while
  engaged; FrameLimit x 30.0f verified at 008F8D80; 0x80000003
  suppression + waiver 00313F60 + validator 00322C50 chain;
  existing-entry gate at 00321A73/79). Unmeasured items honestly
  named in §14. Summary now 26 MET / 23 SCOPE-SHORT / 1 NOT MET.
  Prior: S-24 contract -> MET (rev 27560,
  CONTRACT-stat-derivation.md @32208f36e — cap block, cmove cap,
  D-4 second store, three layer-test pairs, tail, eight-callee
  list all byte-exact) and S-19 RETURNED (rev 27568,
  CONTRACT-separation-pass.md @66f1cb3c5 — P-4/P-5/P-6 verified,
  but refusal-6 "or zero" clause is false (zero owner SKIPS the
  equality check at 00315000) and P-7's "counters do not advance"
  is false (moving body's +0xED increments at 0031525D/00315281)).
- **Prior:** S-27 round 2 RETURNED (rev 27511): FABLE's I-1 repair @50fb65cf8
  is byte-exact (ordered gate table, corrected I-1, postcondition
  names the 00310DE4/00310DEC unit writes — both verified), but
  two stale leftovers contradict it: section 1 "It changes nothing
  itself" and section 7's "deadline check -> six gates" sequence.
  Two-line repair; normative core verified, no re-measure needed.
- **Prior:** S-26 contract cell -> MET (rev 27500):
  CONTRACT-effect-layers.md
  @d31adce77 verified byte-exact — L-1 (rebuild +0x68 zero sites),
  L-2 (mutate 5x+0x68/6x+0x78), L-3 (0x80 bound + both layer tests
  + OR ctx+0x1A), L-5 (both id-15 revocation sites, bits 12/16/23,
  conditional +0x18 reset). Criterion ruled: a SECOND subsystem
  contract alongside the operation one suffices (S-34 precedent).
  Summary counts updated 24/25/1. Record:
  REVIEW-s26-contract-d31adce77.md.
- **Prior:** S-27 contract re-score RETURNED to FABLE — cell stays NOT MET:
  contract is subsystem-scoped with the right invariant shape and
  the spine/Regen-arm/RNG-sweep/timer-families/FrameLimit/counter
  claims all re-verified byte-exact, BUT I-1 is verified FALSE —
  gate 1 (stats block, cmp [rcx+0x698]@00310DCB je->epilogue
  003112D1) precedes the deadline check @00310DEF/DF4/DFC, so a
  stats-less unit's 0x40000000 flag is never cleared; "before any
  gate" and section 10's "I-1 has already run" both wrong. Needs
  "after stats gate, before gates 2-6" + section-10 rewrite.
  Record: REVIEW-s27-contract-60dedcfa0.md.
- **Prior:** published 23841913d + bdf1c5a89 (rev 27137).
  Shadow-audited while idle: FABLE's second arm correction
  3bb58a305 VERIFIED end-to-end
  (arms-as-alternatives wording now correct; its new "0022B6E0 has
  28 calls" claim byte-exact — 28 calls, single ret @0022B7DE) and
  OPUS's Lua two-type commit 85f6a8900 VERIFIED (LuaUserdata's
  0x30 corroborated by ctor 0081F050 + marker arm 0081AE7E
  independently; LuaLClosure n*8+0x20 stride + zeroing-loop base
  byte-exact). Records: REVIEW-fable-i1-arm-correction-3bb58a305.md,
  REVIEW-opus-lua-two-types-85f6a8900.md. TOOLING RECURRENCE:
  va2off must subtract image base 0x120000 — section VAs are RVAs;
  caught it via the known-00249C30 sanity check before trusting
  output (same failure shape as the earlier false-zero-ref scan).
- **Prior:** S-10 is the FIRST L2 MET ROW (rev 26924)
  — all five requirement cells MET; L2 cell + binding gap + stale
  "nothing is MET" intro updated; residuals (flag-bit meaning →
  readiness, live draw order → parity) named non-binding. Prior
  three rulings published 9d6b182d6 (rev 26920): S-10 types MET,
  S-35 contract MET (contra vs FABLE filed: 002498B0 has 3 callers
  not 1), S-13 types MET.
- **Prior:** S-01 types → MET (rev 26880). Residual
  slots DECLARED by OPUS and verified: BootAllocationSlot01FD4A20/
  4A90 — ref counts image-wide exact (1 write-only ref 0022A284 /
  3 refs: write 0022A2A3 + reads 0040AF65/0040AFF2 inside 0040ACF0);
  sizes 0x80000/0x100000 measured in 0022A0B0 beside the nine-
  registrar loop; both BSS. Ruling: slots satisfy the cell — §14
  holds pointee identity unresolved, so slot coverage is the named
  granularity and pointee interiors are quality debt (readiness),
  not coverage. S-01 §5 denominator complete. Record:
  REVIEW-s01-residual-slots-declared.md.
  TOOLING SELF-CORRECTION: an earlier scan this round falsely
  reported zero refs — my .text slice was RVA-indexed while
  functions.tsv/GZF addresses are full VAs (base 0x120000
  included). Re-run VA-indexed; all claims verified.
- **Prior:** S-01/S-46 RE-SCORED (rev 26803). All five
  scalar declarations verified byte-exact — latch is u8 (OPUS's
  correction stands; my "u32" was wrong: 6/6 accesses byte ops).
  Denominator answered: 02089300 inside it. S-46 types → MET (first
  under ruled criterion). Pool registry verified (0022A0B0 calls
  00369D30 ×9; 00369D30 = 022D7FD0+id*0xA8 = ImageAddressArenaRecord).
  Record: REVIEW-rescore-s01-s46-scalars.md. Published e34f44777
  (rev 26867-68).
  Shadow audit while queued: OPUS's three PApplication/PBase
  commits (87b77df84/39b315037/247488a28) verified — parsed RTTI
  directly: both classes' own COLs show attrs=0 nbases=3 chains
  PBase@+8/PMemoryBase@+8 (single inheritance, retraction correct;
  the 13-base read is the descriptor class's vtable, not the
  object's); zero COLs reference PBase's TD 01F475C8;
  PAnimationHierarchyNode 0x10 + PBase@+8 bounds the subobject
  ≤8 B. Record: REVIEW-papplication-rtti-retractions.md.
- **Prior:** types-MET criterion ADJUDICATED (rev 26781,
  P1 delegated from AUDIT-SPEC). Criterion ACCEPTED with two
  precisions (scalar state counts at named granularity; denominator
  = contract's state enumeration, vacuity → unscorable). Applied
  literally: S-46 → PARTIAL not proposed-MET (§3 names counter
  0208E6B0, undeclared — one u32 row closes; DAT_02089300 boundary-
  case second); S-01 → PARTIAL (PApplication carve verified — 93
  rows, fixedTimestep imm at 0079F25D behind ucomiss-zero guard,
  00874320 = 7×0x10; but §5 scalars 02EB4234/01DFE0B4/02064ACC
  undeclared; pool registry reads as ImageAddressArenaRecord,
  noted not fully verified). All OPUS measurements re-derived
  byte-exact. Ruling in _index/L2-VERDICTS.md + both cells updated.
  Record: REVIEW-types-met-criterion-ruling.md. Publish the file
  + this block, then poll for routing.
- **Prior:** three routed ASTRA reviews closed ACCEPT
  (revs 25750/25760/25763): s44-rebind-discriminator (materializer
  extents 192/768/16 B, swap-gate direction, writer +450-as-path,
  240-node registry, rival-framing 95/95 — all byte-verified);
  camera-rng-discriminator (5×4 owner/driver population, full
  eligibility chain, sentinel ordering, entry-ID vs bank-index
  split, clear-preserves-ID, 3+2 sites in alternative branches);
  old-save-start-p (independent decode of FFXII_004, 40/40 bank0 +
  prefix + levels + keep counts + 220/1572 diffs recomputed from
  raw; rejected sample genuinely invalid; screenshots confirm
  presentation). Records: REVIEW-s44/camera-rng/old-save-start-p.
  Both pending contras closed by producers — EQCOUNT-7095 and
  COVDIM-6D-SUM marked DONE and re-verified at HEAD (ff2b22c6f
  "7,086" + nine-record explanation; 6cc3939be "27,175 B — 69%").
  Published 5c886eb7 (rev 25765).
- **Prior:** both DATA contra repairs (`81278ca35`)
  re-verified at HEAD — record `REVERIFY-data-contras-81278ca35.md`.
  SEQREC u16 correction verified exact (4,078/4,097 single-sound
  banks reproduced; TSV regen byte-identical); LISTTYPE type-6
  mrppack scoping verified exact (46 = 10×unit01 + 4×9×unit21).
  BUT the repair cites '7,095 of 11,165 equal the chunk position' —
  that is the stale u8 count; at the corrected u16 width it is
  7,086 (generator's own print agrees; nine-record delta
  enumerated: se010305/se100259/se600278/se602281/se604279/
  se606268/se607280/se608273/se609286 all carry +4=0x0100).
  New contra `AUDITSEM-CONTRA-DATA-SEQREC-EQCOUNT-7095` filed
  (rev 24173) — one-number fix. Also resolved: the stray '11,167'
  seq-record figure was an ad-hoc artifact — three independent
  walks all give 11,165 and zero non-.sab seq records exist.
  `sead-library-span.tsv` working-tree change is a producer's
  regenerated census (in-flight re-scoping), not scratch.
  Publication still blocked: `@publication` held by
  FABLE-PUB-THE-OWED-EFFECT-PAGE-EDITS + two OPUS tasks
  (rev 24183) — publish this round's records once it frees.
  Queue otherwise empty — poll for new routing; re-verify
  the EQCOUNT repair when it lands.
- **Pending requests/reviews:** none open. Both recent contras —
  SEQREC-EQCOUNT-7095 (SWE2-DATA) and COVDIM-6D-SUM (SWE2-FRONTIER)
  — are DONE and re-verified at HEAD.
  The two prior DATA contras (SEQREC-KEYID-SEMANTICS,
  LISTTYPE-TYPE6-MRPPACK) are DONE and re-verified. The 13
  contras formerly listed here (IMPORT-EIGHT, 3703A0, THUNKROOTS,
  22A770, FN2-PLUS100, UG2-CALLERS, EE-MEMBERS, RESIDUAL-109,
  OSCILLATOR, SWFAM-4TO8-ADDENDUM, and the rest of the
  rev-84xx-96xx set) are all DONE on the board; history retained
  in the 'closed' list below.
- **Pending requests/reviews (closed):** AUDITSEM-CONTRA-FABLE-BI11 (rev 9611) —
  UPHELD by FABLE, repaired in be99d4c0 + 32511f8d, re-verified PASSED.
  AUDITSEM-CONTRA-FABLE-EA3-29 (rev 9489) — UPHELD, '3/107' now matches my
  census, '29 hoisted' dropped; re-verified PASSED.
  AUDITSEM-CONTRA-FABLE-RS2-C0 (rev 9476) — UPHELD, 0042A430/+0xC2,C4 and
  0042B310/+0xC0,C2,C4 split now matches the bodies; re-verified PASSED.
  AUDITSEM-CONTRA-FRONTIER-RENDER-VTABLE-DUP (rev 9393) — repaired 3080b69f,
  six deduped cells match the bodies; re-verified PASSED.
  AUDITSEM-CONTRA-FABLE-BU1-NINE (rev 9585) —
  UPHELD by FABLE and repaired (DONE): 'nine of the 16 targets' was 8 under the
  all-branch census; page corrected.
  AUDITSEM-CONTRA-FRONTIER-HUBS (rev 8173) — two defects
  (003DBB60 remap is 1→0, 3→2, else keeps r9+flag; 00387B00 tables are 0208D480/0208DE80 not
  020BD480/020BDE80). Also recorded: my earlier /150 counter-evidence was wrong — FRONTIER's
  /1000 repair is right.
  AUDITSEM-CONTRA-FRONTIER-AUDIO-SLOTS (rev 8138) — nine named
  defects (slot-0 calls own vtable not entries'; Music slot-0 manager calls misattributed;
  01FD36C0 not 01FE36C0; quotient-not-modulo; AND-vs-OR in Seb slot 9; slot-10 five-bit mask;
  Music slot-2 base tail; Stream slot-4 indirect calls; +0x50 gate on Sep slot 5).
  AUDITSEM-CONTRA-FRONTIER-EFFECT-TYPES-2 (rev 8106) — nine
  named defects (queue array is 02091150 not 02092150; loop-as-single-call misreads in
  0x67/0x65/0x66/0x70 setups; 0x61 count; 0x40 map; 0x41 phantom 1T; family-B omits
  1T@+0x190; duplicate "largest walk"; 00457FE0 third path).
  AUDITSEM-CONTRA-FRONTIER-EFFECT-TYPES-00-0A (rev 8004) —
  six defect classes back to FRONTIER (base setup rebases FOUR heads at +0x00–+0x30 not
  three; update-56B and step-43–310B universals break on 0x02; helper order inverted —
  tails run second, extras after; 0x0A's 0044C850/0044B960 swapped; setup field maps wrong
  for 0x04/0x05/0x06-07/0x08/0x0A incl. the 00431770 4× loops; 0x01 walk writes 02AEE908/
  02AEE900 not 02AE2908/02AE2901). AUDITSEM-CONTRA-FRONTIER-MENU-SCREENS-2 (rev 7945) — one
  named defect back to FRONTIER (handbook id-16 gate inverted: 005738D0 builds on bit
  +0x11D0&1 CLEAR, dims path is the bit-SET branch). AUDITSEM-CONTRA-FRONTIER-MENU-SCREENS-1
  (rev 7883) — five named defects back to FRONTIER (quest-list global is 02CA9738 not
  0x7CA531; GEN-RECONCILE runs on all-slots-clear not "any still set"; license index is
  0x7E not 0x85; gambit 0x121 is sent by the destroy arm not construct; editor table is
  00569F1C).
  AUDITSEM-CONTRA-FABLE-EFX-REGISTRY (rev 7833) — narrow repair
  routed to FABLE: 02EBEF88 has 11 writers not 10 (003B8260 missed; propagate to
  effect-element-type-dispatch §2.4), trio are -1-sentinel replace-loops not spawn→set→remove
  triples, "all callers are UI code" needs scoping to the two BattleStats_* callers.
  AUDITSEM-CONTRA-FABLE-RESIDUAL-XREF (rev 7361) — TSV regen + figure restatement pending.
  FABLE-REQ-SWE2-EC7-MKVPARSER-REPAIR — re-verify 100→105 when it lands.
- **Fallback eligible work:** next review-ready semantic package, else another shadow audit
- **Latest coherent commit/checkpoint:** board rev 24162 — three EXP
  reviews closed this round (see 'Exact next action'). Prior: `0040e86b`
  (three repairs PASSED + DQ-2
  ACCEPT). FABLE `3b57c71e` ANSWERED-row pass spot-verified byte-exact:
  `007F1BF8`–`007F1C23` is a full distance computation (subps/mulps/haddps²/
  sqrtps → comiss vs `[rbx+0xE4]` → setb into `+0xE0`); `007F1960` slot-7 init
  reads `[rdi+0x18]` → `[rbx+0xE4]`; `005A6670` is the lazy-descriptor shape,
  `PE_RESULT` string count = 0, vtable `00D311B0` is stored.
- **FRONTIER-REQ-AUDITSEM-RENDER-DIRTY-BITS (`95726a70`): ACCEPT-WITH-NARROWING,
  finished rev 9863.** 56-block/52-handler census of `00427DE0` reproduces
  byte-exact (test sites include register-form `bt eax`/`test al` chains and the
  `cmp; jge` sign test); setter census exact incl. the 20-writer `or 0x800` family
  and all bts+store/group-write masks; no-setter lists and dword-only RMW
  confirmed; `00427BD0` chain walk and 9-byte `003E74B0` exact.
  `AUDITSEM-CONTRA-FRONTIER-DIRTYBITS` (rev 9862) routes: esi caller names wrong
  (actual `0042ED60`→ecx=1 / `00426090`→ecx=0; `00428710` is a *callee*);
  `00427280` clears {5,7,8,10,17} not {5,7,8,15,17} (phantom 15 in union); two
  zero-reference writers (`0042EE10`, `00520430`) omitted from the "whole-process"
  census; clear_site `004282CE`→`004282D3`; prose 42 vs TSV 40. Board rev 9863,
  queue empty for this lane.
- **FABLE `6a65bc9b` music-fade unit — clean ACCEPT.** `00222B70` verified:
  `cvtdq2ps` + `divss [008F6D54]=60.0` (length) and `[00906A44]=127.0` (volume),
  `call 007A81F0`. `007A5400` is the audio-thread loop: `007AD630` (QPC minus
  epoch) − cached tick, `cvtsi2sd` + `jns`/`addsd 2^64` (`00D27A68` = 1.844e19)
  unsigned fixup at `007A546C`, `divsd` by `007AD670` (cached freq `02EAD0C0`,
  filled by `007AD6D0` QPF), `cvtpd2ps` → `007AB5C0`/`007AAEA0` at
  `007A54AA`/`007A54B2`; stores new tick at `007A548C`. Chain
  `002DEE50`→`001DBCA0`→`00210A50`→`00218E50`→`00222B70` each sole-caller exact.
  SEAD span TSV 1197 rows + header ✓.
- **FRONTIER `6973beb4` wm_members §4 — ACCEPT-WITH-NARROWING.** All 108 member
  rows present; 18/18 sampled interior cites land byte-exact; the §2.6
  correction verified (`003C2200` → `jmp 003C26C0` at `003C2209`; `003C26C0`
  populates `+0x18`-based children via `0024A9E0`/`0017D2E0`/`0024A480`).
  `AUDITSEM-CONTRA-FRONTIER-WM-COUNTS` (rev 9970): the loc+track section heading
  says (30) but the table holds 31 rows; flt says (14) but holds 13 — one
  misplaced row or stale parens (total still 108).
- **FABLE `8a82b459` EFX type-4 census — clean ACCEPT.** `0024C460` 17 refs,
  `0024C550` 5, `0024B3A0` 6 — all exact; type-4 passed only at
  `003B28F9`/`003B2A2D`/`003B2BAD` (+`0024C550` at `003B2A37`/`003B2BBB`); the
  six context-build byte writes (2,1,5,7,4,3) at the cited addresses exact;
  `003B28F0`/`003B2B40` caller lists byte-exact.
- **Repair re-verified:** `AUDITSEM-CONTRA-FRONTIER-DIRTYBITS` fix PASSED (applied
  via `d4f57433`, bookkeeping commit `47ee64ac`). All five items corrected
  in-tree: callers `0042ED60`(ecx=1)/`00426090`(ecx=0); mask `{5,7,8,10,17}` and
  union `{0,1,5,7,8,10,17}`; dead writers `0042EE10`/`00520430` named;
  clear_site `004282D3`; prose `40`. Closed (rev 9995).
- **Repair re-verified:** FABLE `c83eeadf` BU-3 correction PASSED byte-exact —
  all five +0xA0 rows land exactly (0028E4BF→003F8EC0, 0028EBD4→003F8C70,
  0028FA80→003F8EA0, 0028FB11→003F8EC0, 0028FB47 tail-jmp→003F8D20); both
  excluded sites confirmed +0xA0D0 (0028E43D lea [rbx+0xA0D0], 0029045E add
  0xA0D0); missed-user claim verified: 003F8C70 gates on [+0x52C6]&1 and walks
  [+0x52C0] records shl-8 from +0x20 through 003F1290 at 003F8C7F–003F8CCE.
- **Shadow verification (not routed, already DONE on board):** FABLE `5648e038`
  GN161 provenance-transfer ruling reproduced end-to-end —
  `provenance_transfer_gn161.py` re-run gives 128/124/109 deltas, all additive
  (empty plate + tag subset), and the exact cohort split 65/12/2/163; the two
  CENSUS-REVIEW flags independently confirmed (`residual_addrs.txt` = 30 entries
  = "GN161 leaves 30"; the 93-verbs page's untagged figure is generation-bound
  since 94 of the 109 GN160 deltas were tagless-before; "111 of 128" tagless
  verified). OPUS `0e802a21` field batch sampled — `0x41C` bit-pattern typing
  (0x3C360B67 = 1/90) and `0x3CC` three-reads-in-one-function both exact.
- **Exclusive-subtree batch — 23 requests closed (revs 12242–12288).** Method:
  `subtree_batch_audit.py` — member/size extraction per section, sizes vs
  functions.tsv, exclusivity via call_graph over the shipping image, interior
  cites disassembled + normalized (rip targets resolved). **21 clean ACCEPTs**:
  001E8580 (21), 00336CE0 (19), 0032E070 (15), 0026C8C0 (14 — every member
  root-only-called), 001B4D70/001BBFC0/002E5750/00304850 (13), 001C7940/002342F0/
  002E28E0 (12), 003692D0/005A08E0+CORRECT (11 — 005CC980 timer + 00637F20 TLS
  arms + 00686C40 21-init/6-factory structure confirmed, 6th registrar call
  nested in 00612550), 001EDDC0/00226640+CORRECT/0027FB70/-SUPP/0031EB20/
  00362850 (10). **2 ACCEPT-WITH-NARROWING**: 00253C70 (22 — nit: 002B6249 cite
  folds `mov ecx,0x500`+`or [rax+0x179D2],cx` into `,0x500`); 001A7A50 (10 —
  nit: `001BD7E0` is `001A92C0`'s callee via site 001A93C9, not `00185A90`'s;
  `00185A90` rightly excluded — outside callers 00183720/001B6A70). Contra:
  AUDITSEM-CONTRA-FRONTIER-SUBTREE-NITS (rev 12242). Spot-verified extras:
  0027FB70 is a widget proc — zero direct callers consistent (lea-installed by
  00280A00 at 00280A6F/00280A85); msg dispatch `[rdx]`→msg1/2/18 arms + tail
  005C5230 exact; 00244F50 factory correction verified (0x70×0x120 pool
  0208EA58, alloc 002497B0); 00226640-CORRECT flag semantics `&~0x200|0x100` vs
  `&~0x100|0x200` + `lea r14,[02EBEC08]` in both walkers byte-exact; 0031EB20
  root callers = 15+self = doc's "16 UI callers, recursive". Record:
  `Tools/work/SWE2-AUDIT-SEM/REVIEW-subtree-batch-23.md`.

- **Switch-families formal review — ACCEPT-WITH-NARROWING (rev 12354).** All 450
  `switch-family-frontier-decode.tsv` case→arm rows reproduce byte-exact across
  12 dispatcher tables (7 direct RVA-dword, 3 two-level byte-index `0028144C`/
  `00277854`/`00282590`, inner `003A5578`/`003A691C`/`003A5618`/`003A69BC`);
  165/165 named-handler bindings confirmed by full sweep. Sizes, dispatch heads,
  caller graphs (002F3360→003A56F0, four 00537xxx tail-jumps→003A4290, 00523380×2),
  destroy-first loaders, record-store fronts — all verified. Two defects routed via
  AUDITSEM-CONTRA-FRONTIER-SWFAM-STATEMAP (rev 12351): **0035CA70 §2.6 state column
  is numbered in arm-address order, not by the +0xC0 selector** — all 14 rows
  mislabeled (each row's work/next-state is right for its arm; real map in resume
  block); **§7.1 id-14 arm 00280EC3 role wrong** — `002CE980`+`00291D50` is id-16's
  head (which then runs a ~12-call battery and falls into id-14's body); real id-14
  is the `+0x280` bit-1 gated `0x8001`/`0x8000` re-dispatch + `002CFCF0` + `00246AD0`.
  Minors: `+0xC0` dword-width in 00280DE0/00281ED0 (not "state byte"); 00442170
  subtype-0 reset leaves +0x8C–+0x8F untouched; 00375500's `00375470` epilogue is
  skipped on nonzero handler result. Record:
  `Tools/work/SWE2-AUDIT-SEM/REVIEW-switch-families-09a13795.md`.

- **NOCALLER-INSTALLERS + -2 — both ACCEPT-WITH-NARROWING (revs 12427/12429).**
  Every mechanical binding byte-exact: combat step-table 52/52 slot→body bindings
  and interior cites (the four graph-edge members are installer-table indirect
  calls through `01EFA5C0`, not direct callers); character-render 9-cite boundary
  repair verified against real extents, old cites confirmed next-function;
  `004269A0` all 25 id↔handler regs exact (bank-A `0041D6C0`, bank-B id5
  `0041D6D0`, singleton `0041D6E0`→`02CA4668`); `01EFFAF0` 75×16 pair table +
  `&0x7F`/`0x4B` clamp + flag-suppression + `call qword[base+id*16]` all exact;
  `002EA320`/`0036C5A0` regs exact; `006349B0` **teardown-thunk reading
  CONFIRMED** — 11 lea sites each → `call 00808B90` (atexit), eleven identical
  103-B destructor bodies (vtable re-stamp `00D580B0` + `+0x48` virtual +
  `006B6700` unlink + `00584730` flag-gated free), zero callers — destructors,
  not initializers; `01E0C490` 15-slot shop dispatch exact (incl. kind-6→7 remap
  behind `002CCB00`, kind-0xA `0x8060`–`0x81FF` range gate); `01EECFC0` 5×4 mode
  matrix exact (same-mode cols 0/2 via r14∈{0,2}, leave cols 1/3 via
  `(ebp?0x18:8)` cmovne, sole two refs in `0030D8B0`, 7 members caller-free);
  `00900F20` vtable + RTTI chain → `basic_stringbuf<char>` exact, sole code ref
  `001DE45A`; `01F00398` table 15 slots + selector adapters exact; `00378540`
  seven publishers all 10-B `mov eax,ecx; mov [rip],rax; ret` byte-exact;
  `interior_cite.py` owner-extent logic sound. **13 prose defects routed** as
  AUDITSEM-CONTRA-FRONTIER-NOCALLER-NITS (rev 12426): `00417DE0` "reads
  bank-A[0x3E] `02CA4600`" false (zero calls in body); `01EFFAF0` ids 0x49–0x4B
  invoker = NULL not `0016D6A0`; "self-call" rows are interior `jmp` targets;
  shop kind-3 remap yields edi∈{0..5} not {1,3,4,5}; shop slot-9 IS the 147-B
  context-fetch twin (twins = 9/10/12; slot-14 `002956B0` = 106 B distinct);
  "slots 4/5 have direct callers" false (zero E8/E9 image-wide); `008C5760`
  vtable slots 16/25 swapped (actual 16=`0017D210`, 25=`0017D1E0`); "`00378B90`
  has a direct caller" false (all seven lea-installed only); member-registration
  cells `02CF9320`/`02CF9380` should be `02CF9330`/`02CF93A0`; `0031373C` cite
  fold (`and…,cx` fed by `mov ecx,0xFFFD`); dyngeo "fifteen shared" is sixteen;
  unowned "fifteen handler entries" is fourteen. Record:
  `Tools/work/SWE2-AUDIT-SEM/REVIEW-nocaller-installers.md`.

## Checkpoints

Append below, newest last. Record corrected facts and remaining work, not file growth.

### 2026-09-13 — shadow audit: arena selection stack (FABLE-ARCH-ARENA-SELECTION-STACK, 8965e28c)

Queue held nothing for this lane; audited the newest universal/family semantic claim.
Independent re-derivation from the authorized EXE (hash verified), four reference-form sweeps
(E8, E9, rip-memop, image-base-indexed, immediate, data-qword) and a site→function pairing check.
Scripts + full review: `Database/Tools/work/SWE2-AUDIT-SEM/` (`arena_stack_census.py`,
`arena_pairing_check.py`, `arena_indexed_refs.py`, `arena_imm_data_refs.py`,
`REVIEW-arena-selection-stack.md`).

**Disposition: REJECT — named defects for producer repair; verified core stands.**

Reproduced exactly: 135/109 push, 153/111 pop (19 tail-jumps), 21/18 byte-stack pairs, sole
0036C1F0 referrer, pop-only set = {0052A130, 0052ADF0} verified in bytes, literal `jmp $` spins,
record layout, category stamps (three sites, doc named one), tag global has **no consumer in any
form** (upgrades the doc's hedged negative).

Defects filed as AUDITSEM-CONTRA-FABLE-ARENA-STACK: tag is `[rsp+4]−5` straddle, not the
call-site address; initializer stores 0 (not "its argument") and is first-init-gated by
022D89B8; byte push overflows by silent no-op and byte pop at depth 0 installs 022D8DCF then
goes negative; map is only ever identity-written (id **is** the index) with an unchecked
sign-extended index and a null+2 crash path on mapped id > 14; allocator hangs when r8==0 and
depth==0 — the enforcement behind push→alloc→pop, unrecorded.

**Follow-up:** FABLE repaired D1–D6 the same evening (board ~719x); auditor re-verification
PASSED with byte checks, including FABLE's refinement that the init gate is whole-mask-zero
(`test r9d,r9d` at 00369D6E), not the per-bit form I filed. Record:
`Database/Tools/work/SWE2-AUDIT-SEM/REVERIFY-arena-repair.md`.

### 2026-09-13 — queued T2 review: libwebm mkvparser EC-7 family (SWE2-EC7, caaed3c4)

Reviewed the 100-member family: re-ran `select_mkvparser.py` (110 entries in run,
44 seeds, 97 in-run + 3 RTTI-scattered = 100 = TSV), replicated its sets with an
independent E8/E9 + rip-lea census (`mkv_audit.py`), and verified every exclusion
bucket and both boundary controls against the shipping image. Scripts + review:
`Database/Tools/work/SWE2-AUDIT-SEM/` (`mkv_audit.py`, `mkv_eh_verify.py`,
`REVIEW-mkvparser-family.md`).

**Disposition: ACCEPT-WITH-NARROWING** — membership, boundary, fingerprint all verify.

Verified: inbound callers only `0067xxxx` (25 sites); outbound only CRT
(`00210EB0`→`jmp 0019C590` = the `free` thunk; `00210EC0`→`jmp 0085E730`;
`00809948/50/58`, `00861EBA` = import/forwarder thunks; `00808xxx–00809xxx` tagged
MSVCCRT/STL). Eight `mkvparser::` vtables + Matroska element IDs real; zero
`mkvmuxer` RTTI. Api-admitted bodies are genuine small member getters/lookups
(e.g. `008028A0` = linked-list lookup on `[+0x24]`, GetTrackByNumber-shaped);
`00803190` is a real API body driving parse pump `00803230`. `008087C4` exclusion
correct — sole caller `008B905C` is a registrar-zone linked-list teardown.

**Narrowing (D1, prose repair for SWE2-EC7):** the five bodies
`007FFCD0/7FFD00/7FFD80/7FFDA0/800150` are **not** "unwind-action dtors serving
006Exxxx frames". Whole-image RVA32 scan: they appear only as `.pdata`
BeginAddresses (007FFD80 appears nowhere); their unwind infos are `flags=0` at
01D529D0/01D6B7C8 — no EHANDLER/CHAININFO; and the EH data at `01DDE4xx` points
INTO the run (235 RVA32s, members' own IP-to-state data), zero into
006E4xxx–6xxx, zero into the five bodies. They are orphan dtors — "joined by
nothing" is literal. `007FFCD0` even calls member `007FFF60`. Routed to FABLE
for T2 adjudication (AUDITSEM-ADJ-FABLE-MKVPARSER).

**Adjudication postscript — my narrowing was itself wrong.** FABLE ruled ADJUST:
the five bodies ARE members (family 100→105). Each is `jmp`'d from an
`Unwind@008A5B30-70` funclet (outside the census population —
`cd.load_functions()` drops `Unwind@`/`Catch_All@`, so my `owner_of` census
silently dropped the edges and they looked orphaned), each funclet is an
unwind-map action (`01DDE508/4B8/464/554/678`), and the owning FuncInfos belong
to member frames `008041F0/00804BE0/00808040/00804CF0/00808240` — all in the TSV.
Producer's "foreign 006Exxxx frames" was wrong; my "orphans" was wrong; FABLE's
"member dtors of member frames" is byte-verified. Instrument lesson recorded in
the review file. Repair routed to SWE2-EC7 (FABLE-REQ-SWE2-EC7-MKVPARSER-REPAIR)
— re-verify when it lands.

### 2026-09-13 — ledger causes: 76 UNSUMMARISED records given causes (FABLE-REQ-AUDITSEM-LEDGER-CAUSES-76)

Read each record's corrected document text (context windows extracted to
`Tools/work/SWE2-AUDIT-SEM/ledger_causes_ctx.txt`) and wrote the `correction`
description + `instrument` slug for all 76 rows CON-038–CON-113 in
`_index/CONTRADICTIONS.tsv`. Only the two permitted cells touched;
`contradiction_index.py status` now reports 113/113 with written correction and
named instrument, UNSUMMARISED 0. Slugs reuse the existing vocabulary where it
matched exactly (`signedness`, `false-symmetry`, `wrong-record-frame`,
`recount`, `no-reader-found`); new slugs name the failing instrument or reading
step (`thunk-hidden-edge`, `unread-callee`, `captured-input-as-producer`,
`register-liveness-bug`, `absorbed-input-generalised`, `non-inert-control`,
`import-slot-adjacency`, …). Apply script retained at
`Tools/work/SWE2-AUDIT-SEM/apply_ledger_causes.py`. No bounded remainder — the
task is complete. DONE at board rev 7306.

### 2026-09-13 — shadow audit: FABLE residual crossref (f8e0716d, the-unresolved-158 §14)

Claim: 50 of 139 residual functions cited elsewhere (22 interior), real AC-1 backlog 89.
**ACCEPT-WITH-NARROWING** — method independently reproduced; every sampled cite is a
genuine code address (no coincidental-constant hits). Narrowings filed to FABLE as
AUDITSEM-CONTRA-FABLE-RESIDUAL-XREF (P3): (1) the backtick-only regex misses real cites —
one genuine interior cite found in the Residual README code listing — while accidentally
dodging two coincidental numerics (range bound, rip displacement); (2) the figures already
drifted to 53/23/86 via the same-day menu-effect-registry page; (3) a residual-folder
README self-cite counts as "another page". Core conclusion stands on either count.
Artifacts: `Tools/work/SWE2-AUDIT-SEM/REVIEW-residual-crossref.md`,
`residual_crossref_audit.py`.

### 2026-09-13 — shadow audit: FABLE menu-effect-registry (b17e1430)

Queue empty again; audited FABLE's newest semantic page (64-record UI effect registry, type-4
EFX pipeline). Independent disassembly of all six routines + a fresh rip-relative census of
`02EBDBC0`–`02EBE5C0` and a writer census of `02EBEF88`
(`Tools/work/SWE2-AUDIT-SEM/efx_registry_census.py`, `REVIEW-menu-effect-registry.md`).

**Disposition: ACCEPT-WITH-NARROWING** — the mechanism verifies byte-exact:
64×0x28 records, id@+0 (0=free) / instance@+8, compacted-prefix early-out scans, reset clears
records + `02EBE5C0` with `0024C460(4)`/`0024C550(4)` and an `0x890` type-4 template through
`0024B3A0`/`003EDAD0`; spawn mints `(counter&0xFFFFFFF)|1<<30` ids, releases the instance on
no-free-record; remove-by-id releases via `0024EE60` and compacts with a `02EBE598` tail-clear;
set writes `inst+0x338` null-guarded; **exactly ten functions** reproduce under my own census;
all named callers verified incl. six `003B2AA0` sites in `00557DB0`.

Narrowings filed as AUDITSEM-CONTRA-FABLE-EFX-REGISTRY (P3): (1) `02EBEF88` has **11**
writers, not ten — `003B8260` (`003B860D`) missed, and the same count is stale in
effect-element-type-dispatch §2.4; (2) the trio are `-1`-sentinel remove→spawn→set
**replace-loops**, not spawn→set→remove triples (measured-from-a-listing); (3) "all callers
are UI code" is evidenced only for `00557DB0`/`005588C0` (named `BattleStats_*` callees);
minor: `003B2930` unregisters without releasing (`0024B580`/`0024B9B0` teardown callers).

### 2026-09-14 — queued review: FRONTIER menu-screens-1 (three pages)

Full independent re-derivation: all dispatch tables dumped from the image (005774E8, 0055DB2C,
005594E4, 0056BB80, 00569F1C), arm bodies disassembled, nine child procedures proven
single-installer by rip-relative census. Result per page:

- **quest list** — named defects: published global is `02CA9738` not `0x7CA531` (a .text
  address, nowhere else in the DB; child reads `02CA9738` back at `005759EE`); GEN-RECONCILE
  teardown runs when **all three** child slots are clear AND `(+0x100&6)!=6` — "if any child
  slot is still set" is inverted.
- **license board** — one defect: index at `0056165F` is `7+0x77=0x7E`, not `0x85`.
- **gambit** — named defects: `{0x121,0,0}` is sent by the id-18 **destroy** arm
  (`0056B51F`–`0056B549`, gated `+0x58E`), not construct; editor table is `00569F1C` and
  `0x121` is a dedicated `cmp eax,0x121/je 00569EE3` pre-table arm, not a table entry.

**Disposition: REJECT** (per-page named defects; repairs routed to SWE2-FRONTIER as
AUDITSEM-CONTRA-FRONTIER-MENU-SCREENS-1, rev 7883). Review:
`Tools/work/SWE2-AUDIT-SEM/REVIEW-menu-screens-1.md`.

### 2026-09-14 — queued review: FRONTIER menu-screens-2 (five pages)

Full independent re-derivation: dispatch tables dumped (0057552C, 005733A0, 0056FA80,
0057CCA8, 00570410, 00554A18), equality chains walked, and installer ancestry re-derived by
rip-relative `lea` census for all **37** claimed edges (25 unlabelled + 7 save/load +
5 world-map §6a) — zero mismatches, including both dual-installer rows. Result per page:

- **handbook** — both dispatch tables byte-exact, construct stores and id-18 resource
  lookup verified; one defect: the id-16 refresh gate is **inverted**. `00572F23
  test byte[+0x11D0],1; jne 00572F74` — `005738D0` builds on bit CLEAR (fall-through),
  dims path is bit SET. Page has it backwards.
- **shared dialogs** — clean: bounds/tables for `0056F810`/`0057C480`, singleton store
  `[rax+0x328]` at `0057C4D9`, chains for `00556F90` {1,2,18} and `00566680` {1,2,12,15,18}.
- **unlabelled panes** — clean: all 25 installer edges exact; `00560910` 20-id bound and
  subtree calls `00561300`/`00558F20` verified; kind-byte compares at `00571ABD`/`00574373`.
- **save/load** — clean: all 7 installer edges exact with the named `SaveLoad_*`/`SaveWrite_*`
  owners; `0057F360` id-12 gate (`msg->a==0x1D ∧ [msg->b]==0xD`) verified.
- **map §6a** — clean: all 5 installer edges exact; id sets {1,24}, {1,14,24}, {1,4,24},
  {1,4,18} and `005542D0` live {1,2,10,12,14,15} all byte-exact.

**Disposition: REJECT** — single named defect to SWE2-FRONTIER
(AUDITSEM-CONTRA-FRONTIER-MENU-SCREENS-2, rev 7945). Review:
`Tools/work/SWE2-AUDIT-SEM/REVIEW-menu-screens-2.md`.

### 2026-09-14 — queued review: FRONTIER effect-types 0x00–0x0A (group 1)

First producer pass over the 195 effect-type handlers. Method: scripted setup-sequence
extractor (call target + `lea rcx` offset per call) over all six derived setups + the base,
plus `disasm_fn.py` reads of every helper/step/update and a size census from functions.tsv.

**Verified:** helper bodies byte-exact (`004304F0`/`00430AF0`/`0042FCF0` = 1/3/4-head
rebasers; `00431040` = `00430A60`×3 under xmm1; `00430A60` = two `{u32,f32}` keyframe
arrays per head, counts `+0xC`/`+0xD`; `00431580` = imul variant on edx arg). Thin steps
(base→tail) and 56 B updates (same tail as step) verify for all thin types. Setup maps
for 0x01/0x02/0x03 exact, incl. the 0x03 load-time unit rescale (×f on three groups +
×0x64 on +0x180). 0x06/0x07 share `00538EB0`.

**Defects:** (D1) base `00500470` rebases **four** heads at +0x00–+0x30, not "three at
+0x10–+0x30". (D2/D3) the §1 universals break on 0x02: update 103 B, step 739 B. (D4)
helper order inverted: every "tail" runs **second**, extras after; 0x0A's actual order is
base→`0044C850`→`0044B960`→`eax→+0x458`. (D5) field maps wrong for 0x04 (seven 1Ts +
4G@+0x1B0, 1T@+0x2A0, H3 is a 4× loop at +0x2B0), 0x05 (3G@+0x150 + 2×1T + H3 loop at
+0x1B0), 0x06/07 (1T@+0x140 not 3G; no 4G@+0x310 — that's the H3 loop base), 0x08 (**nine**
3Gs not eight), 0x0A (1T@+0x1C0 + 4G@+0x1D0 + 4G@+0x220 + 1T@+0x270 + 1T@+0x290). (D6)
type-0x01 walk writes `02AEE908`/`02AEE900`, not `02AE2908`/`02AE2901`.

**Disposition: REJECT** — routed to SWE2-FRONTIER as
AUDITSEM-CONTRA-FRONTIER-EFFECT-TYPES-00-0A (rev 8004). Review:
`Tools/work/SWE2-AUDIT-SEM/REVIEW-effect-types-00-0a.md`.

### 2026-09-14 — queued review: FRONTIER effect-types groups 2–4 + FABLE 0026EE00 notice

Method: same as group 1 — setup-sequence extractor over 15 setup bodies, `disasm_fn.py` on
every cited stub/selector/helper, and an independent re-decode of the dispatcher tables.

**Verified:** `0024B1C0` deferred-free semantics (cap `0x100`, `jae 003697F0`); all three stubs;
`0044B960` PRNG (guard `022D9138`, state `01EF93E8`); all six selector walks; the 0x8C/94/95 and
0x8F/90 sharing clusters; `0xD0`/`0xD1` seventh-payload split; every cited body size; all-default
rows for 0x63/64/6C–6F/93/98–9F/AC. **FABLE's notice upheld**: `0026EE00` is the RGBA8 modulate
(`min(255,(a*b)>>7)`, PMULTH lanes + 0xFF clamp loop + `0036D930`/`0036D8E0` guards), not a
save/restore — the pages' "workbench save/restore" wording mislabels it.

**Defects (9):** queue array `02091150` not `02092150`; `0x61` has one extra single not two;
`0x67`'s "4G@+0x1C0" is a 3×3 loop of nine 4Gs; same loop at `0x65`/`0x66` +0x180; `0x70`'s setup
omits an 8×(1T+3G) loop covering +0x140–+0x3BF (its record's largest region — and `0x70` is
definition-only, so the map IS the semantics); `0x40` map has wrong kinds/order; `0x41`'s
"1T@+0xE0" is the return value; family-B setups omit `1T@+0x190`; "largest walk" claimed twice
(0xA1 3820 B > 0xAB 3790 B); `00457FE0` is three-way.

**Disposition: REJECT** — AUDITSEM-CONTRA-FRONTIER-EFFECT-TYPES-2 (rev 8106). Review:
`Tools/work/SWE2-AUDIT-SEM/REVIEW-effect-types-2.md`. FABLE notice answered UPHELD (rev 8108).

### 2026-09-14 — first review: FRONTIER audio bank/controller per-slot table (BD-3)

Method: `disasm_fn.py` over every named body in both slot tables, including the continuation
ranges past the first flag test in `00223540`/`00224B30`.

**Verified:** base slot-2 teardown ordering; Sep 3/4/5 id-range gates byte-exact (incl. the
0x68+1 vs 0x69 mask asymmetry); Seb triple iterator shape and the `+0x60` map lower_bound; Sep
slot-6 predicate family; controller slot-2 or-accumulate (there the call genuinely IS on each
entry's vtable); controller slot-3 adjustor + map-erase call chain; controller slot-6
pop-or-make on both Music and Stream; `+0x50` lazy-create chain; Sep controller slot-1.

**Defects (9):** slot-0 broadcasts through the bank's OWN `vtable[+0x48]` not "each entry's";
Music slot-0 `00222C00` never calls `00210930`/`00210B30` (those are slot-10's first calls);
handle table is `01FD36C0` not `01FE36C0`; Seb's `[+0x24]` test is `field/150==150` (quotient),
not "mod-150 hits 150"; slot-9 base reads `008C5F6C` not `008C5F6B` and omits the `r8==0 →
007A7A20` tail; Seb slot-9 forwards on `+0x38≠0 OR (+0x14∉{2,0x59})` — page wrote AND; slot-10
is a five-bit mask (`&8`/`&0x10`/`&0x20` → slots 3/4/5-equivalents) not three-bit; Music slot-2
`00222BD0` tails the base teardown (not "driver-only"); Stream slot-4 `0021D4E0` makes three
indirect calls (not "no calls"). Minors: Sep slot-5's `+0x50≠0` gate dropped; controller slot-5
is entry-registration not delegation.

**Disposition: REJECT** — AUDITSEM-CONTRA-FRONTIER-AUDIO-SLOTS (rev 8138). Review:
`Tools/work/SWE2-AUDIT-SEM/REVIEW-audio-slots.md`.

### 2026-09-14 — first review: FRONTIER entry-cited-hubs pass (9b500ccc)

Method: `disasm_fn.py` over all 12 named bodies; every added interior citation checked.

**Verified:** `0030D9A0` (all seven cites incl. the `0030D9E2` reload); `00377C20` (table
`02ADD100`, `rec+8/9` u16, `0xFFF>>15` fallthrough); `002F9860` (reciprocal, 28-bound, empty
fallback `01CEB638`); `00244F00` (msg15 arg `00915058`=0xF); `00254A10` (`bt 0xD81` =
{0,7,8,10,11}); `00247930` (26 B + `|=0x2000`); `00203170` (four identity rows); `00202B70`.
Audio divisor repair confirmed correct — `0x10624DD3@sar6` is signed `/1000` (my earlier `/150`
counter-evidence was wrong; the repair stands).

**Defects (2):** `003DBB60` remap is **1→0, 3→2, else keeps r9 and sets flag bit0** — page wrote
"1→0, 2→2, else→1". `00387B00`'s history-record tables are `0208D480`/`0208DE80`, not
`020BD480`/`020BDE80` (0x30000 off) — the rest of the role read verifies exactly.

**Disposition: REJECT** — AUDITSEM-CONTRA-FRONTIER-HUBS (rev 8173). Review:
`Tools/work/SWE2-AUDIT-SEM/REVIEW-entry-cited-hubs.md`.

Also closed OPUS-REQ-SWE2-AUDIT-SEM-PRESENTATION-THREE (rev 8154): all three pages already carry
OPUS's own falsification passes (8c7cdf6c) with attack/not-checked scoping — spot-verified
byte-exact; the defect my registry audit found sits inside what the pass declared NOT CHECKED.

### 2026-09-14 — shadow audit: FRONTIER switch-families parts 1–3 + repair re-verifications

**Re-verifications (both PASSED):** hubs repair `53d810ad` — `003DBB60` remap now reads 1→0,
3→2, else keeps r9 with flag-bit0 set (matches `sub r11d,1`/`cmp r11d,2`/`or r10b,1` exactly);
`00387B00` tables corrected to `0208D480`/`0208DE80`. Audio-slots repair `c3498219` — all nine
defects + minors corrected, matching my verified reads.

**Shadow audit** (unqueued): `002F6AB0` YM00 dispatch — **all 34 RVA arms byte-exact**;
`00375500` — **all 13 kind arms byte-exact**, filters exact; `0035CA70`/`0035CFA0`/`0035C960` —
14-state machine, factory, and three-arm message proc all exact; store TSV spot-checks pass.

**Defects (3) routed as AUDITSEM-CONTRA-FRONTIER-SWITCH-FAMILIES (rev 8211):** tag-11 RGBA
scale is ×1/128 (`008C5B34`=`0x3C000000`) not ×1/255; factory singleton is `022CA468` not the
9-digit "0202CA468"; `002EFA70` takes `(0, 0x1E, 0, 0)` — the page writes `(0x1E, 0, 0, 0)`.
Minors: mode-machine table is `0035CED0` (page names the site `0035CAA3`); `00375500` re-spins
the handshake bit per entry and runs a shared `00375470` epilogue per dispatched kind.

**Workflow adoption — FF12-WORKFLOW-MIGRATION-20260928-01 (dispatched by SWE2-FRONTIER, 2026-09-28, at next safe checkpoint).**

The user approved a completion-driven workflow migration. Preserve your current identity, active work and ownership. Read the adopted _index/workflow/COMPLETION-WORKFLOW.md and its revision at your next safe checkpoint. OPUS now owns technical migration delivery; ASTRA/SOL independent engineering verification; FABLE connected mechanism completion; FRONTIER operations, safe deployment and capacity allocation. Existing specialist roles remain. This supersedes older operative instructions assigning sole migration architecture to FRONTIER or categorically forbidding useful new tools; it does not supersede full L1+L2 requirements, independent review, safety, game-state protection or history. Do not stop useful work merely to re-plan. Respond through current checked records, self-check changes, consume review, update authorized canonical files and select the next eligible task without user relay. Honour explicit stops and limits. Report a real policy/ownership conflict instead of silently overriding it.

Read the adopted _index/workflow/COMPLETION-WORKFLOW.md, current evidence policy and checked task state. Preserve your existing lane identity, history and peer work. OPUS owns technical delivery, FRONTIER assignments/deployment, SOL independent engineering verification, FABLE completion semantics. Complete your assigned contribution through its required canonical changes and review; a request alone is not package closure. Use existing task IDs and exclusive paths; do not create a competing implementation or direct-edit TEAM. If capped or blocked, checkpoint for a supported handoff and do eligible independent work, without evading limits.

SWE2-AUDIT-SEM: independently evaluate assigned mechanism packages, evidence seals and integration claims. Ask whether the inputs, branches, ownership transitions and consequences actually follow from the original evidence. Check plausible alternatives and runtime/substitution limits. On difficult claims, derive before reading the producer's interpretation where practical. Do not equate green tests, more artifacts or a newer explanation with correctness.

Verify that published runs remain immutable, case maps are exact, and the canonical consumer says what the reviewed evidence supports. Request precise repairs without taking over authorship of the artifact you accept. Validate readable mechanic summaries and actual scope, not only citations. If a required claim stays unresolved, keep it visible; legitimate dispositions do not mean all behavior was recovered. Help finish waiting review queues through existing roles; a positive scoped review is not whole-system or whole-database certification.

Self-check and record exact source/driver/input/result identities and limits. Use a qualified non-author for independent acceptance of your production. A required upstream failure or missing result is not PASS. Preserve historical receipts and relevant regressions; run impacted checks during development, broader campaigns only at governing gates. Update the actual tool/consumer path and persistent procedure so the same defect is caught next time. Use fresh preimages, supported writes, short publication claims and meaningful commits. Keep contribution DONE separate from parent acceptance and whole L1+L2 completion. Respond through the existing board and continue eligible work without user message relay; honour explicit stops and real limits.
