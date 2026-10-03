<!-- TEAM-CURRENT:begin agent=SWE2-ORACLE board_rev=51136 epoch=4 queue_sha=cb0a9463239ff4ed -->
> generated 2026-10-03T14:39:06+00:00 by `team.py current` - do not hand-edit; hand-maintained
> counts and NEXT lines anywhere else are superseded by this block.
> ACTIVE: none
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

# SWE2-ORACLE — inbox and handoff

**Isolated original-code execution.** Bounded calculation, branch and write oracles in controlled memory. One of the eleven fixed production identities (2026-09-13 migration; the
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
   `python team.py apply --agent SWE2-ORACLE --file op.json`. Never edit `TEAM.json` by hand.
5. **Commit explicit reviewed paths** with `publish_paths.sh <message-file> <path> …`. It refuses a
   directory argument on purpose: `git add` on a directory stages every changed file under it,
   including a peer's.

## What this lane is for

**A stub is not proof of its native effects, and agreement between a reconstruction and its own fixture is not evidence.** Disclose every injected value, every stub and the exact entry boundary; omitted initialisation, scheduling and side effects stay open and are written down as open. The control must come from the shipping image or from the documents, never from recollection.

## Review

**Default auditor: `SWE2-AUDIT-SPEC`.** T1 packages need producer self-falsification plus that
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

- **STAND-IN CHECKPOINT 2026-10-03 14:30Z (Claude stand-in for Devin, session bb063a3a; read this first; supersedes the 13:00Z bullet).** All done since 11:20Z: `14bd5582d` 13g bit-14 condition; `c03ad4d97` KO consumers (EXP-198 / contract 13g bit-22 predicate, EXP-231 copy bound); `78271194d` EXP-091 resolver-base repair (G_IMGB 1F83530, positive + negative controls, no old case depended on the branch) - ASTRA-REQ-ORACLE-EXP091-RESOLVER-BASE-CONTROL-1003 DONE. NEXT (owner pass, not yet done): EXP-091 L14/L139 and CONTRACT-commit-action L321-323/L372-373 over-claim 0x20E600 (and six bodies.json entries) as executed; the record-page (the-record-00329220-builds.md L428-433) bit-20 sentence looks reversed against 002FEB41/45 - see `_experiments/evidence/exp091-resolver-base-repair-1003/README.md`. Queue watcher `Tools/work/SWE2-FRONTIER/standin1003/queue_watch.py`; fleet plan holds all 8 lanes until Devin starts (release with `hold_plan.py ""` in the stand-in scratchpad). Publish tools per lane: `Tools/work/<LANE>/standin1003/` (bop.py, mkpub.py, pub_runner.py); splice publishes over peer overlays: `Tools/work/SWE2-FRONTIER/standin1003/splice_pub.py`.

### Latest: 04:33Z, Claude stand-in for Devin (SWE2-ORACLE)

A Claude session (Opus) operated SWE2-ORACLE from 02:10Z to 04:33Z on 2026-10-03, while the Devin session
`tulip-krypton` was rate-limited (breaker until about 07:39Z). **Devin: do not redo any of this. Rebuild from here.**

- **Current package/claim:** none
- **DONE (09:33Z): P1 `OPUS-REQ-ORACLE-L2-CROSSCHECK-1003`**, the independent cross-check of AUDIT-SEM's six L2
  systems (S-02, S-13, S-28, S-43, S-36, S-49), published `3c0182b11` at
  `_index/candidates/swe2oracle-l2-crosscheck-1003/` (`xcheck.py` re-run about 20 min, system Python 3.14). 18/18
  cited replays reproduce; stub-free holds where claimed; 12 reached mutations: 8 KILLED, 4 INVISIBLE. AUDIT-SEM's
  verdicts agreed (four ACCEPT-WITH-NARROWING, S-36/S-49 REJECT). FABLE messaged; board notes for
  `FABLE-REQ-OPUS-FINISH-PACKAGES-ZIP-1003` at revs 50190/50200. Filed `ORACLE-REQ-OPUS-DERIVED-RELABEL-IDEMPOTENT-1003`
  (P1, to OPUS): the new derived gate `890844135` refuses a publish when HEAD's PROGRESS.md is already labelled
  STALE. Do not re-run the cross-check: it is closed.
- **DONE (06:40Z): the coverage review is answered.** SWE2-AUDIT-SPEC finished
  `ORACLE-REQ-AUDITSPEC-EXECCOV-REVIEW-1003` with ACCEPT-WITH-NARROWING at `701804391`: checker `FAILS 0`, all 893
  scripted entries are real hooks, no sealed result modified, docstring finding upheld. Its three wording narrowings
  (mutation per run, not per case; import thunks; stub-detection shape) are applied to the coverage README, with a
  consumer-check record, in the same commit as this line. The seal was re-written and the checker still ends
  `FAILS 0`. Incorporation into the dashboard's executable view is OPUS's (`AUTO-INCORP`), not ORACLE's.
- **DONE (06:32Z): ASTRA's committed render-link runs sealed**, `51853f51d`. Requests
  `ASTRA-REQ-ORACLE-SEAL-COMMITTED-RENDER-LINK-1003` (finish rev `49545`) and
  `ASTRA-REQ-ORACLE-SEAL-RENDER-PATH-CONTROL-1003` (finish rev `49547`). Applier
  `_experiments/evidence/receipts/render_link_receipts.py` (exp201-shaped, `check` `FAILS 0`; ids in
  `render_link_receipts.ids.json`): PREP `r-2b2175e418c2fdef` (prepare.py, 15 cases), CTRL `r-81d89897cfbbfb59`
  (control.py + prepare.py, 3 refusals), PATH `r-e51471d199e0e709` (launch.py + controller + producer, 2 cases,
  synthetic, no FF12 credit). The invalid path run 01 is not sealed (negative control). This closes the follow-up
  promised in the render-link addendum entry below. Do not re-seal: seal() is idempotent, but the requests are
  closed.
- **DONE (05:01Z): first-divergence design note** (user request relayed by FABLE; addendum
  `Database/Tools/work/FABLE/FFXII_PROJECT_IMPROVEMENT_ADDENDUM_2026-10-03.md` section 5, P2), published
  `67869ee22`: `_index/candidates/swe2oracle-design-first-divergence-1003/` (README, `first_divergence_probe.py`
  `FAILS 0` on mt-twist-simd-exec, `first-divergence.tsv`). FABLE was sent the sha. Design only: implementing it (a
  `FIRST-DIVERGENCE:` line per pilot plus a generated `_index/FIRST-DIVERGENCE.tsv` from `parity_status.py --run`)
  is P2 and waits behind DB completion. Do not start it unprompted.
- **DONE: `OPUS-REQ-ORACLE-EXECUTION-COVERAGE-INSTRUMENT-0929-R`** (finish rev
  `49023`). Its review `ORACLE-REQ-AUDITSPEC-EXECCOV-REVIEW-1003` was filed to SWE2-AUDIT-SPEC (rev `49022`,
  `reviews` field set, incorporation owner OPUS). Answer that review when it lands.
- **Also DONE: `ASTRA-REQ-ORACLE-RENDER-LINK-ADDENDUM-1003`** (claimed rev `49024`, finish rev `49087`), with
  the record published at `76bf92900`: `_index/candidates/oracle-render-link-addendum-receipts-1003/`. The existing
  `seal.py` policy applies unchanged. ASTRA's prepared and control runs are not yet sealable for credit, and need
  (1) the drivers `prepare.py` and `control.py` committed side by side at a tracked path (`Database/Tools/.gitignore`
  ignores `work/`), (2) a `cases` list in the prepared result, and (3) `id` instead of `case` in the controls result.
  A temp-store trial plus a fix simulation shows only the driver-commit refusals remain after (2) and (3). If ASTRA
  files a follow-up naming its driver commit, seal both receipts into `_experiments/evidence/receipts/store/` with an
  applier shaped like `exp201_receipts.py`.
- **Published `b742fa6c989e7da7327145b4b81e8649d4b06870`:** the execution-coverage instrument and its record,
  `_index/candidates/oracle-execution-coverage-1002/` (README, `runs/<suite>.json`+`.tsv` for all 124 sealed
  Unicorn suites, aggregate `execution-coverage.tsv`, `SEAL.json`, `check_execution_coverage.py` C1-C6 `FAILS 0`),
  plus `gfz-scripts/execution_coverage.py` and `gfz-scripts/execcov/` (sitecustomize meta-path finder and unicorn
  shim). 124/124 receipts reproduced byte-identically. 1,709 entries touched, **1,307 executed**, 402 NOT executed.
- **What the stand-in changed in your 10-02 work (it was uncommitted when you stopped):** the v1 shim had three
  defects that would have published false executed claims. (1) No stub or redirect detection: entry-patched and
  hook-scripted bodies were recorded `returned`, and each redirect left the shadow stack one frame deep. 99 v1
  "executed" entries are NOT executed. (2) `_load_pe` read SizeOfOptionalHeader at `opt+0x14` (pe+0x2C), so the
  "image" spanned 0x120000..0x18C21471B and `blocks_outside_image` was always 0. (3) `bnd ret` was not recognised
  as a ret. v2 adds the `stubbed` / `scripted` (NOT executed) classes, `returned+faulted`, a `mutated` flag, the
  seal, sibling-suite copies and FileExistsError cleanup in the sandbox, a repo-root retry on any failure, and an
  absolute `--out`. Your v1 shim, driver and outputs are kept in
  `Database/Tools/work/SWE2-ORACLE/standin/` (`shim_v1_init.py`, `driver_v1.py`, `cov_v1_out/`).
- **Run it with system Python 3.14** (unicorn 2.1.4). The analysis venv's unicorn 2.1.0 rejects
  mt-twist-simd-exec's SIMD instructions.
- **Finding to act on (own record):** sound-request-fork-exec's check.py docstring lists `0016D6D0` / `0016DA60` /
  `00199DB0` as "Real bodies", but its code QSTUBs them (`TD6D` / `TDA6` / `TM99` -> `_qstub`). Repair the docstring
  wording. It is recorded in the coverage README.
- **Leftovers:** `_experiments/_cov_runs/` is sandbox scratch, ignored by its own `.gitignore`. The `NUL` files in
  `evidence/commit-callees-exec/`, `evidence/mt-twist-simd-exec/` and two other evidence dirs date from your 10-02
  debugging (17:33 local). They are untracked and were left alone.
- **Next action (Devin):** the sound-request-fork-exec docstring repair. The review upheld the finding (code and
  instrument right, docstring wrong). It touches a SEALED harness: edit only the docstring lines 18-22, never the
  code, then re-run its `check.py` and confirm `result.json` reproduces byte-identically before publishing. The
  owner is the EXP-105 suite's author, routed through SWE2-ORACLE. Optional and recommended by the reviewer before
  new suites are added: extend the execcov shim to class an entry patched with a jump to an out-of-image stub as
  `stubbed`. No current harness does this. Then the surrogate residue and SD-7 residue reads (`00210320`, the PPFX `+0x38` holders) if OPUS routes them back.
  Then continue the queue in `team.py current` order (empty at 04:33Z).
- **Latest coherent commit:** `3c0182b11` (L2 cross-check), after `268c39a1f` (review narrowings), after `51853f51d` (render-link receipts), after `67869ee22` (first-divergence design note), after `76bf92900` (render link addendum
  record) and `b742fa6c9` (coverage record), followed by this inbox publish.

### Earlier: 2026-09-30, SD-107 / SD-7 / SD-62 (SWE2-ORACLE)

- **Package:** `SWE2-ORACLE-SD107-7-62-0930` (OPUS brief `Tools/work/OPUS/oracle_brief_sd107_7_62.md`). Three static records,
  each checker ends `FAILS 0`, published at `dedfaf0d7`:
  - **SD-107 NARROWED** - `_index/candidates/sd107-register-stores-0930/`. `002475D0` stores 1 at `+0xA3` (0xFF -> 1), but the
    nine sites that can pass 1 all act on widget bases (self of registered widget procedures, `00244F50` results,
    `00559860`'s slots); widget and text-element layouts conflict at `+0`/`+0x48`; widgets keep the element at
    `+0xC0`/`+0xD0`/`+0xE0`; no kind reader gets a widget base. OPUS's 93 unbounded stores: 1 setter, 11 same-field copies,
    7 polymorphic `this`, **74 open** (listed in the `.out`).
  - **SD-7 NARROWED** - `_index/candidates/sd7-stored-app-pointer-0930/`. 192 `[vtable+0x78]` sites: 133 excluded by holder
    displacement, 13 by RTTI class of `this`, 2 by constructor vtable, 10 by slot range (GameApplication has 31 slots);
    **34 remain** (5 render-context, 4 Bullet, 20 PPFX holder loads, 5 game-code holders - next read `00210320` for
    `01FC35F8`). The brief's `002E0D39`/`002E2257` are SD-8's `00229F00` sites.
  - **SD-62 ANSWERED (chaining)** - `_index/candidates/sd62-registry-list-links-0930/`. Root `01F2E330`: `+0x10` class
    descriptors (node `+0x50`, writer `00639160`), `+0x28` non-root owners, `+0x00` its own unlinked node. `01F2E780` is a
    0x30-byte descriptor name-hash tree (node `+0x08`, key `+0x20`/`+0x28`). **Differs from OPUS F3:** the PWorld /
    `getInstanceCount` slots belong to a separate method record at `01F2E7B0` (own init `00635B80`, dtor `008AF430`).
- **Requests filed:** `ORACLE-REQ-AUDITSPEC-SD107-0930`, `-SD7-0930`, `-SD62-0930` (SWE2-AUDIT-SPEC, with `reviews`) and
  `ORACLE-REQ-DATA-SD107-ROW-0930`, `-SD7-ROW-0930`, `-SD62-ROW-0930` (SWE2-DATA). Rows and pages not edited here.
- **Concurrent ORACLE session:** while this package ran, another SWE2-ORACLE session held uncommitted EXP-257 edits in
  this inbox (checkpointed by it at `3cd59df59`), so the records were published without the inbox and this block
  followed separately.
- **Scratch:** `Database/Tools/work/SWE2-ORACLE/sd107/`, `sd7/`, `sd62/` (census scripts, board ops; gitignored).
- **Next action:** the execution-coverage instrument, then the surrogate residue (unchanged); SD-7 residue reads
  (`00210320`, the PPFX `+0x38` holders) if OPUS routes them back.
- **Claims:** none left ACTIVE after the finish.

### Earlier: 2026-09-30, SD-182 / SD-183 / SD-184 remainder (SWE2-ORACLE)

- **Package:** `SWE2-ORACLE-SD182-184-0930`, a sub-package of OPUS's `OPUS-SD180-193-0930` (OPUS brief
  `oracle_sd182_184_brief.md`). Three records, each checker ends `FAILS 0`:
  - **SD-182 ANSWERED, authored** — `_index/candidates/sd182-nav-transform-pair-0930/`. The nav table `tab` is one of
    the two 0x68-byte tables `002F6AB0` builds from the map pack's YM00 section (tag 0x1F -> obj+0x40, tag 0x11 ->
    obj+0xA8); `00232380` only rebases `tab+0x18` onto the type-4 sub-chunk; no code stores into a subrecord. In the
    shipped bytes `+0x50` is the inverse of `+0x10` in 89,330 of 89,330 subrecords (to float32 rounding; negative
    control 0 of 89,174).
  - **SD-183 ANSWERED** — `_index/candidates/sd183-steering-modes-0930/` (static + unicorn execution of `0033CEF0`,
    `0033D200`, `0033BAA0`, control `0033CE60` from the page's AM-7). Flag word = `dword[st+0]` = BattleUnit +0x80;
    the dispatcher runs only while the countdown (bits 5-14) is non-zero. Mode-bit writers: `0033CC80` from the
    avoidance direction search `0033A720` (mode 4 fallback; 1 / 2 / 3 / 5 from chooser `00339DF0` + table `01EED4C0`
    and `0033D200`'s return), `003343D0` (mode 6 orbit), `0033E1F0` (mode 0). Modes 1 and 4 share a body and nothing
    distinguishes them. `0033D3B9` is a countdown arm (10), not a mode change.
  - **SD-184 ANSWERED with a named residual** — `_index/candidates/sd184-facing-sources-0930/`. Executed `0033CB70`:
    the fast path mis-normalises only |x| in (5pi, 6pi), (7pi, 8pi)..., not every |x| > 4pi. `setposparty` script
    facings reach BattleUnit +0x160 raw through `00310920`, up to 5.846853 rad (171 constant sites outside [-pi, pi],
    none near 4pi). `00311F70`'s facing is `00336E40`'s +0x30 (bounded). Three publishes the page lacks: `003043A8`,
    `00307A0B`, `00312F77`. All nine `00334120` targets bounded. Only unbounded shipped source: the debug accumulator
    in `evt_t0505` (`event_jump_lr`), reachability not decided.
- **Requests filed:** `ORACLE-REQ-AUDITSPEC-SD182-0930`, `-SD183-0930`, `-SD184-0930` (SWE2-AUDIT-SPEC) and
  `ORACLE-REQ-DATA-SD182-ROW-0930`, `-SD183-ROW-0930`, `-SD184-ROW-0930` (SWE2-DATA). Register rows and pages not
  edited here.
- **Scratch:** `Database/Tools/work/SWE2-ORACLE/sd182/` (disassembly dumps, board ops; gitignored).
- **Next action:** unchanged from the triage entry below: the execution-coverage instrument, then the surrogate residue.
- **Claims:** none left ACTIVE after the finish.

### Earlier: 2026-09-30, FINAL-AUDIT pass 6 owner reading of five rc READMEs (SWE2-ORACLE)

- **Package:** FINAL-AUDIT pass 6 (`check_banned_evidence.py --list`) showed 8 TO READ lines on five ORACLE records.
  Board task `SWE2-ORACLE-PASS6-OWNER-READ-0930`. Every line was read in context. **All five pages are FALSE-POSITIVE,
  and no record was corrected**; none rests a claim on unwind or EH data.
  - `rc11-arena-ten-0930` L19 and L49: `.pdata` fragments are the census population for `riprefs.py`. The `.pdata`
    records and the three chained-unwind parents of `003A9EF0` are named as hits that are **not** references. "No other
    reference" rests on the decoded rip-relative census, so the ban is applied, not broken.
  - `rc12-footer-channels-runstate-0930` L10 and L242: `.pdata` chain roots are extents and the RC-14 sweep's
    population, and the uncovered `.text` runs are swept linearly beside them. The S1-S6 shapes are matched on decoded stores.
  - `rc20-float-push-verbs-0930` L15 and L31: a decoded `E8`/`E9` hit is kept inside its chain-root extent. C5 is a
    control that a thunk with no unwind entry is still found.
  - `rc22-as7-pages-0930` L79: "`.pdata`-less setter" describes `002CEE00`. The only-writer claim rests on the store
    census (`002CEE1A`).
  - `rc8-cascade-count-0930` L16: `memsweep.py`'s population is chain roots plus leaf bodies. The flow result is a
    decoded pointer-flow analysis.
- **No ORACLE disposition row was written, on purpose.** OPUS's committed rows (`23f18aae2`, TSV lines 64-68) already
  hash exactly the current evidence for all five pages: `a9d9e691…`, `a3e364a3…`, `b8758cfc…`, `6f6de079…` and
  `8e3888df…`. They are UNREVIEWED only because the reviewer is empty.
  - `dispositions.Registry.state` returns on the **first** row whose hash matches. A second, author-ORACLE row would be
    shadowed by OPUS's unsigned one even after it was signed.
  - This was measured on a temp copy of the TSV: an appended row with reviewer `SWE2-AUDIT-SPEC` still gives
    `UNREVIEWED` for all five pages.
  - The fix is to sign the existing rows. The request is `ORACLE-REQ-AUDITSPEC-PASS6-RC-DISPOSITIONS-0930`, which
    carries the owner's concurrence.
- **Kit note for OPUS (not fixed here; the kit is not ORACLE's):** a signed disposition row placed after an unsigned
  row with the same hash never applies. `state()` should prefer a reviewed match.
- **Next action:** unchanged from the triage entry below: the execution-coverage instrument, then the surrogate residue.
- **Claims:** none left ACTIVE after the finish.

### Earlier: 2026-09-30, READY-backlog triage + S-08 BGM-machine drain (SWE2-ORACLE)

- **Package:** reduce the READY backlog before the freeze (36 tasks addressed to SWE2-ORACLE at board rev 42656).
  Triage: **21 SATISFIED** by later records or notice-only, **13 STILL NEEDED and done this session** (owner
  annotations plus one execution), **2 STILL NEEDED and left READY**. Scratch: `Database/Tools/work/SWE2-ORACLE/triage0930/`
  (`board.py` claim+finish driver, `annotate.py` idempotent record edits; gitignored).
- **Finished as SATISFIED (board revs 42662-42697):**
  - S-02, 5: `OPUS-REQ-ORACLE-S02-CLOSE-26A5F0-AND-SS7`, `OPUS-NOTICE-ORACLE-S02-SS7-NEEDS-226BE0`,
    `OPUS-NOTICE-ORACLE-S02-READY-PATCH-26A5F0` and `OPUS-NOTICE-ORACLE-S02-SS7-REACH-TABLE-PATCH`, by `fc379f25f`,
    `5bde53415` and `3c8bcc7af`.
  - S-21, 3: `OPUS-REQ-ORACLE-S21-385BA0-REAL-EMPTY-SLOT` and `OPUS-NOTICE-ORACLE-S21-READY-PATCH-385BA0` (`6f1c17e98`);
    `OPUS-REQ-ORACLE-S21-REMAINING-BOUNDARIES` (`67015c61a`, `0bf7c27f4`, `1f92ffe62`).
  - S-47, 2: `OPUS-REQ-ORACLE-S47-24ED80-MAKE-CURRENT-REAL` and `OPUS-NOTICE-ORACLE-S47-READY-PATCH-24ED80` (`86c611a64`).
  - Other contracts, 3: `OPUS-REQ-ORACLE-S05-SAVE-RESTORE-EXEC` (`c305fca98`), `OPUS-REQ-ORACLE-S06-DISPATCHER-STUB-FREE`
    (`8f8d676ed`, `b4382c11e`) and `OPUS-REQ-ORACLE-S49-HEADER-FLIP-REAL-MEMBERS` (`a2948ddd4`, `a69b6e602`).
  - Notices and acknowledgements, 5: `OPUS-NOTICE-ORACLE-226-ENTRIES-NEVER-EXECUTED`,
    `OPUS-NOTICE-ORACLE-EXP189-CONSUMED-STRUCTURALLY`, `OPUS-NOTICE-ORACLE-S13-RESULT-REWRITE` (`ad06c808e`),
    `FABLE-NOTICE-ORACLE-BQ27-LIVE-TARGET-61-SITES` and `FRONTIER-NOTICE-ORACLE-UNJOURNALED-WRITE-33308`. For the last,
    ORACLE's write path is `team.py apply` only.
  - `ASTRA-RETURN-ORACLE-MATRIX-APPLICATION-CONVENTION`: OPUS `e97faa9fe` had already qualified this record's EXP-219
    row.
- **Finished with this commit (owner decisions recorded here and in each record):**
  - **EXP-191 / EXP-149 / EXP-084 addenda.** OPUS's replays adopted: 287 / 288 / 289.
  - **EXP-145.** The `0x861F02` cell is the named import `atan2f` (294).
  - **EXP-095.** The out slot is the action id.
  - **EXP-139.** The five siblings are `lea`-planted callbacks. The three plants were re-read with capstone.
  - **EXP-140.** The clear precedes the signed loop gate, physical zeroing is the caller's (`00323BB0`), and this
    harness entered with `RSP % 16 = 0`.
  - **EXP-099.** The `dead-actor` case is a supplied manager gate.
  - **EXP-097.** Heads-only observation; `m-selflink` is not a self-link mutation. ASTRA's raw-node control is the
    regression, and the historical driver is qualified, not re-run.
  - **EXP-201.** The Open bullet is closed by `eae0ed3c7`. `exp201_receipts.py`: docstring updated, a non-JSON result is
    now a FAIL row, and the new negative control is `N-non-json-result`. The check gives `FAILS 0` and
    `GATE-PENDING none`. EXP-202 / EXP-256 now cite their receipts.
  - **rc30 / rc25 READMEs.** Narrowed per `SWE2CONTRACT-CONTRA-ORACLE-RC30-RC25-0930`. The bytes `00180F81`–`00180F8A`,
    `0017F3E9`, `0017F419` and `0017F440`–`0017F447` were re-read.
  - **`ASTRA-REQ-ORACLE-MULSS-STATUS-LIMIT`.** No ORACLE record uses the emulator's MXCSR status as native proof. A
    grep of every `_experiments/EXP-*.md` and `_index/candidates/*/README.md` for MXCSR / inexact / precision status /
    exception flag hits only ASTRA, OPUS and FABLE records. There is nothing to downgrade in this lane.
  - **`ASTRA-RETURN-ORACLE-ACCESS-DEFAULT-SEAL` and `ASTRA-NOTICE-ORACLE-RAW-BYTE-DELIVERY`: no seal.** `seal.py`
    receipts exist to pin a cited result that sits at a mutable, shared path. This packet's cited files live in its own
    directory, and its raw bytes are preserved additively (`1225845ca`). A second, sealed identity would be the rival
    copy the request forbids.
    - The canonical manifest at `cdc0237c1` stays `INVALID_CANONICAL_MANIFEST_BYTES` (five CRLF-to-LF members), as
      recorded.
    - The raw mirror is the provenance.
    - SWE2-AUDIT-SPEC accepted it, qualified (`REVIEW-0928-P1-WAVE.md`).
  - **`FRONTIER-RT-ORACLE-HWBP-WEDGE`: declined, with a named fact.** The wedge is the state of the live process after
    `hwbp.py` detaches: whether thread contexts keep DR0-7 armed or threads stay suspended. That is a property of the
    Windows debug session, not of any shipped function. Isolated execution has no debugger attach to reproduce it.
    - Prior bound: z255/z256 (`ae1a4a4bc`, `564fdf42b`, "state-dependent").
    - RT-1 is NOT A QUESTION in the register and is carried by `FABLE-CARRIER-TOOLING-AND-CHECKER-PROPOSALS-0926`.
    - ASTRA's live window is closed.
- **Executed (NATIVE-REPLAY): `_index/candidates/s08-bgm-machine-drain-0930/`, for `OPUS-REQ-ORACLE-S08-BGM-MACHINE-REAL`.**
  `s08_bgm_drain.py` / `.out`: 16 checks, `FAILS 0`, byte-identical across two processes. It runs OPUS's block-330
  world, imported read-only.
  - **I3's same-call drain holds** with the stream inactive (every shipped run) and with it active in state 5.
  - **It does not hold** when the machine is in a submitting state (1, or 7 with bytes left) and the pool is full. The
    machine submits through `0032E780 → 0032E870` before it writes its next state. The nested requester stalls into the
    pump, which calls the machine again, and nothing drains. This is shown to depth 8; exhaustion is inferred.
  - **Static:** the machine returns 1 only after a submission. The music page's "submitted or advanced" is wider than
    the code.
  - **No stubs.** Fixtures F1-F5 are listed in the README.
- **STILL NEEDED, left READY:**
  - `FRONTIER-RT-RUNTIME-SURROGATE`. All seven rows are now answered or dispositioned. This task carries the runtime
    residue of two of them:
    - GG-1: `003C87B0`'s paths through `00254B40` and the widget message-1/12/18 handlers;
    - BQ-27: the 40-site residue.
  - `OPUS-REQ-ORACLE-EXECUTION-COVERAGE-INSTRUMENT-0929-R`: a per-run executed-entry record plus an aggregate TSV over
    the sealed receipts.
- **Requests out:**
  - `ORACLE-REQ-AUDITSPEC-S08-BGM-DRAIN-0930` (review, with a `reviews` field);
  - `ORACLE-REQ-OPUS-S08-I3-PROVISO-0930`: the queue contract's I3 proviso and the music page §3.3 return wording.
- **Next action:** the execution-coverage instrument (it should reuse the Unicorn code hooks the sealed drivers already
  install). Then the surrogate residue, in `team.py current` order.
- **Claims:** none left ACTIVE after the finish.

### Earlier: 2026-09-30, SD-162 (SWE2-ORACLE)

- **Package:** register row SD-162, assigned by OPUS. Board task `SWE2-ORACLE-SD162-TRIAL-AWARD-PATH-0930`. The record is
  `_index/candidates/sd162-trial-award-path-0930/`: `sd162_award_path.py` / `.out` (`FAILS 0`), `sd162-award-sites.tsv`
  (1,800 rows) and `README.md`. It is script-corpus evidence plus one static read of the image's kind-5 path table.
- **Answer.** All 1,800 `unkCall_5ad` sites (900 = 100 stage files x 9 languages; one index-39 and one index-40 call per
  file) are in `トライアル監督.main`. Each is dominated by `waitv(scratch1 @0x06)`, the engine's group-completion post;
  group 1 is Trial Mode's only event group. Each also sits under `nowmap()` guards:
  - index 39 needs `!= 0x51F`, then the tenth-stage set, then `== 0x4CF`;
  - index 40 needs `== 0x51F`.
  - The kind-5 path table puts `tri_<g><s>` at field `0x483 + 8g + (s-1)`. So only `tri_j05` (stage 50) and `tri_t05`
    (stage 100) have a live award: 18 live sites, 1,782 statically excluded.
- **Controls:** the item ladder 0x9123..0x912B on stages 10..90; the `bossgaugeopen` negative on dominance; the census
  totals; the `tst_a01` / `slm_a01` path-table slots.
- **Limits:**
  - whether a run clears group 1 is live;
  - the `nowmap()` to loader-index identity is not traced as one value;
  - `008632B0`'s effect is taken from the page.
- **Requests out:** `ORACLE-REQ-AUDITSPEC-SD162-0930` (review) and `ORACLE-REQ-DATA-SD162-ROW-0930` (SWE2-DATA restates
  SD-162 and the page's "900" line).
- **Next action:** answer the review when it lands, then continue the queue in `team.py current` order.
- **Claims:** none left ACTIVE after the finish. Scratch is in `Database/Tools/work/SWE2-ORACLE/sd162/` (gitignored).

### Earlier: 2026-09-30, SD-140 (SWE2-ORACLE)

- **Package:** register row SD-140, assigned by OPUS. Board task `SWE2-ORACLE-SD140-VERTEX-PREP-0930`. The record is
  `_index/candidates/sd140-vertex-prep-kernel-0930/`: `sd140_kernel.py` / `.out` (23 checks, `FAILS 0`), `sd140_emu.py`
  (a Unicorn harness with disclosed stubs) and `README.md`. It combines static anchors, a census control and native
  execution against models.
- **Answer.** `+0x28` is a per-corner RGBA8 vertex colour and `+0x2C` a per-corner float texture coordinate
  (`c18 = c1A = 3·tri + 4·quad` in all 2,252 records).
  - `00432300` is the PS2 modulate: `min(255, e·c >> 7)` per byte, where `c` is the single dword at draw-param `+0x40`,
    and `0x80808080` is the identity.
  - `00433830` is a rounded lerp `trunc(a·t + 0.5 + b·(1 − t))` (= `cur·(1 − w) + next·w`), used only when `+0x1F1`
    bit 4 is clear.
  - Per pass: modulate again by the pass colour (or a flat `param+0x40 ×` pass colour), then optionally
    `alpha × L[normal].w` (`00432CC0`).
  - The twelve builders emit the bytes as float lanes 0..255 unscaled. UV goes as GS STQ, `(u + ou)·Q`, and is
    divided back to `u + ou`.
- **Narrowed:**
  - the per-pass UV operators (`0043E840`, `0043E7B0`, `00434630`, `00434760`, the `+0x1B0` regenerators);
  - the lighting routines that fill `L`;
  - `0026EE00`;
  - the draw backend after the builders;
  - the `00521450` clipper.
- **Contradictions routed to OPUS (not filed):**
  - the-two-transform-primitives.md `00434CD0` subtree: the bit 4/5/6 polarity is inverted;
  - the same page: `00432300` is not "pure staging";
  - the same page: `0043DB90` / `0043E440` / `0043D8F0` are n-gon builders, not field-math helpers;
  - kind-54 §8: "element `+0x40`" is draw-param `+0x40`, and the blend happens only with bit 4 clear;
  - §22.5 BI-3a: the 1.15 / 0.5 math is on the pass offset pair.
- **Requests out:** `ORACLE-REQ-AUDITSPEC-SD140-0930` (review) and `ORACLE-REQ-DATA-SD140-ROW-0930` (SWE2-DATA restates
  SD-140).
- **Next action:** answer the review when it lands, then continue the queue in `team.py current` order.
- **Claims:** none left ACTIVE after the finish. Scratch is in `Database/Tools/work/SWE2-ORACLE/sd140/` (gitignored).

### Earlier: 2026-09-30, SD-120 (SWE2-ORACLE)

- **Package:** register row SD-120, assigned by OPUS. Board task `SWE2-ORACLE-SD120-BINDING-OPS-0930`. The record is
  `_index/candidates/sd120-binding-ops-0930/`: `sd120_ops.py` / `.out` (33 checks, `FAILS 0`), `sd120_emu.py` (a
  Unicorn harness over the shipped bodies) and `README.md`. It combines static anchors with native execution against
  models.
- **Answer.** The working buffer is a CLUT. `003CD840` unpacks 1, 16 or 256 RGBA8 entries into 8.8 lanes (256 in CSM1
  order), and `003D2B60` clamps and repacks them. The eight operations are palette-animation effects:
  - op1 permutes (rotate / clamped shift / mirror);
  - op2 is an additive or proportional tint ramp;
  - op3 fades to a colour;
  - op4 fades to another palette;
  - op5 desaturates with BT.601 luma;
  - op6 tints by strength G/128;
  - op7 sweeps a colour with a ramp;
  - op8 cross-fades to another palette by a Hermite curve (`0053DB50`).
- **Narrowed (not surveyed):**
  - who fills dispatcher-record operands: the callers of `003CCC20`, `00504D30` and `00468160`, were not read;
  - `004314E0`;
  - reachability of the quirks: op7's below-buffer write on negative speed, op6's strength / duration overlap.
- **Contradictions routed to OPUS (not filed):**
  - page §18 says a 32-byte payload; `003CCC20` copies 48 bytes;
  - page §18 says `+0x34` is "bounds-checked"; it is elapsed time against the lifetime `+8`;
  - page §18 says `+0x28/+0x30` are write-only and no writer of `+0x38/+0x40` was found; they are the operation list
    and its links;
  - world-tick lines 2589, 2597 and 2621 describe `0050A100`, `00507120` and `0053DB50`; the code contradicts all
    three;
  - the randomness page line 556 calls the six "formatter".
- **Requests out:** `ORACLE-REQ-AUDITSPEC-SD120-0930` (review) and `ORACLE-REQ-DATA-SD120-ROW-0930` (SWE2-DATA restates
  SD-120).
- **Next action:** answer the review when it lands, then continue the queue in `team.py current` order.
- **Claims:** none left ACTIVE after the finish. Scratch is in `Database/Tools/work/SWE2-ORACLE/sd120/` (gitignored).

### Earlier: 2026-09-30, SD-81 (SWE2-ORACLE)

- **Package:** register row SD-81, assigned by OPUS. Board task `SWE2-ORACLE-SD81-EASTL-CALLERS-0930`. The record is
  `_index/candidates/sd81-eastl-callers-0930/`: `sd81_callers.py` / `.out` (`FAILS 0`), `sd81-callers.tsv` and
  `README.md`. It is static only.
- **Answer.**
  - All 99 EASTL rbtree callers were read. 56 are EASTL's own insert path in 24 instantiations (I01–I24). Every one
    is a unique-key map or set; there is no multimap or multiset.
  - 30 erase and 12 walk bodies are inlined in game or manager code. 90 of the 98 non-member callers are typed (node
    size + key + value). 81 trees are located to a global, a singleton, an RTTI class, a stack local or an array.
  - 15 instantiations are proven map or set by the `EASTL map` / `EASTL set` allocator-name tag.
  - Wrappers: none in front of the six. The 56 insert-path bodies are the wrappers. 6 node-construction helpers sit
    beside them, and 21 thin wrappers sit above the 99.
- **Contradiction raised (not filed; routed to OPUS in the report).** Checks K1 and K2 show that the font `.ker` writer
  `001FDC10` builds a nested `map<rec+4, map<rec+0, adjust>>` through `001FC420`. That contradicts
  font-data-kerning-and-expansion.md §3 ("flat map", "r8d never read back", "structurally inert").
- **Requests out:** `ORACLE-REQ-AUDITSPEC-SD81-0930` (review) and `ORACLE-REQ-DATA-SD81-ROW-0930` (SWE2-DATA restates
  SD-81).
- **Next action:** answer the review when it lands. Then continue the queue in `team.py current` order.
- **Claims:** none left ACTIVE after the finish. Scratch is in `Database/Tools/work/SWE2-ORACLE/sd81/` (gitignored).

### Earlier: 2026-09-29 (SWE2-ORACLE, run by OPUS's Claude subagent)

> **2026-09-29: this lane was run by OPUS's Claude subagent under the SWE2-ORACLE identity** (session
> `OPUS-claude-oracle-0929`), covering the evidence-receipt cluster while Devin's lane was idle. Not a new identity.
> Devin resumes from this entry plus the board; the older entries below are unchanged.

- **Finished, published:**
  - `8b269d9fa`: P0 `FRONTIER-REQ-ORACLE-EXP201-RECEIPT-SEALING` (DONE) plus `OPUS-NOTICE-ORACLE-SEAL-MECHANISM` (DONE).
    OPUS's `seal.py` applied, not edited. The store is `_experiments/evidence/receipts/store/`, with `* -text` so the
    bytes stay exact. `r-95260e713b7dba43` is EXP-201's genuine 394-case run: `aa29615b7`'s own bytes, whose CRLF
    checkout hashes to the cited `be5088bd..`. `r-edb8403635767456` is EXP-202's 407. `r-5be60dc8ce879ae1` is EXP-256's
    556, the current file. All three drivers re-executed byte-identical. The EXP-201 record and contract 13j are bound.
    Regression: `receipts/exp201_receipts.py check`, FAILS 0.
  - `85e6c8ca7`: owner acceptance of FABLE's `b17be47ac` annotations on EXP-086/189/230, checked against the image by
    `_index/candidates/oracle-annotation-acceptance-0929/verify_annotation_bytes.py` (FAILS 0). This closes
    `FABLE-NOTICE-ORACLE-EXP-ANNOTATIONS-APPLIED`, `FRONTIER-REQ-ORACLE-EXP086-RET-AND-EXP189-DESCRIPTIONS`,
    `FABLE-REQ-ORACLE-EXP189-EXP086-RECEIPT-ANNOTATIONS`, `FRONTIER-REQ-ORACLE-EXP230-RELEASE-GUARD-CORRECTION` and
    `FABLE-REQ-ORACLE-EXP230-325A00-GUARD`. Contract line 1676 was already correct at `ac3363c2a`.
- **Pending reviews (SWE2-AUDIT-SPEC):** `SWE2-ORACLE-REQ-AUDITSPEC-REVIEW-EXP201-SEAL-0929` (8b269d9fa) and
  `SWE2-ORACLE-REQ-AUDITSPEC-REVIEW-EXP-ANNOT-ACCEPT-0929` (85e6c8ca7).
- **Open request out:** `SWE2-ORACLE-REQ-OPUS-SEAL-FLATMAP-0929`. seal.py's case parser does not read this harness's
  flat `{case_id: {...}}` result, so `exp201_receipts.py check` prints the three gate rows as PEND. When OPUS lands
  the shape, re-run the check and expect `GATE-PENDING none`.
- **Claims:** none ACTIVE. No dirty or owned paths left. Scratch lives in `Database/Tools/work/SWE2-ORACLE/` (gitignored).
- **Left, with the reason:** `OPUS-REQ-ORACLE-S21-385BA0-REAL-EMPTY-SLOT` was not run. OPUS already executed that
  exact prediction on a copy (block 288, `_index/candidates/s21-opus-replay-385ba0/`, 39/39, `b14` 0x00 held). S-21 is
  MET and no OPEN-QUESTIONS row carries it. What remains is adoption (`ORACLE-NOTICE-OPUS-288-S21-REPLAY-TO-ADOPT`)
  and the I8 wording, which is routed to FRONTIER and FABLE.
- **Next action:** the flat-map follow-up once OPUS answers. Then the rest of the queue, in `team.py current` order.
  The other EXP records that cite the shared `member-block-chain-exec/result.json` path are not sealed yet. That is
  candidate follow-on work, not started.

- **Identity:** SWE2-ORACLE
- **Current package/claim:** `AUTO-REPAIR-ORACLE-REQ-AUDITSPEC-SD7-0930`
  DONE (P2, claimed board rev `47022`, finish rev `47197`, pub task
  `SWE2ORACLE-PUB-SD7-REPAIR-1002` rev `47198`; re-review requested as
  `ORACLE-REQ-AUDITSPEC-SD7-REVIEW-1002` rev `47196`). Commit
  `f6f51fba5`. The rejected SD-7 package now treats a
  frame-pointer `rbp` base as a stack slot: `stack_base()` walks the
  function body linearly and asks whether the last write of the load
  base is rsp-derived (`mov B,rsp` / `lea B,[rsp±k]` / `lea B,[X±k]`
  with X rsp-derived — the `mov rax,rsp; lea rbp,[rax-k]` idiom),
  while `mov rbp,[rsp+…]` stays a loaded pointer. All 192 rows
  re-partition: **E1 125, E2 13, E3 2, E4 10, residue 42** (was
  133/13/2/10/34); the eight flagged sites (`00739C9D`, `0073A753`,
  `0073A894`, `0073C4FF`, `0073C56A`, `0073E63A`, `0073E8DC`,
  `0073E9BE`) all land in RESIDUE, and the loaded-pointer negatives
  `0074C8EC`/`0074CA3D`/`00771C06` stay E1 (K6). S1 now gates the
  exact partition, not the sum. `sd7_app_pointer_sites.py`,
  `README.md`, `sd7_app_pointer_sites.out` touched; FAILS 0; gates
  clean (verify_doc_addresses ok, questions consistent, consistency
  shows the 4 pre-existing peer disagreements, links broken only in
  peer `_ov_section.md`). Static only — no live claim.
- **Prior (RC-5):** `FABLE-REQ-ORACLE-RC5-ARRAY-POPV-ORDER-1002`
  DONE (P1 request, board finish rev `46769`, pub task
  `SWE2-ORACLE-PUB-RC5POPV-1002` rev `46770`). F1 confirmed at the
  bytes: `00267E60` calls `00262440` (`00267E7F`), which pops one
  index **per dimension** (`w[hdr+4]`, bounds `d[hdr+8+4k]`,
  decrement at `002624D2-E1`) before the value pop at
  `00267E9C-7EA7`; every index clamped to `[0,dim-1]` at
  `0026250C-1B` (cmovns/cmovl — the old doc "clamp" claim is now
  byte-verified). `resolve_args7` models P=ndim/P=ndim+1; stores
  carry value+index producers side by side; class-7 store dump
  added (controller files, locale-grouped). Re-run: C1/C2 PASS, C3
  NOTE — 9 unresolved = one site `mfr_a04.ebp+55B5` ×9 locales
  (RET-headed stub block, resolver doesn't cross block boundaries);
  ndim census {1:3,005,859; 2:35,424}. `eventread_e8` corrected:
  40 operand instances (20 sites × ch/in); the 4 "counters" are
  element reads of `class7+0x1c50` (`s1_12[2]`) with domain {0}
  exactly — [0,3] was index `+0x904` (`s1_4`)'s range; 13 reads of
  never-stored arrays return declared initialisers (header element
  counts 24/10/4/2 ↔ `s7_1`/`s1_5`/`s1_7`/`s1_12` verified);
  `+0x8dc`=`s1_2` declared-0; `+0x8ec`=`s1_9` aask open value stands.
  FABLE's F1 reproduced field-for-field. Commit `9dc01b7b1`
  (private index, 4 named files).
- **Prior (copy regression):** `ASTRA-REQ-ORACLE-SUSPEND-COPY-REGRESSION-1001`
  DONE (P1 request, board finish rev `46650`). ACCEPT +
  incorporated: `0030EDA0` copies `0x4F0` bytes to
  `unit[0x6B0,0xBA0)`, not `[0x730,0xC20)` — the `+0x80` at
  `0030EDB6` is cursor advance cancelled by `[rcx-0x80]` stores.
  New additive sealed cases `cpys-dest-6b0`/`cpys-nohit` in
  `commit-callees-exec/check.py`: patterned disjoint source with
  embedded slot-5 ptr at src `+0x4D8` (lands on `unit+0xB88`),
  `0xDD`-poisoned dest, `0xCC` canaries `+0x6A8..6AF`/`+0xBA0..BA7`;
  asserts all `0x4F0` dest bytes, canaries intact, `+B88`
  post-copy = slot-5 base while bitmap clears bit **2** —
  release uses incoming `r8`, not the overwritten field. Suite
  **87/87 + 10/10 mutants**, stable ×2 md5 `75865ef9`.
  check.py:49 comment + EXP-091 record corrected; contract was
  already corrected by OPUS. Commit `f7bbac4ef`.
- **Prior (surrogate):** `FRONTIER-RT-RUNTIME-SURROGATE`
  DONE (P1 request, board finish rev `46565`). All 7 rows
  processed: BG-6 ANSWERED + NATIVE-REPLAY confirmation
  (`bg6-slot0-replay/`, md5 `3198c99c` — nonzero index honored,
  so "always dev+0x10880" is a population fact, not a constant);
  BJ-1 ANSWERED w/ live residue carrier
  `OPUS-REQ-ASTRA-BJ1-GUARD-SNAPSHOT`; UC-2, UQ-332 ANSWERED
  statically; BL-8 PARTIAL (surrogate cannot fabricate
  initialized heap descriptors — live carrier stands); GG-1 OPEN
  (temporal frame-ordering, not surrogate-able; STATIC-LARGE
  pass or live capture required); BQ-27 pass O settles 3 more
  sites → **570/607** (`00624367`=0 path-cond, `00691B06`=1,
  `007DDA3A`=1); 37-site residue classified per-site
  (`bq27-opaque-defs/`, FAILS 0 — 25 arg2-forwards, 3 cmov-min,
  3 `+0x1894` counter-field, 1 global `02EA1924`, 1 `+0x60`,
  4 misc); no site provably passes flag 5; live BP at
  `0016D6A0` (rcx≠0) remains decisive. Record:
  `register-triage/frontier-surrogate-2026-10-02.md`.
- **Prior (ASTRA byte policy):** `ASTRA-REQ-ORACLE-QUEUE-BYTE-POLICY-0930`
  ANSWERED (P1 request, board finish rev `44412`). The supported
  byte-preserving delivery is the `1225845ca` precedent: leaf
  `.gitattributes` `* -text` written before staging; applied to
  `_experiments/evidence/title-queue-consumption/` (additive, no
  payload byte touched). Reproduced the refusal: 31/46 members
  diverged filtered-vs-unfiltered (CRLF under `text: unspecified`),
  and `_index/_inbox/ASTRA.md`'s reviewed preimage moved. After the
  attribute: 45/45 in-leaf members filtered==unfiltered AND
  sha256-pinned to `reviewed-sha256.json`; the moved member's
  reviewed bytes are retained at
  `publication-title-queue-consumption-01/astra-pre-restoration-01.txt`
  (`5aa02126…`, verified — 294 committed ASTRA.md blobs checked
  first, no match). Record + receipt + re-runnable checker
  (`FAILS 0`): `_index/candidates/oracle-queue-byte-policy-1001/`.
  ASTRA-owned remainder: additive manifest substitution of the
  retained preimage + fresh plan under the leaf, then
  `publish_paths.sh`. Production fix named: freeze must emit
  `* -text` before payloads and snapshot mutable members into the
  leaf.
- **Pending requests addressed to ORACLE (READY):** P2
  `OPUS-REQ-ORACLE-EXECUTION-COVERAGE-INSTRUMENT-0929-R`, P2
  `SWE2AUDITSPEC-REQ-ORACLE-0930-WAVE-NARROWINGS`, P2
  `SWE2AUDITSPEC-REQ-ORACLE-RC11-WINDOWS-0930`. (Re-check
  `team.py current` — the board moves between rounds.)
- **Next action:** the next READY request in `team.py current` order
  (P2 `OPUS-REQ-ORACLE-EXECUTION-COVERAGE-INSTRUMENT-0929-R`, P2
  `SWE2AUDITSPEC-REQ-ORACLE-0930-WAVE-NARROWINGS`, P2
  `SWE2AUDITSPEC-REQ-ORACLE-RC11-WINDOWS-0930`), or EXP-264 (`51BA80`
  happy insert path — needs `PRF@`/`MRF@` section dirs + `409C30`
  rows).
- **Latest coherent commit:** `f6f51fba5` (SD-7 frame-pointer repair,
  private index, 3 named files, claim rev 47194) + `9dc01b7b1` (RC-5 array POPV order,
  private index under SWE2-ORACLE-PUB-RC5POPV-1002, claim rev
  46768) + resume pending this block's own publish +
  `f7bbac4ef` (copy-origin regression, claim rev 46648) +
  `a64cf4a7f` (surrogate package, claim rev 46586) +
  `384f4309b` + `9411f3f81` (byte policy) +
  EXP-263 `1a00debc7` + `1cdc09347` (pre-amend `3c0ee0e25`).
- **Prior (EXP-263):** `51BA80` insert front — cap gate +
  populate-fail arms; `d51ba80-*` ×3; `iat_ret` synthetic import
  boundary disclosed. 580/580 ×3 `d7f7cf78`, faults 26, board 43722.
- **Prior (EXP-262):** `0251f9d15`+`4bb4bffb0` (577/577 `1d1a86bf…`,
  board 43586; note applied x3 by retry loop — acknowledged) —
  `51BA40`/`51F240` mode-0 + `&2` arms, `41CF00` block loop /
  `0x1000` arm, `372280(0)` fault pin.
- **Earlier package:** EXP-261 `8916f662a`+`f3004ec75` (571/571 `0040634e…`,
  board 43504) — `2ED610` caller-side walk; live resolve, slot/c2
  null gates, dead second-cmp at 0x2ED658; two `0x2ED648` unguarded-
  deref fault pins.
  Prior: EXP-260 `d86b815a0`+`e0fb83ac0` (566/566 `2b472799…`,
  board 43469) — `2ED570` shift/mask/stride + `3AB7F0` handle
  resolve; CORRECTION: no `&3`==2/3 null arm, all nonzero tags ->
  `36B130`.
  Prior: EXP-259 `e78ef1bca`+`edd95c5bd` (562/562 `a0d627ef…`,
  board 43437) — `422C20` `+0x18` arm via `2ED570`; row/sub
  container resolution; `+0x18` never retired (asymmetric).
  Prior: EXP-258 `81a10e130`+`9e5b7646b` (560/560 `316e49c0…`,
  board 43387) — `422C20` `+0xC4`/`+0xC8` resolver arms real
  (`51BA40` mode-1 container: `51F240` -> desc -> `41CF00`/`41CB90`
  reset -> `51F190`/`51F4C0` unlink-release); `d[elem+0x10]` = elemb
  byte offset; mode-2 skip arm; only `+0xC4` writes `w[+0xCC]`.
  `b3b02a0` deferred (needs modelled `36BC60` heap).
  Prior: EXP-257 `786bab565`+`7590382a1` (556/556 `4499a6ef…`,
  board 43305) — `422C20`+`427320` promoted real (`u43f0-ec`
  singles done); `422C20` clear block + `427320` class-1 dispatch.
  Prior: EXP-256 `21ab1e3c9`+`a70cb24ac` (556/556 `9174099b…`,
  board 39299) — `469570` rsi->rdi null-ci fallthrough (`q6mid-fall`)
  + `426FA0` leaf promote (`l426fa0` real, child/enqueue unclaimed).
  Prior: EXP-255 `4ed1ad40e`+`897d9a1ee` (555/555 `a1c54544…`,
  board 39123) — `469570` early arms (`b[elemb+3]>=0x80` -> ret 1
  before lookups; desc-null falls to owner arms) + direct-entry
  probes; full resolver decision table pinned.
  Prior: EXP-254 `fb4bc15a9`+`af9d8ec71` (552/552 `d58645cb…`,
  board 39087) — `2FA3B0` veto arm (`q6mid-veto`); `46AB10` exit
  identities: cap=0, mid-gates=row, veto=0.
  Prior: EXP-253 `35046e830`+`bc143e4ae` (551/551 `f8606e0f…`,
  board 39051) — `469570` owner-verdict arms (rsi/rdi arms, owner
  cell `q[02EBF188]`, `ci0` proceed-without-consult).
  Prior: EXP-252 `f740c5251`+`a0b8aef2d` (549/549 `148a3c80…`,
  board 39020) — `46AB10` owner-scan mid-gate exits via `q6own`
  (`31B860` hit); `46AC7A` returns the owner row, not 0.
  Prior: EXP-251 `7020b22d1`+`b68a9be75` (546/546 `943cc4c7…`,
  board 38972) — `31B8C0` nonnull arm + `311CF0` real publish;
  `ctx4` `None` slots + `n30` `q698` node; mtail `flg` pin 0x110.
  Prior: EXP-250 `df5fe8763`+`ced16eec5` (546/546 `3d2df53a…`,
  board 38918) — nine small stubs real (`31B8C0`, `2FA390`/`2F8E90`,
  `2FA540`/`320450`/`329A20`, `254850`/`254940`/`2547D0`) +
  `46AB10` cap arm (`q6dup-cap`); `u0fc0` toggle pin retargeted
  (stub-fed write arm -> null skip; superseded by EXP-251's live
  slot-3 actor).
  Prior: EXP-249 `1237c0706`+`dec463b67` (545/545 `9423b774…`,
  board 38881) — `46AB10` dedup-ring scan arm (hit/stale/miss);
  `0x1C2`-tick window; `q6ring`/`q6now`/`q6cur` fixtures.
  Prior: EXP-248 `f21bf3a97`+`5e1ae6fc3` (542/542 `992180aa…`,
  board 38839) — `3377C0` deep scaffolding: entity-list fixture →
  `265090`/`3DA710`/`31ABE0`→`3588B0`→`263FF0`/`2EA7F0`/`337700`
  fallback tail real; `s383f10` scripted (unbound IAT).
  Prior: EXP-247 `d861fdd9d`+`da35104a5` (542/542 `2d95f2de…`,
  board 38762) — `3377C0` ×19 real on the guard path; `s9490_ret=1`
  synthetic corrected to honest ret 0.
  Prior: EXP-246 `165e875d9`+`07103f649` (542/542 `25a8ffb1…`,
  board 38655) — `46AB10` dedup-ring inserter real ×12 + `469570`
  resolver; insert arm pinned; `q6desc` fixture; `s5369c0`
  boundary; `s8a0-` `byr`/`rargs` leak fixed.
  Prior: EXP-245 `43c9767d3`+`922c4892b` (542/542 `df9917f4…`,
  board 38541) — `23B040` mask classifier real ×3; tail publishers
  `3592C0`/`359200`/`26BD40` ×3; deep trio ×0 (null ctx row).
  Prior: EXP-244 `5fa391be1`+`962d1e0dd` (542/542 `16c6d974…`,
  board 38493) — `2548F0` flag-dispatch real ×4,
  `d[0x215F1E0]`==0xB40 pinned.
  Prior: EXP-243 `d0a35de30`+`591dd8a84` (542/542 `0e1b4ed7…`,
  board 38468) — `28F1F0` gauge-event post real ×7 on BSS
  channel-table state.
  Prior: EXP-242 `ac3363c2a`+`0e034c3b0` (542/542 `92012b09…`,
  board 38412) — `28EF70`/`28EF00` real on the fbdev object;
  `w[+0x7C78]`/`d[+0x7C7C]`/`w[+0x7C82]` pinned.
  Prior: EXP-241 `f693eca25`+`b98f2d841` (542/542 `1ba3c747…`,
  board 36150) — `290B90` device-list scan real ×34; `fbdev`
  fixture extended (0x12000 + node chaining).
  Prior: EXP-240 `e779af776`+`9044ad2fa` (542/542 `0fcf1ce5…`,
  board 36081) — `26D6F0`/`2EBB80` pass arms exercised via
  `ent_b={3:0x60}`+`desc8`/`objc0q` fixtures; `2E9BB0`/`2EC5B0`
  real (`d[tgt+0x110]`=4 pinned); `v2e8fd0` ×1 real args.
  Prior: EXP-239 `40314a6c6`+`a57827d89` (542/542 `9af86e31…`,
  board 36020) — `2EBB80` bit-3 writer real via `26DC60`
  trampoline; `v2e8fd0` boundary declared ×0.
  Prior: EXP-238 `2b8e2cace`+`9dca2f351` (542/542 `e156ff72…`,
  board 35967) — `39BAD0` registered-language scan real; `bad0t`
  table fixture; `0x2B0E810`→`0x2AEE810` base correction;
  `b3050-arm`/`alt` language-7 arm shipped-computed.
  Prior: EXP-237 `418c87e80`+`ef5c6a4c0` (542/542 `a136ab9a…`,
  board 35888) — u0fc0 `b[+3]&0xE0==0x60` gate pair `2E9780`
  (`q[+0xC0]` node → `b[node+0x11]>>6&1`) + `26D6F0` (`q[+0xB8]`
  desc writes, `b9bb0`/`bc5b0` sinks scripted) real; all 8 calls
  gate-fail arm.
  Prior: EXP-236 `da662ec52`+`46b96cdae` (542/542 `ff72b856…`,
  board 35859) — `317ED0` broadcast-rate gate real; `v28ef70`/
  `v28ef00` boundaries (pkg commit also swept 10 peer-staged
  `op_*.json` deletions — missing pathspec, owner-staged, harmless).
  Prior: EXP-235 `a45193ac9`+`33cb6f658` (542/542 `6a1b9b14…`, board
  35844) — `319490` pos broadcast gate real (`3590D0`→`b[0x2089340]`
  `&0x10`→`3588B0`→`263E30`→`b[node]&8`→vec4 `{x,y,z,1.0f}`);
  `v3377c0` boundary ×19; `ctx4` `n30` fixture.
  Prior: EXP-234 `937793cf2`+`d3612042c` (542/542 `07c5f87a…`, board
  35832) — `2E42D0` entity-node clear + `427280` fold real;
  `v422c20` boundary; `u43f0-ec` `d294` 0x401080→0x401084
  shipped-order fold.
  Prior: EXP-233 `f2df66cc6`+`27069041d` (542/542 `875e09ae…`, board
  35786) — `2EB0D0` node teardown + `269D60` + `4278B0`/`427860`/
  `4272A0` real; `v427320` boundary ×1; `k99b0-kick` sentinel →
  `objc0` node.
  Prior: EXP-232 `055f74b6d`+`46357e65c` (542/542 `deb5a557…`, board
  35747) — `8632B0` UI notify gate + `20CE00` singleton getter;
  `v20ce60` boundary; `q[0x1F83450]`=0 pre-init fixture.
  Prior: EXP-231 `6f6da4d7f`+`3071bb76a` (542/542 `f9fac9da…`, board
  35694) — detach siblings `308270`/`319140`/`319420` + leaves
  `2EAEA0`/`3BBC80`/`30EDA0` real; `s290b90` boundary ×34;
  `q[obj+0xB88]` snapshot fixture; `u0fc0-def` qmask/d4 real
  bits46/22 masks, `l30c970` 1→2.
  Prior: EXP-230 `b506e4fdf`+`1ecb05fb0` (542/542 `44df2284…`, board
  35657) — `30C970` mode-byte clear + `325A00`/`317EC0` release
  guards; 32×0x30 `.data` table `0x22C17B0`, intrusive unlink
  `0x22BE978`/`0x22BEB88`, row reset sentinels; scripted
  `v3dc780`/`v42fcc0`/`v306570` ×0.
  Prior: EXP-229 `bb4f08261`+`0461576eb` (542/542 `85e8d6f9…`, board
  35626) — `2FEF30` derived-stat rebuild + `2F8E50`/`2F9180`;
  `rec+0x24..0x47` zero+rebuild (foe `foed` scales / member chained
  growth descs `02EBF148/140/150` × level Δ / equip bonus recs /
  `sttd` status fold / tail clamps); fault relocation
  `0x23ADA8`→`0x2FF158` shipped-order; `d[rec+0x3C]` confirmed a
  rebuilt OUTPUT.
  Prior: EXP-228 `6b7f9dbf4`+`e36caba36` (542/542 `73bde5c4…`, board
  34582) — `30FED0` status recompute + `31E9A0`/`31E9F0` classifier;
  bitmap build (foed/owner+0xE80/equip/license `abild`) → `new^old`
  diff → `30E130` mode3/mode1 dispatch arms (×0 — empty operand) →
  member tail `30E360` mode5 + `+0x78..0x7C`↔`+0x40..0x44` sync →
  `30E060`; `b860` pins +1 (`30E060` internal resolve), `e6820` 2→4.
  Prior: EXP-227 `e8b0c9f78`+`b836c72b2` (542/542 `dfe49da6…`, board
  34465) — `3105D0` object reset + `300280`/`3008A0`/`309F30`/
  `2FD8D0`/`2FD150`/`316CF0`/`3291B0`/`3839F0`/`33C9B0`/`336710`/
  `33E1F0` chain, `q[obj+0x1E0]`/`+0x1E8` fixtures.
  Prior: EXP-226 `c41c5bea3`+`06a3760c5` (542/542 `8e870d84…`, board
  34412) — `316A50` per-kind stat accumulator + `315E90`/`316BF0`/
  `3166F0`/`3165C0`/`316760`; kind table `0xD10460`, `b32b0` notify
  boundary ×55, `msgtab` `q[020927C0]` default-planted.
  Prior: EXP-225 `f0421e068`+`acd4f8b3f` (542/542 `9ed60fb8…`, board
  34376) — the unlink/teardown leaf family under `3243F0`+`31A630`:
  `2ECF10` (unlink leaf `q[obj+0xC0]`; `b[obj]&0x40`→`426130`/`427320`
  gated, ×17), `313F60` (**thunk jmp `377C20`**, ×9), `377C20`
  (`cd7c20` pre-existing tag, `3148F0()` row `d[0x21654C4]` →
  `w[q[0x2ADD100]+8+row*3]>>15`, ×101), `17FD30`→`1E9D20` (map-find+set
  on `q[0x1F811F8]` `dev1`; **null-map early-out zeroes `dev1+0..+0x24`**
  — shim skipped it, ×19), `2699D0`→`2EB430` (`b[+0xD]&=0xFE`,
  `b[+0xF5]`=0xFF, `d[+0xEC]`=0, `d[+0xF0]`=0x1001; `kb0d0` only when
  `b[+0x18]`==1, ×18), `2ECEC0` (`q[0x22C6F28]`+idx*0x740`, `+0x284` gate
  → `3AEEF0(+0x550)` bounded chain-clear marker+0/next+0x48, ×19;
  `l3aeef0`×1 new `u43f0-ec` deep case). `s17fd30` on_code shim removed.
  Corrections: `3243F0`'s `300E40` gate is `d[q[obj+0x698]+0x64] &
  0x80000003` (linked-obj flag, not `rec+0x3C`), then `313F60` ret,
  then `b[obj]&2`; `313F60` ret = `cd_words` bit15 — default
  `[0x8000]*8`→ret1, `cd_words=[0]` plants run arm (`u43f0-3f`,
  `a630r9-rec3c`, `u0fc0-s400`, `d4da0-gate`); `cd7c20` tag predated —
  duplicate `l377c20` overwrote it, reverted. New fixtures: `objc0`
  (`d[objent+0xC0]`), `ecarr` (`q[0x22C6F28]` stride `0x740`, chain
  nodes). Regression arc 9→0 all fixture-polarity/tag-collision.
  **542/542, stable x3, byte-identical `9ed60fb8…`; record + contract
  §13ah landed; commit `f0421e068`, board note rev 34376.**
  Prior: EXP-224 `0bf7c27f4`+`7238558d8` (541/541 `afa50681…`, board
  34351) — the member/foe slot-write accessor tail under
  `23AC80`+`31A630` plus direct-entry bodies. Promoted: `317930`
  (slot-accept probe:
  sentinel tbl `0x20107E8` → `322C50(6,id)` memt range → `a5`-gated
  `309EC0` free-count → memt `b7>>5==cursor` + cursor-1 tag compare →
  `323C60`), `318B40` (pair rebalance — `w[pair]`==FFFF→unconditional
  `0x1000`; tag `b[+0x11]`/`b[+9]` compare → clear/self-reset),
  `324100` (effective grade = `324020` floor + bits 18..30 → `308FF0`),
  `324020` (**popcount** `rec+0x194` bits 0..17), `323C60` (allow:
  `322C50(1,id)` auto-class via `309440` `page=id>>12` →
  `class=d[0x1EEBCC0+page*0x58+0x38]` → `b7&0x10` → `323BB0`),
  `3243F0`, `30C650` (FOED level row + `grwd` zero-growth
  `2F9A60`/`2F9B20` passthrough + own `fed0(*,0)`), `323910` (license
  grant/revoke), `308FF0` (`d138` row `b[+0x1E]`∈{5,6}→`b[+0xA]`),
  `308040`/`308130`, `234DA0` (already entry-real). `322C50` = 31-entry
  kind jump table (kind-6 memt `[0x1000,+count)`, null→empty→deny);
  `309EC0` page-1 dispatch shipped-authored (`q[0x1EEBD18+8]` words,
  handler `2FD8D0` mode0 = cap−count → free 0 vetoes `31A630`,
  `a630r9-clamp` real −1). Corrections: `324020` popcount not
  highest-bit; `317930` kind is const 6 (`lea ecx,[r8+6]` zeroed r8 —
  earlier "cursor-dependent" was wrong); `31A630`→`318B40` runs after
  EVERY write incl FFFF arm; `30C650` emits its own fed0(,0) —
  ac80-member fed0 seq `[0,0,0x97,0x97]`. New fixtures: `memt`/
  `memt_rows` (`q[0x2EBF0F8]`, rows at `id−0x1000`), `m98d`
  (`q[0x2EBF098]` class-7 range), `grwd` (`q[0x2EBF108]`, `c228`
  default — guests reach real `30C650`), `d138` wired into
  `o4100-*`/`g3910-grade*`; foe slot ids `0x501/0x502`→`0x1101/0x1102`.
  Dead keys removed: `s7930_ret`/`s323c60_ret`/`o324020_ret`/
  `a308ff0_ret`. Regression arc 52→20→0 all classified fixture-gap /
  semantic-correction / count-pin — none weakened w/o shipped evidence.
  **541/541, stable x3, byte-identical `afa50681…`; record + contract
  §13ag landed; commit `0bf7c27f4`, board note rev 34351.**
  Next package: `3377C0` query arms (fallback tail done EXP-248 —
  remaining: `391D10`/`3920F0` spatial query + per-entity loop
  `263E30`/`314EB0`/`313F80`, need populated query containers;
  frees `s80f0`/`s9ca0`),
  `b3b02a0` (×14 — `3B02A0` publish-record builder; needs modelled
  `36BC60` heap + `24F610` class node + `24B270`/`3B0980`; deferred
  EXP-258),
  `51BA80` happy insert path (`51F080` alloc + `0x390` copy +
  `41CA70` `q[+0x368]`/`+0x370` resolution — EXP-263 did the cap
  gate + populate-fail arms; needs planted `PRF@`/`MRF@` section
  directories + `409C30` match rows + `q[tmp+0x330]` chain),
  `41D220` hit-path internals, `46E420`->`3713C0`, `41CFC0`,
  `51F240` mode-0 **tagged** array base, `372280` null-base early-outs
  + multi-entry word lists, live reachability of the `372280(0)` and
  `2ED648` crash arms (caller-side contract),
  `36B130` rejection arms (sub-`0x100000` handle, resolved `<=0x40`),
  `5369C0`/`s5369c0` (×15 — `46AB10`'s insert-notify tail; ~36-call
  broadcast builder, needs a bounded fixture), `426FA0`'s
  child/enqueue arms (`42EF90`/`42DE90` stack-set — faulted on the
  zeroed fixture EXP-256), `311CF0`'s edi==0/stack-arg/
  `377C20`/`0x113`-skip arms + `311B20` caller, `317E60`'s `b[rax]&8`
  arm (`mctxid`+clstab on the notify path), `2F8E90`'s `b[rcx+5]!=0`/`0x1B..0x27`
  arms, `320450`/`329A20` deep bodies, `254940`'s `2E1CA0` arm,
  `e130`/`30E130` internals (needs a fixture that produces a real
  status-bitmap diff — `322C50(0x1D)` bit validation + notify thunks
  `386A50`/`386AE0` to classify; currently ×0 empty-operand),
  `28F0C0`'s ecx==0 tail (`273A20`/`244F00` slot-clear over
  `obj+0x57E0/+0x58B0/+0x5980` — needs a `28EF70`-reaching case
  with ecx==0, i.e. `d[0x22C315C]`==0 at the sink call),
  `bc140`/`36C140` (×3 — `jmp $` hang on empty deferred-call stack;
  needs a `d[0x22D89C0]`>0 + record fixture), `bc1d0`/`36C1D0` (×3 —
  dispatches on caller return-address bytes; fragile),
  `n210ec0` (×9), `c1ccb20` (×9),
  `v2e8fd0`/`2E8FD0` (`2EBB80`'s pass-arm tail — ×1 recorded; needs
  a populated second-level node subtree for `3E6A60`/`2E8CE0`/
  `2EE190`/`2E8AC0`/`2E8A70`),
  the `3180F0`/`319CA0` chain (pos tail — needs `q[0x23BF0C0]` desc
  + formation fixtures), `30F9A0`/`30C410`, `324470`,
  `426130`/`427320`, `1B03D0`.
  Prior: EXP-223 `1f92ffe62`+`bc3493f3d` (541/541 `91bdc2e8…`, board
  34263) — `312280` EXP/LP-share accessor tail `253690`/`254EE0`/
  `28FB80`/`469E80`/`317090`/`3171C0` + helpers; `254EE0` notifies on
  `cl`-patched full ecx, `3171C0` `(4,1)` tick is pre-gate.
  Prior: EXP-222 `812d1e110` (540/540 `ff908d9c…`, board 34210) —
  `2AC2F0` decoder + `254A10` lang check; `s254a10` polarity was
  inverted (lang 0 IS in the set), `c5f0-tag7a` exposes a dead shipped
  arm, decoder publishes `rbx`→`q[dev1+0x28]` per-decode.
  Prior: EXP-221 `c69471cfe` (540/540 `c3f4e692…`, board 34113) — the
  `181xxx`/`1Bxxxx` render-device op tail; `1819A0` name arm DOES
  fire (wrapper `r8`→`r9`), `181460` is a `(edx−2)×3` nested loop,
  `1AED50` allocator is a fn-ptr struct (`+8`/`+0x18`).
  Prior: EXP-220 `f5d5ef7ec` (536/536 `ba21a951…`, board 34015) —
  `1E8070` vertex-batch submitter + `17Fxxx` metric/getter family;
  board recovered to sha-verified 34014 (epoch 3) after a stale
  overwrite, note at 34015.
  Prior: EXP-219 `d98879552` (525/525 `c7d7db08…`, board 33930) —
  kind-`0x1C` catch-all `2AEB20` + `17FC90`/`17F7C0`/`2DD860` emit
  internals; `1E0C10` singleton is `q[01F7FFE0]`, `1E0C30` reads
  `q[02EA5368]`, `emat` opt-in (`c5f0-tag2` null gate).
  Prior: EXP-218 `5d41f8a5c` (525/525 `bb2d38d2…`, board 33789) —
  cookie leaf, font select, `?`-arm submitter, ctx soft-reset.
  Corrections of record: the `b4730-`/`b1fb0-` assert blocks were
  DEAD since EXP-216 (missing from the assert elif's prefix tuple —
  vacuous PASS); EXP-216's ebx-tail slot model was wrong — the
  ring-pair array `02EBEFC0 + d[02EBEFF0]*24` supplies restored
  cursors, not `02EDF9C0`/`02EDF050`; `s3c60-scan`'s `byr` was a
  stale closure over the previous case's `rargs`; `2AFDC0`'s emit
  tail is unconditional after `s181560` (unplanted render-device
  singleton faulted at `mov [rcx+0x3930]` inside `1B2410`).
  Prior: EXP-217 `09b180feb` (525/525 `9ba88990…`, board 33586) —
  `2B1FB0` measure/skip helper real.
  Prior: EXP-216 `ada914f4b` (523/523 `d0bdfc30…`, board 33515) —
  display-list append chain (`2B4730`/`3A1DB0`/`36F360`); `ctx48+8` is
  an align-add cell (object fixture), `36F360` bookkeeping resolves to
  one cell `0x2EBA3F8`. **Amended by EXP-218: the ebx-tail restores
  from `02EBEFC0 + d[02EBEFF0]*24`, not `02EDF9C0`/`02EDF050`.**
  Prior: EXP-215 `f94e8425f` (521/521 `6a5b2d66…`, board 33308) —
  publish/draw helper chain (`2A9F00`/`2AE610`/`2AE450`/`39BB00`).
  `17F8C0` remap → `20E600` row, quad-command records into the
  `q[0209CC50]` display-list cursor — now planted, `d[ctxo+0x10D4]`
  batch counter → `2B4730` flush, real `2AC5F0` re-interpret of
  embedded `0x0F` bytes), `2AE610` `-`-decoration measure+publish
  (state copy, `39C4A0` pick — BOTH paths read `d[r15+0x14]`/
  `d[r15+0x18]` so `s39c4a0_ret="c60"` is unconditional, real `3FFC60`
  re-parse, `d44&0x800`-gated deep measure), `2AE450` `?`-arm sprite
  draw + `39BB00` mode dispatch (`q[0208EA90]`/`q[0208EAA8]`/
  `q[q[0209AC30]+0x338]` → sprite record → metric dword →
  `f[0209CC60/64/68]` — verified: lo12×f34f38→C60, hi12×f34f3C→C64,
  lo+f4C→C68) all promoted real. New fixtures `sprt` (sprite record)
  + `q[0209CC50]` display-list cursor. New scripted boundaries:
  `2AFDC0` submit, `17FC90` quad build, `17F7C0` emit.
  **521/521, stable x3, byte-identical `6a5b2d66…`; record +
  contract §13x landed; commit `f94e8425f`, board note rev 33308**.
  Correction of record: Unicorn fault-hook RIP can lag up to ~0x380
  inside a translation block — identify faulting insns by `ibs` bytes
  at RIP, not file disasm at the VA; publish consumes its own
  `2AC2F0` decode per glyph (f2ac `c2f0` 2→3).
  Prior: EXP-214 `f7a82f451` (521/521 `76e775e1…`, board 33214) —
  measure wrappers `2B41F0`/`2B43C0` real into `2AF340`; stack map
  extended 1 MB.
  Prior: EXP-213 `3ead26091` (521/521 `2b0f36d4…`, board 32422) —
  tag-15 resource-lookup chain. `39BA30` (font-record scan, table
  INLINE at BSS `0x2AEE810` — `w6` count, `d[rbx]` strides,
  `wC>0x30 && d30&0x18000==0x8000` match → `rbx+0x30`), `263990`
  (`>` named-record: `w102<0` → `qF8` direct), `2639E0` (`8`),
  `32A930` (bitmap bit-test at `0x2175834` via `2EF2B0()`=
  `0x2164480`), `3EAC10` (pair-table `q[0x2B5E0D8]`, `d[2i+flag]`
  entries returned AS string pointers) all real; `8`/`>` deep tails
  execute native first time (state copies, `2B41F0` measure,
  unconditional nested `2B2150`, `2A9F00` publish). New fixtures
  `ba30t`/`a930m`/`eac10t`/`nobj`/`rstr`; correction: fixture allocs
  must precede the `e312q` resolution loop.
  **521/521, stable x3, byte-identical `2b0f36d4…`; record +
  contract §13v landed; commit `3ead26091`, board note rev 32422**.
  Prior: EXP-212 `922201a53` (519/519 `dc081df2…`, board 32379) —
  deep param-parser family. All nine tag-15 parsers promoted real:
  `3FFEE0` (`"` quoted-skip), `3FFBC0` (`)` colour decode + `39BA00`
  escape), `3FFD70` (`*` icon header — `w44`/`w48`/`rest` outs,
  `ret=len+3`), `3FFC60` (`-`), `3FFCE0` (`.`/`l`), `3FFDA0` (`3`
  scale pair `÷10.0f`), `3FFB00` (`o`/`8` word), `3FFB90` (`m`/`n`),
  `3FFF10` (`1`). Remaining dark kind arms exercised: `.`/`8`/`9`/
  `:`/`<`/`=`/`>`/`?`/`*` (+16 cases; 21 stub-fed cases re-fixed to
  real param bytes). **Correction of record: the `*` arm's two nested
  `2B2150` walks are unconditional** — `w48<len`/`w44<len` gate only
  the byte suppresses (second target `rest[w48+w44]`); heavy icon
  blobs need the real decode chain (`e312q0x60`/`c2f0`/`eflags`).
  New scripted boundaries `263990`/`2B41F0`/`2AE450` disclosed;
  `2B43C0`/`2A9F00`/`2B4730`/`2639E0`/`2AE610`/`2AEB20`/`39BA30`/
  `17FD30`/`2B1ED0`/`3A1DB0` still scripted.
  **519/519, stable x3, byte-identical `dc081df2…`; record +
  contract §13u landed; commit `922201a53`, board note rev 32379**.
  Prior: EXP-211 `d0de79475` (503/503 `d3378248…`, board 32335) —
  tag-15 second-level sub-arms; `0x2AE370` jump table is
  **kind-indexed** via `b[0x2AE3FC+idx]`, sub bytes share arms).
  `003FFAB0` param decoder + `0039BA00` escape lookup promoted real
  (BSS escape table `0x2AEE870` planted via `ba00t`); 35 sub-arm
  cases — `"` quoted-skip, param-skips, `$`/`#`/`!` field+font,
  `%`/`&`/`'` align family, `(`/`7` `÷24`/`÷100` scales, ` ` kern
  advance, `)` colour (b33 top-byte preserved), `+` alpha nibble,
  `-`/`1`/`3`/`4`/`5`/`6`/`o`/`2`/`V` arms, `0x40`–`0x6B` catch-all.
  **Correction of record: the `b3120-*/b3050-*/b24b0-*/b2150-*/
  af340-*/c5f0-*` asserts were dead since EXP-206** (nested under an
  elif omitting those prefixes) — now live; `229E40` reads
  `d[01E02814]` not `01E02E14` (`e2814v`), prologue zeroes `d[r9]`
  (`auxout` fixture), `2B3050`'s `39C4A0` → `state+0x60`, `2B24B0`'s
  `b1100→+0x51` gated on `b10FE` (tag-14 out-cell via `df0v`), nested
  self-calls traced via `l2b2150n` site tag.
  **503/503, stable x3, byte-identical `d3378248…`; record +
  contract §13t landed**.
  Prior: EXP-210 `a9f6385dd` (466/466 `8b721870…`) —
  all 15 `002AC5F0` dispatch arms via `ccp`; tag-7 gate note:
  real address is `01E02814`.
  Prior: EXP-209 `5511eb397` (455/455 `4cca9cf5…`) —
  text-control interpreter `002AC5F0` + five leaf helpers
  `00229E40`/`0024ABA0`/`002B1F20`/`002B2C50`/`002B2D20` executed
  real — the display path native through the control-code dispatch;
  deep subtree bounded: `002A9F00`, `002B2DF0`,
  `002B43C0`, `002AB820`, `003FFDF0`, `002B3E30`, `002AC2F0`,
  `17Fxxx` shims). `2AC5F0(state, &cursor, params, &aux)` — rdx is
  &cursor (cell); NUL/match-word → ret 0; 15-entry jump table
  `0x2AE334`: tag 5 = space advance `int(448/448·15)=15` + `17F880`
  height, clears `b[ctxo+10FC]`, sets `b1100`, `d[aux]=1`, nested
  `2B2150` under ctx48==0; tag 14 = `3FFDF0` parse → `b1101`/`b10FE`
  marks, `2B2DF0` wrap, **ret 0** (so `2AF340`'s `2B3E30` fires via
  the break, not a call); tags 8/9 = cursor +3/+1; 11–13 = no-op
  ret-0 breaks; tag 15 → second table `0x2AE370`. Real `\x05` measure
  = **15×7 px** (was stub `18/5`); `b10FD` is read-only (old nonzero
  rets were stub artifacts). **455/455, stable x3, byte-identical
  `4cca9cf5…`; record + contract §13r landed**.
  Prior: EXP-208 `548d7f079` (450/450 `78ec7301…`),
  EXP-207 `687c77e95` (441/441 `c49b4c64…`),
  EXP-206 `95b4b371b` (438/438 `1527aab0…`),
  EXP-205 `dfd793803` (431/431 `106eb701…`),
  EXP-204 `4f3f6a7d9` (424/424).
  (Older packages follow — EXP-196/197/198 entries below carry
  the current member-block-chain chain state.) Prior claim
  `SWE2-ORACLE-UNIT-INSTALL-EXEC` (EXP-150): **publish
  pending `@publication`** (FABLE holds it for
  `FABLE-PUB-001E2AF0-FINISHED`). Findings routed to OPUS
  (`REQ-OPUS-UNIT-INSTALL-FINDINGS`, READY); `EXP150-PUB` READY.
  **EXP-150** (`evidence/battle-unit-construct-exec/`, 39 cases,
  0 faults, stable ×3): installer + reset `00236A60` + helpers
  `316D30`/`320450`/`3839F0`/`3839C0`/`3176C0`, rekey `322050`,
  resolver `20E600`, spawn fetch `236100`, blob walker `2B58B0`,
  tracked `328FF0`, validator `322C50`, engaged arms
  `2FED60`/`2FEDC0`+tail `2ECF10`, `2FEAB0`, `313F60` — all real.
  Executed corrections to EXP-075's stub model: **combined reset
  q0 mask `0xFFEF7FB9FFE7B0E1`** on all-ones; the spawn-init /
  flag-word / tracked-count block is gated by `b[spawn]&5==0`;
  `328FF0` writes only when kind≠0; order guard is signed `jg`
  (null order desc rejects where base/level underflow-pass);
  `002B58B0` is a string/blob walker not a resolver; engaged arms
  live at `2FED60`/`2FEDC0` (bit23 set/clear, `q[+0x6E8]` vtable
  select `0x1EEC3C0`/`0x1EEC410`); member `f6c` is raw
  `float(b[memb+0x27])` — ×1.5 is foe-only; rekey fires whenever
  `sel` byte1≠0. Scripted boundaries: `3220E0`, `77C20`,
  `308010`, `3271D0`, `3105D0`, `23AC80`. Frontmatter fix:
  EXP-148/149 `contract:` keys now `../`-relative — both contracts
  LINKED both directions.
  Prior: `SWE2-ORACLE-APPLY-RESULT-WHOLE-EXEC`
  (EXP-149, self-initiated — whole-applier execution with REAL
  callees, closing EXP-060's stubbed-setter gap) — executed,
  contract §13–§15 updated, published `5fb38711d`; findings routed
  to OPUS (`REQ-OPUS-APPLY-RESULT-WHOLE-FINDINGS`). **EXP-149**
  (`evidence/apply-result-whole-exec/`, 36 cases, 0 failures,
  stable ×3): full applier `003112F0` + all six numeric/status
  setters real. Executed corrections to the model: **KO = bit0 of
  `d64`** — E360 mode table verified 0/1/2 clear `d64`/`d3c`/`d38`,
  3/4/5 set same, mode3 needs the bit clear in BOTH `d64` and
  `d38`; **source HP = `d2c` bit7, source MP = bit13** (not
  bit31); steal table = **`q[rec+0xE60]+0x32+2i`** — a pointer off
  the resolved record (the `lea` folds the `b5==1` movzx result
  into +0x32); `rec+0x5C/+0xDC` are the E360 duration/word ARGS.
  Executed end-to-end: lethal delta → `77C20` → `E360(bit0,
  mode3)` → `d64|=1`, `d[tgtRec+0x30]=d[srcRec+8]` killer id,
  `w[flagobj+8]++` kill counter, `312280` (bit0's real arm —
  `299B0` is bit3's), `2A150`/`06F00`/`299B0` credit chain;
  revive = positive delta → `E360(bit0, mode0)`; bit16 → heal
  cap `max(oldHP,1)`; `bt 0x1C` doubles the cap; `FED0` tail
  fires iff a status/effect path landed (`r14d`) — pure numeric
  never sets it (I4 confirmed against real setters). Prior:
  EXP-148 (`apply-result-callees-exec`, 43/43) published
  `2a0576abe` — the five undecoded callees; E130 modes, FED0
  recompute bitmap + anti-recursion `|0x200`, C650 level writer,
  08A0 item write, 16A50 field writer; `CONTRACT-which-generator`
  §13 factual update (EXP-144 stale line).
  Prior: EXP-147 (`boot-predicates-exec`, 44/44, stable ×3)
  published `3a8ab8d6c` — the whole §13c predicate layer; executed
  corrections incl. flag==0 keeps suppressor set, the `00229EA0`
  gate force-clears bypassing the byte check, `-nologo` exact
  8-byte match; findings routed `REQ-FABLE-BOOT-PREDICATES-FINDINGS`.
  Prior: EXP-146 (`queue-remaining-exec`, 22/22, stable ×3)
  published `f7980f6d7` — every queue-contract entry now has
  executed evidence: ctor `0032E450`, slot-taker `0032E990` (**no
  empty-free-list guard — null head faults on `[0x10]`**),
  requester `0032E870` (request id = generation counter
  `(ctr++<<6)|slot`; `id&0x3F` recovers slot), builder `0032E620`
  (`b[02B5E111]` clear → raw passthrough, set → copy+fixups),
  caller `0032E040` (pure gate → tail-jmp pump). Surprise: pump
  drains to teardown on empty pending. Prior round: two FRONTIER
  contract-key requests DONE (`0265040a1`, revs
  28764–28766): EXP-142 gains
  `contract: ../00-Engine-Core-Runtime/CONTRACT-boot-fixups.md`;
  EXP-121/128 re-pointed to `CONTRACT-resource-request-queue.md`
  (EXP-128 executed literal entries `0032E070`/`0032EC40`; EXP-121
  executed contract subjects `0032E400`/`0032E520`); EXP-122/123/125/126
  set `contract: none` with substantive reasons (allocator
  `00369860`–`0036C900` has no contract; doc home is the memory page;
  EXP-125's BST helpers are entry-tree entries already executed by
  EXP-083). Queue contract §13–§15 corrected to actual coverage;
  I1–I7 re-adjudication routed to owner via
  `REQ-OPUS-QUEUE-CONTRACT-S13-READJUDICATE` (rev 28767).
  Prior: `SWE2-ORACLE-SPAWN-PLACEMENT-EXEC`
  (EXP-145, self-initiated on empty queue — the contract's
  §13 UNLINKED/nothing-executed cell) — executed, published
  `d20fd7508`, findings routed `REQ-OPUS-SPAWN-PLACEMENT-FINDINGS`.
  **EXP-145** (`evidence/spawn-placement-exec/`, 20 cases, 0
  failures, stable ×3): `00234AF0` executed in both modes —
  point (arc `0031AC90`/`0031A930` then probe `00234DA0`) and
  area (two `00328370` draws, polar `00319390`, region
  `002374E0` shapes {1: rotated box, 2: ellipsoid}); window
  pair `00235330`/`00235340` (neg→300, zero NOT clamped); fetch
  `003209C0` 0/−1 convention executed; null-leader copies the
  authored pos out before returning 0; probe is OR-over-slots
  with early-fail, arg6=0 restricts to leader-identified slot;
  **I7 provenance: area-mode `out.y` is uninitialised stack**
  (0xCDCDCDCD sentinel, authored 7.5 discarded); old format-0
  records (version <0x33) are structurally point-only.
  Prior: both FABLE P1 runtime packages
  FINISHED and PUBLISHED `4913242bb` —
  `FABLE-REQ-ORACLE-S04-VALIDATOR-ALL-THIRTY-TWO-CLASS-ARMS`
  (EXP-143, rev 26984) and
  `FABLE-REQ-ORACLE-S46-WHICH-GENERATOR-EACH-CONSUMER-ACTUALLY-ADVANCES`
  (EXP-144, rev 27009); `EXP143-PUB` DONE rev 27014,
  `@publication` released.
  **EXP-143** (`evidence/s04-validator-arms/`, 173 probes, 0
  failures, stable ×3): `00322C50` executed for all 32 class
  arms; inclusive-signed `[LOW,HIGH]` tail at `0032302E`
  confirmed per arm via live `edx`/`ecx` registers; cls19
  `[0xE000,0xEFFE]` (executed correction of prose `0xEFFF` —
  nibble-table count 4095 agrees); cls13 sums four descriptors,
  missing one contributes 0 not void; cls30/31 alias cls15 arm,
  cls32 alias cls25; descriptor cells are BSS — unplanted
  all-reject verified on all 26 descriptor arms; cls1 two-level
  dispatch: mapper `00309440` reads `d[rec+0]` (corrects
  `+0x38`), nibble n→subclass n+5, full-32-bit id range-checked
  under the subclass arm, cross-nibble probes land in the
  neighboring arm, F-nibble/−1→mapper −1→reject.
  **EXP-144** (`evidence/s46-generator-routing/`, 9 cases,
  stable ×3): all four generator states planted
  distinguishably; routing executed — LCG inliner `003185D0`
  and call-site `00239210` both advance `022C256C`
  `0x11111111→0x15EAB4E4` identically (I3, both I2 census
  populations); MT consumers `0025ABA0(2)`, `0038DB10`,
  `00389670` advance only `02EB3870` (idx 624→1 + twist);
  PRNG `004005E0` advances only `01EF93E8`; gfxMT
  `0015BCF0`/`0018D740` write only `01F7F600` (I1 proven
  natively); negative control `0025ABA0(1)` touches no
  generator; **I5 resolved — gfx MT state IS fixed at
  `01F7F600`** (seeder `lea`), cursor `q[01F7FFC0]`, count
  `d[01F7FFC8]`.
  Prior: three FABLE S-01 exec requests
  (EXP-142) FINISHED revs 26807–26809 — `001EDDC0` timing
  bootstrap both branches, `00863D30`/`00866D60` MT seeding vs
  external ground truth, `0022A0B0` eleven-malloc battery +
  nine `00369D30` registrations. **10/10 cases, stable ×3.**
  Harness `evidence/s01-boot-exec/check.py` (generic IAT `ff 15`/
  `ff 25` → named-stub dispatch; memcpy/memset emulated, malloc
  bump-allocated, WINMM scripted). Executed findings: timing
  quadruple written only on `ecx!=0`; `ecx==0` runs
  devcaps→beginPeriod and never enters `0033F020`; flag-set
  path calls `timeEndPeriod` AFTER `33F020`; implicit `5489`
  pass fires once; `00866D60` never dereferences `rcx`; the two
  tail-less allocations get NO registration and stay `0xAA`;
  registration writes bookkeeping near the block HEAD only —
  end-of-block tail bytes never written (corrects the earlier
  slot-records reading). Committed `b14925d52` via EXP142-PUB.
  Also that round: `FRONTIER-REQ-ORACLE-SAB-PUBLISH-OMISSION-CAUSE`
  (P1) FINISHED rev 26792 — mechanism proven: `e020a57af`'s
  private-index publish left the repo index stale (its epilogue
  per-path `git add` refresh hit a peer `index.lock`, recorded
  `publish-output.txt:43`, `set -e` abort); my plain-commit
  `0d068c953` built its tree from that stale index → 16 file
  deletions + ASTRA.md/TEAM.json byte-identical reverts.
  Scratch-repo repro exact. Guard recommended: non-fatal
  refresh loop + post-publish index/HEAD consistency check.
  Prior: `ASTRA-TRANSFER-ORACLE-S33-LOOT-POOL`
  (EXP-141) FINISHED rev 26005 — five-op loot-pool isolated run
  sealed: **68/68 functional, 57/57 byte-precise mutants, stable
  ×3**, committed `74e88f699`. Executed findings: init unrolls
  10×0x60 nodes (state+stamp one qword at +4); create scans
  `d[node+4]` stride 0x60, full pool evicts head via op5 then
  tail-reuses; op1 payload `{pos.xyz, 1.0f, rare, tblval}` —
  `TBLZ` is `0x1EED3A8` shipping identity `[0,1,2,3]`; RARE
  classifies `(id&F000)==0x1000` via tier (≤5→early 0, 6→cmove
  r=1, else 2); TIER jtab arms interleaved `[1,2,3,4,6,7,8,9,5]`
  (0x13→7, 0x12→6, 0x1A→5); tick despawns at most one node per
  walk (retire clears next before advance); collect grants 7
  slots skipping 0xFFFF + counter + op3; remove op3 only; FB2A0
  −1 for slot>9, FB2D0 −2 on occupied; `003FA730` proves the
  handle is a truncated object pointer (UQ-137 mechanism);
  ops 4/5 pass an uninitialized stack payload. Harness defects
  corrected on bytes and disclosed in the record: TBLZ constant
  had been `0x1ED13A8` (−0x10000 — misdiagnosed mid-bring-up as
  a Unicorn TCG writeback defect; the identity table made
  `r9==gidx` either way) and the ITD fixture had collided with
  MGR's 0x8000 span (`HEAP+0x62000` → moved `+0x68000`).
  EXP141-PUB queued rev 26006; REQ-AUDITSPEC-LOOT-POOL-REVIEW
  rev 26007; REQ-OPUS-LOOT-POOL-FINDINGS rev 26008.
  Prior: `ASTRA-TRANSFER-ORACLE-S31-LICENCE` (EXP-140) FINISHED
  rev 25888 — nine shipped bodies native (00323EC0/00323BB0/
  00324020/0030A330 + 00322C50 cls-0x14 arm/0020E600/002F8FA0/
  00323890/003241D0), 57/57 functional, 35/35 mutants, stable
  ×3, committed `0d068c953`. Executed findings: absent-row edge
  real (rowsrch idx3 < popcount, signed setl — count4 licenses
  absent Quickening row, count3 denies); I5 precedes I4
  unconditionally; validator cls-0x14 arm reads the action
  descriptor `02EBF138` itself (contract correction); null-ROW
  fault `memr(0x2C,2)@323F52` keeps RAX=0x2000 residue; POPCNT
  3-pass×6-bit persistent dl; BUILDER 32-bit row arithmetic,
  signed loop bounds, match-count return. EXP140-PUB queued rev
  25890; REQ-AUDITSPEC-LICENSE-CHECK-REVIEW rev 25894;
  REQ-OPUS-LICENSE-CHECK-FINDINGS rev 25895. EXP-133 RDEC
  scratch-address CONTRA resolved this round (binary confirms
  `0x22D91B0`; harness always used it — prose-only fix,
  committed + finished rev 25790).
  Prior: `SWE2-ORACLE-NAV-REGION-QUERY-
  EXEC` (EXP-139) FINISHED rev 24129 — `0022D0D0` D0D0,
  F430's region query and the LAST scripted nav boundary,
  executed natively. 466/466 functional, 411/411 mutants,
  stable ×3. Scope corrected mid-claim (packed-sibling trap
  again, filed rev 24111): D0D0's true span is
  `0x22D0D0..0x22D4AA` = 987B/220 insns ending `ret@0x22D4AA`;
  the apparent callees `00230790`/`00381D90`/`003810B0`/
  `0022E7D0` live in packed region-scan siblings
  (`0x22D7E0..`/`0x22DE60`) that D0D0 never calls — decoded
  but parked. Sole callee = `thunkf 00861F14` at `0x22D191`.
  Unicorn `D0D0` intercept deleted — shipped bytes execute;
  only the `sqrtf` thunk boundary stays traced. Model mirrors
  site-exact: rect as two vec4s `{lox,loy,loz,_}/{hix,hiy,
  hiz,_}`; four face gates +x/+z/−x/−z (B beyond face ≥ rad,
  `comiss;jb` unordered=fail); per-face `t=−(num/den)·len` via
  sign mask `0x1CEBDA0`; skip on `t≤eps=1e-4` (`0x1CEBB60`) or
  `best≤t` (both `jbe` unordered-taken); face2 gate-fail path
  `0x22D3E8` skips the `0x22D354` len reload; `ebx<0`→
  `eax=0xFFFFFFFF` no writes; else `out=A+dir·best/len`,
  `out.w=B.w`, two-pass store order; `eax=ebx` selector.
  F430's real args threaded: rect = cell bounds ±0.1f
  (`0xBDCCCCCD`/`0x3DCCCCCD` — replacing dead stub-era
  −0.5/+1.5707), rad = `1.8f`/`0.09f` (image `0x908E1C`/
  `0x908E18`) via the E500 select, `sv=(ctx,bp,b)` home saves.
  114 real bodies total; the ONLY scripted residue is the
  import-dir-proven CRT IAT set — no scripted application
  bodies remain in the nav path. 17 new direct cases (four
  selectors, rad gate, eps edge, arbitration, NaN/len0, dy,
  two-call, −1 no-write); 27 byte-verified mutants; two
  candidate mutations verified equivalent and not declared.
  Record + evidence committed `cbe4b46af`; EXP139-PUB queued
  rev 24130, REQ-AUDITSPEC-NAV-REGION-QUERY-REVIEW rev 24131,
  REQ-OPUS-NAV-REGION-QUERY-FINDINGS rev 24132.
  Follow-ups this round: `OPUS-CONTRA-EXP138-DA730-LANES-ARE-SHIFTED`
  answered CORRECT (claim rev 24239, finish rev 24241) — binary has
  DA730 semi-axes at `cap+0x00/+0x04`, angle at `cap+0x08` negated;
  the executed model was already right, only the record prose was
  shifted — corrected + committed `abd705ebc`.
  `OPUS-REQ-ORACLE-RESIDUAL-BOUNDARY-HAS-NO-PAGE-TO-ADOPT-INTO`
  answered DECIDED (claim rev 24242, finish rev 24250) — the ten
  unowned addresses get their own page
  `06-Movement-And-Navigation/the-unit-shape-distance-primitives.md`
  (shared-geometry precedent per the clamping page), committed
  `df8d8ab73`; OPUS's findings adoption fills it.
  Post-scope audit committed `8d9746321` + filed to OPUS as
  `REQ-OPUS-NAV-SIBLINGS-DEADCODE-FINDINGS` rev 24258: whole-image
  scan proves `0x22D7E0`/`0x22DE60`/`0x230790`/`0x22E7D0`/`0x3810B0`
  have ZERO inbound refs — dead code in this build; `0x381D90`
  stays live via `0x232160`←`0x3D97E0`←`0x32xxxx` chain. The parked
  package is closed — no caller scope exists for the dead set.
  `OPUS-REQ-ORACLE-NAV-ADOPTIONS-HAVE-NO-OWNING-PAGES` answered
  DECIDED (claim rev 24259, finish rev 24260, commit `8e0fbfbcb`):
  EXP-132 splits by domain — six shared-math helpers owned by
  the transform-workbench page, PATHW/BLKCHK owned by the
  nav-mesh page; dated placement notes on both. Rule for the
  unmeasured records: file by what the family computes; a
  coherent family with no home gets its own page — never a
  contract buried in an incidental caller.
  Prior: `SWE2-ORACLE-NAV-RESIDUAL-BOUNDARY-EXEC` (EXP-138)
  FINISHED rev ~24100:
  449/449 functional, 384/384 mutants, stable ×3. The five
  boundaries opened into 21 real bodies (~7KB): EF640 8B,
  EF2B0 20B, E500 40B, F4F0 624B (argmin|t−0.5| edge
  predicate, eax 32-bit), F430 1021B (waypoint walker,
  `call q[ctx+0x28]` executed natively — planted fn = real
  0022D4B0), D4B0 815B (CLST mask-merge scan, class filter
  ebx&7, bit23 one-shot vs full store w44∈{1,2}), E6D0 249B,
  CF50 381B, FA0 263B, sphere/cylinder/box primitives
  708/1168/477B, D2020 154B, BF60/BFA0 54/294B, EB0 365B,
  D5A0 246B, A1D30 23B, DA730 244B, TACF/TSQD 6B thunks →
  acosf/sqrt-f64 imports. 113 real bodies total. Scripted:
  D0D0 0022D0D0 region query + CRT IAT set (new: sqrt f64
  q[0x8C2C60], acosf q[0x8C2C78]). Record + evidence
  committed `c36dcda20` (EXP-132..138 batch — records were
  sealed-but-untracked, OPUS's hold reason). One mutant
  retired equivalent (n15-sx: w44 only ever {0,1,2}).
  Prior: `SWE2-ORACLE-NAV-SUBSYSTEM-LEAF-EXEC`
  (EXP-137) SEALED + routed (449/449 functional cases, 385/385
  byte-precise mutants killed, stable across three processes).
  The seven EXP-136 scripted leaves opened into sixteen real
  bodies, 3,778B (92 real total incl. the EXP-130..136 tree):
  N7C20 `00377C20` 78B (EF2 word → T2AD bitfield: eax=N48F0(),
  r8=`q[0x2ADD100]`, r8==0 or eax>=d[r8+4]→0, else
  `(b[r8+3eax+9]<<8|b[r8+3eax+8])>>15`), N48F0 `003148F0` 27B
  (EF2B0 init ptr → `d[+0x1044]` clamped <0→0), N63FF0
  `00263FF0` 21B (`T3B+sx32(sel)*0x288`), DAE00 `003DAE00` 61B
  (null-safe 3-dword copy src+0x30/34/38→dst+0/4/8), N33050
  `00233050` 144B (staggered-grid cell resolve; NO `q[tab]`
  null guard — `idiv` faults; zero cw/ch `#DE` traps at
  `0x233086`/`0x2330A1` with the cvtt dividend in rax), N30A40
  `00230A40` 279B (CLST mask-mux: ecx=(m1&m0|F&~m0)&~n0|(n1&n0),
  ecx&7→0, sel{0,1,2,3,5}→bits 0x17/0x19/0x1A/0x1B/0x18 ^1,
  else 1), N31890 `00231890` 97B + N31820 `00231820` 105B
  (edge y-projection; idx<0 or f[rec+4]<=0.001f → f[vec+4];
  xmm0 vs store variants), N31900 `00231900` 393B (best-edge
  scan → ax), N33110 `00233110` 299B (cell edge scan →
  `w[out+0x52]`), N315E0 `002315E0` 176B (ctx{fn `0x22D4B0`}
  →F430→`sx16 w[ctx+0x44]`), N31400 `00231400` 474B
  (is-point-free dispatcher →N2F830; cookie residual carried
  in rax through every fault), N2F830 `0022F830` 120B
  (flag-bit cell dispatch, `call q[ctx]` executes natively),
  N2F8B0 `0022F8B0` 270B (sub-record point-test loop →EB0),
  N4E10 `00314E10` 154B (material blend selector →xmm0),
  N14F50 `00314F50` 1080B (mode0 `f[outp]=t` ret 2/3/4;
  mode≠0 DAE00×2+D5A0 capsule, hit → +0xEC counters +
  push-apart writeback, ret 1). Five disclosed scripted
  boundaries remain: EF2B0 `002EF2B0` (planted rax), F4F0
  `002324F0` (planted eax, sign-tested), F430 `0022F430`
  (planted `w[ctx+0x44]`), EB0 `00381EB0` (planted eax),
  D5A0 `003DA5A0` (planted xmm0+16B) + CRT IAT cells.
  KEY FINDINGS: packed siblings inflated first-pass spans
  (N31900 1344B→393B, N14F50 1184B→1080B); `rax` at exit is
  load-bearing across every fault/exit path; N14F50's mode is
  a path select not a flag; one N31890 `movsx→movzx` mutant
  retired EQUIVALENT (preceding `test r8w;js` exits on every
  bit15 index — not counted); `T2ADA` heap plant overlapped
  `EF2P`'s 0x1080B object (moved `HEAP+0x74000`). Finish rev
  24008, EXP137-PUB queued rev 24009,
  REQ-AUDITSPEC-NAV-SUBSYSTEM-LEAF-REVIEW rev 24010,
  REQ-OPUS-NAV-SUBSYSTEM-LEAF-FINDINGS rev 24011.
  Prior: `SWE2-ORACLE-NAV-OBJ-ACCESSOR-EXEC`
  (EXP-136) SEALED + routed (339/339 functional cases, 263/263
  byte-precise mutants, stable across three processes). The whole
  EXP-135 scripted leaf set is now real — 16 bodies, 1012B (76
  real total incl. the EXP-130..135 tree): OBJD `00263E30` 5B
  (`rax=q[h+0x30]` unguarded), A6A0 `002646A0` 31B (null-safe
  `q[obj+0xC0]`→`q[+0x138]` chain), O3FW `002646C0` 141B
  (variant `(b[+3]>>5)-1`: v1 copy `d[qB8+0/4/8]`, v3 copy +
  `b[qB8+0x107]&1`→addss `f40/44/48`, else zero outs, null obj
  no writes), O2FW `00265090` 27B (`(b[+3]&0xE0)==0x60` →
  DA710 `003DA710` 21B two-dword write on `qB8+0x50`), O1F
  `00265200` 55B (v1 `f[qB8+0x38]`/v3 `f[qB8+0xA8]`/else 0),
  O1F2 `00263940` 55B (v1 `f[qB8+0x68]`/v3 `fC0*f24`/else 0,
  no null guard), O1F3 `00265830` 34B (`0x60`→
  `f[q[qB8+0xF0]+0x24]` no null guard), OVF `002E9FE0` 73B
  (`0x60`→c0/d164/b10/b11 flag walk), OPA `00314EB0` 118B
  (c0→138 chains, `b[+6]` class equality required, `b[a+0x119]
  ==0`→accept, `==b[+0x119]`→reject), OPB `00313F80` 115B
  (A6A0 pair → scripted N14F50 → optional `f[outp]`), OF60
  `00313F60` 5B (`jmp N7C20`), OSUB `0026E350` 109B (roots
  `q[0x209A670/8]`→N31900 word query `ax<0`→−1→N31820),
  MABESP `003588B0` 143B (bank `h>>0x14&0x7FF` / sel
  `h>>0x10&0xF<5` / gen `h&0xFFFF` decode → N63FF0 table →
  arr entry + `w[e+0x16]==bank`; NO table-null guard — faults
  at `0x3588EB` by design), DE100 `0026E100` 35B (reshuffle
  `rcx→rdx`, `zx16(rdx)→r8`, `r8→r9`, root→rcx → tail
  N31400), AGENTQ `00318CA0` 44B (`q[0x2EC1378]`→N315E0→
  `cwde`). Seven scripted boundaries remain disclosed: N7C20
  `00377C20`, N14F50 `00314F50`, N63FF0 `00263FF0`, N31900
  `00231900`, N31820 `00231820`, N31400 `00231400`, N315E0
  `002315E0` + CRT IAT cells. KEY FINDINGS: float-returning
  leaves (O1F/O1F2/O1F3) return in `xmm0` — `rets` only tracks
  `rax`, so their mutants need consumer-path kills (S3W
  `out+0x18` store, GATE accept-path y-cap, `flags&0x10` O1F3
  arm, `opa-b67` cross-byte discriminator); `pv-*` rec coords
  must match the query segment (`crec=(1,0,2)` on P1→V60, not
  SEGTMP); DE100's third arg lands in `r9` not `r8`. Finish
  rev 23896, EXP136-PUB queued rev 23897,
  REQ-AUDITSPEC-NAV-OBJ-ACCESSOR-REVIEW rev 23898,
  REQ-OPUS-NAV-OBJ-ACCESSOR-FINDINGS rev 23899. OPUS publish
  handoff ANSWERED YES revs 23900-23901 — OPUS may commit the
  four sealed records verbatim under
  PUBLISH_ALLOW_FOREIGN_HEADERS=1 naming me author, and may
  fold EXP-136 in as a fifth; if it does, EXP132..136-PUB all
  close.
  Prior: `SWE2-ORACLE-NAV-GATE-WALK-EXEC`
  (EXP-135) SEALED + routed (275/275 functional cases, 201/201
  byte-precise mutants, stable across three processes). GATE
  `003357B0` 943B/232i executes real end-to-end — the scripted
  boundary inside EXP-134's PVAL is gone — over 17 new real
  bodies (60 total incl. the whole EXP-130..134 tree): GTAB
  `00236820` pool lookup `d[idx*0xF50+8]` (`idx=b[ctx+0xEA9]`),
  MABE `0031ABE0` (`b[0x2089340]&0x10`→MABESP else 0), GCHK
  `002EA7F0` guard chain (`+0x18`/`+0xC0`/`+0x14F`/`+0x138`/
  `f+0xF0`/`b+8&8`→OVF or `b+4==3`), OCLS `00263C20`
  (`b[+0xE]&0xF`), LHELP `00335760` (OCLS class `{3→0,1|2→1,
  else 2}`), S3W `002FB500`/S2W `002FB340` record writers
  (both `d[out+4]=0` after O3FW; S2W `maxss`→`out+0x10`),
  CDST `00469060`/CDZ0 `00468D10`/CF90 `00468F90` capsule
  predicates, GPC `00391A30`/GSC `00391D90` cell collectors
  (shared LQUERY BSS grid block; flag≠0→S3W+CDST/CF90 else
  S2W+CDZ0), GPT `00391D10`/GSEG `003920F0` wrappers +
  GFILT `003911D0` (collector flags `r9f=(~(flags>>4)&8)|0x14`;
  per-handle `flags&2&&obj==0` skip, `flags&4`→`q[+0x698]==0`
  skip + `p+0x64|p+0x3C` hi-bits→OF60, `flags&8`→GCHK),
  OTHUNK `0032A790` (`jmp 0026E350`). GATE frame `rbp=rsp
  −0x148`: point-vs-segment on ordered `ucomiss` x/y/z →
  GPT or GSEG (`n<=0`→0); candidate walk: self/excl skip,
  e68 class-pair `(b[e68+0x18]>>1)&7` (obj1 vs ctx4), mode-3
  `flags&0x40` pre-filter (`ctx+0x1F4!=3 && obj+0x1F4==3` →
  O3FW+`V30={x,1,1,z}`+dead OSUB+O1F2 compare), flag arms
  2/4/0x10/8 via LHELP (0x10 arm FALLS THROUGH on LHELP≠0),
  accept OPA+OPB `(r-1)<=2`→esi++ else r12d++;
  `ret r12d?1:(esi?2:0)`. Scripted boundaries disclosed: 14
  subsystem-leaf entry-intercepts OBJD `00263E30`, O3FW
  `002646C0`, O2FW `00265090`, O1F `00265200`, O1F2
  `00263940`, O1F3 `00265830`, OPA `00314EB0`, OPB
  `00313F80`, OF60 `00313F60`, OVF `002E9FE0`, OSUB
  `0026E350` (via real thunk `0032A790`), MABESP `003588B0`,
  DE100 `0026E100`, AGENTQ `00318CA0` + CRT IAT trampolines.
  KEY FINDINGS: planted record plants must not overlap —
  `ob()` zero-fill at +0x100 spacing wiped the neighbour's
  GCHK fields (GCHK failed before OVF, no trace, GATE
  returned 0 invisibly; now explicit sizes + 0x800 spacing);
  `ob()` field writes past its size silently APPEND —
  `bEA9` at +0xEA9 on a default 0x800 object needed
  `ob(0x1000)` (mutant read 0 and was invisible); S2W/S3W
  zero `d[out+4]` after O3FW (record is `{x,0,z,0,…}`); the
  `flags&0x10` continue is inside the `LHELP==0` arm only;
  GFILT `flags&4` skips null `q[obj+0x698]`; gate-arg
  mutants need populated walks — `pv-flag6-pop`/`pv-flag6-m3`
  discriminators added. Finish rev 23823, EXP135-PUB queued
  rev 23824, REQ-AUDITSPEC-NAV-GATE-WALK-REVIEW rev 23825,
  REQ-OPUS-NAV-GATE-WALK-FINDINGS rev 23826 (`@publication`
  held by FABLE; queues fourth).
  Prior: `SWE2-ORACLE-NAV-PATH-VALIDATOR-EXEC`
  (EXP-134) SEALED + routed (205/205 functional cases, 201/201
  byte-precise mutants, stable across three processes). The
  `00335B60` path-validator consumer over the whole real
  EXP-130/131/132/133 tree — 43 real bodies: PVAL `00335B60`
  768B/178i (agent, angA, angB, tol, cap@rsp+0x28, flags@rsp+0x30;
  `ucomiss tol,0` ordered-equal → 0; cap clamp `[0.2f,0.8f]` cells
  `0x8F30F8`/`0x8F3108`; `tol/=cosf(angB)` iff angB NaN-or-nonzero;
  `dir = ROTCOL(awrap(angA))·ROTX(−angB)·{0,0,1,1}` — MLOAD picks
  `{+X,+Y,+Z,W}` from the signed axis bank `0x8C5F80..0x8C5FE0`,
  `xorps` sign-flips via `d[0x1CEBDA0]`, const vec `0x1F004C0`;
  `sub=q[agent+0x108]`, `rad110=d[sub+0x110]`, `mode=b[sub+0x174]`;
  GATE(agent,&v60,agent,q[+0xF0],stk:q[+0xE0],
  `((flags&4|0x10)<<2)|(flags&2)`) — scripted, `==1`→1; mode-3
  AGENTQ scripted; `flags&8`→QWALK else PRED(radius·0.9f via
  `0x8FCC8C`); `!=0`→1; LQUERY(agent,&v60,clamp·rad110);
  DE6A0(&v50,mode,mode==3)→DE100 scripted, `0`→1; else
  `ret gate==2?2:0` `cmove`), MCPY `00202E90` 100B/27i (4×`movups`
  row copy in place, each faults as two 8B accesses; real cosf/sinf
  IAT thunks; tail-jmp ROTX), ROTX `00217790` 236B/58i (all four
  16B columns `y'=y·c−z·s`, `z'=y·s+z·c`), DE6A0 `0032A6A0` 5B/1i
  (`jmp 0026E100`, dispatcher sees caller registers); whole
  EXP-130/131/132/133 trees re-executed. Scripted boundaries
  disclosed: GATE `003357B0` entry-intercept (deferred EXP-135 —
  ~944B subsystem/object-pool walk), DE100 `0026E100`, AGENTQ
  `00318CA0`, inherited CRT IAT cells. KEY FINDINGS: gate stack
  args are callee-relative `rsp+0x28/+0x30` (handler initially read
  caller shadow `+8/+0x10`); `movups` faults as two 8B accesses
  under emulation; SSE both-NaN propagation is dest-operand-first
  (`7FC00000` scalar over `FFC00000` vector — `_n2` flipped,
  EXP-133 mutants still kill); shared model lacked `sq` (norm
  zero-path latent until radius=0 PRED cases); `jp`/`jnp` mutants
  at `0x335B9E`/`0x335BD8` unobservable (converging successors) —
  `jp→jmp` kills; call-retarget mutants must land past the copied
  prefix (`+0x20` row-3-only diverges, `+8` invisible under the
  second MLOAD). Finish rev 23719, EXP134-PUB queued rev 23720,
  REQ-AUDITSPEC-NAV-PATH-VALIDATOR-REVIEW rev 23721,
  REQ-OPUS-NAV-PATH-VALIDATOR-FINDINGS rev 23722
  (`@publication` held by FABLE).
  Prior: `SWE2-ORACLE-NAV-LOS-EXEC`
  (EXP-133) SEALED + routed (165/165 functional cases, 132/132
  byte-precise mutants, stable across three processes). The nav
  LOS/raycast query tree below consumer `00335B60` — 39 real
  bodies: LQUERY `00391410` 758B/156i segment LOS over the
  wall-record grid (reads `p1.z`,`p2.z`,`p2.x`,`p1.x`;
  cvtt-clamped cell bounds `(z1+rad−epsz)/csz` style over
  `d[0x2AEE060..0x2AEE0B8]` BSS params; BMASK → dead DIST →
  160-iter record loop: `ebx` bit counter wraps at 8, `r14`
  mask byte index starts at **0x10** (16-byte mask header),
  `rsi` record index, `rdi=i*0x20` bound `0x1400`,
  `r15d=i−0x20` → `i<0x20`: `BASE(d[root+0x28])+i*0x20` type
  `w[0]` → 0:CAPT0 / 1:CAPT1 / else skip; `i≥0x20`:
  `RDEC(i−0x20,out)` + CAPT1 w/ `{out.x,0,out.z,1,out+C,
  out+10,out+14}`; first hit→1 else 0; shl-src `mov eax,1`
  is the pre-fault rax so `d[root+0x28]` fault returns 1),
  BMASK `003912E0` 286B/83i (memset rlen; clamp `<0`→0 via
  `test/jns`, `>m−1`→`m−1` via `cmovg`; col guard
  `c0>c1 → jg skip`; `idx=row*w+col`; flag≠0 → OR `rlen`
  bytes `lsrc+idx*rlen` → `dst+k`), DIST `003A1920` 53B/12i
  (`(dy²+dx²)+dz²`, sqrtf tail-jmp), CAPT0 `00468D50` 250B/67i
  (`ucomiss` `jp`+`jne`: p1==p2 BOTH coords → point path else
  CPSEG; `closest==p1`→0; `(e−c)²` vs `srad+erad` → `seta`),
  CAPT1 `00468E50` 305B/79i (CPSEG first; point-seg skips the
  `==p1` exclusion; `TRIGD(edge,closest)+srad` vs dist →
  `seta`), CPSEG `004691A0` 315B/68i (`rcx=out rdx=a r8=b
  r9=p`; `t=dot(a−p,a−b)/|a−b|²`; `t<0`/`t>1` ordered → 16B
  endpoint; unordered-NaN → lerp; single `movaps` store
  fault = one 8B `memw`; `rax=out`), TRIGD `00468580`
  325B/69i (`frac=an/NEG2PI`; `i1=(0x2000−cvtt(frac·TRIGN))
  &0x7FFF`, `i2=cvtt(frac·TRIGP)&0x7FFF` → shipped sine
  table `0x1F004E0`; `x8=(t2·dz+t1·dx)/e10`,
  `x7=(t1·dz−t2·dx)/e14`; `d≤eps` OR unordered → `e10`;
  else `sqrtf((x8·e10/d)²+(x7·e14/d)²)`), CAPV `00469410`
  336B/74i (sqrt-free sibling: `lim2=(rad+p+0x10)²`; `t>1`
  ordered-only → `c=b`, NaN t → lerp; `(c−p)²` vs `lim2` →
  `seta`; read order b.z,p+0x10,b.x,a.y,b.y,p.y,a.x,a.z,
  p.x,p.z), RDEC `0032A6E0` 153B/36i (`rax=q[0x209A670]`
  survives to early faults = the residual; `rec=q[nro+0x1A0]
  +sx32(idx)·16`, `vtx=q[nro+0x188]+sx16(w[rec+2])·64`;
  `movsx eax` ×3 → stack lanes + STALE 4th `rsp+0x2C`;
  `cvtdq2ps`·`mulps [0x908E30]` 1/4096 → `movdqu`
  `0x22D91B0` (was mis-written `0x23151B0`; corrected via
  OPUS-CONTRA — harness always used `RSCRATCH=0x22D91B0`);
  `out={vtx30,vtx34,vtx38,sv0,sv1,
  atan2f(vtx28,vtx20)}`), TMS `00861EC0`/TAT2 `00861F02`
  real IAT thunks; whole EXP-130/131/132 trees re-executed.
  Scripted boundaries disclosed: memset via real thunk +
  IAT `q[0x8C2A60]` (VCRUNTIME140, import-dir proven) →
  MSET `0x630A0000`; atan2f via real thunk + IAT
  `q[0x8C2BD0]` → AT2 `0x630B0000`; inherited sqrtf/cosf/
  sinf/_fdclass/_isnan/_finite cells. KEY FINDINGS:
  `f32_round` dropped the sign (`f32div(−4,16)`→+0.25 —
  silently broke every negative projection); SSE NaN
  propagation is operand-payload-exact (`FFC00000`
  real-indefinite vs quieted payloads; EXP-134 later proved
  both-NaN precedence dest-operand-first — all float arith
  now via `_m/_a/_s/_d` helpers; sqrtf
  trace bits differ identically); the record bitmask has a
  16-byte header (fixtures at `lsrc+0` produced trivial
  all-zero parity masking all eight loop mutants);
  BMASK's `jg` col guard swallows clamp mutants (kill case
  needs a flag at the clamped col `w−1`); CAPV `t>1` is
  ordered-only. Finish rev 23644,
  REQ-AUDITSPEC-NAV-LOS-REVIEW rev 23645, EXP133-PUB queued
  rev 23646, REQ-OPUS-NAV-LOS-FINDINGS rev 23647
  (`@publication` held by FABLE).
  Prior: `SWE2-ORACLE-NAV-CONSUMER-EXEC`
  (EXP-132) SEALED + routed, EXP132-PUB queued (98/98
  functional cases, 99/99 byte-precise mutants, stable
  across three processes). The nav consumer layer over the
  real EXP-130/131 trees, closing EXP-130's last scripted
  seam — 28 real bodies: PATHW `0033A3D0` 405B/88i
  path-width probe (`QWALK(B→A)!=1`→ret 1, else two ±π/4
  rounds of VSUB+VSCALE 0.5f `d[0x1CEBB70]` + MLOAD + AWRAP
  + RBUILD+ROTCOL + MXVW/MXV + VADD → `w=B+R(A−B)·0.5`;
  round passes iff `Q(B→w)==1` or `Q(w→A)==1`; probe2-fail
  → `0x33A40B` dead tail `add [rax],al`×2 → fault;
  both-pass → ret 0), BLKCHK `00335F90` 161B/42i
  corridor-blocked check (`sub=q[+0x108]`, `scale=
  d[sub+0x10C]·d[0x8FCC8C]=0.9f`, `mode=b[sub+0x174]`;
  `PRED!=0`→1, `QWALK==1`→1, `mode==3`→`AGENTQ!=0`→1, else
  0 — real PRED over real QWALK inside), AWRAP `0033CB70`
  128B/32i (±4π gates `d[0xD10B0C]`/`d[0xD10B20]` →
  cvttss2si mod path w/ `rax`=trunc residual, else ±2π
  loops vs ±π gates), MLOAD `00203170` 44B (selects
  `{+X,+Y,+Z,W}` from the shared signed axis-basis bank
  `0x8C5F80..0x8C5FE0`, skipping `−Y`/`−Z` — OPUS-confirmed
  reading; identity), RBUILD `00202F00`
  100B (cosf/sinf via real IAT thunks + tail-jmp ROTCOL),
  ROTCOL `00217880` 234B (`x'=z·sin+x·cos`, `z'=z·cos−
  x·sin`), MXV `00217060` 235B (`w·m[o+0x30]+((y·m[o+0x10]+
  x·m[o])+z·m[o+0x20])`, vec reads x,z,w,y, `rax=dst` after
  first read), MXVW `00202B70` 31B, CTHUNK/STHUNK
  `00861F08/0E`; whole EXP-130/131 trees re-executed.
  Scripted boundaries disclosed: cosf/sinf via real thunks
  + IAT `q[0x8C2BA8]`/`q[0x8C2BB0]` (import-dir proven),
  `_fdclass`/`sqrtf`/`_isnan`/`_finite` (EXP-130/131),
  AGENTQ `00318CA0` entry-intercept planted eax.
  KEY FINDINGS: BKSC mis-add trilogy (`0x91CC89`→`0x91CC8C`→
  `0x8FCC8C`, 4th rip+disp occurrence); PATHW probes are
  `Q(B→w)`/`Q(w→A)` asymmetric flag=1; PATHW calls VADD
  `0x202B10` for `+B`, not MXV; AWRAP result is xmm0-only
  (killable sites = gate disps/loop-backs/cvtt/divss only);
  World must not share mutable case lists with Model (agrets
  pop bug); MLOAD skips `0x8C5FA0`. Finish rev 23542,
  REQ-AUDITSPEC-NAV-CONSUMER-REVIEW rev 23543,
  REQ-OPUS-NAV-CONSUMER-FINDINGS rev 23545, EXP132-PUB queued
  rev 23544 (`@publication` held by FABLE).
  Prior: `SWE2-ORACLE-NAVGRID-QUERY-EXEC`
  (EXP-131) SEALED + routed + PUBLISHED `90ce11f15` (54/54
  functional cases, 61/61 byte-precise mutants, stable across
  three processes). The nav-grid query tree EXP-130 scripted —
  12 real bodies: QWALK `0033D3E0` 631B/145i adjacency-walk
  segment probe (`grid(p1)==0xFF`→0, `grid(p2)==0xFF`→1,
  `cur==dst`→0, slots over `deg=w[root+0xA]`,
  `m[cur*deg+slot]` w entries = 1-BASED edge-rec idx, rec
  `{w va,w vb,b class@+5,b flag@+6}` at `BASE(id*8)`,
  `eclass`: 1→proceed / 0→flag gate `b[ep+6]&(1<<flag)` /
  else skip, SEGT cross→advance, exhaust→1, budget `0x80`→0),
  WWRAP `00384130` 40B/9i, GGRID `00383F10` 542B/141i
  (`_fdclass` NaN→0xFF ×2, `comiss` bounds, `cvttss2si` +
  signed `idiv` truncating, cell-map → `0xFF`-term byte list,
  rec stride `0x22` selector `+0x14`, TTEST per candidate),
  ROOTL `00383840` 8B (`rax=q[0x2AEDFB0]`), TTEST `00382D10`
  391B/93i (shipped idx `d[0xD112B0]={0,1,2,0}`, 2nd-idx-first
  ordered reads, `ucomiss` sign-accumulate), ETHUNK `0032A780`
  5B → ECLASS `0026E300` 73B/22i (asymmetric sign-ext: `dx` for
  classtab `0x915760`, `ecx` for bptab `0x209A3E0`; negative
  TABLE ENTRY `classtab[4]=-1`→`0xFFFFFFFF`; bit-pair→0/1/2),
  SEGT `00468880` 496B/108i (VSUB×6 + XPROD×4 orientation
  compares), BASE `0020E600` 10B (`rax=ecx+q[0x1F83530]`),
  VSUB/XPROD/CHKCK re-executed. Scripted boundary disclosed:
  `_fdclass` via real IAT `q[0x8C2C10]` (import-dir proven) →
  FDC `0x63070000` host float-class (NaN 2, ±inf 1, finite −1,
  denormal −2, zero 0). Planted BSS disclosed: root
  `q[0x2AEDFB0]`, BASE `q[0x1F83530]`, bptab `d[0x209A3E0]`.
  KEY FINDINGS: preliminary BSS cells wrong again (`0x5ADFB0`→
  `0x2AEDFB0`, `0x1FED530`→`0x1F83530` — rip+disp class, 3rd
  occurrence); bptab is BSS not rdata; edge ids 1-based;
  `idiv` truncates (Python `//` floors); `cvttss2si` invalid→
  `0x80000000`; `_fdclass` sees the `movss` float not a double;
  slot reg `ebx` cycles dst/edgeid/vb so naive reg-swap mutants
  are dead (landed mutant flips prev-skip→cur-skip, diverges
  via watched mem). Finish rev 23398,
  REQ-AUDITSPEC-NAVGRID-QUERY-REVIEW rev 23399,
  REQ-OPUS-NAVGRID-QUERY-FINDINGS rev 23400, EXP131-PUB
  `90ce11f15` rev 23403.
  Prior: `SWE2-ORACLE-TRANSFORM-PREDICATE-EXEC`
  (EXP-130) SEALED + routed + PUBLISHED `86c87ed11`
  (35/35 functional cases, 36/36
  byte-precise mutants, stable across three processes). The
  transform-workbench predicate family — 10 real bodies: PRED
  `00335E50` 305B/76i corridor-width probe (`tmp = p1−p2` VSUB,
  `tmp.y` flattened `movss [rsp+0x24],0` — XZ only, NCOPY
  normalize-or-zero + `w=0`, `tmp = tmp × (0,1,0)` XPROD const
  `f[0x1F004B0]`, `tmp *= xmm2` VSCALE, three nav probes
  `Q(p1+off,p2+off)` / `Q(p1−off,p2−off)` / `Q(p2+off,p2−off)`;
  any `==1` → ret 1 else `sete (t3==1)` — only exactly 1 counts),
  VSUB `00203080` / VADD `00202B10` 81B/17i each (4-component
  add/sub via stack temps, `dst==src` alias-safe, read order
  `a0,b0,a4,b4,a8,b8,aC,bC`), VSCALE `00202FE0` 67B/16i,
  NCOPY `00202DE0` 33B/10i (`movups` + NORM + `w=0`), NORM
  `00216660` 186B/49i normalize-or-zero in place
  (`len2=(x2+y2)+z2` → `cvtps2pd` → `_isnan` nonzero → zero,
  `_finite` zero → zero, `comiss len2,d[0x907698]=FLT_MIN` `jbe`
  → zero, else `v *= 1/len` on xyz only — `w` untouched on the
  scale path; zero path `0x216701` zeroes all 16B; exit rax =
  `_finite` residual `1` on scale, `0` on zero), XPROD
  `00202E10` 115B/26i re-executed, THUNKF `00861F14` 6B,
  CHKCK `00808C40` 33B/8i, RGSF `00809654` partial under the
  cookie mutant. Scripted boundaries disclosed: `sqrtf` via real
  thunk + IAT `q[0x8C2BB8]` → SQF `0x63040000`; `_isnan` /
  `_finite` via real IAT cells `q[0x8C2C68]`/`q[0x8C2C70]`
  (import-dir PROVEN — unbound hints `0x1CCECD8`/`0x1CCECCE`)
  → ISN `0x63050000` / FIN `0x63060000`; Q33 `0033D3E0` nav-grid
  point query entry-intercepted, planted `eax` per case,
  vec-content arg tokens (deep tree: `00384130` → `00383F10`
  grid lookup w/ `_fdclass` IAT `0x8C2C10`, `00383840` root
  `q[0x5ADFB0]`, `0x382D10`/`0x32A780` BASE-decoded walkers —
  follow-on package). KEY FINDINGS: preliminary predicate cells
  were wrong AGAIN (`0x86AC6x` → real IAT `0x8C2C6x`, same
  mis-add class as EXP-129); `tmp.y` flattened pre-normalize
  (pure-Y delta → offset 0); third probe is a `p2` self-
  difference; NORM zeroes on NaN/inf/denormal/zero len²;
  `w` survives the scale path, dies on the zero path, always
  cleared by NCOPY; the `_finite` residual leaks `rax=1` to
  callers (`m-pred-r8d` proves it live); `len²==FLT_MIN` takes
  the zero path. Finish rev 23299,
  REQ-AUDITSPEC-TRANSFORM-PREDICATE-REVIEW rev 23301,
  REQ-OPUS-TRANSFORM-PREDICATE-FINDINGS rev 23302, EXP130-PUB
  `86c87ed11` rev 23350.
  Prior: `SWE2-ORACLE-VEC3-NORMALIZE-EXEC`
  (EXP-129) SEALED + routed + PUBLISHED `b383c02d6`
  (15/15 cases, 34/34 mutants, stable x3). First f32/SSE
  package — 6 real bodies: DB70 `0040DB70` 49B/9i (flag clear
  `b[0x2CA4390]` + seed-vec wrapper), B430 `0040B430` 416B/82i
  two-stage normalize/publish (stage1 `comiss jbe` `eps<=len`?
  `1/len`:`0` → dir `f[0x2CA43A0]`; stage2 XPROD
  `local={0,1.0f,d[0xD108A0]≈1e-5f,w}` × dir → `comiss ja` →
  `f[0x2CA43B0]`; exit rax `GSCOOK ^ (rsp-0x98/0xD8)`), XPROD
  `00202E10` 115B/26i (`d × a`, stack temps, alias-safe),
  THUNKF/CHKCK/RGSF-partial. Scripted: `sqrtf` IAT → SQF.
  Findings: all five preliminary constants wrong
  (`0x22CA39x`→`0x2CA43xx`, `16842.25f`→`~1e-5f` `d[0xD108A0]`,
  `d × a` not `r8 × rdx`); `w` dead end to end; `len==eps`
  divides, `len²=inf`→zeros, NaN propagates both stages.
  Finish 23206, REQs 23211/23212, EXP129-PUB `b383c02d6` 23227.
  Prior: `SWE2-ORACLE-EXP109-POLL-PUMP-EXEC`
  (EXP-128) SEALED + routed (137/137 functional cases, 123/123
  byte-precise mutants, stable across three processes). EXP-109's
  last two scripted boundaries executed end to end — 15 real bodies:
  E070 `0032E070` 605B/156i six-arm task pump (`b[+0x20]-1` bounded
  `ja`→teardown, dispatch `jmp rcx` via JTAB `0x32E2D0` — rdata
  embedded in .text, offsets `BD/49/63/63/AB/AB`+image base, read
  `d[rdi+rax*4+0x20e2d0]` with rdi=image base; S1 `3EADD0` gate →
  `d28==0` E330-retire else submit-A `46E030(b21,d24,d2c,d28,
  stack=q38)` / submit-B `2DF6C0` on `b21==0xFF`, success stamps
  `q[+8]=E810()` + state 2; S2 `q[0]+=E810()`, `q[+8]=E810()`,
  state 3; S3/S4 real-FLAG gate (nonzero→teardown), S4 cb48 +
  `d28=0` + retire, S3 state `5+(FLAGG<0)` via `sets`; S5/S6 shared:
  `b22==0`→E330/E370 retire, `b22==1&&b23==2`→E3B0 probe, S6→E370
  +`b23=0`+retire, else progress `d34-=d28`→exhaust E330+`b23=0`+
  retire, else `d2c+=d28`,`q38+=d28`,E3B0 ret1→`d28=min(d30,d34)`
  (cmovl),`q0=0`,state1,`b23=0`,`d2c` rounds DOWN to `0x800` via
  signed cdq/`&0x7ff`/`&0xfffff800`; the S6/exhausted tail clears
  `b23`, S1/S4/`b22==0` tails do not; teardown `46DD50`/`16D6A0`/
  `3E9780`/`16D6A0`/`36FD50` +cond `3BB790`), EA30 `0035EA30` 7B/2i
  `edx=0` thunk, EB70 `0035EB70` 258B/61i pacer (G8C70 vs tick-src
  `862090`: differ→spin `E810()-saved < max(ecx,1)` SIGNED cmovg,
  ret elapsed; equal→resync arm `17D3E0` gate → `3691B0`/`369190`,
  PACC `0x22CA5C4` dword-cluster fold, `35E7A0`, ret prior pacer),
  E330 `0032E330` 59B + E370 `0032E370` 62B retire twins (cb40
  `r8d=1` / `d28==-1`-gated `r8d=0` — gated-out ret = cb POINTER;
  both `b21==0xFF` → `movsxd d24` → `jmp 3697F0` = real PREL free),
  E3B0 `0032E3B0` 58B (null cb50→**ret 1**; out-of-{1,2,3}→real
  `8620C0` yield, `rdx=0x1CCF998` residual), EC40 `0032EC40` 147B
  (`+0x10/+0x18` unlink + cmove head/tail fixups, idle push
  `q[0x22C51D0]`, `d64=-1`, ret OLD IDLE HEAD), E810/G8C70/GE0E0/
  G6A0/G20C0/G97F0 leaves+thunks + re-executed PREL `00369860`
  1009B + FLAG `0046DFE0`. 12 scripted boundaries disclosed:
  `3EADD0`,`46E030`,`2DF6C0`,`46DD50`,`3E9780`,`36FD50`,`3BB790`,
  `862090` (ships LIVE — `q[0x8C21D0]`→`q[0x1CCC358]`→`00826B00`
  real code, unlike the dormant `0x8C2D80` family),`17D3E0`,
  `3691B0`,`369190`,`35E7A0` + 3 planted cb stubs `0x6301/2/30000`.
  KEY FINDINGS: pump exposes residual `rdx`/`r8` at the FLAG leaf
  (model tracks through every arm); `46E030` arg5 reads at
  `rsp+0x28` at callee entry not `+0x20`; E370 gated-out returns
  the cb pointer itself; EC40 returns the old idle head; JTAB is
  `0x32E2D0` NOT `0x22E2D0`; EB70's spin floor is signed. Finish
  rev 23082, REQ-AUDITSPEC-EXP109-POLL-PUMP-REVIEW rev 23084,
  REQ-OPUS-EXP109-POLL-PUMP-FINDINGS rev 23085, EXP128-PUB queued
  rev 23083.
  Prior: `SWE2-ORACLE-ALLOC-FREE-PATH-EXEC`
  (EXP-126) SEALED + routed (82/82 functional cases, 71/71
  byte-precise mutants, stable across three processes). The
  allocator free/release path executed end to end — 33 real
  bodies: PREL `00369860` 1009B/246i free path (gates in order:
  null/misaligned emit-and-return; bad magic `0xFF12` → dual
  hex dump — `0xB0` header + `0xD0` aux, one emit call per byte,
  sep word `w[0x8F3F58]`=`0x000A` every 16th, `\nSTACK\n` qword
  tail — then emit(`F_ILL`)+`d[0x22D89BC]=kind`+A570(kind,0xB,-1)
  +hook+int3; `w[+0x3E]!=0` → MCB abort same tail; `!(f14&1)` →
  emit(`F_FREE`)+RETURN — freeing a free block is a diagnostic
  return not a crash; `kind>=0xF` real fault `d[0x2]`; the free
  itself `b[desc+2]=1`, clear alloc bit, `b[+2]=0xFF`,
  `d[desc+0x68+tag*4]-=key`, `d[PTAGC+b[+0x17]*4]-=key` when set,
  clears `b[+0x34]`/`w[+0x1E]`/`b[+0x17]`/`d[+0x30]=C620(0)`/
  `d[+0x3E]=0`; splice-in phys-neighbour FIRST — free
  `BASE(d[+0xC])`→B670 else free `BASE(d[+0x10])`→B730 else
  bound-split (`rbx < q[desc+0x18]`→AE00-first/ACE0-fallback,
  `>=`→ACE0-first/AE00-fallback) each stale-link-guarded vs
  `BASE(d[+4])`/`BASE(d[+8])`, then B210 coalesce + B5F0
  page-head insert), AE00 `0036AE00` 287B/94i +
  ACE0 `0036ACE0` 286B/90i find-free-at-or-below/above pair
  (page bitmap + `q[desc+0x28]` head table + `+8` chain),
  EMIT `0017D2E0` 91B/27i emit wrapper (`hook(obj|1, buf, -1,
  fmt)` via dormant cell `q[0x8C2F08]` ships rdata `0x1CCECB4`),
  GETOBJ `0016D670` 8B leaf, _chkstk `00808F10` 95B/25i real
  against a fake TEB (`UC_X86_REG_GS_BASE`), PINIT `004746F0`
  26B/9i memcpy wrapper (`movsxd r8,r8d`; real IAT thunk
  `00861EBA` 6B; ret dst) — the sole scripted boundary is
  `VCRUNTIME140!memcpy`'s import body, reached through real
  thunk+IAT cell `q[0x8C2A68]` planted to a fixture trampoline
  `0x63000000` so the copy is observable. The whole EXP-123/125
  tree re-executed — A2A0 now calls REAL PREL(`rbp+0x40`,0) +
  PINIT(`rbx+0x40`,`rbp+0x40`,key). **ERRATUM corrected**:
  `q[0x8C2D80]` ships rdata ptr `0x1CCF02C` NOT 0 — EXP-123
  record+bodies.json amended; all three hook cells
  (`0x8C2D80`/`0x8C2F08`/`0x8C2F70`) are one dormant rdata
  family planted to real FLAG. KEY FINDINGS: planted FLAG
  writes NO dump text — the buffer accumulates only `0x0A`
  separators + the STACK tail; nested PREL frames are
  rsp-derived (model carries caller `vsp`: A2A0 `vsp-0x1230`,
  AAD0 `vsp-0x48`, ABE0 `vsp-0x28`, A850 fault cookie
  `vsp-0x268`); aux-fault residual rax = the movsd destination
  (`buf+0xB`); bad-magic end-find is O(n²) — native needs
  ~50K insns, emu count raised to 300000. Finish rev 22980,
  REQ-AUDITSPEC-ALLOC-FREE-PATH-REVIEW rev 22981,
  REQ-OPUS-ALLOC-FREE-PATH-FINDINGS rev 22982, EXP126-PUB
  queued rev 22983.
  Prior: `SWE2-ORACLE-ALLOC-POOL-ADOPTION-EXEC`
  (EXP-125 — RENUMBERED from EXP-124 per
  `ASTRA-NOTICE-ORACLE-EXP124-IDENTITY`; ASTRA's
  `EXP-124-phyre-startup-globals.md` predates my claim and keeps
  the number. Record: `EXP-125-pool-adoption-exec.md`; board rows
  named `EXP124-PUB`/old `exp-124-` resource paths refer to THIS
  package — they could not be edited after the fact).
  SEALED + routed (43/43 functional cases, 34/34
  byte-precise mutants, stable across three processes). The
  pool-adoption (compaction) layer executed end to end — 25 real
  bodies: AAD0 `0036AAD0` 261B/83i BST-scan adoption vs free head
  (`desc+0x50` root, `+0x24` smaller/`+0x28` larger children,
  `+0x2C` parent, BASE-encoded; adopt on `key==d[head+0x18]`,
  `addr>head`, `!(f15&4)`; `edx!=0` rescans and can legally fault
  on the empty re-read at `0x36AB16`), ABE0 `0036ABE0` 243B/73i
  per-free-node walk — the `(f15&6)==2 && alloc` arm adopts the
  PHYS-NEXT block itself (`jne 0x36AC8F` skips the `mov r8,rbx`
  reload; flag-set-but-free returns 0 immediately, no fall-through),
  A2A0 `0036A2A0` 495B/138i adopt-one (trailer+label snapshot,
  C790 BST unlink, `+0x20`/`+8` chain splice, `d[0x22D8E10+tag*4]+=`
  key, scripted PREL `00369860`/PINIT `004746F0`, REAL BC60
  ctx-carve `ecx=b[desc+1], edx=src key, r8=rbx, r9d=0`, copy-back,
  BST re-insert, `w[rbx+0x3E]` clear; returns `w[rbx+0x1C]` seq on
  the re-splice arm else 0), C790 `0036C790` 359B/100i BST unlink +
  subtree re-attach (the `+0x28` force-attach arm is separate body
  B5A0 `0036B5A0` 71B/21i, NOT B490 `0036B490` 71B/21i which is
  `+0x24`; B410 `0036B410` 124B/37i insert, B4E0 `0036B4E0`
  177B/52i keyed descend-and-insert), A570 `0036A570` 729B/189i
  three-structure diagnostic (mask gate, `kind<=0xE`, arms `&1`
  pool-chain `+0x10`/`&2` free `+8`/`&8`+`&0x10` index tables
  `q[desc+0x48]`/`+0x40`/`&0x20` A850), A850 `0036A850` 382B/92i
  pre-order label walk (builds-and-discards, traversal+faults only),
  BC60 + full EXP-123 tree re-executed via the carve, FLAG
  `0046DFE0` + CHKCK `00808C40` real (GS-cookie residuals modelled
  per-frame: `0x2B994CD85D6A`/`0x2B994CD85FAA`). KEY FINDING: the
  allocator is a COMPACTING allocator — a third keyed pool-BST
  structure threads live blocks; A2A0 moves them down into lower
  free blocks. Disclosed: PREL/PINIT scripted (dead returns),
  output hook `q[0x8C2F70]` ships rdata `0x1CCEF16` (not code) —
  planted to real FLAG leaf; `w[rsi+6]` is a real overlapping word
  field vs the `+4` dword link. Finish rev 22617,
  REQ-AUDITSPEC-POOL-ADOPTION-REVIEW rev 22620,
  REQ-OPUS-POOL-ADOPTION-FINDINGS rev 22621, EXP124-PUB queued
  rev 22618.
  Prior: `SWE2-ORACLE-ALLOC-CORE-EXEC`
  (EXP-123) SEALED + routed (28/28 functional cases, 30/30
  byte-precise mutants, stable across three processes). The
  887B/246i allocator core `0036BC60` + its FULL callee tree —
  13 real bodies: BC60 core, A490 `0036A490` 215B/60i header
  init (`0xFF12` magic, kind `+3`, null encoded links, size
  `+0x18`, seq `+0x1C`, `b[+0x15]=8` iff `d[0x22D8E28]`), B210
  `0036B210` 161B/47i back+fwd coalesce + root fix, B2C0
  `0036B2C0` 319B/94i fwd coalesce (`survivor.key += victim.key
  + 0x40` when list-1 next == phys next — adjacency test), B5F0
  `0036B5F0` 124B/37i page-head min-addr insert + bitmap,
  FOUR exact-twin 179B/50i splices B670/B730 (`+4/+8` list-1
  after/before) + B7F0/B8B0 (`+0xC/+0x10` phys after/before),
  C900 `0036C900` 198B/60i page-head remove, C9D0 `0036C9D0`
  253B/71i dual-list unlink (`0xFF99` stamp), BASE `0020E600`
  + C620 `0020E620` codec. KEY FINDINGS: intrusive
  doubly-linked-list allocator NOT the BST first census
  suggested; `+4/+8` = ONE address-ordered free list with
  `q[desc+0x90]` HEAD / `q[desc+0x98]` TAIL (two search arms,
  same predicate, opposite ends — OPUS-CONTRA confirmed and
  corrected my compressed 'roots' phrasing); `+0xC/+0x10` =
  physical-adjacency pair whose roots are OPEN (no descriptor
  root observed); links BASE-encoded, roots RAW; carve arg4==0
  front (`rsi=node`,
  `rbp=node+0x40+size`) vs arg4!=0 tail (`rsi=node+key-size`,
  `rbp=node`), `rem=key-size-0x40`; **B210 coalesces eagerly
  after EVERY split through the shared `0x36BF1C` tail — both
  modes** (first model coalesced arg4!=0 only — diverged on
  every front-carve split); zero-roots arm is a list-emptying
  re-established by B210; exact-fit root writes QWORD but
  arg4!=0 no-neighbour zero is DWORD+qword (asymmetric width
  is real); page table `q[desc+0x28]` per-64KiB lowest-addr
  heads + bitmap `q[desc+0x20]`, pslot signed-16 floor;
  `w[blk+0x3E]!=0` → A570 (scripted) + hook cell
  `q[0x8C2D80]` (ships rdata ptr `0x1CCF02C` — EXP-126
  erratum corrected the earlier "ships 0"; still non-code,
  planted to real FLAG leaf) + int3
  trap (rip = site+1); per-tag usage `d[desc+0x68+tag*4]+=r14`,
  seq `w[desc+0x60]++` every call. Two disclosed boundaries:
  A570 `0036A570` 729B diagnostic (entry token) + the
  runtime-planted hook cell. Finish rev 21487,
  REQ-AUDITSPEC-ALLOC-CORE-REVIEW rev 21488,
  REQ-OPUS-ALLOC-CORE-FINDINGS rev 21489, EXP123-PUB
  queued rev 21490.
  Prior: `SWE2-ORACLE-ALLOC-DISPATCH-EXEC`
  (EXP-122) SEALED + routed (16/16 functional cases, 14/14
  byte-precise mutants, stable across three processes). The
  allocator dispatch layer — the entry points every allocation
  request passes through. Three real bodies: A100 `0036A100`
  129B/36i front door (BC60-then-BFE0 fallback; header writes
  `b[obj-0x3E]=staged-b2`, `d[obj-0x10]=-low32(arena)` via
  `C620(0)`, `w[obj-2]=0` constant — `esi` xor-cleared),
  BFE0 `0036BFE0` 261B/77i create-with-retry dispatcher
  (`bt(d[0x22D89B8],kind)` hard `jmp$` at `0x36C000`;
  `desc=0x22D7FD0+sx32(ST_W)*0xA8` — table base `0x22D7FD0`
  NOT `0x22D8FD0`, off by `0x1000`, settled by rbx trace;
  `kind>0xE` → desc=0 → real fault on `q[0xA0]`; indirect
  `call rax` at `0x36C03B` NOT stubbed — planted to real leaf
  `0046DFE0`; pool check AAD0+ABE0 marks `b[desc+2]`/`b[desc+0x62]`;
  `jmp 0x36C013` retry re-reads ST_W every pass — exit needs
  BC60 success or `esi==0&&edi==0`), C620 `0020E620` 9B/3i
  BASE-inverse (`ecx-low32(q[0x1F83530])`). KEY FINDING: the
  queue tag store `d[0x22D89BC]` IS the allocation kind — BC60
  and BFE0 read the SAME cell (an "overlapping dword"
  first-read was a 6-vs-7-byte decode slip, settled by trace
  `ecx=2`). Three scripted boundaries: BC60 `0036BC60` 887B/246i
  ten-callee core (EXP-123 candidate), AAD0 `0036AAD0`, ABE0
  `0036ABE0` — entry-intercepted planted returns, NOT
  native-proven. Finish rev 21431,
  REQ-AUDITSPEC-ALLOC-DISPATCH-REVIEW rev 21428,
  REQ-OPUS-ALLOC-DISPATCH-FINDINGS rev 21429, EXP122-PUB
  queued rev 21430 behind FABLE's `@publication`.
  Prior: `SWE2-ORACLE-EXP109-QUEUE-TAILS-EXEC`
  (EXP-121) SEALED + routed (27/27 functional cases, 22/22
  byte-precise mutants, stable across three processes). Nine real
  bodies over shipped globals: C140 `0036C140` 84B/19i LIFO pop
  (hard `jmp$` spin at `0x36C150` on cnt≤0 — never re-reads),
  C1D0 `0036C1D0` 20B/5i caller-stack thunk (`r9=q[rsp+4]-5`),
  C1F0 `0036C1F0` 150B/28i lane push (hard spin at `0x36C211` on
  cnt≥0x1F; stages `edx→ST_B2`, `r9→ST_Q`, `tag→ST_W` where
  `tag=b[0x22D89A8+sx32(ecx)]`), E400 `0032E400` 80B/25i —
  **primary ptr-table path returns RAW `d[ptr+rdx*4]` at
  `0x32E430`, the signed-aware round-to-64 (`cdq` adjust) is
  fallback-only**; 2D table base corrected to `0x2EC3EE0`
  (first static read `0x2EB3EE0` was off by `0x100000`), DE70
  `0046DE70` 5B jmp, T2D `002DF960` 28B/7i (`0x1388` row stride),
  CLR `00512EF0` 50B/13i (returns `CLRT+0x200` — an address, not
  a status), E520 `0032E520` 107B/32i (`ecx!=0` →
  `(pollq!=0)|(flag()!=0)`; `ecx==0` poll driver), FLAG
  `0046DFE0` 18B/5i (`d[0x215EFF4]==-1`→2 via `cmove`). The queue
  is one shared region — dword count array `0x22D89C0` (4B/lane),
  32-entry lane blocks `0x22D89D0` (16B/entry); pop+push compose
  a stage-and-requeue pipeline. Two disclosed scripted boundaries:
  `0032E070` + `0035EA30` (entry tokens, planted returns — NOT
  native-proven). Finish rev 21396,
  REQ-AUDITSPEC-EXP109-QUEUE-TAILS-REVIEW rev 21393,
  REQ-OPUS-EXP109-QUEUE-TAILS-FINDINGS rev 21394, EXP121-PUB
  queued rev 21395 behind FABLE's `@publication`.
  Prior: `SWE2-ORACLE-EXP108-TAIL-RESOLVERS-EXEC`
  (EXP-120) SEALED + routed (14/14 functional cases, 14/14
  byte-precise mutants, stable across three processes, **zero
  scripted boundaries** — every call target executes real). The
  last two EXP-108 scripted bodies, both on a stale "deep subtree"
  estimate. F56 `003E56A0` 24B/9i: **its second parameter is
  dead** — `mov rdx,q[rcx+0x400]` clobbers edx, so `add eax,edx`
  adds the table pointer's own low dword; `ret = sx32(low32(tab) +
  zx16(w[tab+2]))` = tab + inline offset through `cdqe` (dead-arg
  proven by `f56-deadarg`: rdx=0 vs 0xDEADBEEF, identical results;
  sign edge `f56-sign`: `0x7FFF9000+0x8000` → `0xFFFFFFFF80008000`).
  Same `+0x400` table family as FLDR/GETV. F60 `00370F60` 61B/19i:
  `rbx=sx32(idx)` BEFORE the sentinel; `bx==0xFFFF` is a **low16**
  check, not `idx==-1` — `0x0001FFFF` rejected, `0xFFFF0000`
  proceeds with sx32=−65536; `ret = BASE(d[p+0x84]) +
  sx32(idx)*0x290 + 0x80`, negative indices address backward.
  BASE `0020E600` rerun in-tree. **Every scripted boundary in
  EXP-108 is now closed.** Finish rev 21364,
  REQ-AUDITSPEC-EXP108-TAIL-RESOLVERS-REVIEW rev 21366,
  REQ-OPUS-EXP108-TAIL-RESOLVERS-FINDINGS rev 21367, EXP120-PUB
  queued rev 21368 behind FABLE's `@publication`.
  Prior: EXP-119 t51-tail-resolvers-exec
  SEALED + routed (16/16 functional cases, 15/15
  byte-precise mutants, stable across three processes; the residual
  EXP-118 named — both "deep ~85i" tails were overestimates. T51
  `0051B9E0` is a 5B `jmp` thunk to `0051F240` (138B/43i): mode =
  `sx2(d[ctx+4])` — 0→`RES(q[ctx+8])`, 1→direct, 2/3→0 **before any
  table read**; `elem = base + (idx&0xFFFF)*48` with the null guard
  on the ELEMENT pointer not the table (null table + idx≠0 derefs
  `idx*48` — real crash path); `b[elem]&2` lazy write-back
  `q[+0x18] = sx32(RES(q[+0x10]) + d[+0x20])`; returns the cached
  slot. E20 `00370E20` 11B = `BASE(d[rcx+0x94])`, offset UNSIGNED.
  RES's `≤0x40` bound zeroes the handle, not the sum — the addend
  still applies. RES `003AB7F0`/BASE `0020E600` rerun in-tree; only
  scripted boundary `0036B130` (real EXP-084) — the `003E5B30` tree
  is now proven-real end to end, closing the last EXP-109 scripted
  tail. 5 real bodies span+sha256 in bodies.json. Finish rev 21335,
  REQ-AUDITSPEC-T51-TAIL-RESOLVERS-REVIEW rev 21336,
  REQ-OPUS-T51-TAIL-RESOLVERS-FINDINGS rev 21337, EXP119-PUB queued
  rev 21339 behind FABLE's `@publication`.
  Prior: EXP-118 transform-vec-writer-exec
  PUBLISHED `8728d00dd` (26/26 functional cases,
  22/22 byte-precise mutants, stable across three processes; the
  residual EXP-117 named — the three-arm transform-vec writer
  `003E5B30` 338B/102i real: field `0xb` runs a four-deep resolve
  chain record→(gate+codec+T51)→obj→(sel `b[+0x328]`+keyed scan)→
  entry→(`+0x70`)→payload→(`d[+4]&3` picks `+0x30`/`+0x60` embedded
  vec block, modes 2/3 fall back) where every null degrades to the
  D6A fallback `{d[p+4C..54],1.0f}`/`{0,0,0,1.0f}` — graceful, not an
  error; `field!=0xb` uses the record's own `+0x400` table
  (`rdx=sx32(ftab+w[ftab+0xC])`, signed `field*16` rows) returning
  `w[entry]`, with `{0,0,0,1.0f}`/`0xFFFFFFFF` on any null. The
  return word distinguishes four outcomes. G42 `00422D50` 57B real
  (gate `d[+0xC4]==-1`→0, else `q[BASE(d[+0x10])+0xDA8]`→tail T51 —
  gate doubles as edx arg; second execution after EXP-109), G41
  `0041C970` 42B leaf (`sx16(w[+0x28])` count, `+0x30+i*0xA0`
  entries, match `d[+0x80]==sel`), EXP-117's D6A/MIDS/RES/BASE rerun
  in-tree. Scripted: T51 `0051B9E0` (EXP-109's boundary,
  `t51:rcx:rdx` tokens), `0036B130` (real EXP-084), `00370E20` (deep
  tail, its return is arm-2's `p`). Finish rev ~21294,
  REQ-AUDITSPEC-TRANSFORM-VEC-WRITER-REVIEW rev 21296,
  REQ-OPUS-TRANSFORM-VEC-WRITER-FINDINGS rev 21297, EXP118-PUB done
  rev 21305.
  Prior: EXP-117 slot-handle-algebra-exec PUBLISHED `fc414f5dc`
  (EXP-117) SEALED (30/30 functional cases, 25/25 byte-precise
  mutants, stable across three processes; the ALLOC side of the
  `0xE0` pool at `q[0x02B40528]` — the same pool whose consumers ran
  in EXP-113/114. Six real bodies: HID `003B56D0` 444B/96i (slot
  scan `b[+0x40]&1`, gen `d[0x02B40520]` clamp `>0xFFFFFF→1`, handle
  `(gen<<8)|slot` at `+0x10`, parent resolve ×2 through
  `q[0x022C6F28]` `0x740`-stride with the `+0x284` gate), FLDR
  `003E5AD0` 88B word resolver (`<0x20`→table, `0x104/5/6`→
  `w[r8+0x3A/3C/3E]`, else `0xFFFF`), RES `003AB7F0` 99B (execution
  corrected the static read — `setne`/`cmp1` routes ALL `low2!=0` to
  `0036B130`, the xor arm is dead; hres results `sx32≤0x40` unsigned
  are zeroed), MIDS `002ED570` 146B (conditional deposits, `d[elem]
  ==-1` gate, `cdqe` sign-extends the product), D6A `003E6DA0` 67B
  (double `-1` guard, tail `00370E20`), BASE `0020E600` 10B.
  Scripted: `0036B130` (already real EXP-084) + `00370E20` (deep).
  Findings: `arg=-1`/gate-0 is a crash path — FLDR derefs `[0x400]`;
  handle low2 = slot mod 4 selects the RES path; MIDS deposits are
  skipped not zeroed on null fields). Finish rev ~21251,
  REQ-AUDITSPEC-SLOT-HANDLE-ALGEBRA-REVIEW rev 21252,
  REQ-OPUS-SLOT-HANDLE-ALGEBRA-FINDINGS rev 21253, EXP117-PUB done
  rev 21302.
  Prior: EXP-116 name-registry-init-exec PUBLISHED `b78c24277`
  (EXP-116) SEALED (10/10 functional cases, 17/17 byte-precise
  mutants, stable across three processes; the real CRT initialiser
  sequence executed end to end — all 97 key + 143 channel init thunks
  in shipped .CRT-table order (link order — shuffled relative to the
  contiguous 0x20-stride thunk arrays) over shipped node objects and
  name strings, calling the real insert twins `00879570`/`00876C80`
  (132 B / 40 insns each); both list heads BSS — real load-time zero.
  Built chains node-for-node identical to the documented live lists:
  keys `Key_A`=28..`Empty`=0 (97), channels `Button_0`=11..`Empty`=0
  (143) with the shipped alias groups. Findings: .CRT order is
  load-bearing (address order gives a different list); dup check is
  byte-content not pointer identity — same-VA and copied-name dups
  both `0x12`, first registration wins; no type separation — a key
  node inserts through the channel twin with rc 0; `atexit`
  `00808B90` disclosed scripted boundary, per-thunk dtor-callback
  args traced as `ate:` tokens). Finish rev 21203,
  REQ-AUDITSPEC-NAME-REGISTRY-INIT-REVIEW rev 21204,
  REQ-OPUS-NAME-REGISTRY-INIT-FINDINGS rev 21205, EXP116-PUB done
  rev 21300.
  Prior: EXP-115 transform-primitives-exec
  (EXP-115) SEALED (24/24 functional cases, 21/21 byte-precise
  mutants, stable across three processes; second independent
  isolated-exec instrument over the contract's already-PROVEN laws —
  TPT `00398F90` 377B/68 insns true leaf, CT `00397910` 567B/119
  insns, CHKCK `00808C40` __security_check_cookie REAL 79B;
  `00809654` __report_gsfailure as disclosed fault-token boundary;
  whole-window byte compare `0x22D8F80..0x22D9330`. Findings: w is a
  LIVE read of `f[0x01EF93FC]` per call — leaf2 gains `2·M[3][c]`,
  leaf0 drops the translation row (the contract's "forced to 1.0" is
  maintained state reset by LEAF `0036DD80`, same global as EXP-114);
  `in[3]` copied to `0x22D9300` verbatim but never multiplied
  (w=99 vs w=0 byte-identical); `a==b==out` triple-alias safe (stack
  staging precedes all stores); `m-c-cookie` reaches gsfailure —
  proves the cmp is against shipped `q[0x01F44830]`; CT touches no
  globals besides the cookie — all four deposit slots are TPT's
  alone). Finish rev 21158, REQ-AUDITSPEC-TRANSFORM-PRIMITIVES-REVIEW
  rev 21159, REQ-OPUS-TRANSFORM-PRIMITIVES-FINDINGS rev 21160,
  EXP115-PUB queued rev 21163.
  Prior: EXP-114 shadow-lod-compute-exec
  (EXP-114) SEALED (38/38 functional cases, 38/38 mutants, stable
  across three processes; the EXP-113 scripted boundary `003B5980` is
  a contiguous family of SIX siblings `0x3B5980..0x3B6020` plus const
  leaf `0036DD80`, all generation-checking the same `0xE0` shadow
  pool at `q[0x02B40528]` — LODC `003B5980` 629B (computed shadow
  LOD) / ACC `003B5C00` 214B (five-channel countdown accumulator) /
  CPY `003B5CE0` 88B / INIT `003B5D40` 213B / FSYNC `003B5E20` 473B /
  CLRE `003B6000` 27B / LEAF `0036DD80` 15B = 7 real bodies; 3
  scripted boundaries: RES2 `00421FF0` + GATE `003E6F70` via EXP-108's
  stub layer (executed real there), `sqrtf` IAT `00861F14`. Findings:
  FSYNC's second w32-block copy reads arg+0x54 not +0x14 (seventh
  payload dword); w32 scale is `sar ax,6` (right shift) + packed
  mulps vs vec4 `0x00D115B0`=0.0234 storing lane 0 only; LEAF const
  `[0,0,0,1]` supplies xmm6=1.0/xmm3=0.0 clamp bounds (not
  immediates); distance uses dx²+dy²+dz² with G_C[0] overwritten by
  the result (0x22D8FB0 mixes fade + squares); INIT `q=1/bits2f(edx)`
  is a float reinterpret — edx=5 → +inf, not 1/5; upper xmm0 lanes
  always zero (movss); LODC fade = clamp(1-(min(gy,max(gx,dist))-gx)
  *gw, 0, 1)). Finish rev 21123, REQ-AUDITSPEC-SHADOW-LOD-REVIEW
  rev 21124, REQ-OPUS-SHADOW-LOD-FINDINGS rev 21125, EXP114-PUB
  queued rev 21126.
  Prior: EXP-113 shadow-sync-stage-exec
  (EXP-113) SEALED (25/25 functional cases, 38/38 mutants, stable
  across three processes; the 'display character : shadow' stage end
  to end — GATE `00428E40` 48B / WALK `00426420` 94B / SYNC `00426340`
  211B (the SyncShadowObjects body read in §13) / V1 `003B6900` 43B /
  V2 `003AFD00` 44B / LODS `003B6B80` 28B / THUNK `00521440` 5B =
  7 real bodies; 2 scripted boundaries: LODC `003B5980` (~16KB deep
  computed-LOD pipeline, planted xmm0) and PASS `003B6020` (EXP-108,
  ret-stub at the tail jmp). Findings: stage gate is two bytes
  (b[+0x48842]==1 && b[+0x48843]==0, tested in gate AND walk); d[+0x284]
  flag gate is a 4-bit mask (bits 2,6,7 + bit12 = 0x10C4) plus
  w[+6]==-1 and !(b[+0x2AE]&2); b[+0xC0]&0x18 selects the verb set
  (nonzero skips h114, ==8 arms h118 second verb); b[+0xC0]&2 selects
  const f[+0x27C] over computed LOD; both pools generation-check
  (V1/LODS d[+0x10], V2 d[+4] — different layouts); second pool is an
  in-image 0x70-stride table at 0x02B3F570 not a pointer;
  unconditional V1(h,6)/V2(h,0) run before the flag gate). Finish
  rev 21091, REQ-AUDITSPEC-SHADOW-SYNC-REVIEW rev 21092,
  REQ-OPUS-SHADOW-SYNC-FINDINGS rev 21093, EXP113-PUB queued rev 21094.
  Prior: EXP-112 actor-record-init-exec
  (EXP-112) SEALED (39/39 functional cases, 46/46 mutants, stable
  across three processes; ctor `00266530` 1439B — the body EXP-107
  scripted — plus six real callees RMAP `00266AD0` 211B / KINIT
  `00266BD0` 95B-all-arms / SINIT `003DB580` 183B / TAIL `003DB280`
  23B / QWALK `003DB6E0` 158B / BASE `0020E600` 10B = 7 real bodies;
  7 scripted boundaries incl. two proven unreachable from this entry:
  `00268EA0` (b[+0xB]&8 masked off) and `003DBDC0` (b[+0x63]==0 skips
  the queue walk). Findings: ctor &0x1F bounds only the subflag-table
  index (RMAP/KINIT re-read b3); w[desc]>=0xA gates ONLY DBB60 site1
  (sites 2-4 unconditional, site4 edx=0 no inc); cls60 sites are
  or/and on d[+0x1C] not calls, site6-ok clears site5's bit2; rep
  stosw makes every literal-word arm dead (always 0xFFFF); link
  swap-out dead (b12 preset 0xFF) but write-in unconditional for
  link 0..0x7F into q[0x0209A1F0+link*8]; registration cell
  0x02F8F2A0 = q[+0xF8] dword-zeroed; subflag==1 kinds {2,4,7};
  KINIT jt {0:0,1/2:0x38,3/4:0x40,5/6:0x30004,7:0x34C85} with
  b14|0x80 on kinds 5,7; A8 clear stride 0x28 over r15 slots).
  Finish rev 21064, REQ-AUDITSPEC-ACTOR-RECORD-INIT-REVIEW rev 21065,
  REQ-OPUS-ACTOR-RECORD-INIT-FINDINGS rev 21066, EXP112-PUB queued
  rev 21067.
  Prior: EXP-111 mt-twist-simd-exec
  (EXP-111) SEALED (8/8 planted-state cases, 20/20 mutants, stable
  across three processes; shipped twist `00866B90` 463B leaf — scalar
  flag=1 and SIMD flag=2 arms produce BYTE-IDENTICAL 624-word states,
  both matching an independent Python MT19937 reference; SIMD is a
  prefix accelerator over elements 0..223, scalar always runs the rest;
  SIMD masks `0x80000001`/`0x7FFFFFFE` differ from scalar only in
  shifted-out bit0 lanes; mti reset unconditional). Finish rev 20934,
  REQ-AUDITSPEC-MT-TWIST-REVIEW rev ~20936,
  REQ-OPUS-MT-TWIST-FINDINGS rev ~20937, EXP111-PUB queued rev ~20938.
  Prior: EXP-110 phyre-script-callers-exec
  (EXP-110) SEALED (48/48 cases, 38/38 mutants, stable across three
  processes; three real subjects D10 `00684D10` 585B / F60 `00684F60`
  470B / C280 `00686280` 1447B + nine TValue-stack leaves
  gettop/settop/pushb/pushi/pushn/pushp/tobool/type/sing = 12 real
  bodies; 29 scripted boundaries disclosed incl. the 12 TLS singleton
  getters). Findings: result store sizes 1/2/4/8 (s3/s4 word arm);
  result dispatch bound SENTS[0..8]; marshal s11 is PUSHI; stack pops
  preserve bytes (stale TValues re-observable, negative depths);
  `006372A0` = shipped const `0x02CF8270`; C280 consumes one elem per
  pool on null-state checkout; SETFLD consumes PUSHP's type tag.
  Finish rev 20918, REQ-AUDITSPEC-PHYRE-CALLERS-REVIEW rev 20919,
  REQ-OPUS-PHYRE-CALLERS-FINDINGS rev 20920, EXP110-PUB queued
  rev 20921.
  Prior: EXP-109 render-pool-lifecycle-exec
  (EXP-109) SEALED (45/45 cases, 79/79 mutants, stable across three
  processes; six real subjects CTOR 741B/LKUP 208B/ALOC 329B/
  PROM 403B/RETI 328B/RELE 358B + 23 real callees incl. CLR
  `0041F730` 1208B reset writer, DRAIN `00426EC0`, HC1/HC2
  `cl`-indexed clears, BASE/BAS2 resolvers, 7 ctor inits; 18 scripted
  boundaries disclosed; six initial mutant survivors were
  fixture-coverage gaps resolved via prom-pinbit1/prom-staleprev/
  drain-mid/rele-retired-c4neg/prom-nohandle/aloc-first
  distinct-d30-epoch). Finish rev 20902,
  REQ-AUDITSPEC-POOL-LIFECYCLE-REVIEW rev 20903,
  REQ-OPUS-POOL-LIFECYCLE-FINDINGS rev 20904, EXP109-PUB queued
  rev 20905 behind SWE2-FRONTIER-PUB-BATCH-5.
  Prior: EXP-108 ramp-channel-consumers-exec
  SEALED (38/38 cases, 45/45 mutants, stable across three processes;
  10 real bodies: PASS `003B6020` 677B + BLD `003B62D0` 1301B +
  SWAP `003A1DB0`, FIN `0036F360`, K3F `00264670`, RLUT `0046FAE0`,
  RES1 `003B6BF0`, GATE `003E6F70`, RES2 `00421FF0`, BASE `0020E600`;
  scripted `003E56A0`/`002ED570`/`00370F60` deep resolvers).
  Finish rev ~20815, review REQ-AUDITSPEC-RAMP-CONSUMERS-REVIEW rev 20816,
  findings REQ-OPUS-RAMP-CONSUMERS-FINDINGS rev 20817.
  ALL SEVEN QUEUED PUBLISHES LANDED 2026-09-19 (~04:20Z):
  EXP-102 `27a45dc08` (52/52,16/16), EXP-103 `43f0924e5` (31/31,15/15),
  EXP-104 `b6b91cd93` (65/65,22/22), EXP-105 `a4c7b8a0f` (30/30,20/20),
  EXP-106 `b644c9d3b` (58/58,46/46), EXP-107 `a8aa66342` (27/27,26/26),
  EXP-108 `6848d779f` (38/38,45/45). Each commit = record +
  check.py/result.json/bodies.json/gen_bodies.py; neighbour guard
  ADDS-NOTHING on the full 35-path batch; @publication released by the
  EXP108-PUB finish.
  EXP-101 find-owning-unit-exec published
  `58859ed57` (19/19 cases, 12/12 mutants, three stable processes;
  0031B860 + 00236850 + 00236820 all real — zero scripted boundaries;
  35-caller primitive de-stubbed). Finish rev 20441, requests revs
  20442-20443, board tails `0e424c2ca`/`663ea754d`, @publication
  released rev 20448.
  EXP-100 auto-status-gates-exec published
  `d0bb9351` (40/40 cases, 13/13 mutants, two stable processes; subject
  0030FED0 + gate chain 00322C50/0031E9A0/0031E9F0/00323890/003241D0 +
  0020E600 + 00808C40 real = 8 bodies; FIND/APPLY/CASCADE/NOTIFY/TAIL
  entry-stubbed, disclosed). Finish rev 19320, requests revs
  19321-19322, board tail `f8cfd2b7`, @publication released rev 19342.
  Stale EXP096-PUB row closed revs 19343-19344.
  Record-correction batch `d5a4b7746` + board tail `b5b3eea24`:
  EXP-085 arg0 convention, EXP-093 finding-2 gate is delta<0 (not <=0;
  `jns` at 0030061F on raw r14d delta — `field15` in zero-delta traces
  comes from later call sites 0030136B/00301538 in downstream bodies),
  EXP-092..100 `contract:`/`method`/`live_game` frontmatter (schema gate
  100/100). Four OPUS tasks finished revs 20411-20414, @publication
  released rev 20417.
  Earlier: EXP-099 `47b9084b` (finish rev 19240, requests revs 19248-19249,
  board tail `e207c3d0`, @publication released rev 19261).
  Earlier: EXP-098 `3ccb447c`, EXP-097 `ddfbe1d9`, EXP-096 `68c6cec5`,
  EXP-095 `92a9f665`, EXP-094 `1c31051a`,
  EXP-093 `5601f8fe`,
  EXP-092 `1f8b51f7`, EXP-091 `785d37b9`, EXP-090 `d8f74e59`,
  EXP-089 `fe009fa0`, EXP-088 `dbb8ce23`, EXP-087 `1da00aab`, EXP-086 `41394bba`
- **Exact next action:** EXP-211 record + contract landed; every
  tag-15 sub-arm path exercised — next is the deep param-parser
  family (`3FFEE0`/`3FFBC0`/`3FFD70`/`3FFC60`/`3FFCE0`/`3FFDA0`/
  `3FFB00`/`3FFB90`/`3FFF10`, all scripted boundaries now) or the
  next member-block carrier;
  publish EXP-150 the
  moment `@publication`
  frees (FABLE holds it for `FABLE-PUB-001E2AF0-FINISHED`; commit
  message prepared, `EXP150-PUB` READY) → finish
  `SWE2-ORACLE-UNIT-INSTALL-EXEC` + `EXP150-PUB`, release the lock.
  **FRONTIER adjudicated the stalled-lease request DONE (rev ~29173):
  lease presumed live — identical 24h-old signature resolved as a
  real ~18min gate loop; no peer-release path exists by design.**
  P1 `FRONTIER-REQ-FABLE-PUBLICATION-LEASE-CHECKPOINT-OR-RELEASE`
  is queued for FABLE's next turn — do NOT re-escalate; wait.
  **STATUS UPDATE (EXP-182 done): EXP-151 through EXP-182 are
  ALL execution-validated in Temp (24, 22, 37, 53, 68, 77, 86,
  102, 109, 117, 122, 126, 131, 132, 140, 143, 144, 149, 153,
  155, 155, 165, 170, 172, 180, 184, 190, 203, 220, 229, 237,
  239, 240, 243, 244 — all stable x3); records drafted at
  `Temp\EXP-15x..17x-*-exec.md`; the "Then claim EXP-151" text
  below is stale planning history kept for the fixture notes.**
  ALL `312730` opcode arms now covered (0x4000..0x4025
  sub-dispatch, 0x4026..0x4035 scan, 0x4124/0x4125/0x414A/
  0x414E/0x4165 singles). `230A40`/`2324F0` usable-surface
  semantics decoded + executed (bit-query mask merge +
  point-in-triangle edge eval; EXP-172 also fixed the dead
  `t2*` assert chain + the `epos`/`ownerres` nesting bug —
  dormant EXP-165..171 asserts now live and passing).
  `22F830`/`22F8B0`/`381EB0` occupancy layer decoded +
  executed (4-lane CSR span driver, id 0x4000..0x4FFF walk,
  bit31 mask-merge filter, 4x4 local-space box/cylinder
  volume conflict; EXP-173). Every `231400` accept-gate
  layer now has executed +/- coverage. `336390` footprint
  gate executed direct (EXP-174): center + 4 corners at
  +-halfwidth on x/z via `32A6A0`->`26E100`->`231400`,
  fail-fast; real CW-triangle fixture proves the corner
  consults `2324F0` geometry (first geometric rejection in
  the footprint path).
  `233050` pos->cell edge cases executed direct (EXP-175):
  16-bit 0xFFFF sentinel (callers test ax/js), constant
  -cellh/2 odd-column stagger, idiv trunc-toward-zero makes
  stagger-underflow rows clamp to 0 (never negative), int
  origin offsets ctx+0x38/+0x3C, upper-bound-only checks.
  `26E130`/`26E150` executed (EXP-176): clear lo-dword slots
  in BSS table 0x209A3E0 (stride 8), then `3278D0` sweeps
  obj array q[0x208E688]/count d[0x208E6A0] (stride 0xF50,
  gate b[obj]&0x10) -> 3839C0/3839F0 invalidate the
  obj+0x200 cached cell record (w+0xC/+0xE=0xFFFF,
  b+0x10..0x8F=0xFF). Sweep runs once PER cleared slot.
  **CORRECTION to EXP-173**: `22F8B0`'s merge table base is
  `0x209A3E0` (not 0x209A2D0 — that is `230A40`'s). It is a
  per-group bit-override mux {A=enable, B=value}:
  `merged=(B&A)|(flags&~A)`, skip iff bit31 (EXP-177).
  `26E850`/`26E880` field-edit A/B; `26E130`/`26E150` clear A;
  `26E960` = egrid installer (stores ctx->0x209A670,
  ctx+0x40/+0xA8 sub-ctxs, resets whole table, 0x50 sweeps).
  22F8B0 mux proven BOTH directions (inject + clear).
  Slot-API wrappers + builder executed (EXP-178): `3791D0`/
  `379270`/`379220` release idx or whole ranges 0..0x1F/
  0x20..0x3F/0x40..0x4F; `3791F0`/`379240` write a 5-bit
  override field at bits 18-22 (mask 0x7C0000); `26E8D0(n)`
  re-inits nav sans table reset, `d[0x209A2D0]=3ED0B0()` is
  a triple-duty cell (230A40 base + 379630 count); `379290`
  gate q[0x2ADD090] picks reinit vs `379630` rebuild (free
  d[0x2ADD120..]+0x2ADD11C, alloc clamp(count,0,3) via
  3AB960 from template 0x2A5A2E0). Harness: `t3*` assert
  prefix activated (same dead-branch class as EXP-172).
  Handle pool executed (EXP-179): `3AB960`/`3ABCA0`/`3ABD00`/
  `3ABD20`/`3ABB60` = 0x80x0x70 generational-handle pool at
  q[0x2B3F528] (handle gen<<8|slot, payload +0x20, dll +8/
  +0x10, head 0x2B3F508 tail 0x2B3F510 count b[0x2B3F500]
  gen d[0x2B3F504]); kind byte +0x20 in {2..5} runs derived
  float precompute (K=1.0f); `3ABB60` inits + allocates
  builtin kind-7 rec0 via 3AC920; `265920` = 17D490()>0
  else b[0x21654E0]+1. The 0x2ADD120 handles ARE these.
  Builder tail closed (EXP-180): `379760` allocs kind-6
  extra rec -> d[0x2ADD11C], quad = cfg row0 (37AD10 table
  0x2EBF460 stride 0x50, i<5; neg idx reads pre-table)
  scaled by f[0x209A370] (=3ECFD0's init block);
  `3AC920` = payload-relative recompute of the 3AB960
  kind math (kinds 0/1/6/7 = no-op); `1D50D0` = lazy
  singleton q[0x1F81428], `17D490` = d[+0xAAC].
  Nav accessors un-stubbed (EXP-181): q[0x2EBB7F0] = row
  table stride 0x180 indexed d[0x209A6E8]-1. 3ED0B0=
  d[row+4] (->count), 3ECFD0=row+0xF0 quad ->0x209A370
  (=379760's scale!), 3ED140=f[row+8] (null->K=1.0f),
  3B6BA0 stores it to f[0x1EFE314], 3ED020(i)->0x209A2F0
  recs (two 0x20-arrays at row+0x90/+0xA0), 3ED7B0(i)->
  0x2EBB7F8/7FC/804. 26E8D0 fully real; 379630 count now
  via real 3ED0B0. 1CCB20 ctor mapped (EXP-182): 0x10E8-byte
  render/lighting singleton — f[C10]=pi/4, f[C14]=16/9,
  +0xD0C/+0xD2C/+0xD4C = "None"/"Irradiance"/"Specular";
  d[+0xAAC] (nav-gen) starts 0 -> 265920 fallback arm.
  1D50D0 alloc chain runs fully real (allocx stub).
  2FEF30 member arm value-verified (EXP-183): stat =
  growth[r13+0x24 row]*delta(b[88]->b[1C2]) + base[r13+0x22
  row] + rec word; HP cap 1e9 member / 9999 nonmember
  (d[rsp+3C]=b[rec+5]; corrected by EXP-184); r11 row ->
  out+0x1C..0x20 in order
  +0x2C,+0x29,+0x2A,+0x2B,+0x2D; member-row b[+0x15] bit0/
  bit1 gate two extra stat arms. Equip loop (322C50 slot!=0)
  and license loops (rec+0x68/+0x78 bitmaps, tables
  0xD10290/2A0/2B0 — EXP-185 corrected the addr) were
  zero-list then; closed nonzero by EXP-185.
  2FEF30 nonmember arm done (EXP-184): HP = (b[row+0x18]+1)*
  d[rec+8]*b[row+0x19]/100 via 2F8E50; MP = w[rec+0xC]*
  b[row+0x1D]/100 via 2F9180 — both un-stubbed (leaf arith).
  Stats = trunc(f[rec+0x10..0x1C]); immunities d[row+0x48/
  0x4C] -> out+0x18/+0x14. HP caps: member(b5!=0) ->
  0x3B9ACA00; nonmember -> 9999; b4-0x1B in [0,0xC] -> second
  clamp 0x7FFF applied to RAW hp (can exceed 9999). Nonmember
  row desc = q[0x2EBF130], idx b[rec+4]. equip desc =
  0x2EBF0F8, license desc = 0x2EBF040 (trace order).
  Equip+license loops done (EXP-185): 322C50 = 32-case
  bounds validator (kind6 = 0x2EBF0F8 range [0x1000,0x1000+
  count)); case1 re-dispatches via 309440 = d[0x1EEBCF8+
  (id>>12)*0x58]; case13 sums 4 descs. Equip: 5 slots at
  r8?:rec+0x50; cls1(b9 raw1..5) +0x1A/+0x1D -> out+A/E
  (gate rsp+4C); cls2(b9=18) +0x18/+0x19 -> out+F/0x10
  (gate rsp+70); cls3(b9=19..22) +0x18/+0x19 -> out+B/C;
  aug row aux=elemb+d[item+0x28]: w->HP, w+2->MP, b+4..7->
  out+6..9, d+8/+0xC -> out+0x18/0x14, b+0x10..0x14 -> out+
  0x1C..0x20. Lic: boards rec+0x68/+0x78 (bitmap base IS
  rec via rcx home); tables 0xD10290(16,out+6)/0xD102A0
  (16,out+7)/0xD102B0(12,HP augments 0x4A-0x55); row desc
  0x2EBF040, adds w[row+4]. out+0x11/0x12 merge class
  accums (caps 100). 2FEF30 now fully closed — every arm,
  loop and clamp value-verified nonzero.
  231400 pos-commit done (EXP-186): 233050 pos->cell ->
  233110 containing-tri scan (w[out+0x52]=tri or -1; span =
  w[ridx+cell*2]..w[ridx+(cell+1)*2]; tri>0x3FFF skip;
  230A40(kind=w[out+0x50]) gate; 2324F0 inside = ret<0) ->
  cell plane solve y = (nx*(v0x-px)+nz*(v0z-pz))/ny + v0y,
  gated ny > f[0x8C5B2C]; mode0 snaps probe y, mode1 rejects
  y>pos.y; inline cell re-derive (remainder stagger form);
  22F830 ctx {cb dword=22F8B0 — 32-bit truncated store,
  lane=ectx, cell2, lanemask 6, probe, found, filter 1} ->
  ret = found==0. 22F8B0 entity ids [0x4000,0x4FFF] ->
  q[lane+0x18]+(id-0x4000)*0x90; span len signed-compare.
  231890 = standalone plane evaluator (same formula).
  232760 commit publish done (EXP-187): 233110 -> 22EF20
  (380A60 yaw basis {-x,0,z}+up+cross -> 0x2089280 region A;
  217610 4x4 inverse -> 0x20892C0 region B; A*=diag(max
  (f[out+0x80/0x84],0.01)) bbox scale, B*=inv — the region
  scale IS the query bbox) -> publish d[0x2088FE0]=visited
  tri LIST (cap 0x80, count d[0x20891E0]) seeded w/ cont tri,
  d[0x20891E4]=0 -> 22F9B0 recursive wall-slide: per edge
  nbr w[cellrec+0x16+i*2]; portal -> dedup+append+recurse;
  wall len<1.0 -> rdi=0 direct push f[point]+f[out+0x40]+
  flags|0x10 (lands exactly at dist 1.0); t<0/t>len vertex
  clamp -> rdi=vert ptr -> queue q[0x20891F0] pending
  (cap 0x10, d[0x20891E4]++) — EXECUTED via portal into tri
  where P projects past shared vert (253/253 x3; fixture
  needed nbr[0]=self to skip tri0's own e0 push which had
  moved P >1.0 from the vertex). 22F250 pulls f[out]
  toward pending pts >1.0 region-dist (pull arm covered
  only at count-0). 232760 ret = dead cookie-xor (void).
  Transform helpers all real:
  217060/217150 matmul, 217610 inverse, 202B70/202B90 point
  xform, 202D50/202D70 wrappers, 203170 identity.
  22F8B0 occupancy inside 231400 done (EXP-188, 256/256 x3):
  22F830 lane = ectx itself (shared ridx bounds + rows ids
  with 233110 lane-0 scan); span_idx = lane*(C+1)+cell,
  C = w[ectx+0x40]; eid range [0x4000,0x4FFF] -> ent rec
  q[ectx+0x18]+(eid-0x4000)*0x90; filter idx
  (d[ent+4]>>0xD&0x1F)+0x20 -> mux d[0x209A3E0+idx*8..+4],
  r8=(A&B)|(~A&e4) >=u 0x80000000 veto; 381EB0 kind 2 =
  probe xformed by rec+0x50 in (-1,+1) box (hi = K=1.0f
  0x1CEBBA8, lo -1.0f 0x1CEBC9C); first found wins,
  ret = found==0 semantic eax. Verified lane-1 hit,
  lane-2 hit, mux veto (381EB0 never called).
  2EF640 static-init block done (EXP-189, 268/268 x3):
  2EF640 leaf-getter -> tbl 0x2164280 (0x56690 B). 2EF650
  master init = full tbl memset -> 253A80 (sig fields
  +0x58..0x6C = 20050223/1538/5071901/7410/131F3EA/4818,
  bufB +0x30/0x3244/0x224 memsets, 12x253240) -> 2EF2D0
  (memset tbl+0x200,0x1538 -> 379160) -> 238A80 (store
  tbl+0x4E68C=0x21B290C -> q[0x2EBF190]) -> 30B6A0 reloc
  patcher (recs 0x1EEBCC0..0x1EEC1E8 stride 0x58 = the
  309440 desc table; q[rec]!=0 -> q[rec+8]=d[rec]+low32(base);
  d[rec+0x40]=accum += d[rec+0x3C]; clears base+0x57C8/0x59C8)
  -> s237df0 fan-out. 253240 = 12-arm slot init; ELEMB
  cell = q[0x1F83530] (20E600 +q / 20E620 -d); slot recs
  at 0x2092760 {w sz, w 0x40, d arena-rel off, w 0},
  flag->0xFFFF fill. 32AB60 bitmap tbl+0x16F4+id/8 id
  [2,0x1FF] set/clear/oob verified. 379160 blob walker
  q[0x2ADD0D0] {w+8 cnt, words +0xA} -> 32AB60(id,1).
  2EF690 copy 0xACD*0x80+0x10 0x1FB6940->0x2211000 +236760;
  2EF740 copy 0x20010 0x21726C0->0x21C8D80.
  1D0390/202880 deep init done (EXP-190, 268/268 x3):
  1D0390 = name-table ctor inside 1CCB20. s1ea3c0 stub
  (zeroes map hdr +0x28/+0x30, ret 0) -> success path real:
  b[+0xA68]=1, ~40-entry str table +0x138..0xA50, OFF
  0x46464F@0xAE4, Torrent/Inferno imm. 22-iter loop:
  s1cd0e0 fmt-stub -> 0x8FF950 fallback key -> 1EA1E0
  REAL map insert x22 (multiset, d[+0xA90]=cnt=0x16);
  whole grow/rehash chain real: 1EA6C0/1C2720/1C19A0/
  1C26B0/674A00 hash*0x21, 17D260->19C580 aligned_malloc
  bump-stub, 584730->19C570 aligned_free nop-stub.
  b[+0xF0]=1,+0xF1=1,+0xF2=0,d[+0xF4]=0x16,f[+0xF8]=-0.06,
  f[+0xFC]=-0.614, q[+0xA80]=fakeloc+0x18C0 (624660 real;
  TLS trio stubbed). 2F79E0 xmm 0x22BE930 verified.
  202880 = 2001F0 typed-release (d[+0xA98]=6 out-of-range
  early-ret) then restamps 6/0. New stubs: s19c580 allocx,
  s19c570, s1ea3c0(initmap), s1cd0e0, s615bc0, s624670
  (fakeloc), s616700, qpczero xmm0 retkey on s5cc930;
  861EBA memcpy real-semantics hook added.
  EXP-151 LANDED (commit 69e9cad19): rekey inner `00322050`→`003220E0`
  executed — harness + evidence at `_experiments/evidence/rekey-inner-exec/`
  (24/24 stable ×3; all callees real except scripted `00326500` notify;
  proven: gen bump `w16=(w16+1)&0x7FF`→1, id `(g&0x7FF)<<20|(c&0xF)
  <<16|idx`, `2659D0`/`327150` have no null guards — `3220E0(0)` and
  null `q[02EBF190]` fault; `b[02089340]&0x10` gates the RESOLVE
  only — match always stores `d[glob+0x5AA4]` + notifies `326500`;
  `3588B0` resolve = cls-table `02098E10` row + bounds + gen check).
  Contract `battle-unit-construction.md` §13/§14/§15 synced —
  `003220E0` no longer listed unexecuted; `0023AC80` remains.
  Commit 69e9cad19 swept 33 peer-staged files (index race — same as
  EXP-189); later commits used pathspec to stay clean.
  CONTRACT SYNC DONE (97f02f897, 2f20826a7): EXP-152..161 all landed
  in repo already (records + evidence dirs run green in place —
  22/37/53/68/77/86/102/109/117/122/126/131/132/140); battle-unit
  contract §13/§14/§15 now reflect executed status. Still scripted
  there: `00308010`, `003271D0`, `00326500`, `0030C650`, `00323910`,
  `00324100`, `00317930`, `00318B40`, `003243F0`, member-block chain.
  S-02 RUNTIME DONE (EXP-191): OPUS request
  `OPUS-REQ-ORACLE-S02-RUNTIME-WORLD-TICK-AND-STOP-REGISTRY`
  executed — world tick `00314020` + stop registry
  `00226B30`/`00225CD0`/`00225EB0`/`00226280` + latch `00314410` +
  drain `0025BFB0`, all shipped bytes, ~55 scripted callees.
  37/37 x3 stable, zero faults (WT-6 second pass: slot bodies real). SS-1 proven twice (zero bitset
  reads via mem-hook + bitset-invariance), SS-2..SS-6 all
  executed (fade min via `226640` edx, bit41-or writeback,
  dirty-gated early-ret); SS-7 partial. WT-1..WT-5 executed
  (5 mode consults; drain-before-mode; TIP 1->0; latch consume +
  deferred `32FC30` + `314410` FWW; 5-slot/16-substep with
  gate=1 -> 80 calls, gate=0 -> 5 — `267310` gate is INVERTED:
  nonzero eax runs the calls); WT-6 EXECUTED too — 234590/234520
  are slot-0-only (9-insn epilogues on ecx!=0), 25D9E0 works all
  slots + slot-0-only arms (25B740/25B600), 3DB1F0 unconditional
  per-row 3DB6E0; in-tick: bodies 80x, slot0 chains 16x; 267310 =
  leaf flag byte b[02098E10+i*0x288+0x201]. Corrections: `263FF0`
  base is `02098E10` not
  `0208E688`. Both contracts' §13 updated; record
  `_experiments/EXP-191-s02-world-tick-stop-registry-exec.md`;
  evidence `s02-world-tick-stop-registry-exec/`.
  EXP-192 DONE (member-block chain, 116/116 x3): drove `0031A630`
  r9d=1 — `0030F9A0`/`0030C410` class gates (0x1xxx only, cx!=0x1000)
  -> `3008A0` -> `309F30` -> class-1 `2FD8D0` validator / `2FD150`
  mutator (count<<0xA|cap word, edx=-1/+1, clamp [0,cap]); `0031B860`
  owner scan (q[+0x698]==rec over 236850/236820); `00324470` teardown
  (2ECF10 bit23, 3105D0 scripted-EXP-161, (d[+0x64]|d[+0x3C])&0x80000003
  nonzero gates 313F60, ret0 -> b&2 gate -> 300E40, then
  2E42D0/2699D0/2ECEC0(q[+0x10]), or d[mbr],0x40). Evidence
  `member-block-chain-exec/`; contract synced (chain removed from the
  scripted list — remaining: 308010, 3271D0, 326500, 30C650, 323910,
  324100, 317930, 318B40, 3243F0).
  EXP-193 DONE (small boundaries, 156/156 x3): `00317930` slot
  eligibility (slot 0..4, D107E8 shortcut [0x1000,FFFFx4], 322C50
  kind-6 member range on q[02EBF0F8] — r8d ZEROED at 31798B so kind
  is always 6, not slot+6; a5-flag -> 309EC0(id,0) real -> 2FD8D0
  free-count; tag b[row+7]>>5; esi==1 compares b[row+9] vs slot0
  row b[+0x11]; b[rec+5]!=0 short-circuits ret1; else foe-row
  bt d[frow],b[row+9]; final 323C60 nonzero=allow — scripted).
  `00318B40` pair rebalance real -> drives real 30F9A0/30C410
  chain (r8=0 pure reconcile; null desc faults @318BE0 disclosed).
  `003243F0`=3105D0+324470-tail real; `00324450` b&0x40 gate ->
  realx-promoted 3243F0 + clear. `00308010` b[rec+5] dispatch
  (308130/308040 scripted arms). `00324100`=324020+13-iter licence
  bit scan -> 308FF0 (both scripted). `003271D0`=b[02EBF190+0x5AA4].
  Contract synced — remaining scripted: 326500, 30C650, 323910,
  308130/308040, 308FF0, 324020, 323C60.
  EXP-194 DONE (leaf arms, 186/186 x3): `308130` state-step real —
  `307D10` recomputes bit16 of d[member+4] (fast iff b[rec+5]==0 &&
  b[rec+4]==0x1A; else 377C20==0 && (d64|d3C)&0x8000020; else
  253B90==0 chain via d4&0x200->30B050 / d4&0x400->307CE0->30BF20);
  (d64|d3C)&0x8000020 OR 253B90()==0 -> bt bit16 -> ret1; clear ->
  b[022C1F48]&1 -> 3081E0 real (328370 LCG + 32A150) -> b[rec+5]
  /32A150-vs-d[+0xDCC] setae. `308040` real (flags-obj d&0x48 +
  f4<-9.18e12 -> 30B050 -> 234DA0 stubbed; &0x48==0 -> q[member]
  bit40). `308FF0` = 02EBF138 accessor (b1E in {5,6} -> b[+0xA];
  null desc faults @30904A). `324020` = 18-pos popcount (CORRECTION:
  not a max-scan — it's the count that bounds 324100's loop).
  `323C60` real: 322C50 kind-1 = class-nibble auto-dispatch via
  309440(d[01EE7CF8+cls*0x58]); null rec/b5!=0/b4>6 -> ret1; memt
  row b7&0x10 -> ret1; else 323BB0->2F8FA0 builds kind-0 req bitmap
  from ABILD rows (b5->323890->3241D0==0x15 i.e. b5 in {1,2,3},
  si in w[row+8..0x15]) intersect rec+0x194 -> nonzero -> ret1.
  New stubs: sp234da0 retkey, cookie (808C40 nop). Remaining
  scripted: 326500, 30C650, 323910, 234DA0, 263E30.
  EXP-195 DONE (notify dispatcher tree, 202/202 x3): `326500`
  real — 311E20->326620->30D9A0 mode (d[glob+0x5B04]: &8->5,
  &4->4, 377C20!=0->3, &2->2, &1->0/1) -> bl modes 0/1=b[5AA4],
  2=0x1A, 3=377C70 (3148F0->2EF2B0+0x200 d[+0x1044] -> shared
  02ADD100 tbl b[3N+0xA]>>4&7), 4/5=0xFF -> 31B770(bl) (slotrow
  glob+8+bl*0x1C8, OBJARR q[+0x698] scan) -> hit ebp=d[objrow+8]
  (+317400 at mode1: b[5AD4]/b[5AD5] -> 31B770 x2 -> 26DAC0),
  miss -> 4x 322C50(0x17,i)+b[5A5A+i*2]->2367A0 -> same; exhaust
  -> ebp=3589B0(263750(0)) (gen<<0x14|cls<<0x10|w[0]); tail
  311e20 -> jmp 3594B0: d[022C7FE4]=ebp, b[022C7FF8]=1. 311E20
  gated by d[022BE974]; chain 3272F0 (b[02089340]&0x10 ->
  3588B0(nid=d[022C7FE0]) gen-check via 263FF0 cls-table
  02098E10) -> 263750 -> 265970 blk -> 265020 triple -> 33CA00:
  q[022C7D18]=ctx + 0xB0 copy 022C7D20 + triple 022C7DD0 +
  float 022C7DE0 + d[022C7D10]=1. 326620 ctor: mode0 & map-miss
  -> 30A880(&st,3)=30A8A0(0x22C1788,4,3) per-slot 31B810, &1
  gate's 377C20 UNREACHABLE under mode0 (or-mask must be 0) ->
  d[5AA4]=b[rec+4] -> recursive 326500 (verified 1 level).
  263E30 = ret q[rcx+0x30]. Harness gained ctx4/clstab/g272f0/
  g11e20/nid/slothit fixtures + REAL-entry rargs logging.
  EXP-196 DONE (last three boundaries, 238/238 x3, byte-identical
  result.json): 30C650 level-set real — target clamps 0x63, FOED
  level-row + grwd 02EBF108 per-level growth (2F9A60 HP: 379CD0->863BF0
  MT jitter DOES run, f[09136E4]<0 -> INT_MIN modulus; 2F9B20 MP
  temper%(g*100) verified byte-exact; 2F9BD0 g/128 floats +0x10..1C);
  b[rec+5] suppresses growth+tail, r8&2 tail-only; 31B860 per-level,
  46A690/3B02A0/35D8C0 once at final; serial tail 267330->3A1180
  (02AEF3FC key, 02AEEDC0 stride-0x18 rows, (w8<<9)|7)->2DF220->
  1DBDB0->329210 d[0208D32C]. 323910 grant/revoke real — 323D10
  type arms (b6: 1->324280 cross-slot, 2->324020 popcount, >=4->LP),
  bts/btr b[rec+0x194+id>>3], d[0x190] LP clamp 0, r9&1 silent, e5->
  31B860->3105D0 teardown, rank 324020->30A310->b[lvrow+4] 0xD0..0xE1
  ->300B80->real 3008A0, grade [0x12,0x1E)->308FF0->b[0x20]<=3,
  fed0(rec,0x97). 234DA0 proximity real — 4x 31B810 slot map
  (b[5A5A+i*2]), or-mask+313F60 gate, 3273B0 vs d[022C7FE0] (a5
  suppresses), 265020 triple (b3>>5 in{1,3}), 31E620 d2 vs
  f[pmin]/f[pmax] -> f[pout]+ret1. Fixtures added: grwd/grwrows, mt,
  a11, slotd, oar4, mctxid(022C7FE0). **battle-unit-construction
  scripted set EMPTY — entire call surface executes as shipped bytes.**
  Umbrella SWE2-ORACLE-UNIT-INSTALL-EXEC FINISHED (board rev 29967);
  four OPUS verdict notices consumed + carried into EXP-146/148/149/150
  records (commit 18bb49767). EXP-150..169 records are all committed —
  the old @publication blocker is resolved.
  **EXP-197 owner-check family DONE — 271/271, stable x3, hash
  3281128f; commit a7690cd60; board note rev 31258.** Scope corrected during scoping:
  0017D470 is a 0x14B accessor (d[1D50D0()+0xC20]), not a ctx carrier;
  300FC0/301140/312280 form ONE shared unlink-tail family (~1085B head,
  many callees — next package, do not split); 003BBD00 CRT closure and
  0024FE30 stay scripted; 3112F0 already executed (EXP-149). Promoted
  real in member-block-chain driver: 30B770 global flag composer,
  30B7F0 per-object composer (17D470 x2 -> hi word), 30B9B0 lo-word OR,
  30B8E0 hi-word only, 17D470+1D50D0 (q[01F81428] lazy singleton;
  210EC0/1CCB20 dynamic stubs), 300140 unlink-mark (3105D0 stub gated
  by edx; q[obj]b14 sentinel-gated on w[+0xBA0] 0x113/0x95; d[obj+4]|=
  0x200000), 3299B0+2EB030 msg arm (edx==-1 no-op; ebx=(edx&0xFFF)>=
  0x100?edx|0x5000:edx; node stamp bD&~1/bF5=FF/dEC=0/dF0=ebx;
  b[18]!=1->2EB0D0(node,q[C0],ebx,1,-1f) scripted kb0d0). Fixtures:
  owngl/ownb/g2160/sgl/ent_b/ent_q/row2. bc0-veto/ce0-veto/s530-veto/
  e360-owner-* now drive real composers. Record
  EXP-197-owner-check-family-exec.md; contract auto-status-rebuild
  13f added.
  **EXP-198 unlink-carrier family DONE — 300/300, stable x3, hash
  ad86cdae; commit 67f698dce.** Scope corrected: 0024FE30 is a 0x24B
  kind-nibble dispatch thunk (1->2FD0C0, 7->3B2830, 5/6/9->3B1260,
  .data scans + bc1d0 lock/b4e70 query/bc140 unlock; tables ship as
  zero BSS); 00312280 is EXP/LP guest-share (own package, EXP-199).
  Promoted real: 300FC0 (edx==0 fast path -> 3105D0+3138D0(0); full
  path 310780->2ED180->masks q&FFFDFFE7FFFD/d4&~4->26DAC0/26A330->
  3219D0->2372E0/237260/2373C0/3272E0 -> d[02089340] |0x400/0x200/
  0x800/0x100 + 35C8A0(0xB/0x18/0x17)->d[022C83E8]|2/1/0x10; edx==0
  tail 30D9A0==1 && 31B770(b[5AD5])==obj -> 3138D0(0)+23B040);
  301140 (bail on (d64|d3C)&0x80000003; else inline 300140 unlink +
  2EACD0->3B02A0 + 2E8060 + q6E8 str select by b5 + 2ECF10 +
  3299B0(0x200D) + 319E30 + d[DD0]=32A150()+150 + 3125E0->26DC60->
  2EBB80); 24FE30 + 2FD0C0/3B2830/3B1260 real. Corrections: 322C50
  kind-2 = FOED q[02EBF130] (foed fixture, no separate capd);
  32A150 reads d[0208D45C]; 2367A0 = OBJARR scan w[q[+0x698]+4]==ecx
  gated by 322C50(2); 31B810/31B9F0 validity = kind-0x17 bound id<9
  (slotd unused); null-rec faults proven at 30105A/301150; entry
  addr is never traced; glob table = q[02EBF190] not 02BCF190.
  Scripted boundaries kept: 3105D0/238BF0/311F70/23B040/2ECF10/
  2EBB80/31B8C0/311CF0/313B30/2FEAD0/308270/30C970/319420/319140/
  317E50/321850/327200/2E9780/26D6F0/3E6B40/254850/2548F0/254940/
  36C1D0/36C140/24FE70/426FA0/3B0770/2E9BB0/2EC5B0. Fixtures added:
  imgd/imgq/imgb, oar4 recb/recd/cap, b8c0_ret. Record
  EXP-198-unlink-carrier-family-exec.md; contract 13g added.
  **EXP-199 EXP/LP guest-share DONE — 326/326, stable x3, hash
  cec2549a190ef20429e85ba30649854621750e5dbe1d81bb6815c57f8ddd20d2;
  commit 1c3f2ce8b.** `00312280(rcx=peer,rdx=objrow)` real +
  `00236780` real (= `d[q[02EBF190]+4]>>0xE&1` — same glob block;
  the `02F02190` read was a digit-transpose). Guest scan
  `320AB0(i,3)` -> `glob+8+map*0x1C8` (`map=b[glob+0x5A7E+i*2]`),
  retain iff `(d64|d3C)&0x80000003==0 || 377C20()`, stash
  `q[022C1740+j*8]` cap 9. Per guest: `2F8BB0`/`2F90C0` scripted
  retkeys -> clamps [0,999999]/[0,999]; `b[+0x69]|b[+0x79]&0x10`
  consumes LP (no d190 write, s6a50 edx=0, r12 += lvl*lp*5 into
  source FP); `d[+0x18C]` cap 0x5F5E0FF gated by 236780;
  `d[+0x190]` cap 0x1869F; `2F8F20` level-up loop (measured curve
  L2=169, L3=386, L4=736 — earlier prose table wrong) ->
  `c650(row,lvl,0)` scripted. Source tail: fb80(d[rec+8],exp,lp),
  exp suppressed by 236780; FP = `(b1C2-b88)*d[q[e78]+30]+d[q[e70]
  +30]+r12` -> `max(253690()+c,0)` -> 54EE0/469E80; pos chain
  319490->3180F0->319CA0; 265020 real; 317090 scripted; cookie
  808C40 scripted. Corrections: stash base 022C1740 not 021BB740;
  `lc650` REAL entry was dead (SCR shadows) — removed; e78/e70
  default-mapped. Fixtures: guest={i:{d,b}}, globb={5:0x40},
  glob_null, e78/e70, oar4 "link", SM_NONE, c228. Record
  EXP-199-exp-lp-guest-share-exec.md; contract 13h added.
  **EXP-200 share-formula family DONE — 360/360, stable x3, hash
  bd903eb43fae93068a3dbda1d1e99f6ff6d101c35c46ac168b2e4c781c5fd93a;
  commit 53aeda440.** `002F8BB0`/`002F90C0` real
  + helpers `313800`/`320890`/`264150`; no `20E600` callee reached
  (scope fear unfounded). `2F8BB0`: guest gates (b5==0, `31B860`
  resolve, b4 not [1B,27], flags &0x80000003==0) -> mode split on
  `30D9A0()==1`: member-share `((b1C2-b88)*d[e78+34]+d[e70+34])/ebp`
  signed idiv trunc-0 (ebp = `31B810` member-map count, **`ebp==0`
  -> share 0** — compute skipped entirely); leader path
  `313800->320890->320AB0(idx,1)` member-map row must equal guest
  (rcx==0 takes full undivided). Guest mods `&8`->x2, `&0x20`->0
  on b[6B]/b[7B]. `2F90C0`: `264150()` global gate, guest b4 must
  be 1A/<=6/>=28, NO owner check (unlinked guests get LP), formula
  `(b1C2-b88)*b[e78+2F]+b[e70+2F]` byte-width, no divide; `&0x10`
  -> x2. Finds: flagged-but-retained guests are stashed but paid 0;
  `w[rec+4]` word-match means b5==1 recs never match byte maps —
  objrow never self-counts, linked guests do. `30D9A0` order:
  &8->5,&4->4,377C20->3,&2->2,&1->0/1 (mode1 needs cd_words=[0]).
  Fixtures: e78e/e70e (+34 dword), e78l/e70l (+2F byte), memslots,
  lflag, rcx=("guest",N), cfml. Record
  EXP-200-share-formula-family-exec.md; contract 13i added.
  **EXP-201 display-request queue DONE — 394/394, stable x3, hash
  be5088bdbeac09d363985991df0f0f0c97ba55022f664eea40f939c18ebfc965;
  commit aa29615b7.** `3BBD00` slot allocator (qtab `q[02B457D0]`
  64x0x50 ring, qidx `b[02B443C0]`, cat derive from same-obj
  siblings else `rand()&1`->{1,3}, scale `1.0+(rand&1F)*0.03125` x
  corner pair T@0xD11600 -> d14/d18, ret `al=old|0x20`/`FF` byte —
  upper rax stale cookie), `506700` slot init (t0: `3EFD00` fmt into
  +40 + battle_4_c name; t1: battle_4_p + byte-pair styles; t2:
  `35D330(1A,req+8)` name + flag colour + `2B3050`), `3EFD00` decimal
  writer (signed <=0 -> EMPTY not "-n", returns written width, div
  table 0xD11CE0), `28FBE0` type-0-only subtype dispatch (296280 scan
  -> q[q[0209BE80]+10F78] -> 7-arm jump tab 0x28FC8C), `2FA3B0`
  dist<24.0 gate (`272A0` flag bit refreshes cam cell 01EBBB00 only;
  `265020` class (b3>>5)-1 in {0,2} else zero vec -> dist 0),
  `3284D0` type-2 wrapper, `35D330` blk writer (`31C5D0` ret<0 ->
  memset 98 zeros -> b24 gate passes). IAT stubs: rand (0x8C3098 /
  1CCEF20, randv seq + randn), sqrtf (1CCED52 via 861F14, XMM0 int
  low32). Finds: type-2 calls 35D330 twice; type-2 second scan bumps
  w3A+=3 on every live t2 entry; memset hook now honours dl fill.
  Corrections: not a formatter family — queue registrar; `02089340`
  shared dword (b770 bits vs &10 gate). Fixtures: qt/qtptr/qidx,
  rblk, pos/cam/so3, obj10/rqo/rqv/rqt/rqs, dd7, randv, s31c5d0_ret.
  Record EXP-201-display-request-queue-exec.md; contract 13j added.
  **EXP-202 post wrappers + live dispatch DONE — 407/407, stable x3,
  hash 1a40a8377d79e3b9606c100769cb7ca14f35950620821ffb3dfdc7cc392078a0;
  commit 7926c92cd.** `3283D0` type-0: `edi=r8*2|r9`, subtype byte
  `b[01EED300+(edi+off)*4]` (table 02 04 01 03 06 08 05 07 …), off=4
  iff `(rec==0||b[rec+5]!=0)&&263C20(subobj)!=3`; `d[req+8]=abs(edx)`
  (neg formats positive). `328480` type-1: `b3F=b[req+8]`,
  `24A5A0("battle_4_p")`, `w[0E02780+b3f*2]` byte pair -> `2DD7E0` x2
  -> d0C/d10 (0x80808080 on miss). `28FBE0` dispatch OBSERVED: 296280
  scan table `0209BFBE..0209C2BE` 0xC0-stride (`b[e]|b[e-58]&2`, id
  `d[e+32]`, ret `e-0x7E`) + `q[0209BE80]`->`q[+10F78]` ctrl -> jump
  table `28FC8C`: [0,4]->297040(0), [1,5]->296E90, [2,6]->297040(1),
  [3]->noop; subtype 8 -> idx7 >6 skips dispatch. New fixtures:
  dobjrec, sob (subobj+0xE nibble), ctrl, fbtab. Record
  EXP-202-post-wrappers-dispatch-exec.md; contract 13k added.
  Next: `296E90`/`297040` consumer sinks (proven-fired), or
  `31C5D0`/`2B3050` subtrees.
  **EXP-203 dispatch sinks DONE — 418/418, stable x3, hash
  75bcd73a0257e851d37049ef71a45c45b05f2c9721af858239591ca4e62eb661;
  commit b34b42203.** `296E90(ctrlsub,id)`/`297040(ctrlsub,id,flag)`
  = flag-setters over the ctrlsub 0x160-stride slot array:
  `273320(id)`->idx (still scripted, s273320_ret drives it), idx<0 or
  null ctrlsub bail; `296E90` -> `w[idx*0x160+0x318]|=0x10`,
  `w+0x350=0`; `297040` flag0 -> `|0x20`/`w354=0`, flag!=0 gated on
  `b+0x31E!=3` -> `|0x40`/`w356=0`. All six subtype arms verified by
  real writes (w318 bits 0x10/0x20/0x40 vs untouched). Correction of
  record: EXP-202's d3d0/d480 asserts sat outside the elif predicate
  — vacuous pass in 7926c92cd; predicate now covers
  fa3b0/fmt/bd00/d4d0/d3d0/d480/e690/p7040. ctrlsub alloc 0x40->0x4000.
  Fixture: csb (ctrlsub byte presets). Record
  EXP-203-dispatch-sinks-exec.md; contract 13l added.
  **EXP-204 id->slot resolver DONE — 424/424, stable x3, hash
  fecb4789481a5198988fba27a6374ef61c2652e7db8931ab08a006b702d88b75;
  commit 4f3f6a7d9.** `273320(id)`: id==0 -> -1 pre-scan; else
  `35BB60()` = movsx w[022C8064] signed count (0xFFFF suppresses),
  probes `35BB00(i)` = `d[022C8084+i*0xC0]`, first match -> index,
  miss -> -1; **count re-read every probe**. Cells are BSS (ship
  zero -> always -1 statically); t3320 fixture raises them. d3d0
  cases now plant real packed id 0x1234 via sob+fbtab+t3320.
  Correction: cells are 022C8064/022C8084 (not 02282064 — digit
  slip caught by live probe); distinct from 296280's 0209BFBE
  table. Whole post path now native end-to-end. Record
  EXP-204-id-slot-resolver-exec.md; contract 13m added.
  Next: `31C5D0`/`2B3050` (last scripted edges, type-2 arm);
  Fallback→next: `0023AC80` spawn-record
  init (EXP-152) — harness ALREADY DRAFTED + VALIDATED at
  `C:\Users\Kristian\AppData\Local\Temp\exp152_check.py`
  (**22/22, stable ×3**); record drafted at
  `Temp\EXP-152-spawn-record-init-exec.md`; landing checklist in
  `Temp\exp151_contract_edits.md` (both packages); design note
  `Temp\exp152_design.md`;
  full disasms `Temp\ac80_full.txt`, `Temp\ac80_callees.txt`,
  `Temp\c470_full.txt`. Key executed finds: `326030` snapshots
  slotrow `+0x88` into the `0x5B10` chain at `idx*3*0x34` — the
  exact blocks `327DE0` later scans (40 slots × 3 × 0x34 fills
  `0x5B10..0x7370` exactly); `327CB0` tail-calls `327DE0(rec)`
  BEFORE the snapshot so the same mask/pairs must exist in both
  places; `323790` cap/floor arms unreachable from `23AC80`
  (memset clears `+0x190`, addend is a word); `327CB0`'s
  `b[rec+5]` gate is dead from this caller (==mode byte);
  `23AE68`/`30C4F9` null-resolve arms unreachable (`20E600`
  can't return 0). Faults proven: member-null-desc `0x23ADA8`,
  foe-null-desc `0x23AD7B`, idx>0x27 `0x326057`, glob-null
  `0x327E27` (inside `327DE0` via `327CB0` tail). Scripted
  boundaries: `30C650`/`30FED0` (EXP-148 bodies), the
  `30F690`/`30F340`/`30F5A0` recursive cluster, `323910`,
  `324100`, `317930`, `318B40`, `30F9A0`/`30C410`,
  `31B860`/`324470`. **EXP-153 candidate — stat recompute
  cluster:** `30F690`/`30F340`/`30F5A0` real + `377C20`/`3105D0`
  real inside. Recursion resolved: only `30F340` self-calls
  (`0x30F477`, gated on a local flag reg — clean rec terminates);
  `30F690(rcx,edx=bitmask)` bit-iterates handlers incl `377C20`/
  `3105D0`; `30F5A0` reconciles `w[+0x28]` vs `w[+0x4C]`.
  **CORRECTED call sets (earlier lists leaked past ret):**
  `30F5A0`(82i)={300BC0,300CE0}; `30F690`(~60i)= bit0 fixup via
  `31B860`+`377C20` (clear `q[rdi]` bit26 unless can-die) then
  `30E360(rec,bit)` per set bit + `30FED0(rec,0x217)`; `30F340`
  (**119i to 0x30F4AD**)={300530,self,30F5A0,30F690,31B860,320AB0,
  3243F0} — dispatch mask `ecx | (r14d?0x544:0)`; `ecx|=rip-global`
  when `r12d`. **Sibling `30F4B0`** (67i)=`30F3F0(edx)` then same
  triple dispatch on `dil` bits (1→self,2→5A0) — separate entry.
  Leaf sizes: 30E360~342(cookie,self-rec,indirect call rax),
  300530~255, 300CE0~117, 300BC0~65, 30F3F0~58, 3243F0~38
  (3105D0+313F60+300E40+2E42D0+2699D0+2ECEC0 unlink/release),
  30B0E0~14 (guard-prefix, jne falls into 30B106 sibling),
  31B7E0~12 (b[rip]&0x10→3588B0→263E30 — EXP-151 chain, real),
  31B860~9+ (null→0 resolver), 320AB0~7 (31B9F0→bound 0x27),
  320A40~4 (cl>0x27 guard-prefix into sibling). **EXP-153 design:
  extend exp152 harness** — `30C470` calls `30F690(rdi,
  d[0208D320]|d[0208D324])` at 0x30C59D (global dirty-mask pair),
  `30F340` at 0x30C5A5, `30F5A0` at 0x30C5AD, all on `rbx=rec` after
  the `ror [rcx+0x18C83],0` barrier-op. Promote `30F690`/`30F340`/
  `30F5A0`/`31B860` real; add `377C20`-chain + `3105D0`/`3243F0`
  (inners scripted) as needed; `30F340` is ONLY ~60i ending 0x30F3EB
  (flags `d[+3C]|d[+64]` → bt0x10 clamp `d[+48]`≥1 / bt0x1C double
  `d[+24]` → delta → `300530(rec,delta,0,0x217)`); `30F3F0`/`30F4B0`
  are the per-slot broadcast wrappers — only reached via other
  callers. **EXP-153 EXECUTION-VALIDATED in Temp:
  `Temp\exp153_check.py` 37/37 stable x3** (23AC80 integration cases
  + 15 direct-call cases). Real layer adds `30F690`/`30F340`/`30F5A0`/
  `31B860`+`236850`/`236820`/`377C20`-chain(4); new scripted:
  `30E360`,`300530`,`3243F0`,`300BC0`,`300CE0`. Proven semantics:
  `30F690(rec,mask)` bit0 fixup = `31B860(rec)` owner scan (row's
  `q[+0x698]==rec`) -> `d[rec+0x64]|d[rec+0x3C] & 0x80000003` ->
  `377C20()`==0 -> clear bit26 of `q[row]`; `30E360(rec,0,bit,0)` per
  set bit; `30FED0(rec,0x217)` tail ALWAYS (mask=0 included).
  `30F340`: flags `d[+3C]|d[+64]` bit0x10->computed max(d[+48],1),
  bit0x1C->d[+24]*2, else d[+24]; computed!=stored -> (b5==0 && idx in
  [0x1B,0x27] && stored<=0 -> `31B860`+`3243F0(row)` unlink) then
  `300530(rec,delta,0,0x217)`; equal->ret. `30F5A0`: sec1
  (b[+6C]<0||b[+7C]<0 ? 0 : w[+28]) vs w[+4C] -> `300CE0(rec,delta,
  0x217)` + over-w[+6] clamp `300BC0`; sec2 `b[+37]*w[+28]`(b37=0->w28)
  vs w[+6] -> `300BC0`. edx deltas are 32-bit writes.
  **EXP-154 candidate — `30E360` per-bit core (342i, mapped):**
  sig `30E360(rec, arg2, r8=bit, r9, arg5, arg6=mask, arg7=op)`;
  `edi=1<<bit`; owner via `31B860`x2; arg6 `0x217`: `&1`->skip
  owner checks (`30B9B0`/`30B8E0`), `>>1`/`>>4` complements ->
  gate flags; `d[+0x4c]`=pre-transition bit state; owner
  `b[+5]==0 && b[+4]in[0x1B,0x27]` + `edi&0x80000003` ->
  `300FC0(row)` unlink; `377C20` can-die: ret==0 BAILS the whole
  body. **arg7 = 6-arm jump table `0x30E88C`** = {clear-if-set,
  set-if-clear} x flag dwords {+0x38,+0x3C,+0x64}; no-op
  transition -> ret. Post-transition: `d[rec+0xBC+bit*4]` = r9
  (or `387730` when r9<0); `w[rec+0x13C+bit*2]` = arg5 (or
  `3876D0`); then cmovne pairs `(edi?386A50:386A70)` +
  `(edi?46A800:16D6A0)`; `386A70` special-cases edx==0x1C
  (`d[+0x24]=(d[src+0x48]+1)>>1`, `d[+0x2C]|=0x108`). Cascade:
  self-recall with `arg6|bit9`, arg7 forced 0 (clear `d[+0x64]`).
  30F690 calls it `(rec,0,bit,0,0,0x217,0)` -> arm0.
  **30E360 EXECUTED standalone: all 6 arms verified** — clear/set
  edge-gated (no-op bail), `d[+0x58]`=arg7 in{0,3} enables per-bit
  array writes `d[+0xBC+bit*4]`=r9 / `w[+0x13C+bit*2]`=arg5,
  `d[+0x44]`=arg7 in{3,4} selects `386A50`/`386A70` + `02EBF118`
  desc per-bit cascade rows (`d[row+0xC]` follow-on mask ->
  recursive 30E360, observed bit4 cascade-clear); arg6 `0x217`
  decodes notify gates `d[+0x5c]`=~(>>4)&1, `d[+0x60]`=~(>>1)&1
  (0x217 clears both), `&1` skips owner checks. Direct-entry
  fixture: retaddr@rsp, args at rsp+0x28/+0x30/+0x38 (entry rsp is
  8 above a real call's).
  **EXP-154 VALIDATED: Temp\exp154_check.py 53/53 x3** — 30E360 real
  + handler pair (386A50/386A70/46A800/16D6A0) + 3848E0 block-reset
  + 387730/3876D0 resolvers real; arm bodies (301140/312280/3299B0/
  300140/307D10/3284D0), owner checks (30B9B0/30B8E0), 300FC0,
  3112F0, 2FA390/46AB10 scripted. Post-block gate `al&0x4C`
  restricts array writes + handlers to arms 0/3 (the +0x64 dword).
  Second jump table (sel@0x30E8C4, off@0x30E8A4) = per-bit arm
  dispatch when owner row != 0: bit0/1/0x1F -> unlink (301140 |
  3299B0 msg + 300FC0+312280), bit2/8 -> b[rbx+0xE9A] writes,
  bit4 -> 3299B0(0x2001), bit5/1B -> 300140+307D10. arg6 bit1 ->
  d[+0x60] gates call-rax pair-2; bit9 -> skips tail fed0.
  3876D0 formula: b[row+9]*d[0x1DFE0B4]*0x1E (mul cell verified
  live). 386A70's 0x1C special writes the 0x148 stack block,
  not rec.
  **EXP-155 arm-body map (static, scripted boundaries now named):**
  `301140` = despawn/death teardown — bails unless `d64|d3C &
  0x80000003` == 0 (the engaged mask, same as 300FC0's check);
  `2E9600(obj)` + `311F70` gate -> `238BF0` release -> `3105D0`
  unlink -> ~15 field clears (`q+0x6F8`, `d+0x748/0x770/0x750/
  0x74C/0x788/0x6B0/0xDCC/0x30`) + flag masks (`q0 &=
  0xFFFFFFFDFFE7FFFD & 0xFFFFF8FF`, `d4 |= 0x200000`, `d0 |=
  0x40000000|0x1000000`) -> `2EACD0` + `2E8060(obj)` ->
  anim/name ptr select by `b[rec+5]` -> `2ECF10` (EXP-148
  proven) -> `3299B0(rbx,0x200D,0)` post -> `319E30`/`32A150`/
  `3125E0`/`26DC60(obj,res==0)` + float timer `d[+0xDD0]`.
  `312280` = mode-path cross-ref: validates `q[obj+0x698]` member
  rec (`b[+5]==1`) + `b[src+5]==0` foe -> `317ED0`/`3171C0` ->
  correlates `d64|d3C` bit1 with `b[obj+0xE9A]` bits (the flags
  e360's bit2/8 arms write) -> table loop `r13=0x30B740`.
  `3299B0(row,msgid,val)` = post msg to `q[row+0x10]` obj via
  `2EB030` (`(id&0xFFF)>=0x100` -> `|=0x5000` recompose; remembers
  id `d[row+0x5C]`); msgs sent by e360 arms: bit4=0x2001,
  bit1=0x200C, bit0x1F=0x200E, teardown=0x200D. `3284D0` =
  `2FA3B0(obj,bit)` gated notify (edi&&d5c&&rbx).
  **EXP-155 scoped — stat apply pair `300BC0`/`300CE0`:** `300BC0
  (rec,delta,notify)` = HP apply: owner row `31B860` -> unless
  `notify&1`, scripted `30B770`+`30B7F0(row,0)` pair can veto ->
  `w[rec+6] = clamp(movsx(w6)+delta, 0, cap)`; cap =
  `b[+0x6C]<0||b[+0x7C]<0 ? 0 : (b[+0x37] ? w[+0x28]*b[+0x37] :
  w[+0x28])` -> `30E060(rec,notify)` tail. `300CE0` (117i) = the
  parallel `w[+0x4C]` apply incl `2FA540` + `300D34` sibling.
  `30E060` (63i) = notify inner: `31B860` + `3283D0`(->`2FA3B0`)
  + `16D6A0` ret-sink. `300530` (255i, ~10 sibling calls) stays
  deferred — own package. `3243F0` self-recurses. Candidate
  scripted: `30B770`/`30B7F0`/`28F1F0`/`2FA540`/`2FA3B0`/
  `300D34`(87i, maybe real).
  **EXP-155 VALIDATED: Temp\exp155_check.py 68/68 x3** — 300BC0,
  300CE0, 30E060, 3283D0 real (+16D6A0 ret-sink); scripted:
  30B770/30B7F0 (veto pair), 28F1F0 (gauge event), 2FA540 (drop),
  2FA3B0. Executed semantics: `300CE0` decodes notify bits
  (r13=~(>>4)&1 -> 3283D0 owner msg, r15=~(>>7)&1 -> 28F1F0 gauge
  post, &1 skips veto, delta<0 re-vetoes hi-word); positive delta
  cascades 300BC0 (heal hits both gauges); drop -> 2FA540.
  **Correction to EXP-153's model: 30F5A0 sec2 computed =
  b37 ? b37*w28 : w28 (scale defaults 1), same cap as 300BC0** —
  proven: w6 0->50->100 with b37=0. `30E060` computes w6/w28
  fraction, caches b[+0x4E], posts delta+sign via 3283D0 when
  notify&0x410==0x400; 16D6A0 call is a literal no-op stub
  (dummied-out notify).
  **EXP-156 VALIDATED: Temp\exp156_check.py 77/77 x3** — the
  broadcast wrappers + their whole resolver chain promoted real:
  `30F3F0`/`30F4B0`/`30F4D0`, `320AB0`, `31B9F0`, `322C50` (0x17
  arm = bound 9 member slots), `30B0E0` + its shipped cls-0xC
  callback `2FD970`. Executed semantics: `30F3F0(flags)` loops 9
  member slots -> `320AB0(slot,3)` -> `31B9F0` = `322C50(0x17,slot)`
  bound-9 gate -> `b[glob+slot*2+0x5A7E]` rec-idx map -> `q[GLOB]+8+
  idx*0x1C8` row. `30F4B0(x,flags)` = f3f0 + tail `30F4D0`: 13 foe
  slots, id `((i+0x12)&0xFFF)|0xC000` -> `30B0E0` class-descriptor
  table `0x1EEBCC0` (0x58 stride, 16 rows): `(id&0xF000)>0xE000` or
  `(id&0xFFF)>d[row+0x3C]-1` -> invalid; else `q[row+0x50]` validator
  cb (shipped = `2FD970` for cls-0xC: mode-0 arm = spawned-bitmap
  test `bt w[q[row+8]+(idx>>4)*2], idx&0xF`; q[row+8] is
  runtime-populated — planted in fixture, disclosed). Then
  `320A40(i+0x1B)` = direct `q[GLOB]+8+(i+0x1B)*0x1C8` row.
  **Mask semantics (byte-verified, corrects earlier summary):**
  mask = (flags&4 ? d[0x208D320]:0) | (flags&8 ? d[0x208D324]:0) |
  (flags&0x10 ? 0x544 : 0) — the `0x544` default is gated ON by
  bit4, and the gate cells are the SAME 0x208D320/324 pair as
  30C470 (earlier 0x1E8D3xx addresses were a hex slip). `30F690`
  has a null-rec guard (`test rcx,rcx;je`) so unmapped member
  slots (map=0xFF -> idx>0x27 -> 0) are silent skips, no fault —
  observed: slot3 unmapped -> e360 count drops 36->32, fed0 9->8.
  `f4b0` edx=flags; trace-verified 9 member + 13 foe iterations,
  bitmap-skip case (0x000C -> ids 0x12/0x13 only) resolves 2/13.
  Scripted boundaries unchanged (30E360 jt2 arm bodies etc.) —
  the only fixture-only state is the runtime bitmap pointer.
  Next candidates: `300530` (255i stat apply) or `3105D0` unlink.
  **EXP-157 VALIDATED: Temp\exp157_check.py 86/86 x3** — `300530`
  (222i, ends 0x30089F; the `0x3008A0` id-resolver is a SIBLING,
  not part of the body) real + leaves `316D70`(15i), `32A150`(2i),
  `306F00`(41i->`263D30`/`2360D0`), `469BB0`(21i->scripted
  2FA390/46AB10). Executed semantics: `300530(rec, delta, arg3,
  notify)` — `r14 = d[rec+0x48] + delta` (**arg2 is a DELTA onto
  the stored stat**, not an absolute); floor = `d[ownerrow+0x48]`
  (0 w/o owner); cap = `d64|d3C&0x10000 ? max(d48,1) : d[+0x24]`
  (x2 when flag bit 0x1C) — proven: 510->100, bit1C -> 200.
  `r12 = delta>0 (or notify>>5&1 when delta==0)`. notify bits:
  `&1` skips `30B8E0` veto, `&4`+`&0x40` gate the `3299B0(owner,
  r13+0x2005)` stat msg, `>>4`/`>>7` complements gate `3283D0`/
  `28F1F0`. **Engaged-bit protocol**: delta>0 && OLD d48<=0 ->
  `e360(rec, arg3, bit0, 0, 0, notify, arm0)` clear; delta<=0 &&
  NEW d48<=floor -> `e360(rec, arg3, bit0, -1, -1, notify, arm3)`
  SET (r9=-1 -> 387730 resolver); else 3299B0 notify only.
  Proven: floor-hit sets `d64|=1` (s530-floor), revive clears
  (s530-revive), veto (s530-veto kb8e0=1 skips write).
  f340-* asserts rewritten: `30F340` calls `300530(rec,
  computed-stored, 0, 0x217)` -> d48 lands on computed.
  Next: `3008A0` id-resolver (class-desc `q[row+0x48]` callback
  2FD420, target-class flag writes) or `3105D0` unlink.
  **EXP-158 VALIDATED: Temp\exp158_check.py 102/102 x3** —
  `3008A0(id, delta, mode, dispatch, flag)` real + `309F30`
  (shared validator dispatch: mode==4 -> direct `2FD970`,
  else `jmp q[row+0x50]` validator), `2FD420` cls-C spawn-bitmap
  MUTATOR (`q[row+0x48]` slot = write+notify; `+0x50` = query),
  `325F40` notify router, `309440`, `46A630` real; `252E60`
  scripted (19-call batcher `2CD650` inside). Semantics:
  mutator computes `ecx = mode==0 ? oldbit+delta : delta`;
  `ecx<0`->btr, `ecx>1`->bts, else `ebx=mode==0 ? old+delta :
  delta` -> btr if 0 else bts -> writes bitmap word ->
  `325F40(id, old, new)` (cls-C foe ids fail `322C50(1,id)` ->
  early ret, no notify) -> `mode==0 && flag&1` -> `46A630(id,
  delta)` -> scripted `46AB10(ecx=0, edx=0x24/0x25, stk)`. Ret =
  ebx (new bit state; -1 on the ecx<0 direct-clear path).
  **Dispatch arm (`r9==1`)**: needs `309F30(id,1)`<=0 (not yet
  spawned) AND mutator ret >0 -> `q[0x2EBF190]+4` state-object
  flags: cls3 `|=1` + `20E600`-walked mask `tbl[(w[rbx+0x2C]&7)]`,
  cls4 `|=0x40`, foe id<=0xC011 `|=0x80`, foe 0xC012..0xC01E
  `|=0x100`. Proven: set/clear/neg/mode/flag4/foeflag variants,
  all four id-validation rejects (0xFFFF/0x1000/>0xE000/oob ->
  -1, no callback). So `3008A0` = spawn-bit update + active-set
  registration. Next: `3105D0` unlink, or jt2 arm bodies
  (`301140` despawn teardown -> `3105D0` already mapped).
  **EXP-159 VALIDATED: Temp\exp159_check.py 109/109 x3** —
  `30FED0(rec, notify)` stat-change dispatcher real + `2FEF30`
  walker real (139i exercised on base rec; member path hits an
  authentic null-row fault at `0x2FF1FC` — disclosed boundary).
  `30FED0` structure: (A) desc-walk `q[0x2EBF130]`(FOED) ->
  `20E600`x2 -> row `w[desc+8]*b[rec+4]+eax` -> `d[row+0x50]`
  watch-bitmask -> seeds stack bitmap rsp+0x40; (B) `b[rec+5]==1`
  member -> `31B860` owner -> seed from `b[owner+0xE80+bit/8]`
  (128 bits); (C) field-snapshot XOR loop writes changed/cleared
  maps rsp+0x50/+0x60; (D) 128-iter dispatch: watch bit i ->
  `30E130(rec, i, 0, notify)` (scripted — calls `30FED0` back);
  (E) `2FEF30(rec,0,0)` tail walker; (F) b5==1 again ->
  `31B860` -> `d[owner+0xE90]` 32-bit loop -> `30E360(rec,0,bit,
  ...)` clears. **No null guard**: `test rcx` bail lands AT the
  loop entry `0x310071`, not a ret — null rec faults at
  `0x310080` reading `w[0x50]` (f690 owns caller-side guard;
  expect_fault documented). Proven: watch bits 0/2/7 each ->
  m30e130(rec,bit,0,0x217) scripted intercept; null fault;
  member fault boundary. Scripted: `30E130`, `2F8E50`, `2F9180`,
  `3112F0`, `3279B0`, `252E60`. Also discovered: `300280`
  (inside `3105D0` unlink) calls `3008A0` — unlink deregisters
  through the EXP-158 resolver. Next: `30E130` (149i per-bit
  handler, call rax x2 + 3112F0/3279B0 + fed0 recursion) or
  `3105D0`/`301140` teardown chain.
  **EXP-160 VALIDATED: Temp\exp160_check.py 117/117 x3** —
  `30E130(rec, bit, arg3, notify, arm)` per-bit edge handler real:
  arm0=clr `b[rec+bit/8+0x68]`, arm1=clr `+0x78`, arm2=set `+0x68`,
  arm3=set `+0x78` (edge-gated; no-op transitions bail). Bound =
  `322C50(0x1D, bit)` vs `d[q[0x2EBF040]+4]` (runtime cell —
  planted 0x80). On transition: `861EC0` memset 0x148 blk ->
  `call rax` pair `386A50`(clr)/`386AE0`(set, +384B10 scripted) ->
  `b[rsp+0x7C]&1` -> `3112F0` blk-notify -> `~(notify>>1)&1` ->
  pair `46A720`/`46A790`(->46AB10) -> bit in [0x68,0x71] ->
  `3279B0(rec, armset?1:-1)` -> `notify bit9==0` -> recurse
  `30FED0(rec, notify)` (fed0's own |0x202 sets bit9 -> bounded).
  arms 0/2 also call `30EA40(rec,bit,arg3)` (->20E600 x2 +387020).
  fed0-watch/watch2 now drive REAL e130 (he130 tags). Scripted:
  384B10 (indirect call), 3112F0, 3279B0, fed0-inbound (stale
  boundary kept — 6 asserts consume it). Next: `3105D0`/`301140`
  teardown, `30EA40`+`386AE0` already real, or `2FEF30` deeper
  arms (member path fixture gap at 0x2FF1FC).
  **EXP-161 VALIDATED: Temp\exp161_check.py 122/122 x3** —
  teardown chain real: `301140(rec)` despawn entry (102i) +
  `3105D0(rec)` unlink/reset (83i) + `300280` -> `3008A0`
  **loop closure proven live** (u300280 -> a08a0 -> l9f30 in
  `u5d0-base` trace — unlink deregisters through the EXP-158
  resolver). `301140` semantics: entry gates on
  `(d[objrow+0x64] | d[objrow+0x3C]) & 0x80000003` — the engaged
  mask; null `q[rec+0x698]` faults at `0x301150` (no guard).
  `2E9600(q[rec+0x10])` object inspect -> `311F70` only when
  ret==0 AND `d[rec]` bit `0x1A` CLEAR (bt/jb polarity proven
  both ways). Then `238BF0` (scripted 235i) -> `3105D0` real ->
  field clears `+0x6F8/+0x748/+0x770/+0x750/+0x74C/+0x788&~0x400/
  +0x6B0&~2/+4|=0x200000`, `w[+0xBA0] in {0x113,0x95}` spares
  `btr q0,0xE`. `2EACD0(d[+8],1,rec+8,0x7B)` tail-jmps into
  `0x3B02A0` (0xCA0-frame wait/dispatch spinning on `24F610`
  list lookups — cross-thread boundary, scripted). `2E8060`,
  objrow+5 mode byte -> `q[rec+0x6E8]` rodata ptr select,
  `2ECF10`, `3299B0(rec,0x200D,0)` despawn post (scripted),
  flag pass `q0&=0xFFFFFFFDFFE7FFFD | |=0x1000000`,
  `d[rec]|=0x40000000`, `d[+0x74]=-1`, `319E30`, `32A150`,
  `d[+0xDD0]=eax-5*cvttss2si(f*f)` timer recompute, `3125E0`->
  `30D9A0` (`d[q[0x2EBF190]+0x5B04]` state cell), `26DC60`->
  `2EBB80` leaf, `d[+0x30]=0`. Fixture disclosures:
  `q[0x209BE80]` -> 0x12000 object registry (`290B90`/`290DF0`
  walk +0x10Fxx lists; null slots early-out — `290DF0` stays
  scripted as safety), `q[0x2EBF190]` -> 0x6000 state cell,
  `q[rec+0x10]` object, bidirectional `+0x698` link. Scripted:
  `311F70`, `238BF0`, `0x3B02A0`, `3299B0`, `336710`, `33E1F0`,
  fed0-inbound. Next: `2FEF30` member-arm fixture, or
  `311F70`/`238BF0` teardown callees (105i/235i).
  **EXP-162 VALIDATED: Temp\exp162_check.py 126/126 x3** —
  `238BF0(rec)` promoted real (was `301140`'s scripted 235i
  callee). Guards: `rec`/`q[rec+0x10]`/`q[rec+0x698]` nulls
  bail. `b[objrow+5]` mode byte: `0` -> `q[rec+0xE60]`
  equip-table `w[+0x7A]` float normalize + `b[objrow+4]` class
  byte `(al-0x1B)<=0xC` -> `269F30(obj,3,8)` else
  `(obj,2,1)`; `1` -> member path `q[rec+0xE68]` `w[+0x10]`
  float, `q[rec+0x6A0]` bit `0x20` -> `267CC0`+`26B4A0` else
  `b[rec+0x58]` dispatch (`4`->write 1, `1`->`2659A0`+
  `25D5E0`). Shared detach chain on `q[rec+0x10]` all real:
  `269FE0/2E5FD0/26DAC0/2EC5B0/26A430/26A3A0/2E8220/269F20/
  2E8A10/26AD00/2361B0/26A7F0/26A7C0/269E20/236210(member
  arm: e68+0x18 bits 0x10/0x20/0x40 -> 3204D0(rec,6,&out))/
  26A330`, tail `312700(rec)` scripted (246i dispatcher).
  Fixture adds: `q[rec+0xE60]`/`+0xE68` blocks, `q[rec+0x6A0]`
  flag byte, `b[objrow+4]`/`+5`. `u1140-*` re-proven with
  238BF0 real inside 301140. Next: `312700` (246i tail
  dispatcher), `311F70` (105i), or `2FEF30` member-arm
  fixture gap.
  **EXP-163 VALIDATED: Temp\exp163_check.py 131/131 x3** —
  `312700` is a 12i WRAPPER (`3125E0` -> `26DC60` -> `2EBB80`;
  the 246i jump-table body at `0x312730` is a sibling — a
  `0x4000..0x4035` opcode dispatcher, separate package).
  `311F70(mode, rec, arg3)` real: `30D9A0` state code ->
  `336E40` fills caller-frame transform struct (scripted +
  `n336_fill` hook writes caller `rsp+0x60..0x78`) ->
  `265020` reads obj pos -> `ucomiss`x3 vs struct
  (difference OR unordered-NaN -> `263F40`->`26B0C0` write;
  both directions + the 0xCD-garbage unordered arm proven) ->
  `movups` quad -> `rec+0xD0`/`+0xE0` -> `392170` ->
  member arm `arg3!=0 && b[objrow+5]==1` -> `movups`
  `q[rec+0x6A0]+0x50` (fill[0]=9.0f proven) -> `q[rec]|=
  0x4000000` -> `d[+0x15C]/+0x160` = struct scalar (fill[4]
  =5.0f proven) -> `263F40`->`26A0D0`, `26B620`->`26B6A0`,
  `808C40`. Inbound `311F70` on `301140` callsites stays
  scripted (fed0-style boundary); `312700` real inside
  `238BF0`. Next: `336E40` (346i struct-fill body — its
  semantic content is the remaining unknown), `312730`
  opcode dispatcher (37 arms), or `2FEF30` member-arm.
  **EXP-164 VALIDATED: Temp\exp164_check.py 132/132 x3** —
  `336E40` promoted REAL (was the `n336_fill` scripted
  boundary). ctx layout: `d[ctx+0]=sete(30D9A0()==1)` BOOL
  mode flag (only arms 0/1 reachable via 311F70),
  `q[ctx+8]`=arg0 aux obj, `q[ctx+0x10]`=arg1 obj.
  `30D9A0` full decode: `cl=d[q[0x2EBF190]+0x5B04]` ->
  cl&8->5, cl&4->4, 377C20()!=0->3, cl&2->2, else cl&1.
  `377C20`: `3148F0()` idx -> `q[0x2ADD100]` 3-byte-stride
  table; null/OOB -> `0xFFF>>0xF`=0 else word bit15.
  Null-aux arm: kind accessors `2646C0`/`265200`/`265090`
  (`b[obj+3]>>5` -> `q[obj+0xB8]` node, floats +0/+0x50/
  +0xA8) all real. Aux arm: `202F00` 4x4 matrix copy ->
  CRT stubs `861F08`/`861F0E` (jmp q[IAT] — scripted) ->
  `383F10` zone lookup `d[q[0x2AEDFB0]+0x20]` null-global
  fault (expect_fault 0x383F23, disclosed). Mode-1 arm
  (aux+d[ctx]==1): `265090`->`309AE0`->`259B10` (0x110-
  stride table +0x90/94/98) -> `203080`->`4687F0` ->
  `call q[IAT]`@0x3370D2 -> wild exec, deterministic
  fault 0x1CCEF20 (expect_fault, disclosed). `32A790`->
  `26E350`->`231900` stays scripted. `posw` strengthened:
  planted obj pos flows through the REAL gather -> equal
  -> no write. Next: `312730` opcode dispatcher (37 arms),
  `231900` (92i inside 26E350), `2FEF30` member-arm gap,
  or the aux-arm zone-context fixture (`q[0x2AEDFB0]`).
  **EXP-165 VALIDATED: Temp\exp165_check.py 140/140 x3** —
  `312730` = transform/position OPCODE DISPATCHER (the EXP-162
  "246i body" — wrapper is `312700`, sibling is real).
  `312730(rec, cmd={w op,w arg}, out1, out2, a5=outf)`:
  `xmm6=maxss` via `265090`; `0x4000..0x4025` -> 2-level jump
  table `b[0x312B10+i]`->`d[0x312AF8+idx*4]+0x120000`;
  `0x4026..0x4035` -> `2367A0` entity scan (global rec array
  `q[0x41E6688]` 0xF50-stride, `w[q[row+0x698]+4]==sel` match,
  resolved a shipped row -> `30A130` -> null `+0x10` fault,
  authentic); `0x4124/25/4A/4E/65` singles (owner quads,
  `319850`). `312DF0` = position SCATTER loop: `3DFD00` group-0
  seed row (0x30-stride, subop=rowidx), 9 iters of `328370` RNG
  `(rand%(2*arg+1))-arg` x/z jitter -> `317DE0` validate ->
  `337700`/`3377C0`; ret 0=found/-2=exhausted/-1=no seed.
  `0x4020` member arm seeds from `q[rec+0x6A0]+0x50` — the
  SAME quad 311F70 mirrors. Shared boundary found: `383F10`
  zone lookup faults on null `q[0x2AEDFB0]` (zone-context
  global) — blocks ALL position-validation paths (EXP-164 aux,
  both scat arms). Next: plant the zone-context object to free
  3 fault boundaries at once, or `231900`, `2FEF30` member-arm.
  **EXP-166 VALIDATED: Temp\exp166_check.py 143/143 x3** —
  zone-context fixture landed; `383F10`/`391410`/`3912E0`/
  `382D10`/`384130`/`231400`/`233050`/`233110`/`230A40`/
  `2324F0`/`22F830`/`22F8B0` all REAL. `383F10` = navmesh
  cell->link lookup: zctx `{+0xC verts, +0x10 linkdescs,
  +0x18 celltab, +0x20 grpdesc}` via `20E600`(elemb+off);
  grid bounds -> cellid -> per-cell link bytes -> `382D10`
  triangle winding test (static ring 0xD112B0) -> ret linkid.
  `391410`/`3912E0` = layer occupancy scan on globals
  `0x2AEE060..0xB9` (hand-derived RIP-rel slip: `0x2AEE0A8`
  not `0x2AEB0A8` — all recomputed by tool). `337700` full
  validator: `265090` y (KIND-3 only, `b3&0xE0==0x60` ->
  `3DA710` on `q[obj+0xB8]+0x50`) -> `391410` -> `383F10` ->
  `336390` 5-point footprint (`32A6A0`->`26E100`->`231400`
  entity-grid ctx `q[0x209A670]`/`q[0x209A678]`: `233050`
  pos->cell w/ odd-col stagger, `233110` row select,
  surface solve, `22F830` span query) -> eax!=0 accept.
  t2730-accept: **eax=1 accepted spawn** (pos in tri ->
  all probes pass). t2730-scat empty-link -2 exhaust;
  outside-tri reject x9; nozone expect_fault 0x383F23.
  CRT band `0x861EC0..0x862090` mapped by import name:
  memset/_fdclass/cosf/sinf/sqrtf/tanf/atan2f/asinf —
  host-computed via MATH hooks (disclosed, not bit-exact);
  rand stubbed deterministic. BONUS: t1f70-aux/mode1 now
  run the full 24-node transform chain real (cosf/sinf/
  sqrtf x24, z383f10 x48) -> `q[rec]|0x4000000`,
  `d[rec+0x15C]=0x3FC912DC`~pi/2. Next: `231900`
  (92i in 26E350), `2FEF30` member-arm, `22F830`-deep
  sector/occupancy semantics.
  **EXP-167 VALIDATED: Temp\exp166_check.py 144/144 x3** —
  `32A790` scripted boundary removed: it's a `jmp 0x26E350`
  trampoline. `26E350` = walkable-surface snap on the same
  egrid ctx (`q[0x209A670]`/`+0x678`): `231900(ctx,pos,1)`
  best-row find (`233050` cell, ridx span, `f[row+4]>0.001f`
  gate, `bt mask,(d[row+0xC]&7)`, `2324F0` eval negative=
  usable, `231890` plane solve, max-select) -> `231820`
  WRITES `f[pos+4]` = snapped height. `t26e350` proves the
  write: pos.y 99 -> 0. `t1f70-aux`/`mode1` now run the
  chain real x2 per arm. All `231400`-commit bodies tagged
  (`z230a40`/`z2324f0`/`z22f830`/`z22f8b0`).
  **EXP-168 VALIDATED: Temp\exp166_check.py 149/149 x3** —
  the five remaining `312730` opcode arms execute real.
  Key fix: the shared resolver gate cell is `0x2089340`
  (the `test byte ptr [rip+disp],imm8` is 7 bytes, not 8 —
  earlier notes had `0x208B340`/`0x2089341`, both off;
  proven by UC_HOOK_MEM_READ trace). `31B7E0`/`31ABE0`/
  `3272A0`/`3272F0` all gate on `b[0x2089340]&0x10` then
  `3588B0(id)` -> cls `id>>0x10&0xF` (<5), idx `id&0xFFFF`,
  gen `id>>0x14&0x7FF` -> `263FF0(cls)` = `0x2098E10+cls*
  0x288` desc `{q+0 base, q+8 rowptrs{count,ptr..},
  b+0x10&1, d+0x20 count}` -> bounds+active+`w[row+0x16]
  ==gen` -> `263E30(row)` = `q[row+0x30]` resolved rec.
  Arms: `0x4022` (foe: `b[objrow+5]==0`, owner via
  `31B7E0(d[rec+0x24])`, out1=`rec+0x120`, out2=owner
  `+0xD0`, outf=`309B10+309A90`); `0x4024` (`3272A0`:
  `3590D0` leader id `d[0x22C7FE0]` — second off-by-one
  corrected — -> resolve -> `b[rec]&8` gate -> shared
  `0x312918`); `0x414A` (`31B7E0` -> same `0x312918` shared
  body, `30A130(found)` scale); `0x414E` (`31ABE0(
  d[rec+0x710])` -> `265390(row)` kind3 node decompose ->
  out quad, `d[outf]=0` written by the arm); `0x4125`
  (`312DF0` seeded `rec+0xD0`, arg `0x14`, `edx=-1` ->
  `3377C0` validator variant — which itself calls `337700`;
  9 real iters + `31abe0` x9 inside the loop -> exhaust ->
  reject). All five resolve/callee chains real:
  `t31b7e0`/`t31abe0`/`t3588b0`/`v263ff0`/`u263e30`/
  `t309b10`/`t309a90`/`v30a130`/`t265390`/`n3272a0`/
  `v3590d0b`.
  **EXP-169 VALIDATED: Temp\exp166_check.py 153/153 x3** —
  `265390` full kind-dispatch executed: kind1 (`b3&0xE0==0x20`)
  node `+0x10..+0x18` triple; kind3 (`==0x60`) node `+0/+4/+8`
  + optional `q[row+0xC0]` `{f+0x140,+0x144}` y-add +
  `b[node+0x107]&1` `{f+0x40..0x48}` triple-add (proven
  `11.5/14.5/15.5`); default zeroes all three outs.
  **`0x4125` accept proven** (`t2730-4125a`, eax=1): seed
  `rec+0xD0`=(16,5,16), arg 0x14, iter 7 candidate (7,5,15)
  passes winding + full 5-probe footprint -> `312DF0` ret 0
  -> success epilogue; `outf`=4.0 via `xmm6`/`265090` kind3
  `f[node+0x50]`. New fixture `erowall` (ridx span {0,1} for
  all 64 cells), `onodeoff`, `orowc0`.
  **EXP-170 VALIDATED: Temp\exp166_check.py 155/155 x3** —
  `0x4165`/`319850` closest-entity scan real: list
  `q[0x2EC1360]` `{d+0 id, q+0x18 next}` -> `2FB310(id)`
  static pos table `0x22BE7F0+id*0x20` (`b[+0]` flag, quad
  `+0x10`) -> `3A1960(rec+0xE0)` squared-XZ dist ->
  strictly-closer wins (`f[0x2F973B8]` best-dist seed,
  runtime-init'd, 0 in image — planted FLT_MAX). Reject
  proven (null list -> edi -1 -> eax 0); accept proven
  (2 nodes, closest wins, out1/out2 quad). Notable:
  **the output quad's w lane is caller-frame garbage**
  (0xCDCDCDCD — `319850` repacks only x/y/z); `outf` =
  `xmm6 + C - 0.1f` = 0.9. Two more RIP off-by-one fixes:
  list head `0x2EC1360` (was `0x3C92E60`), table
  `0x22BE7F0` (was `0x4BE47F0`). All `312730` dispatch
  arms now have executed coverage.
  **EXP-171 VALIDATED: Temp\exp166_check.py 155/155 x3** —
  the `2FEF30` member-arm fixture gap CLOSED: `b[rec+5]!=0`
  -> `0x2FF0E1` four-level `20E600` chain — descs
  `0x2EBF120` (member row, `b[rec+4]` idx), `0x2EBF148`
  (`w[r13+0x22]`), `0x2EBF140` (`w[r13+0x24]` — the old
  `0x2FF1FC` fault site), `0x2EBF150` (`w[r13]`) — then
  ~200i stat accumulation: `ecx = b[+0x1C2]-b[+0x88]` delta
  x `rbx.b[+0x27..+0x2C]` + `rbp` same + `rec.w` pairs;
  `b[r11+0x29..0x2D]` -> out; `b[r13+0x15]` bit-gates two
  more arms. `30FED0` member tail: `31B860` owner scan ->
  `q[objrow+0x6A0]` bit7 -> `b[obj+0x78]` -> `b[rec+0x40]`.
  `fed0-b5`/`fed0-b5own` both fault-free; new `membarm` +
  `obj6a0` fixture keys.
  **EXP-172 VALIDATED: Temp\exp166_check.py 165/165 x3** —
  `230A40`/`2324F0` usable-surface semantics decoded +
  executed. **`230A40(ctx,rowidx,kind)`** = row-usability
  bit query: two-level field substitution over the
  runtime-built BSS mask table `0x209A2D0`
  (`idx1=mask>>0xD&0x1F`, `idx2=mask>>3&0xF+0x40`,
  `ecx=((B1&A1)|(~A1&mask))&~A2|(B2&A2)`), `test cl,7`
  reject, kinds 0/1/2/3/5 -> `!bit23/25/26/27/24`,
  kind 4/6+ -> 1. **`2324F0(ctx,rowidx,scratch)`** =
  point-in-triangle edge eval: caller seeds `q[scr+8]` = P
  `{f+0 x,f+8 z}`; 3-edge loop (`d[0x908DE8]={1,2,0}` ->
  v0->v1,v1->v2,v2->v0) computing `cross(e2,e1).y` via real
  `0x202E10`; edge qualifies iff `n.y<-1e-4` AND
  `len>1e-4`; ret argmin `|dot/len-0.5|` edge idx, init -1;
  `231900` uses ret<0 = inside = usable. CW-tri interior
  -> 0xFFFFFFFF; edge0 violator -> 0. **Two harness bugs
  fixed**: `main()` dispatch `elif` never matched
  `t2730-*`/`t26e350` (dead asserts since EXP-165 — now
  live and passing, retroactively enforcing EXP-165..171
  claims); `epos` was nested inside `ownerres` (t26e350
  now gets its real position pointer). Mask-table base
  corrected to `0x209A2D0` via UC_HOOK_MEM_READ.
  **Executed standalone on zeroed rec:
  all three ret clean; `30F690(0xFFFFFFFF)` walks the full 32-bit
  dispatch with zero faults/zero scripted hits — every per-bit
  handler gates on rec fields.** Base fixture is trivial. **`377C20` can-die
  is NOT heavy — it's a 4-leaf chain**: `2EF640`→const `2164280`,
  `2EF2B0`→+0x200, `3148F0`→`max(d[0x21654C4],0)` (selected idx),
  `377C20`→bounds `d[q[2ADD100]+4]` then bit15 of
  `w[tbl+idx*3+8]` (**3-byte stride** — `rcx+rax+8` addressing).
  **Executed standalone: 6/7 pass (idx-zero expectation wrong —
  idx 0 is valid), flag/clear/oob/null/neg/edge all correct.**
  EXP-148/149/150 scripted it unnecessarily (my earlier 400-insn
  survey ran past its ret). Also real-able leaves:
  `308010` (0x75), `3271D0` (tail→`327150`). Static map detail: memset `0x1C8`+sentinels,
  master gate `02089300`, sel byte1 mode
  (1=member/`02EBF120`, 0=foe/`02EBF130`+`b[row+0x2E]` count min 1),
  `w[+4]=sel`, `30C470` (0x1B0, 9 calls incl `30FED0`); member →
  4×`31A630` slot writes (`w[+0x16]/+0x1C` then 0xFFFF×2; leaf,
  `si==0xFFFF` skips, null→-1); foe → `323790` gil clamp (leaf,
  `[+0x190]+=edx` clamp [0,0x1869F]), `02EBF038` scan
  `b[row+7]&(1<<idx)` → `323910` (0x299, 15 calls — deepest),
  5×`31A630` from `w[+0xA..+0x12]`, `327CB0` (0x12A, `w[+0x14]`),
  `326030` slot-counter clear + 3×0x34B block copy `+0x88`→
  `glob+idx*0x9C+0x5B10` (idx>0x27 → r8=0 → fault), `327DE0`
  (0x191, slot-row init), `b[+0x2C]&0x40`→`d[0]|=4`. Also mapped:
  `3105D0` reset bit4 helper (0x1A0, mapped): guard `q[+0x698]≠0`,
  `310780(+0x80)` teardown, `30C970(b[+0x695]/+0x696)` ref releases
  →0xFF, `300280`, flag masks `q0&=0xFFFFBFF75FFFCFFF`+
  `0xFFF3FFFFFEFFFFFF`, `d4&=0xFFDFFF7F`, `d[+0x690]=0`, `16D6A0`,
  loop `i<d[0208E6A0]` clearing `~(1<<b[+0xEA9])` in every object
  row's `d[+0xEA0]`, `316CF0(+0x778)`, `3291B0`/`33C9B0` (+0x80
  sub-clears), field clears `+0x6B4..+0x768`. 7/9 callees would stay
  scripted — low density; `23AC80` is the better heavy package.
  EXP-146 published `f7980f6d7` — every entry of
  `CONTRACT-resource-request-queue` now has executed evidence;
  I1–I7 verdicts sit with OPUS under the already-filed
  `REQ-OPUS-QUEUE-CONTRACT-S13-READJUDICATE`. Prior:
  contract-key round `0265040a1`, EXP-145 `d20fd7508`, EXP-143
  + EXP-144 `4913242bb`, EXP-142 `b14925d52`, EXP-141 path fix
  `738940bbc`. Remaining UNLINKED executable cells:
  `CONTRACT-boot-fixups` §13c (time-base triple readers).
  Note for future packages: FABLE's corpus sweep found
  EXP-142 is cited ZERO times in L2-VERDICTS.md and no
  00-Engine-Core-Runtime page mentions it — propagation to
  verdict/subject pages is a gap to close when the S-01
  contract owner asks, not something to self-edit.
  Prior: publication queue CLEARED — all ten
  EXP132..141-PUB rows finished revs 26015-26036 while
  `@publication` was free. Evidence commits:
  132..138 `c36dcda20`, 139 `cbe4b46af`, 140 `0d068c953`,
  141 `74e88f699`; board tails `eac6b7e76`, `2b21ae62b`,
  `6d7250f6a`, `c0e8c9581`, `9cfeb40a9`, `a0999d391`,
  `534f62c6d`, `ff499cc68`, `837a1d1d7`, `ddd3f9ca9`.
  Prior state: EXP-139 sealed, committed
  `cbe4b46af`, routed (finish rev 24129, EXP139-PUB rev
  24130, review rev 24131, findings rev 24132). The nav path
  is now real end-to-end except CRT IAT cells — the scripted
  nav-boundary campaign is DONE. Next package — RESOLVED by the post-scope
  audit (commit `8d9746321`, findings filed rev 24258):
  the parked region-scan siblings `0x22D7E0..`/`0x22DE60`
  and their exclusive callees `0x230790`/`0x22E7D0`/
  `0x3810B0` have ZERO inbound references anywhere in the
  image (no call/jmp/jcc/lea/imm32/qword; no CFG table
  exists) — dead code in this build, not claimable through
  any caller scope. `0x381D90` is the one live body, via
  `0x232160` (`r8w∈[0x4000,0x5000)` tail-jmp) ← `0x3D97E0`
  ← `0x32CF50` ← `0x32B390` ← `0x32B1C0` ← `0x32AEC0` —
  a `0x32xxxx` subsystem chain whose top is also
  unreferenced. `0x22EF20` reaches via `0x232380` ←
  `0x2F6DBE`/`0x2F6DD2`; `0x22FFE0` via `0x17D82C`.
  The generic leaves (`0x202C70`×81, `0x202D70`→matmul
  `0x217150`×86, `0x202D50`→rigid-inv `0x217610`×16,
  `0x380800`×15) land with whichever subsystem scope
  claims a caller. The nav harness is at its natural
  boundary — check the ready queue / inbound requests
  for the next claim; the next real package lives in a
  non-nav subsystem scope.
  Inbound notices resolved this round: EXP-129 epsilon-boundary sentence
  corrected (OPUS reading verified — same predicate, opposite
  branch polarity; finish rev 23724), the sealed-uncommitted
  observation answered as publish-queue state (finish rev
  23727), its follow-up re the third/fourth untracked record
  answered the same way (finish rev 23829), and the OPUS
  named-handoff publish offer answered YES (finish rev 23901).
  Publish discipline unchanged: explicit paths only,
  `publish_paths.sh` private index, verify each listed path is
  mine, check the staged column first.
  Prior seven-row publish chain (2026-09-20): EXP120-PUB
  `1f633b3e5`, EXP121-PUB `8597a52da`, EXP122-PUB `a0a9ef221`,
  EXP123-PUB `eaf187c0a`, EXP124-PUB→EXP-125 `e06d047c6`
  (renumber documented in commit + finish note), EXP126-PUB
  `eb72b00e3`, EXP128-PUB `e0531bd21`.
  Prior publishes: EXP109-PUB `70bcc75cf`, EXP110-PUB `d90f096f5`,
  EXP111-PUB `4301934a7`, EXP112-PUB `a5594090b`, EXP113-PUB
  `e35d73da4`, EXP114-PUB `b842a915d`, EXP115-PUB `092ce86e1`,
  EXP116-PUB `b78c24277`, EXP117-PUB `fc414f5dc`, EXP118-PUB
  `8728d00dd`, EXP129-PUB `b383c02d6`, EXP130-PUB `86c87ed11`,
  EXP131-PUB `90ce11f15`.
- **Pending requests/reviews:** `REQ-AUDITSPEC-LICENSE-CHECK-REVIEW`
  (rev 25894), `REQ-OPUS-LICENSE-CHECK-FINDINGS` (rev 25895),
  `REQ-OPUS-NAV-SIBLINGS-DEADCODE-FINDINGS`
  (rev 24258), `REQ-AUDITSPEC-NAV-REGION-QUERY-REVIEW`
  (rev 24131), `REQ-OPUS-NAV-REGION-QUERY-FINDINGS` (rev 24132),
  `REQ-AUDITSPEC-NAV-RESIDUAL-BOUNDARY-REVIEW`
  (rev 24106), `REQ-OPUS-NAV-RESIDUAL-BOUNDARY-FINDINGS` (rev 24107),
  `REQ-AUDITSPEC-NAV-SUBSYSTEM-LEAF-REVIEW`
  (rev 24010), `REQ-OPUS-NAV-SUBSYSTEM-LEAF-FINDINGS` (rev 24011),
  `REQ-AUDITSPEC-NAV-OBJ-ACCESSOR-REVIEW`
  (rev 23898), `REQ-OPUS-NAV-OBJ-ACCESSOR-FINDINGS` (rev 23899),
  `REQ-AUDITSPEC-NAV-GATE-WALK-REVIEW`
  (rev 23825), `REQ-OPUS-NAV-GATE-WALK-FINDINGS` (rev 23826),
  `REQ-AUDITSPEC-NAV-PATH-VALIDATOR-REVIEW`
  (rev 23721), `REQ-OPUS-NAV-PATH-VALIDATOR-FINDINGS` (rev 23722),
  `REQ-AUDITSPEC-NAV-LOS-REVIEW`
  (rev 23645), `REQ-OPUS-NAV-LOS-FINDINGS` (rev 23647),
  `REQ-AUDITSPEC-NAV-CONSUMER-REVIEW`
  (rev 23543), `REQ-OPUS-NAV-CONSUMER-FINDINGS` (rev 23545),
  `REQ-AUDITSPEC-NAVGRID-QUERY-REVIEW`
  (rev 23399), `REQ-OPUS-NAVGRID-QUERY-FINDINGS` (rev 23400),
  `REQ-AUDITSPEC-TRANSFORM-PREDICATE-REVIEW`
  (rev 23301), `REQ-OPUS-TRANSFORM-PREDICATE-FINDINGS` (rev 23302),
  `REQ-AUDITSPEC-VEC3-NORMALIZE-REVIEW`
  (rev 23211), `REQ-OPUS-VEC3-NORMALIZE-FINDINGS` (rev 23212),
  `REQ-AUDITSPEC-EXP109-POLL-PUMP-REVIEW`
  (rev 23084), `REQ-OPUS-EXP109-POLL-PUMP-FINDINGS` (rev 23085),
  `REQ-AUDITSPEC-ALLOC-FREE-PATH-REVIEW`
  (rev 22981), `REQ-OPUS-ALLOC-FREE-PATH-FINDINGS` (rev 22982),
  `REQ-AUDITSPEC-POOL-ADOPTION-REVIEW`
  (rev 22620), `REQ-OPUS-POOL-ADOPTION-FINDINGS` (rev 22621),
  `REQ-AUDITSPEC-ALLOC-CORE-REVIEW`
  (rev 21488), `REQ-OPUS-ALLOC-CORE-FINDINGS` (rev 21489),
  `REQ-AUDITSPEC-ALLOC-DISPATCH-REVIEW`
  (rev 21428), `REQ-OPUS-ALLOC-DISPATCH-FINDINGS` (rev 21429),
  `REQ-AUDITSPEC-EXP109-QUEUE-TAILS-REVIEW`
  (rev 21393), `REQ-OPUS-EXP109-QUEUE-TAILS-FINDINGS` (rev 21394),
  `REQ-AUDITSPEC-EXP108-TAIL-RESOLVERS-REVIEW`
  (rev 21366), `REQ-OPUS-EXP108-TAIL-RESOLVERS-FINDINGS` (rev 21367),
  `REQ-AUDITSPEC-T51-TAIL-RESOLVERS-REVIEW`
  (rev 21336), `REQ-OPUS-T51-TAIL-RESOLVERS-FINDINGS` (rev 21337),
  `REQ-AUDITSPEC-TRANSFORM-VEC-WRITER-REVIEW`
  (rev 21296), `REQ-OPUS-TRANSFORM-VEC-WRITER-FINDINGS` (rev 21297),
  `REQ-AUDITSPEC-SLOT-HANDLE-ALGEBRA-REVIEW`
  (rev 21252), `REQ-OPUS-SLOT-HANDLE-ALGEBRA-FINDINGS` (rev 21253),
  `REQ-AUDITSPEC-NAME-REGISTRY-INIT-REVIEW`
  (rev 21204), `REQ-OPUS-NAME-REGISTRY-INIT-FINDINGS` (rev 21205),
  `REQ-AUDITSPEC-TRANSFORM-PRIMITIVES-REVIEW`
  (rev 21159), `REQ-OPUS-TRANSFORM-PRIMITIVES-FINDINGS` (rev 21160),
  `REQ-AUDITSPEC-SHADOW-LOD-REVIEW`
  (rev 21124), `REQ-OPUS-SHADOW-LOD-FINDINGS` (rev 21125),
  `REQ-AUDITSPEC-SHADOW-SYNC-REVIEW`
  (rev 21092), `REQ-OPUS-SHADOW-SYNC-FINDINGS` (rev 21093),
  `REQ-AUDITSPEC-ACTOR-RECORD-INIT-REVIEW`
  (rev 21065), `REQ-OPUS-ACTOR-RECORD-INIT-FINDINGS` (rev 21066),
  `REQ-AUDITSPEC-MT-TWIST-REVIEW` (rev ~20936),
  `REQ-OPUS-MT-TWIST-FINDINGS` (rev ~20937),
  `REQ-AUDITSPEC-PHYRE-CALLERS-REVIEW` (rev 20919),
  `REQ-OPUS-PHYRE-CALLERS-FINDINGS` (rev 20920),
  `REQ-AUDITSPEC-POOL-LIFECYCLE-REVIEW` (rev 20903),
  `REQ-OPUS-POOL-LIFECYCLE-FINDINGS` (rev 20904),
  `REQ-AUDITSPEC-RAMP-CONSUMERS-REVIEW` (rev 20816),
  `REQ-OPUS-RAMP-CONSUMERS-FINDINGS` (rev 20817),
  `REQ-OPUS-RECORD-POOL-FINDINGS` (rev 20750),
  `REQ-AUDITSPEC-RECORD-POOL-REVIEW` (rev 20755),
  `REQ-OPUS-FIELD-PASS-FINDINGS` (rev 20691),
  `REQ-AUDITSPEC-FIELD-PASS-REVIEW` (rev 20690),
  `REQ-OPUS-FIND-OWNING-UNIT-FINDINGS` (rev 20442),
  `REQ-AUDITSPEC-FIND-OWNING-UNIT-REVIEW` (rev 20443),
  `REQ-OPUS-AUTO-STATUS-GATES-FINDINGS` (rev 19321),
  `REQ-AUDITSPEC-AUTO-STATUS-GATES-REVIEW` (rev 19322),
  `REQ-OPUS-FIELD-MUSIC-SELECTION-FINDINGS` (rev 19248),
  `REQ-AUDITSPEC-FIELD-MUSIC-SELECTION-REVIEW` (rev 19249),
  `REQ-OPUS-BATTLE-MODE-COMPOSITION-FINDINGS` (rev 19196),
  `REQ-AUDITSPEC-BATTLE-MODE-COMPOSITION-REVIEW` (rev 19197),
  `REQ-OPUS-CLASS-DESCRIPTOR-DTOR-FINDINGS` (rev 19168),
  `REQ-AUDITSPEC-CLASS-DESCRIPTOR-DTOR-REVIEW` (rev 19169),
  `REQ-OPUS-SOUND-REQUEST-FINDINGS` (rev 19128),
  `REQ-AUDITSPEC-SOUND-REQUEST-REVIEW` (rev 19129),
  `REQ-OPUS-GAMBIT-WALK-FINDINGS` (rev 19057),
  `REQ-AUDITSPEC-GAMBIT-WALK-REVIEW` (rev 19058),
  `REQ-OPUS-PHYRE-HEADER-FINDINGS` (rev 18978),
  `REQ-AUDITSPEC-PHYRE-HEADER-REVIEW` (rev 18979),
  `REQ-OPUS-HPWRITE-CALLEES-FINDINGS` (rev 18927),
  `REQ-AUDITSPEC-HPWRITE-CALLEES-REVIEW` (rev 18928), `REQ-OPUS-BAZAAR-CALLEES-FINDINGS` (rev 18788),
  `REQ-AUDITSPEC-BAZAAR-CALLEES-REVIEW` (rev 18789), `REQ-OPUS-COMMIT-CALLEES-FINDINGS` (rev 18735),
  `REQ-AUDITSPEC-COMMIT-CALLEES-REVIEW` (rev 18736), `REQ-OPUS-REWARD-GATE-FINDINGS` (rev 18661),
  `REQ-AUDITSPEC-REWARD-GATE-REVIEW` (rev 18662). Still open:
  `REQ-OPUS-ACHIEVEMENT-EVALAWARD-FINDINGS` (15249),
  `REQ-AUDITSPEC-ACHIEVEMENT-EVALAWARD-REVIEW` (15250),
  `REQ-OPUS-SAVE-CONTAINER-FINDINGS` (15169), `REQ-AUDITSPEC-SAVE-CONTAINER-REVIEW` (15170),
  `REQ-OPUS-BODYPOOL-GUARDS-FINDINGS` (15065), `REQ-AUDITSPEC-BODYPOOL-REVIEW` (15066),
  `REQ-OPUS-STATUS-WRITE-FINDINGS` (14909), `REQ-AUDITSPEC-STATUS-REVIEW` (14910),
  `REQ-OPUS-VERB-LIFECYCLE-FINDINGS`, `REQ-AUDITSPEC-VERB-REVIEW`,
  `REQ-OPUS-EFX-REBASE-FINDINGS`, `REQ-AUDITSPEC-EFX-REVIEW`, `REQ-OPUS-ACTORPOOL-LIVE-HEADER`
- **Fallback eligible work:** unassigned ready queue; remaining isolated-only residual is
  partial-coverage contracts — lua-chunk-loader family remainder, field-runtime-pass 1297-byte
  pass body (achievement-counters residual done by EXP-089; reward-gate callees done by
  EXP-090)
- **Latest coherent commit/checkpoint:** EXP-213 committed
  `3ead26091` (521/521 ×3, hash `2b0f36d4…`; resource-lookup chain
  real + 8/> deep tails; board note rev 32422); EXP-212 committed
  `922201a53` (519/519 ×3, hash `dc081df2…`; nine deep parsers
  real + dark kind arms; board note rev 32379); EXP-211 committed
  `d0de79475` (503/503 ×3, hash `d3378248…`; dead-assert repair
  for EXP-206..210 included; board note rev 32335); EXP-210 committed
  `a9f6385dd`/`811059ad0` (466/466 ×3, hash `8b721870…`; board note
  rev 32183); EXP-209 committed
  `5511eb397`/`1bda2ec80` (455/455 ×3, hash `4cca9cf5…`; board note
  rev 32141); EXP-208 committed
  `548d7f079`/`1564679ff` (450/450 ×3, hash `78ec7301…`; board note
  rev 32092); EXP-207 committed
  `687c77e95`/`9673c2f46` (441/441 ×3, hash `c49b4c64…`; board note
  rev 32024); EXP-206
  `95b4b371b`/`cca377b5c` (438/438, `1527aab0…`; board note
  rev 31997); EXP-205 `dfd793803`/`f08118e5e` rev 31943;
  EXP-204 `4f3f6a7d9`/`9fac212a4` rev 31857). Older chain:
  EXP-140 sealed +
  routed + committed `0d068c953` (record + evidence dir; 57/57
  functional, 35/35 mutants, stable ×3; finish rev 25888,
  EXP140-PUB 25890, requests 25894/25895). Note: that commit
  swept already-staged peer files incl. an
  `audio-pan-authored-positive` evidence-dir deletion — shared-
  index failure mode; future shared-path commits go through
  `publish_paths.sh` only. EXP-133 prose fix committed +
  CONTRA finished rev 25790. Post-EXP-139
  follow-ups landed — `abd705ebc` (EXP-138 DA730 lane
  correction, CONTRA answered), `df8d8ab73` (unit-shape
  primitives page + README, NOPAGE decided), `8d9746321`
  (post-scope dead-code audit into EXP-139 record + page;
  findings filed rev 24258), `8e0fbfbcb` (EXP-132 ownership
  placements on workbench + nav-mesh pages, finish rev 24260). EXP-139 SEALED +
  routed + COMMITTED `cbe4b46af` (record + evidence dir;
  finish rev 24129, EXP139-PUB 24130, requests 24131/24132).
  Prior batch: EXP-132..138 committed `c36dcda20` (six
  records + evidence dirs; finish revs 24008-24011 +
  EXP-138 ~24100, EXP138-PUB 24105, requests 24106/24107).
  EXP132..139-PUB rows remain READY behind `@publication`
  (held by FABLE-PUB-THE-CORESOURCEVOICE-RENDER-ANOMALY,
  ACTIVE) — formal closes pending the lock. Latest published: EXP-131 evidence
  `90ce11f15` (HEAD); EXP-130 evidence `86c87ed11`; EXP-129
  evidence `b383c02d6`. Publish
  chain 2026-09-20: `1f633b3e5`
  (EXP-120), `8597a52da` (EXP-121), `a0a9ef221` (EXP-122),
  `eaf187c0a` (EXP-123), `e06d047c6` (EXP-125 via EXP124-PUB),
  `eb72b00e3` (EXP-126), `e0531bd21` (EXP-128), `b383c02d6`
  (EXP-129). Older: EXP-101
  evidence `58859ed57`
  + board tails `0e424c2ca`/`663ea754d`. Record-correction batch
  `d5a4b7746` + board tail `b5b3eea24`. EXP-100 evidence `d0bb9351`
  + board tail `f8cfd2b7`. Previously EXP-096 `68c6cec5` —
  board tail in this commit. Publish guard
  `check_publish_neighbours.py` runs before every publish. RESOURCE-KEY LESSON: `@publication`
  reservation tasks must use the literal resource key `@publication` — `resource:@publication`
  displays as claimed but `publish_paths.sh` refuses it (fixed via EXP086-PUB2; PUB retired).
  STILL UNPUBLISHED: my `neighbour-dispositions.tsv` verdict row sits in a file carrying
  SWE2-DATA's unstaged verdicts — left for a shared-surface publish by its owner.

## Checkpoints

Append below, newest last. Record corrected facts and remaining work, not file growth.

- 2026-09-16 — OPUS-REQ-SWE2-ORACLE-RAMP-CHANNEL-DIFF done: `diff_ramp_channels.py` executed —
  483 commands, 129 compared lines, 0 mismatches; all six shipped entries bitwise-agree with the
  reconstruction. Transcript: `_experiments/evidence/ramp-channel-diff/run.txt`. The harness
  docstring carries a contract correction worth propagating: the pause gate is `02B40524` (the cell
  BEFORE the table qword), not `02B4052C`.
- 2026-09-16 — OPUS-REQ-SWE2-ORACLE-SAVE-CONTAINER-ROUNDTRIP done: **18/18 real saves round-trip
  bit-for-bit**. `header('SAFH'|u32 declared|u32 n)` + RC4(MD5(rotl(title,n)[:31]), deflate-9) —
  decrypt+inflate produces exactly `header+4` bytes, and classic-zlib level-9 recompression
  reproduces the shipped ciphertext identically. Caveat recorded: the zlib-ng build's level-9 output
  does NOT match (encoder difference); classic zlib 1.3.2 does. Evidence:
  `_experiments/evidence/save-container-roundtrip/`.
- 2026-09-16 — OPUS-REQ-SWE2-ORACLE-SHORT-READ done: NULL-argument paths now executed —
  handle-global==0 and dest==0 both take `je 0x866a70`, return 0 through the real outer, write only
  the RESULT global; `je`→`jne` mutant detected. Prefix/stale-tail/cursor were already covered by
  ASTRA's `short-read-execution.json`. Evidence: `_experiments/evidence/short-read-null-path/`.
- 2026-09-15 — ASTRA-REQ-ORACLE-COMMAND-OBSERVER-PIN done: the stale `runtime_probe.py` pin
  (`f82b0c6a` = commit `797828d6`) drifts only in the `--check` CLI path — none of observe.py's four
  imported symbols (`find_process`, `module_base`, `CONTROL_ADDR`, `CONTROL_BYTES`) is touched, so
  repin is justified. Minimal candidate in
  `_experiments/evidence/EXP-037-command-observer/live-recovered/` (observe.py, test_observe.py,
  dependencies.json, PIN-RECONCILIATION.md); 11/11 existing controls pass.
- 2026-09-16 — OPUS-CONTRA-AUTHORED-TABLE-LIVE-CLAIM adjudicated: the EXPERIMENT was right, the
  contract §13 header was stale. EXP-079 is live (method C) against CONTRACT-authored-table-row-lookup
  and §15 already carried it; only the header still denied live capture. Header superseded; gate26
  now classifies the contract LIVE and the two instruments' live sets differ only by
  input-name-registry (legitimate in-contract-only case). Also closed: stranded-lmap (OPUS's
  correction verified), pass-22 top-decile (all 9 rows already dispositioned by FABLE/SWE2-DATA),
  R3 tail (a-typed-list→CoreRuntimeScheduling row dispositioned CROSSING-ACCOUNTED — codec pair
  fan-out, bullet added to its crossings section), publish guard adopted (ran clean on the pending
  batch). Board revs 14602–14615.
- 2026-09-15 — EXP-083 complete: the resource entry tree's whole call graph executed as shipped
  (45 cases, 5 mutants all detected). Headline: the link encoding only works when the decoder base
  `[01F83530]` is 0 — `enc(0)` under a nonzero base decodes to a wild pointer and faults the second
  insert — so links are truncated pointers and the constraint is nodes below 4 GiB, not "within 4 GiB
  of the base". The removal rebalance the contract left underived is now executed evidence. Evidence:
  `_experiments/evidence/resource-entry-tree-execution/`; record `_experiments/EXP-083-*.md`.
  Routed: OPUS (contract text) + SWE2-AUDIT-SPEC (audit). Write access to the repo was unavailable for
  part of the block; the record and board ops were applied once writes resumed.
- 2026-09-16 — SWE2-ORACLE-EFX-REBASE-EXEC done: EXP-084 sealed — 52/52 cases, 7/7 mutants,
  17 shipped bodies at real VAs. Executed: the two deltas are independent and per-field (the
  combined path's +0x390 compare is against the item, not a second context); the signed-32-bit
  window is exact at -2^31 inclusive and +2^31-1, diverges silently at +2^31 (base +2 GiB up,
  links -2 GiB down), and no-ops links at +4 GiB; both equality guards are 64-bit while the delta
  is 32-bit; the resolver <=0x40 reject band is low32(slot+8) in {0} u [0xFFFFFFC0,0xFFFFFFFF]
  (bit31-set low32 results survive); offset-0 null preservation requires codec base 0, and a
  nonzero base also breaks 003AA3D0's offset-0 list terminator — second base-must-be-0 witness.
  Disclosed: 0024D540 ran as slice 0024D619..0024D686 with a jmp$ boundary patch; 0024ED80
  ret-stubbed in two rdx!=0 driver cases; 005004C0/00442460 exercised via default return arms.
  Evidence: `_experiments/evidence/efx-rebase-execution/`; record
  `_experiments/EXP-084-efx-source-rebase-execution.md`. Routed:
  SWE2-ORACLE-REQ-OPUS-EFX-REBASE-FINDINGS (rev 14731) + REQ-AUDITSPEC-EFX-REVIEW (rev 14732).
  Published: `1429abdd` (EXP-084 record + check.py + result.json + bodies.json + this inbox).
- 2026-09-16 — SWE2-ORACLE-VERB-LIFECYCLE-EXEC done: EXP-085 sealed — 35/35 cases, 9/9 mutants,
  five shipped bodies at real VAs, zero stubs of shipped code (callbacks are fixture data by
  design). Executed: the phase machine including the phase>=2 entry arm section 7 doesn't draw;
  the phase byte is re-read after result and selects int-0 / int-slotC / float-slotC; the +0xC
  clear lives only in the phase-0 arm; test al,1 is the whole running check; begin's return is
  discarded; poll's r9 is residual; begin alone gets the manager at [rsp+0x28] callee-side.
  CORRECTION: the rebind calls 00358940 on the MANAGER — the actor table is [manager+8], not the
  context's. The push bound is 0x3F (index 63 unreachable); a negative depth passes it and writes
  the type byte inside the depth dword itself. Evidence:
  `_experiments/evidence/verb-lifecycle-execution/`; record
  `_experiments/EXP-085-verb-lifecycle-execution.md`. Routed:
  SWE2-ORACLE-REQ-OPUS-VERB-LIFECYCLE-FINDINGS + SWE2-ORACLE-REQ-AUDITSPEC-VERB-REVIEW.
- 2026-09-16 — SWE2-ORACLE-STATUS-OP-EXEC done: EXP-086 sealed — 67/67 cases, 9/9 mutants,
  `0030E360` + nine real callees as shipped, real `status_data.bin`. Two contract claims
  refuted by execution: the applier `003112F0` is unreachable (both builders clear the gate
  bit) and the cascade's null path faults at VA `0xC` rather than degrading. Deliberate
  faults measured at VA 8/9 per default. Evidence `_experiments/evidence/status-write-execution/`;
  record `_experiments/EXP-086-*.md`. Routed: REQ-OPUS-STATUS-WRITE-FINDINGS (14909),
  REQ-AUDITSPEC-STATUS-REVIEW (14910).
- 2026-09-16 — SWE2-ORACLE-BODYPOOL-GUARD-EXEC done: EXP-087 sealed — 49/49 cases, 9/9 mutants,
  creator `002E3500` + all five consumers + 14 real leaf callees as shipped. Central contract
  claim CONFIRMED: exhaustion is quiet loss — NULL stored untested at actor+0x138, every
  consumer write gated; release→alloc recycles the just-released body immediately. CORRECTION:
  codec/row table base is `0x02098E10`, not `0x02649E10`. Measured: cons2 edx dispatch
  {0:chain,2:3,3:5,else:2}, null-ctx fault at VA 0xC0, cons5 dominated reloads. Harness note:
  unicorn `mem_write`/`mem_read` API intermittently fails on mapped pages on this host —
  all fixture I/O is ctypes host-buffered via `mem_map_ptr`; stable across 3 processes.
  Evidence `_experiments/evidence/movement-body-pool-guards/`; record
  `_experiments/EXP-087-*.md`. Routed: REQ-OPUS-BODYPOOL-GUARDS-FINDINGS (15065),
  REQ-AUDITSPEC-BODYPOOL-REVIEW (15066).
  Published: `1da00aab` (EXP-087 record + check.py + result.json + bodies.json + this inbox).
- 2026-09-16 — SWE2-ORACLE-SAVE-CONTAINER-EXEC done: EXP-088 sealed — 46/46 cases, 9/9 mutants,
  the last nothing-executed contract closed. Writer `00866200`, reader `008666B0`, inner
  `00865D90`, decrypt `00865840`, encrypt `00865AE0` plus the real zlib deflate/inflate
  subtrees, all at canonical VAs. Round-trip both directions; every admission gate executed —
  three distinct failure shapes (raw-fill on size<=4/bad-magic, truncate on size<=12/n>31,
  store-then-reject on declared>1MiB). Findings: writer eax=0 on success AND deflate-abort
  (silent save abort — header-only sav_tmp abandoned); sav_org backup gated on `02B40E04`;
  chunk Final = chunk<0x3E8 literal (multiples of 1000 never Final); reader fills vector to
  DECLARED size. DISCLOSED: CryptoAPI is a faithful HLE model — call order/constants/flags/
  hash-data measured, but derived-key bytes vs real advapi32 unverified (needs real .sav or
  live call). Evidence `_experiments/evidence/save-container-transform/`; record
  `_experiments/EXP-088-*.md`. Routed: REQ-OPUS-SAVE-CONTAINER-FINDINGS (15169),
  REQ-AUDITSPEC-SAVE-CONTAINER-REVIEW (15170).
- 2026-09-17 — SWE2-ORACLE-BAZAAR-CALLEES-EXEC done: EXP-092 sealed — 80/80 cases, 11/11
  mutants, two stable processes, ZERO stubs. The bazaar contract's three scripted oracles
  (gate 00322C50, id-op 003008A0, fam +0x50) all execute as shipped bytes; 16 bodies in
  bodies.json. Corrections for the contract: the refresh/tally-query path reads the fam+0x20
  BYTE table (+0x50 edx=3 arm), not the u16 tally; purchase's idop(loot,0,1,3) is a byte
  absolute-zero; the r9==1 u16 arm clamps low10 UP to the hi6 field; 00322C50 kind 1
  re-dispatches via fam+0x38 class numbers (fam13->0x12 same goods window, fam14->0x13);
  null registry rejects at the gate but a null ROW pointer is an unguarded +0x16/+0x14
  fault (kept as expect_fault cases); purchase zeroes sold bytes so repeatable rows re-run
  and fail the predicate post-purchase. fam14 +0x48 = the clamped gil-bank write
  (00254EE0). Evidence `_experiments/evidence/bazaar-callees-exec/`; record
  `_experiments/EXP-092-*.md`. Routed: REQ-OPUS-BAZAAR-CALLEES-FINDINGS (18788),
  REQ-AUDITSPEC-BAZAAR-CALLEES-REVIEW (18789). Finish rev 18787.
- 2026-09-17 — SWE2-ORACLE-PHYRE-HEADER-EXEC done: EXP-094 sealed — 25/25 cases, 10/10
  mutants, two stable processes. `0059A3B0` PClusterHeader loader executes from shipped
  bytes end-to-end: real `00160210` static init builds the `0x2CAA0A0` descriptor,
  real `0063E2E0`/`0063CE80`/`0059FDB0` walk+dispatch, real
  `0059A6F0`/`0059C180`/`0059A780`/`0059A8B0` namespace swap (21 bodies). Verified:
  arg7 is the id-check gate (real caller `0059E070` sets 1 — ids validated even on LE
  headers); null `nsRec.buf` is a hard 6 even at len 0; `outLen` three-way dispatch
  incl. a second `0063E2E0` pass when swapped; `descswap` r8b = direction flag with
  parent chain via `desc+0x78`; member node `+0x28` bit1 skip. Disclosed fixtures:
  stream I/O boundary, member-node graph (deferred reflection registration out of
  scope), member-type swap leaf (logs + real bswap). Evidence
  `_experiments/evidence/phyre-header-exec/`; record `_experiments/EXP-094-*.md`.
  Routed: REQ-OPUS-PHYRE-HEADER-FINDINGS (18978), REQ-AUDITSPEC-PHYRE-HEADER-REVIEW
  (18979). Finish rev 18977. Published `1c31051a`.
- 2026-09-17 — SWE2-ORACLE-GAMBIT-WALK-EXEC done: EXP-095 sealed — 35/35 cases,
  14/14 mutants, two stable processes. Walk `00305CC0`, evaluator `003014C0`
  and notify `004697C0` executed from shipped bytes (11 real bodies); commit
  `0030F760` scripted per EXP-091, `00301AD0` scripted per-slot (804-body
  closure disclosed). Verified: subgroup base = set+0x20 + 24*sum(counts
  [0..idx-1]) via pair loop, count byte reread each iteration, stride 0x18,
  failed-commit-continue, first-success return; resume = mode AND ctx AND
  ctx+4&0x4000 offering only flag-0x40 records while mode!=0 skips flag-0x80;
  resume point ctx==rec -> ret 1 pre-eval; third call gated by latched
  unit+0x714 != 0xFFFF with r9d=4; eval chance==0 -> match else
  roll%100 < chance; LCG 00328370 state at 0x22C256C. Evidence
  `_experiments/evidence/gambit-walk-exec/`; record `_experiments/EXP-095-*.md`.
  Routed: REQ-OPUS-GAMBIT-WALK-FINDINGS (19057),
  REQ-AUDITSPEC-GAMBIT-WALK-REVIEW (19058). Finish rev 19053. Published `92a9f665`.
- 2026-09-17 — SWE2-ORACLE-SOUND-REQUEST-EXEC done: EXP-096 sealed — 39/39 cases,
  14/14 mutants, three stable processes. The request path executes real from
  shipped bytes end to end up to the dispatcher: verb `00357040` (real typed
  pops `00267E10` / push `0026B4E0`), all four wrappers `00249C60`/`00249CA0`/
  `00271500`/`0024A1A0`, all four resolvers `003A1180`/`003A11F0`/`003A1070`/
  `003A1100`, liveness `00267330` + mute `00267310`, gate2 `003603C0`, play
  call `002DF220` masking, reshape `002DF0F0` (16 bodies). `001DBDB0`/
  `001DBE90`/`002DEE80`/`008620C0` entry-scripted, disclosed. Verified: gate1
  matrix (gateless `00271500` proceeds with gate set); selector 1->`003A1100`,
  2->`003A1070`, else->`003A1180`; `003A11F0` has no liveness call; handle
  arithmetic slot=lo16, w8|wA<<16 == handle&0x7FFFFFFF, ret slot<<9+index;
  liveness byte slot*0x288+0x2098E20 bit0/bit7 vs mute byte +0x1F1; resolver
  fail -> -1 vs play id=-1/gate2 -> 0; dispatch args measured at entry:
  pan=arg3 truncated sil (8 bits), volume=arg4 masked &0x7F, id btr 31.
  Fixture lesson: `00267330`'s +0x10 lands on base 0x2098E10, effective
  +0 rel 0x2098E20. Evidence `_experiments/evidence/sound-request-exec/`;
  record `_experiments/EXP-096-*.md`. Routed: REQ-OPUS-SOUND-REQUEST-FINDINGS
  (19128), REQ-AUDITSPEC-SOUND-REQUEST-REVIEW (19129). Finish rev 19126.
  Published `68c6cec5`.
- 2026-09-18 — SWE2-ORACLE-CLASS-DESCRIPTOR-DTOR-EXEC done: EXP-097 sealed —
  15/15 cases, 10/10 mutants, two stable processes. Destructor `00633390`
  executes from shipped bytes with both formerly-scripted callees real:
  `0063D640` (sub-object registry detach) and `006B6700` (+0x60 unlink
  drain), plus TLS getter `006373D0` on the initialized arm (4 real bodies;
  `_aligned_free` `00584730` scripted at entry, rcx logged in order).
  Verified: vtable `0xD581C0`->`0xD31168`; counter guard — [obj+0xE8]+1 ==
  [0x2CF8260] decrements, incl. the 0xFFFFFFFF wrap edge; `0063D640` real
  ABI is (rcx=[obj+0x70] subobj, rdx=obj) — it self-links obj's +0x50 node
  and detaches sub+0/+8 from the registry iff sub's +0x10 list is empty AND
  sub != TLS-current (empty: T,T + detach; members: no T; current: one T,
  no detach); pass-1 frees payload node+0x18 then node for +0x90/+0xA0
  owned nodes in node order; +0x80/+0xB0 and pass-2 are unlink-only;
  `006B6700` is a pure drain. Disclosed: heap internals, lazy-init arm,
  list roles. Evidence `_experiments/evidence/class-descriptor-dtor-exec/`;
  record `_experiments/EXP-097-*.md`. Routed: REQ-OPUS-CLASS-DESCRIPTOR-DTOR-FINDINGS
  (19168), REQ-AUDITSPEC-CLASS-DESCRIPTOR-DTOR-REVIEW (19169). Finish rev
  19167. Published `ddfbe1d9` + tail `79967298`.
- 2026-09-18 — SWE2-ORACLE-BATTLE-MODE-COMPOSITION-EXEC done: EXP-098
  sealed — 19/19 cases, 10/10 mutants, two stable processes, ZERO scripted
  boundaries. The whole composition the pilot ran split executes real:
  ladder `0030D9A0` -> predicate `00377C20` -> index `003148F0` ->
  ctx `002EF2B0` -> base `002EF640` (5 bodies, ~238 B). Verified: six
  modes in contract priority (8>4>pred>2>1); early returns emit no
  predicate-trace tokens; predicate calls fire iff reached; index =
  `[0x21654C4]` cmovs-clamped; count bound `jae` + null-table refuse;
  row u16 bit15 at `tab+3*idx+8`, `>>15` (bit14-only row answers 0 —
  killed m-shr); flags re-read after the predicate call. Disclosed:
  setters/save/consumers and the queued live half stay out. Evidence
  `_experiments/evidence/battle-mode-composition-exec/`; record
  `_experiments/EXP-098-*.md`. Routed: REQ-OPUS-BATTLE-MODE-COMPOSITION-FINDINGS
  (19196), REQ-AUDITSPEC-BATTLE-MODE-COMPOSITION-REVIEW (19197). Finish
  rev 19195. Published `3ccb447c`.
- 2026-09-18 — SWE2-ORACLE-AUTO-STATUS-GATES-EXEC done: EXP-100 sealed —
  40/40 cases, 13/13 mutants, two stable processes. Subject `0030FED0`
  (1787 B) re-run with the gate/classifier oracles REAL: validity
  dispatcher `00322C50` (1025 B, 32 arms; arm 6 = equipment-id range
  `[0x1000, 0x1000+[tab+4])` over `[02EBF0F8]`), equipment gate
  `0031E9A0` + classifier `0031E9F0` (row+9 -> class 1-9 -> gate;
  only gate 3 contributes `row+0x1A`), licence gate `00323890` +
  classifier `003241D0` (row+5 BYTE is the arg — not the row pointer —
  classes 0x15-0x1E -> gate; only gate 2 contributes the 8 grants),
  resolver `0020E600`, cookie `00808C40` — 8 real bodies. Measured
  corrections: licence walk is id 0..360 inclusive over `rec+0x194`;
  `rec+0x7C` is BOTH the mp/w6 deny byte and prior[4]; the subject never
  writes acc back to `+0x78`; flags|0x202 reach APPLY/CASCADE/TAIL args;
  kind 0/1 differ in the def-row vs unit-mask halves, not in the
  equip/licence loops. Disclosed: FIND `0031B860`, APPLY `0030E130`,
  CASCADE `0030E360` (body real in EXP-086), NOTIFY `002FEF30`, TAIL
  `0030E060` entry-stubbed with arg capture; IMG32 arena is fixture
  memory at 0x50000000. Evidence `_experiments/evidence/auto-status-gates-exec/`;
  record `_experiments/EXP-100-*.md`. Routed: REQ-OPUS-AUTO-STATUS-GATES-FINDINGS
  (19321), REQ-AUDITSPEC-AUTO-STATUS-GATES-REVIEW (19322). Finish rev
  19320. Published `d0bb9351` + tail `f8cfd2b7`; stale EXP096-PUB closed
  (19343-19344).

**Workflow adoption — FF12-WORKFLOW-MIGRATION-20260928-01 (dispatched by SWE2-FRONTIER, 2026-09-28, at next safe checkpoint).**

The user approved a completion-driven workflow migration. Preserve your current identity, active work and ownership. Read the adopted _index/workflow/COMPLETION-WORKFLOW.md and its revision at your next safe checkpoint. OPUS now owns technical migration delivery; ASTRA/SOL independent engineering verification; FABLE connected mechanism completion; FRONTIER operations, safe deployment and capacity allocation. Existing specialist roles remain. This supersedes older operative instructions assigning sole migration architecture to FRONTIER or categorically forbidding useful new tools; it does not supersede full L1+L2 requirements, independent review, safety, game-state protection or history. Do not stop useful work merely to re-plan. Respond through current checked records, self-check changes, consume review, update authorized canonical files and select the next eligible task without user relay. Honour explicit stops and limits. Report a real policy/ownership conflict instead of silently overriding it.

Read the adopted _index/workflow/COMPLETION-WORKFLOW.md, current evidence policy and checked task state. Preserve your existing lane identity, history and peer work. OPUS owns technical delivery, FRONTIER assignments/deployment, SOL independent engineering verification, FABLE completion semantics. Complete your assigned contribution through its required canonical changes and review; a request alone is not package closure. Use existing task IDs and exclusive paths; do not create a competing implementation or direct-edit TEAM. If capped or blocked, checkpoint for a supported handoff and do eligible independent work, without evading limits.

SWE2-ORACLE: prioritize the existing immutable-receipt seal and direct-checkpoint-writer repair before expanding overlapping publication. Reconcile latest ownership and preserve work from capped sessions. Seal exact driver/input/case/result/environment identities per run; keep development files separate. Cumulative reuse must reference actual case subsets, never count inherited cases as new trials. Restore old receipts only from authentic bytes; otherwise limit old claims and use clearly new runs. Enforce this through actual execution-credit publication.

Replace the actual unsafe checkpoint caller with supported board note/transaction APIs. Test stale-memory and contention cases without mutating live history; a mutex elsewhere does not protect a bypass. Complete pending EXP-086/189/230 annotations using existing evidence at the recorded scope. Do not rerun every experiment to correct prose. Continue precise original-code work after the bounded repairs; branch reachability, synthetic state and imported-service substitutions must be disclosed.

Self-check and record exact source/driver/input/result identities and limits. Use a qualified non-author for independent acceptance of your production. A required upstream failure or missing result is not PASS. Preserve historical receipts and relevant regressions; run impacted checks during development, broader campaigns only at governing gates. Update the actual tool/consumer path and persistent procedure so the same defect is caught next time. Use fresh preimages, supported writes, short publication claims and meaningful commits. Keep contribution DONE separate from parent acceptance and whole L1+L2 completion. Respond through the existing board and continue eligible work without user message relay; honour explicit stops and real limits.
