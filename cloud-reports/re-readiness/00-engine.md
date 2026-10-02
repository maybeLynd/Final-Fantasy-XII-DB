# Reconstruction readiness — `FFXII TZA/00-Engine-Core-Runtime/`

| | |
|---|---|
| Stream | R (reconstruction readiness), per [`docs/cloud-briefs/re-readiness.md`](../../docs/cloud-briefs/re-readiness.md) |
| Board task | `OPUS-CLOUD-R-READINESS-00-1002` |
| Date | 2026-10-02 |
| Snapshot | this repo's text snapshot only (`34861cfd`); no executable, Ghidra or live game was used. Several pages in this folder are being edited by other lanes; every quotation is the snapshot's text. |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every item is a quotation or a paraphrase of a page, with its location. |

**Counts:** **51 pages** read (39,297 lines: 50 system pages + `README.md`; every line of prose, status and correction text read; the 4,275-row appendix of `VTIDX` counted and sampled by script), **60 member-file rows** checked for layout and counts only · **257 entry-point rows** mapped across 10 page groups · **176** self-stated open gaps + **102** structural gaps · **545 contradictions**: **269 value-changing** (**168** itemised, of which **40** have a favoured side settled by a dated correction on the pages, wholly or in part, and **128** have no favoured side; plus **101** count rows; all "page-text only - needs local check") and **276 stale / banner** · **Rating: NOT YET** overall (boot, tick, gate, stop registry, mode ladder core, encoded-id registry, accessors and the console frame MOSTLY; log, duplicate-name rules, class validator, workbench save/restore and transform primitives READY; the `0209BE80` singleton layout, the skip sub-steps, the mode transition dispatcher, the text resolvers, the basis helpers, the 267 workbench member routines, object-method behaviour and the action-timeline interpreter NOT YET).

## How to read the citations

Every citation is `ALIAS:line` (or `ALIAS:a-b`). Each alias is exactly one page; the path is relative to
`FFXII TZA/00-Engine-Core-Runtime/`. "Not stated" means none of the 51 pages says it. Where a page outside this
folder is the only place a point is made, it is given as a path from `FFXII TZA/` and was **not** audited for this
report. The work was split into ten page groups (the subsection numbers 1.1–1.10, 2.1.1–2.1.10 and so on follow
them); identifiers in parentheses after a `G-n` id (for example `G-12 (G1-resslot)`) are the group reader's own
labels, kept because the rating table cites them.

**Citation check.** Every quoted span with a citation (984 of them) was compared by script with the cited lines of
the snapshot. All but six matched; the six are table cells quoted as `a | b`, quotes with a link or a code-block gap
elided, a footnote quoted with an elision across two lines, and a word ("Thirteen") cited against a list of lines. Where a quote starts one or two lines above the cited
line, the citation was moved to the line where the quote starts.

| alias | page | lines |
|---|---|---:|
| `README` | `README.md` | 80 |
| `BOOT` | `what-the-engine-fixes-at-boot.md` | 590 |
| `C-BOOT` | `CONTRACT-boot-fixups.md` | 846 |
| `FLOAT` | `Startup-Data-Construction/generated-float-table-builders.md` | 652 |
| `APP` | `Application-Root/game-application.md` | 2,464 |
| `TICK` | `Battle-Frame/the-world-tick-and-the-field-frame.md` | 2,815 |
| `C-TICK` | `Battle-Frame/CONTRACT-world-simulation-tick.md` | 343 |
| `FORCE` | `Force-Fight-Mode/force-fight-mode.md` | 419 |
| `GATE` | `Per-Frame-Update-Gate/one-word-decides-which-fifteen-subsystems-tick.md` | 570 |
| `C-GATE` | `CONTRACT-per-frame-update-gate.md` | 1,836 |
| `STOP` | `System-Stop-Registry/the-time-stop-and-system-stop-registry.md` | 849 |
| `C-STOP` | `System-Stop-Registry/CONTRACT-system-stop-registry.md` | 348 |
| `MODE` | `Battle-Runtime-Mode/battle-runtime-mode-ladder.md` | 1,439 |
| `C-MODE` | `Battle-Runtime-Mode/CONTRACT-battle-runtime-mode.md` | 673 |
| `LOG` | `Diagnostics-Logging/the-formatted-log-call-and-its-level-gate.md` | 415 |
| `DUP` | `duplicated-function-names-and-how-to-resolve-them.md` | 423 |
| `ONES` | `the-all-ones-empty-convention.md` | 402 |
| `EID` | `the-encoded-id-space-and-the-query-record.md` | 1,178 |
| `CLS` | `the-encoded-id-class-registry.md` | 652 |
| `C-EID` | `CONTRACT-encoded-id-space-and-class-registry.md` | 423 |
| `QREC` | `the-query-record-from-initialization-to-reuse.md` | 234 |
| `BASIS` | `the-basis-column-helpers.md` | 195 |
| `ABI` | `ABI-Recovery/derived-call-signatures.md` | 350 |
| `EEVU` | `Shared-Transform-Workbench/the-ee-and-vu0-register-bank.md` | 390 |
| `SAVE` | `Shared-Transform-Workbench/the-workbench-has-a-save-and-restore-and-nine-functions-use-it.md` | 391 |
| `WB` | `Shared-Transform-Workbench/the-shared-transform-workbench.md` | 734 |
| `PRIM` | `Shared-Transform-Workbench/the-two-transform-primitives.md` | 1,680 |
| `C-WB` | `CONTRACT-shared-transform-workbench.md` | 247 |
| `C-SAVE` | `CONTRACT-transform-workbench-save-restore.md` | 488 |
| `C-PRIM` | `CONTRACT-transform-primitives.md` | 512 |
| `RTTI` | `Object-Model/rtti-vtable-object-model.md` | 1,161 |
| `VTIDX` | `Object-Model/vtable-method-index.md` | 5,219 |
| `HUBS` | `Shared-State-Accessors/cross-subsystem-accessor-hubs.md` | 956 |
| `NBR` | `Shared-State-Accessors/the-shared-neighbours-pass-22-keeps-finding.md` | 479 |
| `OWN` | `Ownership-Boundary/intentionally-ownerless-functions-and-shared-scratch.md` | 1,017 |
| `C-CON` | `Developer-Tuning-Console/CONTRACT-developer-tuning-console.md` | 443 |
| `CON282` | `Developer-Tuning-Console/the-282-command-parameter-console.md` | 616 |
| `TUNES` | `Developer-Tuning-Console/what-the-console-tunes.md` | 1,269 |
| `CON2` | `Developer-Tuning-Console/the-second-console-table.md` | 319 |
| `EVSLOT` | `Developer-Tuning-Console/the-event-slot-panel-and-its-dead-feeder.md` | 354 |
| `CMDNAMES` | `Developer-Tuning-Console/console-command-names.md` | 439 |
| `ARMDIV` | `Developer-Tuning-Console/ARM-CATALOGUE-WORK-DIVISION.md` | 612 |
| `ARM-A` | `Developer-Tuning-Console/arm-catalogue-slice-A-ids-12-43.md` | 422 |
| `ARM-B` | `Developer-Tuning-Console/arm-catalogue-slice-B-ids-44-75.md` | 440 |
| `ARM-C` | `Developer-Tuning-Console/arm-catalogue-slice-C-ids-76-107.md` | 359 |
| `ARM-D` | `Developer-Tuning-Console/arm-catalogue-slice-D-ids-108-139.md` | 480 |
| `ARM-E` | `Developer-Tuning-Console/arm-catalogue-slice-E-ids-140-171.md` | 495 |
| `ARM-F` | `Developer-Tuning-Console/arm-catalogue-slice-F-ids-172-203.md` | 458 |
| `ARM-G` | `Developer-Tuning-Console/arm-catalogue-slice-G-ids-204-235.md` | 317 |
| `ARM-H` | `Developer-Tuning-Console/arm-catalogue-slice-H-ids-236-267.md` | 387 |
| `ARM-I` | `Developer-Tuning-Console/arm-catalogue-slice-I-ids-268-293.md` | 417 |

## Pages read

All 51 pages were read: every line of prose, front matter, status and correction text (the `VTIDX`
appendix rows were counted and sampled by script). The status columns are as each page states them.

| alias | front-matter status / readiness | `last_reviewed` · `audit.last_pass` | body banner(s) that state a status | lines |
|---|---|---|---|---|
| README | no front matter; `\| Status \| see [`../_index/COVERAGE.md`]…` (README:9) | none | per-page status claims README:14, 25, 29, 33, 37, 45, 50, 59, 64 (see C.2) | 1-80 (all) |
| BOOT | "DOCUMENTED — every register row is closed (owner re-status 2026-09-30, OPUS) — no registered residue left …" (BOOT:4) | last_reviewed 2026-09-30 (BOOT:18) · audit.last_pass 2026-09-03 (BOOT:22), passes 1 (BOOT:21), falsification_passes 1 (BOOT:19), crossref_clean false (BOOT:24) | none beyond front matter; dated "Answered/ANSWERED 2026-09-30" boxes BOOT:183, 201-205, 298-311; page has 2026-10-01 section BOOT:540 | 1-590 (all) |
| C-BOOT | no `status:`; "readiness: BEHAVIORALLY UNDERSTOOD" (C-BOOT:6), "confidence: PROVEN" (C-BOOT:7), level L2 (C-BOOT:5) | last_reviewed 2026-09-29 (C-BOOT:15) · audit.last_pass 2026-09-29 (C-BOOT:18), kind falsification (C-BOOT:19), but `by: OPUS` / `date: 2026-09-20` (C-BOOT:21-22) | "NOTHING IS SCORED HERE" (C-BOOT:441, 444); §14 Unresolved C-BOOT:478-499 | 1-846 (all) |
| FLOAT | "DOCUMENTED — every question the page asks is answered: … owner read 2026-09-30 (OPUS, …)" (FLOAT:4) | last_reviewed 2026-09-02 (FLOAT:18) · audit.last_pass 2026-09-02 (FLOAT:21), passes 2 (FLOAT:20), falsification 2026-09-02 "6 claims overturned, 11 survived" (FLOAT:24-26) | "**Status is `PARTIAL` deliberately.**" (FLOAT:55) with superseding note "The status word stays until the owner read; 2026-09-30" (FLOAT:56-58); banner "Identity found 2026-09-13 …" (FLOAT:31-39) | 1-652 (all) |
| APP | "status: AUDITED" (APP:4) | last_reviewed 2026-09-02 (APP:18) · audit.last_pass 2026-09-02 (APP:21), passes 4 (APP:20), crossref_clean true (APP:23) | "### Status … **This document has now had its first falsification pass.**" (APP:443-448); page carries dated edits to 2026-10-01 (APP:2404, 2121) | 1-2464 (all; long interior-citation tables read row by row) |
| TICK | `status: AUDITED` (TICK:4); `readiness: BEHAVIORALLY UNDERSTOOD` (TICK:8); `confidence: PROVEN` (TICK:9); `level: L1` (TICK:7) | `last_reviewed: 2026-09-10` (TICK:16) · `last_pass: 2026-09-12`, `last_pass_kind: authored`, `crossref_clean: false` (TICK:19-22) | none in body; README:63-64 calls it "**DOCUMENTED, tier 1.**" | 2815, all read |
| C-TICK | `readiness: CONTRACT READY` (C-TICK:6); `confidence: PROVEN` (C-TICK:7); `level: L2` (C-TICK:5) | `last_reviewed: 2026-09-29` (C-TICK:20) · `last_pass: 2026-09-29`, `last_pass_kind: falsification`, `crossref_clean: false` (C-TICK:23-26) | "**Authored 2026-09-22 by FABLE.**" (C-TICK:32); "## Falsification pass 1 — 2026-09-29 (OPUS): every invariant survives" (C-TICK:328) | 343, all read |
| FORCE | `status: AUDITED` (FORCE:4); no `readiness:` key (not stated) | `last_reviewed: 2026-09-02` (FORCE:18) · `last_pass: 2026-09-02`, `last_pass_state: falsification-pass`, `crossref_clean: true` (FORCE:21-23) | "**DOCUMENTED.** The flag, both its readers, its setter, its feature enable, the script verb that drives it, and its fifteen consumers are all read." (FORCE:32-33) | 419, all read |
| GATE | `status: AUDITED — the other fourteen groups (UQ-28, ten by mechanism and four by call shape) and the node type (UQ-25, the target-line object) answered 2026-09-17; UQ-27 and UQ-29 closed earlier` (GATE:4); `readiness: SEMANTICALLY IDENTIFIED` (GATE:8); `confidence: PROVEN` (GATE:9) | `last_reviewed: 2026-09-11` (GATE:17) · `last_pass: 2026-09-13` (GATE:21), `passes: 1` (GATE:20), `falsification_passes: 2` (GATE:18) | "**Count restated 2026-09-11 (OPUS-FRAMEGATE-16TH):** … a reimplementer counting groups needs **sixteen**" (GATE:29); "## 10. Reopened 2026-09-08 — nothing writes the enable word…" (GATE:277) | 570 (all read) |
| C-GATE | `readiness: BEHAVIORALLY UNDERSTOOD` (C-GATE:6); `confidence: PROVEN` (C-GATE:7); `crossref_clean: false` (C-GATE:22) | `last_reviewed: 2026-09-11` (C-GATE:17) · `last_pass: 2026-09-12` (C-GATE:20) | "## 15a. Falsification pass 1 — 2026-09-12 (OPUS), SURVIVED" (C-GATE:337); "**Evidence class: isolated original-code. Live capture: still absent…**" (C-GATE:214) | 1836 (all prose read; §§ after 1338 are per-function notes, all read) |
| STOP | `status: AUDITED — the registry, its ids and its consumers read; …(SM-5…) answered 2026-09-18; … (SM-3)…(SM-2)…(SM-1) answered 2026-09-17` (STOP:4); **no `readiness:` line in front matter** (STOP:1-17) | `last_reviewed: 2026-09-12` (STOP:10) · `last_pass: 2026-09-12` (STOP:13) | "Authored by FABLE, 2026-09-12." (STOP:27) | 849 (all read) |
| C-STOP | `readiness: CONTRACT READY` (C-STOP:6); `level: L2` (C-STOP:5); `crossref_clean: false` (C-STOP:26) | `last_reviewed: 2026-09-29` (C-STOP:20) · `last_pass: 2026-09-29` (C-STOP:23) | "**Authored 2026-09-22 by FABLE.**" (C-STOP:32); "## Falsification pass 1 — 2026-09-29 (OPUS): every invariant survives" (C-STOP:305) | 348 (all read) |
| MODE | MODE:5 "status: AUDITED — the ladder and its six modes read (O-4 answered 2026-09-12: summon, chocobo, the field bit, the two event-party modes); the 0035BC50 and 00313DB0 sections' lists are all ticked; status line brought up to date 2026-09-18 (FABLE)"; no `readiness:` field | MODE:18 `last_reviewed: 2026-09-12` · MODE:21 `last_pass: 2026-09-02` (MODE:22 `falsification-pass`) | MODE:35 "**PARTIAL.** The ladder, its inputs and its persistence are read at tier 1." ; MODE:38-39 "What keeps the page PARTIAL is the residue of the two consumers opened below" | 1439 |
| C-MODE | C-MODE:6 `readiness: CONTRACT READY`; C-MODE:7 `confidence: PROVEN`; C-MODE:5 `level: L2` | C-MODE:17 `last_reviewed: 2026-09-12` · C-MODE:20 `last_pass: 2026-09-12`; C-MODE:22 `crossref_clean: false` | C-MODE:263-264 "**Evidence class: isolated original-code. Live capture: still absent, and that is the gate this subsystem fails.**" | 673 |
| LOG | LOG:4 "status: AUDITED — the sink class (Phyre::PTTYCallback) and slot 1's behaviour answered 2026-09-18 (§7) …"; LOG:8 `readiness: SIGNATURE RESOLVED`; LOG:7 `level: L1`; LOG:25 "promoted: 2026-10-01 DOCUMENTED -> AUDITED" | LOG:17 `last_reviewed: 2026-09-08` · LOG:21 `last_pass: 2026-09-13` | LOG:30-31 "**The filename still says `level-gate`.** … **there is no level gate** (§9, 2026-09-13)"; LOG:41 "**⚠ Corrected 2026-09-13 (§9) — there is no level gate.**"; LOG:117 "**⚠ The whole "gate" reading below is withdrawn (2026-09-13, §9).**" | 415 |
| DUP | DUP:4 `status: AUDITED`; no `readiness:` field | DUP:20 `last_reviewed: 2026-09-03` · DUP:23 `last_pass: 2026-09-13` | none stating a status | 423 |
| ONES | ONES:4 `status: AUDITED`; no `readiness:` field | ONES:19 `last_reviewed: 2026-09-03` · ONES:22 `last_pass: 2026-09-13` | none stating a status | 402 |
| EID | `status: "REOPENED — SECTION-05 corrects producer semantics; historical audit retained, independent acceptance pending"` (EID:4); `production_review: "SECTION-05 original-code controls; historical corpus/caller work not newly certified"` (EID:20) | last_reviewed 2026-09-22 (EID:19) · last_pass 2026-09-12 (EID:47) | "The full current specification is [from initialization to reuse]…" (EID:169); "**The following FY-3 consumer census is retained as historical bounded evidence, not a new exhaustive consumer proof.**" (EID:196-197); open box "**OV-5.** SECTION-05: shipped-state reachability … and formal independent acceptance." (EID:608-609) | 1-1178 |
| CLS | `status: "DOCUMENTED — the SECTION-05 validator/filler reopening is resolved (SECTION-05 accepted by a non-author review 2026-09-29); row layouts SUPERSEDED under UQ-80's class-1 ruling; which classes code passes is answered (RC-1: 26 named; 4, 16, 22 and 27 by no caller)…"` (CLS:4) | last_reviewed 2026-09-22 (CLS:19) · last_pass 2026-09-13 (CLS:22); `crossref_clean: false` (CLS:24) | "*The trigger this page was reopened for is resolved (2026-09-30, SWE2-CONTRACT, cited, not re-run).* SECTION-05 is accepted by a non-author review" (CLS:50-51) | 1-652 |
| C-EID | `readiness: BEHAVIORALLY UNDERSTOOD` (C-EID:6), `confidence: PROVEN` (C-EID:7); `production_review: "SECTION-05; locally validated, independent acceptance pending; prior audit metadata is historical"` (C-EID:14) | last_reviewed 2026-09-30 (C-EID:13) · last_pass 2026-09-30 (C-EID:17) but `date: 2026-09-21` (C-EID:21) | "**Current specification: SECTION-05 (2026-09-22), local production complete; independent acceptance pending.**" (C-EID:26-27); "Falsification pass 1 — 2026-09-30 (OPUS): ten clauses survive; one premise in §14 is broken" (C-EID:382) | 1-423 |
| QREC | `status: PARTIAL` (QREC:4); `readiness: BEHAVIORALLY UNDERSTOOD` (QREC:7); `production_acceptance: "local checks passed; formal peer acceptance pending"` (QREC:12) | last_reviewed 2026-09-22 (QREC:11) · last_pass 2026-09-29 (QREC:15) | "Falsification pass 1 — 2026-09-29 (OPUS): every structural clause survives" (QREC:203); open box "**OV-8.** Actual game reachability…" (QREC:196) | 1-234 |
| BASIS | `status: AUDITED` (BASIS:4); `falsification_passes: 1` (BASIS:20) | last_reviewed 2026-09-03 (BASIS:19) · last_pass 2026-09-03 (BASIS:23); `crossref_clean: false` (BASIS:25) | "**Cited by no document in this database.**" (BASIS:31) | 1-195 |
| ABI | `status: DOCUMENTED — every register row is closed: …` (ABI:4) | last_reviewed 2026-09-29 (ABI:11) · last_pass 2026-09-13 (ABI:14); `crossref_clean: false` (ABI:20) | "**This page disposes of nothing and does not move the EC-7 frontier**" (ABI:37-38) | 1-350 |
| EEVU | EEVU:4 "status: DOCUMENTED — the translated-vs-C split (UQ-38) is OUT OF EVIDENCE BOUNDARY (2026-09-28 …) … Re-statused 2026-09-29 (FABLE)"; no readiness key | EEVU:12 `2026-09-14` · EEVU:15 `2026-09-14` (falsification EEVU:18 `2026-09-14`; EEVU:19 "crossref_clean: false") | EEVU:25 "**The 1.5 KB area this database calls the shared transform workbench is the register set of a PS2 CPU, kept in memory.**"; EEVU:322 "Zero defects found." | 1-390 (all read) |
| SAVE | SAVE:9 "status: AUDITED — the nine users placed (UQ-41), the lanes' signed ceiling (UQ-42) and the computation's meaning (UQ-43) all answered 2026-09-17"; SAVE:7 "readiness: BEHAVIORALLY UNDERSTOOD"; SAVE:8 "confidence: PROVEN" | SAVE:17 `2026-09-08` · SAVE:21 `2026-09-13` | SAVE:183 "### SUPERSEDED 2026-09-08 — that is the `b = 0` case of a three-operand rule" | 1-391 (all read) |
| WB | WB:4 "status: AUDITED"; no readiness key | WB:18 `2026-09-02` · WB:21 `2026-09-02` | WB:34 "> **IDENTIFIED 2026-09-14 (FABLE): the area is the register bank of the PS2 assembly emulation.**"; WB:485 "`DOCUMENTED`, one falsification pass." | 1-734 (all read) |
| PRIM | PRIM:7 "status: AUDITED"; PRIM:8 "readiness: BEHAVIORALLY UNDERSTOOD   # §5a adds live observation of the STATE, not of the functions running"; PRIM:9 "confidence: PROVEN" | PRIM:17 `2026-09-08` · PRIM:21 `2026-09-13` | PRIM:29-32 "*2026-09-14 (FABLE):* the "workbench" is the register bank of the PS2 assembly emulation … The laws below were measured by execution and stand." | 1-1680 (all read) |
| C-WB | C-WB:6 "readiness: CONTRACT READY"; C-WB:7 "confidence: PROVEN" | C-WB:19 `2026-09-29` · C-WB:22 `2026-09-29` (C-WB:25 "crossref_clean: false") | C-WB:241 "No correction." | 1-247 (all read) |
| C-SAVE | C-SAVE:6 "readiness: BEHAVIORALLY UNDERSTOOD"; C-SAVE:7 "confidence: PROVEN" | C-SAVE:17 `2026-09-11` · C-SAVE:20 `2026-09-12` (C-SAVE:22 "crossref_clean: false") | C-SAVE:250 "**Evidence class: isolated original-code. Live capture: still absent.** (2026-09-12)"; C-SAVE:390 "## 15a. Falsification pass 1 — 2026-09-12 (OPUS), SURVIVED" | 1-488 (all read) |
| C-PRIM | C-PRIM:6 "readiness: DIFFERENTIAL TESTED   # … original axis: NOT runtime validated (section 13)"; C-PRIM:7 "confidence: PROVEN" | C-PRIM:11 `2026-09-17` · C-PRIM:21 `2026-09-12` | C-PRIM:172 "**Evidence class: isolated original-code. The two laws have NOT been observed in the running game.**"; C-PRIM:215 "Verdict `FAIL_INCOMPLETE`." | 1-512 (all read) |
| RTTI | `status: AUDITED` (RTTI:4); `evidence_tier: 1` (RTTI:6); `last_pass_state: novelty-claims-retracted-corroboration-established` (RTTI:26) | `last_reviewed: 2026-09-02` (RTTI:22) · `last_pass: 2026-09-02` (RTTI:25); provenance "re-verified 2026-09-21 (OPUS)" (RTTI:14) | "> **CORRECTED.** This paragraph first said Bullet was present "not Phyre's"." (RTTI:50); "> **RETRACTED.** This section was first headed *"Libraries this names for the first time"*" (RTTI:211); "**PARTLY RETRACTED — the surplus rows ARE folded code…**" (RTTI:734); "**RETRACTED — section 13.**" (RTTI:754) | 1,161 (all read) |
| VTIDX | `status: AUDITED` (VTIDX:4); `evidence_tier: 1` (VTIDX:6); `last_pass_state: four-attacks-survived-discharged-GN158` (VTIDX:23) | `last_reviewed: 2026-09-02` (VTIDX:19) · `last_pass: 2026-09-02` (VTIDX:22); provenance "re-verified 2026-09-21 (OPUS)" (VTIDX:14) | "its open question, **B-3**, then sat at *RECOVERED — NOT YET APPLIED*. This document applies it" (VTIDX:29-30); "## 14. RETRACTION — the unreached figure was wrong by 8.5x" (VTIDX:2614); "~~no vtable, no call, no taken address~~ … **RETRACTED — §14**" (VTIDX:2575) | 5,219 (all prose/headings/updates read; appendix table 240-2455 counted by script, sampled) |
| HUBS | `status: AUDITED` (HUBS:4); `last_pass_state: falsification-superlative-overturned-tables-exact` (HUBS:22) | `last_reviewed: 2026-09-02` (HUBS:18) · `last_pass: 2026-09-02` (HUBS:21), `passes: 2` (HUBS:20) | none in body; README lists it as "**DOCUMENTED, tier 1.**" (README:59) | 1-956 (all read) |
| NBR | `status: AUDITED — the last open box (UQ-32: the slot records, bit 7 of +0x10, and its first setter 0026C8C0) answered 2026-09-17, with UQ-33 and UQ-34` (NBR:4); `last_pass_state: OPUS-falsification-headline-falsified-sizes-and-caller-counts-hold` (NBR:16) | `last_reviewed: 2026-09-14` (NBR:12) · `last_pass: 2026-09-14` (NBR:15), `passes: 1` (NBR:14) | §10.4: "Those numbers are **historical, as of the run that produced them**" (NBR:433) | 1-479 (all read) |
| OWN | `status: AUDITED` (OWN:4); `last_pass_state: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2` (OWN:23 — a hash, not a state) | `last_reviewed: 2026-09-02` (OWN:19) · `last_pass: 2026-09-02` (OWN:22), `passes: 1` (OWN:21) | "`DOCUMENTED`, one falsification pass." (OWN:490); README: "**DOCUMENTED, tier 1, one falsification pass.**" (README:37) | 1-1017 (all read) |
| C-CON | `readiness: BEHAVIORALLY UNDERSTOOD` (6); `confidence: PROVEN` (7) | `last_reviewed: 2026-09-21` (19) · `last_pass: 2026-09-29` (22), `passes: 1` (21), `crossref_clean: false` (24) | "**Provenance.** Sections 2–5, 7 and 10 are **NATIVE/STATIC**, re-derived here. … Section 13 is **empty**." (37-38); "**Empty.** The console is a developer build's menu; nothing here has been observed running." (297); "`crossref_clean` stays `false`." (399) | 444 |
| CON282 | `status: DOCUMENTED — UQ-22, UQ-23 and RC-4 are ANSWERED and every box on the page is closed (owner re-status 2026-09-30, OPUS) …` (4) | `last_reviewed: 2026-09-03` (18) · `last_pass: 2026-09-03` (21), `passes: 1` (20), `crossref_clean: true` (23) | "`audit.passes` 0 → 1. **Status stays `PARTIAL`.**" (501) | 617 |
| TUNES | `status: DOCUMENTED — the rate at which PhyreEngine invokes slot 8 answered … owner read 2026-09-30 (OPUS, …)` (4) | `last_reviewed: 2026-09-03` (18) · `last_pass: 2026-09-12` (21), `passes: 1` (20), `crossref_clean: false` (23) | "**passes: 1 · last_pass: 2026-09-12**" (1063) | 1270 |
| CON2 | `status: DOCUMENTED — what the codes name answered 2026-09-30 …` (4) | `last_reviewed: 2026-09-03` (19) · `last_pass: 2026-09-03` (23), `falsification_passes: 1` (20), `crossref_clean: false` (25) | none beyond front matter | 320 |
| EVSLOT | `status: CORRECTED — earlier "dead feeder" verdict retracted; … the one open item is RC-5 …` (4-8) | `last_reviewed: 2026-09-29` (17) · `last_pass: 2026-09-29` (20), `last_pass_kind: falsification` (21) | title "# The event slot panel and its live feeder" (25) (the file name still says `dead-feeder`) | 355 |
| CMDNAMES | `status: AUDITED — the 3.9 falsification item resolved 2026-09-18: …` (4) | `last_reviewed: 2026-09-03` (19) · `last_pass: 2026-09-03` (23), `falsification_passes: 1` (20), `crossref_clean: true` (25) | "**GENERATED — do not hand-edit.**" (31) | 440 |
| ARMDIV | `status: AUDITED` (ARMDIV:4); `last_pass_state: cross-slice-figures-rederived-from-image-two-corrections` (ARMDIV:19); `crossref_clean: true` (ARMDIV:20) | `last_reviewed: 2026-09-13` (ARMDIV:14) · `last_pass: 2026-09-13` (ARMDIV:18) | "**What this page is now.** It began as the work order … The slices are delivered" (ARMDIV:25-26); History banner "## SLICES B-I ARE OPEN - hold cleared 2026-09-03" (ARMDIV:80); "**96 of 282 ids catalogued; 186 remain.**" (ARMDIV:290); "**The table is closed.** Nine slices, five sessions, every action id catalogued." (ARMDIV:456) | 613 |
| ARM-A | `status: AUDITED` (ARM-A:4); `crossref_clean: false` (ARM-A:25) | `last_reviewed: 2026-09-03` (ARM-A:19) · `last_pass: 2026-09-03` (ARM-A:23) | "**`passes: 1` here means one pass happened, not that the document is finished.**" (ARM-A:331-332) | 423 |
| ARM-B | `status: AUDITED` (ARM-B:4); `crossref_clean: false` (ARM-B:25) | `last_reviewed: 2026-09-03` (ARM-B:19) · `last_pass: 2026-09-03` (ARM-B:23) | same `passes: 1` banner (ARM-B:255-256) | 441 |
| ARM-C | `status: AUDITED` (ARM-C:4); extra `parent_tag: GN159` (ARM-C:19) beside `parent_tag: GN162` (ARM-C:12) | `last_reviewed: 2026-09-03` (ARM-C:20) · `last_pass: 2026-09-03` (ARM-C:24) | same banner (ARM-C:304-305) | 360 |
| ARM-D | `status: AUDITED` (ARM-D:4); `parent_tag: GN159` (ARM-D:18) beside GN162 (ARM-D:12) | `last_reviewed: 2026-09-03` (ARM-D:19) · `last_pass: 2026-09-03` (ARM-D:23) | "> **Flagged 2026-09-08, unresolved.**" (ARM-D:128); same banner (ARM-D:435-436) | 481 |
| ARM-E | `status: AUDITED` (ARM-E:4); `parent_tag: GN159` (ARM-E:18) | `last_reviewed: 2026-09-03` (ARM-E:19) · `last_pass: 2026-09-03` (ARM-E:23) | same banner (ARM-E:408-409) | 496 |
| ARM-F | `status: AUDITED` (ARM-F:4); `parent_tag: GN159` (ARM-F:19) | `last_reviewed: 2026-09-03` (ARM-F:20) · `last_pass: 2026-09-03` (ARM-F:24) | same banner (ARM-F:361-362) | 459 |
| ARM-G | `status: AUDITED` (ARM-G:4); `parent_tag: GN159` (ARM-G:19) | `last_reviewed: 2026-09-03` (ARM-G:20) · `last_pass: 2026-09-03` (ARM-G:24) | same banner (ARM-G:267-268) | 318 |
| ARM-H | `status: AUDITED` (ARM-H:4); `parent_tag: GN159` (ARM-H:19) | `last_reviewed: 2026-09-03` (ARM-H:20) · `last_pass: 2026-09-03` (ARM-H:24) | same banner (ARM-H:349-350) | 388 |
| ARM-I | `status: AUDITED` (ARM-I:4); `parent_tag: GN159` (ARM-I:19) | `last_reviewed: 2026-09-03` (ARM-I:20) · `last_pass: 2026-09-03` (ARM-I:24) | same banner (ARM-I:359-360) | 418 |

**Member files** (used only to confirm layouts and counts; no item below rests on a member file alone):

| file | rows | checked against | result |
|---|---:|---|---|
| Startup-Data-Construction/members/builder-store-extents.tsv | 75 (76 lines), 16 columns every row | FLOAT:108-109 (26+40=66 pairs, 65 builders), FLOAT:253-254 (28 / 49 calls, `004E3110` twice), FLOAT:510-513 (memset 18, `008631D0` 40, `008631E0` 29, none 15), FLOAT:622 (74 objects with a next pointer, 66 exact; 5 in-band memset-less short), FLOAT:631 (16 helper-less incl. `0047E140`) | AGREE: per hub 27 + 48 rows; band=1 rows 26 + 40 = 66, 65 distinct builders (`004E3110` duplicated); in-band memset 18, hdr 40, reg 29, none 15; 74 rows with a gap, 66 extent==gap; 16 helper-less rows (15 in band + `0047E140`); last object `02AED330` has no gap. DISAGREE/NOTE: (a) total rows = 75 objects, not 66 (see C.1 counts); (b) row `02AE8900 004F4F80` gap `0x2E0` vs FLOAT:528 gap `0x530` (FLOAT's table measures to the next in-band pointer); (c) row `02AE9290 004DA3C0 hdr+memset` extent `0x70` gap `0x280`, memset size `-` — not in FLOAT's 17-row memset table (FLOAT:519-537) nor in FLOAT:622's five short objects (G.2); (d) the tail-jump builders `004A8860` (`02AE1EF0`, C-BOOT:683) and `004C3610` (C-BOOT:521, 617) have no row. |
| Startup-Data-Construction/members/bh3_hubs.py, builder_store_census.py, builder_store_extents.py | scripts (63/88/57 lines) | FLOAT:252, 324-325 | consistent: `builder_store_extents.py:4` "Band = 00480000-004FFFFF (the page's 66)"; `builder_store_census.py:1` "the 66 hub-called builders" (page says 65 builders / 66 pairs — wording only). |
| Application-Root/boot-singleton-01f7f598-accesses.tsv | 249 (250 lines), 8 columns every row | not cited by APP (no link found); nearest text APP:1044-1088 (`01F7F598` singleton) and APP:491 (size `0xDD8`) | Columns `function name site disp kind instruction route note`; 7 functions (`00184CE0`, `00184E60`, `00184F20`, `00186CD0`, `00189C20`, `0062DD10`, `006CB5F0`), kinds w 218 / r 22 / addr 9, route all "ctor-seeded 01F7F598" (31 "zeroclear"), 182 distinct disps, max `0xDD0` (< `0xDD8`, agrees with APP:491). NOTE: 22 rows (all `00186CD0`) fall inside the spans APP:1061-1062 calls previously "unobserved" (`+0xB08`…`+0xB78`, `+0xCE0`…`+0xD08`); APP says the slot-load census found 0 there and states no ctor-seeded count. No row count stated on APP to check. |
| `stick-world-vector-022c7fd0-accesses.tsv` | 10 (8 columns all rows) | TICK:1155 | **disagrees in coverage**: TSV lists only `004742A0` as accessor of `022C7FD0` (all 10 rows writes); TICK:1155 says `00358C60` "copies the 16 bytes at `008C5FD0` to `022C7FD0`" (`00358C6D` movaps) — that writer is absent from the TSV. No page states the TSV's row count (not stated). |
| `stick-basis-022c7fa0-accesses.tsv` | 35 (8 columns) | TICK:511 (`004742A0` … `00380800`) | consistent: TSV accessors are `004742A0` (22 rows), `00380800` (10), `004745B0` (3); TICK:511 names `004742A0` calling `00380800`. `022C7FA0` itself is named on none of my pages; row count not stated. |
| `manager-sub-8fa0-slot-record-02b8-accesses.tsv` | 60 (8 columns; kinds r 32 / w 17 / rw 9 / addr 2) | none of TICK/C-TICK/FORCE name `_8FA0` or `0x2B8`; cross-checked C-GATE:593 (`+0xAC0` to `002BE300`/`002BEA40`) | route note "ManagerSub0209BE80_8FA0 +0xAC0 stride=0x2B8 count=2" agrees with C-GATE:593/1706 (outside my pages); row count stated nowhere. |
| Per-Frame-Update-Gate/manager-singleton-0209be80-accesses.tsv | 1435 | "the **136 bodies that load the slot `0209BE80`**" (GATE:444, C-GATE:444); "143-body closure" (C-GATE:690) | 203 distinct functions, all `route-seeded PTR 0x0209BE80`. The tsv counts a closure, so the populations differ: **does not reproduce 136 or 143** |
| …/manager-sub-0209be80-00a0-accesses.tsv | 83 | `_00A0` "9 offsets" over "+0x0–+0xC and +0x52A0–+0x52C6" (C-GATE:607) | 17 distinct disps, max 0x52C6; the extreme matches but the count does not |
| …/manager-sub-0209be80-57e0-accesses.tsv | 472 | `_57E0` "32 offsets", "+0x0–+0x26AE" (C-GATE:609) | 126 distinct disps, max 0x26B3; count and range differ (the tsv includes "exposed" helper routes) |
| …/manager-sub-0209be80-7ea0-accesses.tsv | 124 | `_7EA0` "13 offsets", "+0x0–+0x76" (C-GATE:610); GATE:254 "0028CD80 and 0028CE90 on the two 0x20-byte lanes at +0x30 and +0x50" | 20 distinct disps, max 0x76 (range agrees). The tsv places **0028CD80 on the object base** (disps 0x10, 0x20, 0x24, 0x28), not on a lane: **disagrees with GATE:254** (see C.1) |
| …/manager-sub-0209be80-7fb0-accesses.tsv | 90 | `_7FB0` "27 offsets", "+0x0–+0x104" (C-GATE:611) | 28 distinct, max 0x106; close |
| …/manager-sub-0209be80-8fa0-accesses.tsv | 187 | `_8FA0`: "every one of them lies in `+0x1030`–`+0x10FA`" / "first 4,144 bytes of this child are untouched" (C-GATE:583, 595) | 56 distinct disps, including 0x40–0xB8 and 0xAC0–0xB78, 0xD40, 0x10FC, 0x10FE: **disagrees** (part of it is the `+0xAC0` sub-object and "exposed" helper routes) |
| …/manager-sub-0209be80-a0d0-accesses.tsv | 9 | `_A0D0` "2 offsets", "`+0x960`, `+0x984`" (C-GATE:613) | 5 disps (0x0, 0x960, 0x964, 0x974, 0x984); GATE:503 itself names `+0x974`; **count disagrees** |
| …/manager-sub-0209be80-ab30-accesses.tsv | 149 | `+0x710` writer/reader `00296490`/`00296960` (C-GATE:551-552); `+0x61CC` (C-GATE:717) | rows present at 002964BA/0029696A; max disp 0x61CC: **agrees** |
| …/manager-sub-57e0-array-record-accesses.tsv | 30 | claim-slot records at `_57E0+0x270` (C-GATE:1225-1227) | route `ManagerSub0209BE80_57E0+0x270`: **agrees** on base |
| manager-sub-00a0e-ntry-accesses.tsv (00 root) | 51 | `_00A0` memset at `+0x4020` (C-GATE:627, 1824) | route `+0x20 stride=0x100 count=64` ends at +0x4020: **consistent** |
| manager-sub-0209be80-5380-accesses.tsv (root) | 65 | `_5380` `+0x420/+0x428/+0x430` (C-GATE:626) | present; no count stated |
| manager-sub-5380-pool-a/b/c-entry-accesses.tsv (root) | 41 / 2 / 2 | `_5380` "6 offsets", "+0x0–+0x430" (C-GATE:608) | pools at +0x0 (0x30×12), +0x240 (0x28×6), +0x330 (0x28×6), ending at +0x420: **consistent** with the triple at +0x420 |
| manager-sub-7ea0e-ntry-accesses.tsv (root) | 50 | "two `0x20`-byte lanes at `+0x30` and `+0x50`" (GATE:254) | route `+0x30 stride=0x20 count=2`; only **0028CE90** uses it (disps 0x10–0x18). **Agrees** for 0028CE90 |
| manager-sub-7fb0-record-accesses.tsv (root) | 95 | `00296860`: "`n` entries of `0x110` bytes from `+0x104`" (GATE:254) | route `_7FB0 +0x0 stride=0x110 count=6`: the tsv starts at +0x0, the page at +0x104: **disagrees on base** |
| manager-sub-0d0-record-accesses.tsv (root) | 1 | — | one row (`0028E43D lea rcx,[rbx+0xa0d0]`, route `_A0D0 stride=0x110 count=2`); not stated by any page |
| System-Stop-Registry/system-stop-record-accesses.tsv | 121 | "`00226B30` walks both record arrays … 56 records … writes only the first qword … and byte `+0x14`" (C-STOP:105-107); "`+0x08` qword and `+0x15`–`+0x17` — are still unobserved" (C-STOP:243-244) | route `stride=0x18 count=56` plus `+0x540 … count=2`: **agrees**. But **00227680 writes `+0x8`** six times (00227698, 002277A1, 0022793E, 00227C0E, 00227C46, 00227C82): **disagrees with C-STOP:243-244** |
| System-Stop-Registry/system-stop-registry-accesses.tsv | 3 | base `01FD4160` (STOP:43); `lea r12,[rax+0x2a0]` for record B (STOP:44) | **agrees** |
| `manager-0209ac60-accesses.tsv` | 964 (426 functions; kinds r 742, w 179, rw 24, addr 19; every route "route-seeded STATIC 0x0209AC60 \| PTR 0x0209AC30") | MODE:895 (`0209AC30`, fields `+0xC8`/`+0xD0`/`+0xDED`), MODE:909 (`00228777` write `+0xC8`), MODE:910 (`00228856` "`dec al; mov [rcx+0xDED], al`"), MODE:1272-1276 (`002CCC70` reads `0209AC30`'s `+0x290`) | AGREE for `00228700` `00228777` 0xC8 w, `002287D0` `00228832` 0xC8 r, `002289D0` 0xD0 r ×2, `002287D0` `00228858` 0xDED w (page cites the `dec` at `00228856`, tsv the store at `00228858` — same pair). DISAGREE: no row for `002CCC70`; the only `+0x290` reads are `002C1A80`/`002C1C27` and `002CCBA0`/`002CCBA7`. Layout: 8 columns `function name site disp kind instruction route note`. |
| `manager-sub-0209ac60-02f8-00c0-accesses.tsv` | 128 (31 functions) | not cited by any of my pages | layout same 8 columns; route "CHAIN ManagerSub0209AC60_02F8 +0xC0"; nothing to compare |
| `manager-sub-0209ac60-02f8-accesses.tsv` | 83 (13 functions) | not cited | layout same; route "CHAIN Manager0209AC60 +0x2F8"; nothing to compare |
| `party-selection-registry-ptrs-022c8388-accesses.tsv` | 2 (1 function `0035BC50`, both `w` at `0035BDC3`/`0035BDDF`, disp 0 via `r14`) | MODE:725-726 "a parallel array of four resolved registry pointers runs at `022C8388` with stride 8" | consistent (writer is `0035BC50`, through a cursor register; the tsv does not show the stride) |
| ABI-Recovery/derived-call-signatures.tsv | 562 | ABI:86, ABI:90-96 (0→144, 1→163, 2→155, 3→63, 4→37), ABI:98-101 (27 lower bounds, 468 rax, 6 float, 7 spill) | agree on every figure |
| ABI-Recovery/derived-call-signatures-stack-args.tsv | 562 (570 lines = 7 `#` comment lines + header + 562; same address list as the main table) | ABI:125 ("562 rows", "12 read stack parameters", nine arity-4, `002FD420` pos 5, `008628F0` pos 5, `0085DDE0` pos 7-9, "Twenty-nine rows" unplaced) | agree (12 rows with positions; 29 rows `all_reads_placed=0`) |
| ABI-Recovery/derived-call-signatures-explained.tsv | 442 | ABI:230 (106/109/110/91/26; 19 lower bounds; 376 rax; 5 float; 6 spill) | agree |
| ABI-Recovery/derived-signatures-ctor-types.tsv | 7 (2 comment lines + header) | ABI:191 ("finds seven") | agree |
| ABI-Recovery/derived-signatures-this-types.tsv | 40 | ABI:190 ("40 sit at a vtable slot … 24 belong to one class … 16 are ICF-folded") | agree (24 single-class, 16 multi) |
| encoded-id-query-record-accesses.tsv (top-level 00) | 326, all `function = 0031C5D0` | not cited by any of the six pages (grep). Compared with EID:172, EID:187-191, EID:532-542, QREC:131-133, QREC:142, QREC:164 | agree on sites: `0031C5F0` +0x18 w; `0031CA42`/`0031CA47` +0x54 r/rw; `0031CF60` +0x38 w (`[rbx-2]`); four +0x08 writes (`0031C9B9`, `0031CF49`, `0031DBBA`, `0031DCEC`); `0031CA59` +0x50; `0031CA28`/`0031CA36` +0x44/+0x48; `0031DA71`–`0031DA9D` +0x44 RMW; `0031DFF6` +0x23; `0031E29D`–`0031E2E2` +0x25; +0x2A ×2; +0x36 ×1. **Disagrees in coverage:** max offset is 0x60; the class-10 loop's later stores (+0x40…+0x90, QREC:142) are not listed, and the loop's `lea rbx,[rbx+8]` (`0031CF67`) is recorded as disp `0x42` kind `addr`. |
| Shared-Transform-Workbench/members/ee-register-census.tsv | 267 | EEVU:40 "267 functions (389,071 bytes) … 257 of them are ARCH frontier, and 188 are cited by no page"; EEVU:135-143 (99 GPR / 32 MMI / 217 vector / 72 both / 22 vf00-only / 1 HI-LO-only `00506A40` / 79 cited, 69 frontier / 188 = 233,191 B) | AGREES on every figure (awk: 267 rows, size sum 389071, frontier A 257, cited 79 (69 frontier), uncited-frontier 188 / 233191 B, GPR 99, GPR+MMI 32, vector 217, both 72, vf00-only 22, HI/LO-only `00506A40`) |
| Shared-Transform-Workbench/members/ee-register-members.tsv | 188 | EEVU:156 "every `frontier=A / cited=no` row"; EEVU:164-169 (111 / 41 / 20 / 16) | AGREES (split column: translated 111, C+fragments 41, C-fragment 20, MMI-mixed 16) |
| Shared-Transform-Workbench/members/ee-member-calls.tsv | 267 | EEVU:261 "whole 47 / mostly 38 / C+fragments 182 … They disagree on 95 of the 188"; EEVU:259 "47 whole-shaped (5 of which FRONTIER's density instrument calls C+fragments), 31 C by both instruments, 95 undecided" | AGREES (verdict whole 47 / mostly 38 / C+fragments 182; C+fragments∧C+fragments 31; whole∧C+fragments 5; mostly∧C+fragments 5; C+fragments∧translated 95). Disagrees with the unstruck "41 C" at EEVU:262 (see C.1) |
| Shared-Transform-Workbench/ee-vu-0-register-bank-accesses.tsv | 1 | no page of the group cites it (only `_index/ADDRESS-INDEX.md:9342`) | single row: `003CCA70` site `003CCA74` `movups xmm0, xmmword ptr [rdx]` "route-seeded STATIC 0x022D8F10" — a pointer read of GPR[0]; consistent with EEVU:128-130 (pointer accesses are not attributed); no page states it |
| transform-workbench-saved-pointer-accesses.tsv (top level) | 1 | C-SAVE:350-356 (pointers `02EC0A00` 8 B/item, bound "N at 32") | AGREES: `0036D930` site `0036D969` "ARRAY 0x02EC0A00 stride=0x8 count=32" |
| transform-workbench-saved-value-accesses.tsv (top level) | 1 | C-SAVE:353-354 (values `02EC0800` 16 B/item) | AGREES: `0036D930` site `0036D977` "ARRAY 0x02EC0800 stride=0x10 count=32" |
| members/transform-workbench-saved-*.tsv | — | — | no such files exist in members/ (only the two top-level ones) |
| `Object-Model/members/zero-at-load-objects-named-by-rtti.tsv` | 369 lines − 22 `#` lines − 1 header (`global	vtable	rtti_decorated`) = **346** | RTTI:963-964 ("**346 of them resolve to an RTTI name**"), RTTI:967-974 family table | **Agree.** 3 columns every row. Families by grep: `PClassDescriptorConcrete` 261, `…WithoutDefaultConstructor` 38 (+1 that is `PClassDescriptorHeaderWithoutDefaultConstructor`), SQEX 33, `PClassDescriptorHeader` 4 — match RTTI:969-973. `02CAA0A0`→`00D249A8` is data row 4 (file line 27) as RTTI:953/958 say. `02EAD010`, `02EAD040`, `02EADD70`, `02CBB900` present (RTTI:978-979, 992). Header comment repeats 1,172 / `008C31D8-008C5678` / 450 / 346. |
| `Object-Model/p-named-semantic-descriptor-accesses.tsv` | 25 − 1 = 24 | neither RTTI nor VTIDX cites it (grep: only `_index/ADDRESS-INDEX.md` refers to it) | no page claim to check; layout `function name site disp kind instruction route note` |
| `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/members/rtti-class-vtables.tsv` (outside 00; cited by RTTI as `members/rtti-class-vtables.tsv`) | 2,287 non-`#` lines − 1 header = **2,286** | RTTI:444 ("reproduces the table's **2,286** vtable rows"), RTTI:414 ("**1,739** rows … whose mangled name ends `@Phyre@@`") | **Agree** (2,286 rows; 1,739 with mangled column ending `@Phyre@@`). Note RTTI:414's relative link resolves to `Object-Model/members/`, where the file does not exist. |
| `22-…/members/phyre-registrar-classes.tsv` (outside 00) | header only checked | RTTI:439 ("**`registrars 409`** in its own header"), RTTI:433 (399 names) | **Agree** (header: "named descriptors 399", "registrars 409"). Same broken relative path (RTTI:438). |
| Shared-State-Accessors/untagged-hub-callers.tsv | 49 (50 lines; 8 columns `hub caller size tag prev_named next_named vtable_class named_callees`) | HUBS:300-301 "(49 rows: 16 + 21 + 12)"; HUBS:302-322 per-hub address lists | AGREES: hub1=16, hub2=21, hub3=12; every address listed in HUBS:302-322 is present; the ten nav-map functions `003BD480`…`003C1070` (HUBS:310) are 10 rows; sizes match page sizes where both state them (`003B8670` 4578 = OWN:192; `0037AD40` 742 = HUBS:636; `00402F00` 545 = HUBS:644; `003DE640` 183 = HUBS:648; `0031C0F0` 174 = HUBS:652; `0032A060` 154 = HUBS:664; `002FAED0` 129 = HUBS:669; `00317D80` 94 = HUBS:628) |
| Ownership-Boundary/action-timeline-opcodes.tsv | 128 (129 lines; columns `opcode case_index case_address callees`) | OWN:502-506 "opcode `1 … 128`", "62-case jump table", OWN:536 "66 opcodes (4, 23, 64–127) are no-ops" | AGREES: 128 opcode rows; 62 distinct case indices (0-61); 66 no-op rows exactly {4, 23, 64-127}. DISAGREES: opcode 128 row reads `(inline, no call)` vs OWN:537 correction (opcode 128 calls `002EB740`); opcode 37 row lists only `003333B0` vs OWN:521 correction (37 dispatches a timeline event, kind 4); opcode 11 row lists `003ACA80` where OWN:533 names `003ACA90` for 10/11; inline-without-call rows after the opcode-128 correction are 10 (35 36 45 46 54 55 60 61 62 63) vs OWN:537 "a dozen others" |
| `members/console-tunables-consumers.tsv` | 97 data rows (103 lines: 5 `#` lines + header); columns `addr in_block arm_ids labels setting_name outside_readers` | CON282:248 "(97 rows: arm ids, labels, loader key, outside readers)"; CON282:248 "22 keyed, 14 read, 34 named or read"; CON282:249 "83 rows with no outside reader split 80 inside the block and 3 outside it"; CON282:321 "86 of them fall in one span"; CON282:329 `01F82D20` "nudged by **18** different commands" | AGREE: in_block=1 86, =0 11; keyed 22; read 14; named-or-read 34; no reader 83 (80 in block); `01F82D20` row has 18 arm ids |
| `members/scenewide-cbuffer-map.tsv` | 294 data rows (1 `#` line + header); columns `cbuffer_off hlsl_variable element_byte snapshot_off block_off tunable_addr` | CON282:250 "(294 store offsets, no two disagreeing about one offset)"; "K4 80/80"; "one layout (0x5F0 bytes, 154 variables)"; "block +0x190.. becomes mShadowCascadeProjection0..7 (0x2F0..)" | AGREE on 294 rows, 294 distinct cbuffer offsets; all 80 no-reader in-block addresses of the consumers TSV appear as `tunable_addr`; `0x2F0 mShadowCascadeProjection0 … 0x190 02CB8160` present. 148 distinct `hlsl_variable` names vs "154 variables": not directly comparable (the TSV lists only stored variables) |
| `map-lighting-tuning-02cb7fd0-accesses.tsv` (folder level) | 58 rows; columns `function name site disp kind instruction route note` | no page in this group cites it (repo grep: only `_index/ADDRESS-INDEX.md`, a tools script and an audit report). Compared with TUNES:550 "`005DC580` writes 43 offsets" and TUNES:156 `006084B0` "7 sites" | DISAGREE / different instrument: 45 `w` rows from `005DC580`, 45 distinct displacements (vs 43); 13 `r` rows from `006084B0` (vs 7 rip-relative sites; the TSV's route is "route-seeded STATIC 0x02CB7FD0 base+…") |
| `members/event_slot_setter_replay.json` | 8 shipped cases, 2 mutants, `ok: true` | EVSLOT:51-60 "**8/8 cases hold**" with the eight listed cases; EVSLOT:62 the two mutants | AGREE: 8 case keys; `push_event_minus1` marker 1 / counter1 0; `push_slot2` marker 2; mutant `must_fail` sets match |
| `members/*.py` (3 scripts) | not counted (scripts) | EVSLOT:49 cites `event_slot_setter_replay.py`; the other two are not cited by my pages | present |
| `members/console-tunables-consumers.tsv` | 103 lines, 5 `#` comment lines + 1 header ⇒ **97** data rows; 22 with a `setting_name`, 14 with `outside_readers` | CON282:248 "(97 rows: arm ids, labels, loader key, outside readers)"; "22 keyed, 14 read" (CON282:248) | **agree** (97 / 22 / 14) |
| same file, row `01F82D20` | arm_ids `134,166,263,264,271…281,283,284,285` = 18 ids (D1, E1, H2, I14) | ARMDIV:469 "**18** — D 1 · E 1 · H 2 · I 14"; ARM-I:38 "fifteen of its twenty-two live commands" | agrees with ARMDIV / ARM-H; **disagrees with ARM-I (15)** — see C.1 |
| same file, row `01DF6E48` | outside_readers `001C5930 ; 001C5F20 ; 001C61F0 ; 001C6C00` = 4 | ARM-A:295-296 (five, incl. `001C7940`), ARM-A:301 (parser + "three siblings"), ARM-A:303 ("the five JSON readers") | **disagrees with ARM-A:296/303 (5)**; agrees with ARM-A:301 (4) |
| same file, row `02CB814C` | arm_ids `32` "Display texture density" | ARM-A:101 (id 32 target `d+0xC2C` only) | slice row does not list `02CB814C` — see G.2 |
| same file, row `02CB813C` | arm_ids `53` "Debug Cubemap" | ARM-B:81 (id 53 target `—`) | slice row leaves target blank — see G.2 |
| same file, rows `02CB80A0`–`02CB812C` | 36 rows, arm ids 63–98, 9 keyed (`80A0/A4/A8/AC`, `80D4/D8/E4`, `8104`, `8128`) | ARM-C:115-116, ARM-C:232 | **agree** |
| `members/scenewide-cbuffer-map.tsv` | 296 lines | not cited by my pages (cited by CON282:250) | not checked |
| `map-lighting-tuning-02cb7fd0-accesses.tsv` | 59 lines | not cited by my pages | not checked |
| CMDNAMES table (not a .tsv, generated) | 282 action rows + id 294 | arm address for all 282 ids vs the nine slice tables (scripted join) | **0 arm-address disagreements; 56 ids on `001D4BFA` in both**; field column disagrees only for id 28 (`02CB8130`, CMDNAMES:111) — see C.2 |

## 1. Interface

The system's interface as the 00 pages state it, per page group: **entry points** (functions with their callers),
**inputs and outputs** (data read and written, with record layouts), **state** (globals and objects, with
lifetime), **order** (what runs when, and what triggers it) and **dependencies** (other systems). Every row carries
its citation; "not stated" marks a silence.

### 1.1 Boot fixups, startup data construction and the application root

Pages: `README`, `BOOT`, `C-BOOT`, `FLOAT`, `APP`.


#### 1.1.1 Entry points

| function (address + name) | role | callers as stated | cite |
|---|---|---|---|
| `007A3770` WinMain (45 B) | calls `IsDebuggerPresent` then `007980A0` (the game's `main`, 2,153 B) | MSVC WinMain slot | BOOT:209-214 |
| `007980A0` real main | "where the boot sequence this page describes is entered"; calls platform/online init `007A0C60`, `008655E0`, `0020CD80` | `007A3770` | BOOT:211-214, 428-430 |
| `0017D000` latch writer | allocates, calls `0017D4C0` (+31), `00210EC0` (+41), `0018A840` (+59), `00189000` (+111), writes `+0x113C`=1 (+116) | PhyreEngine run loop → GameApplication startup (BOOT:262-263); thunk `0017D150` (APP:623) | FLOAT:81-90, APP:74, 629-634 |
| `0017D4C0` init burst (387 B) | stores five globals `01F7F4C0`…`E0`, ~35 init calls; calls `0022A0B0` | `0017D000` | APP:630-631, BOOT:237, C-BOOT:44 |
| `0022A0B0` boot fixer (978 B) | seeds MT, sets button masks, frame-base constant, 11 allocs / 9 registrations; calls hubs `0037DF90`, `0037E0F0` | `0017D4C0` only ("its only caller") | BOOT:30, 236-237, C-BOOT:837 |
| `0022BDF0` frame-base selector (146 B) | `ecx = (settings row 18 == 1)` → tail `001EDDC0`; `-nologo` argv scan → `00314DE0(1)` | `0022A0B0` | BOOT:110, 238; C-BOOT:201-204, 314-319 |
| `001EDDC0` frame-rate bootstrap (165 B / "~160 B") | 60 arm writes `01DFE0B4`=2, `01DFE0B8`=2.0f, `01DFE0BC`=0.5f, `01F82E38`=1, runs LUT battery `0033F020`; 30 arm does `timeGetDevCaps`/`timeBeginPeriod`; tail `0032AE70`, `003333D0`, `00337A00` | `0022BDF0` tail | BOOT:239, 497-509; C-BOOT:256-265 |
| `00379CF0` → `00863D30` RNG_MT19937_Seed | seed 5489 on first use (latch `02EB4234`), then caller's seed | boot site `0022A410` (C-BOOT:839) [BOOT:38 shows "002648.."]; `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` at `005843D3` | BOOT:41-47, 240-241; C-BOOT:63-66, 839 |
| `0036D240` allocation shim (14 B) | tail-jumps to CRT `malloc` thunk `0085E730` | `0022A0B0` ×11; `0037B3D0` | BOOT:223, 242, 576 |
| `00369D30` arena initializer (707 B) `(id, block, size, slotCount)` | registers arenas | `0022A0B0` (2-9, 0xB), `0037B3D0` (0xB), `003E9AA0` (0xC), `0025A990` (0xD), `0025AA30` (0xE) | BOOT:184-186, 243, 353 |
| `0022A4F0` button-mask applier (66 B) | rewrites `01E0C2A0`/`01E0C2A4` | tail of `DecideButton` setter `0017E6E0` | BOOT:222, 244, 548 |
| `00229F10` frame-base setter (7 B) | `mov [02064ACC], ecx; ret` | `002695A0` (area transition `002628B0`), `0026DB10` (verb `mainloopallsyncv`, handler `003464B0`) | BOOT:117, 247, 551; C-BOOT:80, 840 |
| `0022A770` field frame (2,001 B) | sole reader of `02064ACC`; waits via `0035EC80`→`0035EB70` | frame dispatcher `0022A580` (APP:709-710) | BOOT:245, 270-271, 382-387 |
| `0035EB70` tick pacer (258 B) | waits `max(n,1)` ticks | `0022A770` via thunk `0035EC80` | BOOT:246, 385-387, 560 |
| `0037DF90` (344 B) / `0037E0F0` (596 B) builder hubs | `lea rcx,[obj]; call builder` pairs, 26 / 40 into band | `0022A0B0` | FLOAT:83-86, 101-110, 157 |
| `008631D0` (15 B) header writer; `008631E0` (84 B) MPG record appender | stamp `+0/+3/+4`; append to `02EAF930` at counter `02EB37B0`, handle at `+4` | builders | FLOAT:546-559, 192-195, 645-649; C-BOOT:779-783 |
| `0020E600` / `0020E620` handle codec | `h + [01F83530]` / `p − [01F83530]` | 4,371 sites of `0020E600` | FLOAT:581-592 |
| `0022C970` VIF1 interpreter | dispatches `0x4A` MPG arm (`0022CA3D`–`0022CA60`) | not stated here | FLOAT:36, 613-618 |
| GameApplication vtable `008C5760` (31 slots) | slot 0 dtor `0017CC70`; slot 2 VBF mount `0017CEB0`; slot 4 frame tick `0017CCD0`; slot 7 input `0017CE50`; slot 8 render `0017D090`; 21/22 `0017CFD0`/`0017D170`; 23/24 `0017CDF0`/`0017CE20`; slots 3,6,9,10,15,16,25 | framework dispatch through table ("no direct E8/E9 caller") | APP:105-115, 597-614 |
| `0017D6E0` per-frame pump (404 B) | fetches/advances 13 singletons | slot 4 on all three paths | APP:225-232, 401-407, 479-497 |
| `0022A580` frame dispatcher prologue (465 B) | pause mirror, mode-change on `02064AD3`, worker queue, jump to frame bodies | not stated | APP:706-710 |
| `00229590` PauseMenu handler | sets/clears pause flag via `0017E720` | registered by `002282F0` at `0022832E` | APP:264-269, 678-689 |

#### 1.1.2 Inputs and outputs

Inputs: `GameSetting.ini` `DecideButton` (index 25, default 0 = Circle) BOOT:104; `FrameLimit` via `0017D8F0` = `mov rax,[01F82D20]; mov eax,[rax+0x48]` (settings row 18) C-BOOT:47, 202-203; argv `-nologo` C-BOOT:314-319; `../FFXII_TZA.vbf` + `../../..` APP:59-64, 359; `_time64` on load C-BOOT:64-66.

Memory budget (BOOT:126-138, 345-359):

| id | base | size | alloc size / site → slot | cite |
|---|---|---|---|---|
| 2 | `0x01DC0000` | 29.75 MiB | `0x1DC0010` @`0022A1E1` → `01FD49F8`; reg `0022A2AE` | BOOT:128, 345, 356 |
| 3 | `0x00D20000` | 13.12 MiB | `0x0D20100` @`0022A1F2` → `01FD4A00`; reg `0022A2CB` | BOOT:129, 346 |
| 4 | `0x00100000` | 1.00 MiB | `0x0100010` @`0022A203` → `01FD4A08`; reg `0022A2E7` | BOOT:130, 347 |
| 5 | `0x001C0000` | 1.75 MiB | `0x01C0100` @`0022A214` → `01FD49F0`; reg `0022A304` | BOOT:131, 348 |
| 6 | `0x06C00000` | 108.00 MiB | `0x6C00400` @`0022A225` → `01FD4A10`; reg `0022A321` | BOOT:132, 349 |
| 7 | `0x03000000` | 48.00 MiB | `0x3000100` @`0022A236` → `01FD4A30`; reg `0022A33E` | BOOT:133, 345 |
| 8 | `0x02000000` | 32.00 MiB | `0x2000100` @`0022A247` → `01FD4A38`; reg `0022A35B` | BOOT:134, 346 |
| 9 | `0x01200000` | 18.00 MiB | `0x1200010` @`0022A258` → `01FD4A40`; reg `0022A377` | BOOT:135, 347 |
| 11 | `0x00400000` | 4.00 MiB | `0x0400100` @`0022A269` → `01FD4A18`; reg `0022A394` | BOOT:136, 348 |
| — | unregistered | 0.5 MiB | `0x0080000` @`0022A27A` → `01FD4A20` (write-only) | BOOT:161-166, 349 |
| — | unregistered | 1 MiB | `0x0100000` @`0022A28B` → `01FD4A90` @`0022A2A3` (see C.1) | BOOT:165, 350 |

Tail = handle-slot count, 16-byte handle records; header + two page bitmaps + slots×16 table at block start (BOOT:150-153, 303-306). No allocation return is tested (C-BOOT:226-241). Runtime bases, not image addresses (BOOT:140-144).

Frame-base / time-base cells (C-BOOT:256-275; BOOT:251-257):

| cell | off / on (30 / 60) | readers | cite |
|---|---|---|---|
| `01DFE0B4` dword | `1` / `2` | 120 functions, 211 sites, 21 `div` | C-BOOT:273 |
| `01DFE0B8` f32 | `1.0f` / `2.0f` | 37 / 45 | C-BOOT:274 |
| `01DFE0BC` f32 | `1.0f` / `0.5f` | 93 / 182 | C-BOOT:275 |
| `01F82E38` mode flag | not stated / `1` | 13 functions | C-BOOT:263, 283 |
| `02064ACC` | `2 / [01DFE0B4]` | one reader `0022AE8F` | BOOT:254, 383-387 |

Predicates: `001EDDA0`, `001EDEC0`, `001EDE80` (sum `d[02064AD8]+d[02064AA8]`), `001EDE70` (flag verbatim); suppressor `01DFE0C0` ships 1, sole writer `001EDEF0`, via `00184960` (callers `0022A0B0`, `0022B7E0`, `00250540`, `002507C0`) C-BOOT:286-310, 458-469.

Packet template header (FLOAT:184-190, 546-559):

| offset | width | meaning | cite |
|---|---|---|---|
| +0x00 | u16 | `dx` (header) / `1` (registered) | FLOAT:548, 554 |
| +0x03 | u8 | kind `0x10` (plain) / `0x30` (registered) | FLOAT:549, 553 |
| +0x04 | u32 | 0, or 32-bit handle of own `02EAF930` entry | FLOAT:550, 559, 579-580 |
| +0x08 | u32 | `0x03000000` or `0x0300001E` | FLOAT:186 |
| +0x0C | u32 | `0x02000000` or `0x020001F1` | FLOAT:187 |
| +0x18 | u32 | `0x01000404` | FLOAT:188 |
| +0x1C | u32 | `0x6CNN0000` | FLOAT:189 |
| registry entry (16 B @ `02EAF930`+16n) | u32 + u64 | `r8d \| 0x4A000000`, program pointer; 1,000 records, no bound check | FLOAT:555-558, 269-270 |

Objects: `02ADEF40`–`02AED330` in .data zero-fill tail (FLOAT:116-121); per-object sizes FLOAT:519-537, 622-628 and `members/builder-store-extents.tsv`.

GameApplication object, `0x1140` B (APP:124-125, 144):

| offset | width | meaning | cite |
|---|---|---|---|
| +0x00 | ptr | vtable `008C5760` (base `01CB2508` during destroy) | APP:134-136 |
| +0x08 | — | `PBase` subobject (mdisp 8) | APP:177-178 |
| +0x48 | f64 | frame delta | APP:222 |
| +0xD24 / +0xD28 | — | window size, 1280×720 from ctor `00792459` | APP:63, 280-281 |
| +0xDF8 | ptr | backend | APP:282 |
| +0x10D4 | — | console block dword (scale) | APP:262 |
| +0x1130, +0x1138 | — | touched by slot 2 (meaning not stated) | APP:63 |
| +0x113C | u8 | one-way startup latch (1 W @`0017D074`, 3 R) | APP:73-80 |
| +0x113D | u8 | slot-4 run-once guard | APP:91-96 |

Pump singletons (APP:483-497): 13 rows `global / Ensure / update / size` (e.g. `01F81260` SaveloadManager `0xA78`; `01F7F598` renderer `0xDD8` pumped three times; `01F82CE0` ScreenImage `0x38` with fade fields `+0x00,+0x04,+0x0C,+0x10,+0x14,+0x1C,+0x20` APP:512-522). `01F82C80` FrameMarkerSingleton layout APP:1377-1389. Manager-pointer block `01F7F4C0`–`01F82D00` APP:640.

Files read: `../FFXII_TZA.vbf` (APP:46, 359); `./GameData/%s/ArtData/shaders/anisolighting.dds.phyre` (APP:667); `/GameData/D3D11/ArtData/shared/idmaps.txt` (APP:2338); `./GameData/%s/ArtData/chr/%s_%s.ah` (APP:312). Files written: `/Capture 4K/capture…tga` (APP:2382).

#### 1.1.3 State

| global | size / init | writer(s) | reader(s) | lifetime | cite |
|---|---|---|---|---|---|
| `02EB4234` MT first-use latch | byte, 0 → 1 on first seed | `00863D30` | `00863D30` | process | BOOT:44-45, 256 |
| MT state object `01CCFAC8` | 624 dwords, index `0x270` | `00866D60` | MT consumers (66) | reseeded on load from clock | BOOT:43, 77; C-BOOT:176 |
| `01E0C2A0` / `01E0C2A4` | dword `0x2000`/`0x4000`, swapped if `DecideButton`==0 | `0022A0B0` (`0022A10C`,`0022A119`), `0022A4F0` | every other of the 90 referencing sites is a `test word ptr` read (input arbiter `00253C70`, menus, widget handlers) | rewritten per Config change | BOOT:97-106, 222, 253 |
| `02064ACC` | dword; `.data` initial not stated; `2/[01DFE0B4]` | boot `0022A1A7`, `00229F10` | `0022AE8F` | recomputed every area change | BOOT:254, 288-289, 383 |
| `01DFE0B4` | ships `1`, `2` on 60 branch | `001EDDC0` only | 120 functions | set once at boot | C-BOOT:205-206, 264-268 |
| `01DFE0B8` / `01DFE0BC` | ship `1.0f`/`1.0f` | `001EDDC0` | 37 / 93 functions | boot | C-BOOT:267-275 |
| `01F82E38` | initial not stated; `1` on 60 branch | `001EDDC0` | 13 functions | boot | C-BOOT:263, 283 |
| `01DFE0C0` suppressor | ships `1` | `001EDEF0` (from `00184960`) | 3 predicates | — | C-BOOT:298-301 |
| `01F82E40` / `01F82E3C` | timer period / armed byte | `001EDDC0` 30 arm | `001EDDC0` 60 arm | — | BOOT:498-508 |
| `01FD49F0`–`01FD4A90` pool pointer slots | qword | `0022A0B0` | registrar; `0040ACF0` (1 MiB), none (0.5 MiB) | never freed (not stated) | BOOT:163-178, 257 |
| arena descriptor byte `022D8662` | — | `0036BC60` marks on uninitialised arena | — | — | BOOT:205 |
| `02ADD930`–`02ADD933` arena-11 regrowth bytes | `0037B390` sets 1/4/0, then 0/3 | `0037B390`, `0037B3D0` | `0037B3D0` | — | BOOT:575-576 |
| `0208E6B0` LCG area counter | post-increment per battle-area init | `00234315` | `00234301` | process | BOOT:82-87 |
| `02EAF930` registry / `02EB37B0` counter | 1,000 × 16 B | `008631E0` only | via handle codec | process | FLOAT:193, 265-270, 585-589 |
| packet objects `02ADEF40`–`02AED330` | zero-fill .data then immediates | 65 builders (+2 tail-jump) | VIF1 interpreter, effect builders | built once at startup | FLOAT:121, 173-176, 41-46 |
| `02064E30` emulated VU memory | 1,024 cells; `0x4000` clear by `0022CB90` | `0022CB90` | VU microprograms | — | FLOAT:35; APP:1670-1671 |
| GameApplication `+0x113C` | 0 → 1 once | `0017D000` | slots 4, 7, 8 | never cleared | APP:73-82 |
| 13 pump singletons `01F7F598`…`01F82D30` | lazy `cmp [G],0 → alloc → ctor → store` | Ensure stubs | `0017D6E0` | constructed at boot by `0017D4C0` | APP:479-481, 640, 646-648 |
| `01F810F0` pause flag | 1 byte, zeroed | `0017E720` (via `001997E0`) | getter `0017E4E0`, mirrored to `02F974A0` | — | APP:264-277, 2414 |
| `01F7F598` renderer | `0xDD8`, accessor `00189120` (117 callers) | `00189000` | 175 member bodies | — | APP:491, 1052-1057 |
| `01F82C80` FrameMarkerSingleton | `0xF778` | `001D62D0` | `001D6000` per frame | — | APP:1370-1393 |
| `02090790` handler table | 12 × `0x20` | `002486B0` | — | — | APP:2254 |

#### 1.1.4 Order

- Process: `WinMain 007A3770` → `007980A0` (BOOT:209-214) → PhyreEngine run loop → GameApplication startup (BOOT:262).
- `0017D000`: +31 `0017D4C0` → +41 `00210EC0` → +59 `0018A840` → +111 `00189000` → +116 latch (FLOAT:81-90, 305-306, 431). APP:629-634 states a different order (C.1).
- Inside `0022A0B0`: `0022BDF0` "runs first, and then" `02064ACC = 2/[01DFE0B4]` (BOOT:110-113; `0022A18B`–`0022A1A7` BOOT:369-371); 11 mallocs `0022A1E1`–`0022A28B` straight line then 9 registrations `0022A2AE`–`0022A394`, first test after at `0022A3DF` (C-BOOT:226-232); seed site `0022A410` (C-BOOT:839). Position of the hub calls, `0022CB90`, `00266D10`, `002368D0`, `0036D990` (`0022A125`, EEVU:311) not ordered on my pages (G.2).
- `0036F4D0` call order: `0036D280`, `00465F60(0x100)`, `003A1D50`, `00467BB0`, `0026E1D0`, `00382910`, `003ECF70`, `00475310`, `003ED820`, tail `00467AD0` (BOOT:572).
- EXP-001: engine "starts on the 30 fps base and switches later in startup" — PROBABLE (C-BOOT:218-224).
- Per framework frame (outside my pages, TUNES:653-656): slot 7, slot 4, viewports, slot 8, run by `0079C140` from loop `00796490`.
- Slot 4: latch gate → dt from `+0x48` → run-once `0017D650` behind `+0x113D` → `0017D6E0` on all three paths (APP:219-232). Pump order of the 13 singletons: only "`01F7F598` … once early, then twice more" and `01F82D30` "the last getter called in the tick" (APP:529-537).
- Field frame: `0022A770` → `0035EC80` → `0035EB70` waits `[02064ACC]` ticks (BOOT:270-271); while pause flag set runs only `002506D0` and the camera section (APP:272-274).
- `0022A580` prologue → dispatch on `02064AD3` into frame bodies (APP:706-710).
- Load: `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` reseeds from clock (C-BOOT:63-66).
- Area transition `002628B0` → `002695A0` → `00229F10` (C-BOOT:80).
- Config change: `0017E6E0` → `0022A4F0` (BOOT:222, 548).

#### 1.1.5 Dependencies

- 21-RNG-And-Determinism (which-roll-is-on-which-generator, rng-streams, CONTRACT-gameplay-generators) BOOT:78-88, 220.
- 24-Compiler-And-CRT-Runtime/Memory-And-Allocation (arena layout, `0036C1D0` selection) BOOT:154, 193, 223, 291.
- 19-Save-Load-Settings/Game-Settings-Config (FrameLimit, DecideButton, settings row 18) BOOT:224, 512; C-BOOT:210.
- 17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md (packet contents, interpreter) FLOAT:36, 45, 180, 243; 17-…/Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md BOOT:175; 17-…/Character-Render-Records BOOT:416; 17-…/Character-Rendering/character-render-object.md APP:86.
- 22-Middleware-PhyreEngine (Phyre application, between-two-frames) BOOT:237; APP:275, 591.
- 09-Combat-AI-And-Gambits (Z-11 time-base word) BOOT:374-376; 10-Status-Periodic-Terminal (periodic drain `[01DFE0B4]×30/3`) C-BOOT:351-353.
- 99-Unresolved-Residual text-element dispatch table (`001EDEC0` consumer) C-BOOT:311.
- 02-Resource-And-Asset-Pipeline (VBF archive; `.ta` lists) APP:559, 757.
- 15-Input binding profiles; 18-Audio boundary APP:267, 279.
- Within 00: Diagnostics-Logging (`005CDAA0`) APP:896; Developer-Tuning-Console (`+0x10D4`, render pass list) APP:112, 262; Object-Model vtable index APP:753.

### 1.2 World tick, field frame and force-fight mode

Pages: `TICK`, `C-TICK`, `FORCE`.


#### 1.2.1 Entry points

| function (address + name) | role | callers as stated | cite |
|---|---|---|---|
| `00314020` `World_UpdateSimulationTick(mode, flag)`, 845 B | the world tick: prologue, deferred request, mode-dependent slot loops, fixed tail; returns `eax = (mode == 0)` | `0022A770` (mode 2, field frame, `ecx`=0, `edx`=`edi`), `MainLoop_UpdateAndRenderFrame` `0022B8C0` (mode 3, `ecx`=1,`edx`=1), `0022BC20` (mode 5, 1,1) | TICK:48-56, TICK:157-158, TICK:362, TICK:580-583, C-TICK:49, C-TICK:105-106, C-TICK:336 |
| `00314960` (7 B) tick-in-progress getter `mov eax, [022C2548]; ret` | reentrancy deferral gate | "12 call sites in 12 bodies" (8 paired with `001EDDA0`, plus `00246753`, `003D912F`, `003D96C8`, `0052BB4A`) | C-TICK:50, C-TICK:220-231 |
| `0025BFB0` (179 B) manager request queue drain | drains mask `02099ABC` before any mode test | the tick at `00314078` | TICK:81-94, C-TICK:73-74 |
| `00234590` `BattleSystem_RunFieldFrameOrchestrator(slot)`, 752 B | 23 ordered steps, slot 0 only | the tick (`003141D4` mode 0; `00314116` mode 1, no-op) | TICK:104, TICK:114, TICK:206-235, TICK:363 |
| `0025D9E0` `ActorManager_RunFieldRuntimePass(slot)`, 1,297 B | the actor drive loop | the tick (`003141DB`, `0031411D`) | TICK:105, TICK:115, TICK:367, TICK:717-724 |
| `00234520(slot)`, 109 B (also "~220 B") | slot-0 post-step; one-shot `0208E6A8` | the tick (`003141E2`, `0031412B`) | TICK:106, TICK:256-260, TICK:369, TICK:1475 |
| `003DB1F0(slot)`, 132 B | per-record post-pass (`+0x63` countdown, `+0xA0` walk, `003DB6E0`) | the tick (`00314211`, `00314124`) | TICK:110, TICK:116, TICK:138-142, TICK:368 |
| `002623A0(slot)`, 152 B | per-slot end of tick; publishes `02099D70`/`02099D78`; `002E5180` over records | the tick `00314254`–`00314273` | TICK:147-150, TICK:370 |
| `00233F70` `BattleUnit_UpdateLifecycleAndCombatFrame(slotField, record)`, 467 B | per-unit lifecycle callback | no direct caller; stored at record `+0x38` by `00265A20` (`00265A4F lea`, `00265AA8`); called by `0025DF00` at `0025E222` | TICK:264-274, TICK:364 |
| `00265A20` `ActorSystem_BindBattleUnitsForEligibleRecords`, 320 B ("~200 B" at TICK:1435) | binds units for records `+0x14 ≥ 0x80`, up to 32 | not stated | TICK:265-268, TICK:365 |
| `0025DF00` `WorldActor_UpdateRuntimeAndScriptExecutionState`, 1,228 B | calls the callback under four gates | per actor inside the drive loop | TICK:269-274, TICK:366, TICK:1010 |
| `0032FC30` `WorldSimulation_ProcessDeferredModeRequest`, 66 B | deferred world-mode dispatch | the tick `003140BA` (`(0, request)`) | TICK:74, TICK:418, TICK:1260-1264 |
| `003DF760` (48 B) | indexed registry-slot setter | mode 0 calls `(0, n, 0,0,0)` n=1..5 | TICK:100, TICK:901-903, TICK:1665-1669 |
| `003DAC70(00314F30)` | movement-body separation pass | the tick tail | TICK:145-147, TICK:1360-1364 |
| `002EEEB0` (18 B) | fixed tail end: `002EE430()` then `002EF050` | the tick tail | TICK:157, TICK:653-654 |
| `002E09A0` (1,002 B) | router input-mailbox drain | the tick tail `0031427D` | TICK:866-875, TICK:885 |
| `00362850` (1,036 B) | audio listener update | tick tail | TICK:154, TICK:893-897 |
| `003E7650` | presentation-parameter push over `02B59D80` | tick tail | TICK:156, TICK:897-900, TICK:438-448 |
| `00253B90` (12 B) | force-fight predicate `flag == 0` | 7 direct sites + 8 via thunk `0030C0D0` = 15 (incl. orchestrator step 5) | FORCE:60, FORCE:106-107, FORCE:233-241, TICK:217 |
| `00253BA0` (27 B) | effective reader `enable ? flag : 0` | `00276650`, `00276D30` (UI) | FORCE:144, FORCE:255-266, FORCE:390-397 |
| `00254EA0` (54 B) | setter with `003BA2E0` veto | only `003444D0` (`setforcefightmode`, id `0x0334`) | FORCE:71-83 |
| `00252C80` (134 B) | second writer (R2 toggle apply) | not stated on FORCE (R2 page) | FORCE:148, FORCE:177-180 |
| `003BA2E0` (27 B) | feature enable: `02B4053C && 02B4053D` | `00252C80`, `00253BA0`, `00254EA0` | FORCE:96-99, FORCE:403-409 |
| `003444D0` (23 B) | `setforcefightmode` handler, 1 pop | script VM dispatch | FORCE:81-87 |

#### 1.2.2 Inputs and outputs — record layouts

**Actor-manager slot record** (`02098E10`, stride `0x288`, 5 slots):

| offset | width | meaning | cite |
|---|---|---|---|
| `+0x10` | byte | bit 0 live; bit 7 (held / start-up unsettled; `00267330` returns bit 7 when bit 0 set, else 1) | TICK:138, TICK:191, TICK:425, TICK:1683-1685 |
| `+0x11` | byte | bit 0, bits 2/3 gates; bit 3 in request rules | TICK:720-721, TICK:955 |
| `+0x12` | byte | pending-wake list nonempty | TICK:721-722 |
| `+0x13` | byte | set → request-eligible | TICK:955 |
| `+0x17` | byte | bits 4/7 suspend/active; bits 0–1 required set by `00265680` | TICK:722-723, TICK:931 |
| `+0x20` | dword | count read by `00263C30` | TICK:1586 |
| `+0x28` | qword | passed as `rcx` to the unit callback | TICK:272, TICK:425 |
| `+0x48` | qword | returned by `00264610` | TICK:1122 |
| `+0x108` | qword | unload hook, null on every shipped path | TICK:956, C-TICK:217-218 |
| `+0x1D0`/`+0x1D8` | word arrays | `00263C50` / `00263B50` | TICK:1120-1121 |
| `+0x1D6`, `+0x1DE` | | record range `[+0x1DE, +0x1DE + +0x1D6)` for `002E5180` | TICK:150 |
| `+0x200` | byte | `& 2` body iterates `020AA1F0`-side table | TICK:723-724 |
| `+0x201` | byte | sub-step opt-in bitmask (bit per skip request) | TICK:123-126, TICK:177, TICK:565 |

**Actor storage record** (per-record post-pass): `+0x63` two-pass countdown; `+0x89` count of `0x14`-byte entries at `[+0xA0]`, entry `+0x11` state 1→2 (TICK:138-142, TICK:910-918).

**Unit callback gates on the record**: `+0x09` bit 5 clear, `+0x14` bit 4 set, `+0x18 == 0`, `+0x13` bit 1 / `+0x09` bit 6 clear; sets `+0x0D` bit 6; callback at `+0x38` (TICK:271-274).

**Battle unit flags (first qword)**: bit 1 no-op/torn down, bit 3 required, bit 4 simulated, bit 16 must be clear, bit 24 reaction pending (excluded from reset loop), bit 33 teardown on idle path (TICK:572-575, TICK:935-951). Unit `+0x698` stats record, `+0x714` id, `+0x6B4`, `+0xE68`, `+0x80` (TICK:218, TICK:287, TICK:296-297).

**Skip-request entry** `022CB730 + (manager × 8 + k) × 16`: `b_00` bit in `+0x201`, `b_01` row in pending/active arrays `022CB9C0`/`022CB9D8`, `b_02` state, `dw_08` begun, `dw_0C` armed (TICK:187-190). (Contradicted at TICK:1328-1331, TICK:2171, TICK:2606 — see C.1.)

**Router mailbox**: eight `0x68`-stride records at `0215F200` (state word `+8`; 6 → `002A28B0`, 7 empty; `+0x38`/`+0x3E` bit 7); cells `0215F1A0` pending, `0215F1A4`/`0215F1A8` posted args; exempt ids `0xE9000` = 12,15,17,18,19 (TICK:679, TICK:866-891).

**`02EBEC00` pool record** (24 B, 36 slots): `+0x00` u32 key (0 = free), `+0x08` pointer to class-chained registry object, `+0x13` flag byte (TICK:813-835).

**`003DF760` tables**: entry `n` of four eight-entry tables `02B59C40[n]`, `02B59C80[n]` (ptr), `02B59CC0[n]`, `02B59CE0[n]` (dword) (TICK:901-903) — contradicted by TICK:1666-1668.

**Battle-state word `02089340`** bit table (TICK:328-349); area init writes `(w & 0xFFFFC01E) | 0x10` (TICK:324-326).

**UI-request flag word `022C83E8`**: bit 0 ← `0x18`, bit 1 ← `0x0B`, bit 4 ← `0x17`; bit 8 set on game-over route (TICK:237-239, TICK:431, TICK:845).

**Force-fight**: `01E0C2B8` dword flag (FORCE:58); enable bytes `02B4053C`/`02B4053D` (FORCE:98); availability rule reason `0x24` on `raw[5]==0 && ((raw[0x64]|raw[0x3C]) & 0x08000020)==0 && force_off && actionId ∉ {0x113,0x95}` (FORCE:128-131). Exempt ids = Dismiss, Dismount (FORCE:182).

Files read/written: none stated (not stated). Script corpus census only (FORCE:170).

#### 1.2.3 State

| global | size / init | writer(s) | reader(s) | lifetime | cite |
|---|---|---|---|---|---|
| `022C2548` tick in progress | u32; image initial value not stated | `00314047` (=1), `0031435D` (=0) | only `00314960` | 0→1→0 within each tick call | C-TICK:56, C-TICK:79-85, C-TICK:137-139, TICK:426 |
| `01EED060` deferred request (latch) | i32, image `0xFFFFFFFF` | `00314410` (stores arg when negative, raises request 4); tick clears to -1 (`0031407D`–`00314092`) | tick | one-shot | C-TICK:57-58, C-TICK:90-91, TICK:72, TICK:1141 |
| `01EED064` deferred mode request | i32, image `0xFFFFFFFF`; 16 accesses, 4 writers 12 readers | tick clear `003140BF`, two `WorldTransition_*` stagers, the reset | tick → `0032FC30(0, req)` | consumed once per tick | C-TICK:87-92, TICK:72-75 |
| `02098E10` slot array | 5 × `0x288`; zero-initialised `.data` | `0026C8C0` bind (zero), `0026A5B0` (`+0x201` bits) etc. | many | static | TICK:63-67, TICK:956, C-TICK:60, C-TICK:218 |
| `02099ABC` manager request mask | bits 0–4 | drain (clears), `00266D10` (stores 0 at `0026713B`), producer `0026A5F0` | `0025BFB0` | per tick drain | TICK:83-90, TICK:955 |
| `0209A1F0`–`0209A20F` party roster pointers | four ptrs | zeroed by drain when bit 0 set | not stated | | TICK:85-86 |
| `0209A2B0`–`0209A2C4` five-field block | | reset every tick by `0025D650` | group-completion lock writes `0209A2C4[2]` | per tick | TICK:77-79, TICK:433 |
| `022C252C`, `022C2530` tick counters | dword | `++` at `00314231`/`0031423E`; reset by `00314010`/`00314000` | not stated | callers of resetters not stated | TICK:144-145, TICK:427 |
| `022C2544` float | | `00314940` copies `01CEBBA8` (1.0f) | time-scale block | not stated | TICK:155, TICK:428, TICK:1142 |
| `02089340` battle-state word | bits per §2.5; init mask `(w & 0xFFFFC01E) | 0x10` at area init | many (§2.5) | many | bits 0,5–13 cleared at area init; bit 4 cleared at area unload `002341E4` | TICK:312-349, TICK:430 |
| `0208E6A8` one-shot callback / `0208E6A4` handle | qword / dword | set by `0023B020`; nulled by `00238A60` | `00234520` (calls and nulls when `(02089340 & 5)==1` and bit 1 clear) | one-shot | TICK:256-260, TICK:330, TICK:1108, TICK:432 |
| `0208D45C` raw tick counter | dword | `0032A100` when `003EBA90(0)` changed vs `022C317C` | `GameClock_GetRawTickCounter` | | TICK:214, TICK:435 |
| `022C83E8` UI-request flag word | | `0035C8A0`, `0035C8E0`, `0035C7B0(11,1)` bit 8 | `0035C700`, `0035C740` | | TICK:237-239, TICK:845, TICK:1160-1161 |
| `02099D70`, `02099D78` | pointers | `002623A0` per slot | not stated | per slot | TICK:148-149, TICK:434 |
| `022CB730` skip entries, `022CB9C0`/`022CB9D8` pending/active | 16 B entries | `00360980`, `00360710`, `00360A50` | `00267310`… | | TICK:187-199 |
| `022CB720` skip/lane mask | dword | `003601B0` (bit set), `003601C0` (bit clear) | | | TICK:786, TICK:1630-1633, TICK:1805 |
| `022C2578` candidate-cache generation | dword | `00325060` (+1 mod 8), `00325080` (=7) | | | TICK:708, TICK:1144 |
| `02AEE060` nav grid params (0x60) + `02AEE0A0` grid ptr | 0x460 cleared | built only by `002342F0`; torn down by `00392710` | | area init → area unload | TICK:706 |
| `01E0C2B8` force-fight flag | dword; initial value not stated | `00254EA0` (setter, veto), `00252C80` (second writer) — "four write sites in two functions" | `00253B90` (raw, 15 consumers), `00253BA0` (effective, 2 UI) | global, not per-unit | FORCE:58, FORCE:68, FORCE:143-149, FORCE:160, FORCE:263-266 |
| `02B4053C` event veto enable | byte; boot 1 | `003BA300(cl)`: `00266D10` boot =1, `002628B0` every area unload =1, verb `debug_setfightstatusbyevent` (0x206B) | `003BA2E0` | never cleared in shipped game | FORCE:170 |
| `02B4053D` companion | byte; boot 1 | `003BA310(cl)` once at boot | `003BA2E0` | never cleared | FORCE:170 |

#### 1.2.4 Order

- Frame dispatcher `0022A580` dispatches on `02064AD3`; modes 2/3/5 call the tick (TICK:580-583). Field frame (mode 2) calls only when `!001800E0() && (!001800C0() || !001EC560())` (TICK:58-59; C-TICK:211-212 `!A && (!B || !C)`).
- Tick order: `[022C2548]=1` → `003EB9A0`, `003DAA20`, `003DA2F0(1.0f)`, `003DD210(1.0f)`, `0025BFB0` → `01EED060` clear → `01EED064` consume (markers + `0032FC30`) → `003DAA40`, `0046AFA0`, mode-0-only `00358C60`; `00268650`, `0025D650`, `00255810`, `0037D890`, `0025D640` → slot loops → tail (TICK:69-79, C-TICK:137-138).
- Mode 0: `003DF760(0,n,…)` n=1..5; for step 0..15 { for slot 0..4 [gate step≠0 by `+0x201`]: orchestrator, drive pass, `00234520`; if step 0: `002E0D90`, `00268D00`; for slot 0..4 [gate]: `003DB1F0` }. Mode 1: slots 3..4 once: orchestrator (no-op), drive pass, `003DB1F0`, `00234520` (no-op); then `002E0D90`. Other: none (TICK:98-121; C-TICK:99-104).
- Tail: counters ++, `003DAC70(00314F30)`, `002623A0(slot)` for ticked slots, then `00358EE0(mode)`, `002E09A0`, `00359800`, `003DE640`, `002E0940`, `0037C1A0`, `003E7EC0`, `00228480`→`0036FD90(0)`, `002F1770(mode, edx)`, `002EF910`, `0036E1E0`, `003DEB30`, `003DF670`, `003606E0`, `00362850`, `00362DA0`→time-scale block, `003E7650`, `0025D950`, `00263660`, `002EEEB0`; `022C2548=0`; return (TICK:144-158, TICK:598-599).
- Orchestrator 23 steps (TICK:211-235); then per unit inside drive pass: lifecycle frame (TICK:276).
- Step 6 reset loop runs every second field frame under steady predicate (TICK:218, TICK:569-570).
- Force fight: set by script verb at script time; consumers read whenever they run (FORCE:78-83, FORCE:106-117). Enable bytes set at boot (`00266D10`) and area unload (FORCE:170).

#### 1.2.5 Dependencies

- 22-Middleware-PhyreEngine frame dispatcher (TICK:49, TICK:986-987).
- 04-Actor-Entity field runtime pass, actor-manager record map, actor storage record map, battle-unit field map (TICK:65, TICK:270, TICK:911, TICK:931, TICK:936).
- 99-Unresolved-Residual cutscene slots (`+0x201` writers) (TICK:64, TICK:929, TICK:998-999).
- 06-Movement-And-Navigation movement body pool (TICK:75, TICK:147, TICK:343); FORCE locomotion divisor (FORCE:113, FORCE:220).
- 05-Spawn-Encounter-Lifecycle (group completion, retirement) (TICK:82, TICK:229, TICK:990-993).
- 15-Input capability policy (TICK:216, TICK:847; FORCE:112, FORCE:218), R2 toggle (FORCE:46, FORCE:174).
- 11-Party (TICK:220); 16-UI request router (TICK:243, TICK:874); 17-Presentation (screen fade TICK:784, rig TICK:448, render records TICK:899); 18-Audio voice packs (TICK:795); 02-Resource request queue (TICK:798), battle text banks (FORCE:182); 01-Script-VM verb table/binding/dispatch (TICK:336, TICK:917, FORCE:221); 10-Status statuses / periodic tick (TICK:854, TICK:996); 03-World-Area-Field bit 15 (TICK:854); 07-Combat-Action availability (FORCE:219).
- Inside 00: Battle-Runtime-Mode (TICK:374, TICK:994; FORCE:222), System-Stop-Registry (TICK:982; C-TICK:131), Per-Frame-Update-Gate (TICK:984; C-TICK:130), Application-Root (TICK:924; C-TICK:203), Shared-Transform-Workbench (TICK:1041).
- C-TICK layer crossings: ActorEntity, MovementAndNavigation, Party, WorldAreaField, Audio, InputGameplay, CombatAction, Presentation (C-TICK:251-273).

### 1.3 Per-frame update gate and system stop registry

Pages: `GATE`, `C-GATE`, `STOP`, `C-STOP`.


#### 1.3.1 Entry points

| function | role | callers as stated | cite |
|---|---|---|---|
| `0028E290` (745 B) FramePump / "the fan-out" | reads `01E0C464` 16 times and calls 16 gated groups | "reached from `002507C0`, itself from `0022A770` and `0022B7E0`" (C-GATE:42); "the sole pump caller `002508AB`" (C-GATE:305); STOP calls it "the battle-HUD draw `0028E290` (named scope `display UI : battle`, `002508A4`)" (STOP:299) | C-GATE:41-43, GATE:47-56 |
| `002507C0` | pump parent; also calls `001EDE80` at `00250896` to gate `003BBA60` | `0022A770`, `0022B7E0` | C-GATE:305-306, C-GATE:1702 |
| group handlers (16) | see I.4 order table | `0028E290` | C-GATE:118-135 |
| `00289970` (35 B) | group 0x0001: "runs `0028A550`, then `0028A350`, then tail-calls `0028A620`, all on the same object" | gate, `add rcx, 0x5380` at `0028E2AB` | C-GATE:1804, GATE:565 |
| `001EDE80` (61 B) | group 0x0002 A predicate | gate; also `003E00C0`, `00477480` directly (C-GATE:50), `0025DF00` (C-GATE:378-379) | GATE:254, GATE:521-523 |
| `003F8B40` (162 B) | group 0x0002 A: callback-node list walker on `singleton+0x80` | gate `0028E2C5`–`0028E2D4` | GATE:524-531, C-GATE:1734 |
| `00291B90` (208 B), `003F6100`, `003F24D0` (167 B), `003F24A0` | group 0x0002 B, "gated *additionally* by `dil&1`" | gate | C-GATE:299-301, C-GATE:1356, 1726, 1821-1822 |
| `002917E0` (930 B) | group 0x0004: target-line builder | gate | GATE:225, C-GATE:1582 |
| `0028C4C0` (42 B) → `0028BB50` (2,387 B) | target-line list walk → per-node angular update | gate; `0028BB50` has "One caller" | GATE:140-158 |
| `0028C4B0` (5 B) → `0028D1C0` (154 B) | `jmp` thunk → reaper / "null-gated per-frame body" | gate | GATE:424-428, GATE:225 |
| `003F6BB0` (1,051 B) + `003F7050` (154 B) | group 0x0008 | gate | GATE:91, 254; C-GATE:1754 |
| `003F9F40` (536 B) | group 0x0020 widget spawner on `_57E0` | gate | GATE:254, 451 |
| `003F80D0` (14 B) | group 0x0040 on `_A0D0` | gate | GATE:254, C-GATE:1823 |
| `00296860` (223 B) | group 0x0080 level-up blink spawner on `_7FB0` | gate | GATE:254, 454 |
| `003F8EC0` (284 B) | group 0x0100 on `_00A0` | gate; also `0028FAF0` (C-GATE:386) | GATE:254, 450 |
| `003F31B0` (164 B) | group 0x0200 list reaper | gate | GATE:254, C-GATE:1730 |
| `003FA790` (143 B) | group 0x0400 on `_57E0` list `+0x2490` | gate | GATE:254, C-GATE:454 |
| `0028C870` (197 B) | group 0x0800, tail-`jmp`, on `_7EA0` | gate `0028E56A` | GATE:98, 113-115 |
| `00273900` → `0030C300` | group 0x1000 ("group 7") Libra / incapacitation scan | gate | GATE:254, 535-548 |
| `00290CF0` (243 B) | group 0x2000 constructor of the `0x61F0` battle menu | gate | GATE:254, C-GATE:572-573 |
| `00290EB0` (319 B) | group 0x4000 spawner for `+0x10F90` request | gate | GATE:254, C-GATE:1344 |
| `002C6180` (295 B) | group 0x8000 | gate | GATE:254, C-GATE:1352 |
| `00291750` | singleton constructor (memset 0x10FD0) | not stated | C-GATE:1075-1089 |
| `0028F8B0` region: `0028F8CA`/`0028F8CF` | singleton allocation `0x10FD0` via `00271420`, publish at `0028F8D4` | not stated | C-GATE:699-701 |
| `00226280` (952 B) | stop **apply** | "Most wrappers tail-jump to it" (STOP:78); "exactly 25 call/jmp edges, all synchronous wrappers — **no frame poll exists**" (C-STOP:232-233); `00313DB0`, `0026A1D0`, `00266D10`, `00263660`, `0026C3E0` (C-STOP:326-346) | STOP:170-187, C-STOP:51 |
| `00226BE0` (1,936 B) | stop **start** `(id, actorHandle, flag, …, count, handles)` | 13 wrappers `00227370`–`00227640` + 9 direct callers in `00266D10` (×2), `00263480`, `0026A1D0`, `00263230`, `0026B980`, `00313DB0`, `002678C0`, `00254740` | STOP:52, STOP:262, STOP:358-360 |
| `00225CD0` `(id, fade)` | stop **cancel** | wrappers `002260A0…`; `00252D90`, `002544C0` (UI close), `00263050`, etc. | STOP:80-84, STOP:237-261 |
| `00225EB0` | area-unload cancel variant | "one caller, `002628B0`" | STOP:84, C-STOP:211-214 |
| `00227680` | per-id record builder, 28-case switch at `00227744` | `00226BE0` | STOP:56, C-STOP:54 |
| `00226640` | per-actor pass `(allExempt, fadeLength, 0)` | apply | STOP:178, 189-205 |
| `002269A0` (162 B) | set-5 fold + enqueue | per-actor pass | STOP:225 |
| `00226B30` | registry reset / initialiser | not stated | STOP:50, C-STOP:105-107 |
| `00226B10(id)` / `00226BC0()` / `00226BA0()` / `00226BD0(id)` | record address / any-active / combined-restricts / test-bit | `00226BC0`: "the main loop `0022A770` and `00357380`" | STOP:48-50 |
| `00226A50` (89 B) / `00226AB0` (91 B) | single-actor set-6 / set-7 fold | `0035A720`, `0035A7A0`, `0035A8D0` | STOP:207, 743-764 |

#### 1.3.2 Inputs and outputs — record layouts

**Enable word and pump argument**
| item | width | meaning | cite |
|---|---|---|---|
| `01E0C464` | `uint32` (corrected) | 15 live bits (`0x1`…`0x8000` except `0x10`); "ships `FF FF FF FF`" | C-GATE:45, GATE:231-233 |
| pump `ecx` = `word[01E0C2B0]` | word | bit 0 gates group 0x0002 B (`0028E3B7 test dil, 1`) | C-GATE:82-85, C-GATE:301 |

**Target-line node (group 0x0004)**, `0xD80` B, no vtable (GATE:225)
| offset | width | meaning | cite |
|---|---|---|---|
| +0xBB0 | sub-object | handed to `00271650` | GATE:225 |
| +0xC70..+0xCAF | 4 vectors | copied by `00202C90` | GATE:225 |
| +0xD00 | ptr | image asset `targetline_p` | GATE:225 |
| +0xD14/+0xD18 | f32 | angle | GATE:225 |
| +0xD2C | dword | actor id (compared with `+0x10F6C`) | GATE:225, 492 |
| +0xD34 | f32 | busiest field (14 sites); sibling decay block | GATE:199, 252 |
| +0xD40 | f32 | not stated beyond "f32" | GATE:192 |
| +0xD44 | ? | **timer** (GATE:225) **or radian field** (GATE:252); see C.1 | GATE:225, 252 |
| +0xD48 | dword | variant `0x6040003`/`0x6040004` | GATE:225 |
| +0xD4C | flags | bits `0x2`/`0x40` (and `0x8` cleared by `0028C4F0`) | GATE:225, C-GATE:1571 |
| +0xD50 | mode | `== 1` selects sub-block `0x4E0`, else `0x3C0` | GATE:190 |
| +0xD54 | word | state: 1 live, 5 reap (also 3, 4 per `0028C4F0`) | GATE:225, C-GATE:1569-1573 |
| +0xD68 / +0xD70 | ptr | prev / next | GATE:225 |
| +0xD78 / +0xD7C | ? | fed to `00181930` | C-GATE:1594 |

**Singleton `[0209BE80]`**: size `0x10FD0` (C-GATE:699-701). It has seven EMBED children, `_00A0` 0x52E0, `_5380` 0x460, `_57E0` 0x26C0, `_7EA0` 0x110, `_7FB0` 0xFF0, `_8FA0` **0x1110** (corrected), `_A0D0` 0x990 (C-GATE:492-502, GATE:449-457). Other regions: `+0x80` list head, `clearedBlock0080` 0x18 B (GATE:532); `+0xAA60` 196 B memset region; `+0xAB30` widget storage (0x720 widget or the 0x61F0 battle menu) (C-GATE:532-577); hole `+0xB244..+0x10CFB` (C-GATE:687); `+0x10EF0` record; `+0x10F00` target-line list head (GATE:225); `+0x10F10` node chain (TICK, outside my pages); `+0x10F20/+0x10F30/+0x10F40` pointers written by gate (C-GATE:105); mailboxes `+0x10F60..+0x10FA8` (GATE:490-499); `+0x10F68` flag word (bits 1, 3, 4, 6, 8, 10, 12, 13, 0x2000); `+0x10F78`/`+0x10F80` pointers (C-GATE:263); `+0x10FC0` → `0x8030` allocator block (C-GATE:1132-1134); header `+0x08..+0x7C` table (C-GATE:660-670).

**Stop registry**
| address / offset | width | meaning | cite |
|---|---|---|---|
| `01FD46D4` | u32 | active-request bitset, bit *n* = id *n* (0–27); "NOT read by the apply step" | STOP:42, C-STOP:65 |
| `01FD4160 + id×0x18` | 0x18 | record A; first qword = permission mask | STOP:43, C-STOP:61 |
| `01FD4400 + id×0x18` | 0x18 | record B; first qword = mask | STOP:44, C-STOP:62 |
| record +0x08 | qword | "still unobserved" (C-STOP:243-244); the tsv shows 00227680 writing it | C-STOP:243 |
| record B +0x10 | i32 | fade length; −1 = none; 0 at process start | C-STOP:63, 103-114 |
| record B +0x14 | byte | "flag byte" / "flag argument (stored at record B `+0x14`)" vs "zeroed at start/reset" (see C.1) | STOP:44, 94; C-STOP:242-243 |
| `01FD46D0` | u8 | dirty byte | STOP:45, C-STOP:66 |
| `01FD46A0`–`01FD46C8` | — | combined masks and fade; fades at `01FD46B0`/`01FD46C8` set −1 by init | STOP:46, C-STOP:113 |
| permission bit layout | — | A bit c → set 1, B bit c → set 4, A bit 8+c → set 2, B bit 8+c → set 5, A bit 16+c → set 6, B bit 16+c → set 7, set 3 = A bit 28 AND bit 8+c; "A *set* bit is an exemption" | STOP:57-60 |
| A bit 31 | — | 1 manager when set, 3 when clear | STOP:61-63, C-STOP:131-134 |
| B bit 41 | — | OR-ed on every apply; cleared on slot 13 only by `0022603A` | C-STOP:119-123, 222-229 |
| 28 records | — | full table of A+0/B+0 per id × flag | STOP:106-138 |
| per-actor live/pending | — | set1 BU `+0xF10` / `+0x54`/`+0x60`; set2 actor `+0x10C` / `+0x110`/`+0x114`; set3 ctrl `+0x170` / `+0x174`/`+0x178`; set4 `+0x164` / `+0x168`/`+0x16C`; set5 `+0x158` / `+0x15C`/`+0x160`; set6 BU `+0xF14` / `+0x4C`/`+0x58`; set7 BU `+0xF18` / `+0x50`/`+0x5C` | STOP:199-205 |
| global outputs | — | B35 → distance cull; B32,33,40-44 → `002DF370`/`002DF640` audio; A/B 25-27 → `0209215E`/`02092162`; A/B 36-37 → `002547C0`/`00254840` (0x10/0x0E) = `01E0C2B0`/`01E0C2AC`; A29 → `0035B4B0(5)`/`0035B510(0xFF)`; A39 → `002E24C0`/`002E24E0`; B/A24 → `002EA8B0`/`002EA8E0`; A30 → `0025A5D0` | STOP:180-187, STOP:299 |

#### 1.3.3 State

| item | address / size | initial value | writer(s) | reader(s) | lifetime | cite |
|---|---|---|---|---|---|---|
| enable word | `01E0C464`, 4 B | `FF FF FF FF` | none in image | `0028E290` only (16 tests) | static `.data` | GATE:231-233, 283-284; C-GATE:45 |
| pump arg word | `01E0C2B0` | not stated (C-GATE: written `0xF` at `002539E5`) | `002539E5` (C-GATE:301); `002547C0` (STOP:828); save apply `00253970` (STOP:299) | `0028E290` bit 0 | static | C-GATE:301-302, STOP:299, 828 |
| singleton | `[0209BE80]`, `0x10FD0` B | memset 0 by ctor `00291750`; `+0x10F90 = 0xFFFFFFFF`; `+0x10FC0` = new 0x8030 block | many | 136 slot loaders | allocated at `0028F8CF` "under the null guard at `0028F8C5`"; **destruction not stated** (teardown `00290990` handles only the target-line list and `+0x7EA0`, C-GATE:1526-1529) | C-GATE:699-701, 1075-1089 |
| target-line node | 0xD80 B from allocator `+0x10FC0` | zeroed by `00275550` | builder `002917E0` | `0028BB50`, `0028C4F0`, `0028D1C0` | freed by `0028FA50` → `00273B40` | GATE:225 |
| Libra bit | singleton `+0x10F68` bit 1 | 0 (ctor memset) | gate `0028E41C`–`0028E427` | `00290100` → `002BFD20` | per frame | GATE:543-548 |
| party scan array | `022C1740`, 9 entries | not stated | `0030C300` | not stated | per frame | GATE:254, 537-538 |
| registry slots | `01FD4160`..`01FD46A0` (56 records) | first qword −1, +0x14 0 (by `00226B30`), +0x10 = 0 ("past `.data`'s file-backed end (`01F7E400`)") | start/cancel/apply | apply | process | C-STOP:103-114 |
| active bitset / dirty | `01FD46D4` / `01FD46D0` | not stated (presumably zero, by the same `.bss` argument: **not stated**) | start, cancel | `00226BC0` etc.; apply reads dirty only | process | STOP:42-45 |
| live/pending stop words | per actor / BU / controller | not stated | start (pending), per-actor pass (live) | sets' consumers | actor lifetime | STOP:189-205 |

#### 1.3.4 Order

- Frame: `CoreRuntimeScheduling -> 0022A580 -> 0022A770 / 0022B7E0 -> 002507C0 -> 0028E290` (GATE:47-56). `002507C0` first calls `001EDE80` to gate `003BBA60` and then the pump (C-GATE:305-306, 1702).
- Inside the pump, test order (not bit order): `0x0001, 0x0002(A), 0x0004, 0x0008, 0x0020, 0x0002(B, +dil&1), 0x1000, 0x0040, 0x0080, 0x2000, 0x4000, 0x0100, 0x0200, 0x0400, 0x8000, 0x0800(tail jmp)` (C-GATE:118-135). Between groups the singleton is re-loaded "after almost every group" (C-GATE:104). Inner tests on `+0x10F68` bits 3 (`0028E2EE`) and 8 (`0028E4B3`) exist (C-GATE:327); **which calls they gate is not stated**.
- Stop registry: start → (wrapper usually) apply → per-actor pass → global effects; the apply "Runs only when dirty" (STOP:172). "**no frame poll exists**" (C-STOP:233), so the apply runs only synchronously from wrappers. Start-only paths leave dirty raised until the next applying wrapper (C-STOP:231-238).
- Boot: `00266D10` raises 4 and 5 and cancels 5, 4, 7 (STOP:245). Input words are set to `0x3FF` at boot by `0024C970` (STOP:299).

#### 1.3.5 Dependencies

- Battle-Frame / world tick (00): frame modes and the field hold ids 4/5/7 (STOP:339-340, GATE:41-42).
- 19-Save-Load-Settings: the `FrameLimit` time base `01DFE0B8` (GATE:180, 274), outside 00, not audited. Inside 00 this is confirmed by C-BOOT:268, 274 and BOOT:503-505.
- 10-Status-Periodic-Terminal: status bit 30 = Libra (GATE:541-542), outside 00.
- 02-Resource: the `targetline_p` image-name block (GATE:225), outside 00.
- 16-UI: request router (STOP:271, 343); widget constructor `0x61F0` (STOP:309), outside 00.
- 17-Presentation-Rendering: fade channels / bone trails / add-motion (STOP:203, 294, 457, 561-565), outside 00.
- 04-Actor-Entity: kind byte, contexts, battle-unit map (STOP:99, 286, 345-346), outside 00.
- 15-Input: capability policy (STOP:347-348), outside 00.
- 11-Party: focus contract (C-STOP:149, 303), outside 00.
- 22-Middleware: frame modes 5/6 (STOP:271), outside 00.
- Combat/Party/Actor helpers: `00320AB0`, `00377C20`, `003588B0`, `PartyRoster_GetActorBySlot` `00263750`, `PartyFocus_GetCurrentPackedActorHandle` `003590D0` (GATE:409-415; C-STOP:336).

### 1.4 Battle runtime mode ladder, diagnostics log, duplicated names, all-ones convention

Pages: `MODE`, `C-MODE`, `LOG`, `DUP`, `ONES`.


#### 1.4.1 Entry points

| function (address + name) | role | callers as stated | cite |
|---|---|---|---|
| `0030D9A0` `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` | the ladder: returns 0..5 from `+0x5B04` bits 3,2, field bit 15, bits 1,0; 105 B; no args; no null check | C-MODE:112-115 lists `0023B040`, `00253C70`, `0023A570`, `003266C0`, `00235EA0`, `00320230`, `0035BC50`, `00313DB0` (inline), "and the two mode getters"; MODE:207 also `00309AE0`, `00311F70`; C-MODE:644 `003135C0`; MODE:429 `00309A90`; C-MODE:444 "**20 call sites, all in the `0x2FF…0x326` battle cluster**" (see C.1) | MODE:58-74, C-MODE:53-56, C-MODE:228-237, C-MODE:318-325 |
| `00377C20` `FieldData_GetActiveFieldRecordBit15` (thunk `00313F60`, TICK:405, HUBS:484) | mode-3 predicate: table `*(02ADD100)`, count `+4`, 3-byte rows from `+8`, bit 15 of the LE u16; null/out-of-range → `0xFFF >> 15` = 0 | the ladder; items `00309FB0`/`0030FD10`, economy `00312280`, `00313A00`, `AiOrder_EvaluateAndResolveActionTarget` | C-MODE:117-119, C-MODE:239-259, C-MODE:126-128, C-MODE:606 |
| `003148F0` `WorldTransition_GetActiveOrPendingFieldId` | the active field index for `00377C20`; negative clamped to 0 | `00377C20`, `00233780`, `003160C0` | C-MODE:117, C-MODE:334-337, C-MODE:125-129 |
| `00303EC0` (= `getchocobomode`) | `return ladder() == 2` | 6 direct (`0023B040`, `00253C70`, `0023A570`, `00235EA0`, `00320230`, `0035BC50`) + 15 via thunk `0037C860` = 21 | MODE:194-203, MODE:301-304, MODE:633 |
| `003135C0` (= `getsummonmode`) | `ladder() == 1`; 24 B, 7 callers | thunk `0037C8F0`; `00338490` | C-MODE:644-647, MODE:297, MODE:207 |
| `003072C0` / `00307280` (`geteventpartymode` / `geteventparty2mode`) | `ladder() == 4` / `ladder() == 5` | script verbs `0x0510` / `0x0515` (handlers `00355FE0` / `00356370`) | C-MODE:59, MODE:139-142, MODE:531-533 |
| `003135E0` / `00313550` | bit 0 getter / setter (summon); setter tails `0035C620` on change | setter: `00328BD0`, `0034E1F0`, `0034FE80`, `0050FFB0` (MODE:1240); verbs `summonread` `0203` / `summontopartyread` `0207` / `btlAtelSetSummonMode` `3044` | MODE:110, MODE:294-297, MODE:1238-1245, C-MODE:174-177 |
| `00303EE0` / `00303D90` | bit 1 getter / setter (chocobo), setter side effects | verbs `ridechocobo` `037E` (thunk `0037CFF0`), `getoffchocobo` `037F` (thunk `0037CFC0`), `setchocobomode` `03EC` (thunk `0037D100`) | MODE:111, MODE:237-260, MODE:298-301, C-MODE:155-172 |
| `003072E0` / `00307240` | bit 2 getter / setter (event party) | script VM: thunks `0037C8B0` ← `00356DF0`; `0037D120` ← `00351B40` | MODE:112, MODE:121-124 |
| `003072A0` / `00307200` | bit 3 getter / setter (event party 2) | thunks `0037C890` ← `003573A0`; `0037D110` ← `00351E50` | MODE:113, MODE:121-124 |
| `0030DA10` | reset: zeroes `+0x5B04` and `+0x5B08` | "for `BattleSystem_ResetRuntimeState`" | MODE:282-283, MODE:583-584, C-MODE:60 |
| `0030D8B0(commit)` + table `01EECFC0` | mode-transition dispatcher; compares ladder with `+0x5B08`, indexes 32-byte rows; writes `+0x5B08` when `commit ≠ 0` | `00233AA0` (field runtime pass, when all four roster members idle), `00233CF0`; C-MODE:406-407 task `0037C730` → `00233AA0` → `0030D8B0(1)` | MODE:345-377 |
| handlers `00313600`/`00313730`/`00313650` (summon), `00304180`/`00304060`/`00304400`/`00304140` (chocobo), `0016D6A0` (empty stub) | enter/leave/same-mode arms of `01EECFC0` | only `0030D8B0`'s two `call [rbx + rdx*8]` sites `0030D920`, `0030D952` | MODE:350-373 |
| `00303F00` | chocobo turbo (`btlAtelSetChocoboTurboMode` `302F`, handler `0050F8A0`) | `0050F8A0` | MODE:302, MODE:316-320 |
| `00304440` | ride's per-frame timer handler | not stated | MODE:315, MODE:448 |
| `00304680` | ride's end / dismount path | `00304140` | MODE:111, MODE:322-327 |
| `002EF3C0` / `002EF410` | `SaveTransitionMetadata_CaptureToRecord` / `…RestoreFromRecord` | restore called by `00584210` (MODE:962) | MODE:269-285, MODE:964-984, C-MODE:79-86 |
| `00584210` `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` | clears bit 0 on load | not stated | MODE:586-587 |
| `005843E0` `WorldTransitionSnapshot_RestorePersistencePairFor…` | clears bit 1 (`0058446A`) | not stated | MODE:588-589 |
| `00306BD0` `BattleAction_InitializeGlobalSpecialSequenceMode`, `00306B10`, `00306760` `BattleAction_UpdateSpecialPresentationSequence`, `003065D0`, `0030CE10` `BattleAction_TryEnterGlobalSpecialSequence` | the `022C2160` special-sequence machine (states 0–7, kinds 1–7) | `003065D0` "on the field frame's step 11" | MODE:379-425 |
| `0035BC50` | battle-menu selection-state builder (four gates, four `0xC0`-stride slots) | direct caller of `00303EC0`; `0035D980` (`0035BC50(0)`) | MODE:671-790, MODE:1381 |
| `00313DB0` | target-selection cursor; drains 64-entry ring; tail `jmp 0x313a00` | not stated | MODE:792-872 |
| `00253C70` `InputGameplay_ArbitrateDigitalInputAndModalState` | Input consumer; 22-member exclusive subtree | not stated | MODE:880-929 |
| `00309A90` | distance threshold: 24.0 under force-fight; 3.8 in mode 1; 2.2 otherwise | "four call sites" (AI order precondition, locomotion order-goal decoder, one body twice) | MODE:427-433 |
| `005CDAA0` (the formatted log call) | `(channel, fmt, ...)`: 16 KB stack buffer, `__stdio_common_vsnprintf_s`, lazy sink, vtable slot 1 | 136 non-EH caller functions, 245 sites | LOG:53-56, LOG:249-276, LOG:363-374 |
| `0019C5D0` | `vsnprintf` wrapper, clamps negative to `-1` | 120 non-EH callers | LOG:96-108 |
| `0016D670` `__local_stdio_printf_options` | returns `&02EBA3D0` | 23 call sites; writer `00809C50` | LOG:61-87 |
| `005CDA30` / `005CD9C0` | magic-static accessors (sink object `02CB6140` / sink pointer `02CB6150`) | `005CDAA0` cold path | LOG:172, LOG:201, LOG:285-287, LOG:323-328 |
| `005CDB90` | sink slot 1: `DebugBreak()` on channel 4 when a debugger is present | via `[02CB6150]` vtable | LOG:201, LOG:371-372 |
| `00379CF0` → `00863D30` `RNG_MT19937_Seed` | thunk / body example | callers reference the thunk | DUP:41-45, DUP:208 |
| `00379F20` → `0035B450` → `0035B650` | default-argument forwarder chain (`mov dl, 2`) | not stated | DUP:87-90, DUP:322-333 |
| `0016D6A0` | 3-byte `ret`; `_guard_check_icall` and array-delete helper folded | CFG slot `008C31C0`, forwarder `0017E7D0`; 1,149 deleting destructors | DUP:229-251 |
| `00512CD0` `RelationLook_RemovePooledRelationRecord` (+ `00512C80`, `00512D80`, `00512EF0`, `00512F30`) | pool unlink over 32 × 16-byte records at `02CA81F0` | `00512D80`, `00512F30` | ONES:41-51, ONES:299-302, ONES:397 |

#### 1.4.2 Inputs and outputs — record layouts

**Runtime state block `*(02EBF190)`** (MODE:458-476, C-MODE:67-77)

| offset | width | meaning | cite |
|---|---|---|---|
| `+0x5AD0` | (u16 per outside page) | bit 1 = summon sequence active (`00313600` sets, `00313730` clears) | MODE:352, MODE:364-365 |
| `+0x5AD4` | 1 | the Esper's party-table row; reset value `0x1B` (Belias) | MODE:296, MODE:336, MODE:341-342 |
| `+0x5AD5` | 1 | the caster's type byte / summoner | MODE:331, MODE:335 |
| `+0x5AD8` / `+0x5ADC` | (f32 implied) | summon timers, set from party row `+0x32` (250) | MODE:336-338 |
| `+0x5AD0..+0x5AEF` | 32 | persisted across transitions | MODE:280, MODE:463 |
| `+0x5AE0` | u32 (MODE) / 8 (C-MODE) | chocobo flags: bit 0 timers armed, bit 1 turbo on, bits 2-3 turbo charges (3 per ride) — see C.1 | MODE:464, MODE:317-319, C-MODE:74 |
| `+0x5AE4` | f32 | ride time, `0x43340000` = 180.0 on mount, channel 1 | MODE:315, MODE:465 |
| `+0x5AE8` | f32 | turbo time, 10.0 per charge, channel 2 | MODE:316, MODE:466 |
| `+0x5AEC` | u32 | last turbo argument; zeroed on dismount | MODE:320, MODE:467 |
| `+0x5B04` | u32 | mode flags; bits 0..3 consulted (only `cl` is tested) | MODE:468, C-MODE:72, C-MODE:318-322 |
| `+0x5B08` | u32 | previous mode (dispatcher) | MODE:469, C-MODE:73 |
| `+0x5A48` | 9 selectors | nine-entry selector; `+0x5AA4` leader | MODE:328, MODE:537 |
| `+0x5A5A`/`+0x5A6C`/`+0x5A7E`/`+0x5A90` | nine u16 each | mapping-class tables 1–4 (corrected 2026-09-14) — see C.1 | C-MODE:149, C-MODE:388 |

**Transition record** (written by `002EF3C0`, read by `002EF410`) — MODE:271-278 and C-MODE:80-85 (corrected 2026-09-26):

| rec offset | width | source | cite |
|---|---|---|---|
| `+0x04` | dword | `DAT_021B28E4` | MODE:272 |
| `+0x08` | qword | `state+0x5AE0` | MODE:273, C-MODE:81 |
| `+0x10` | qword | `state+0x5AE8` | MODE:274 |
| `+0x18` | qword | `state+0x5AD0` (restored only when `rec+0x18` bit 1 set) | MODE:275, C-MODE:84-85, MODE:969-970 |
| `+0x20` | qword | `state+0x5AD8` | MODE:276 |
| `+0x28` | dword | `state+0x5B04` | MODE:277 |
| `+0xC`/`+0x10` floats | | restored through `00304790`/`003047C0` when `byte[rbx+8] & 1`, then `+0x5B04 |= 2` | MODE:971-973 |

**Field-record table `*(02ADD100)`**: `+0x04` count, rows from `+8`, stride 3; flag = bit 15 of `(row[1] << 8) + row[0]`, i.e. bit 7 of `row[1]` (C-MODE:77, C-MODE:242-254, C-MODE:285-290).

**Transition table `01EECFC0`**: rows of 32 bytes, 4 cells (8-byte pointers) per mode row; rows 0 and 4 zero; row 3 `0016D6A0` ×4 (MODE:348, MODE:357-373). Column semantics contradict — see C.1.

**Special-sequence globals** (MODE:385-404): `022C2160` state 0–7; `022C215C` kind (table at `00306D08`, ids `0x94`–`0x113`); `022C2168` owner; `022C2158` flags; `022C1F50` accumulated-HP table "32 entries of 16 bytes" (internal inconsistency, C.1); one-shot `0208E6A8`.

**Countdown row API `02B5EBC0`** (stride `0x14`): `[row+0]` value, `[row+4]` bound, `[row+8]` float value, `[row+0xC]` rate, `[row+0x10]` 0, `[row+0x11]` arrived flag (MODE:1061, MODE:1425); byte getter `003EBB70` reads `02B5EBD1 + idx*20` (MODE:1065-1068). Rate "`0.016675` or `0.02` per tick by `00290180()`" (MODE:549-550).

**Selection state block (`0035BC50`)** (MODE:735-747): `022C8060` dword flags (bit 0 focus matched, bit 2 picker latch), `022C8064` word accepted count, `022C8066` word, `022C8068` dword, `022C806C` focus handle, `022C8070` preferred selector, `022C8074` word matched index (init -1), `022C8076` word (init -1), `022C8078` qword pointer; slots `022C8080`+`0xC0`k (k<4): `+0x00` flags byte, `+0x04` packed actor handle, `+0x60` word (MODE:723-729); `022C8388` four pointers stride 8; command list `022C83F0`/`022C83F4`/`022C83F8`.

**Target cursor ring** (MODE:801-860): head `022BEDA0`, tail `022BEDA1`, 64 entries × 8 at `022BEDA4` (dword handle + 4 bytes padding); selected unit `02089350`; unit flag bits 12 (queued) / 13 (popped).

**Log call I/O** (LOG:124-140 withdrawn; LOG:249-273, LOG:317-321): in `ecx` channel, `rdx` fmt, varargs; `vsnprintf_s(options=4, buf, 0x4000, _TRUNCATE(-1), fmt, locale 0, ap)`; out: virtual slot 1 `(sink, channel, buf)`; nothing returned stated. Options qword `02EBA3D0` = 4 (LOG:78-86).

**Pooled relation record** (ONES:291-297): 16 bytes; `+0x4` key, `+0xC` own slot 0–31, `+0xD` prev (`0xFF` none), `+0xE` next (`0xFF` none), `+0xF` low nibble kind (0 free). List head (separate): head `+0xC`, tail `+0xD`, count `+0xE` (ONES:300-302).

#### 1.4.3 State

| global/object | size | initial value | writer(s) | reader(s) | lifetime | cite |
|---|---|---|---|---|---|---|
| `02EBF190` (pointer slot) | 8 | 0 (BSS) | `00238A92` in `00238A80` (tail of `002EF650`), `00233C33` in `00233C10`; both store `021B290C` | 131 reader functions | set at boot transition (state-0 exit), never nulled | C-MODE:425-436, C-MODE:520 |
| `state+0x5B04` | 4 | not stated directly (save-image memset by `002EF650`, C-MODE:437-438; zeroed by `0030DA10`) | setters `00313550`/`00313840`/`00303D90`/`00307240`/`00307200`, `00306760`, `002EF410`, `00584210`, `005843E0`, `0030DA10` | ladder, getters, `00304140`, `00313650`, `002EF3C0` | persisted across transitions and saves | MODE:576-589 |
| `state+0x5B08` | 4 | zeroed by `0030DA10` | `0030D8B0` when `commit ≠ 0` | `0030D8B0` | not stated beyond reset | MODE:375, MODE:446 |
| `022C2160`/`022C215C`/`022C2168`/`022C2158` | dwords | 0 = idle | four writers `00306BD0`, `00306B10`, `00306760`, `003065D0` | 26 `.text` refs; 11 readers of `state−5 ≤ 1` | per special sequence | MODE:385-425 |
| `022C1F50` table | 32 × 16 B | not stated | `00306760` | `003065D0` kinds 3/4, `0030D810` | cleared after kind 3 | MODE:391, MODE:406-414 |
| `022BEDA0`/`022BEDA1`/`022BEDA4` ring | 2 B + 512 B | zeroed by `0030FE60` | `00304E4B`–`00304E74` | `00313DB0` | not stated | MODE:849-860 |
| `02089350` | 8 | not stated | `00313DB0` | capability policy | not stated | MODE:828-829, MODE:840 |
| `022C8060`..`022C8078`, `022C8080` slots | see I.2 | `022C8074`/`022C8076` = -1 per pass | `0035BC50` | `0035D980` | rebuilt per call | MODE:735-747, MODE:1381 |
| `02CB6150` sink pointer / `02CB6158` guard / `02CB6140` object / `02CB6148` guard | 8/4/—/4 | guard per MSVC magic static | `005CDAA0` cold path (`005CDB81`), `005CDA30`, `_Init_thread_header`/`footer` | `005CDAA0` | built on first log call; `atexit` `008AADA0` | LOG:169-172, LOG:201, LOG:265-272 |
| `02EBA3D0` options qword | 8 | zero, then `|= 4` by `00809C50` before game entry | `00809C50` only | 22 readers | fixed from C-init | LOG:78-86 |
| `02EAED3C` `_tls_index` | 4 | loader-written (LOG) | loader (LOG:282) / `00189CE0` (APP:772) — C.1 | 709 functions | process | LOG:169, LOG:280-284 |
| pool `02CA81F0`–`02CA83EF` | 32 × 16 | init loop `00512F10`–`00512F1F` writes `+0xC` = n, clears kind nibble | five pool users | same | not stated | ONES:279-302 |

#### 1.4.4 Order

- Ladder is a pure query; asked whenever a consumer asks (C-MODE:583 "`TIMING` — nothing here establishes *when* a consumer asks").
- Transition dispatcher `0030D8B0` runs from `00233AA0` "which [the field runtime pass] §5 reaches when all four roster members are idle, and by `00233CF0`" (MODE:345-347); also from the party-read-in task `0037C730` (C-MODE:406-407).
- Ride per-frame: "the frame handler copies the channel back each frame" (MODE:315).
- Special sequence: state 6 set by `003065D0` "on the field frame's step 11" (MODE:403); state 3 "from the owner's frame" (MODE:400).
- Boot: `02EBF190` filled at the tail of `002EF650`, run from `0022B6E0` inside the `0209273C == 5` block; leaving master state 0 requires that init in the same tick (C-MODE:437-456).
- Save/load: capture on transition, restore, then normalise (`00584210`) clears bit 0; snapshot restore clears bit 1 (MODE:584-589).
- Log: `02EBA3D0 |= 4` at C-initializer time "before the C++ walk and before game entry" (LOG:82-84); sink built on the first log call (LOG:265-272).
- `0035BC50` raises the leader picker (request 3) "once, latched by `022C8060` bit 2" (MODE:787-790). Not stated when `0035BC50` itself runs per frame.

#### 1.4.5 Dependencies

- Script VM (`01-Script-VM-Native-Bridge`): verbs `0x050F`–`0x0516`, `0203`/`0207`/`3044`/`0408`/`0512`, `037E`/`037F`/`03EC`/`0407`/`0511`, `302F` (MODE:136-143, MODE:292-302).
- World/Area/Field (`03-World-Area-Field`): field-record bit 15 (MODE:617; C-MODE:564-567); area id `003148F0`.
- Party (`11-Party`): roster slot 3 (mount), battle-state block map (MODE:263-265, MODE:310, MODE:536).
- Save/Load: `002EF3C0`/`002EF410`/`00584210`/`005843E0`; save image `021B290C` (C-MODE:432-436).
- Presentation (`17-Presentation-Rendering`): render record array `022C6F28` stride `0x740`, `003E6AA0`, `RenderRecords_ProcessDirtyState` `00427DE0`, `003B3C00` (MODE:553-569).
- UI (`16-UI`): request router, `02092730`, request ids 3, 11, 24 (MODE:774, MODE:786-787).
- Developer console: commands 229/230 via `0017D380`/`0017D3A0` (`+0xE1D`/`+0xE1E`) (MODE:315, MODE:319).
- Combat Action (`07-Combat-Action`): `00306760`, action rows, `Dismiss`/`Dismount` (MODE:342-343).
- Force-fight mode (00, FORCE): `00309A90` returns 24.0 under force-fight (MODE:428-429).
- LOG: CRT import `api-ms-win-crt-stdio-l1-1-0.dll` (LOG:113, LOG:208-209); PhyreEngine `Phyre::PTTYCallback` (LOG:201); 24-Compiler-And-CRT-Runtime lazy statics (LOG:289-292).
- DUP: 24-Compiler-And-CRT-Runtime thunk layer (DUP:255); 22-Middleware-PhyreEngine reflection (DUP:261).

### 1.5 Encoded-id space, class registry, query record, basis helpers, ABI recovery

Pages: `EID`, `CLS`, `C-EID`, `QREC`, `BASIS`, `ABI`.


#### 1.5.1 Entry points

| function (address + name) | role | callers as stated | cite |
|---|---|---|---|
| `00309440` FUN_00309440 (30 B) | id → class: `[01EEBCF8 + (id>>12)*0x58]`, nibble > 0xE → −1 | class-1 arm of `00322C50`; `0031C5D0` | EID:91-94, EID:718-726, C-EID:48, C-EID:412 |
| `00322C50` BattleEncodedId_IsValidForClass | class 1..32 validator, 32-entry table `00323054`, shared tail `0032302C`/`0032302E` | 71 functions, 110 sites; 84 pass a constant class; 26 are `0031C5D0` arms | CLS:76-84, CLS:232, CLS:313-316, CLS:404, C-EID:49 |
| `0030B6A0` InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState | fills descriptor lanes +08/+20/+30, prefix +40, zeroes state+57C8 (0x200), ANDs state+59C8 (0x80) with F8 | `SaveRuntime_RebindImageBackedGameplayState` (00238A80); call sites `00233C2A`, `00238A89` | EID:108-129, C-EID:50, C-EID:282, CLS:581 |
| `0031C5D0` query-record filler (8,136 B) | clears QWORD+18, dispatches `class−1` through `0031E598`; returns 0 / −2 / class-19 −1 | "fourteen direct callers" (EID:62); 12 own-record callers (EID:208); "17 direct callers" (CLS:321); `0035D330`, `0035D380`, `0035E070`, `00536410` | EID:171-181, C-EID:51, CLS:173 |
| `0035D330` row/DWORD wrapper | writes tag + DWORD+4 of `022CA520`, calls filler, zeroes 0x98 on negative, returns record | 76 (edges.tsv) / 75 (census) / 159 sites | EID:176-178, EID:206, EID:675, CLS:321-322, C-EID:52 |
| `0035D380` id/WORD wrapper | writes tag + WORD+6 of `022CA480`; same failure rule | 14 / 15 sites | EID:176, EID:207, CLS:321, C-EID:53 |
| `0035E070` | third producer: writes `id<<16` to `022CA524`, class 1 to `022CA520`, calls filler, formats +0x18 with text `0x833` | not stated | EID:181 |
| `00309EC0` BattleEncodedId_DispatchQueryMode0Value (102 B) | `0xFFFF`/nibble>E → −1; bound `id&0xFFF` vs +0x3C; `jmp [+0x50]` as `handler(id, 0)` | 14 callers (CLS:627); `0031C5D0`, `00315E90`, `00301AD0`, `00317930`, `00576A50` | EID:131-137, C-EID:345-351, CLS:625-633, C-EID:409-416 |
| `0030AE30` BattleEncodedId_DispatchQueryMode1 | same, mode 1 | `0031C5D0` | EID:132, C-EID:412 |
| `0030ADC0` BattleEncodedId_DispatchQueryMode3 | third fixed-mode twin | `0030B270` | EID:290-291, EID:798, C-EID:412 |
| `003008A0` Inventory_ModifyEncodedItemAndUpdateDiscoveryState | the one write entry `(id, delta, absolute, channel, flags)` | 25 callers; bundle handlers `002FD530`/`002FD640`/`002FD780`; `00300BA0` shim | EID:279-286, EID:1033-1037, C-EID:413 |
| `00300BA0` (28 B) | fixed-flags trampoline `(rcx, rdx, r8d=1, r9d=1)` into `003008A0` | `00239960`, `0023AF50`, `0032A830` | EID:1033-1037 |
| `00309F30` Inventory_QueryEncodedItemStateByClass | read entry `(id, mode)`, mode 4 → bitset query | `003008A0`; `0030A4E0` | EID:288-290, CLS:574 |
| `002FD150` / `002FD8D0` InventoryPackedCountClass_MutateChannels / _QueryChannel | packed-count handlers | descriptor +0x48 / +0x50 | EID:303-315 |
| `002FD420` / `002FD970` InventoryBitsetClass_MutateState / _QueryState | bitset handlers | descriptor +0x48 / +0x50 | EID:317-324 |
| `002FD530` / `002FD640` / `002FD780` / `002FD880` | bundle 14 / selector 15 / bazaar 18 / gil 19 mutate handlers | descriptor +0x48 | EID:337-342 |
| `00325F40` InventoryDerivedIndex_UpdateOnPresenceTransition | 0↔non-zero → add `00252E60` / remove `002535D0` | every channel-1 change | EID:313, EID:375-386 |
| `00253240` SaveRuntime_InitializeImageBackedPointerDescriptor | builds capacity table `02092760` | `SaveRuntime_InitializeHeaderAndImageBackedState` (via `SaveRuntime_ResetActiveImageAndRebindState` `002EF66F`); `00253480` (← `0035C584`, tail from `0030483D`) | EID:407-430 |
| `00236C30` (1,037 B) | area-load binder of descriptor slots from `battle_pack.bin` directory | `00238850` (CLS:579) | EID:228-233, CLS:172, CLS:228 |
| `002F9860` / `002F9920` | text/description id resolvers (`id/1000`, `id/10000` buckets) | `0029FF60`, `0029CB80`, filler +0x10 | EID:469, EID:932-942, C-EID:358, C-EID:362-366 |
| `0062DDE0` / `0062DFB0` | basis-column helpers `C -= B*t` / `C += A*b + T*a` | "who calls either function" not claimed (BASIS:112-113); VTIDX:1409-1410 lists them as `PWorldMatrixFlyController` slots 7 and 8 | BASIS:31-47 |
| `00189130` (642 B) | writes the basis layout; three axis-angle rotations via `00185100` | `FUN_00187950` (Presentation) | BASIS:119-145, BASIS:158, BASIS:162 |
| `00185100` (951 B) | call-free 4×4 product `out[rdx]=[rcx]×[r8]` | `00189130` ×3 | BASIS:166 |
| ABI subjects `0031B760` (1 pointer arg), `003299B0` (3 args, r8d parked at +0x2C) | contract corrections | `0031B760`: 25 spawn callers etc.; `003299B0`: `00313500` | ABI:62-79, ABI:183-185, ABI:323 |

#### 1.5.2 Inputs and outputs

**Encoded id (16 bits):** "nibble = id >> 12 ; index = id & 0xFFF … class = descriptor[+0x38] = 5 + nibble … valid = index < descriptor[+0x3C]" (EID:489-492). Id bases per class `0`..`E000` (CLS:490-492).

**InventoryClassDescriptor (0x58) at `01EEBCC0`, 15 rows** (EID:112-125, EID:494-499, C-EID:61-72):

| offset | width | meaning | cite |
|---|---|---|---|
| +0x00 | QWORD tested, low DWORD used | region A offset in state block | EID:114, EID:495, C-EID:65 |
| +0x08 | QWORD | region A pointer (runtime) | EID:115, C-EID:66 |
| +0x10 | u32 | region A length in WORDs | EID:116, C-EID:67 |
| +0x14 | 4 | "Four-byte declared interiors; no meaning promoted here" | C-EID:68 |
| +0x18 / +0x20 | QWORD / QWORD | region B offset / pointer | EID:117-118 |
| +0x28 / +0x30 | QWORD / QWORD | region C offset / pointer | EID:119-120 |
| +0x38 | u32 | class 5..19 | EID:121 |
| +0x3C | u32 | id count | EID:122 |
| +0x40 | u32 | cumulative id base (exclusive prefix, 32-bit wrap) | EID:123, C-EID:71 |
| +0x44 | 4 | no meaning stated | C-EID:68 |
| +0x48 / +0x50 | fn ptr | mutate / query handler | EID:124-125 |

Shipped rows (EID:501-516): 5: 0x40 A+0x4748(64w) C+0x57C0; 6: 0x1A4 A+0x47C8(420w); 7: 0x200 A+0x4B10(512w) B+0x57C8; 8: 0x51 A+0x4F10(6w); 9: 0x18 A+0x4F1C(2w); 10/12/16: 0, no handler; 11: 0x100 A+0x4F20(16w); 13: 0x200 A+0x4F40(32w); 14: 0x200, 15: 0x100, 18: 0x80, 19: 0xFFF mutate-only; 17: 0x20 A+0x4F80(2w). Sum 6892 (C-EID:76).

**Packed-count word:** bits 0-9 total (cap 99), bits 10-15 reserved; mode 0 total−reserved, 1 total, 2 reserved, 3 region-B byte (EID:301-306, EID:547-552). **Bitset:** word `index>>4`, bit `index&0xF` (EID:318, EID:554-555).

**EncodedIdQueryRecord (0x98)** (EID:518-520, C-EID:78-82, QREC:40-41, QREC:90-120):

| offset | width | meaning | cite |
|---|---|---|---|
| +0x00 | DWORD | class tag (class 1 may rewrite) | C-EID:78, QREC:92 |
| +0x04 | DWORD | row request (classes 2..4, 19..29, 32) | C-EID:86 |
| +0x06 | WORD | id request (classes 1, 5..11, 13..18, 30, 31); overlaps high half of +4 | C-EID:86, QREC:40-41 |
| +0x08 | ptr | auxiliary text (classes 10, 20, 21, 24 …) | EID:520, QREC:100-113 |
| +0x10 | ptr | description | EID:520 |
| +0x18 | ptr | name; cleared at entry `0031C5F0` | EID:171-172, QREC:65 |
| +0x20 / +0x24 | s32 | query channel 0 / 1 | EID:135-136, EID:520 |
| +0x21..+0x25 | bytes | licence bytes (25/32), status +0x25 low 5 bits (26) | EID:215, QREC:114-115, QREC:164-165 |
| +0x28, +0x2A, +0x2C, +0x30, +0x36 | various | class-specific (see QREC §4) | QREC:103-120, QREC:160-165 |
| +0x38..+0x90 step 8 | DWORD | class 10 sentinels `FFFFFFFF` | QREC:140-146 |
| +0x3C, +0x44, +0x48, +0x50, +0x54 bit0, +0x58/+0x5C/+0x60 | | class 6 equipment block | EID:532-534, QREC:128-138 |
| +0x94..+0x97 | 4 | untouched by class-10 loop | QREC:145-146 |

Per-class producer table: QREC:90-120 (32 rows). Failure: direct −2/name cleared; wrapper zeroes 0x98 (C-EID:182, QREC:68-72).

**Bundle rows:** class 14 12 B `{u32 gil; u16 itemA; u16 countA; u16 itemB; u16 countB}`; class 15 12 B `u16 idA[3]; u16 idB[3]`; class 18 36 B (EID:562-564).

**Derived-index lists:** u16 id arrays in `*(020927C0)`, counts `+0x47B8 + 4×list`, capacity table `02092760` `{u16, s16 capacity, u32 offset}`; bases/capacities table EID:415-418; category flags `+0x3244` bits 1..8 (EID:387-401).

**Basis structure:** twelve floats `+0x08…+0x34`, rows A/B/C, fourth column T at `+0x14/+0x24/+0x34`; scratch `+0x38…+0x74` (BASIS:57-68, BASIS:107-110).

**Files read:** `battle_pack.bin` st2e sections, `+4` row count, `+8` stride, rows at `+0x20` (EID:72, EID:233); directory offsets per class EID:239-268.

#### 1.5.3 State

| global/object | size | initial value | writer(s) | reader(s) | lifetime | cite |
|---|---|---|---|---|---|---|
| `01EEBCC0` descriptor table | 15 × 0x58 (to `01EEC1E8`) | runtime lanes/prefix zero on disk; offsets/counts/handlers authored | only `0030B6A0` stores (E11) | 28 functions / 49 refs (C-EID:268-270); "fifteen functions" (EID:291-297) | rebuilt on each rebase; "Repetition recomputes" | EID:75, C-EID:101-104, C-EID:392, C-EID:400-401 |
| `022CA520` / `022CA480` static records | 0x98 each | not stated | wrappers, `0035E070` | callers via returned pointer | static; aliasing on next call | C-EID:110-113, QREC:74-77 |
| state block (rebase base) | not stated | not stated | inventory handlers | | "`02164280 + 0x4E68C`, passed by both callers" | C-EID:281-282 |
| `[02EBF190] + 4` discovery flag dword | 4 | not stated | `003008A0` | `00318CD0` | not stated | EID:285-286, EID:363-373 |
| `01EECF98` school bits `{2,4,8,0x10,0x20}` | 5 | image data | — | `003008A0` | static | EID:365-366 |
| `01EED1B0` nibble → list map | 11 pairs | image data | — | `00325F40` | static | EID:377-381 |
| `02092760` capacity table | 12 × 8 | zero on disk | `00253240` | `00252F40` | rebuilt on image reset | EID:407-430, EID:1110-1120 |
| `020927C0` image-backed block pointer | ptr | not stated | `00253970` binds it to runtime buffer `+0x8200` | list code | not stated | EID:382, EID:405-406 |
| `01F83530` relocation base | QWORD | "**It is zero at image load**" | none by rip store; one computed route `00210570` id `0xFFFB` | `0020E600`, `0020E620` | "supported, not proven" zero for process life | C-EID:284-295 |
| `02EBF038…02EBF150` slot descriptors | count at +4 | bound at area load | `00236C30` (+ helpers) | validator arms, filler | rebound each area load | CLS:208, CLS:228, CLS:263-265 |
| `02EBF078` fourth key-item slot | | ships `0 × 10` | `00236EDA` | validator | | CLS:367-375, C-EID:256-258 |
| `01E0C560` ring counter / `0209C390` 8×0x20 slots | | not stated | `0029CB80` | callers | "small rotating scratch" | C-EID:366 |
| `02ADED98` schedule row pointer | | not stated | `0037DDD0` | `0037DEA0` | | EID:444 |
| `022BE930` / `01EEBAF0` concurrence debug override | | not stated | | `002F8D60` | | EID:438 |

#### 1.5.4 Order

- Area load: "`00236C30` binds the descriptors from the blob directory (34 sections)" (EID:576); "the descriptor pointers are rebound at every area load by `00236C30`" (CLS:263-264).
- Save load / reset: "`0030B6A0` rebases the fifteen inventory class descriptors onto the state block" (EID:577); "This is an on-disk observation, not proof of live order." (C-EID:158).
- Image reset: capacity table rebuilt "whenever the active image is reset" (EID:430).
- Inventory change: `003008A0` → before `00309F30` → `+0x48` handler → `00325F40` → `0046A630` → discovery bit on first acquisition (EID:578-582).
- On demand (menus, messages): wrappers → `0031C5D0` → validator → arm (EID:569-574).
- Per frame: `0037DDD0` from `MainLoop_UpdateAndRenderFrame` (movie fade schedule) (EID:444, EID:645-649).
- Starting inventory: `0023AF50` after `002370C0` state reset (EID:439).
- Basis helpers: not stated.

#### 1.5.5 Dependencies

- 02-Resource-And-Asset-Pipeline: battle text banks (EID:71-73, EID:692), authored-data table registry / UQ-80 (CLS:186-188, CLS:291-297).
- 11-Party: battle state block field map (EID:694), party configuration class 23 (CLS:131).
- 12-Items-Equipment-Shops-License: item id encoding (EID:100, EID:693), bazaar page (EID:330, EID:352), licence check (CLS:130), shop table (EID:447).
- 19-Save-Load-Settings: save payload field map (EID:382, EID:695).
- 07-Combat-Action: message table (EID:315, EID:697).
- 09-Combat-AI-And-Gambits (EID:262); 13-Rewards (EID:440); 17-Presentation screen fade (EID:648); 16-UI shop screens (EID:759).
- 05-Spawn-Encounter-Lifecycle CONTRACT-group-completion-and-respawn (ABI:81-82); 22-Middleware-PhyreEngine (ABI:102-103); 21-RNG (CLS:563).
- Within 00: VTIDX for `0062DDE0`/`0062DFB0` (not cited by BASIS).

### 1.6 Shared transform workbench (EE/VU0 register bank, save/restore, primitives)

Pages: `EEVU`, `SAVE`, `WB`, `PRIM`, `C-WB`, `C-SAVE`, `C-PRIM`.


#### 1.6.1 Entry points

| function (address + name) | role | callers as stated | cite |
|---|---|---|---|
| `0036D990` (74 B) emulation start-up | stores vf00 = (0,0,0,1) and prints `"Sizeof 64 bit int = %d\n"` with 8 and the completion line through `0017D280` | boot routine `0022A0B0` at `0022A125` | EEVU:73-74, EEVU:277, WB:365-368 |
| `0036D9E0` (918 B) clear | "writes **80 slots and reads none**"; qword pairs over `022D91B0`–`022D9428`, plus vf00 header | `003DFFE0` (channel-rate emit) and `CharacterRender_UpdateCombatLookAndAuxControllers` `003E00C0` | WB:109-121, WB:229-234, C-WB:55, C-WB:247 |
| `0036DD80` (15 B) vf00 re-establish | `movaps xmm0,[008C5FD0]` → `movups [01EF93F0],xmm0` | 33 frontier callers; `0025C830`, `0035DCC0`, audio `00361DE0`/`003623C0`/`00363FD0`, `002F1D90` | WB:628-631, EEVU:70, EEVU:372-374, SAVE:287 |
| `0036DD90` (11 B) / `0036DDA0` (8 B) | `or dword [022D9470], 0x80` / `0x40`; never read | `00361DE0`, `003623C0` | EEVU:248-251, EEVU:374 |
| `0036D930` (89 B) Save | variadic: `ecx` = count, pointers in `rdx`,`r8`,`r9`, stack; copies 16 B per pointer; assigns depth | exactly nine: `0044BAC0`, `0026EE00`, `0042FDB0`, `003AFDD0`, `00431D30`, `00462260`, `003D8E50`, `002F1D90`, `002F1CE0` | SAVE:58-74, SAVE:122-132, C-SAVE:44, C-SAVE:119-131 |
| `0036D8E0` (66 B) Restore | no args; writes saved values back for `i < depth`; depth = 0 | same nine; four by tail-jump `0026F413`, `003AFFAB`, `00431F0A`, `0046242E` | SAVE:76-84, SAVE:115, C-SAVE:45, C-SAVE:133-140 |
| `00398F90` (377 B) `TransformPointByWorkbenchMatrix(in rcx, out rdx)` | row-vector × rows 1–4, w forced from `01EF93FC`; four deposits | 74 non-EH callers / 102 sites (C-PRIM: 81 fns) | PRIM:64-104, PRIM:296, PRIM:412, C-PRIM:44, C-PRIM:283 |
| `00397910` (567 B) `ComposeTransforms(a rcx, b rdx, out r8)` | `out = b × a`, staged, 64 B | 82 non-EH callers / 129 sites (C-PRIM: 86 fns) | PRIM:106-137, PRIM:297, PRIM:412, C-PRIM:45, C-PRIM:283 |
| `003970A0` (44 B) matrix getter | copies `022D91B0`..`+0x30` to `[rcx]` | "seven callers" (PRIM:317) / "28 frontier callers" (PRIM:692) / 29 Presentation bodies (C-WB:247) | WB:83-100, C-WB:54 |
| `0039AF70` general installer | copies whatever `rcx` points at into rows 1–4 | 116 unique call sites (82 calling functions) | PRIM:319-331, C-PRIM:226-268 |
| `0039B550` (195 B) `Workbench_InstallMatrix4x4` | installs `02AEECB0` at all 82 sites; also publishes `02AEE7F0` low32 | 82 sites (fade node `002F1F40`, `0039C4C0`–`0039CCB0`, `00434CD0`–`00455DB0`) | PRIM:311-316, PRIM:328, PRIM:630-635 |
| `003977B0` (349 B) | in-place 4×4: `M[rcx] = M[rdx] · M[rcx]` (row-major) | `00434CD0`, `00435050` | PRIM:805-807, PRIM:567, PRIM:1558 |
| `00397ED0` (342 B) | vec4-by-4x4 transform loop, in-place-safe | 34 frontier callers | WB:623-627 |
| `0026EE00` (1,560 B) colour modulate | `out_byte[i] = min(255, (2·((row[i]·(a+b)) mod 256) + ((a·b)>>7)) mod 512)` | 104 callers; `00442600`, `004427D0`, `00442550`, `002F1F40` | SAVE:150, SAVE:187-191, SAVE:294 |
| `003AFDD0` / `00431D30` / `00462260` | float4 / int32 → byte4 pack via row `022D8F30` | — | SAVE:287 |
| `002F1CE0` / `002F1D90` | 3-vector length / point distance (Q, `022D8F90`) | — | SAVE:287 |
| `003D8E50` | scaled random (RNG gate `022D9138`, state `01EF93E8`) | 43 sites | SAVE:287, C-SAVE:49 |
| `0042FDB0` / `0044BAC0` | authored-expression colour form / type-`0x0A` element walk | `0042FDB0` from 80 sites | SAVE:287, C-SAVE:48 |
| `0025A8E0` (164 B) | VCLIP into `022D9130` | `0025C830` | EEVU:67, WB:589 |
| `0036DDC0`, `0036E1E0` (173 B), `0036DE70` | readers/refresh of the 32×24 B table at `022D94B0` | `0036E1E0` ← `World_UpdateSimulationTick` `00314020` | WB:318-327, WB:732 |
| vocabulary: `00202B10` VADD, `00203080` VSUB, `00202FE0` VSCALE, `00202DE0` NCOPY, `00216660` NORM, `00202E10` XPROD, `00202C90` copy, `00203170` MLOAD, `00202F00` RBUILD, `00217880` ROTCOL, `00217060` MXV, `00202B70` MXVW, `0033CB70` AWRAP, `00335E50` PRED | executed under EXP-130/132 | many (Movement `0033xxxx`, actor, audio, UI) | PRIM:1129-1202, PRIM:1277-1284, PRIM:475-486 |
| `0024C060` | builds `02AEECB0`/`02AEEA20` | `0024B9B0` ×4, VFX group draw `0024D370` | PRIM:336-344, PRIM:491-502 |

#### 1.6.2 Inputs and outputs — record layouts

**Register bank (EEVU:84-98, all BSS):**

| offset/address | width | meaning | cite |
|---|---|---|---|
| `01EF93F0` | f32[4] | vf00 = (0,0,0,1); `01EF93FC` its w=1.0 | EEVU:87, C-PRIM:390-391 |
| `022D8F08` | u32 | save depth | EEVU:88, C-SAVE:59 |
| `022D8F0C` | dword | bit-offset parameter `00502280` → `00501820` | C-SAVE:192-201 |
| `022D8F10 + 16k` | 128-bit | GPR[k], k=0 `$zero` never written | EEVU:89-90 |
| `022D9110` / `022D9120` | 128-bit | HI / LO | EEVU:91-92 |
| `022D9130` | u32 | CLIP flag word | EEVU:93 |
| `022D9138` | u32 | RNG enable/mode, not workbench | EEVU:104, WB:224 |
| `022D9140`–`022D916C` | 12 dwords | GPR↔XMM spill slots (`022D9140` unreferenced) | EEVU:231-247 |
| `022D9198` | f32 | Q | EEVU:94 |
| `022D91A0` | f32[4] | ACC | EEVU:95 |
| `022D91A0 + 16n`, n=1..31 | f32[4] | vector registers (`022D91B0`..`022D9390`) | EEVU:96 |
| `022D9470` | u32 | write-only sticky flags 0x80/0x40 | EEVU:97, EEVU:248-255 |
| `022D94A0` | 64-bit | loop register (not assigned) | EEVU:105 |
| `022D94B0` | 32 × 24 B | record table: `+0` u32 id; `+4` u16 state; `+6` result of `0024DE70`; `+8` s8 (manager, TICK); `+0x10` u8 flags | WB:326-327, WB:732, C-WB:114-115 |

**Save arrays:** pointers `02EC0A00` (8 B/item), values `02EC0800` (16 B/item), structurally 32 items, unenforced (C-SAVE:57-59, C-SAVE:350-360).

**Point-transform deposits:** `022D9300` input (vf22), `022D91A0` accumulator without translation (ACC), `022D9310` result (vf23), `022D8F90` result ($t0), `[rdx]` (PRIM:94-100, PRIM:258-260, C-PRIM:93-111, C-PRIM:273).

**Audio source record (WB:334-348):** base `022CBAF0` + table word; shape `+9 & 0x7F` (0/1/2); radii `+0x38`/`+0x54`/`+0x58`; yaw `+0x50`; half-extents `+0x30`/`+0x34`; own position `+0x20..+0x28`; `+0x14` segments of 32 B from `+0x40`.

**Other tables:** `02EBE5E0` 32 slots × 0x30 (key dword, `byte[+0x20]` bit 0, `+0x1C` arm) (WB:679-697); `01F004E0` sine table 0x8000 entries (PRIM:812-813, PRIM:1654).

**Formulas:** point law PRIM:73; compose PRIM:115-118; `003977B0` float order PRIM:807; modulate SAVE:188-189; `00432300` PRIM:613; `00216660` gates PRIM:1139-1149; MXV alias PRIM:1283. Files read/written: none stated (all BSS).

#### 1.6.3 State

| global | size | initial value | writer(s) | reader(s) | lifetime | cite |
|---|---|---|---|---|---|---|
| bank `022D8F00`–`022D9500` | 1,536 B | zero (past raw data, `01F7E400`) | 249 functions | 251 readers | process; "Registers are volatile by definition" | WB:70-72, WB:202, EEVU:115, C-WB:69-71 |
| vf00 `01EF93F0` | 16 B | 1.0 in file image (`00 00 80 3F` at `01EF93FC`) | `0036D990`, `0036D9E0`, `0036DD80` (C-PRIM/EEVU); "two writers" (WB) | 98 / 129 / 136 functions (see C.1 counts) | set at boot, re-established at runtime | EEVU:70, C-PRIM:374, C-PRIM:398-405 |
| depth `022D8F08` | u32 | zero (BSS) | Save `0036D982` (assign), Restore `0036D91A` (=0) | Restore `0036D8E6`/`0036D912` | per save window | C-SAVE:382 |
| save arrays | 32 × (8+16) B | not stated (BSS) | Save | Restore | overwritten by each Save | C-SAVE:57-58 |
| `022D9470` | u32 | zero | `0036DD90`/`0036DDA0` | none | never cleared (not stated) | EEVU:248-251 |
| `022D94B0` table | 768 B | zero; reset loops set "state word = idx+4 for all 32 slots" | `0036DE5A`, `0036DF6A`, `0036E2F8`, `0036E1E0` | `0036DDC0`, `0036E1E0` | not stated | C-WB:118-120, WB:732 |
| rows 1–4 matrix | 64 B | zero | `0039AF70`, `0039B550` | `003970A0`, `00398F90` | "whatever the last routine to use them loaded" | EEVU:114, PRIM:309-318 |

Threading: one user thread (EEVU:271).

#### 1.6.4 Order
- Boot: `0022A0B0` → `0036D990` at `0022A125`, then `0022CB90` clears VU1 memory `02064E30` (EEVU:73).
- `0036D9E0` is run by the rig frame `003E00C0` and `003DFFE0` (C-WB:247) — per-frame, despite "initializer" naming (WB:107).
- `0036E1E0` runs from `World_UpdateSimulationTick` `00314020` (WB:732).
- Audio: `00362850` listener update → `003631B0` per source → shape helpers (WB:331-337).
- VFX: `00259030` eight sites + `002590F0` call `0024D370` "up to ~40 draws a frame"; `0024C060` once per container (PRIM:491-502).
- Update loop reaches 183 of 267 members, draw loop 40, 35 shared; 84 reached by neither directly (EEVU:270).
- Save/Restore bracket: Save at entry of window, Restore at exit; four restores are tail-jumps (SAVE:115); no nesting on direct graph (SAVE:296, C-SAVE:164-181).
- Element code: compose → install (`0039AF70`) → run points through `00398F90` (PRIM:334).

#### 1.6.5 Dependencies
- 17-Presentation-Rendering (largest client: EEVU:362; effect type dispatch PRIM:332-333; VIF1/VU1 layer EEVU:73; oscillator EEVU:183; element types SAVE:287).
- 18-Audio (closest-point helpers WB:328-352, EEVU:374).
- 21-RNG-And-Determinism (`022D9138`, `003D8E50`: WB:269-271, SAVE:287).
- 02-Resource-And-Asset-Pipeline (authored randomness / expression evaluator SAVE:287; `fontcolor.bin` PRIM:643).
- 03-World-Area-Field (MWeather PRIM:1183).
- 00 boot (EEVU:73), world tick (WB:333, WB:732), ActorEntity/Movement/UI/Party (EEVU:372-390).
- PS2 executable `SLPM_667.50` not shipped (EEVU:227).

### 1.7 Object model (RTTI and the vtable method index)

Pages: `RTTI`, `VTIDX`.


#### 1.7.1 Entry points

| function | role | callers as stated | cite |
|---|---|---|---|
| `001E8580` (text flush) | "the sole constructor and owner of the `DynGeoFontTextSpecial*` objects anywhere in the image" | only caller `0017F850`; `0017F850` called by interpreter `002AC5F0` at `002AD7AE`/`002AC7EC` | RTTI:255-256, 289-291, 390-393 |
| `00213A00` / `00213960` / `002138C0` | constructors `Shadow` / `ShadowFinal` / `Final` (sizes 0x168/0x168/0x170) | `001E8580` at `001E86BB`,`001E88C4` / `001E8A7D` / `001E8F84` | RTTI:267-280 |
| `002142A0` | "slot-10 shared draw" of the four 12-slot vtables | "reached **through the vtable**, and nothing here observes that dispatch" | RTTI:257, 307-312 |
| `00160210` | worked-example CRT static initializer: constructs object at `02CAA0A0` via `00597690`, stamps vtable `00D249A8`, `jmp atexit` with dtor `008A8150` | the CRT initializer table `008C31D8`–`008C5678` (1,172 entries) | RTTI:956-958, 962-964 |
| `008C31D8` table (1,172 slots) | "the **C++ dynamic initializer table**" (`__xc_a` at `008C31D0`) | walked by the CRT "from *outside* its bounds" | RTTI:695-703 |
| `005FD050` | "the MSVC magic-static lazy-singleton getter" returning `02CC0410`; one-time `00615840` construction | "39 frontier callers at census (all in the `0060xxxx`/`0061xxxx` Phyre descriptor band)" | VTIDX:3332-3338 |
| `006A4100` (`PPhysics::PUtilityPhysics` slot 1) | "a lazy singleton init through the stored vtable" (`byte[01F2CDF0]`, `qword[[01F2E9B8]+8]`) | not stated | VTIDX:3101-3107 |
| slot-5 `PClassDataMemberPhyreArray<…>` adapters (e.g. `005C9760`) | "the canonical Phyre member-array element accessor" | not stated (vtable dispatch) | VTIDX:2908-2913, 3017-3025, 3052-3057 |
| `00215320` (`CharacterOrderedObject` slot 1) → `001F5D70` | 9-byte this-adjusting thunk → "the object's render-submission pass" | not stated | VTIDX:2865-2876 |
| `001C2670` (`MultipleDebugDisplay` slot 0) | scalar deleting destructor, object `0x4670` bytes | not stated | VTIDX:2892-2894 |
| `0077E0B0` (`CDepthOfField` slot 3) | "per-frame context gather" | not stated | VTIDX:2794 |
| `007D6270` (`Sd::Driver::SurroundReverb` slot 5) | "per-frame parameter ramp stepper" | not stated | VTIDX:2802 |
| `0075C080` / `007307A0` | `InitializeDevice` (slot 0 of `CRenderTextureArray` / `CTextureUtil`) | `007307A0` calls `007273E0` = `CGPUResourceManage` slot 0 | VTIDX:2803, 2805-2810 |
| Gi* slot 1 (e.g. `GiTrans` `00862D40`) | "slot 1 is execute-against-device" | not stated | VTIDX:2493-2496 |
| `002778C0` `BattleMenu_UpdateCommandSelectionAndDispatch` | "the message proc installed on a widget" (address taken by `lea r8` at `00276DD3`) | address-taken | VTIDX:2626-2631 |
| all 4,275 appendix methods | identity (class, slot) only — "This index gives identity — class and slot — not behaviour" | "Not applicable — this is an index" | VTIDX:127-128, 152 |

#### 1.7.2 Inputs and outputs — record layouts

**MSVC Complete Object Locator** (RTTI:60-68; VTIDX:46-58), at `vtable[-1]`:

| offset | width | meaning | cite |
|---|---|---|---|
| +0x00 | DWORD | signature, "1 on x64" | RTTI:61 |
| +0x04 | DWORD | offset — "this vftable's offset in the object" | RTTI:62 |
| +0x08 | DWORD | cdOffset | RTTI:63 |
| +0x0C | DWORD | pTypeDescriptor, "RVA -> TypeDescriptor" | RTTI:64 |
| +0x10 | DWORD | pClassDescriptor, RVA | RTTI:65 |
| +0x14 | DWORD | pSelf, "RVA of this locator" (the validation) | RTTI:66, 71-72 |

TypeDescriptor `{ void *pVFTable; void *spare; char name[]; }`, name form `.?AV<name>@<ns>@@` / `.?AU…` (RTTI:68; VTIDX:75). Name is "NUL-terminated and contains `@@` internally" (RTTI:847-848); two real names are 264/265 chars (RTTI:852-854).

**Phyre reflection field record:** "Phyre stores short field names inline in the reflection record — SSO-style, up to 7 characters plus a NUL" (RTTI:910-911). Offsets not stated.

**Objects with stated sizes:** `DynGeoFontTextSpecialShadow/ShadowFinal` 0x168, `Final` 0x170 (RTTI:277-280); `MultipleDebugDisplay` 0x4670 (VTIDX:2893-2894); `RazorMarkerPushObj` 0x1 (VTIDX:2485). The §10 census says "92 of 125 classes now have a code-stated object size" (VTIDX:2472) but **does not tabulate the sizes on the page**.

**Other layouts stated (selection):**
- `vector<0x318>` element (CharacterOrderedObject submission list): `+0xF0`/`+0xF8` scalars, `+0x100`/`+0x108`/`+0x110` matrix destinations; source object fields `+0x4B4` visible, `+0x480` id, `+0x4A4`, `+0x4B5`, `+0x4B8`/`+0x4BC`/`+0x4C0`, matrices at `+0x584`/`+0x5C4`/`+0x604` (alt `+0x4C4`/`+0x504`) (VTIDX:2868-2884).
- `005DC400` fixed-shape ctor: `[+0]=0x1010105`, `+4=1`, `+8`/`+0x14`=0, `+0xC=1.0f`, `+0x18=0x400` (VTIDX:4463-4464).
- `005DC1C0` base ctor: `word[+8]=0`, `dword[+0xC]=1`, `[rcx]=rdx`, `or dword[rdx+0x18],0x100`, registers into `[rdx+0x20]` (VTIDX:4469-4473).
- `0067FFB0` aligned-size descriptor: `+8` stack arg, `+0x10`/`+0` zero, `+0x18=(rdx+7)&~7`, `+0x1C=r8d`, `+0x20=(r9+7)&~7` (VTIDX:4385-4388).
- `005DCBE0` ctor (vtable `02CF7A30`): `+8` word 0x300, `+0x18`=2 (VTIDX:5002-5007); `005DBF30` installs same vtable at `+0x20` (VTIDX:5019-5023).
- 0x18-stride record (`005D87E0`): `+0` word, `+2`/`+3` bytes, `+8` tagged string, `+0x10`/`+0x14` dwords (VTIDX:5027-5038).
- 0x38-stride `PAnimationHierarchy` record (`005A5BD0`): `+0`/`+8`/`+0x10`/`+0x18` qwords, `+0x20` dword, `+0x28` tagged string, `+0x30` dword (VTIDX:5197).
- 0x138-stride `PAnimationHierarchy` node: `+0xFF`, `+0x100` count / `+0x108` 16-byte pair table, `+0x110`/`+0x118` vectors, `+0x130` order field (-1 = unordered) (VTIDX:5045-5113, 5185, 5193).
- 0x58-stride records `005BEDC0`/`005B7FD0`/`005A5CC0` (`+0x28` tagged string) (VTIDX:5116-5183); 0x98 flat copy `005A5DC0` (VTIDX:5163-5167); 0xE8 records `006C0BA0` (VTIDX:4610-4618).
- Ownership-flag conventions: bit 31 of a count dword = owned/borrowed (VTIDX:3353, 4414, 4908); bit 0 of a pointer = "intrusive-marker convention … borrowed vs owned" (VTIDX:4564-4566); inline storage when count <= 1 (VTIDX:4969-4970, 4985).
- `006BA720` type-index → record size table `{8, 0xC, 0x10, 6, 1, 2, 3, 0x30, 0x40, 4}` (VTIDX:4633-4641).
- `002D7FA0`: `0209E6B0` indexed record pointer, stride 48 (`(idx+idx*2)<<4`) (VTIDX:4399-4401).
- zero-at-load census file layout `global | vtable | rtti_decorated` (file header line 23).

Files read/written at runtime: not stated (the pages are static-analysis indices). Tool artifacts: `Tools/work/rtti/vtables.tsv` (25,798 rows) (RTTI:21), `classes.tsv`/`methods.tsv`/`report.md` (RTTI:323-324).

#### 1.7.3 State

| global/object | size | initial value | writer(s) | reader(s) | lifetime | cite |
|---|---|---|---|---|---|---|
| `02CAA0A0` (`PClassDescriptorConcrete<PClusterHeader>`) | not stated | zero at load; vtable `00D249A8` stamped by CRT init | `00160210` (`call 00597690`, `and dword [02CAA19C], ~2`) | not stated | created before `main`; destroyed via `atexit` dtor `008A8150` | RTTI:950-958 |
| 346 zero-at-load globals in `.data` tail (from `01F7E400`) | not stated | vtable = link-time constant | 379 CRT initializers | not stated | static init / atexit | RTTI:962-965; tsv header |
| `02CC0410` (descriptor-table singleton) | not stated | constructed once by `00615840` | `005FD050` (TLS index `02EAED3C`, epoch `02CE2610`) | 39 Phyre-band callers | `atexit` registration of `008ADDD0` | VTIDX:3332-3341 ("NOT claimed: the object's class") |
| `[01F7F4C0]` heap singleton | — | — | — | `001E8580` `new` sites (`call 001A1470`) | — | RTTI:271-273 |
| `[01F811F8]` text singleton | — | — | — | `0017F850` via `001B5FA0()` | — | RTTI:256 |
| `byte[01F2CDF0]` / `[01F2E9B8]` | — | — | — | `006A4100` lazy init | — | VTIDX:3103-3104 |
| `02E59BB8` list / `02E59BC0[]` table; `02E58CA0`/`02E58CB0` | — | — | dtors `006C0FE0` / `006BEC40` remove | — | "the registry removal" | VTIDX:4596-4629 |
| `04A7C3A8` | — | — | `001FB310` (`[this+0x4C0]` →) | — | — | VTIDX:2883 |
| PPFX manager `[01F3BA68]→01F3BA78`, counter `dword[02EA0B3C]` | — | — | thunk `006DA8A0` decrements | `CDepthOfField` slot 3 | — | VTIDX:2794 |
| `dword [02EAD348]` driver global | — | — | — | getter `007AED00` | — | VTIDX:2795 |
| `02E48BD0` / `02E47ED0` | — | — | stored by `0069ECE0` into `+0x28` | — | — | RTTI:1032-1036 |
| debug gates `01F3BA80`, `02EA0B40`, `01F3BA90` | — | — | — | `007307A0` | — | VTIDX:2817 |
| `02EA18B1` gate byte | — | — | — | `00721B10` (`CRenderTexture` slot 1) | — | VTIDX:1977 |

#### 1.7.4 Order

- CRT initializers run "before `main`" and register teardown with `atexit` (RTTI:955-958). Order within the 1,172-entry table: "Not sorted (51 % ascending) and ordered in owner blocks — link order" (RTTI:704).
- Text draw: interpreter `002AC5F0` → `0017F850` ("*draw what the last frame accumulated*", scope `display : draw Font`) → `001E8580` constructs `DynGeoFontTextSpecial*` objects; slot-10 draw via vtable (RTTI:255-257, 290-293, 307-312). Frame position otherwise not stated.
- Per-frame (no trigger/time stated): `CDepthOfField` slot 3 (VTIDX:2794), `SurroundReverb` slot 5 (VTIDX:2802).
- `00199D50`/`001E1D90` family: deleting-dtor flag tests (VTIDX:3125-3159) — when objects are destroyed: not stated.
- All other ordering: not stated ("Call chain — Not applicable", VTIDX:127).

#### 1.7.5 Dependencies

- 22-Middleware-PhyreEngine (Phyre reflection, `PMethodCallerConcrete`; descriptor initializers) — RTTI:508-514, 985-987; VTIDX:228-229.
- 23-Third-Party-Libraries (Bullet, Yebis, mkvparser, JsonBox, eastl) — RTTI:213-217.
- 18-Audio (`SQEX::Sd`, `.sab` banks, `ShoutAudioBank`) — RTTI:163-164, 182-192, 387.
- 16-UI (text/DynGeo contract, character mapping) — RTTI:244-257.
- 99-Unresolved-Residual (glyph-run rendering; unowned-code census; largest unclassified) — RTTI:255, 297, 352; VTIDX:2566, 2608.
- 24-Compiler-And-CRT-Runtime (static-initialization order) — RTTI:677.
- 08-Combat-Formula (step table `01EFA5C0`, interpreter sites) — RTTI:398-403, 675, 680-683.
- 07-Combat-Action (battle action handler table `01EEC460`) — RTTI:676.
- 06-Movement-And-Navigation (battle locomotion) — RTTI:520, 620.
- 02-Resource-And-Asset-Pipeline (VBF shout path tables) — RTTI:195-197.
- 17-Presentation-Rendering (`Gi*` render commands) — VTIDX:2565.
- 00 Application-Root (GameApplication) — VTIDX:2505-2506.
- Crossing lists (tier 2, edge-file only): Presentation, Input, CombatAI, CombatFormula, Items, RNG, Resource, Audio, ActorEntity, Gameplay, Party, Script_VM, UI, WorldAreaField — VTIDX:2837-2862; Status_Periodic_Terminal, Audio, CombatFormula, Presentation, UI — RTTI:939-947.

### 1.8 Shared-state accessors and the ownership boundary

Pages: `HUBS`, `NBR`, `OWN`.


#### 1.8.1 Entry points

| function (address + name) | role | callers as stated | cite |
|---|---|---|---|
| `00265020` `Actor_GetWorldPosition` (61 B) | actor world position; class-gated (class 1 or 3) | 79 callers / 11 subsystems; table by subsystem; 16 untagged listed | HUBS:47, 58-72, 78-80, 206, 302-309 |
| `003148F0` `WorldTransition_GetActiveOrPendingFieldId` (27 B) | returns `max(0, payload[+0x1044])` | 49 callers / 10 subsystems; incl. `00233780`, `002F8060`, `003160C0` | HUBS:82-125, 207, 292-296 |
| `00236820` `BattleUnit_GetBySlotIndex` (37 B) | `[0208E688] + slot × 0xF50` after bound `slot ≤ [0208E6A0] − 1`; no occupancy check | 40 caller functions / 46 call sites; 9 subsystems | HUBS:127-141, 161, 208, 342 |
| `00236850` `BattleUnit_GetSlotCount` | returns `[0208E6A0]` | not stated as a count | HUBS:162 |
| `00358940` `ActorManager_GetRecordByOrdinal` | `manager+8` array, entry `[arr + 8 + i × 8]`; no generation check | 75 callers | HUBS:163 |
| `003589B0` `ActorHandle_EncodeRegistryEntry` | packs `((entry+0x16 & 0x7FF) << 20) \| ((entry+0x15 & 0xF) << 16) \| entry+0` | 63 callers | HUBS:164 |
| `003588B0` `ActorHandle_ResolveRegistryEntryByPackedId` | class bits 16-19 `< 5`, manager `02098E10 + class × 0x288`, generation bits 20-30 must equal `entry+0x16` | not stated | HUBS:165 |
| `0031B7E0` `BattleUnit_ResolveByFocusHandle` | only while bit 4 of `02089340`; returns `entry+0x30` | 35 callers | HUBS:166 |
| `00320A40` `BattleStats_GetByBattleSlotIndex` | party index 0-39 → `*(02EBF190) + 8 + i × 0x1C8` | 18 | HUBS:167 |
| `00320AB0` `BattleStats_GetByMappedBattleSlot` (49 B) | via `BattleSlotMap_ResolveMappedBattleSlot` `0031B9F0` | 25 | HUBS:168; NBR:145-147 |
| `0031B770` `BattleUnit_FindByCombatantId` | scans pool for unit whose `+0x698` equals party element; cannot return an enemy | 10 | HUBS:169, 180-183 |
| `0031B860` `BattleStats_FindOwningBattleUnit` (83 B) | same pool scan for any stats record | 62 | HUBS:170; NBR:140-143 |
| `002367A0` `BattleUnit_FindByDefinitionSelector` | class-2 id; pool walk on stats `+4` (u16), 0xFF compared as 0xFFFF | 10; opcodes `0x4026`–`0x4035` of the locomotion decoder | HUBS:171, 193-197 |
| `002EF2B0` `SaveImage_GetPersistentPayloadBase` (20 B) | `002EF640()` (static `02164280`) + 0x200 | 70 callers | HUBS:331, 606-612 |
| `00264010` (53 B) | sign router: `ecx>=0` → `00358940`; `<0` → `003590D0` then `003588B0` | 32 frontier callers | HUBS:572-576 |
| `00263F10` (44 B) | type-2 record forward via `003587C0` | 31 frontier callers | HUBS:577-581 |
| `003587C0` (50 B) | class byte → manager → `[tbl + ebx*8 + 8]` | 10 | HUBS:586-593 |
| `002F9860` | encoded-id → runtime record resolver (id/1000 bucket `< 0x1C`, id%1000 index) | 129 callers at census | HUBS:552-565 |
| `00264790` (30 B) / `00264770` (30 B) | gated `movsx word[+0x7C]` / `[+0x7E]` of `02098E10` ptr, else -1 | 00264770: `002B7B80`, `002BA310`, `004048E0` | HUBS:671-677, 818-828 |
| `00320A30` (16 B) | `+0x698` link read | `002F8060`, `002F8E70`, `002FA290`, `00469A50` | HUBS:785-791 |
| `0018E470` (34 B) | two-call context gate `0065E5D0`/`001976E0` & `byte[+0xA0]` | "several hundred callers" | HUBS:846-863 |
| `00249C60` (51 B) | play current context's sound: mute guard, `003A1180`, tail `002DF220(id, 0x40, 0x7F)` | 99 callers | NBR:78-81, 265 |
| `003A1180` (111 B) | packed handle `02AEF3FC` → id, generation-checked, `(word[+8] << 9) + argument` | CombatFormula, Rewards, Presentation `0046CC70` | NBR:92-96, 370-371 |
| `00267330` (39 B) | `byte[02098E10 + slot*0x288 + 0x10]`: bit0 set → bit 7, else 1 | `0050EEE0`, `00358CB0` | NBR:97-98, 371-372 |
| `002DF220` (92 B) | play entry; `003603C0()` must be 0; masks 0x7F; clears bit 31; tail `001DBDB0` | `003112F0`, `0030C650`, `00357040` | NBR:99-101, 369 |
| `003603C0` (8 B) | `return (signed char)[022CB726]` | not stated | NBR:100, 269 |
| `001DBDB0` (76 B) | forwards id to audio manager singleton `01FD36A0`; group `id >> 9` | `002DF010`, `002DEF40`, `002DF220` | NBR:102, 280-298, 448 |
| `00322C50` `BattleEncodedId_IsValidForClass` (1,025 B) | `class - 1 > 0x1F` → 0; 32-entry jump table `00323054`; `0 <= id < count` per slot | 71 callers | NBR:108-118, 329 |
| `00307D10` `BattleUnit_UpdateEngagementStateFlag` (224 B) | engagement test `([sub+0x64] \| [sub+0x3C]) & 0x8000020`; Chocobo short-circuit | not stated | NBR:122-134, 149-151, 332 |
| `00312280` `BattleUnit_ProcessDefeatRewardsAndLoot` (857 B) | killer `rcx`, defeated `rdx`; `+0x698` gate, `+0xE9A` bit 3 suppresses | not stated | NBR:204-215 |
| `0020E600` `ImageAddress_ResolveRuntimePointer` (10 B) / `0020E620` `RuntimePointer_EncodeImageAddress` (9 B) | `D(u)=B+u32(u)`, `E(p)=u32(p)−u32(B)`, `B=[01F83530]` | 815 / 279 callers | NBR:164-186, 275-276 |
| `001EDE70`, `0032A150` `GameClock_GetRawTickCounter`, `00229E40`, `00229DF0`, `00229EA0`, `001EDDA0`, `001EDEC0`, `00229E70` | global accessors / predicates | not stated | NBR:227-236 |
| `0026C8C0` `ActorManager_BindLoadedDefinitionPayload` | first setter of slot `+0x10` bit 7 (`or 0x82`) | only caller `0032F850` | NBR:326 |
| `003B8670` (4,578 B) action timeline interpreter | `(record, prevTime, nowTime, nowTimeF)`; fires entries with `prevTime < key ≤ nowTime` | `004FF2C0` (from `0046E990`, `0046EFD0`), `0046EFD0` (from `00333280`/`003331A0`) | OWN:496-512 |
| `004FF2C0` (85 B) | multi-arm record interpreter on `byte[rcx+1]` | `0046E990`, `0046EFD0` | OWN:511-512, 600-609 |
| `005004C0` (497 B) | effect-subtype switchboard; tail-jump only | not stated | OWN:194, 437-442, 987-997 |
| `00521BB0` (1,757 B) | scratch materializer | not stated | OWN:193, 574 |
| `00433830` (3,202 B) | "shared tessellation helper" | not stated | OWN:195, 272-273 |
| `003697F0` (13 B) | null-safe release → `00369860` (validating deallocator, magic `0xFF12`) | 140 frontier callers | OWN:620-633 |
| `002F31C0` (233 B) | type-tagged retire-and-requeue | 42 frontier callers | OWN:635-646 |
| `0036C140`/`0036C1D0`/`0036C1F0`/`0036B160`/`0036BFE0`/`003697C0`/`0036C110`/`0036C1A0` | scratch-pool queue/dequeue family over `022D89xx`/`022D8Exx`/`022D7FD0` | "~75 resource consumers" / "the seven consumers" | OWN:915-961, 1003-1005 |

#### 1.8.2 Inputs and outputs — record layouts

Save image persistent payload (HUBS:216-219, 331, 606-612):

| offset | width | meaning | cite |
|---|---|---|---|
| base | — | `SaveImage_GetActiveRuntimeBuffer() + 0x200`; buffer static `02164280` | HUBS:331, 611 |
| +0x1044 | i32 | "active or pending field (area) id; negative means none" | HUBS:218 |

Battle unit pool (HUBS:161-162): base `[0208E688]`, count `[0208E6A0]`, stride `0xF50`. Unit `+0x698` = stats record pointer (HUBS:175-177; NBR:140-143); unit `+0xE9A` flag byte, bit 3 suppresses reward processing, `(&5)==5` separate path (NBR:210-215); unit `+0xDCC` zeroed on one path (NBR:159).

Stats record (0x1C8 B, 40 records at `[02EBF190] + 8`) (HUBS:167; NBR:146-147, 332):

| offset | width | meaning | cite |
|---|---|---|---|
| +4 | word (bytes +4/+5) | "whole encoded definition id"; `+5 == 0` party table `02EBF130`; row 0x1A Chocobo | NBR:332; HUBS:171 ("stats record `+4` (u16)") |
| +5 | byte | `== 1` active-battle-unit predicate | NBR:207-214 |
| +0x3C | dword | authored permanent-status word | NBR:332 |
| +0x64 | dword | runtime status word (OR-ed with +0x3C before test) | NBR:136-138, 332 |
| +0x38 | dword | immunity word that can block +0x64 | NBR:332 |

Masks: `1` = KO; `0x80000003` = KO, Stone, X-Zone; `0x8000020` = Confuse, Berserk (NBR:332); `& 0x10` behind `byte[02089340] & 0x20` (NBR:134).

Actor-registry entry / packed handle (HUBS:163-166): entry `+0` ordinal, `+0x15` (4 bits) class, `+0x16` (11 bits) generation, `+0x30` unit pointer; handle = gen<<20 | class<<16 | ordinal. Manager `02098E10 + class × 0x288`: `+0`, `+8` array (count at `[arr]`, entries `[arr+8+i*8]`), `+0x10` bit 0, `+0x20` bound (HUBS:165).

Actor-manager slot `+0x10` byte (NBR:299-326): bit 0 slot live; bit 1 and bit 7 set together by `0026C8C0` (`or 0x82`); bit 7 = start-up unsettled; bits 3,4 cleared (`and 0xE7`); bit 5 holds start-up; `+0x11` bit 0 copy of bit 7, bit 1; `+0x17` bit 7; `+0x20` record count; `+0x28` (0 → field-entry work).

Audio record array (NBR:92-96): 24-byte records at `02AEEDC0`, `+8`/`+0x0A` words = generation; handle at `02AEF3FC`.

Encoded-id resolver `002F9860` (HUBS:555-561): bucket presence table `image+0x2DA3D80`, pointer table `image+0x2E773C0`, record `+0x04` count, `+0x14` encoded pointer; miss → `01C8B638`.

Action timeline record (OWN:500-506): byte `+1` kind (only 2 reaches interpreter); byte `+0x10` entry count; entries 16 B from `+0x14`: byte `+0` opcode 1..128, word `+2` time key, rest opcode-specific; opcode→case byte table `003B994C`, 62-case jump table `003B9854`. Opcode table: action-timeline-opcodes.tsv.

Action context singleton `[02F97348]` (OWN:514-518): `+8` acting unit, `+0x10[i]`/`+0x90[i]` per-target handle arrays, `+0xC` per-target hit mask, `+0x368`/`+0x36A`/`+0x378` flag words, `+0x372` target count, `+0x374` hits delivered. Event kinds: 3→0, 13→1, 26→3/6/7/8 by dword `+4`, 34→2, 37→4, 128→5 (OWN:522-537).

Shared scratch (OWN:169-174, 205-209): `022D9198`–`022D9428` (660 B), `022D8F90`–`022D900E` (130 B), `022D8F30`–`022D8F50` (36 B), `022D9110`–`022D9138` (44 B); `022D9138` RNG enable/mode word (OWN:181-182). Object count disputed (C.1).

Files read/written: none stated (save payload is in-memory image; file format not stated).

#### 1.8.3 State

| global/object | size | initial value | writer(s) | reader(s) | lifetime | cite |
|---|---|---|---|---|---|---|
| save payload `+0x1044` | i32 | not stated | not stated ("What writes `+0x1044` and when is the residue that U-1 covers") | `003148F0` (49 callers) | save state | HUBS:94-98, 295-296 |
| `02164280` active runtime buffer static | not stated | not stated | not stated | `002EF640` | not stated | HUBS:331 |
| `0208E688` / `0208E6A0` pool base / count | not stated | not stated | not stated | `00236820`, `00236850` | not stated | HUBS:161-162 |
| `02089340` bit 4 | bit | cleared by reset | set by `BattleSystem_InitializeAreaState` `002342F0` at `00234339`; cleared by `002341C0` at `002341E4` | `0031B7E0` | battle-system init → reset | HUBS:188-191 |
| `02098E10` slot array (5 × 0x288) | 0x288 each | memset 0 by slot reset `00266D10` | `0026C8C0` (+0x10), pass `0025D9E0` | `00267330`, `003588B0`, `00264790`, `00264770`, `0026AF80` | boot reset → bind on load completion | NBR:301, 326; HUBS:165 |
| `02091098` | dword | not stated | not stated | `00249C60` (mute guard) | not stated | NBR:79 |
| `022CB726` | byte | not stated | not stated | `003603C0` | not stated | NBR:100 |
| `02AEF3FC` / `02AEEDC0` | handle / 24-B records | not stated | not stated | `003A1180` | not stated | NBR:92-93 |
| `01FD36A0` audio manager singleton; `01FD36B4` play-handle counter (31-bit, skips 0) | not stated | not stated | `00212950` | `001DBDB0` | not stated | NBR:283, 290-291 |
| `01F83530` image base B | qword | not stated | not stated | `0020E600`, `0020E620` | not stated | NBR:169-186 |
| `01F82E38`, `0208D45C`, `01E02814`, `02064AD2`, `02064AD3` (frame-mode byte), `01DFE0C0`, `01E02820` (float rate) | — | not stated | `0022AF50` sets `02064AD3`=3, `0022B000` sets 5; `00229E70` stores 1.0 | accessors NBR:229-236 | not stated | NBR:229-236, 243-244 |
| `022C1F48` (bits 0x06), `022C1F40` (qword) | — | not stated | `00307D10` | not stated | not stated | NBR:158-159 |
| `0215F1AC` / `0215F1B4` capability words | dword | not stated | `002E1C40` | not stated | not stated | NBR:455-460 |
| `0215FD98` / `021641F0` | ptr / dword | not stated | `002EACC0` (from `0032F850`, `0032FB70`) | "later readers" | not stated | NBR:469-475 |
| `02F97348` action context | ≥ 0x3AF (not stated as size) | not stated | `0046E990` writes the pointer (OWN:575) | `003B8670` (57 refs), arms | not stated | OWN:514-518, 575 |
| `02EBA4F0` target array, `02EC0F88` | — | not stated | `0046E990` | `003B8670`, `003B8260`, `003B99D0` | not stated | OWN:518, 557, 575 |
| `02EBEF88` / `02EBEF90` sub-object tables (32 × 8-B rows; up to 0x140 slots) | — | not stated | `003A9070`, `003A9790` | family `003A8Cxx` | not stated | OWN:558, 1007-1015 |
| eight `Gi*` factory cache globals `02EAF900`…`02EB3858` | 8 B … 0x90 | not stated | factory's own store only | none ("Nothing reads them") | no release | OWN:319-334 |
| scratch pool `022D89B8`, `022D89BC`, `022D89C0`, `022D89C8`, `022D89D0`, `022D8DD0`, `022D8E10`, `022D8E18`, `022D8E1C`, `022D8E20`, `022D8E28`, `022D7FD0` (0xA8 descriptors, ≤ 0xE), `021B89C0`/`021B89D0`/`021B89A8` | — | not stated | `0036C1A0`, `0036C1F0`, `0036C5D0` | `0036C140`, `0036C110`, `0036B160`, `0036BFE0` | not stated | OWN:915-959, 1003 |

#### 1.8.4 Order

- `BattleSystem_InitializeAreaState` `002342F0` sets `02089340` bit 4 and calls `SpawnKeep_RotatePersistenceBanksForAreaTransition` `00233780`, `SpawnGroup_ResetLifecycleLedger`, `Loot_InitializeWorldPickupPool`, `Navigation_GetWorldBoundsXZ` (`002343B5`), `003924B0` (`0023441E`); teardown `002341C0` clears the bit and calls `Navigation_ClearDataset` (`002341C9`) (HUBS:188-191, 950, 954, 956). Its caller: `ActorSystem_InitializeManagerRuntime` `0026CE60` (HUBS:940). When in the frame: not stated.
- Slot bit-7 lifecycle: boot slot reset `00266D10` zeroes slots → load completion `0032F850` → `0026C8C0` sets bits 1+7 → `ActorManager_RunFieldRuntimePass` `0025D9E0` clears/rewrites bit 7 each pass until no record runs; on the settling pass with `+0x28 == 0`, `WorldTransition_SetOptions` called (NBR:304-326).
- Sound requests refused while slot start-up unsettled (NBR:317-318); sound order: `00249C60` → `003A1180` (→ `00267330`) → `002DF220` → `001DBDB0` → selector → player at manager `+0x08` (NBR:78-101, 283-294).
- Timeline: entry fires once "on the frame the playhead passes it" (OWN:503-505); drivers `0046EFD0` (sub-resource instantiation `00333280`/`003331A0`) and `004FF2C0` (OWN:507-512). Which frame phase calls them: not stated.
- `PartyFollow_SolveFormation` `00338490` is the one Movement site of hub 3 that is both loop-resident and reachable from the per-frame world tick (HUBS:327-329, 358-361); tick walk includes `WorldActorScriptVM_InterpretBytecode` `0025E4C0` (HUBS:372).
- Frame-mode byte `02064AD3`: `0022AF50` → 3, `0022B000` → 5 (NBR:243-244).

#### 1.8.5 Dependencies

Named: Actor/Entity (`../../04-Actor-Entity/battleunit-slot-pool-and-actor-class.md`, HUBS:423; unit-definition page HUBS:177, 192; actor-manager record field map NBR:302); Spawn (`05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md`, HUBS:424); Movement (`06-Movement-And-Navigation/heading-speed-to-position-delta.md`, HUBS:425); Audio (`18-Audio/`, HUBS:426; voice-pack page NBR:86); Script VM storage classes (`01-Script-VM-Native-Bridge/...`, HUBS:331); Resource (`02-Resource-And-Asset-Pipeline/resource-section-addressing.md`, HUBS:470; authored-data-table-registry NBR:329); Status (`10-Status-Periodic-Terminal/...two-layer-effect-model.md`, HUBS:513; the-thirty-two-statuses NBR:332); Combat Action availability (`07-Combat-Action/...`, NBR:329); RNG (`21-RNG-And-Determinism/rng-streams.md`, OWN:182, 372); CRT (`24-Compiler-And-CRT-Runtime/...`, OWN:373); Shared-Transform-Workbench (OWN:161, 314). All outside 00, not audited, except Shared-Transform-Workbench (00).

### 1.9 Developer tuning console: dispatcher, tunables, second table, event slot, names

Pages: `C-CON`, `CON282`, `TUNES`, `CON2`, `EVSLOT`, `CMDNAMES`.


#### 1.9.1 Entry points

| function | role | callers as stated | cite |
|---|---|---|---|
| `001D1660` `DevConsole_DispatchCommand` (13,753 B, body `001D1660`–`001D4C19`) | the dispatcher: one indirect `jmp r9` through a 282-entry RVA table at `001D4C1C`; ids 12–293 | only `001CD040` (tail `jmp`, `001CD049`); "`001D1660` has **zero `E8` call sites in the image**" | C-CON:52-57; CON282:62-77, 145, 221-222, 262 |
| `001CD040` (14 B) adapter | "`test dl,dl / mov r9d,r8d / sete r8b / jmp 001D1660`" | only call site `0017DD34` in `0017DB90` | CON282:146, 262, 505 |
| `0017DB90` Config-screen row handler | 23-way case table; issues 16 literal ids | `0023B3D0` in `0023B330`, `0023B84C` in `0023B6F0` (Config screen row procs) | CON282:203-206, 214-219, 262, 271 |
| `001CD0E0` `DebugMenu_Render` (11,276 B) | row renderer: prints `"%s%s%f"`, label from `[ctx + id*8 + 0x130]`, reads code table at `001CDBF7`, `+0xAAC`, counters `01F832B0` | called by `001D5260`/`001D0190` (CMDNAMES); `001D5520` formats with it (APP, outside group) | C-CON:52, 217-218; TUNES:102, 149; CON2:228; CMDNAMES:38-39, 430; EVSLOT:151 |
| `001C0330` (197 B), `001B3860` (71 B), `001C0480` (181 B) | per-row display-string / value-record materialisers | run by `001CD0E0` | C-CON:341, 356, 360 |
| `003058B0` `Debug_SetGilToMaximum` (10 B) | `mov ecx, 0x5F5E0FF` then `jmp 00254EE0` (`GameState_SetGil`) | "called **once**, from one arm" | CON282:130-139; C-CON:271 |
| helpers `001A9930` (8 B, `*(01F81168)`), `00193D50` (66 B, lazy `0x4A8` at `01F7F5F0`), `001DF340` (10 B indexed dword store), `001DDAB0` (8 B, `*(01F82D18)`), `001C2F40` (8 B, `*(01F81270)`) | singleton getters / store used by arms | call sites 45/33/13/10/9; arms 14/16/15/2/4 | CON282:115-121; C-CON:206-209, 380 |
| `00162410` | static initializer of the `02CB7FD0` object: `lea rcx,block / call 005DC720 / lea rcx,008AB7C0 / jmp atexit` | static init | TUNES:67-74, 540-541 |
| `005DC720` → `005DC580(this)`, `005DC430(this+0xD0)` | block constructor and default setters | `00162410` | TUNES:386-397 |
| `001C7940` (11,445 B), `001C3D50` (4,607 B) | scene-config loaders: `Lookup(name)` → typed read → store | `001C7940` called by `001C7290`/`001C61F0` | TUNES:275-296, 476-480; CON2:213-214, 232-233 |
| `001F0AD0` (2,738 B) | writes 144 addresses (8 shadow matrices + scalars) | only caller `00187950`, inside `"update shadowmap"` scope | TUNES:203-236 |
| `006084B0` (1,419 B) | copies the whole block into the 0x598 snapshot at `00604750`'s `rbp+0x270` | only caller `00604750` | TUNES:192-201; CON282:250 |
| `00604750` | writes the GPU `SceneWideParameterConstantBuffer` field by field from the snapshot | not stated | CON282:250 |
| `0020AC30` (572 B) name-classifying setter `(index, path)` | event-slot names + `sum_`/`spc_`/`0001` flags | via thunk `001EC660` from `0032FD64` in `ActorResource_BeginManagerResourceSetLoad` (`0032FCA0`) | EVSLOT:98-124, 141 |
| `0020AF10` (203 B) event pusher `(index, event_id)` | queues an id into a slot | via thunk `001EC6A0` from `0026B775` (`0026B750`), `00354B6D` (`00354B20`), `00354EDA` (`00354E80`) | EVSLOT:126-142 |
| `001EC560` (59 B) pending probe; `0020AA30`/`0020AA40` flag getters (8 B) via `001EC5C0`/`001EC5E0` (17 B) | consumers | `00180120` (at `00229A53`), `0025DF00` (`0025E0F0`/`0025E100`), `0034CF90`, `0034D790` | EVSLOT:152-157, 185-186, 247-249 |
| `0017D490` `WorldField_GetDebugWeatherSlotOverride` | returns `[singleton + 0xAAC]` | `0025ACA0`, `002620E0`, `00265920`, `0026D910` | CON2:98-109, 230 |
| `001D50D0` (66 B) | console settings singleton getter (`0x10E8` B, cached `01F81428`) | `0017D490`; Config path (slice B, outside group) | CON2:116, 229 |

#### 1.9.2 Inputs and outputs — record layouts

Dispatcher input: `r9d` = id, valid 12–293 after `add r9d, -0xC`; `cmp r9d, 0x119` / `ja` (C-CON:53-54, 106-108; CON282:65-73). Prologue: "`movzx esi, r8b ; arg 3 -> sil`", "`movzx ebx, dl ; arg 2 -> bl (the direction flag)`", "`mov rdi, rcx ; arg 1 -> rdi`" (TUNES:872-874). Signature as adopted: "`(void *ctx, u8 direction, u8, int id)`" (TUNES:888).

Dispatch table (C-CON:66; CON282:75-77, 161):

| offset | width | meaning | cite |
|---|---|---|---|
| `001D4C1C + (id−12)*4` | 4 | image-base-relative RVA of the arm; 282 entries, all inside `001D1660`–`001D4C19`; 227 distinct targets, 56 ids → `001D4BFA` | C-CON:66, 102-103, 117-118 |

Label table: `ctx + id*8 + 0x130`, stride 8, 293 labels for ids 1–294 (C-CON:67; CMDNAMES:38-45). Full id→label→arm→field list ids 12–294 in CMDNAMES:93-377; ids 1–11 labels in CON282:267-269.

Authored-code table at `01DF6E68` (`.data`), stride 16 (C-CON:68-75; CON2:241):

| offset | width | meaning | cite |
|---|---|---|---|
| +0x00 | 8 | `char* codePtr` to "three letters + four digits" or NULL | C-CON:72; CON2:54-67 |
| +0x08 | 4 | `index + 1` for every entry | C-CON:73; CON2:241 |
| +0x0C | 4 | zero in every entry read | C-CON:74 |
| extent | — | 1,314 entries (`01DF6E68`..`01DFC088`), 601 codes | C-CON:77-78; CON2:76, 241 |

Render-settings block `02CB7FD0`..`02CB8438` (1,132 B; part of a larger static object initialised out to `+0x1020`) (TUNES:59-77, 185-195):

| range | meaning | cite |
|---|---|---|
| `+000..+18F` | console-tunable settings, 84 arm-touched addresses | TUNES:186 |
| `+190..+38F` | 8 × 64 B shadow matrices (cascades), written by `001F0AD0` from `object+0x1C0 + n*0xD8` | TUNES:187, 213-217 |
| `+390..+44F` | shadow scalars and counts; `block+0x3E4` = live cascade count | TUNES:188, 258-260 |
| `+450..+470` | copied separately, two arm-touched | TUNES:189 |
| `+0xB4` (`02CB8084`) | last-applied MSAA sample count (copy of `01DF0900`), 0 = off | TUNES:670-691 |
| named offsets (29) | table with names and defaults | TUNES:335-365, 414-442 |
| block → snapshot | block `+X` → snapshot `+0x110+X` (0x598 B); then `00604750` → cbuffer (0x5F0 B) | CON282:250; TUNES:197-201 |
| per-offset cbuffer map | `members/scenewide-cbuffer-map.tsv` | CON282:250 |

Second settings run `01F82ED8`–`01F82F08` (13 named globals; `01F82EE4`, `01F82F04` unnamed) and `01DFE198`/`01DFE19C` (TUNES:455-469).

Event-slot table (EVSLOT:85-94):

| address | width | meaning | cite |
|---|---|---|---|
| `01F832B0` | 5 × dword | per-slot pending-event counter | EVSLOT:87 |
| `01F832C4` | dword | cleared by the pusher each push; incremented by `001EC690` | EVSLOT:88, 302 |
| `01F832C8` | `std::string` 0x20 | "current" name | EVSLOT:89 |
| `01F832E8` | byte | flag A: `sum_` and `0001` | EVSLOT:90 |
| `01F832E9` | byte | flag B: `spc_` and not `sum_` | EVSLOT:91 |
| `01F832F0` | 5 × 0x20 | per-slot name `std::string` | EVSLOT:92 |
| `01F83390` | 5 × 0x20 | per-slot `std::vector<int>` | EVSLOT:93 |
| `01DFE40C` | dword | index marker | EVSLOT:94 |

Files read: `JsonData/CutScenes/<name>.json` (`Common.mDofFocusDistance`, `Common.mDofApertureFnumber`) by `001C5750` for `sum_` names (EVSLOT:37-39, 116-118). Paths validated by regex `(.*)(\\plan_master\\([a-zA-Z]+)\\event\\)(.*)` at `00905958` (EVSLOT:102-104). Scene-config key strings `008FA700`–`008FAB00`, 93 references (TUNES:300-310; CON2:242). Nothing persisted (C-CON:337).

Other object fields: console settings singleton `0x10E8` B: labels `+0x130 + 8×id`, `+0xAAC` `debugWeatherSlotOverride` (s32), `+0xAB4` field id for the code table (CON2:111-118, 249); `+0xC72` id 28 toggle, `+0xC74/+0xC7C/+0xC78` saved floats (CMDNAMES:419); other `rdi+…` fields per id in CMDNAMES:112-376. `PostProcessParamContext` (0x4A8): `+0x110` enable, `+0x114` focus, `+0x118` f-number, `+0x11C`, `+0x120` (35.0) (EVSLOT:219-221); `+0x4A2` = `mUseLinearTonemap == 1` → frame `+0x9A` (CON2:126-143).

#### 1.9.3 State

| global/object | size | initial value | writer(s) | reader(s) | lifetime | cite |
|---|---|---|---|---|---|---|
| block `02CB7FD0` | 1,132 B in an object to `+0x1020` | loader-zeroed, then `005DC720` chain (107 offsets); 27 named defaults listed; 8 offsets stay 0 | constructors; console arms; loaders `001C7940`/`001C3D50`; `001F0AD0`; `001846B0`/`001846F0` (`+168`) | 24 accessors (list TUNES:704) | static ctor `00162410`, `atexit` teardown | TUNES:65-77, 395-397, 414-442, 528-563, 704 |
| `01F7F5F0` `PostProcessParamContext` | 0x4A8 | not stated | `00193D50` lazy ctor; arms (33 call sites/16 arms); `001C7940` (`+0x4A2`); `00194250` | `0018EEE0` | "lazily constructs … on first use"; "deallocated: nothing" | C-CON:91-92, 200-202; CON2:141; EVSLOT:219-221 |
| `01F81300` | same object as `[01F7F5F0]` (`0015CAF0`) | not stated | loaders' settings stores | — | not stated | EVSLOT:219; TUNES:172, 477-479 |
| `01F81428` console settings singleton | 0x10E8 | not stated (ctor `001CCB20` clears labels) | `001D0390` label fill; arms | `001CD0E0`, `0017D490` | built on first use by `001CCB20` | CON2:116-118, 229 |
| `01F81168` map-art context | 0x520 | not stated | — | `001A9930` | not stated | CON282:117, 253-255 |
| `01F82D18` display object | 0x180 | not stated | — | `001DDAB0` | not stated | CON282:120, 258 |
| `01F81270` `MultipleDebugDisplay` | 0x4670 | not stated | — | `001C2F40` | not stated | CON282:121, 260 |
| `01F82D20` `GameSettingConfig` ptr | 31 u32 at `+4×index` | written once at `00798261` by `007980A0` | — | 61 functions | not stated | TUNES:601-613 |
| `01F82EA8` shadow object | 0xB08, count `+0x13C` = 3 | ctor literal 3 | ctor `001EF389` only | `001F0AD0` | singleton, also `01F812C8` | TUNES:268, 568-600 |
| `01DF0900` MSAA word | dword | ships as 4 | `00186CD0` | `00186410`, `00187950` | not stated | TUNES:681-697 |
| event-slot arrays | see I.2 | not stated | `0020AC30`, `0020AF10`, `0020A760`, `001EC680`, `001EC690` | `001CD0E0`, `001D0190`, `001EC560`, flag getters | not stated | EVSLOT:85-94, 299, 302 |
| `01DFE40C` marker | dword | not stated | setter (restores −1), pusher (left set), `001EC680` | `001EC560` | — | EVSLOT:94, 124, 133 |

#### 1.9.4 Order

- Dispatch: one press → `0023B330`/`0023B6F0` → `0017DB90` → `001CD040` → `001D1660` → one arm, then shared epilogue `001D4BFA` (212 of 226 arms jump there) (CON282:203-206, 479-480). Out-of-range enters the epilogue at `001D4C09` (C-CON:109-112).
- "a press takes effect on the next frame" (C-CON:249-250); "meanwhile, every frame: … `00187950` runs the render passes … `001CD0E0` draws the menu" (TUNES:493-496).
- `001F0AD0` "runs once per rendered frame after readiness" via `00187950` ← `0017D090` (GameApplication slot 8), slot 8 run after slot 7 (input), slot 4 (animate), viewports' render (TUNES:620-658).
- Scene load: `001C7940`/`001C3D50` store settings (TUNES:485-487, 518; CON2:253). `+0x4A2` "re-written on every map load that reaches the key" (CON2:271).
- Boot: block static ctor `00162410` (TUNES:67-74); loader zeroing before any constructor (TUNES:542-544).
- Event slots: setter on manager resource-set load; pusher on event-play verbs; readers per actor driver and field-frame gate (EVSLOT:258-273).

#### 1.9.5 Dependencies

- 17-Presentation-Rendering: render command list contract reads `PostProcessParamContext` switches (C-CON:93-98); post-processing contract step 6/7 (CON2:136-139; EVSLOT:221-225).
- 22-Middleware-PhyreEngine: slot 8 cadence, post-process passes (TUNES:627-658; CON282:256-257).
- 16-UI Config screen: the only caller route (CON282:214-219).
- 19-Save-Load-Settings: `GameSettingConfig` (TUNES:607-609).
- 03-World-Area-Field: weather override `+0xAAC` (CON2:111-115); `map_ref.bin` pack census (CON2:77-79).
- 99-Unresolved-Residual cutscene name slots (EVSLOT:46, 275); 18-Audio (`001DBB00`, `002DEBA0`) (C-CON:408-414); Rewards (`00254EE0`) (C-CON:418-428); Battle-Frame (field-frame gates) in 00 (EVSLOT:233).
- Shaders: SceneWideParameterConstantBuffer in `phyrechrshader.fx`/`phyredefaultlitshader.fx` (CON282:250).

### 1.10 Developer tuning console: the arm catalogue (work division and slices A-I)

Pages: `ARMDIV`, `ARM-A`, `ARM-B`, `ARM-C`, `ARM-D`, `ARM-E`, `ARM-F`, `ARM-G`, `ARM-H`, `ARM-I`.


#### 1.10.1 Entry points

| function | role | callers as stated | cite |
|---|---|---|---|
| `001D1660` console dispatch (13,753 B; body `001D1660`–`001D4C19`) | one indirect jump through a 282-entry RVA table at `001D4C1C` to 227 targets | one way in: `001CD040` tail-jumps to it; `001CD040`'s only call site is `0017DD34` in `0017DB90`, called by the Config screen's row procs `0023B3D0`, `0023B84C`; only 16 ids issued (`0x86`, `0xA6`, `0x10A`, `0x110`–`0x119`, `0x11B`–`0x11D`) | ARMDIV:35, ARMDIV:40; ARM-B:43-63; ARM-B:191-197 |
| `001D4C1C` dispatch table | dword RVAs, entry for id n at `001D4C1C + (n − 12) × 4`, + image base `0x00120000` | read by `001D1660` (`001D16A3`) | ARMDIV:161-162; ARM-B:54 |
| `001D4BFA` | do-nothing target of 56 ids **and** common tail of 212 of 226 real arms | all arms | ARMDIV:41; ARMDIV:113-116 |
| `001D4B49` (arm of id 281 "Glare") | three-entry shared epilogue: `4B59` (ids 276, 280), `4B60` (279), `4B65` (134, 166, 274, 275, 277, 278) | jumps from 9 ids in D, E, I | ARM-H:225-236; ARM-I:131-136; ARMDIV:490-493 |
| `001CD0E0` row renderer (`DebugMenu_Render`) | prints each row `"%s%s%f"` with label `[ctx + id×8 + 0x130]`; renderer table 294 entries, base 1 (`lea eax,[r13-1]` / `cmp eax,0x125`) | `001D5260`, `001D0190` | ARM-E:130-140; ARM-E:151-153; ARM-H:274-277 |
| `001D0390` label filler | stores label `char*` per id; 293 non-empty labels ids 1–294 + id 298 | `001CCB20` (`001CCEA4`) | ARMDIV:43; ARM-A:211 |
| `001D50D0` console settings-object getter | returns the `0x10E8`-byte singleton cached at `01F81428` | Input bodies `00197800`/`00197160`/`00197790`; `001FA3D0`, `001BC190`, `00187950`, `001F8D10`, `001D5650` | ARM-A:211; ARM-A:369-371; ARM-F:229-230 |
| `001CCB20` singleton builder | builds object on first use, clears labels (`001CCE6F`), calls `001D0390` (`001CCEA4`); sets defaults (`+0xC58` = 0 at `001CCC9F`, `+0xE30` = 0 at `001CCDDD`, `+0xDDC` = 0x11 at `001CCD7D`, `+0xCF9..CFB` = 1 at `001CCEE0`/`001CCEE9`) | `001D50D0` | ARM-A:211; ARM-F:292-296; ARM-G:180-182; ARM-G:193-194; ARM-G:207 |
| `00162410` → `005DC720` (→ `005DC580`, `005DC430`) | static initializer + ctor of the `02CB7FD0` tuning object; destructor `008AB7C0` via `atexit` | static init | ARM-E:234-245; ARM-E:451-470 |
| `001DF340` | 10-byte property setter `obj->dword[edx] = r8d` | arms of ids 134, 166, 271–281, 284, 285; `007A0C60`, `001DD170` | ARM-I:193-202; ARM-E:289-291; ARM-I:397-400 |
| `001DF2C0` | MSAA gateway (id 277): step mod 5, skip modes whose bit is clear in `cfg+0x44C` | arm 277 | ARM-I:295-297 |
| `001A9930` | 8-byte getter `[01F81168]` (map-art context) | 14 arms / 45 call sites | ARM-D:194; ARM-D:264-265 |
| `00193D50` | lazy getter of the render-parameter block | 16 arms / 33 call sites | ARM-D:195; ARM-B:206-211 |
| `00189120` | 8-byte getter `[01F7F598]` (0xDD8 render object) | id 103 (`001D2B15`), "117-caller hub" | ARM-C:145; ARM-C:236-238 |
| `001C2F40` | 8-byte getter `[01F81270]` `MultipleDebugDisplay` (0x4670) | ids 51, 218, 219 | ARM-G:222-224; ARM-B:212 |
| `001DBB00(category, byte)` | sound-category mute | ids 205–207 | ARM-G:203-207 |
| `003058B0` / `00305A00` / `00305960` + `003058C0` | set gil / LP / level to max | ids 199 / 200 / 201 | ARM-F:132-134 |
| `002DEBA0` / `002DF2A0` | get/set `0215EFD0` (3D Sound Behind Ratio) | id 217 | ARM-G:214-216 |
| `0017E7A0` | step `01DF0010` (Extra BGM status) | id 220 | ARM-G:217 |
| `002FBA40` / `002FBA50` | get/set `022BE950` Print Magic Info | id 183 | ARM-F:318 |
| `001B1C00`/`001B0F90` get, `001B1FF0` set; `002B6650`…`002B66C0` | track-map placement accessors | ids 189–193 | ARM-F:301-306 |
| `0032E010` / `0032E030` | integer get/set | id 267 | ARM-H:180-181 |
| `00182DE0` / `00182E10` | window-mode / resolution push | ids 263, 264 | ARM-H:189-191 |

#### 1.10.2 Inputs and outputs

**Dispatcher arguments** (ARM-B:46-62; ARM-F:219): `rcx` → `rdi` settings object; `dl` → `bl` arg 2; `r8b` → `sil` arg 3. `001CD040` sets `r8b = (dl == 0)` (ARM-B:193). Id bound `add r9d,-0xC` / `cmp r9d,0x119` / `ja 0x1D4C09` (ARM-B:47-52).

**Console settings object** (`0x10E8` B, cached `01F81428`; ARM-A:211), fields stated:

| offset | width | meaning (id) | cite |
|---|---|---|---|
| +0x130 + 8·id | ptr | label per row | ARM-E:298 |
| +0xA68 | b | initialised | ARM-E:299 |
| +0xA6C | d | cursor row | ARM-E:300 |
| +0xA80 | ptr | object id 166 calls virtually (`+0x60` slot) | ARM-E:301; ARM-E:280-284 |
| +0xA88 | d | page index (page·22 + row) | ARM-E:302; ARM-E:315-317 |
| +0xAA8 | d | Load ps2 savedata from slot (15), wraps mod 200 | ARM-A:84; ARM-A:265 |
| +0xAB8 | — | Change cast shadow object (24) | ARM-A:93; ARM-A:270 |
| +0xABC/+0xABD/+0xABE | b | Enable Map/Character/UI Display (34, 35, 37) | ARM-A:276 |
| +0xAC0 | d | Enable VFX Display (38), mod 3 | ARM-A:107; ARM-A:277 |
| +0xAC4 | b | Enable Shadow Display (40) | ARM-A:278 |
| +0xAC6 | b | Show Map Hide Group (176) | ARM-F:263 |
| +0xAC8/+0xACC/+0xAD0 | d | Particle Draw Type Range cursor/cursor/count (177, 178) | ARM-F:110-111; ARM-F:171-172 |
| +0xAD4/+0xAD8/+0xADC | d | Map render DisplayList Id range (180, 181) | ARM-F:113-114 |
| +0xAE0 | d | Fusion Technique Select (182), clamp [0,8] | ARM-F:115 |
| +0xC04 / +0xC08 | d | HBAO NumSteps (43) bounds 2,0x13 / id 44 same bounds | ARM-A:112; ARM-B:72 |
| +0xC0C | b | Camera Over Write flag (103); also listed by id 60 | ARM-C:91; ARM-B:88 |
| +0xC10/+0xC14/+0xC18 | f32 | FOV / Aspect Ratio / Camera scale (104–106) | ARM-C:92-94 |
| +0xC20 | d | Invincible (14), wraps 3; read by `0017D470` | ARM-A:83; ARM-A:232 |
| +0xC28 | d | id 60 | ARM-B:88 |
| +0xC2C | d | Display texture density (32) | ARM-A:101; ARM-A:274 |
| +0xC34/+0xC35 | b | Huge Damage (185) / Enable mouse control camera (187) | ARM-F:118-120; ARM-F:267-268 |
| +0xC38 | d | Camera speed (186), mod 4 | ARM-F:119 |
| +0xC3C/+0xC3D/+0xC3E | b | key-mapping-from-file (188) / Japanese keyboard (293) / File Cache Enable (202) | ARM-F:121,135; ARM-I:179 |
| +0xC40/+0xC44/+0xC48 | d | Load chr (20) / Variation (21) / CLUT (22) | ARM-A:267-269 |
| +0xC58 | d | step selector for 190–193; always 0 | ARM-F:180-190; ARM-F:291-296 |
| +0xC70 | b | 100% Spawn Rare Monster (197) | ARM-F:130 |
| +0xC71 | b | Use normal map (29) | ARM-A:98 |
| +0xC72 + save area +0xC74…+0xC98 | b + 12 | Use PS2 lighting (28) | ARM-A:97; ARM-A:136-142 |
| +0xCEC/+0xCED/+0xCEE | b | set gil/LP/level toggles (199–201) | ARM-F:132-134 |
| +0xCF0 | b | Switch diffuse texture (33) | ARM-A:102 |
| +0xCF4 | f32 | Debug high model skeleton (26) | ARM-A:95; ARM-A:235 |
| +0xCF9/+0xCFA/+0xCFB | b | Music / Voice / Sound Effect mutes (205–207) | ARM-G:68-70; ARM-G:202-207 |
| +0xD07 | b | id 208 | ARM-G:71 |
| +0xD08 | d | id 54 | ARM-B:82 |
| +0xD78 | d | Yebis enable (175), 3 states | ARM-F:108; ARM-F:274 |
| +0xD90 | d | Procedural texture rotation ratio (196) | ARM-F:129 |
| +0xDA0 | d | Load sample chr (19), cap 0x12 | ARM-A:88 |
| +0xDB4 / +0xDB8..+0xDD4 / +0xDD8 | d | id 225 value / 8 digits / cursor | ARM-G:78; ARM-G:115 |
| +0xDDC | d | constructor sets 17; no reader | ARM-G:192-200 |
| +0xDE0 / +0xDE4..+0xE00 / +0xE04 | d | id 226 | ARM-G:79; ARM-G:117 |
| +0xE0C / +0xE14 (/+0xE18 per ARMDIV) | d | id 227 value / sub-field selector (/ hours modulus) | ARM-G:80; ARMDIV:533-535 |
| +0xE1C/+0xE1D/+0xE1E | b | ids 228–230 | ARM-G:81-83 |
| +0xE2C / +0xE30 | d / b | Set scenario flag index (231) mod 311 / coarse-fine flag (always 0) | ARM-G:84; ARM-G:180-187 |
| +0xE34..+0xE58 | d pairs stride 8 | five counters + modifier flags (238–242) | ARM-H:247-251 |
| +0xE5C/+0xE60/+0xE64 | d | steal/poach/drop success state (243–245) | ARM-H:252-254 |
| +0xE68 | d | stat array stride 12 (ids 247–258) | ARM-E:304 |
| +0x10A8 | d | selected character | ARM-E:305 |
| +0x10B8 | f32 | Master Volume Ratio (260) | ARM-H:255 |
| +0x10BC | d | window mode mirror (263) | ARM-H:256 |
| +0x10C4 | d | mirror — **id 267 per ARM-H:257, id 268 per ARM-I:154** (C.1) | |
| +0x10CC/+0x10D0/+0x10D4 | d | mirrors 269, 270; id 288 counter | ARM-I:155-156,174 |
| +0x10D9 | b | After Water fix enable (62) | ARM-B:217 |
| +0x10DC / +0x10E0 | d / b | ids 291 (mod 4) / 292 | ARM-I:177-178 |

**`02CB7FD0` tuning object** (static C++ object; ARM-E:243): fields +0x000…+0x070 for ids 140–164 with shipped defaults (ARM-E:86-110); +0x074…+0x090 water (slice D, ARM-E:311); +0x0D0 sub-object `chrFresnelSpecular*` (ARM-E:312); +0x464 SSS enable byte = 1, +0x468 SSS Width = 7.0 (ARM-E:113-114); arrays `02CB80A0`–`02CB812C` (ids 63–98, ARM-C:115-116), `02CB8130/34/38` (ids 108–110, ARM-D:74-76), `02CB8140` (107), `02CB8144` (113), `02CB8148`/`02CB8150` (ids 30, 31), `02CB7FE8`–`02CB7FF4` (136–139), `02CB8044`–`02CB8060` (120–126, 135), `02CB806C` (119).

**`01F82D20` `GameSettingConfig`** (`0x65C` B, 31 dword slots, property n = dword n; ARM-I:188; ARM-I:193-202): property → id map ARM-I:212-226; `+0x08` window mode (263/264, ARM-H:189-190); `+0x40` WaterQuality (134, ARM-D:339-344); `+0x38` property 14 (166, ARM-E:427-429). Defaults table `00900CE0` 31 × 4 presets, column 0 (ARM-D:352-356).

**Map-art context `[01F81168]`** (0x520 B; ARM-D:264-266): `+0x2C0`…`+0x448` fields with keys and readers (ARM-D:277-311), `+0x2E4` EnableIBL byte, `+0x2E5`, `+0x2F8` WaterQuality copy (ARM-D:318-335).

**Render object `[01F7F598]`** (0xDD8): `+0xC0C` camera-override switch, `+0xCC4/CC8/CCC` FOV/aspect/scale (ARM-C:241); `+0xDBA`, `+0xDC8`, dirty byte `+1` (ARM-I:303-305).

**Other tables read:** `01DFC0D0` 311 scenario values (ARM-G:185-187); `01DFD150` 31×9 value-label table (ARM-I:210); `00900EE8` = {1,2,4,8,9} (ARM-I:304); `01DF0018` BGM labels (ARM-G:218). Files: JSON sidecar `JsonData/CutScenes/<scene>` re-parsed via id 12 (ARM-A:301).

#### 1.10.3 State

| global/object | size | initial value | writer(s) | reader(s) | lifetime | cite |
|---|---|---|---|---|---|---|
| `01F81428` → console object | 0x10E8 | built on first use | `001CCB20` | `001D50D0`, `001D1660`, `001CD0E0` | first use; destroy not stated | ARM-A:211 |
| `02CB7FD0` tuning object | ≥ +0x1020 per ARM-E:466-467 | ctor defaults (ARM-E:86-117) | `005DC720`/`005DC580`/`005DC430`; console arms | arms, renderer | static init `00162410`, `atexit` destructor `008AB7C0` | ARM-E:234-241 |
| `01F82D20` → GameSettingConfig | ≥ 0x65C | `00900CE0` col 0; `+0x44C` = 1, `+0x658` = 0x101 | `007980A0` (store `00798261`), `001DF340` | 156 reads | built by `007980A0`; destroy not stated | ARM-D:339-356; ARM-I:188-191 |
| `01F81168` map-art context | 0x520 | ctor `001A2130` (`+0x2F8` = 2 then WaterQuality; `+0x2E4` word 0x101) | `001A98B0` | `001A9930` | rebuilt → WaterQuality re-copied (only then) | ARM-D:264-266; ARM-D:324-335 |
| `01F7F598` render object | 0xDD8 | ctor `00184F20` | `00189000` | `00189120` | not stated | ARM-C:241 |
| `01F81270` MultipleDebugDisplay | 0x4670 | not stated | not stated | `001C2F40` | not stated | ARM-G:222-224 |
| `01DF6E48` Read Json Data | byte | 1 in image | id 12 | `001C5930`, `001C5F20`, `001C61F0`, `001C6C00` | image | ARM-A:295; ARM-A:301 |
| `02CB8148` / `02CB8150` | byte / dword | — / 0 at load | ids 30 / 31 | `001E2AF0` | — | ARM-A:298-300 |
| `01DFE191` Fresnel Reflection enable | byte | 1 | id 99, `001A5B30` | `001F8D10`, renderer | image | ARM-C:244-256 |
| `01DFE192` Camera Light enable | byte | not stated | id 61 | not stated | | ARM-B:216 |
| `01DFE1AC` SSS Diffuse a | f32 | 1.0 (image) | id 169 | none found | image | ARM-E:262-264 |
| `01F82EE4` SSS Diffuse b | f32 | unknown | id 170 | — | zero-filled tail | ARM-E:116; ARM-E:350-352 |
| `01F82ED0` | f32 | not stated | id 112 | — | | ARM-D:78 |
| `01E02801` FrameSkip Enabled | byte | 1 | id 287 | `001E05F0` | image | ARM-I:308-315 |
| `022BE950` Print Magic Info | dword | not stated | `002FBA50` | `002FC4A0`, renderer | | ARM-F:318-320 |
| `01E0CE50..5C` track-map floats | f32 ×4 | 0.67, 0.6, 1.0, 21.0 | ids 190–193 | `002B6B50`, `002B7B80`, `002B8EE0` | image | ARM-F:302-310 |
| `0215EFD0` 3D Sound Behind Ratio | f32 | 0.3 (`002DE360`) | id 217 | world tick `0031431A`/`00314324`, `00363109`, renderer | | ARM-G:214-216 |
| `01DF0010` Extra BGM status | dword | 1 (image) | `0017E7A0` | `0017E490` | | ARM-G:217-221 |
| `01F7F4E8` | byte | not stated | "no RIP-relative writer" | `0017E490` | | ARM-G:219-221 |

#### 1.10.4 Order

- Boot: `00162410` static init → `005DC720` writes every default of `02CB7FD0` (ARM-E:324); console object built on first `001D50D0` call (ARM-A:211). Frame placement of the console call is **not stated** beyond the Config-screen row procs (ARM-B:191-196).
- Per press: dispatcher → table → arm → `jmp 001D4BFA` (or into `001D4B49` interiors) (ARM-A:190-195; ARM-H:225-236). Renderer draws each row independently (ARM-E:322-323).
- Id 103 OFF edge re-seeds +0xC10..C18 from the render object (ARM-C:140-143). Id 264 acts only when window mode ≤ 1 (ARM-H:167-169). Id 28 ON edge saves/zeroes, OFF restores (ARM-A:126-134).
- Map-art context copies WaterQuality once at construction (ARM-D:333-335). Scene load writes config keys (ARM-E:325).

#### 1.10.5 Dependencies

Audio (`002DEBA0`, `001DBB00`, `00210B30`/`002112D0`, 18-Audio driver page; ARM-G:205-210), Resource (`002EEEE0`; ARM-A:366), Presentation (materializers `001D5120`/`001C7360`/`001C7520`; ARM-A:364-365), 19-Save-Load-Settings Game-Settings-Config (ARM-I:186-189; ARM-D:330-343), 08-Combat-Formula Steal (`FK-3`; ARM-A:211), 16-UI Map-Screens (ARM-F:310), 22-Middleware-PhyreEngine Post-Process-Chain (ARM-A:233; ARM-D:314), 99-Unresolved-Residual cutscene slots (ARM-A:301), Economy `GameState_SetGil` `00254EE0` (ARM-F:234), combat target eligibility `0030B7F0` (ARM-A:283-285), Application-Root (`game-application.md`; ARM-C:238; ARM-G:223). All marked outside 00 except Application-Root.

## 2. Gaps

### 2.1 Gaps the pages state themselves (still open, live-only, or declared limits)

Only gaps that no later dated line on the 00 pages answers are listed. A gap that a later line answers is a stale
claim and is in §3.2.

#### 2.1.1 Boot fixups, startup data construction and the application root

| id| quote + cite | why a port needs it |
|---|---|---|
| G-1 (RC-3 residue) | "*Not claimed:* why the 0.5 MiB block is allocated." (BOOT:178-179) | harmless to replicate, but sizing budget |
| G-2 (RC-2 residue) | "*Not claimed:* why the sizing adds those bytes." (BOOT:306-307) | allocation sizes must match |
| G-3 (pacer tick) | "what one pacer tick is in wall time is not claimed here" (BOOT:389-390) | frame timing |
| G-4 (pool contents) | "what each pool holds is not claimed here" (BOOT:230) | memory map |
| G-5 (boot window) | "**How long the startup window is** in which the time base is still `1` … `PROBABLE`, unmeasured" (C-BOOT:498-499) | boot order of time base |
| G-6 (reachability) | "no execution of boot's own reachability" (C-BOOT:490-492) | evidence only |
| G-7 (I1/I4 ruling) | "`I1` and `I4` await theirs" (C-BOOT:441) | evidence only |
| G-8 (arena 10 limit) | "*Limit:* a call through a pointer assembled at run time would not be seen." (BOOT:189-190) | arena completeness |
| G-9 (predicate consumers) | "**What consumes those predicates** is read out for one of them" (C-BOOT:310-312) | half-rate behaviour |
| G-10 (0x4A top byte) | "no individual consumer of a `02EAF930` row is named here" (FLOAT:592-593) | packet use |
| G-11 (`008631D0` bytes) | "NOT claimed: byte `+1`/`+2` are never written by this helper" (FLOAT:651-652) | header layout |
| G-12 (pointer pair) | "what the pair is *named* (a pointer position is the shape) is not established" (APP:287) | input mapping |
| G-13 (`0018A7D0` / `001EBA40`) | "What `0018A7D0`'s pair gates, and which subsystem `001EBA40` belongs to, the bodies do not name." (APP:700-701) | pause side-effects |
| G-14 (`01F81240` name) | "the name stays unclaimed" (APP:673) | — (role known) |
| G-15 (7 class names) | "none is claimed" (APP:315, 585) | naming only |
| G-16 (`01F7F598` fields) | "**no meaning is claimed for any of the 24 rows** … The remaining 224 bytes stay declared gaps" (APP:1086-1089); array extents "explicitly not established" (APP:1080-1081) | renderer object layout |
| G-17 (FrameMarker gap) | "`+0x2C38` \| 512 bytes, **not touched by any of the eight tied bodies**" (APP:1387) | layout |
| G-18 (`0061D490`) | "`0061D490` is not stated here (1,211 B, several paths)" (APP:2404) | device path |
| G-19 (quad records) | "What the four `0x30` records *are* … is upstream of this subtree" (APP:852-853) | screen setup |
| G-20 (log sink) | "NOT claimed: which class implements the sink" (APP:903) | diagnostics |
| G-21 (texture-resize callers) | "Callers outside these selected paths are not covered." (APP:1474) | robustness |

#### 2.1.2 World tick, field frame and force-fight mode

| id| quote + cite | why a port needs it |
|---|---|---|
| G-22 (EX-8 residual) | "**Residual:** the identity of the pools at `02EBB6F0`, `02EBEC00` and `02B58960`, and of message kind 2." (TICK:810-811); `02EBEC00` record laid out but "**What this does NOT do is name the subsystem.**" (TICK:837) | skip-begin notifications act on these pools |
| G-23 (EX-3 residual) | "Residual: the identities of the record tables `0215F200` and `02B59D80`." (TICK:903-904) | tail drains/pushes over them |
| G-24 (orchestrator helpers) | "Not established: which of the 23 steps `0030CBE0`/`0030CE10` implement, and the `00D103B0` table's case↔step mapping." (TICK:527-528) | step 11 behaviour |
| G-25 (step 11 / 16 / 23) | "`0030CBE0`, `003065D0` \| CombatAction, unread" (TICK:223); "`00304440` \| unread" (TICK:228); "`002F82F0` \| unread" (TICK:235) | per-frame field steps |
| G-26 (tail unread) | "Then the fixed list, cited by address because most are unread" (TICK:150-151) | tail callees order known, behaviour partly |
| G-27 (`003DF760` loop) | "`003DF760(0, n, 0, 0, 0)  for n = 1, 2, 3, 4, 5 … unread`" (TICK:100) (later answered TICK:901-903, but with contradicting addresses, see C.1) | — |
| G-28 (0x0B/0x17/0x18 wording) | "**The on-screen wording of the three screens is not read**" (TICK:861) | UI only |
| G-29 (`001800E0` byte) | "which command sets the byte is not matched" (TICK:926) | when mode 2 skips the tick |
| G-30 (FZ-11) | "what the nibble means is FZ-11" (TICK:343) | bit 13 semantics |
| G-31 (nav grid) | "Not established: whether initialisation can run twice without an unload between … and whether the 0x400 bytes are one 128-entry table" (TICK:706) | grid lifetime |
| G-32 (reset battery) | "teardown vs re-init is not named by the bytes" (TICK:637) | `00253A30` semantics |
| G-33 (`001EDDA0` globals) | "NOT claimed: which subsystem owns either global" (TICK:1547) | — |
| G-34 (slots 3/4 identity) | "*Which actor managers slots 3 and 4 hold is not established here.*" (C-TICK:108) | what a menu frame advances |
| G-35 (`00265680` meaning) | "(its meaning is not named on this page)" (C-TICK:316) | pump gate |
| G-36 (callees not described) | "*Their addresses are deliberately not cited*" / "nothing about any callee" (C-TICK:263-265) | contract asserts order only |
| G-37 (AN-4 residue) | "*Not read:* the identity of the `0208E6A4` handle and what `0031ADB0` does with the answer." (FORCE:198) | combo continuation |
| G-38 (fleeing effects) | "What fleeing changes beyond the label — enemy pursuit, command availability — is the consumer census below, not that observation." (FORCE:50-51) | gameplay effect of R2 |
| G-39 (`00248220`) | "NOT claimed: what `00248220` does for the absent case" (FORCE:365) | save path |
| G-40 (EX-9 residue) | "What remains unobserved (the native effects of the two callbacks on a live area change)" (TICK:956) | init/unload effects |
| G-41 (`00362E30` null path) | "whatever `eax` held when it does not - the null path leaves the register unset" (TICK:2590) | undefined return |

#### 2.1.3 Per-frame update gate and system stop registry

| id| quote + cite | why a port needs it |
|---|---|---|
| G-42 (G-bit4) | "**`0x10` is not among them**" … "NO ADMISSIBLE SOURCE" (GATE:227-232); C-GATE:284-294 closed as "provably dead" | Harmless: the bit has no behaviour. Closed. |
| G-43 (G-hole-write) | "**What genuinely remains is narrower than a subsystem hand-out: an INDIRECT call.**" (C-GATE:1146) | Bounded. The 23,224-byte hole needs only zero-init. |
| G-44 (G-57E0) | "**What indexes `ManagerSub0209BE80_57E0 + 0xD0` with stride `0xD0`?**" (C-GATE:1014); "the 8,728 bytes stay unobserved" (C-GATE:1000); partly answered by `b2e83fb7a` (C-GATE:1225-1227) | `_57E0` layout for the 0x0020/0x0400 groups |
| G-45 (G-AB38) | "**This is extent, not meaning.** … the 1,800 bytes stay unexplained" (C-GATE:564-565) | battle-menu / 0x720 widget interior |
| G-46 (G-8FA0) | "**So the first 4,144 bytes of this child are untouched by its own owner family.**" (C-GATE:595) | `_8FA0` layout |
| G-47 (G-callshape) | "the four call-shape groups name their callees but not what those compute" (GATE:254: 0x0008, 0x0100, 0x2000, 0x8000) | Four of the 16 groups have no behaviour described |
| G-48 (G-node-0D40) | "`node +0x0D40   f32`" (GATE:192) with no meaning; `+0xD78/+0xD7C` unnamed (C-GATE:1594) | Node layout completeness |
| G-49 (G-282) | "What `+0x282 = 0x100` shows on screen is not read here." (GATE:551) | Libra display |
| G-50 (G-10FA0) | "*Nothing in the sweep reads it back; the reader must reach it another way*" (GATE:496) | intervention-menu tutorial mode |
| G-51 (G-subobj) | "*Not covered: the three sub-object rows of the same request (`+0x24` of the `+0x7EA0` sub-object, `+0x974` of `+0xA0D0`, `+0xC8` of `+0x57E0`).*" (GATE:503-504) | mailbox completeness |
| G-52 (G-reg-consumer) | "the registry's consumers are unread (its owner is the object `001B1580` builds…)" (GATE:318-319) | only matters if the enable word is ever made writable |
| G-53 (G-live) | "| any runtime observation | **none exists** |" (GATE:269); "Not established, and it cannot be observed without modifying the word" (C-GATE:185) | parity |
| G-54 (G-slot-tail) | "The remaining bytes — `+0x08` qword and `+0x15`–`+0x17` — are still unobserved." (C-STOP:243-244) | record layout (the tsv contradicts it for +0x08) |
| G-55 (G-fade0) | "*Not read here:* whether a 0-length fade behaves differently from none for the consumer of the combined value." (C-STOP:116) | first-apply behaviour |
| G-56 (G-cancel-dispatch) | "the id dispatch at `00225E44`–`00225E5F` is not tabulated here" (STOP:84); "the page does not tabulate the cancel's id dispatch either" (C-STOP:285-286). EXP-191 tabulates it for `00225EB0` only (C-STOP:213-214) | cancel side effects per id |
| G-57 (G-sets67) | "`00226A50` / `00226AB0` … and `00263560` also reach sets 6 and 7's hooks … their bodies are not read here." (STOP:207-208). Later measured (STOP:743-764), but `00263560` is still unread | single-actor stop |
| G-58 (G-ch11) | "What channel 11 carries and what the other flag bits of `+0x10` / `+0x11` mean are open." (STOP:293) | set 4 effect |
| G-59 (G-bit24) | "*What I did not read.* `00423B10` in full …; `003E7D10` …; and the **consumers** of either field." (STOP:457). Partly superseded by the SM-2 answer (STOP:294) | set 3 effect |
| G-60 (G-19bit4) | "`+0x19` bit `0x04` bypasses the mark-only arm; its meaning is not inferred." / "**Open.** The producer of `+0x19` bit `0x04`…" (C-GATE:422, 427) | name-binding drain |
| G-61 (G-SS7) | "**SS-7 partial**: … the per-request reach bit was not isolated" (C-STOP:215-216) | manager breadth |

#### 2.1.4 Battle runtime mode ladder, diagnostics log, duplicated names, all-ones convention

| id| quote + cite | why a port needs it |
|---|---|---|
| G-62 (G1-dist) | MODE:431-432 "none read here, so *what the distance is compared against is not stated*" | `00309A90`'s 3.8/2.2/24.0 is useless without the comparison it feeds |
| G-63 (G1-resslot) | MODE:424-425 "`0032F6E0` / `0032F6C0` / `0032ED70` / `002671F0` are a resource-slot family indexed with 3, not read further here" | the special-sequence states 2/3/6 gate on them |
| G-64 (G1-chanunit) | MODE:549-550 "The channel's unit is the countdown API's … not converted here" | ride/turbo timings in seconds |
| G-65 (G1-asset) | MODE:568-569 "Which authored asset row 3 names is that resource's matter, not this page's." | dismount presentation |
| G-66 (G1-rmd1) | C-MODE:418-420 "**Residual:** … which specific visible outcome each drives … is inferred from the map's role, not observed per-site." | modes 4 vs 5 behaviour in play |
| G-67 (G1-thread) | C-MODE:472-476 "a thread-entry-point census against the 20 ladder call sites was not enumerated" | null-pointer safety on threads |
| G-68 (G1-284) | C-MODE:502 "*Not claimed:* what `[record + 0x284]` is." | dismount hand-off gate |
| G-69 (G1-live) | C-MODE:373-375 "**One attach answers all three, and none has been performed.**" | live confirmation of bits 1/2/3 and 180.0f |
| G-70 (G1-consumers) | C-MODE:339-341 "the 21 consumers, and every live-only item … EXP-098 discloses the mode setters as not exercised"; C-MODE:588-589 "`INTEGRATION`, because the ladder's meaning is entirely in its consumers" | the ladder's behaviour is its consumers |
| G-71 (G1-chan) | LOG:179-180 "*Limit, not a question:* the developers' names for the channels are not in the image." | none (no behaviour) |
| G-72 (G1-thunks) | DUP:185-188 "**Why some functions have thunks and others do not.** … **How many of the 692 differently-named thunks are load-bearing**" | caller censuses / hook placement |
| G-73 (G1-ptrs) | DUP:367-369 "Whether the 384 pointer references are vtable slots, jump tables or something else: the **sections** were measured, the structures were not. The 17 double-edgeless cases were sampled at six" | identifying stored-pointer dispatch |
| G-74 (G1-gaprepro) | DUP:361-364 "a census offered as re-runnable should be re-runnable, and this one is not, from anything in the repository." | none (meta) |
| G-75 (G1-ff) | ONES:134-135 "**Whether every `0xFF` byte store in §4's 169 is a sentinel.** Certainly not" | per-field empty values |
| G-76 (G1-zero) | ONES:327-329 "**80 candidates is not a finding that `0` is used as an empty marker**; none has been adjudicated" | per-field empty values |
| G-77 (G1-412) | ONES:371-372 "`+0x412`'s behaviour is read, its subject is not." | the countdown's owner record |

#### 2.1.5 Encoded-id space, class registry, query record, basis helpers, ABI recovery

| id| quote + cite | why a port needs it |
|---|---|---|
| G-78 (OV-5 / OV-8 residue) | "**OV-8.** Actual game reachability of the deliberately abnormal counts/pointers/state layouts." (QREC:196); residue: "'Zero for the process life' is **supported, not proven**." (C-EID:294-295) | whether `0020E600` must model a nonzero / ≥4 GiB base |
| G-79 (string lifetime) | "Their lifetime across resource unload/rebinding, and shared-record thread/reentrancy constraints, remain separate unanswered obligations." (QREC:79-81); ruled a declared limit (C-EID:248) | menu code holding returned name pointers across reloads |
| G-80 (reentrancy) | "Concurrent/reentrant safety remains unestablished." (C-EID:113) | static record aliasing |
| G-81 (OV-1 output meaning) | "per-slot downstream semantics … ruled a declared limit" (C-EID:247); "not assertions that every field's downstream purpose is understood" (QREC:87-88) | consumers of +0x28…+0x60 |
| G-82 (row layouts) | "the residue of 60 unmapped bytes in 8 tables … The four class slots that are not pack entries (`02EBF150`, `02EBF120`, `02EBF0D8`, `02EBF0D0`) are named there and not measured." (CLS:291-296) | table rows feed the filler |
| G-83 (02EBF020 groups) | "what the two ids select is open … Which script situations select each group is not read." (EID:441) | command list presets |
| G-84 (key items order) | "a player-facing check that the Key Items tab lists maps first is not made here" (EID:275) | UI ordering |
| G-85 (other languages) | "Only the `us` pack was decoded; other language packs are not checked here." (CLS:376); "Other language packs are not checked." (CLS:540) | — (EID:71 says identical) |
| G-86 (census limits) | "a record pointer handed to another function is not followed … a read through a saved stack copy would be missed" (EID:221-223); C-EID:314-316 residual | absent-reader claims |
| G-87 (BASIS purpose) | "**What this document does not claim:** what the structure is, what `A`, `B`, `C` and `T` mean, who calls either function, or what the two parameters of `0062DFB0` represent." (BASIS:112-113) | whole helper pair has no semantic contract |
| G-88 (ABI types) | "the residue - the 511 untyped position-1 rows" / "The class-derivation residue is the 151 pointers plus the 16 undecided." (ABI:192-193); "the caller route is still the next step" (ABI:191) | argument types for 562 rows |
| G-89 (ABI floors) | "Twenty-nine rows have at least one frame-relative read the tracker could not place … their result is itself a floor" (ABI:125); "a function whose every register position is dead is invisible to this test too" (ABI:166-167) | arity may be under-reported |

#### 2.1.6 Shared transform workbench (EE/VU0 register bank, save/restore, primitives)

| id| quote + cite | why a port needs it |
|---|---|---|
| G-90 (UQ-36) | EEVU:226 "*OUT OF EVIDENCE BOUNDARY 2026-09-27 … answerable only from the PS2 executable `SLPM_667.50`*" | row index → vf name; not needed if the port keeps addresses |
| G-91 (UQ-38) | EEVU:259 "Closed for the gate, unanswered in fact." | whether each member maps to a library routine or inline code |
| G-92 (UQ-39) | EEVU:265-267 "The residue stays unanswered in fact." | identity of templates |
| G-93 (022D9470 flags) | EEVU:252 "Which VU flags they are cannot be recovered here" | none (write-only) |
| G-94 (target alias) | SAVE:97 "Whether any caller passes such a target is not established." | Save/Restore edge behaviour |
| G-95 (row byte 1) | SAVE:292 "Which value the nine callers leave in byte 1 of the operand row `022D8F10` is not read here" | modulate ceiling |
| G-96 (row meaning) | SAVE:294 "what each caller's row operand represents is named only by its position" | modulate inputs |
| G-97 (indirect nesting) | SAVE:296 "an indirect call from one of them into another of the nine would not appear"; C-SAVE:319-320 "Requested from ASTRA; not claimed here." | depth-of-one safety |
| G-98 (BSS interleave) | C-SAVE:359-360 "safe only while that record's `+0x28`+ tail stays unused; whether it does is unenumerated." | memory layout of save values |
| G-99 (`02AEEA20` rows) | PRIM:342-344 "`02AEEA20`'s upper three rows have **no RIP-relative writer** in the image" | matrix source contents |
| G-100 (projection divide) | PRIM:151-152 "the divide happens somewhere else, in code this page has not read." | render path |
| G-101 (`0039B550` mode dword) | PRIM:650 "NOT claimed: `0039B550`'s published mode dword's semantics." | installer side effects |
| G-102 (`005002E0`/`0039A9B0`) | WB:638-639 "NOT claimed: which semantic pass drives `005002E0`'s two range windows, or which table owns the `022D8F30` min/max pairs" | predicate semantics |
| G-103 (record types) | PRIM:470-473 "the record types are not named … `003F3E40`'s jump table … not opened" | residual consumers |
| G-104 (bank residence) | PRIM:686-688 "NOT claimed: the physical meaning of the `023393xx`/`03B0E7Fx`/`01EA47xx` banks" | other banks |
| G-105 (title-screen routine) | C-PRIM:298-299 "which routine holds them *at the title screen specifically* is not runtime-confirmed" | none (live only) |
| G-106 (runtime) | C-PRIM:329 "any runtime observation of either function EXECUTING … UNKNOWN"; C-SAVE:388; C-SAVE:205 "Not established." | validation |
| G-107 (mutation) | C-PRIM:215 "Verdict `FAIL_INCOMPLETE`." | test adequacy |
| G-108 (float order) | PRIM:807 "Other MXCSR settings, subnormals and NaNs are not read" | bit-exact compose |
| G-109 (`0209AC30`+0x2C8) | PRIM:712 "NOT claimed: the `0209AC30`+0x2C8 record's owner" | — |
| G-110 (ops summary) | EEVU:196-197 "The `ops_summary` column is register traffic in instruction order, not a VU0 disassembly — masks and the actual arithmetic are still in the bodies." | every member must be translated |

#### 2.1.7 Object model (RTTI and the vtable method index)

| id| quote + cite | why a port needs it |
|---|---|---|
| G-111 (S37-1 slot-10 draw) | "A live capture of the slot-10 call is still the thing that would witness the draw itself, and that remains `PROPOSED-OPUS-S37-1`'s business. **This is NATIVE/STATIC evidence, not live.**" (RTTI:310-312) | text draw path order |
| G-112 (AS-5 accessor) | "which accessor each class declares at that slot is not recovered here" (RTTI:405) | 1,349 classes' slot 1 semantics |
| G-113 (zero-at-load fields) | "It says **nothing about the object's other fields** … the 104 writes that did not resolve to an RTTI name are unclassified here" (RTTI:994-997) | initial state of 346+104 globals |
| G-114 (work queue) | "**304 of the 346 are objects no page has ever mentioned**" (RTTI:992) | identity of static objects |
| G-115 (BA-1) | "Closed for the gate, unanswered in fact." (VTIDX:151); "Per-function provenance survives only in the unshipped `FF12X64.pdb`" (VTIDX:148) | 2,611 shared method bodies have no owner |
| G-116 (BA-5) | "**The eighth is unreconciled. BA-5.**" (VTIDX:2521-2522) | class set for size census |
| G-117 (single-route sizes) | "**Sizes for 80 of 125 game classes rest on a single route.**" (VTIDX:2531) | allocation sizes |
| G-118 (singleton class) | "NOT claimed: the object's class … the singleton's type name is not established here" (VTIDX:3340-3341) | `02CC0410` type |
| G-119 (CTextureUtil) | "`CTextureUtil` slots 1–4 (`00731AD0`–`0075ADF0`) remain unnamed." (VTIDX:2820) | PPFX device init |
| G-120 (BA-3 naming) | "the shape of const/non-const overload pairs (not verified by name)" (VTIDX:176) | method identity |
| G-121 (lua call site) | "the "call site" claim it was listed under remains unverified" (VTIDX:217-218) | — |
| G-122 (residue) | "no figure here should be quoted as if the two instruments agreed about them" (VTIDX:2756-2757); 351 functions with "no route found" (VTIDX:2658) | unreached code |
| G-123 (shout, narrower) | "**Still open on the narrower point:** *battle* voice specifically" (RTTI:200-201) — but see C.2 (answered 2026-09-22) | — |
| G-124 (AS-1b) | "reopen if the character controller is ever seen in a reflection registration table" (RTTI:628-629); "strong absence of evidence, not evidence of absence" (RTTI:626) | physics movement path |
| G-125 (crossings) | "**1 of the 12 bodies on that layer are read, the rest are counted**" (VTIDX:2854) | — |

#### 2.1.8 Shared-state accessors and the ownership boundary

| id| quote + cite | why a port needs it |
|---|---|---|
| G-126 (U-1/UQ-30 residue) | "What writes `+0x1044` and when is the residue that U-1 covers." (HUBS:295-296), while U-1 is "closed — the register row is WITHDRAWN" (HUBS:289) | the current-area id writer and timing are unknown |
| G-127 (hub 4 not established) | "which ids pass `BattleEncodedId_IsValidForClass(2, …)` … whether any caller stores a slot index across a pool reset." (HUBS:199-200) | 0xFF→0xFFFF path reachability |
| G-128 (U-4 frequency) | "Hot-or-cold is a frequency question and stays ASTRA's." (HUBS:336) | performance only |
| G-129 (`002F9860`) | "NOT claimed: which subsystem's records the 28 buckets hold" (HUBS:564-565) | record identity |
| G-130 (`00264010`) | "NOT claimed: what `003590D0` resolves the negative value against, or which tag system `+0x18` carries." (HUBS:583-584) | semantics |
| G-131 (`00307D10` gates) | "`00377C20` and `00253B90` gate the paths and are **not read**." (NBR:159-160) | engagement-flag paths |
| G-132 (unread neighbours) | "**Unread, and named as such:** `00226BE0` (1,936 B, 23 pairs), `00261F90` (335 B, read only to its first branch)" (NBR:258-259) | callees of shared paths |
| G-133 (UQ-31 residue) | "**Not read:** the group object's play body behind the wrapper, and the selector-`1` player at `+0x10`." (NBR:297-298) | sound playback body |
| G-134 (`02064AD3` writers) | "`0022AF50` sets to **3** and `0022B000` sets to **5** (§3 and §4)" (NBR:243-244) — §3/§4 of NBR do not describe these | mode-body semantics |
| G-135 (`00229E70` MXCSR) | "The game's MXCSR at this site is not established" (NBR:236) | NaN behaviour |
| G-136 (`01F83530`) | "That it is the PE or module image base is the name's reading, not established here." (NBR:186) | pointer codec base |
| G-137 (timeline residue) | "What each opcode's operands mean, and the authoring-side name of the track, are the residue" (OWN:539-540) | operand layouts of all 62 cases |
| G-138 (`003697F0`) | "NOT claimed: which heap `00369860` serves (CRT vs arena) or the `arg2` flag's meaning" (OWN:632-633) | allocator |
| G-139 (`002F31C0`) | "NOT claimed: the six handlers' identities … or which list pair `rdi` heads." (OWN:645-646) | teardown |
| G-140 (BQ-15) | "Whether every other category's shared helpers were held to the same rule is untested." (OWN:344) — carried to a board task (OWN:345) | classification only |

#### 2.1.9 Developer tuning console: dispatcher, tunables, second table, event slot, names

| id| quote + cite | why a port needs it |
|---|---|---|
| G-141 (RC-5) | "- [ ] **RC-5.** Which names and event ids the event-slot routes of §3 store" (EVSLOT:189); "**Proposed disposition, for a non-author reviewer:** ANSWERED … Not self-closed." and "the reviewer did not rule on the ANSWERED proposal." (EVSLOT:217) | domain of names/ids the slot table holds |
| G-142 (shared ids) | "**What the 56 shared ids were** before they were retired to the do-nothing arm" (C-CON:309-310) | history only; low |
| G-143 (code-table readers) | "*What the other 1,020 entries serve, if anything outside the console, is not read here.*" (C-CON:82-83); "*Not claimed:* that the engine reads this table to load a map" (CON2:86-87) | whether the table is load-bearing outside the console |
| G-144 (63 arms' writes) | "The other 63 ids stop at an object the fixture did not plant, or at a trapped import. Their write scope is not measured." (C-CON:190-191) | arm side effects |
| G-145 (runtime) | "**Empty.** … nothing here has been observed running." (C-CON:297); "**Not tested:** … **FULL SUBSYSTEM** while §13 is empty." (C-CON:337-339) | parity |
| G-146 (shader use) | "Which pixel the shaders compute from each variable is GPU bytecode and not claimed." (CON282:250) | visual effect of each tunable |
| G-147 (step column) | "**The `step` column is indicative, not verified per row.**" (CON282:341) | exact step per arm |
| G-148 (DoF two-source) | "No code path was followed from either source to `fParam_FocusDistance`." (TUNES:141-142) | DoF precedence |
| G-149 (MSAA writes) | "*Not claimed:* which values the shipped options menu writes to the framework setting." (TUNES:692) | defaults |
| G-150 (RC-8 limit) | "*Limit:* a pointer carried through an indirect call or a bulk copy is outside the census." (TUNES:593-594) | cascade count certainty |
| G-151 (§4 corroboration) | "it is not corroborated by any consumer, because no consumer of these addresses carries a string that names one." (TUNES:799-801) | binding confidence |
| G-152 (retail execution) | "*Static routes do not show that every retail state executes them. That is a live question.*" (EVSLOT:31) | which states fire |
| G-153 (path census) | "the census that produced it is not retained | not stated — unanchored" (EVSLOT:298) | path counts |
| G-154 (RC-6 why) | "*Not claimed:* why the entries were left so." (CON2:94) | low |
| G-155 (RC-4 assumption) | "**Assumption 2, stated:** the readers of `ext+0xA8` all lie in `00600000`-`00620000`" (CON282:284) | capture-row behaviour |
| G-156 (crossref) | "`crossref_clean` stays `false`." (C-CON:399) | neighbours unresolved |

#### 2.1.10 Developer tuning console: the arm catalogue (work division and slices A-I)

| id| quote + cite | why a port needs it |
|---|---|---|
| G-157 (D-13) | "**Flagged 2026-09-08, unresolved.** The paragraph above says **thirteen** arms; the table below maps **twelve** arm ids" (ARM-D:128-134) | which arms touch the map-art context |
| G-158 (D-134) | "Id 134's two follow-up calls have **15** and **2** callers image-wide respectively; neither is characterised here" (ARM-D:248-249) | side effect of changing WaterQuality |
| G-159 (D-2F8) | "*Not established:* a reader of `+0x2F8` or `+0x2E5`." (ARM-D:333) | |
| G-160 (E-name) | "**What the object at `02CB7FD0` is called.**" (ARM-E:346) | naming only |
| G-161 (E-166) | "**The virtual target of id 166** and the meaning of the `0x0E` selector (§7)." (ARM-E:349) — selector answered elsewhere (property 14, ARMDIV:475), virtual target still open | soft-particle toggle behaviour |
| G-162 (E-170) | "**Defaults for ids 170 and 171** — neither field is written by a constructor found here." (ARM-E:350) | initial values |
| G-163 (E-171) | id 171 target "`+0x1EC` of the object returned by the accessor called at `001D2A38`" (ARM-E:117) — accessor never named | SSS Blur owner |
| G-164 (F-bytes) | "Each arm then flips its byte; what reads those bytes was not traced." (ARM-F:315-316) | |
| G-165 (G-flag) | "Which store applies the chosen value to the story flag was not traced here." (ARM-G:189) | id 231 effect |
| G-166 (G-DDC) | "**What stays open.** What the 17 means." (ARM-G:199) | |
| G-167 (G-4E8) | "`01F7F4E8` has no RIP-relative writer, so its source was not traced." (ARM-G:221) | BGM forcing |
| G-168 (H-states) | "**What the non-negative states of ids 243–245 select.**" (ARM-H:293) | 100% steal/poach/drop semantics |
| G-169 (H-265) | "**What ids 265 and 266 address.** The accessor's object is not named" (ARM-H:295-296) | display/adapter object |
| G-170 (H-props) | "**Properties 11, 19, 20, 21** … reached by no arm" (ARM-H:300-301) | outside console |
| G-171 (I-9) | "What the value `9` for mode 4 selects in the renderer was not read." (ARM-I:307) | MSAA mode |
| G-172 (I-skip) | "Who calls `001E05F0` was not traced here." (ARM-I:315) | frame-skip order |
| G-173 (A-json) | "What the five JSON readers skip, and what that draw mode selects downstream, were not read." (ARM-A:303) | |
| G-174 (A-arg) | "whether they have one that receives it as an argument is not established" (ARM-A:255-257) — partly superseded by labels (ARM-A:261) | |
| G-175 (C-106) | "Whether that was intended is not recoverable from the code" (ARM-C:161) — closed as NO ADMISSIBLE SOURCE (ARM-C:242) | none |
| G-176 (B-frame) | "Who calls it is still untraced." (ARM-B:61) — answered at ARM-B:191-197 (C.2) | |

### 2.2 Structural gaps found while mapping (a port needs these and no 00 page states them)

Each item names a function, formula, field, initial value or format that a re-implementation needs, with the line
that shows the gap (usually a callee named and never described, or a value used and never given).

#### 2.2.1 Boot fixups, startup data construction and the application root

- **S-1.** Order of calls inside `0022A0B0` beyond seed/masks/frame-base/allocs: hubs `0037DF90`/`0037E0F0`, `0022CB90` (APP:1661-1663), `00266D10`, `002368D0` (BOOT:433), `0036D990` (EEVU:311), `00184960` (C-BOOT:309) — none of my pages gives their sequence; BOOT:226-227 "what any of the ~60 further boot calls do" is replaced only by the unordered subtree census (BOOT:392-407).
- **S-2.** `0017D6E0` pump order of the 13 singletons: APP:529-531 says "its ordering relative to the others is load-bearing" but no page gives the order; also the `edx` mode values and the "zero -> return 9" meaning (APP:226, 231) are not stated.
- **S-3.** `0017D650` (slot-4 run-once initialiser) is named (APP:224, 604) and never described.
- **S-4.** Initial value of `01F82E38` (C-BOOT:267-268 gives defaults for three cells only) and the `.data` initial of `02064ACC` before boot are not stated.
- **S-5.** "four `1.0f` values written to `02064AC0`–`02064AD4`" (BOOT:377): which four addresses is not stated; the range contains `02064ACC` and the frame-mode byte `02064AD3` (C.1).
- **S-6.** Object `02AE9290` (builder `004DA3C0`, hdr+memset) — TSV extent `0x70`, gap `0x280`, no memset size; C-BOOT:799 "`00861EC0` zeroes `0x70`"; FLOAT's size tables (FLOAT:519-537, 622-628) never give its size or explain the `0x210` remainder.
- **S-7.** Objects built by the two hub tail jumps (`004A8860` → `02AE1EF0`, C-BOOT:683; `004C3610`, C-BOOT:617 object not named) have no row in `builder-store-extents.tsv` and no size on FLOAT.
- **S-8.** `001EDDC0` LUT battery callees `0046FBF0`, `00471100`, `00473210`, `0033E310` listed as "Shared callees outside the census" (BOOT:530-531) with no description; table formula only for walkers (BOOT:525-528).
- **S-9.** `0018A840` (412 B, called at `0017D000`+59) given only as "`malloc` + the `001DE540` SIMD leaf + `00615CD0`/`0061D9C0`" (APP:632-633).
- **S-10.** GameApplication destruction: "*the application is never deleted* is probably true at runtime" (APP:375) — lifetime end of the root and of all 13 singletons not stated.
- **S-11.** Fields `+0x1130`, `+0x1138` touched by slot 2 (APP:63) have no meaning; slots 1,12,13,17-20,28-30 inherited (APP:166) — behaviour on other pages only (TUNES:652 names slot 28).
- **S-12.** MT19937 internals `00866D60`/`00866B90` and arena allocator internals are only on pages outside 00 (BOOT:220, 154).

#### 2.2.2 World tick, field frame and force-fight mode

- **S-13.** **Initial value of `01E0C2B8`** (force-fight flag) at boot/new game/load: not stated on FORCE (FORCE:58, FORCE:142 give only address). FORCE:299-300 asserts "the mode persists into save payloads" but no line shows the flag being serialised or restored.
- **S-14.** **What the `01EED060` latch's value is used for**: the tick only clears it to -1 (TICK:72; C-TICK:182 "consumed once → `cmovns`→`-1`"); no consumer of its stored value is named.
- **S-15.** **The tick's second argument (`edx` / `edi` "the field frame's own flag")** (TICK:54): only forwarded to `002F1770(mode, edx)` (TICK:153); what the flag means and what `002F1770` does with it: not stated.
- **S-16.** **Time-scale block formula** (TICK:155-156): `00362DB0()` plus `022C2544`, "compared against `002DEBA0()` [Audio], the smaller clamped to `1.0f`" — `002DEBA0` and `00362DB0`'s values not described (TICK:509 gives only "`00362DB0` (`022CBB28`)").
- **S-17.** **Prologue callees without behaviour**: `003EB9A0` (only a call list TICK:2036), `003DA2F0(1.0f)`, `003DD210(1.0f)`, `0025D640`, `0037D890`, `0046AFA0` (TICK:70-77; TICK:511 "`0046AFA0` (`02CA6040`–`4C` const bank)").
- **S-18.** **Tail callees without behaviour**: `003DE640`, `0037C1A0`, `003E7EC0`, `002F1770`, `002EF910`, `0036E1E0`, `00228480`, `00362DA0` (TICK:151-157; cluster tables TICK:505-512 give call shapes only).
- **S-19.** **`003DB6E0(record)`** called per live record by the post-pass (TICK:141): never described.
- **S-20.** **Unit-frame callees**: `00307C70`, `0033A240`, `003057D0`, `0030CA50`→`00322310`/`003228E0`, `00267240` (TICK:288-304) not described.
- **S-21.** **`00234520` callees** `00313DB0`, `00319090` (TICK:257) not described; `00313CD0` only gate shape (TICK:1480).
- **S-22.** **Initial image values** of `022C2548`, `02089340`, `0208E6A8`, `022C252C`/`022C2530`: not stated (C-TICK:17 says three tick-state globals' image bytes were read, but only `01EED060`/`01EED064` values are given, C-TICK:90-91).
- **S-23.** **Readers of `022C252C`/`022C2530`** and callers of resetters `00314010`/`00314000`: not stated (TICK:427).
- **S-24.** **Consumers of `0209A1F0`–`0209A20F`, `02099D70`/`02099D78`**: not stated beyond writers (TICK:85-86, TICK:434).
- **S-25.** **`0022BC20` mode-5 body** beyond its tick call: "~80 B … `"PAD CONTROL"` tagged block" (TICK:1468-1469) — contents not described.

#### 2.2.3 Per-frame update gate and system stop registry

- **S-26.** **The reproduction formula omits the gate's own state writes and inner tests.** C-GATE:105 says the gate writes "`object+0x10F68` bit 1, and the three pointer fields `+0x10F20`, `+0x10F30`, `+0x10F40`". C-GATE:327 names inner tests `0028E2EE test byte ptr [rbx+0x10F68], 8` and `0028E4B3 … 0x100`. C-GATE:263 names `+0x10F78`/`+0x10F80` pointer fields. §12 (C-GATE:190-209) has none of these. No page states which callee result is stored to which pointer field, or which group each inner test gates.
- **S-27.** **Group 0x0002 A and the 0x0004 multi-call sequence.** The table lists six calls for 0x0002 (GATE:89) and three for 0x0004 (GATE:90). The formula calls one function per group (C-GATE:194-195). The conditional call of `003F8B40` on a non-zero `001EDE80` (GATE:524) and the head pointer `[0209BE80]+0x10F00` passed to `0028C4C0` (GATE:225) are not in the formula.
- **S-28.** **Singleton lifetime end.** The allocation is stated (C-GATE:699-701). No destructor or free of the `0x10FD0` object is stated in any of the four pages.
- **S-29.** **Initial value of `01E0C2B0`.** C-GATE gives a writer and the value `0xF` (C-GATE:301). STOP adds `002547C0` (STOP:828). The `.data` initial value and the order of writes relative to the first pump call are not stated.
- **S-30.** **Four call-shape groups** (0x0008, 0x0100, 0x2000, 0x8000): callees are named, but bodies such as `002C8D60`, `003F7BC0`, `003F9720`, `0035BAD0` are given only as call lists (GATE:254, C-GATE:1457, 1666).
- **S-31.** **Registry: initial `01FD46D4`/`01FD46D0` values** are not stated (only the records' values, C-STOP:103-114).
- **S-32.** **Set-3 / set-4 consumers' on-screen effect** is not stated; the pages give only the mechanism (STOP:293, 457).
- **S-33.** **`00226BE0` argument list is elided**: "`00226BE0(id, actorHandle, flag, …, count, handles)`" (STOP:52). The elided arguments are not described. Other evidence shows five or six arguments (`00226BE0(0x16, 0, 0, −1, −1)`, TICK:846; `00226BE0(6, 0, 0, 0, ecx, flag)`, STOP:830).
- **S-34.** **"the reset" naming:** C-STOP:226 attributes the slot-13 bit-41 clear to "the reset" at `0022603A`. That address falls in `00225EB0` (area-unload) per EXP-191 (C-STOP:213-214), not in the initialiser `00226B30` (STOP:50). Which function a port's reset must reproduce is not stated directly.

#### 2.2.4 Battle runtime mode ladder, diagnostics log, duplicated names, all-ones convention

- **S-35.** **`0035C620`** — the bit-0 setter's propagate tail: "both changed paths tail `0035C620` to propagate" (MODE:1243-1244), "a recorded boundary" (C-MODE:346); never described on my pages.
- **S-36.** **`00313840`** (summon reset) — named as "(reset) clears" (MODE:110) and as the target of `00313650`, but its body/effects are not given on my pages (direction contradictory, C.1).
- **S-37.** **Initial value of `+0x5B04`/`+0x5B08` at new game** — only implied by the save-image memset (C-MODE:437-438) and `0030DA10`; when `0030DA10` runs is "for `BattleSystem_ResetRuntimeState`" (MODE:584) with no trigger stated.
- **S-38.** **`003EBD00`** and the countdown API (`003EBC50`) semantics (start/arrival) — `003EBC50` row fields given (MODE:1061) but `003EBD00` is named only (MODE:365, MODE:977-981).
- **S-39.** **`00229EA0`** "the mode query `00229EA0` is 5 or 6" (MODE:895) — a second "mode query" never described.
- **S-40.** **Consumers `00235EA0`, `00320230`** — listed as callers (MODE:203) with no description.
- **S-41.** **`003C5FF0`** first gate of `0035BC50` (MODE:705) and `BattleMenu_BuildCommandEntryList` (MODE:712) — named only.
- **S-42.** **`00313A00`** — `00313DB0` tail-calls this "289-byte function" (MODE:796-797); body not described; "a notification chain runs" (MODE:829) unspecified.
- **S-43.** **`00306D90`** "presentation worker" (MODE:998) and `0030D720` "defaults reset" (MODE:1118) — the special-sequence end path depends on them; only shape given.
- **S-44.** **Who calls `00304440` per frame** — MODE:315 "the frame handler" with no caller or frame position stated.
- **S-45.** **`002EB0D0`** actor-event hand-off (MODE:327) — named only.
- **S-46.** **`02EBF190` block size** — "≥ 23 KB" (MODE:219, MODE:461) only a lower bound.
- **S-47.** **LOG**: none structural for a port (sink does nothing but break on channel 4).
- **S-48.** **ONES**: the "global scale" and "a draw" of `004225A0` (ONES:251, ONES:254) are unnamed.

#### 2.2.5 Encoded-id space, class registry, query record, basis helpers, ABI recovery

- **S-49.** **Two state blocks, relation unstated.** Regions live in "the battle state block" (EID:114, "u32 offset of the class's **region A** in the battle state block"; class 5 A `+0x4748`, 64 words, EID:150), while list counts live at "`+0x47B8 + 4 × list`" of "the **image-backed state block** `*(020927C0)`" (EID:382-383). If one block, `+0x47B8` falls inside class 5's region A (`+0x4748`–`+0x47C7`). No page says whether the rebase base `02164280 + 0x4E68C` (C-EID:282) and `*(020927C0)` are the same object.
- **S-50.** **Initial value / creation of the state block** not stated (only its address, C-EID:282).
- **S-51.** **Slot-descriptor header (02EBFxxx) layout** is never given as one record: "count at `+4`" (CLS:208), row base `0020E600(dword [table directory + 0xC])` (C-EID:278), stride `word[+8]` (C-EID:358, EID:1017); `003845F0` AreaData_BindAndRebaseSectionDescriptor is named (CLS:172) but its behaviour is not described.
- **S-52.** **Filler arms not given as formulas:** "the complete filler remains the class table, original instructions and named test evidence—not an invented uniform row-copy formula" (C-EID:222-223).
- **S-53.** **Callees named, not described:** `0031E9A0` (C-EID entry, EID:533 "stores `0031E9A0(row)` at `+0x50`"; only "select equipment views" C-EID:151); `003241D0` (CLS:648, EID:541); `0046A630` obtain line (EID:314); `002CD650` sort (EID:384); `GameState_SetGil` (EID:339); `00318CD0` command gates (EID:367); `002EFA70`/`002EFE40` (EID:444, later named in EID:646-648 via outside-00 page).
- **S-54.** **Text bank decode** (`02EBF170`, `shr 0xb`, `[rax+rcx*4+4]`) only sketched (EID:737); full bank format is on a page outside 00.
- **S-55.** **Descriptor +0x14/+0x44:** "no meaning promoted here" (C-EID:68).
- **S-56.** **BASIS:** the "two components of the previous matrix … carried into the base" are not identified (BASIS:144-145); rotation axes not named ("two about one axis, one about another", BASIS:139-140); the two helpers' parameters unnamed.
- **S-57.** **ABI page is a measurement, not an interface:** "A derived signature is not an explanation." (ABI:36).

#### 2.2.6 Shared transform workbench (EE/VU0 register bank, save/restore, primitives)
- **S-58.** The 267 member routines (389,071 B) are a census, not a specification: EEVU:40 "188 are cited by no page"; EEVU:149-152 "Membership says **how** the member computes. It does not say **what** it computes." A port needs each body's arithmetic.
- **S-59.** Callees named but not described: EEVU:261 lists `00430B90`, `003A8950`, `ImageAddress_ResolveRuntimePointer` among the common callees; none is described in the group. `0036E1E0` calls `0024DE70` (WB:732) — undescribed. `0039AF70` body given only as "copies whatever `rcx` points at (`0039AF70`–`0039AF94`)" (PRIM:320).
- **S-60.** `0039B550`: "a `cvtdq2ps` conversion of an int4 row accumulated into a global float" (PRIM:634-635) — the global is not named.
- **S-61.** `003D8E50`'s 23-bit recurrence is deferred to another page (SAVE:287); `0042FDB0`/`0044BAC0` are described "by their callees" only (SAVE:287 "the three large ones by their callees").
- **S-62.** Initial ids of the `022D94B0` records: only the state reset is stated (C-WB:118-119); field `+6` and the rest of the 24 B are not laid out ("`…`" in WB:326).
- **S-63.** Save arrays' initial content not stated (C-SAVE:57-58).
- **S-64.** Frame position of most members not stated: EEVU:270 gives reachability counts only.
- **S-65.** `022D9140`–`022D916C` slot owners per function not listed (EEVU:233-237).
- **S-66.** `0036D9E0`'s role per frame (called by `003E00C0`, C-WB:247) vs "initializer" (WB:107-124): when and why it clears is not stated.

#### 2.2.7 Object model (RTTI and the vtable method index)

- **S-67.** **Behaviour of the 4,275 methods**: "This index gives identity — class and slot — not behaviour. **Nothing here has had its body read.**" (VTIDX:152-153); BA-2 was closed only by ruling ("SUPERSEDED 2026-09-26 … a population-coverage statement", VTIDX:154), not by reading. Only ~250 bodies are described in the update sections (VTIDX:2863-5219).
- **S-68.** **Per-class object layouts/sizes not tabulated**: §10 reports counts ("92 of 125", VTIDX:2472) but no per-class size table on the page.
- **S-69.** **Slot semantics across classes**: "or that a slot number means the same thing across classes" is explicitly not claimed (VTIDX:201-203).
- **S-70.** **Callees named but not described on these pages**: `00597690` ("whatever the constructor computes at `00597690`", RTTI:995); `00584730` (used as free throughout, e.g. VTIDX:4409, never described); `0017D260`/`00584740`/`001A1470`/`00809950` allocators (VTIDX:4751, 5057; RTTI:272; VTIDX:2893); `00810240`/`0080FA50`/`00810F60` type registration (VTIDX:4762-4767); `0083A3A0` (RTTI:937, 1028); `00861F14`; `0020E680`/`0020E670`/`0020E630` (RTTI:1042-1047; VTIDX:4479-4481); `005CCB80(1)` "count release"/"yield" (VTIDX:4393, 4441); `00808C40` CFG guard.
- **S-71.** **No runtime order**: "Call chain — Not applicable" (VTIDX:127).
- **S-72.** **Reflection invocation**: physics is reached through `PMethodCallerConcrete` objects; "there is no edge to find" (RTTI:512) — the reflection dispatch tables a port would need are not described here (points to 22-Middleware).
- **S-73.** **Zero-at-load object field initial values**: not stated (RTTI:994-996).

#### 2.2.8 Shared-state accessors and the ownership boundary

- **S-74.** Initial values and writers for pool globals `0208E688`/`0208E6A0` not stated (HUBS:161-162 only read them).
- **S-75.** `Actor_GetWorldPosition` body given only as pseudocode "(from Actor/Entity, repeated …)" (HUBS:227-233); `movementState` origin not stated on these pages.
- **S-76.** `SaveImage_GetPersistentPayloadBase` offset known, but payload layout beyond `+0x1044` not stated (HUBS:216-219).
- **S-77.** Action context `02F97348`: allocation, size and lifetime not stated; only field reads (OWN:514-518).
- **S-78.** Timeline opcodes: callees given by the TSV but per-opcode operand layout absent ("the rest opcode-specific", OWN:503).
- **S-79.** `003A1180` "argument" source and `00249C60`'s caller-supplied value not stated (NBR:96).
- **S-80.** `001DBDB0` group player body/play wrapper not read (NBR:297).
- **S-81.** Scratch-pool class semantics (`022D89BC` class word, `022D7FD0` descriptors) not stated beyond mechanics (OWN:915-959).
- **S-82.** Frame placement (which phase of the frame) of the hubs, audio chain, and timeline interpreter not stated.

#### 2.2.9 Developer tuning console: dispatcher, tunables, second table, event slot, names

- **S-83.** Per-arm behaviour is not on these pages: "Per-id arm semantics | the nine arm-catalogue slices, ids 12–293 | carried" (C-CON:325); "**The nine slice documents are the authority for behaviour**" (CMDNAMES:89). A port of the 226 arms needs the slices (outside this group).
- **S-84.** Direction mapping: the arm increments when `bl` is zero (`test bl, bl / je … addss`, CON282:381-386) and the adapter sets `r8b = (dl == 0)` (CON282:505), but which physical press (left/right) gives which `dl` is not stated; CON282:507 says only "called with the left/right direction of the press".
- **S-85.** Console settings singleton (0x10E8) layout and the constructor `001CCB20`'s initial values: only `+0x130`, `+0xAAC`, `+0xAB4`, `+0xC72..` and per-id `rdi+…` cells are named (CON2:116-118; CMDNAMES:112-376); no initial values.
- **S-86.** Block defaults: "the chain writes **107 distinct block offsets**" (TUNES:395) but values are listed only for 27 named offsets (TUNES:414-442); "`+43C` `+444` | … | —" has no default (TUNES:442). The 45 `005DC580` immediates exist only in an uncited TSV.
- **S-87.** Menu UI: the renderer's printing is stated (`"%s%s%f"`, C-CON:268) and its helpers (TUNES:1107-1117), but row selection, cursor, input handling and how the developer menu opens are not: "nothing here establishes *how* it is opened" (TUNES:522-524).
- **S-88.** `0017DB90`'s 23 cases → 16 ids mapping not tabulated (CON282:271).
- **S-89.** Code table contents: only sample codes (C-CON:79; CON2:57-66, 80); the full list comes from an outside TSV (CON2:78).
- **S-90.** `001F0AD0` scalar writes: "The remaining **28 writes** land above `02CB835F`" (TUNES:958) are unnamed except `block+0x3E4`; `001EF6D0`'s "frustum maths" is elided (TUNES:246).
- **S-91.** Event slots: initial values of the arrays not stated; the notifier "`00189120` + `0016D6A0`" (EVSLOT:129) and `0032E400` existence check (EVSLOT:141) are not described; `001EC4B0` "(three callers)" not named (EVSLOT:159).
- **S-92.** 79 callees of the dispatcher: most are not described here (C-CON:204).

#### 2.2.10 Developer tuning console: the arm catalogue (work division and slices A-I)

- **S-93.** **Caller cadence of the console**: only the Config-screen route is stated (ARM-B:191-196); when `001D1660` runs in a frame is not stated on any of my pages.
- **S-94.** **`001D4C1C` table contents**: the per-id arm column exists (all slice tables), but the decoding rule needs the image base `0x00120000` (ARMDIV:161-162) — stated; fine. The 22-row page table used by the renderer (`table[page·22 + row]`, ARM-E:315-317) is not given.
- **S-95.** **Accessor for id 171 and ids 265/266** never named (ARM-E:117; ARM-H:91-92).
- **S-96.** **Id 53 target**: slice row blank (ARM-B:81) while the consumers TSV binds id 53 to `02CB813C` "Debug Cubemap".
- **S-97.** **Id 32 second target**: ARM-A:101 gives only `d+0xC2C`; the consumers TSV also binds id 32 to `02CB814C`.
- **S-98.** **Id 28 full save list**: ARM-A:97 lists twelve `rdi` save fields; CMDNAMES:419 adds `01DFE190`–`01DFE192`, map-art `+0x2D0/+0x2D4/+0x2E4`, bytes `02CB7FD0`/`02CB7FE4`, and recomputes `02CB8080` — no slice states that mapping.
- **S-99.** **Ids 45–57 "other" arms**: getters/setters named but `00193F70`, `00182FD0`, `0017FE10`, `001D5230`, `00184660`, `001B1620`, `001AD4D0` effects described in one line only (ARM-B:204-217).
- **S-100.** **Ids 177/178 and 180/181 "then one call"** callee not named (ARM-F:111, ARM-F:114); ids 205–207 named; id 182 "one call with value−1" callee not named (ARM-F:115); id 263 "a string-taking function" not named (ARM-H:165).
- **S-101.** **Destruction / lifetime** of the console object at `01F81428`: not stated.
- **S-102.** **`+0x10C4`** owner ambiguous (C.1).

## 3. Contradictions (statements a re-implementer would have to choose between)

Quotes are exact, from the snapshot. `…` marks an elision; emphasis markers (`**`, `~~`, `*`) inside a quote are
kept as they appear on the page. "Favoured" is named **only** where a dated correction on the pages settles the
point; otherwise the item says **no favoured side**. Where the corrected claim is still printed unstruck elsewhere,
the item says where. Every value-changing item is **page-text only - needs local check**: this session cannot see
the executable.

### 3.1 Value-changing (behaviour, offsets, addresses, sizes, constants, formulas, function extents)

Favoured side named, wholly or in part (40 items): C-V1, C-V11, C-V31, C-V32, C-V33, C-V34, C-V42, C-V43, C-V53, C-V58, C-V65, C-V66, C-V67, C-V68, C-V73, C-V90, C-V91, C-V92, C-V100, C-V101, C-V102, C-V103, C-V104, C-V105, C-V113, C-V117, C-V119, C-V125, C-V128, C-V129, C-V132, C-V133, C-V137, C-V138, C-V140, C-V149, C-V152, C-V154, C-V162, C-V164. C-V68 is listed although its two sides already agree after a dated correction (`C-EID:347`); it is kept so that the corrected text is not reused. Every other C-V item has no favoured side.

#### 3.1.0 Cross-group items (one contradiction reported by more than one reader)

**C-V1.** **`0016D6A0`: a three-byte `ret`, or a release / free / over-range report.** *(found by three readers; merged)*
- Side A: `DUP:229`: "**`0016D6A0` has a three-byte body: `ret`.**" (§8b, "added 2026-09-13, OPUS", `DUP:224`); `QREC:217`: "| Q6 | §3 "the original `ret0` stub" | **survives**: `0016D6A0` is `ret 0`, three bytes, with 2,868 call sites." (falsification pass 1, 2026-09-29, `QREC:203`); `C-EID:55-56`: "the original three-byte `ret 0` at `0016D6A0` … That stub is not an error-state proof"; `VTIDX:101`: "`ret` placeholder"; `MODE:352`: "the empty stub `0016D6A0`".
- Side B: `TICK:454`: "`0016D6A0` is the string-member release."; `TICK:511`: "`0016D6A0` free"; `RTTI:1093-1097`: "each allocation immediately handed back to `0016D6A0` on the same allocator object"; `EID:1114-1116`: "`ecx > 0xB` reports `0016D6A0(0x200)` and clamps the index to 0".
- Status: **favoured side A** for the body, by the dated §8b measurement (`DUP:224-229`, 2026-09-13) and the dated pass row Q6 (`QREC:217`, 2026-09-29). Neither strikes side B: `TICK:454`, `TICK:511`, `RTTI:1093-1097` and `EID:1114-1116` are unstruck. A port that implements the call as a free or as an error report changes memory or control behaviour at 2,868 call sites. A separate count disagreement on the same address (three tables vs 1,291 classes) is C-V106.
- page-text only - needs local check

**C-V2.** **`001EC560`: does it require `00265680()` to hold, or to answer zero?** *(found by two readers; merged)*
- Side A: `TICK:928-929`: "`001EC560` is *the current cutscene slot `01DFE40C` is 0–4, its per-slot flag at `01F832B0` is set, and `00265680()` holds*"; `EVSLOT:152`: "`001EC560` probes `[01DFE40C] ≤ 4 → 01F832B0[index]`, nonzero runs `00265680`."; `EVSLOT:247`: "| `001EC560` | pending probe | 59 B | `01F832B0[marker] != 0` and `00265680()` |".
- Side B: `C-TICK:209-210`: "`001EC560` = `01F832B0[dword[01DFE40C]] != 0` (index bounded ≤4) **and** `00265680() == 0`"; `C-TICK:326`: "the story word selected by `01DFE40C` out of `01F832B0` is non-zero and `00265680` answers zero".
- Status: no favoured side. The 2026-09-22 strike note near `C-TICK:199-212` corrects the map-art address, not this polarity. The polarity decides whether the field frame's third entry gate runs or skips while the slot-0 manager is ready.
- page-text only - needs local check

**C-V3.** **What `00265020` is: the force-fight / console getter, or `Actor_GetWorldPosition`.** *(found by two readers; merged)*
- Side A: `FORCE:305-308`: "`00265020`'s reader population continues into … The force-fight getter is read wherever the mode matters"; `TUNES:755`: "`00265020` — the console-side fetch the arms share".
- Side B: `FORCE:327`, `FORCE:342`: "`Actor_GetWorldPosition` (00265020)"; `TUNES:1187`: "`Actor_GetWorldPosition` (00265020)"; `TUNES:1123`: "`00265020` is also called by 16 **Movement**-layer bodies". `FORCE:60` and `FORCE:143` make `00253B90` the force-fight flag reader.
- Status: no favoured side. Each page states both identities.
- page-text only - needs local check

**C-V4.** **Console step-size census: two populations, two answers.** *(found by two readers; merged)*
- Side A: `ARMDIV:44`: "magnitudes 0.01 × 58, 0.02 × 11, 0.05 × 10, 0.1 × 9, 0.001 × 7, 0.03 × 3, 1.0 × 2, 0.005556 × 1, 0.5 × 1"; `CON282:433-437` (the same table, "| **total** | **102** |").
- Side B: `C-CON:140-141`: "**56 arms step by exactly 0.01**, then 0.1 (7), 0.02 (7), 0.001 (6), 0.05 (5), 1.0 (4), **0.005 (4)**, 0.03 (3) and **0.005556 (2)**" (runtime replay, `C-CON:139`). `ARM-F:123-125` has ids 190–192 stepping "**0.002, scaled**", which is in neither table.
- Status: no favoured side. The methods differ (static table walk vs runtime replay from zero), and neither page retracts the other. A port's per-arm step constants come from the slices, not these tables (see S-83).
- page-text only - needs local check

#### 3.1.1 Boot fixups, startup data construction and the application root

**C-V5.** **Where the 1 MiB block's pointer is stored**
- Side A: `BOOT:350`: "0022A28B  0x0100000 -> (not stored here)"
- Side B: `BOOT:164-165`: "the 1 MiB block's pointer goes to `01FD4A90` (`0022A2A3`)"; also `C-BOOT:228-230`: "each is followed only by `mov ecx, <next size>` and a store of `rax` into its `.data` pointer slot (`01FD49F0`–`01FD4A90`)"
- Status: no favoured side (BOOT:165 is a "Narrowed (cited 2026-09-30)" note citing `_types/fields.tsv`, but it does not strike BOOT:350). BOOT:350 still unstruck.
- page-text only - needs local check

**C-V6.** **Boot seed call site**
- Side A: `BOOT:38`: "002648..  func_0x00379CF0(0x11B9);      // through a 5-byte thunk -> 00863D30"
- Side B: `C-BOOT:839`: "a third caller of the seed thunk … survives: exactly `0022A410` and `005843D3`"
- Status: no favoured side (C-BOOT falsification 2026-09-29 does not mention BOOT:38). `002648..` lies outside `0022A0B0`'s 978-byte body.
- page-text only - needs local check

**C-V7.** **Order inside `0017D000`: allocate before or after `0017D4C0`**
- Side A: `FLOAT:83-87`: "+31   call 0017D4C0 … +41   call 00210EC0            allocate" (offsets "SURVIVED, all five exact", FLOAT:431)
- Side B: `APP:629-630`: "`0017D000` itself allocates an `0x80` record into `[01F7E340]`, then calls three bodies before latching `+0x113C`: **`0017D4C0`** …"
- Status: no favoured side.
- page-text only - needs local check

**C-V8.** **`02064ACC` value after boot at default settings**
- Side A: `BOOT:378-379`: "with the shipped value of `1` the quotient is `2`" (with BOOT:110: "`0022BDF0` … runs first, and then")
- Side B: `C-BOOT:212-214`: "in the vanilla install with default settings the answer is the non-zero branch — `setting[18] = 1`, quadruple written, `01DFE0B4 = 2`" (so `2 / 2 = 1`)
- Status: no favoured side; C-BOOT:218-224 adds a PROBABLE ordering ("the engine starts on the 30 fps base and switches later in startup") that would make the boot division read `1` — undecided.
- page-text only - needs local check

**C-V9.** **`02064AC0`–`02064AD4` "four 1.0f values" overlap integer/byte cells**
- Side A: `BOOT:377`: "alongside four `1.0f` values written to `02064AC0`–`02064AD4`"
- Side B: `BOOT:254`: "`02064ACC` \| frame-base constant \| `.data` dword \| `2 / FrameLimit`"; `APP:707`: "the mode-change detect on `02064AD3`"; `C-BOOT:465`: "comparing `movsx b[02064AD3]` against the mode argument" (and MODE contract `C-MODE:451`: "`byte[02064AD3]` (0–6, default→`0022A770`)")
- Status: no favoured side; the four float addresses are not given (G.2).
- page-text only - needs local check

**C-V10.** **`001C0D40` lazy or unconditional**
- Side A: `APP:640`: "`001C0D40` →`[01F81258]` (alloc `0x1B8`, ctor `001BE730`) … the shared shape `cmp [G],0 → jne done → alloc → ctor → store [G]`"
- Side B: `APP:2437`: "calls `0016D6A0(qword 01F81258 is null)`, then always allocates `0x1B8` bytes … and stores the result at `01F81258`"
- Status: no favoured side (APP:2437 is OPUS 2026-10-01 interior read but does not strike APP:640).
- page-text only - needs local check

**C-V11.** **Number of pumped singletons: 16 vs 13**
- Side A: `APP:227`: "37 callees: 16 are 8-10 byte singleton getters"; repeated `APP:236` "the other fifteen follow", `APP:251-252`, `APP:404`
- Side B: `APP:299`: "**BE-6 — ~~partly~~ answered 2026-09-27.** The tick pumps **13 lazily-constructed singletons**, not 16."; `APP:479`
- Status: favoured side B by `APP:299` (dated 2026-09-27 answer). Side A still repeated unstruck at APP:227, 236, 251-252, 404.
- page-text only - needs local check

**C-V12.** **`0037E0F0` call/lea count**
- Side A: `FLOAT:253-254`: "`0037E0F0` makes 49 (48 distinct; `004E3110` twice)"
- Side B: `BOOT:401`: "`0037E0F0` (596 B — 48 call sites, 47 distinct targets: **45** in the `0047xxxx`–`004Fxxxx` band plus member calls `002EFF50`/`002F0110`"; `C-BOOT:521`: "46 straight `lea rcx, …` … each handed to a … initializer, with a lone `jmp 004C3610`"; TSV: 48 rows
- Status: no favoured side.
- page-text only - needs local check

**C-V13.** **`0037DF90` call count**
- Side A: `FLOAT:253`: "`0037DF90` makes 28"; `FLOAT:108` "26 from the first hub" (into band)
- Side B: `BOOT:401`: "`0037DF90` (344 B — calls **27** distinct `0047xxxx`–`004Exxxx` bodies"; `C-BOOT:637`: "thirty `lea rcx, 02ADExxx/02AExxxx` + `call` pairs"; TSV: 27 rows
- Status: no favoured side.
- page-text only - needs local check

**C-V14.** **Gap after `02AE8900`**
- Side A: `FLOAT:528`: "`02AE8900` \| `004F4F80` \| `0x2E0` \| `0x530`"
- Side B: `members/builder-store-extents.tsv` row 32: `02AE8900 004F4F80 … 0x2E0 0x2E0` (next object `02AE8BE0`, builder `0047A800`, out of band)
- Status: no favoured side (population difference: FLOAT's table measures to the next in-band pointer; not stated on page).
- page-text only - needs local check

**C-V15.** **`0022A0B0` described as a hub**
- Side A: `APP:776`: "`0022A0B0`, the startup chain's second hub"
- Side B: `FLOAT:157`: "hubs \| `0x0037DF90` (26 calls), `0x0037E0F0` (40 calls)"; EEVU:325 "`0022A0B0`, the startup hub"
- Status: no favoured side.
- page-text only - needs local check

**C-V16.** **Role of `0079C140`**
- Side A: `APP:281-282`: "rewritten by the screen-mode routine `0079C140` from `GetSystemMetrics`"
- Side B: `TUNES:652` (other 00 page): "its per-frame update is the inherited slot 28 `0079C140`, run by the loop `00796490`"
- Status: no favoured side (may both hold; neither page reconciles).
- page-text only - needs local check

#### 3.1.2 World tick, field frame and force-fight mode

**C-V17.** **`001EDDA0` predicate globals**
- Side A: `TICK:1543`: "`dword[01FCE0C0] != 0` **or** `dword[0209DE38] == 0`"
- Side B: `TICK:1066`: "(`001EDDA0` — the 27 B `[01DFE0C0] != 0 || [01F82E38] == 0` predicate —"; also `C-TICK:226`: "`[01DFE0C0] != 0 || [01F82E38] == 0` predicate"; `NBR:234`: "`[01DFE0C0] != 0 \|\| [01F82E38] == 0`"; `C-BOOT:288`: "`01DFE0C0` (suppressor) first, then `01F82E38` (flag)"
- Status: no favoured side (no dated correction); Side B repeated on four lines across three pages.
- page-text only - needs local check

**C-V18.** **`003DF760` table addresses**
- Side A: `TICK:901-902`: "pointers `02B59C40[n]` and `02B59C80[n]`, dwords `02B59CC0[n]` and `02B59CE0[n]`"
- Side B: `TICK:1666-1668`: "`qword[0x2A39C40 + i*8] = r9`, `qword[0x2A39C80 + i*8] = stack arg`, `dword[0x2A39CC0 + i*4] = r8d`, `dword[0x2A39CE0 + i*4] = ecx`"
- Status: no favoured side.
- page-text only - needs local check

**C-V19.** **Skip pending/active arrays `022CB9C0`/`022CB9D8` vs `021AB9C0`/`021AB9D8`**
- Side A: `TICK:188-189`: "its row in the pending / active dword arrays `022CB9C0` / `022CB9D8`"; `TICK:178`: "pending bits at `022CB9C0`"
- Side B: `TICK:2171`: "`0x21AB9C0`/`0x21AB9D8` dword tables, `022CB732` `rax<<7` records"; `TICK:2606-2607`: "the two `02CDC4xx`-region dword masks at `+0x21AB9C0`/`+0x21AB9D8` per slot"
- Status: no favoured side.
- page-text only - needs local check

**C-V20.** **Skip-entry stride / `00360710` shape and extent**
- Side A: `TICK:187-188`: "a 16-byte entry at `022CB730 + (manager × 8 + k) × 16`"; `TICK:178`/`TICK:191-198` describe `00360710` checking live/armed, audio stop, eleven notifications, through `0036084F`
- Side B: `TICK:1328-1331`: "`00360710` (64 B) — an 8-byte-element range bound: `rsi = movsxd(edx)` count, `r14 = movsxd(ecx)` start … `rdi = r14 + rsi*8` over the `022CB730` array"
- Status: no favoured side. (64 B cannot contain sites up to `0036084F` cited on the same page.)
- page-text only - needs local check

**C-V21.** **Timed-record pool `02EBB6F0` (0x50) vs `01EAB6E0` (x80)**
- Side A: `TICK:789-790`: "the `0x50`-stride pool at `02EBB6F0`"; `TICK:1196`: "whose `0x50`-byte entry at `*02EBB6F0`" with count "dword `02EBB6E0`"
- Side B: `TICK:2502-2503`: "`ecx` bounds-checks against `dword[01EAB6D8]`, selects the x80 record in `01EAB6E0`" (`00467730`)
- Status: no favoured side.
- page-text only - needs local check

**C-V22.** **Loader state `020C51C0` vs `022C51C0`**
- Side A: `TICK:1577-1579`: "re-polls `[020C51C0]` … returns `([020C51C0] != 0) | !0046DFE0()`"
- Side B: `TICK:1867`: "`0032E070` (the `022C51C0` loader state-machine pump)"
- Status: no favoured side.
- page-text only - needs local check

**C-V23.** **Slot table base `0209BE10` vs `02098E10`**
- Side A: `TICK:683`: "`00267360` (50 B) | the slot-0 probe … indexes the `0x288`-stride table at `0209BE10`"
- Side B: `TICK:63`: "**actor-manager slot array at `02098E10`, stride `0x288`**" (and every other `0x288` reference, e.g. TICK:1120-1122, TICK:1584-1585)
- Status: no favoured side.
- page-text only - needs local check

**C-V24.** **Frame-mode numbers of the three tick callers**
- Side A: `TICK:54-56`: "| 2, the field frame | `0022A770` …| 3, the full-menu frame | `MainLoop_UpdateAndRenderFrame` `0022B8C0` …| 5, the capture-backed frame | `0022BC20`"; `TICK:581-583` same
- Side B: `C-MODE:469-470`: "`00314020 ←` state arms `0022B8C0` (2), `0022BC20` (3), `0022A770` (>6)"; `C-MODE:451`: "(0–6, default→`0022A770`)"
- Status: no favoured side.
- page-text only - needs local check

**C-V25.** **`00234520` extent**
- Side A: `TICK:256`: "**`00234520(slot)`** (109 B)"; `TICK:369`: "| `00234520` | 109 B |"
- Side B: `TICK:1475`: "`00234520` (~220 B) — 64-aligned stack frame; `ecx == 0` runs `0023B040` (`00234531`/`00234533`)" (TICK:256 puts the slot test at `0023452F`)
- Status: no favoured side.
- page-text only - needs local check

**C-V26.** **`00265A20` extent and loop bound**
- Side A: `TICK:365`: "`00265A20` | 320 B"; `TICK:267`: "up to 32 of them (`00265A8F`)"
- Side B: `TICK:1435-1437`: "`00265A20` (`ActorSystem_BindBattleUnitsForEligibleRecords`, ~200 B) — loops `dword[rcx+0x20]` slots"
- Status: no favoured side.
- page-text only - needs local check

**C-V27.** **`0022BC20` extent vs its tick call site**
- Side A: `TICK:56`: "`0022BC20` | `0022BCC8`–`0022BCCF`, same label" (ATEL CONTROL)
- Side B: `TICK:1468-1469`: "`0022BC20` (~80 B) — `0016D6A0(3)`, `0017F740(0)`, `0036F2F0`, then a `"PAD CONTROL"` tagged block" (80 B ends at ~`0022BC70`, before `0022BCC8`)
- Status: no favoured side.
- page-text only - needs local check

**C-V28.** **First mode test site**
- Side A: `TICK:91`: "**This call sits before the mode test (`0031410C`)**"; `TICK:120`: "`0031410C jne -> 00314231`"
- Side B: `C-TICK:73-74`: "`0025BFB0` is called at `00314078`; the first mode test is `003140CF`"; `C-TICK:68-69` tests "at **`003140CF`, `003140DC`, `00314103`/`00314108` and `00314249`/`0031424E`**" (no `0031410C`)
- Status: no favoured side (C-TICK falsification 2026-09-29, C-TICK:337, confirms its own sites but does not address TICK's `0031410C`). WT-2's conclusion is the same on both sides.
- page-text only - needs local check

**C-V29.** **`0036DE70` store value**
- Side A: `TICK:797`: "it sets `+4 = 4`"
- Side B: `TICK:1786-1787`: "it stores `bx+4` into `word[+4]`"
- Status: no favoured side.
- page-text only - needs local check

**C-V30.** **`003DEE10` streaming-slot base**
- Side A: `TICK:806-807`: "the manager's eight `0x38`-stride streaming slots at `02B58960 + m × 8 × 0x38`"
- Side B: `TICK:1944`: "`003DEE10` (432 B) is the `0x38`-stride streaming-slot drain … over `02B59360`/`02B59C20`"
- Status: no favoured side.
- page-text only - needs local check

#### 3.1.3 Per-frame update gate and system stop registry

**C-V31.** **Enable word width: 16-bit vs uint32**
- Side A: `GATE:33`: "**A single 16-bit word decides, every frame, which sixteen groups of updates run at all**"; `C-GATE:28`: "One 16-bit word at `01E0C464` decides which subsystems tick"; `C-GATE:103`: "the enable word at `01E0C464`, sixteen bits, every frame"
- Side B: `C-GATE:45`: "**`uint32`** … *CORRECTED 2026-09-25 (OPUS): this cell said `uint16`. … MSVC does not emit a dword read of a 2-byte global; §3 proves not-`uint8`, not `uint16`.*"
- Status: favoured side B by "*CORRECTED 2026-09-25 (OPUS)…*" (C-GATE:45). Still repeated unstruck at GATE:33, C-GATE:28 and C-GATE:103.
- page-text only - needs local check

**C-V32.** **Gate test widths: all `test byte` vs 8 byte + 8 dword**
- Side A: `GATE:262`: "| one enable word, fifteen masks | 16 `test byte [01E0C464], imm` sites in `0028E290`"; `GATE:53`: "test byte [01E0C464], <mask>   x15"
- Side B: `GATE:66-67`: "**8 are `test byte`** and **8 are `test dword`**"; `C-GATE:344`: "**8 byte + 8 dword = 16**"
- Status: favoured side B by the dated pass "## 11. Falsification pass 1 — 2026-09-13 (OPUS)" (GATE:332), which measured "`0x01`–`0x80` as `test byte ptr` × **8**; `0x100`–`0x8000` as `test dword ptr` × **8**" (GATE:345). Still unstruck at GATE:262 (evidence table) and GATE:53 (diagram, which also says "x15").
- page-text only - needs local check

**C-V33.** **FramePump takes an argument, and the formula ignores it**
- Side A: `C-GATE:191`: "void FramePump(void) {                      /* 0028E290 */"; `C-GATE:198`: "if (en & 0x0002) Group_00291B90();      /* same bit, second group */"
- Side B: `C-GATE:82-85`: "**And §2's "none used by the gate logic" is wrong.** `0028E2A0 mov edi, ecx` … `0028E3B7 test dil, 1` gates the second of bit 1's two groups … A reimplementation taking no parameter runs that group unconditionally"
- Status: favoured side B by "**CORRECTED 2026-09-12 (`OPUS-FRAMEGATE-ISOLATED`)**" (C-GATE:61). The §12 formula (C-GATE:191-209) still has no parameter and no `dil&1` test.
- page-text only - needs local check

**C-V34.** **Group handler signatures: nullary vs one EMBED child each**
- Side A: `C-GATE:193-208`: "if (en & 0x0001) Group_00289970(); … if (en & 0x0800) Group_0028C870();"
- Side B: `C-GATE:439-442`: "§13's reconstruction sketch writes the handlers as `Group_003F9F40()`, `Group_00296860()` and so on — nullary … **They each take one specific EMBED child of the `0209BE80` singleton**"
- Status: favoured side B by the dated section "(2026-09-18, OPUS)" (C-GATE:437), which explicitly corrects the sketch. The sketch at C-GATE:193-208 is unstruck. Side B cites "§13", but the sketch is §12.
- page-text only - needs local check

**C-V35.** **Pump argument `word[01E0C2B0]`: single writer, always 0xF vs stop-apply writes 0x10/0x0E**
- Side A: `C-GATE:301-302`: "`dil&1` — the pump's first argument, `word[01E0C2B0]`, written once at `002539E5` with `0xF` (so always true in this build)"; repeated at `C-GATE:335`: "feeds the pump `word[01E0C2B0]` (single writer `002539E5`, value `0xF`)"
- Side B: `STOP:299`: "*A/B bits 36..37*, the words `01E0C2B0`/`01E0C2AC` given `0x10` or `0x0E`: … `01E0C2B0` is the argument of the battle-HUD draw `0028E290` … the battle draw tests bit 0 … both words are also restored by the save apply `00253970`"; `STOP:828`: "`002547C0` | 12 B | stores `cx` in word `01E0C2B0` (its entry instruction), then tail-jumps to `003BBF90`"
- Status: no favoured side. Under side B, every stop that reaches the A/B 36–37 path writes a value with bit 0 clear (`0x10`, `0x0E`), so group 0x0002 B would be skipped. Side A says it always runs.
- page-text only - needs local check

**C-V36.** **`001EDE80` meaning: pause / cutscene-name-slot counters vs half-rate / frame counters (same logic)**
- Side A: `GATE:254`: "`001EDE80` returns 1 under the pause predicate (`[01F82E38]` zero or `[01DFE0C0]` set) and otherwise the sum of the two cutscene-name-slot counters `0022A080()` and `0022A030()`"; `C-GATE:297-298`: "`001EDE80` — the pause/cutscene-name-slot predicate"
- Side B: `GATE:520-523`: "**Group 2 (`0x0002`, the half-rate walker).** … It returns 1 unless half-rate is on (`[01F82E38] != 0` and `[01DFE0C0] == 0`). Under half-rate it returns the sum of the two frame counters `[02064AD8]` and `[02064AA8]`."
- Other 00 pages: `C-BOOT:290` "`1`, unless the mode is on and unsuppressed — then `0022A080() + 0022A030()`"; `C-BOOT:462` "`001EDE80`'s live-path sum is `d[02064AD8] + d[02064AA8]`"; `BOOT:505` "`dword[01F82E38] = 1`" on "the 60 fps arm" (BOOT:502). These support "mode = 60 fps", not "pause".
- Status: no favoured side. The truth tables agree; the meaning differs (pause vs 60-fps half-rate), and so does what the counters are.
- page-text only - needs local check

**C-V37.** **Group 0x1000 (Libra) member selection: "or" vs "kept only when"**
- Side A: `GATE:254`: "collects into `022C1740` the members whose status words `+0x64` or `+0x3C` carry `0x80000003` (KO, Stone, X-Zone) or whose field record bit 15 (`00377C20`) is set"
- Side B: `GATE:537-539`: "A member carrying a terminal status (`statusWord1|statusWord2 & 0x80000003`: KO, Stone, X-Zone) is kept only when `FieldData_GetActiveFieldRecordBit15` holds."
- Status: no favoured side. The 2026-09-25 section (GATE:510) does not say it corrects UQ-28. The two also name the group differently: "a party incapacitation scan" (GATE:254) vs "Libra" (GATE:541-542).
- page-text only - needs local check

**C-V38.** **Target-line node `+0xD44`: timer vs radian angle field**
- Side A: `GATE:225`: "`+0xD44` a timer bounded by the per-kind constants at `00916028`/`0091602C` with the kind byte from `00916010`"
- Side B: `GATE:252`: "both constants act on the SAME radian field, `node+0xD44`, as a floor and a minimum step … the field they act on is radian-valued"
- Status: no favoured side. Both are dated 2026-09-17 (FABLE).
- page-text only - needs local check

**C-V39.** **`0028CD80` operand: a 0x20-byte lane vs the `_7EA0` object**
- Side A: `GATE:254`: "then `0028CD80` and `0028CE90` on the two `0x20`-byte lanes at `+0x30` and `+0x50`: a two-lane rotating fade"
- Side B: `C-GATE:1646`: "`0028CD80` … `word[rcx+0x28]` bit 0 gates the update … `byte[+0x2A]` … `float[+0x20]` … `dword[+0x2C] += 0x10`" (offsets past a 0x20 lane). Compare `C-GATE:1690`: "`0028CE90` … `+0x14` bit `0` … `+0x13` ramps … `+0x10` accumulates", which uses different offsets for the same roles.
- Member tsv: `manager-sub-0209be80-7ea0-accesses.tsv` places `0028CD80` at `_7EA0` base disps 0x10/0x20/0x24/0x28. `manager-sub-7ea0e-ntry-accesses.tsv` (lanes +0x30 stride 0x20) has only `0028CE90`.
- Status: no favoured side.
- page-text only - needs local check

**C-V40.** **`0029FB50` reached through `0028BB50` by the 0x0020 group vs `0028BB50` has one caller in group 0x0004**
- Side A: `GATE:481`: "the fixed-width decimal digit writer the `0x0020`-group widget spawner reaches through `0028BB50`"
- Side B: `GATE:157-158`: "**`E8` = 1** (`0028C4D3`, the walk above), **`E9` = 0** … One caller, no address-taken reference." (the walk is group 0x0004's `0028C4C0`)
- Status: no favoured side.
- page-text only - needs local check

**C-V41.** **`00377C20` called "the one word this page is named for"**
- Side A: `GATE:401-402`: "**That getter is the one word this page is named for**, so the crossing is the AI layer reading the same gate as the fifteen subsystems"
- Side B: `GATE:283-284`: "`01E0C464` has **16 references in the entire image. All 16 are in `0028E290`, and all 16 are `test`.**"
- Status: no favoured side by a dated correction. Side B is confirmed by the dated pass at GATE:347. `00377C20` is `FieldData_GetActiveFieldRecordBit15`, not `01E0C464`.
- page-text only - needs local check

**C-V42.** **What writes the 23,224-byte hole: only the constructor memset vs also the 0x61F0 battle-menu clear**
- Side A: `C-GATE:1094-1095`: "23,224 bytes **never read and never individually written, and zero-initialised wholesale exactly once, at construction.**"; `C-GATE:1130`: "So on the extended sweep the constructor's `memset` remains the **only** bulk write reaching the hole."
- Side B: `C-GATE:711-719`: "> **RETRACTED 2026-09-19 (OPUS) — it does extend into it** … **a 0x61F0-byte clear of the handed-out object** … the hole at `+0xB244` is **inside it**"; `C-GATE:734-735`: "**`4d05cc7a0`'s bound — "the constructor's memset remains the ONLY bulk write reaching the hole" — is wrong by one.**"
- Status: favoured side B by "RETRACTED 2026-09-19 (OPUS)" (C-GATE:711). Side A is still unstruck at C-GATE:1094-1095 and C-GATE:1130.
- page-text only - needs local check

**C-V43.** **`_8FA0` size: 0x1130 vs 0x1110**
- Side A: `GATE:476` (struck) and `C-GATE:473` (struck) "`_8FA0` (`0x1130`)"; `C-GATE:612`: "| `_8FA0` | 4,400 |" (4,400 = 0x1130); `C-GATE:582`: "touch **sixteen offsets** across 4,400 bytes"; `C-GATE:600`: "103 offsets over 43,456 bytes" (the total uses 4,400)
- Side B: `C-GATE:502`: "**`_8FA0`'s size corrected `0x1130` → `0x1110`, 2026-09-21 (OPUS), closing `CON-124`.**"; the C-GATE:499 table row says `0x1110`
- Status: favoured side B by the 2026-09-21 correction. Still repeated unstruck as 4,400 at C-GATE:582, 612 and in the 43,456 total at C-GATE:600.
- page-text only - needs local check

**C-V44.** **Allocation site of the `0x8030` child block**
- Side A: `C-GATE:731`: "`00291750` allocates `0x8030` at `0029176F` and stores it at `00291779`"
- Side B: `C-GATE:1132-1133`: "`0029176A` allocates `0x8030` bytes and `00291779` stores that pointer"
- Status: no favoured side.
- page-text only - needs local check

**C-V45.** **`00226280` behaviour: AND over 28 slots vs best-fit search over 1024 entries (other 00 page)**
- Side A: `C-STOP:74-78`: "**SS-1 — The combined restriction is an AND over ALL TWENTY-EIGHT slots** … The loop walks `01FD4410` to `01FD46B0` in steps of `0x18` — **28 slots**"; `STOP:172-173`
- Side B: `TICK:1553-1557`: "the loop at `002262E4` walks a packed table rooted at `01FD4410` with `ebp = 0x3FF` as the element mask and `0x20000000000` as a validity bit … — a best-fit/free-slot search over a 1024-entry index space, not a linear lookup."
- Status: no favoured side by an explicit correction. C-STOP's dated pass (C-STOP:305-320) and EXP-191 support side A but do not mention TICK.
- page-text only - needs local check

**C-V46.** **Record B `+0x14`: flag argument stored vs zeroed at start**
- Side A: `STOP:94-95`: "The **flag** argument (stored at record B `+0x14`) changes the records of ids 4, 6 and 7 only."; `STOP:44`: "a flag byte `+0x14`"
- Side B: `C-STOP:242-243`: "**`+0x14` byte — zeroed** at start/reset in both records (`00225E30`/`00226003`/`00226008`)"
- Status: no favoured side.
- page-text only - needs local check

**C-V47.** **`00225CD0` labelled "start"**
- Side A: `C-STOP:210-211`: "start `00225CD0` and stop-sweep `00225EB0` both set it"
- Side B: `C-STOP:53`: "| cancel | `00225CD0` |"; `STOP:80`: "**Cancelling** — `00225CD0(id, fade)`"
- Status: no favoured side. C-STOP:211-212 then calls `00225CD0` the one that "**clears** the request's bitset bit", which is consistent with cancel.
- page-text only - needs local check

**C-V48.** **UI close path listed among "start-only" bodies**
- Side A: `C-STOP:233-235`: "Start-only bodies that return with dirty raised: `002273B0`, … `00252D90`, `002544C0`, `002630FD`, `00313EB1` (start-A)"
- Side B: `STOP:241-243`: "released by … the UI close path (`00252D90`, `002544C0`)"; `STOP:827`: "`002544C0` … a non-negative result tail-calls `00225CD0(result, -1)`"
- Status: no favoured side.
- page-text only - needs local check

**C-V49.** **System-stop flag word address: `0215F1DC` vs `0215F1D0` (same bits 0, 1, 9, 20)**
- Side A: `STOP:271`: "sets bits 0, 1, 9 and 20 of the system-stop flag word `0215F1DC`"; `STOP:483`: "`or dword[0215F1DC], 0x100203`"
- Side B: `STOP:832-834`: "`002E06B0` … clears bits 0, 1, 9 and 20 of dword `0215F1D0`" (likewise `002E2400`, `002E2440`)
- Status: no favoured side. These may be two different words written by different functions. The page does not say.
- page-text only - needs local check

**C-V50.** **`0035C7B0` on `022C83E8` bit 8: sets vs tests**
- Side A: `STOP:271`: "Its raiser `0035C7B0` … sets bit 8 of the request word `022C83E8`" (and `TICK:845` "sets `022C83E8` bit 8")
- Side B: `STOP:526-527`: "`0035C7B0` (~62 B) — `dword[022C83E8] & 0x100` test"; `STOP:794`: "`0035C7B0`'s `& 0x100` test"
- Status: no favoured side.
- page-text only - needs local check

**C-V51.** **Initial bit pattern of the enable word**
- Side A: `C-GATE:289`: "Bit 4 is therefore set (`0xFFFF` at ship)"
- Side B: `C-GATE:173`: "The word ships as `FF FF FF FF`"; `GATE:233`: "the word ships `0xFFFFFFFF`"
- Status: no favoured side (side B is repeated on more pages). The value matters under C-GATE:45's `uint32`.
- page-text only - needs local check

#### 3.1.4 Battle runtime mode ladder, diagnostics log, duplicated names, all-ones convention

**C-V52.** **Transition table `01EECFC0`: which column is which (summon and chocobo rows)**
- Side A: `MODE:350`: "| mode | same-mode (`commit = 0` / `≠ 0`) | leave (`commit = 0` / `≠ 0`) |" with `MODE:352`: "| 1 summon | the empty stub `0016D6A0` / `00313600` … | `00313730` … / `00313650` …" and `MODE:353`: "| 2 chocobo | `00304180` … / `00304060` — the mount | `00304400` — disarms and detaches the rider … / `00304140` …" (i.e. col 1 = `00313600` / `00304060`, col 2 = `00313730` / `00304400`)
- Side B: `MODE:364`: "| 1, 1 | `00313730` |" ; `MODE:365`: "| 1, 2 | `00313600` |" ; `MODE:368`: "| 2, 1 | `00304400` |" ; `MODE:369`: "| 2, 2 | `00304060` |" ; corroborated by `C-MODE:392-393`: "`00304060`/`00304140` — `call rax` slots 10/11 of the `01EECFC0` hook table" (slot 10 = row 2 col 2)
- Status: no favoured side (the 2026-09-14 binding table, MODE:357, does not say it overturns the column headers). MODE:350-353 unstruck.
- page-text only - needs local check

**C-V53.** **`00313650`: resets when bit 0 is set or when it is clear**
- Side A: `MODE:352`: "`00313650` — resets through `00313840` if bit 0 is still on"
- Side B: `MODE:366`: "`+0x5B04` bit 0 **clear** → tail `00313840`, set → `ret` (the doc table's "if bit 0 is still on" reads it the other way; `je` at `0031365E` jumps on clear)"
- Side C: `MODE:580`: "`00313650` sets bit 0 through `00313840` when it is clear (the summon reset, §2c);" — while `MODE:110` says "`00313840` (reset) clears"
- Status: favoured side B by `MODE:357` "*(2026-09-14 — NOCALLER-INSTALLERS: the matrix's five no-caller members bound.*" with the explicit note at MODE:366. Side A (MODE:352) still unstruck; MODE:580 contradicts both on what `00313840` does to bit 0.
- page-text only - needs local check

**C-V54.** **`00307200` / `00307240`: setters or getters**
- Side A: `MODE:121`: "00307200 (set bit 3 -> mode 5)  <- thunk 0037D110 <- 00351E50"; `MODE:122`: "00307240 (set bit 2 -> mode 4)  <- thunk 0037D120 <- 00351B40"; `C-MODE:57`: "| the four setters | `00307200` bit 3 · `00307240` bit 2 · `00303D90` bit 1 · `00313550` bit 0 |"
- Side B: `MODE:1050`: "Two plain `jmp` thunks into the `02EBF190 + 0x5B04` bit getters."; `MODE:1054`: "| `0037D110` | `00307200` | `dword[+0x5B04] >> 3 & 1` |"; `MODE:1055`: "| `0037D120` | `00307240` | `dword[+0x5B04] >> 2 & 1` |"
- Status: no favoured side (no dated correction either way; C-MODE:343-345 2026-09-26 executed "the bit-3/bit-2 setters (one write, none when equal)" without naming addresses). MODE:1050-1055 unstruck.
- page-text only - needs local check

**C-V55.** **`00313550` operates on which object**
- Side A: `MODE:1241-1242`: "`ecx` is compared against bit 0 of the `+0x5B04` dword on the `02EC4BA9` object"
- Side B: `C-MODE:71-72`: "`*(void **)0x02EBF190` | 8 | the `BattleSystemState` block" / "`state + 0x5B04` | 4 | **the mode flags word.**"; `MODE:110`: bit 0 getter/setter `003135E0`/`00313550` on the same word
- Status: no favoured side.
- page-text only - needs local check

**C-V56.** **Width and meaning of `state+0x5AE0`**
- Side A: `MODE:464`: "state + 0x5AE0              u32    chocobo flags: bit 0 timers armed, bit 1 turbo on, bits 2-3 turbo charges (3 per ride)"
- Side B: `C-MODE:74`: "| `state + 0x5AE0` | 8 | the special-sequence word; bit 1 and bits 2–3 are touched by the bit-1 setter |"
- Also (MODE cites it at MODE:310; outside 00, not audited): `11-Party/Battle-State-Block/the-battle-state-block-field-map.md:115`: "| `+0x5AE0` | 4 | **the event-party state word** of the mode ladder"
- Status: no favoured side. MODE:381-383 places "the global special-sequence state" at `022C2160`, not in the block.
- page-text only - needs local check

**C-V57.** **Persisted footprint: one mode word or two**
- Side A: `MODE:280-281`: "the persisted footprint is **`state+0x5AD0 .. +0x5AEF` (32 bytes) plus the mode word at `+0x5B04`**" (capture list MODE:272-277 has no `+0x5B08`; C-MODE:80 "writes it to `rec+0x28`")
- Side B: `MODE:375-377`: "The persisted footprint §"It survives area transitions" describes is therefore the chocobo's block plus the two mode words — a ride survives a zone change and a save."
- Status: no favoured side.
- page-text only - needs local check

**C-V58.** **Battle slot map base and shape (`+0x5A58` vs `+0x5A5A`)**
- Side A: `MODE:536`: "**battle slot map** ([the battle-state-block field map](…) `+0x5A58`, four 18-byte entries)"
- Side B: `C-MODE:149`: "(~~`+0x5A58`, four 18-byte entries~~ the four mapping-class tables at `+0x5A5A`/`+0x5A6C`/`+0x5A7E`/`+0x5A90`, nine u16 each, classes 1–4 of `0031B9F0`; entries 0, 1, 3 below are classes 1, 2, 4 — corrected 2026-09-14)"
- Side C (other 00 page): `HUBS:168`: "then one of five byte arrays of the block at `+0x5A58`…`+0x5A90`"
- Also `C-MODE:400-401`: "returns `byte[state + slot*2 + 0x5A90]` (`0031C2C7`) — the class-4 mapped row" (byte read at a 2-byte stride, vs "nine u16").
- Status: favoured side B by `C-MODE:149` "corrected 2026-09-14" (outside 00, not audited, the cited field map at line 91 carries the same 2026-09-14 correction). MODE:536 still repeats `+0x5A58` four 18-byte entries unstruck; HUBS:168 "five byte arrays" unstruck.
- page-text only - needs local check

**C-V59.** **`002E73C0`: tail-calls `003E6AA0` when `+0x284` is non-zero or zero**
- Side A: `C-MODE:490-491`: "002E73F3  cmp  dword [rcx + 0x284], 0" / "002E73FA  jne  0x3E6AA0                  ; TAIL CALL"; `C-MODE:498-499`: "it is reached only when `[record + 0x284]` is non-zero"; `MODE:555`: "when its `+0x284` is non-zero, calls `003E6AA0(record, n)`"
- Side B: `C-MODE:655-656`: "only when the record's `[+0x284]` word is zero does it tail `003E6AA0`" (also "word" vs "dword")
- Status: no favoured side (C-MODE:650 is dated 2026-09-18, later than RMD-3's 2026-09-15, but does not say it corrects it).
- page-text only - needs local check

**C-V60.** **Ladder callers: the six direct wrapper callers listed as callers of `0030D9A0`, and outside the stated address range**
- Side A: `C-MODE:112-115`: "**Callers of the ladder:** `PartyControl_RecomputeSuppressionFromLeaderBattleState` (`0023B040`), `InputGameplay_ArbitrateDigitalInputAndModalState` (`00253C70`), `BattleUnit_ApplyUnitDefinition` (`0023A570`), … `00235EA0`, `00320230`, `0035BC50`, `00313DB0` (inline), and the two mode getters."
- Side B: `MODE:194-203` (those six are the direct callers of the wrapper `00303EC0`, not of `0030D9A0`); `C-MODE:444-445`: "The ladder `0030D9A0` has **20 call sites, all in the `0x2FF…0x326` battle cluster**" (excludes `0023B040`/`0023A570`/`00235EA0`/`00253C70`/`0035BC50`)
- Status: no favoured side.
- page-text only - needs local check

**C-V61.** **Function extents vs the page's own interior citations**
- Side A: `MODE:1006`: "`00303F00` (~27 B)" (repeated MODE:1023); Side B: `MODE:316-319` cite `00303F59`, `00303F98`–`00303FC8`, `00303FED`–`00303FFD`, `0030400A`–`0030403B` inside the turbo handler `00303F00`.
- Side A: `MODE:1012`: "`00304060` (~11 B) — `0031B8C0(3)` non-null gate"; Side B: `MODE:315` "the mount handler starts countdown channel 1 … (`003040C6`–`003040E4`)", `MODE:317` "set at the end of the mount handler `00304131`".
- Side A (other 00 page): `TICK:1493`: "`00304440` (~27 B) — `byte[02EBF190 + 0x5AE0] & 1` gate"; Side B: `MODE:315` cites `00304458`–`00304468`, `00304474`–`00304485`, `003044A6`–`003044E7`, `MODE:318` `003044EC`–`00304584` in the frame handler.
- Side A: `MODE:988`: "`00306760` `BattleAction_UpdateSpecialPresentationSequence` (293 B)"; Side B: `MODE:334` "at `00306931`–`003069F3`", `MODE:339-341` "`003069F8`–`00306A31` … `00306A6D`–`00306A87`"; `ONES:232-238` `00306877`–`00306891`; (outside 00, not audited) battle-state-block field map:160 "(`00306760`, 911 B)".
- Status: no favoured side for any of the four.
- page-text only - needs local check

**C-V62.** **`022C1F50` accumulated-HP table entry layout**
- Side A: `MODE:391`: "the accumulated-HP table: 32 entries of 16 bytes (`+8` the target unit, `+0x10` the HP delta), the source at `+0`"
- Side B: same line — a field at `+0x10` lies outside a 16-byte entry.
- Status: no favoured side (internal).
- page-text only - needs local check

**C-V63.** **Who writes `02EAED3C`**
- Side A: `LOG:281-282`: "It is the module's `_tls_index`, written by the loader — **not a logging index**."
- Side B (other 00 page): `APP:772`: "| `00189CE0` | `00189D4C` | `call _Init_thread_header` — TLS-init bracket around a `0018A620` call run; also writes `02EAED3C` |"
- Status: no favoured side.
- page-text only - needs local check

**C-V64.** **Who publishes the sink pointer `02CB6150`**
- Side A: `LOG:201`: "the second magic static `005CD9C0` publishes that object's address as the sink pointer `02CB6150`"
- Side B: `LOG:269-270`: "005CDB75  call 0x5CDA30                   ; build it" / "005CDB81  mov  [rip + 0x26E85C8], rax     ; -> 02CB6150" (the log call itself stores `005CDA30`'s result); `LOG:285-286`: "`005CD9C0` … guard `02CB6158`, `lea rax, [02CB6150]`, return"
- Status: no favoured side.
- page-text only - needs local check

**C-V65.** **The log call's "gate" and argument order (corrected; still echoed)**
- Side A: `LOG:132-136`: "/* the gate, and it is per-thread */ … if (*(int32_t *)0x02CB6158 > lvl) … return; /* dropped */"; `LOG:129-130`: "`__stdio_common_vsprintf(…, buf, /* size */ 0x4000, fmt, /* locale */ (void *)-1, ap);`"
- Side B: `LOG:275-276`: "**Both branches reach `005CDB31`.** … **No message is ever dropped**"; `LOG:319-320`: "**`r9 = -1` is `count`, i.e. `_TRUNCATE`**, and the locale is the **`0`** … §5 reads the `-1` as the locale and omits `count`."
- Status: favoured side B by `LOG:117`: "**⚠ The whole "gate" reading below is withdrawn (2026-09-13, §9).**" Still repeated: `LOG:236` (2026-09-14 note) "the level `cmp` is at `005CDB29`"; `APP:897` "`__stdio_common_vsprintf` into a `0x4000` stack buffer" (import is `…vsnprintf_s`, LOG:208).
- page-text only - needs local check

#### 3.1.5 Encoded-id space, class registry, query record, basis helpers, ABI recovery

**C-V66.** **Who touches the descriptor table: 15 functions vs 28**
- Side A: `EID:291-297`: "A whole-image census of the table base `01EEBCC0` finds fifteen functions: … — the only code that touches the descriptors at all."
- Side B: `C-EID:268-270`: "49 rip-relative references into the table sit in 28 functions: both packed handlers, both bitset handlers, the query dispatchers and the equipment snapshot pair … among them."
- Also within EID: `EID:163-164`: "`InventoryEquipment_SnapshotAndClearTemporaryState` (`0030FBE0`) walks it by the descriptors' counts (`01EEBCFC` = class 5's `+0x3C`, `01EEBD28` = class 6's `+0x10`" — not in the fifteen. Other 00 page: `TICK:2217`: "`00308DE0` (149 B) is a world-tick body - `003008A0` single call plus `01EEBD54`/`01EEBF0C`."
- Status: favoured side B by "*Corrected 2026-09-30 (OPUS, on FABLE's and SWE2-AUDIT-SEM's findings; `falsify_encoded_id.py` E10 / E11):*" (C-EID:267-268) and E10 "**BROKEN**" (C-EID:400). EID:736 keeps "15 functions" valid only for the base address. EID:296-297 "the only code that touches the descriptors at all" is still unstruck.
- page-text only - needs local check

**C-V67.** **00309EC0 dispatches to query vs "mutate or query"**
- Side A: `CLS:252-253`: "the mode dispatcher `00309EC0`, which routes by nibble to a record's mutate or query handler"
- Side B: `C-EID:345`: "`qword[+0x50]` non-null tail-dispatches `jmp rax` … **as `handler(id, 0)`**"; `CLS:631-633`: "`jmp qword[row+0x50]` … tail-dispatches the row's mode-0 handler"
- Status: favoured side B by "*Corrected 2026-09-26 (OPUS, contract owner).*" (C-EID:347) with argument capture "at both query handlers" (C-EID:351). CLS:252 (2026-09-30 section) still says "mutate or query".
- page-text only - needs local check

**C-V68.** **00309EC0 argument order**
- Side A: struck "~~with `(0, cx)`~~" (C-EID:345)
- Side B: `CLS:632-633`: "tail-dispatches the row's mode-0 handler with `(edx=0, ecx=cx)`"; `C-EID:345` "**as `handler(id, 0)`**"
- Status: agree after correction (C-EID:347, dated 2026-09-26). No live conflict; recorded for completeness.

**C-V69.** **00309EC0 out-of-range return**
- Side A: `CLS:633`: "Out-of-range ids return 0."
- Side B: `EID:132-134`: "return −1 for `0xFFFF`, −1 for a nibble above `0xE`, index the record by the nibble, bound `id & 0xFFF` by `+0x3C`, and tail-call `+0x50` … **a class without a query handler answers 0**" — the out-of-range-index result is not stated; `C-EID:141`: "`FFFF` and invalid nibble are rejected separately."
- Status: no favoured side (not a direct contradiction; the index-out-of-range value is stated only at CLS:633).
- page-text only - needs local check

**C-V70.** **00309440 calls the validator vs leaf**
- Side A: `CLS:211-212`: "`00322C50` itself is Gameplay-owned — called by `0031B9F0`/`0031C5D0` and called *from* `00301AD0`, `00309440`, `00323910`, `00327CB0`"
- Side B: `CLS:248`: "the validator and `00309440` are leaf code, EXP-143"; body EID:718-726 / CLS:466-472 has no call.
- Status: no favoured side (no dated correction), but both instruction listings show no call.
- page-text only - needs local check

**C-V71.** **Function extents in "exclusive subtree" sections**
- Side A: `EID:804`: "`0031C5D0` (~105 B) — six-register body"; `EID:793`: "`0030B270` (`BattleIdClassD_RefreshPrerequisiteRuntimeFlags`, ~105 B)"
- Side B: `EID:740`: "`0031C5D0` is 8,136 bytes"; `CLS:173`: "`FUN_0031C5D0` (8,136 B)"
- Status: no favoured side by dated correction; ~105 B is also given for two unrelated functions.
- page-text only - needs local check

**C-V72.** **"Exclusive" subtree members that have other callers**
- Side A: `CLS:601-609`: "The `003008A0` exclusive subtree — 1 member bound … `00309F30`"
- Side B: `CLS:574`: "page-cited `Equipment_EvaluateCandidateLoadoutAndBuildDerivedStats` (0030A4E0) … call … `Inventory_QueryEncodedItemStateByClass` (00309F30)"
- Status: no favoured side.
- page-text only - needs local check

**C-V73.** **Validator class mapping (other 00 page)**
- Side A: `NBR:329`: "every class from 1 to 32 resolves to one registry slot (four slots serve more than one class: `02EBF110` classes 22..24, `02EBF068` classes 15, 30, 31, `02EBF138` classes 19, 20, `02EBF038` classes 25, 32), class 13 concatenates three slots"
- Side B: `CLS:91-92`/`CLS:98`: class 13 "four counts summed", class 19 "*range `0xE000`–`0xEFFE`*", class 22 "*literal bound 4*", class 23 "*literal bound 9*"; `CLS:519-520`: "`00322FA6  mov ecx, 4` … `00322FAF  mov ecx, 9`"
- Status: favoured side B by "(corrected 2026-09-13)" (CLS:113), "**Added 2026-09-13**" (CLS:119), "Falsification pass 1 — 2026-09-30 (OPUS)" E4 "Arm `00322F63` loads `0xE000` and `0xEFFF`" (C-EID:394), and "**CLOSED 2026-09-23**" four-slot sum (C-EID:250-255). NBR:329 (dated 2026-09-17) still repeats the old mapping unstruck.
- page-text only - needs local check

**C-V74.** **Class 16 census cites the class-15 arm address**
- Side A: `EID:355-356`: "a whole-image rip-relative census of `02EBF060` finds only the validator (`00322EBB`)"
- Side B: `CLS:104`: "`00322EBB` serves 15 / 30 / 31"; `CLS:431`: "`00322EBB` → 15/30/31"
- Status: no favoured side (EID's site may be the class-16 arm next to it; not stated).
- page-text only - needs local check

**C-V75.** **002F9920 bucket table address**
- Side A: `EID:936-937`: "buckets the id into a 28-entry pointer table at `02FDA3D80`" (nine hex digits)
- Side B: `C-EID:358`: "`002F9920` (314 B) is the bucketed sub-table search over `02EC3D80`/`02F973C0`"; `C-EID:126`: "Description ready/root arrays | `02EC3D80`, `02F973C0`"
- Status: no favoured side; side A is malformed.
- page-text only - needs local check

**C-V76.** **Empty-record default of the text resolvers (other 00 page)**
- Side A: `HUBS:560-561`: "Returns `01C8B638` (a static empty record) on any miss" (002F9860)
- Side B: `EID:937`: "a null entry returns the `01CEB638` default" (002F9920); `HUBS:837-838` "answers the `01CEB638` empty row"
- Status: no favoured side (different functions; differ by one digit).
- page-text only - needs local check

**C-V77.** **Slot-descriptor header layout**
- Side A: `EID:1152`: "`word[+6]` is the row count … `0020E600(dword[+8])` resolves the table base, `word[+4]` strides `ecx` rows in" (shop table `02EBF158`)
- Side B: `CLS:84`: "compare the id against the count at its `+4`"; `C-EID:278`: "`0020E600(dword [table directory + 0xC])`"; `C-EID:358`: "`word[+8]*i + 0020E600(+0xC)`"
- Status: no favoured side (may be two formats; not stated).
- page-text only - needs local check

**C-V78.** **Jump-table address given as RVA**
- Side A: `CLS:648-650`: "`003241D0()` minus `0x15` indexes a 9-entry jump table at `002038E4`"
- Side B: page convention `CLS:80`: "`jump table at 00323054`" from `0x120000 + 0x203054`; `002038E4` + `0x120000` = `003238E4`.
- Status: no favoured side.
- page-text only - needs local check

**C-V79.** **00323890 argument**
- Side A: `EID:540-541`: "Classes 25 and 32 store `00323890(row+5)` at `+0x23` … the result of `003241D0` minus `0x15`"
- Side B: `CLS:648`: "`00323890` (83 B) is the class-map decoder: `003241D0()` minus `0x15`"
- Status: no favoured side (whether row+5 reaches `003241D0` is not stated).
- page-text only - needs local check

**C-V80.** **BASIS translation slots +0x0C/+0x1C/+0x2C vs +0x14/+0x24/+0x34**
- Side A: `BASIS:130-131`: "those three are written **individually into `+0x0C`, `+0x1C` and `+0x2C`** — **the fourth slot of each of the three rows**"
- Side B: `BASIS:62-64`/`BASIS:67`: fourth column at "`+0x14`, `+0x24` and `+0x34`"
- Status: no favoured side; agrees only if `00189130`'s destination is the structure `+0x08`, which is not stated.
- page-text only - needs local check

**C-V81.** **BASIS scratch offsets**
- Side A: `BASIS:75-77`: "`0062DE6E  mov dword ptr [rcx + 0x44], eax ; the scratch fourth slots are zeroed` … `+0x54` … `+0x64`"
- Side B: `BASIS:89-90`: "`movups xmm6, xmmword ptr [rcx + 0x38] ; the saved fourth column` … `[rcx + 0x48] ; column A`"; `BASIS:110`: "both use `+0x48 … +0x70` as scratch" (row fourths would be `+0x54/+0x64/+0x74`; `+0x44` would be inside the saved column).
- Status: no favoured side.
- page-text only - needs local check

**C-V82.** **00300BA0 "shared query" vs modify entry**
- Side A: `EID:1036-1037`: "falls into `003008A0` - the two-ones-shim into the shared query."
- Side B: `EID:279-280`: "`Inventory_ModifyEncodedItemAndUpdateDiscoveryState` (`003008A0` …) is the one entry that changes what the party owns"
- Status: no favoured side (label; the shim also fixes `absolute = 1`, `channel = 1`, which no other line confirms).
- page-text only - needs local check

#### 3.1.6 Shared transform workbench (EE/VU0 register bank, save/restore, primitives)

**C-V83.** **vf00 writer count (2 vs 3)**
- Side A: `WB:365`: "**It has exactly two writers and they write the same thing.**"; `WB:381-382`: "the two-writer count is exact rather than merely unseen."
- Side B: `EEVU:70`: "Exactly **3 writers**, all storing (0, 0, 0, 1)."; `C-PRIM:398-405` (three: `0036D990`, `0036D9E0`, `0036DD80`); `PRIM:87` "all three of its writers (`0036D9A8`, `0036D9E8`, `0036DD87`)"; WB itself `WB:628-631` (`0036DD80` … `movups [01EF93F0],xmm0`).
- Status: no favoured side by an explicit strike of WB:365; C-PRIM:418-420 (2026-09-19) explains that a sweep "addressed to" the cell "found two, missing `0036DD80` entirely". WB:365/381 still unstruck.
- page-text only - needs local check

**C-V84.** **What `022D8F10` is: `$zero` vs caller-filled operand row / table**
- Side A: `EEVU:64`: "**0 writers, 44 readers.** … which is `bne rX, $zero`."; `EEVU:89`: "GPR[0]  $zero           never written"
- Side B: `SAVE:162`: "`022D8F10` is an *operand the caller must have left there*"; `SAVE:292`: "no rip-relative store writes that row, so the callers fill it through pointers"; `PRIM:1502`: "`word[r9]` keys the `022D8F10` table"; `PRIM:610`: "loads the `022D8F10` staging row"
- Status: no favoured side. If A holds, the modulate's row term (SAVE:188) and UQ-42's ceiling byte are always zero. (Outside 00, not audited: `02-Resource-And-Asset-Pipeline/Authored-Expressions/how-an-authored-number-gets-its-randomness.md:687` says `003D2B60` is "writing `022D8F10`"; SAVE:287 cites that page.)
- page-text only - needs local check

**C-V85.** **Rows protected by Save: only `022D8F30`/`022D8F90` vs also `022D8F40`**
- Side A: `SAVE:146-147`: "**`022D8F30` and `022D8F90` are the only two addresses that anything in this image bothers to protect**"; `WB:281-282`: "`022D8F30` (5 callers) or `022D8F90` (3), with one saving both"
- Side B: `C-SAVE:341`: "one passes `ecx = 2` (`004300F9`, saving rows `022D8F30`+`022D8F40`)"
- Status: no favoured side (C-SAVE's 2026-09-23 "CLOSED" does not strike SAVE §5 or WB:282).
- page-text only - needs local check

**C-V86.** **`0044BAC0`'s save window: one call (`sqrtf`) vs `0044B8C0` inside it**
- Side A: `SAVE:296`: "there is **no branch and exactly one call - `00861F14 sqrtf`**"; `C-SAVE:175`; `C-SAVE:428` (1 call)
- Side B: `SAVE:381`: "`0044B8C0` (160 B) is the matrix-scalar helper `0044BAC0` runs inside its save window"
- Status: no favoured side.
- page-text only - needs local check

**C-V87.** **How `0044BAC0` reaches the other users**
- Side A: `C-SAVE:167-168`: "The ninth, `0044BAC0`, can — and only through `0026EE00`"
- Side B: `SAVE:296`: "`0044BAC0` (3,461 B) reaches `0026EE00`, `002F1D90`, `003AFDD0`, `003D8E50`, `0042FDB0` and `00431D30`"; `C-SAVE:413`: "`0044BAC0` transitively reaches **six of the other eight**"
- Status: no favoured side (C-SAVE §15a dated 2026-09-12 adds the six but does not strike line 168).
- page-text only - needs local check

**C-V88.** **Save capacity: "at most two rows" vs any count**
- Side A: `C-SAVE:342-343`: "a single save window can protect at most two rows — a whole matrix is unreachable through this convention."
- Side B: `C-SAVE:62-63`: "A caller saving a 64-byte matrix must pass four pointers"; `C-SAVE:261` (executed at depths "0, 1, 2, 3, 4, 5 and 8"); `C-SAVE:470`
- Status: no favoured side (within one page).
- page-text only - needs local check

**C-V89.** **Scope of `0036D9E0`'s clear: "whole area" vs `022D91B0`–`022D9428`**
- Side A: `WB:253`: "`0036D9E0` ── clears the whole area, reads nothing"; `C-WB:141`: "`0036D9E0` clears it wholesale"; `C-SAVE:199-201` "the wholesale-clear hazard stays: clearing the region between `00502280`'s store and `00501820`'s read would corrupt the parameter"
- Side B: `WB:230`: "`for (row = 022D91B0; row < 022D9428; row += 16)`"; `WB:391`: "80 slot writes `022D91B0`–`022D9428`" (excludes `022D8F00`–`022D91AF`, including `022D8F0C`, the GPRs and ACC)
- Status: no favoured side.
- page-text only - needs local check

**C-V90.** **UQ-38 bracket: 41 vs 31 "C by both instruments"**
- Side A: `EEVU:262`: "The bracket stands (47 whole-shaped, 41 C, 95 undecided)."
- Side B: `EEVU:261`: "*(corrected 2026-09-28, FABLE … both instruments agree on C+fragments for **31** members…)*"; `EEVU:4` "static bracket 47 / 31 / 95"; `EEVU:259`
- Status: favoured B by `EEVU:261` "~~the 41 both instruments call C+fragments are settled that way~~ *(corrected 2026-09-28 …)*"; TSV agrees (31). "41 C" still unstruck at EEVU:262.
- page-text only - needs local check

**C-V91.** **Composer stack staging offsets**
- Side A: `PRIM:131`: "(`[rsp+0x40]` and `[rsp+0x80]`)"; `C-PRIM:88`
- Side B: `C-PRIM:319`: "**§15a: the staged offsets are `[rsp+0x40]`–`+0x70` and `[rsp]`–`+0x30` in the current body; the row's `+0x80` does not appear**"
- Status: favoured B by the dated falsification pass `C-PRIM:331` "## 15a. Falsification pass 1 — 2026-09-12 (OPUS)"; A still unstruck at PRIM:131, C-PRIM:88.
- page-text only - needs local check

**C-V92.** **`00398F90` at title screen: not running vs withdrawn**
- Side A: `C-PRIM:199`: "**So `00398F90` is not running at the title screen**"
- Side B: `PRIM:180`: "~~**So `00398F90` is not running at the title screen**~~ — **WITHDRAWN 2026-09-21 (ASTRA …)**"
- Status: favoured B by PRIM:180; still unstruck at C-PRIM:199.
- page-text only - needs local check

**C-V93.** **`00398F94` loads ACC vs row 1**
- Side A: `PRIM:625`: "`00398F94` is `movups xmm0, [rip+...]` loading the ACC row"
- Side B: `PRIM:389`: "`00398F94 movups xmm0, [rip + 0x1f40215]` resolves to **`022D91B0`**" (ACC is `022D91A0`, EEVU:95)
- Status: no favoured side.
- page-text only - needs local check

**C-V94.** **What `003970A0` reads: rows 1–4 vs "vector-unit-5 quadrant"**
- Side A: `EEVU:71`: "is rows 1–4"; `PRIM:30`: "VU0 vector rows 1–4"
- Side B: `PRIM:695-696`: "a 64-byte snapshot of the vector-unit-5 quadrant into caller storage"
- Status: no favoured side.
- page-text only - needs local check

**C-V95.** **Sine table address `01F404E0` vs `01F004E0`**
- Side A: `PRIM:729`: "indices into the sine table `r8 = 01F404E0`"
- Side B: `PRIM:812`: "`r8 = [01F004E0]` LUT base"; `PRIM:893`, `PRIM:913`, `PRIM:1570`, `PRIM:1654`; other 00 page `TICK:1046`: "**`01F004E0` is a 32,768-entry sine table**"
- Status: no favoured side.
- page-text only - needs local check

**C-V96.** **`022D9130`: CLIP flag word vs "staging bank"**
- Side A: `EEVU:67`: "`0025A8E0`: `shl eax, 6` … That is `VCLIP`."; `EEVU:93`
- Side B: `WB:589`: "bumps the `022D9130` staging bank"; `WB:593-594`: "`0025A8E0`'s `022D9130` cells are the same staging bank the `00433830` blend kernel consumes."
- Status: no favoured side.
- page-text only - needs local check

**C-V97.** **Who prints the emulation banner (`00908D80`)**
- Side A: `EEVU:74`: "`0036D990` stores vf00 and prints … the completion line, through `0017D280`"; `BOOT:403` "`0036D990` (`00908D68`/`80`)"
- Side B: other 00 page `APP:1661-1673`: "`0022CB90` (138 B) … then two `0017D280` report calls on the `00908D68` / `00908D80` strings"
- Status: no favoured side.
- page-text only - needs local check

**C-V98.** **Banner string text**
- Side A: `EEVU:38`: "`"PS2 Assembly emulation initilization completed! "`"
- Side B: `WB:368`: "`"PS2 Assembly emulation initilization completed! *** \n"`"
- Status: no favoured side.
- page-text only - needs local check

**C-V99.** **Save `lea` instruction addresses**
- Side A: `SAVE:66-67`: "`0036D953  lea  r9, [02EC0800]`" / "`0036D95A  lea  r8, [02EC0A00]`"
- Side B: `C-SAVE:353-354`: "values array `lea`'d at `0036D954` … pointers `lea`'d at `0036D95B`"
- Status: no favoured side.
- page-text only - needs local check

**C-V100.** **`022D94B0`/`B4`: pointers vs record table**
- Side A: `WB:222-223`: "`022D94B0   void*` … `022D94B4   void*`"; `WB:144`, `WB:207`, `WB:394`, `WB:523`
- Side B: `WB:315`: "**BQ-17 ANSWERED 2026-09-12 (FABLE): not two pointers — the base of a 32-entry table of 24-byte records**"; `C-WB:113-116` "*Corrected 2026-09-23 …*"
- Status: favoured B by WB:315 / C-WB:113; A unstruck at WB:144, 207, 222-223, 394, 523.
- page-text only - needs local check

**C-V101.** **Call sites "156" vs 231**
- Side A: `PRIM:290` "the 156 call sites around them are not"; `PRIM:352` "156 call sites were counted"; `C-PRIM:379` "§14's 156 call sites"
- Side B: `PRIM:55`: "(~~156 call sites~~ — 156 is the *caller* sum; the **sites** are **231**, 129 and 102; corrected 2026-09-13)"; `C-PRIM:283`
- Status: favoured B by PRIM:55; A unstruck at PRIM:290, PRIM:352, C-PRIM:379.
- page-text only - needs local check

**C-V102.** **`0039AF70` sites and source (232 / always `02AEEA20`)**
- Side A: `PRIM:309-310` (struck) "`0039AF70` (232 raw call sites) always copies **`02AEEA20`**"
- Side B: `PRIM:319-320` "**Corrected 2026-09-13** … `0039AF70` does **not** always copy `02AEEA20` … **116 unique call sites**"
- Status: favoured B by PRIM:319; not repeated unstruck in the group (PRIM:314 "the 232 sites" is still unstruck in the same paragraph).
- page-text only - needs local check

**C-V103.** **`003977B0` product order**
- Side A: `PRIM:807` (struck) "`M[rcx] = M[rcx] · M[rdx]`"
- Side B: `PRIM:807` "*Corrected 2026-09-27 …*: in row-major storage the result is `M[rcx] = M[rdx] · M[rcx]`"
- Status: favoured B; not repeated unstruck; heading "post-multiply" (PRIM:805) kept, with the 2026-09-28 note on convention.
- page-text only - needs local check

#### 3.1.7 Object model (RTTI and the vtable method index)

**C-V104.** **Distinct virtual-method count 6,886 vs 6,883**
- Side A: `VTIDX:61`: "**2,286 vtables across 2,248 classes, holding 6,886 distinct method addresses**"; `VTIDX:78`: "| distinct method addresses | **6,886** |"
- Side B: `RTTI:372`: "**6,883 is correct.** Section 6. **AS-7.**"; `RTTI:489`: "**The correct count is 6,883**"; also `VTIDX:2572`: "| **in a vtable** — what RTTI can name | **6,883** |"
- Status: favoured side B by `RTTI:464` "## 6. Falsification pass 2026-09-02 (second) - AS-7 settled" (same date as VTIDX's recovery, VTIDX:28-29; VTIDX:183 cites RTTI §§13–14 so VTIDX postdates it). Side A still repeated unstruck at VTIDX:61 and VTIDX:78; VTIDX contradicts itself (VTIDX:2572/2655).
- page-text only - needs local check

**C-V105.** **Unambiguously-owned set: 4,275 (includes the 3 AS-7 non-pointers) vs 4,272**
- Side A: `VTIDX:30`: "**4,275 function addresses, each tied to exactly one C++ class and vtable slot.**"; the appendix lists `00444F4C` (`PLOD::PUtilityLOD` slot 3, VTIDX:251), `006C6543` (slot 16, VTIDX:1238), `00755F6D` (slot 11, VTIDX:1362); `VTIDX:2541`: "**4,275 admitted, 4,275 published, 0 missing, 0 extra**" (re-derived from `methods.tsv`)
- Side B: `RTTI:95`: "| exactly one class | **4,272 (62.1 %)** |"; `RTTI:888`: "**they are inline ASCII strings, not pointers** … `vtable_map.py` requires a known function *entry* and rejects them"; `RTTI:476-478`: the three are mid-function (`FUN_00444340` + 0xC0C etc.)
- Status: favoured side B by `RTTI:464`/`RTTI:489` (dated falsification pass 2026-09-02, "A vtable slot never points mid-function", RTTI:481). 4,275 − 3 = 4,272 and 2,611 + 4,272 = 6,883. VTIDX repeats 4,275 unstruck (VTIDX:2, 30, 42, 79, 92, 2536, 2580, 2671) and README:33. A port keying `(class, slot)` from VTIDX would install three ASCII constants as methods.
- page-text only - needs local check

**C-V106.** **`0016D6A0` folding scale: three tables vs 1,291 classes**
- Side A: `RTTI:103-104`: "(`0016D6A0`, a bare `ret 0`, is shared by three unrelated tables)"
- Side B: `VTIDX:101`: "0016D6A0          3 B   in 1,291 classes   <- _guard_check_icall, a `ret` placeholder"
- Status: no favoured side. Side A unstruck.
- page-text only - needs local check

**C-V107.** **rtti_recover.py vtable count before the fix: 2,286 vs 2,284**
- Side A: `RTTI:39-40`: "**Both find exactly 2,286 vtables**"; `RTTI:330`: "| vtables | **2,286** | **2,286** |"; `RTTI:787-792`: "`classes.tsv`'s `vtables` column **sums to 2,286** … rtti_recover.py   2,286 vtables  ->  2,133 classes"
- Side B: `RTTI:864`: "vtables                  2,284        2,286          2,286"; `RTTI:853-854`: "both were silently dropped. That is the missing 2 of 2,286 vtables."
- Status: no favoured side (§14 undated). Side A repeated unstruck in the page banner (RTTI:39).
- page-text only - needs local check

**C-V108.** **vtable_map.py row/slot count: 25,794 vs 25,798 (gap 191 vs 195)**
- Side A: `RTTI:490-491`: "25,794 named slots here against 25,603 there, 191 apart"; `RTTI:569`: "| (address, class, slot) triples | 25,603 | 25,794 |"
- Side B: `RTTI:77`: "| vtable slots | 25,798 |"; `RTTI:712`: "`vtable_map.py` emits **25,798** rows"; `RTTI:865`; `VTIDX:184-185`: "differing by 1 row out of 25,798"
- Status: no favoured side.
- page-text only - needs local check

**C-V109.** **Cause of the method-table gap: vtable_map.py demangler (AS-8) vs rtti_recover.py demangler**
- Side A: `RTTI:373-375`: "**ANSWERED** - a **naming** difference … This tool's demangler doubles the outer namespace on template classes."; `RTTI:587`: "**AS-8 closed - no data defect, a cosmetic defect in this pass's own tool.**"
- Side B: `RTTI:712-714`: "The gap was blamed on the demangler defect. **It is not caused by that** … the old splitter was **injective**"; `RTTI:797-800`: "`rtti_recover.py`'s demangler **discards template arguments**"
- Status: no favoured side (§§12–14 undated). AS-8 answer still unstruck at RTTI:373-375 and RTTI:571-572 ("The 191 extra triples are entirely **class-name strings**").
- page-text only - needs local check

**C-V110.** **`00385F60` extent: ~144 B vs contains `003863D0` (2,302 B)**
- Side A: `RTTI:1009`: "`00385F60` (`BattleFormula_ResolveTargetResult`, ~144 B)"
- Side B: `RTTI:683`: "`003859FF` in `00385680` alongside `003863D0` in `00385F60`" (0x470 bytes past entry); `08-Combat-Formula/Steal/the-steal-roll.md:149`: "| `00385F60` | 2,302 B |" (outside 00, cited via RTTI's step-table link, not audited)
- Status: no favoured side.
- page-text only - needs local check

**C-V111.** **Slot numbers in VTIDX follow-up tables vs VTIDX appendix (5 roots)**
- Side A (follow-up tables): `VTIDX:3225` `0062FB30` "(10)"; `VTIDX:3227` `006342B0` "`PClassDescriptorDynamic` (0)"; `VTIDX:3229` `006421B0` "(0)"; `VTIDX:3243` `00643530` "(0)"; `VTIDX:3255` `00680D80` "(0)"
- Side B (appendix): `VTIDX:1448` `0062FB30` slot 14; `VTIDX:1478` `006342B0` slot 7; `VTIDX:1667` `006421B0` slot 10; `VTIDX:1707` `00643530` slot 10; `VTIDX:562` `00680D80` slot 10
- Status: no favoured side (appendix is the attacked set, VTIDX:2543 "0 mismatches", but that attack predates the follow-up tables). Script check of all `root | class (slot)` rows in VTIDX:2456-5219 found only these 5 mismatches.
- page-text only - needs local check

**C-V112.** **Class attribution in update sections taken from the neighbouring table column**
- Side A: `VTIDX:3399`: "`001F3740` (355 B) is the `RenderSSSObj`/`btSphereShape` vtable row body"; `VTIDX:3407`: "`001F2A20` (323 B) is the `CopyBufferObj`/`btInternalTriangleIndexCallback` vtable row body"; `VTIDX:2865`: "`00215320` — the appendix's `CharacterOrderedObject` slot-1 method (`0084AAC0`)"
- Side B: `VTIDX:2351`: `001F3740` | `RenderSSSObj` | 1 and `00837F00` | `btSphereShape` (second triple); `VTIDX:2326`: `001F2A20` | `CopyBufferObj` | 1 and `00835FC0` | `btInternalTriangleIndexCallback`; `VTIDX:2404`: `00215320` | `CharacterOrderedObject` | 1 and `0084AAC0` | `btTriangleConvexcastCallback` | 0
- Status: no favoured side; the Bullet names and `0084AAC0` belong to the other triple on the same appendix row.
- page-text only - needs local check

**C-V113.** **GameApplication has / lacks a deleting destructor**
- Side A: `VTIDX:2468`: "NEITHER   30      no deleting destructor at all"; `VTIDX:2505`: "The remainder of `NEITHER`: `GameApplication` (never deleted — see [the application root]…)"
- Side B: `APP:129`: "### The object is exactly `0x1140` bytes, and slot 0 says so"; `APP:361`: "| **`GameApplication` has no deleting destructor** | slot 0 being one | **OVERTURNED.** |"; VTIDX's own appendix lists slot 0 `0017CC70` (VTIDX:2185)
- Status: favoured side B by `APP:340` "## 10. Falsification pass 1 - 2026-09-02" ("OVERTURNED", APP:361). Side A still unstruck at VTIDX:2505; `README:31` also still says "Never deleted, hence no stated object size." This also moves the NEITHER/A_ONLY counts in VTIDX:2464-2472.
- page-text only - needs local check

**C-V114.** **GameApplication vtable slot count: 30 vs 31**
- Side A: `RTTI:237`: "| `GameApplication` | 30 | the root application object |"
- Side B: `APP:28`: "a vtable of 31 slots at `0x008C5760`"; `APP:354`: "| 31 vtable slots | a 32nd function pointer | **SURVIVED.**"
- Status: no favoured side (APP's dated pass tests 31 against 32, it does not address RTTI's 30).
- page-text only - needs local check

**C-V115.** **`00863850` (GiColorRect slot 1): execute-against-device vs exception thunk**
- Side A: `VTIDX:2496`: "**They are render command objects, and slot 1 is execute-against-device.**" (Gi* family); appendix `VTIDX:2441`: `00863850` | `GiColorRect` | 1
- Side B: `VTIDX:3375`: "`00863850` (738 B) is an exception-thunk body - the `008C5F80`-`008C5FD0` rdata run"
- Status: no favoured side.
- page-text only - needs local check

**C-V116.** **`001C0F20` identity**
- Side A: `VTIDX:2739`: "`SaveloadManager_ParseDisableAutosaveList` (`001C0F20`, 2,028 B)"
- Side B: `VTIDX:3367`: "`001C0F20` (2,028 B) is the `008F6600`-vtable object body - 10 `001EDF00` string copies, the `"EASTL basic_string"` vtable string"
- Status: no favoured side (could both hold; neither cross-references the other).
- page-text only - needs local check

#### 3.1.8 Shared-state accessors and the ownership boundary

**C-V117.** **Shared scratch page object count: 62 vs 13**
- Side A: `OWN:159`: "Re-derived from writer sets, the page holds **62 objects, not 13**"
- Side B: `OWN:277`: "**Do not treat `022D8F00`–`022D9500` as one region.** It is 13 objects"; also `OWN:405`: "It is **thirteen objects**, one of which is RNG control state."; `README:42`: "why `022D8F00`–`022D9500` is thirteen objects rather than one."
- Status: favoured side A by `OWN:157` "**CORRECTED 2026-09-02 — the object count below is wrong**" (and WB:439 "### CORRECTED: 62 objects, not 13"). Corrected claim still repeated unstruck at OWN:277, OWN:405, README:42.
- page-text only - needs local check

**C-V118.** **Size of the `022D8F00`–`022D9500` area: 1,436 vs 1,536 bytes**
- Side A: `OWN:404-405`: "that `022D8F00`–`022D9500` is *one* 1,436-byte shared scratchpad"
- Side B: `WB:202`: "`022D8F00`–`022D9500` | the transform workbench | BSS region, 1,536-byte"; `WB:212`: "022D8F00 .. 022D94FF        1,536 B"
- Status: no favoured side (no dated correction; 0x600 = 1,536 by the page's own bounds).
- page-text only - needs local check

**C-V119.** **Number of wrong sub-labels: three vs two**
- Side A: `OWN:39`: "**Three labels within it do not hold**, and they are named."; `OWN:429`: "### FOUND: three labels that are wrong"; `OWN:490-491`: "with three named exceptions in the sub-labels"; `README:40`: "**Three sub-labels are wrong**"
- Side B: `OWN:282`: "**TWO are wrong (corrected 2026-09-22, FABLE):**"; `OWN:298-299`: "**ANSWERED 2026-09-26 … two** labels are wrong, not three."
- Status: favoured side B by OWN:282 / OWN:298 (dated 2026-09-22, 2026-09-26). Still repeated unstruck at OWN:39, OWN:429, OWN:491, README:40.
- page-text only - needs local check

**C-V120.** **`005004C0` callees: 39 callees vs no call / forty jump targets**
- Side A: `OWN:194`: "39 callees — a router, but a large one"; `OWN:293`: "`005004C0` (497 B, 39 callees) is a switchboard"
- Side B: `OWN:283`: "no `call` in its 497 bytes and forty tail-jump targets"; `OWN:438-441`: "**forty distinct `jmp` targets** … the graph's “39 callees” are those tail jumps"
- Status: no favoured side on 39 vs 40 (the 2026-09-22 correction explains "callees" as jumps but leaves 39 ≠ 40 unreconciled).
- page-text only - needs local check

**C-V121.** **`003B8670` objects: 15 private vs 15 written / 8 exclusive**
- Side A: `OWN:306-307`: "15 private objects including `0209218C+20` and `020925A0+12` that nothing else in the image writes"
- Side B: `OWN:358`: "15 written objects, 8 of them exclusive"; `OWN:446`: "`003B8670` (15 written objects, 8 exclusive)"
- Status: no favoured side (side A is inside a struck box, OWN:304-308 `~~`, so it is struck text; side B unstruck).
- page-text only - needs local check

**C-V122.** **`02F97348` described as private state, but other 00 pages read/write it**
- Side A: `OWN:514`: "**The private state is the current action context.** The singleton `[02F97348]`"
- Side B: `TICK:2765`: "`003A7050` (581 B) is the twin timer-decay channel the world tick runs on singleton `02F97348`"; `TICK:1170`: "for the four dwords `+0x110` to `+0x11C` of `*02F97348`, calls `002FC340` on each non-zero one and zeroes it"; `C-TICK:295`: "`003A3E30` … consult on singleton `02F97348`"
- Status: no favoured side.
- page-text only - needs local check

**C-V123.** **`00433830` write footprint: 84 consecutive bytes vs 52-byte run + 11 others vs ~0x380 block**
- Side A: `OWN:230-232`: "(it writes 84 consecutive bytes of one buffer) instead of the correct **1 run of 52 bytes plus 11 others**"
- Side B: `OWN:395-397`: "**Eighty-four consecutive bytes.** One buffer … the same function writes **12 objects**, the largest a 52-byte run"; `OWN:573`: "writes `022D9304`, tail of a `022D8F90`-based scratch block of ~0x380 bytes"
- Status: no favoured side (84 consecutive bytes cannot coalesce into a 52-byte largest run under the stated ≤8-byte gap rule; OWN:573 is a third extent).
- page-text only - needs local check

**C-V124.** **`00433830` role: tessellation helper vs blend kernel**
- Side A: `OWN:195`: "shared tessellation helper"; `OWN:272-273`: "reached from tessellation, mesh building and colour packing paths"
- Side B: `PRIM:593`: "the dst2 channel kernel — no calls; a pure-SIMD weighted blend over the `022D8Fxx` staging cells"; `WB:594`: "the `00433830` blend kernel"
- Status: no favoured side.
- page-text only - needs local check

**C-V125.** **Audio play constants labels (pan/volume) — corrected, but struck labels repeated**
- Side A: `NBR:84`: "~~"volume `0x40`, parameter `0x7F`"~~"; `NBR:270`: "forwards `(0, id, volume, parameter)` to the audio manager singleton"; `NBR:284`: "`(manager, 0, id, volume byte, parameter)` … masks the parameter to `0x7F` a second time"; `NBR:293`: "`(handle, id, volume, parameter)`"
- Side B: `NBR:81`: "pan 0x40, volume 0x7F"; `NBR:84-90`: "**They are the other way round** … the **`0x40`** to `002256F0` — **the pan wrapper** … the **`0x7F`** to `002257E0` … a level, normalised."
- Status: favoured side B by `NBR:84` "until 2026-09-21 (FABLE)". The old "volume" (second arg) / "parameter" (third arg, the 0x7F-masked one) labels are still used unstruck at NBR:270, NBR:284, NBR:293 (and "parameter" at NBR:99-101).
- page-text only - needs local check

**C-V126.** **`0020E600` subsystem reach: 17 vs 21**
- Side A: `HUBS:481`: "| 17 | 815 | `ImageAddress_ResolveRuntimePointer` | runtime infrastructure |"
- Side B: `NBR:336`: "`ImageAddress_ResolveRuntimePointer` (10 B, 815 callers in 21 owning subsystems)"
- Status: no favoured side (different dates/methods: HUBS 2026-09-02, NBR 2026-09-14).
- page-text only - needs local check

**C-V127.** **`002F8060` size: 648 B vs ~128 B**
- Side A: `HUBS:211`: "| `002F8060` | `BattleUnit_TryTriggerNearbyAuthoredFieldAction` | 648 B |"
- Side B: `HUBS:543`: "`002F8060` (`BattleUnit_TryTriggerNearbyAuthoredFieldAction`, ~128 B)"
- Status: no favoured side.
- page-text only - needs local check

**C-V128.** **Opcode 128: inline vs calls `002EB740` (page vs TSV)**
- Side A: `action-timeline-opcodes.tsv` row opcode 128: "128	60	003B92F3	(inline, no call)"
- Side B: `OWN:537`: "~~128 and a dozen others are inline without a call~~ *(Corrected 2026-09-30, SWE2-DATA …: opcode 128 calls `002EB740` … as event kind 5 with that target"
- Status: favoured side B by the OWN:537 dated correction (2026-09-30). The TSV still carries the uncorrected row.
- page-text only - needs local check

**C-V129.** **Opcode 37 dispatch (page vs TSV)**
- Side A: `action-timeline-opcodes.tsv` row 37: "37	34	003B9234	003333B0 FUN_003333b0" (no `002EB740`)
- Side B: `OWN:520-527`: "opcodes ~~13, 26 and 34~~ **13, 26, 34 and 37** *(corrected 2026-09-29, FABLE: opcode 37 was missing)* dispatch other timeline events the same way … 37: kind 4."
- Status: favoured side B by the OWN:521 dated correction (2026-09-29). The TSV row is not updated (it may reach the dispatch by an inline jump, as the 128 correction shows; not stated).
- page-text only - needs local check

**C-V130.** **Opcodes 10/11 callee `003ACA90`**
- Side A: `OWN:532-533`: "**10** / **11** run the render reset family … (`003ACA90`, `003AFD30`, `003B6930`"
- Side B: TSV opcode 11 row: "003B81A0 FUN_003b81a0; 003ACA80 FUN_003aca80; 003AFD30 …" (no `003ACA90`)
- Status: no favoured side.
- page-text only - needs local check

**C-V131.** **`02098E10` rows: five slots vs "rows < 3 only" config table**
- Side A: `NBR:301`: "**The records** are the five actor-manager slots."; `C-TICK:60`: "the actor-manager slot array, stride 0x288 -- FIVE slots"; `HUBS:165`: "class … (must be `< 5`…)"
- Side B: `OWN:694-698`: "`byte[obj+0x15]` picks a row of the `02098E10` config table (0x288-stride, rows < 3 only) … everything else (kind >= 3 …) forwards"
- Status: no favoured side (OWN may be stating only that function's bound; it names the array a "config table").
- page-text only - needs local check

#### 3.1.9 Developer tuning console: dispatcher, tunables, second table, event slot, names

**C-V132.** **Stepping arms: all bidirectional vs 51 one-way**
- Side A: `CON282:391`: "**102 of 102** fixed-step arms have this shape — a `test` on a register flag, then a `subss` and an `addss` against the *same* constant. Not one arm steps in a single direction."
- Side B: `C-CON:262-263`: "~~110 arms carry both `addss` and `subss`~~ **110 arms reach `addss`, and 59 of them also reach `subss`; 51 step one way only** *(CORRECTED 2026-09-29, falsification pass 1)*"
- Status: on the mnemonic count, favoured side B by "*(CORRECTED 2026-09-29, falsification pass 1)*" (C-CON:263) and D10 "**corrected**: 110 arms reach `addss`; 59 also reach `subss`" (C-CON:382). The corrected claim is still repeated unstruck at CON282:90 "(`addss` *and* `subss`, one arm doing both) | **110**". On *direction*, no favoured side: CON282:465-468 shows arms that step both ways with one `addss` (sign from a ±1.0 register), so "one way only" by mnemonic may not mean one direction.
- page-text only - needs local check

**C-V133.** **How arm extents are bounded**
- Side A: `CON282:85-86`: "Classifying each of the 226 by the instructions between its entry and the next arm's"
- Side B: `C-CON:386-389`: "My first arm census cut the body at each next table entry. … Arms share tail code, so that cut is wrong. The counts above follow each arm's control flow from its entry"
- Status: favoured side B by the 2026-09-29 pass (C-CON:364, 386-389). CMDNAMES:402 "bounding it at the next *address* is right" sides with neither. CON282:86 and 294 ("each arm's instruction range classified between its entry and the next arm's") are still unstruck.
- page-text only - needs local check

**C-V134.** **Whether 0.005556 is a literal constant**
- Side A: `C-CON:141-142`: "The last two are loaded as no literal. The arms compute them"
- Side B: `CON282:416-423`: "The step census, with the sign composed, is exactly symmetric" … "| 0.005556 | 1 | 1 |"
- Status: no favoured side.
- page-text only - needs local check

**C-V135.** **Literal-constant census (1.0, extra constants)**
- Side A: `CON282:101`: "1.0  x8"
- Side B: `C-CON:376`: "survives: all eleven, including 1.0 ×11. The census also finds 0.5 ×4, −0.02 ×3 and 0.002 ×3, which the table did not list"
- Status: no favoured side. C-CON:134-137 itself calls the difference "method, not error".
- page-text only - needs local check

**C-V136.** **Where the +0.01 constant lives**
- Side A: `CON282:162`: "| `008F30E4` | `.rdata` f32 | `+0.01` — the dominant step, referenced 88 times |"
- Side B: `CON282:400-401`: "the pool holds `+0.01` at `009002BC` and `-0.01` at `009002F4` as separate floats"; `CMDNAMES:419`: "steps it up or down by the constant at `009002BC`"
- Status: no favoured side. Also CON282:383 has `[008F30E8]` as 0.05, next to `008F30E4`.
- page-text only - needs local check

**C-V137.** **What indexes the authored-code table (console id vs field id)**
- Side A: `C-CON:168-169`: "The renderer indexes the table by the id itself (`001CDBDF`–`001CDBF7`: `[base + id*16 + 0x1CD6E68]`)"; `C-CON:291`: "code  = qword[0x01DF6E68 + id*16]"
- Side B: `CON2:75`: "**Answered 2026-09-30 (SWE2-CONTRACT): they are map-pack names, and the table is indexed by field id.**"; `CON2:249`: "(fieldId from the singleton's +0xAB4)"
- Status: favoured side B by that dated answer (CON2:75-83), which also answers the contract's `dst0104` question. C-CON:80 already says "index from `[r15+0xAB4]`". Still unstruck: C-CON:158-165 (I-7, "area codes", "a reading of the table as a per-id key"), C-CON:290-292 (§12), C-CON:305-308 (§14 items 1–2).
- page-text only - needs local check

**C-V138.** **Authored-code table extent and NULL count**
- Side A: `C-CON:68`: "| **authored codes** | `01DF6E68` in `.data` | **16** | 294 (ids 0–293) | `id` |"; `C-CON:261`: "**A NULL code pointer** → 183 of the 294 entries"
- Side B: `C-CON:77`: "**CORRECTED 2026-09-25 (OPUS) - the table is 1,314 entries long, not 294.**"; `CON2:241`: "`.data`, 1,314 × 16 B | … 601 codes"
- Status: favoured side B by the 2026-09-25 correction. 294 is still repeated unstruck at C-CON:68, 73 ("for all 294 entries"), 158, 261, 291 ("NULL in 183 of 294") and 321 ("all 294 entries decoded").
- page-text only - needs local check

**C-V139.** **`008AB7C0`: getter vs destructor vs registration**
- Side A: `CON282:249`: "the 12-byte getter `008AB7C0` returns it and has no listed caller"
- Side B: `TUNES:72`: "`lea  rcx, [rip+0x749399]    ; -> 008AB7C0, the destructor`"; `TUNES:540-541`: "`lea rcx, [008AB7C0]` and `jmp 00808B90` — the `atexit` registration of its teardown"
- Side C: `TUNES:1214-1216`: "`lea rcx, [02CB7FD0]` then `jmp 005DDDB0` … registers the `02CB7FD0` record with the `005DDDB0` registration body"
- Status: no favoured side. Outside my pages, ARM-E:239-241 (00 folder) agrees with side B ("`atexit(destructor)`").
- page-text only - needs local check

**C-V140.** **Block defaults: constructor vs none**
- Side A: `CON282:328`: "in the zero-filled tail of `.data` — no file image, built at run time."
- Side B: `TUNES:65-67`: "**Corrected 2026-09-03: "uninitialised, built at run time, no file image" was wrong.** The block is a **C++ static object** with a constructor and an `atexit` destructor, and its defaults are immediates in `.text`."
- Status: favoured side B by the dated correction (TUNES:65), refined by TUNES:542-544 (2026-09-13): no file image, loader-zeroed, then constructed. Still unstruck: CON282:328; TUNES:169 "`.data`, uninitialised"; TUNES:270 "uninitialised `.data` neighbourhood".
- page-text only - needs local check

**C-V141.** **`001F0AD0`'s write extent in the block**
- Side A: `TUNES:188`: "+390 .. +44F   shadow scalars and counts   001F0AD0; includes the four mMapShadow* names below"
- Side B: `TUNES:932`: "span **`02CB8160` … `02CB8404`**" (that is, `+0x190..+0x434`); `TUNES:520`: "**Do not patch `+190..+434`.**"; `TUNES:958-959`: "ending at `001F1543` → `02CB83E8`"; `TUNES:362-365`: the `mMapShadow*` offsets `+438..+444` are named by `001C7940`
- Status: no favoured side.
- page-text only - needs local check

**C-V142.** **When the loaders run: per frame vs scene load**
- Side A: `TUNES:493-494`: "meanwhile, every frame: / `001C7940 / 001C3D50      read the same block through movss`"
- Side B: `TUNES:518`: "overwritten from config at scene load"; `CON2:253`: "map load: 001C7940 -> 001FF740("mUseLinearTonemap") -> 00193D50 block +0x4A2"
- Status: no favoured side.
- page-text only - needs local check

**C-V143.** **Next-frame effect: "nothing double-buffers it" vs a double-buffered snapshot**
- Side A: `C-CON:249-250`: "a press takes effect on the next frame, because the block the arms write is the block the renderer reads; nothing double-buffers it."
- Side B: `CON282:250`: "The snapshot is 0x598 bytes, change-checked by a 0x598-byte memcmp and double-buffered at owner +0x4E0, and it is NOT the GPU layout."
- Status: no favoured side. They may describe different objects (the block vs the staged snapshot). The block-to-GPU latency is not settled.
- page-text only - needs local check

**C-V144.** **Is `00265680` itself a field-frame entry gate?**
- Side A: `EVSLOT:232-234`: "it is one of the field frame's three entry gates"; `EVSLOT:254`: "| `00265680` | manager-slot readiness gate | 149 B | one of the field frame's entry gates |"
- Side B (00): `TICK:919`: "**What the field frame's three entry gates `001800E0`, `001800C0`, `001EC560` test**". There `00265680` is a sub-test of `001EC560` (TICK:928-930).
- Status: no favoured side.
- page-text only - needs local check

**C-V145.** **Who reads the classification flags**
- Side A: `EVSLOT:173`: "The flags are read both by console arms and by the script driver's wait-park gate (§4)."
- Side B: `EVSLOT:185-186`: "The consumer set is closed: seven call sites in four functions, `00180120`, `0025DF00`, `0034CF90`, `0034D790`, all read"
- Status: no favoured side. EVSLOT:185 is a dated pointer but does not strike line 173.
- page-text only - needs local check

**C-V146.** **Config-screen id set and case-table extent**
- Side A: `CON282:262`: "the arms carry exactly **16** ids: `0x86`, `0xA6`, `0x10A`, `0x110`–`0x119`, `0x11B`–`0x11D`" (same at 216, 271); `CON282:271`: "a 23-entry table (`0017DBBF`..`0017DBDE`)"
- Side B: `CON282:270`: "a 23-way jump table (`0017DBC2`..`0017DBDE`) whose cases forward ids of 12 and above (`0x86`, `0x10A`, `0x110`..`0x11D`) and none below"
- Status: no favoured side. Line 271 is later (2026-09-18) but does not explicitly overturn 270. Side B omits `0xA6` and adds `0x11A`, which is id 282, `Save Config File`, on the shared arm (CMDNAMES:365).
- page-text only - needs local check

**C-V147.** **`0017D490` extent**
- Side A: `CON2:98`: "**has a dedicated nineteen-byte accessor:**"
- Side B: `CON2:230`: "| `0017D490` | `WorldField_GetDebugWeatherSlotOverride` | 20 B |"
- Status: no favoured side. The quoted asm, `0017D490`..`0017D4A3 ret`, spans 20 bytes.
- page-text only - needs local check

**C-V148.** **Dispatcher return type**
- Side A: `CON282:176`: "`int DevConsole_DispatchCommand(void *ctx, u8 a, u8 b, int id)`"
- Side B: `C-CON:55`: "| return type | none established — the arms are `jmp` targets inside one body, not callees. |"
- Status: no favoured side.
- page-text only - needs local check

#### 3.1.10 Developer tuning console: the arm catalogue (work division and slices A-I)

**C-V149.** **Block tunables "consumed by nothing" vs copied whole into the shader constant buffer**
- Side A: `ARM-C:215-217`: "**ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): character Fresnel-specular and hair / eye lighting tuning values. All 36 are named, and in this build nothing outside the console reads any of them.**"; `ARM-C:227-228`: "The bank is written and displayed, and nothing consumes it."; `ARM-B:167`: "**What they control in this build: nothing outside the console.**"; `ARM-B:176`: "the knobs are console-only."
- Side B: `CON282:249`: "*Narrowed 2026-09-18 (FABLE): the 63 are traced after all — to the staged shader-constant buffer, not to a body.* … **Every one of the 80 sits at `+0x004` .. `+0x17C`**"; `CON282:250`: "**ANSWERED 2026-09-27 (OPUS):** each of the 80 becomes a named variable of the shipped shaders' SceneWideParameterConstantBuffer … the character Fresnel/Hair/Eye A-B families -> chrFresnel*/hChr*/eChr*/xChr*/yChr* (0x238-0x2C4)".
- Status: favoured side B by the later dated "ANSWERED 2026-09-27 (OPUS)" (CON282:250). Side A is still repeated unstruck at ARM-B:160-176, ARM-C:215-229; also ARM-E:331-334 / ARM-E:348 ("Whether the 21 `Map …` floats have a consumer at all"), ARM-D:380-392 ("Nothing can walk it as an array"), ARM-A:301 ("nothing else reads either global").
- page-text only - needs local check

**C-V150.** **`02CB7FE8`–`02CB8144` "no pointer into the block can be formed" vs a `this`-based walk**
- Side A: `ARM-D:388-392`: "**Nothing can walk it as an array, and that is the decisive part.** The census finds **zero `lea`** anywhere in the span: **no instruction takes the address of any slot**, so no pointer into the block can be formed and no `base + index*4` access can exist."
- Side B: `ARM-E:243-244`: "So **`02CB7FD0` is an object base, not a global**, and every `02CBxxxx` field in this slice is `this + offset`."; `CON282:249`: "`006084B0` staging sixteen bytes at a time … (a base-register walk `base+0x00` .. `base+0xD0` and on, the very access shape a rip-relative census cannot see)"; `ARMDIV:444`: "Passed by `lea rcx` to a constructor, **so every `02CBxxxx` field is `this + offset`**".
- Status: no explicit dated retraction of ARM-D's UQ-17; CON282:249-250 (2026-09-18/27) is later. Literal `lea` claim is about `02CB7FE8`+ while the base is `02CB7FD0`, so only the conclusion conflicts. No favoured side by the rule; later dated text supports B.
- page-text only - needs local check

**C-V151.** **Id 28's float constants**
- Side A: `ARM-A:160-162`: "**Not one of those references is in slice A.** The only float constants here are `1` and `-1`, in id 26." (also ARM-A:95 "**the only float arm in this slice**")
- Side B: `ARMDIV:45`: "**Id 28 is not a stepper:** it multiplies three values by `0.2126` / `0.7152` / `0.0722` — the Rec.709 luma weights — inside the save / zero / restore toggle"; CMDNAMES:419 "recomputes `02CB8080`".
- Status: no favoured side (ARMDIV §1 is dated 2026-09-13 but does not retract ARM-A's line). ARM-A:161 unstruck.
- page-text only - needs local check

**C-V152.** **Hub counts 45 / 33: arms vs call sites**
- Side A: `ARMDIV:259-260`: "`001A9930` is used by 45 arms, `00193D50` by 33"; `ARM-A:153-154`: "one serving **45** arms, the other **33**"; ARM-A:110 "calls the 33-arm shared helper".
- Side B: `ARM-D:194-197`: "`001A9930` | 14 | **14** | **45** … **The numbers 45 and 33 reproduce exactly — as call sites.**"; `CON282:113`: "*(CORRECTED 2026-09-29, OPUS …: "used by" counted **call sites**, not arms.)*"
- Status: favoured side B by CON282:113 "CORRECTED 2026-09-29" (also CON282:149). Side A still unstruck at ARMDIV:259 and ARM-A:110-111, ARM-A:153.
- page-text only - needs local check

**C-V153.** **Which accessor has "47 caller functions"**
- Side A: `ARM-D:162`: "The accessor is a hub — **47 caller functions image-wide**" — D's accessor is `001A9930` (ARM-D:264), 14 arms / 45 sites (ARM-D:194).
- Side B: `ARM-F:238-239`: "The accessor used by ids 172–174 and 179 … **16 arms, 33 call sites, 47 caller functions image-wide.**" (16 arms/33 sites = `00193D50`, ARM-D:195)
- Status: no favoured side.
- page-text only - needs local check

**C-V154.** **`01F82D20` is never nudged vs "nudged by 18" / "MOV r32"**
- Side A: `ARMDIV:42`: "**24 in 18 arms**, all 8-byte loads … **reproduced** — a pointer slot, never nudged"; `ARMDIV:315`: "**`01F82D20` is a pointer slot and is never nudged.**" (Corrections, 2026-09-03)
- Side B: `ARMDIV:195`: "The hottest single address is `01F82D20`, nudged by **18** different commands." (unstruck); `CON282:329`: "The hottest single address is `01F82D20`, nudged by **18** different commands (… re-counted 2026-09-30 …)"; `TUNES:603`: "every access found is a `MOV r32` read"
- Status: favoured side A by "Corrections to this work order, 2026-09-03" (ARMDIV:313-324) and the 2026-09-13 census (ARMDIV:42). Side B unstruck at ARMDIV:195, CON282:329 (dated later only for the count), TUNES:603 (width).
- page-text only - needs local check

**C-V155.** **Distance `01F82D20` → `01F82ED0`**
- Side A: `ARMDIV:328` / `ARM-D:184`: "`01F82ED0`, sixteen bytes further into the same region"
- Side B: arithmetic of the two addresses the same lines give: `0x01F82ED0 − 0x01F82D20 = 0x1B0` (432 bytes).
- Status: no favoured side; internal arithmetic.
- page-text only - needs local check

**C-V156.** **Arms referencing `01F82D20` in slice I: 15 vs 14**
- Side A: `ARM-I:38-39`: "fifteen of its twenty-two live commands dereference one shared pointer"; `ARM-I:94-95`: "slice I holds fifteen of them"
- Side B: `ARMDIV:469`: "**18** — D 1 · E 1 · H 2 · I 14"; `ARM-H:197`: "18, across slices **D (1), E (1), H (2), I (14)**"; consumers TSV row `01F82D20` (11 + 3 I ids = 14).
- Status: no favoured side (ARMDIV §H is undated). D1+E1+H2+I15 = 19 ≠ 18.
- page-text only - needs local check

**C-V157.** **`+0x10C4` owner: id 267 or id 268**
- Side A: `ARM-H:257`: "`+0x10C4`           mouse vertical camera speed, mirrored from the accessor" (id 267 "Mouse Control Vertical Camera Speed", ARM-H:93)
- Side B: `ARM-I:154`: "| 268 | `001D4731` | int step via a getter/setter pair | mirrors to `d+0x10C4` |" (id 268 "Mouse Control Horizon Camera Speed", CMDNAMES:351)
- Status: no favoured side.
- page-text only - needs local check

**C-V158.** **Id 200's party walk: `022C1740` vs `02EBF190`**
- Side A: `ARM-F:133`: "`00305A00`: stores LP `+0x190 = 99,999` … for each party member the nine-slot walk `BattleStats_GetByMappedBattleSlot(i, 3)`, `i < 9`, finds (roster kept at `022C1740`)" ("corrected 2026-09-13")
- Side B: `ARM-F:313-314`: "Id 200, *"Set LP to max"*, calls `00305A00` (`001D3EB6`), the 170-byte function that walks the party through `02EBF190`" ("Answered 2026-09-14"); `CON282:298`: "`00305A00` reads `02EBF190`"
- Status: no favoured side (the 2026-09-13 row correction is about calls; the 2026-09-14 answer is later but does not address the roster address).
- page-text only - needs local check

**C-V159.** **Id 227 wrap: every sub-field mod 60 vs hours mod a runtime value**
- Side A: `ARM-G:80`: "**each sub-field mod 60**"; `ARM-G:124-125`: "**modulo 60, four times in the body.**"
- Side B: `ARM-G:288-290`: "**227 is an h:mm:ss editor** whose hours wrap modulo a **runtime** value"; `ARMDIV:533-535`: "**hours wrap mod a runtime value at `+0xE18`**"
- Status: no favoured side (amendment undated, "recorded as an amendment rather than folded in", ARM-G:287). ARM-G:80 table row unchanged.
- page-text only - needs local check

**C-V160.** **`005DC720` / `005DC580` targets and range**
- Side A: `ARM-E:244-245`: "`FUN_005dc720` calls a base constructor `FUN_005dc580` with `rcx = this`, then `FUN_005dc430` with `rcx = this + 0xD0`"; `ARM-E:257`: "`005DC580` covers `0x00–0xC4` and `005DC720` covers `0x42C–0x4D8`"
- Side B: `ARM-E:454-455`: "`005DC580` + `005DC430` init the `+0xD0` member" (SWE2-EC7-126 update 2026-09-21); `ARM-E:461-468`: "a 2-iteration loop … rooted at `+0xA1D` before `+0x1010`/ `+0x1018`/`+0x1020` are zeroed"; `TUNES:76`: "`005DC720` initialises fields out to `+0x1020`"; `TUNES:509`: "`005DC720` (`+42C..+468`)"
- Status: no favoured side for the `005DC580` target (TUNES:390 and TUNES:546-547 agree with side A on `rcx = this`); range `0x4D8` vs `+0x468` vs `+0x1020` unresolved.
- page-text only - needs local check

**C-V161.** **Id 108's step constant**
- Side A: `ARM-D:74`: "| 108 | `001D1FE6` | `02CB8130` | 0.02 | one constant, `subss`/`addss` |"
- Side B: `CMDNAMES:419`: "Arm 108 (*Diffuse intensity*, `001D1FE6`–`001D200F`) loads the float and steps it up or down by the constant at `009002BC`"; `CON282:400`: "the pool holds `+0.01` at `009002BC`"
- Status: no favoured side (CON282:162 and ARM-E:67 put `+0.01` at `008F30E4`, so `009002BC`'s value is itself disputed across pages).
- page-text only - needs local check

**C-V162.** **"Every stepping arm holds both directions / the flag was universal" vs id 38**
- Side A: `ARMDIV:244-246`: "Every stepping arm holds both directions"; `ARM-F:63-64`: "In slices A–D the flag was universal among stepping arms"
- Side B: `ARM-A:107`: "| 38 | `001D1C83` | integer step | `d+0xAC0` | 1 | `inc` only — no direction test" (corrected 2026-09-13)
- Status: favoured side B for id 38 by "corrected 2026-09-13" (ARM-A:107). Side A unstruck at ARMDIV:244 and ARM-F:63.
- page-text only - needs local check

**C-V163.** **Label-shape claim vs id 103**
- Side A: `ARM-E:160-161`: "Every `cmp`/`sete` arm in both slices carries a label ending in "enable" or "Enabled"."
- Side B: `ARM-C:283`: "`cmp`/`sete` in 99 and 103"; id 103 label "Camera Over Write (O to capture)" (ARM-C:320; CMDNAMES:186).
- Status: no favoured side. (Used as one of four alignment proofs.)
- page-text only - needs local check

**C-V164.** **Loader writes vs "genuine outside consumers" in the block, and `02CB8128`**
- Side A: `ARM-B:179`: "**27 have a genuine outside consumer.** … `001C3D50` and `001C7940` together take 19 slots (`02CB8044`–`02CB8060`, `02CB80A0`–`02CB80AC`, `02CB80D4`, `02CB80D8`, `02CB80E4`, `02CB8104`)… **So the block IS consumed - just not here.**" (MEASURED 2026-09-16)
- Side B: `ARM-C:223`: "**writes** by the scene-config loaders `001C3D50` / `001C7940` to the nine keyed slots" incl. `02CB8128` (ARM-C:232); `ARM-B:174`: "The scene-config loaders `001C3D50` / `001C7940` write only the neighbouring gap slots" (2026-09-25)
- Status: favoured side B (loaders are writers) by "ANSWERED 2026-09-25" (ARM-B:160; ARM-C:215); ARM-B:179 unstruck. The listed slots number 16, not 19, and omit `02CB8128` (keyed per ARM-C:232 and the TSV).
- page-text only - needs local check

**C-V165.** **`EnableIBL` key bound to two addresses**
- Side A: `ARM-D:284`: "| `+0x2E4` | — (byte) | `EnableIBL` (`001C98B5` / `001C98CA`) |" (map-art context, 2026-09-25)
- Side B: `CON282:248`: "`EnableIBL` at `01DFE190`"; consumers TSV row `01DFE190 … EnableIBL`
- Status: no favoured side (could be two stores of one key; neither page says so).
- page-text only - needs local check

**C-V166.** **Kinds of slice I sum to 28 for 26 ids**
- Side A: `ARM-I:46-50`: 13 property + 4 boolean + 4 integer + 3 getter/setter + 4 unimplemented (= 28)
- Side B: `ARM-I:52`: "**22 real arms.**"; `ARM-I:181`: "**22 real arms and 4 unimplemented**" (table rows: 13 + 3 + 3 + 3 = 22)
- Status: no favoured side.
- page-text only - needs local check

**C-V167.** **Slice F direction census 11 / 8 / 8 vs nine unconditional ids**
- Side A: `ARM-F:58-60`: "`bl` only … 11 | … two separate buttons | 8 | … neither … | 8"; `ARM-F:62`: "**Eight of the 27 arms ignore the direction flag completely.**"
- Side B: `ARM-F:244-245`: "Ids 176, 179, 183, 185, 187, 188 and 199–201 flip regardless" (nine ids); table rows with "**none**": 176, 179, 183, 185, 187, 188, 199, 200, 201 (ARM-F:109-134)
- Status: no favoured side.
- page-text only - needs local check

**C-V168.** **Slice H non-empty arms: 16 vs 14**
- Side A: `ARM-H:218`: "all 16 non-empty arms exit to `001D4BFA`"; `ARMDIV:493`: "all 16 of its arms exit to `001D4BFA`"
- Side B: `ARM-H:52`: "**18 do-nothing · 8 counter/cycle arms · 5 call arms · 1 float step.**" (32 − 18 = 14 real)
- Status: no favoured side.
- page-text only - needs local check

### 3.1.C Counts that disagree (no behaviour attached, but a port's tables or a checker's assertions would differ)

#### 3.1.C1 Counts that disagree: Boot fixups, startup data construction and the application root

- Startup objects: 66 (`FLOAT:349` "There are 66 objects, not 75", favoured by falsification 2026-09-02) vs 74/75 (`FLOAT:32-33` "48 of the 74 hub targets"; `FLOAT:622` "Over all 74 objects with a next pointer"; TSV 75 rows; `README:26` "build 75 objects"). TSV supports 75 total / 66 in band; the 66 correction holds only for the band population.
- Builders reached: 65 (`FLOAT:109`, `FLOAT:351`) vs 67 (`FLOAT:281-282` "Counting the hubs' two tail jumps, the hubs reach 67 in-region builders").
- Unreached region functions: 131 (`FLOAT:228`, `FLOAT:360`) vs "the region's *other* 132 functions" (`FLOAT:271`).
- Helper-less builders: 15 (`FLOAT:4`, `FLOAT:513`, `FLOAT:630`) vs 16 (`FLOAT:188` "in all sixteen helper-less builders"; `FLOAT:631` "sixteen with `0047E140`").
- Prototype objects: "six of these objects" (`FLOAT:41`) lists seven addresses (`FLOAT:41-42`).
- `008631D0` callers: 40 (`FLOAT:511`) vs "48 frontier callers at census" (`FLOAT:645`).
- Exact memset rows: "nine are exactly equal" (`FLOAT:516`) vs eleven marked exact after the 2026-09-17 corrections (`FLOAT:521-536`).
- `001EDDC0` size: 165 B (`BOOT:239`) vs "~160 B" (`BOOT:497`).
- Frame bodies: "the six frame bodies" (`APP:709`) lists seven (`APP:709-710`).
- GameApplication bodies: "any of the 22 GameApplication vtable bodies" (`APP:418`) vs 18 overridden (`APP:123`).
- `006CB5F0`: "the twelve diagonal fields" lists eight offsets (`APP:1860-1864`).
- `0017D4C0`: "allocates `0x10`" (`APP:631`) vs "`00210EC0` quintuple" (`APP:1202`).
- Workbench population: `APP:415` "functions touching 022D91B0..+0x400 : 247", `APP:411` "152 owned writers" vs `README:50` "249 functions write one 1.5 KB area" (different populations/extents).
- "battery's smallest fill" `00482410` 471 B (`C-BOOT:727`) followed by smaller battery members `004978F0` 458 B … `004B0B70` 376 B (`C-BOOT:731-759`).

#### 3.1.C2 Counts that disagree: World tick, field frame and force-fight mode

- **Mode consulted "five times" vs four sites**: `C-TICK:67` "**WT-1 — The frame mode is a PARAMETER consulted five times**" vs `C-TICK:337` "the mode is held in `r14d` and tested at the four cited sites" (C-TICK:68-69 lists four site groups). No favoured side.
- **`cmp …, 5` sites: five vs six**: `C-TICK:167` "Count the `cmp … 5` sites and assert **five**" and `TICK:66-67` (five listed) vs `TICK:1008` "`00314132 cmp ebx, 5` (and five more)". No favoured side.
- **Manager slots: five vs three**: `C-TICK:94` "**WT-5 — Five slots**" vs `C-STOP:215-216` "the start/stop fan-out walks all 3 manager slots". No favoured side (may be a sub-walk; page-text only).
- **`23 steps` vs 39 calls**: reconciled on page (TICK:1014-1017); no contradiction.

#### 3.1.C3 Counts that disagree: Per-frame update gate and system stop registry

- UI-owned groups: `GATE:124` "**Six of the fifteen masks' groups are `UI`-owned**" vs the GATE:86-102 table, which marks five masks UI (`0x0004`, `0x0008`, `0x0100`, `0x0400`, `0x2000`).
- Groups: `GATE:286` "A word that fifteen update groups depend on" and `C-GATE:476` "The fifteen groups still do not account for the whole singleton" vs sixteen groups (GATE:29, C-GATE:152).
- Body population: `C-GATE:1033` "Across all 38,161 bodies" vs `C-GATE:287` / `C-GATE:334` "all 35,713 `.pdata` bodies".
- `_8FA0` owners and members: `C-GATE:581` "Censused from the fourteen thunk owners plus five bodies … **nineteen member bodies** touch **sixteen offsets**" vs the `C-GATE:499` owner list (12 functions) and `C-GATE:612` table "| `_8FA0` | 4,400 | 16 | 14 |" (16 members, 14 offsets).
- Zeroed-byte total: `C-GATE:1219` "the corpus-wide total is **52,076 bytes across 163 spans**". The stated inputs (42,192 + 11,593 − `_5380`'s 1,087) give 52,698; the difference of 622 equals the unstated removal of `_57E0ArrayRecord` (C-GATE:1171). Later `C-GATE:1250` gives 52,758 / 167 spans.
- Apply callers: `TICK:1552` "`00226280` — 952 B, 9 A-measured callers" vs `C-STOP:231-232` "exactly 25 call/jmp edges".
- Slot loaders: "136 bodies" (C-GATE:444) vs 203 distinct functions in `manager-singleton-0209be80-accesses.tsv` (a closure population; see P).
- `_A0D0` offsets: `C-GATE:613` "2 | 2 | `+0x960`, `+0x984`" vs `GATE:503`, which also names `+0x974` (the tsv has five disps).
- Undefined-residue upper bound: `C-GATE:1335` "the 3,862 are where it will not" vs corrected "≤ 3,079 bytes in 191 spans" (C-GATE:1288, 1315).

#### 3.1.C4 Counts that disagree: Battle runtime mode ladder, diagnostics log, duplicated names, all-ones convention

- Ladder callers: `C-MODE:444` "**20 call sites**" vs `MODE:534` "among the ladder's 21 callers" and `C-MODE:147` "Of the 21 callers" (21 is `00303EC0`'s count, MODE:443).
- Movement edges: `MODE:206` "(30 call edges)" vs `C-MODE:122` "**Movement** asks and answers on 13 edges".
- `022C2160` readers: `MODE:420` "Eleven readers test `state − 5 ≤ 1`" vs nine enumerated at `MODE:420-423`.
- `00254B50` jump table: `MODE:1094` "dispatches a six-arm jump table" vs five targets listed at `MODE:1095-1096`.
- `01EECFC0` rows: `MODE:348` "only modes 0–4 are in the table" vs `MODE:606` "`01EECFC0` dumped as six 32-byte rows".
- C-MODE evidence row: `C-MODE:508` "the ladder's six tests … and the two early returns" vs `C-MODE:541` "Four `test` instructions; the fifth decision is an `and`" / `C-MODE:545` "**"Two early returns" is four**" (row is annotated inline).
- DUP group census: `DUP:57`/`DUP:275` 53 thunk+body groups vs `DUP:329` "a reader re-running it gets 52 groups plus one it cannot place".
- DUP gap census: `DUP:160-169` "33,346 gap regions … 255 … **17** … **16** … at least 766" vs `DUP:355` "**33,329 / 509,056 / 253 / 15 / 14**" and `DUP:362-363` "**at least 764** by this count" (recorded as reproducibility gap; no favoured side).
- DUP thunk-caller census: `DUP:128-133` 325/140/185 (edges.tsv) vs `DUP:151`/`DUP:284` "**234 / 132 / 102**" (direct rel32) — page says both are defensible.
- ONES pairs: `ONES:162` "Three of the six are adjacent pairs" vs `ONES:112` "**Corrected 2026-09-13 (§9): two adjacent pairs, not three**" (favoured ONES:112; ONES:162 unstruck).
- `005CDAA0` callers: `LOG:55` "**136**" vs `APP:892` "239 B, 77 frontier callers at census" (different census basis).
- `0016D670` callers: `LOG:216` "both callers immediately use `[rax]`" vs `LOG:233` "**23 direct call sites, not two**".

#### 3.1.C5 Counts that disagree: Encoded-id space, class registry, query record, basis helpers, ABI recovery

- Direct callers of `0031C5D0`: "fourteen" (EID:62), "76 / 14 / 14" (EID:675), "12" own-record (EID:208), "17 direct callers" (CLS:321). Callers of `0035D330`: 76 (EID:675), 75 (EID:206), "159" (CLS:321). Probably functions vs sites; units not stated for CLS:321. C-EID:309 "all 191 wrapper/filler call sites" = 17+159+15.
- Sections bound by the loader: "34 `st2e` sections" (EID:72, EID:576); "33 times … 36 distinct descriptors" (CLS:172); "all 23 `st2e` tables of the shipped `battle_pack.bin`" (CLS:291); "fourth section (index 36" (CLS:371).
- RC-1 classes named: "code names 25 classes … Never named … 4, 15, 16, 19, 22 and 27" (CLS:322-324) vs "**Code names 26 classes** … Classes 4, 16, 22 and 27 are passed by no caller" (CLS:332-334, answered 2026-09-30, matches CLS:4).
- ABI control rows: "46 signatures" (ABI:9, ABI:18) vs "control rows parsed from contracts | **47**" (ABI:47; 46 comparable).
- ABI typed rows: "position 1 typed for 51" (ABI:4) vs 40 + 7 = 47 (ABI:190-191) vs "228 typed" (ABI:192).
- ABI frontier: "the 562 functions below are still in it" (ABI:38) vs "the frontier now holds **342**" (ABI:88, 2026-09-17).

#### 3.1.C6 Counts that disagree: Shared transform workbench (EE/VU0 register bank, save/restore, primitives)

- vf00 readers: `WB:371` "98 functions read `01EF93F0`" / `EEVU:70` "**129 readers**" / `EEVU:225` "`vf00` by 136" / `C-PRIM:414` "176 sites".
- ACC users: `EEVU:69` "83 writers, 46 readers" / `C-PRIM:368` "356/535 (47r/84w)" / `PRIM:299` "**70 functions reference it**" / `C-PRIM:113` "67 writers" / `EEVU:225` "ACC by 142".
- `022D9300`: `PRIM:300` "68 functions" vs `PRIM:346` "41 writers / 63 readers" and `C-PRIM:114` "`022D9300` has 41 writers and 63 readers" vs `C-PRIM:368` "47r/63w" (replaced 2026-09-21 at C-PRIM:365).
- `022D8F90`: `PRIM:301` "64 functions and 668 references" vs `PRIM:346`/`C-PRIM:114` "47 / 59" vs `C-PRIM:368` "44r/60w" vs `WB:205` "8 aligned rows, 2 Presentation functions" vs `WB:516` "| 2 | `022D8F90`–`022D9010` | 128 | 64 | 47 |" (columns: bytes, max writers, max readers).
- Callers of the primitives: `PRIM:52-53` 82 / 74 non-EH vs `C-PRIM:283` 86 / 81 fns vs `PRIM:628` "64 frontier callers" (`00398F90`); `C-PRIM:37` "156 non-EH callers" vs `C-PRIM:283` "137-fn union".
- `003970A0` callers: `PRIM:317` "the getter `003970A0`'s seven callers" / `PRIM:692` "28 frontier callers at census" / `C-WB:247` "Twenty-nine Presentation bodies" / `README:53` "28 of its 29 callers are **Presentation**".
- Population touching the region: `C-WB:93` "267" (`022D8F00`–`022D9500`) vs `EEVU:40` "267 functions" (range `022D8F10`–`022D949F` + vf00, EEVU:9) — same number over different ranges, unreconciled; `WB:133` "216" row-touchers; `APP:415` "247" (`022D91B0..+0x400`).
- Objects in the region: `WB:443` "**62 groups**" vs `README:42` and other 00 page `Ownership-Boundary/intentionally-ownerless-functions-and-shared-scratch.md:277` "It is 13 objects".
- Vector rows: `WB:36`/`EEVU:96` 31 rows vs `WB:204`/`WB:218` "32 rows" over `022D91A0`–`022D939F` (includes ACC).

#### 3.1.C7 Counts that disagree: Object model (RTTI and the vtable method index)

- VTIDX composition table (VTIDX:111-118) sums to **4,245**, not 4,275: it omits `SebAudioBank`, `btTriangleShape`, `btDbvtBroadphase` (10 each; VTIDX:2229, 2239, 2249).
- "92 of 125 classes now have a code-stated object size" (VTIDX:2472) vs AGREE 12 + A_ONLY 80 + B_ONLY 3 = 95 (VTIDX:2464-2467).
- NEITHER 30 (VTIDX:2468) vs 19 (VTIDX:2491) + 5 named + "7 filter edge cases" (VTIDX:2505-2508) = 31.
- Attack false positive "**2,134 admitted addresses missing**" (VTIDX:2551) vs "**2,141 ≈ 4,275 / 2.**" (VTIDX:2556).
- Battle action table "337" slots (RTTI:676) vs "8 distinct handlers across 341 slots" (RTTI:699).
- AS-4 singletons: 3,639 (RTTI:633) / 3,643 (RTTI:638) vs per-section 1,963 + 1,678 = 3,641 (RTTI:646-647).
- SQEX: "254 `SQEX::Sd` classes" (RTTI:161) vs "218 classes / 254 vtables" (RTTI:333).
- Physics: "**23 of 73** `Phyre.*Physics` functions" (RTTI:144) vs "3 of 70 `Phyre.Physics` functions" (RTTI:151).
- AS-1b: "Seventeen classes … **Sixteen of them are reflection metadata**" (RTTI:594-595) vs the table, which lists 12 descriptor vtables + 1 object (RTTI:599-603).
- Unreached residue: 351 fn / 87,959 B (VTIDX:2658) vs 435 fn / 81.8 KB (VTIDX:2666) vs 485 fn / 107,931 B (VTIDX:2751) — stated by the page as instrument differences.

#### 3.1.C8 Counts that disagree: Shared-state accessors and the ownership boundary

- "168 callers across 14 subsystems" (HUBS:30; README:59-60; OWN:261) vs the three tables, which name 16 distinct owner subsystems (11 at HUBS:60-71, plus World/Area/Field, Platform, Save at HUBS:106-115, plus Combat AI, Items at HUBS:133-139).
- "There are nine" resolvers (HUBS:154) vs 11 rows in the table (HUBS:161-171).
- "ran `audit_crossrefs.py` over all 33 existing documents and reported **128 UNACCOUNTED NEIGHBOUR findings across 43 documents**" (HUBS:395-396): 43 > 33.
- `FieldData_GetActiveFieldRecordBit15` (00377C20) "(65 callers)" (HUBS:948, dated 2026-09-30) vs "Combined, the predicate has **110 distinct callers**" (HUBS:496).
- Ledger totals: OWN:31 "38,131 … 28,137" (re-derived at GN161) vs OWN:267 "9,409 + 585 + 28,009 = 38,003" and OWN:351 same; OWN:120 "28,137 *(was 28,009)*".
- Census base: "over 34,270 function bodies" (OWN:321) vs "all 38,161 real bodies" (OWN:354, 380).
- Gi* factory objects: "eight" (OWN:315) vs sizes listed for seven: "Three of the eight objects are **8 bytes** … The others are `0x10`, `0x18`, `0x70` and `0x90`." (OWN:327-330).
- Timeline inline-without-call: "a dozen others" (OWN:537) vs 10 TSV rows after the 128 correction.
- Scratch-pool consumers: "the ~75 resource consumers" (OWN:915) vs "the seven consumers" (OWN:935).
- Pass-22 neighbours: "all 1,551 neighbours" (NBR:55) vs "the 1,545 remaining neighbours" after naming 8 read functions (NBR:258-259).
- Neighbour hub cut: "remove **35 of the 922 pairs**" (NBR:60-61) vs "**32 pairs** … dispositioned `MECHANICAL`" (NBR:196) and "changes the shipped findings by 0, and the R3 clauses-1+2 findings by −12" (NBR:335).
- Layer census: "spans thirteen subsystems" (NBR:355, 374) vs "nineteen layer names account for every measured edge" (NBR:384).

#### 3.1.C9 Counts that disagree: Developer tuning console: dispatcher, tunables, second table, event slot, names

- Arms: CON282:34 "runs one of **226** distinct arms" vs C-CON:117 "**I-3 — 282 IDS, 227 DISTINCT ARMS**". Both count 227 targets (CON282:84), so this is wording.
- Addresses: CON282:246 "**97 addresses in a 1,132-byte block at `02CB7FD0`**" vs CON282:321 "**97 distinct `.data` addresses**, and **86 of them fall in one span**". The TSV agrees with 86. Also CON282:335 "Three of the 88 nudged addresses".
- Block reader count: TUNES:96-97 "**The function count of 25, and every identification below, are unaffected.**", TUNES:762 "The function counts — 25 here", TUNES:785 "**Take 25 as a floor**" vs TUNES:90-92 "**28 referencing functions, 24 of which access the block**" *(corrected 2026-09-30)*. Favoured 28/24. The 25 stays unstruck at 96, 762 and 785.
- Labels: C-CON:67 "**293** (ids 1–294)" vs CON282:270 "the id space is one array of 294 rows".
- Adapter: CON282:262 "the three-instruction adapter `001CD040`" vs CON282:505, which quotes four instructions.
- `005DC580` offsets: TUNES:550 "`005DC580` writes 43 offsets" vs `map-lighting-tuning-02cb7fd0-accesses.tsv`, 45 distinct write displacements (uncited file).
- Event paths: EVSLOT:108-109 "the US table alone carries 284 such paths including 39 `sum_`, 15 `0001` and one `spc_`" vs EVSLOT:197-201 "329 event-script paths … 13 are `sum_<x>0001` … 1 is `spc_z0000` … 26 are other `sum_` names … 289 set nothing".
- cbuffer variables: CON282:250 "154 variables" vs 148 distinct names in `scenewide-cbuffer-map.tsv` (stored ones only).
- Directory size: C-CON:31 "the directory holds **thirteen documents**" vs 16 `.md` files now (adds the contract, ARM-CATALOGUE-WORK-DIVISION and EVSLOT).
- Withdrawn split: CMDNAMES:81 "the withdrawn **102 / 71**" vs CON282:90-92 "110 | 63".

#### 3.1.C10 Counts that disagree: Developer tuning console: the arm catalogue (work division and slices A-I)

- ARM-A:114 "touching **26 distinct fields**" (also ARM-A:213, ARMDIV:201, ARMDIV:231) vs ARM-A:237 "classifies eighteen of the thirty offsets" and ARM-A:241-249 (4 + 14 + 12 = 30).
- ARM-A:296 five `01DF6E48` readers vs ARM-A:301 parser + "three siblings" (4) vs consumers TSV (4); ARM-A:303 "five JSON readers".
- ARM-B:198 "The 16 "other" arms" vs ARM-B:200 "**twelve** arms `other`" (self-corrected 2026-09-25).
- ARM-B:37 "thirteen … walk a floating-point value … by a hundredth" vs ARM-B:129 two of them at `0.001`.
- ARM-B:179 "68 slots are touched" in `02CB8000`–`02CB8120` (73 dwords ⇒ 5 untouched) vs ARM-D:380-381 "**Only four dwords in the whole span are unreferenced**".
- ARM-D:376 "all 89 dwords from `02CB7FE8` to `02CB8144`" vs (0x8144 − 0x7FE8)/4 + 1 = 88.
- ARM-D:37 & ARM-D:112 & ARM-D:253 & ARM-D:404 "Thirteen"/"13 accessor arms" vs ARM-D:110 "Twelve float fields" / 12 table ids (self-flagged ARM-D:128).
- ARM-C:52 "the other 24 float arms are unbounded" vs 27 float arms − 2 clamped = 25.
- ARM-E:331 "the 21 `Map Eye` / `Map BGNPC` / `Map Hair` **floats**" vs 23 such float rows (ids 140–146, 148–151, 153–164; ARM-E:86-110).
- ARM-E:168-169 "named 21 offsets … **Twenty of those 21 have a console arm**" vs TUNES:367 "**21 of the 86 console-arm addresses now carry a name.** The other 8 named offsets … have no console arm" (29 named).
- ARM-H:39 "Fourteen rows show the selected party member's stats and the game's running counters" vs ARM-H:44/105 "**Fifteen**" (236, 237, 246–258).
- ARMDIV:378 "**21-25 float arms use `addss`/`addss`**" vs ARMDIV:382 per-slice 25 + 21 + 1 = 47 (History section; ARMDIV:44 supersedes with 47).
- ARMDIV:382 per-slice line "F 0" vs ARMDIV:45 "+ ids 173 / 174" in the signed `ADD/ADD` 50.
- ARM-A:338 etc. "duplicate labels … **0 of 283**" vs ARMDIV:43 "293 non-empty" labels + id 298 (populations differ: 282 + id 294).
- CMDNAMES:44 "**293 labels, ids 1-294**" omits ARMDIV:43's id 298 label (2026-09-13).

### 3.2 Stale "not read / open" claims, struck-but-repeated text, and banner disagreements

These do not change a value; a re-implementer would only be misled about what is known or about a page's status.
"Answered by" names the dated line that settles it where there is one.

#### 3.2.1 Boot fixups, startup data construction and the application root

| id | stale or banner text (quote+cite) | answered or contradicted by (quote+cite, dated) |
|---|---|---|
| C-S1 | README:14 "**PARTIAL, tier 1.**" (System-Stop-Registry) | STOP:4 "status: AUDITED — … answered 2026-09-17" |
| C-S2 | README:25 "**PARTIAL, tier 1.**" (FLOAT) | FLOAT:4 "status: DOCUMENTED — … owner read 2026-09-30" |
| C-S3 | README:29 "**DOCUMENTED, tier 1.**" (APP) | APP:4 "status: AUDITED" |
| C-S4 | README:33 "**DOCUMENTED, tier 1.**" (VTIDX) | VTIDX:4 "status: AUDITED" |
| C-S5 | README:37 "**DOCUMENTED, tier 1, one falsification pass.**" (OWN) | OWN:4 "status: AUDITED" |
| C-S6 | README:45 "**PARTIAL, tier 1.**" (EEVU) | EEVU:4 "status: DOCUMENTED — … Re-statused 2026-09-29 (FABLE)" |
| C-S7 | README:50 "**DOCUMENTED, tier 1, one falsification pass.**" (WB) | WB:4 "status: AUDITED" |
| C-S8 | README:59 "**DOCUMENTED, tier 1.**" (HUBS) | HUBS:4 "status: AUDITED" |
| C-S9 | README:64 "**DOCUMENTED, tier 1.**" (TICK) | TICK:4 "status: AUDITED"; TICK:8 "readiness: BEHAVIORALLY UNDERSTOOD" |
| C-S10 | README:25-26 "197 functions / 522 KB of generated float math that build 75 objects" | FLOAT:70-74 "There are **66** objects, not 75. The 65 builders total **32,848 bytes**, not 522 KB" and "the values are **not computed**" (falsification 2026-09-02) |
| C-S11 | README:31 "Never deleted, hence no stated object size." | APP:293-294 "**BE-4 ANSWERED — exactly `0x1140` = 4,416 bytes**" (falsification 2026-09-02, APP:371-374) |
| C-S12 | README lists 9 systems (README:13-68); folder also holds GATE, FORCE, MODE, LOG, DUP, ONES, EID, CLS, QREC, BASIS, ABI, SAVE, PRIM, RTTI, NBR, console pages and 6 CONTRACT pages | not listed (index incomplete; no dated note) |
| C-S13 | FLOAT:55 "**Status is `PARTIAL` deliberately.**" | FLOAT:4 "DOCUMENTED … owner read 2026-09-30"; FLOAT:56-58 itself says status waits for the owner read |
| C-S14 | FLOAT:37-39 "The boxes below stay unticked until the question ledger is free" | FLOAT:38-39 "*(Stale since: every box in §7 is ticked …; noted 2026-09-30)*" |
| C-S15 | FLOAT:18/21 last_reviewed / last_pass 2026-09-02 | dated edits to 2026-09-30 (FLOAT:4, 171, 202, 316) |
| C-S16 | FLOAT:645 "the header initialiser §12 already counts at 40 call sites" | no §12 on the page (sections 1-8, 10, 9, 11) |
| C-S17 | BOOT:22 audit.last_pass 2026-09-03; BOOT:18 last_reviewed 2026-09-30 | page has 2026-10-01 section (BOOT:540) |
| C-S18 | BOOT:90-91 "`00379CF0` is a **5-byte thunk** … and is **not in the function list**" | BOOT:240 "listed in the function list since this page was written" |
| C-S19 | BOOT:162 "**what they are is not established by this function.**" | BOOT:170-178 "*RC-3 answered 2026-09-30*" |
| C-S20 | BOOT:152-153 "what the extra tail bytes serve is not established" | BOOT:159-160, 301-306 "RC-2 … ANSWERED 2026-09-30" |
| C-S21 | BOOT:181-182 "**Whether id 10 is registered elsewhere or does not exist is not answered here**" | BOOT:183 "*Answered 2026-09-30 (SWE2-CONTRACT), static: no code in the image registers id 10.*" |
| C-S22 | BOOT:379 "What `02064ACC` feeds is not established here." | BOOT:382 "**Its one reader is the field frame … (answered 2026-09-30 …)**" |
| C-S23 | BOOT:220 "**Not read: the tempering constants**" | BOOT:220 "*Read since (cited 2026-09-30 …)*" |
| C-S24 | BOOT:405 "`00259180` (the RNG stream seed — one of two `022D9138` writers, §"random number generator")" | BOOT §"random number generator" (BOOT:35-93) discusses only `00863D30` / `02EB4234`; `022D9138` is "RNG enable/mode" per WB:224 |
| C-S25 | C-BOOT:138-139 "**what they are is not established by this function**" (two allocations) | BOOT:170-178 RC-3 answered 2026-09-30 |
| C-S26 | C-BOOT:140-142 "**Whether it is registered elsewhere or does not exist is unanswered**" | BOOT:183 answered 2026-09-30 |
| C-S27 | C-BOOT:101 "**What the tail bytes are *for* is still open**"; C-BOOT:480-482 | BOOT:301-306 RC-2 ANSWERED 2026-09-30 |
| C-S28 | C-BOOT:483-488 §14 unresolved: two allocations, "Whether pool id 10 exists" | BOOT:170-178, 183 (2026-09-30) |
| C-S29 | C-BOOT:15 last_reviewed 2026-09-29 vs C-BOOT:21-22 `by: OPUS` / `date: 2026-09-20` | C-BOOT:18 last_pass 2026-09-29 (internal mismatch) |
| C-S30 | C-BOOT two sections numbered "### 13d" (C-BOOT:336 and C-BOOT:365) | — |
| C-S31 | C-BOOT:386 "**§13c already established that no allocation return is ever tested**" | the finding is in §13b (C-BOOT:226-234); C-BOOT:496 also says "§13b" |
| C-S32 | APP:18/21 last_reviewed / last_pass 2026-09-02 | dated edits to 2026-10-01 (APP:2121, 2404) |
| C-S33 | APP:291-292 "What the base class *is* remains open, and is carried below." | APP:295-296 "**BE-5** … **ANSWERED — `Phyre::PFramework::PApplication`**" |
| C-S34 | APP:302-305 "The remaining seven … need runtime or authored evidence from outside the executable"; APP:582 "The remaining seven need runtime evidence" | APP:313-315 "*ANSWERED 2026-09-27 …: all 13 have a role read from code.*" |
| C-S35 | APP:318 "Five remain uncharacterised by role." | APP:313 ANSWERED 2026-09-27 (all 13) |
| C-S36 | APP:640 "`00199790` →`[01F810F0]` (the BE-2 focus singleton's global)" | APP:264 "*The byte is the pause flag.*" (BE-2 ANSWERED 2026-09-12) |
| C-S37 | APP:654 "the still-unnamed `0x238` singleton" | role answered APP:495 (2026-09-26) — name still unclaimed, so only partly stale |
| C-S38 | APP:1025, 1031 "SWE2-EC7-18 update (2026-05-15)", "SWE2-EC7-19 update (2026-05-15)" | date precedes all other page work (2026-09); likely mis-dated |
| C-S39 | APP:820 and APP:824 identical "Script_VM_Native_Bridge — CLIENT (45 edges)" bullets; APP:2310 and APP:2314 identical `001A09E0` paragraphs | duplicates |
| C-S40 | APP:827 "`001D7A20` … the body §"render pass" names as running "from the slot-4 pump through" the pass list" | APP:276-277 says `001D7A20` is "from the slot-4 pump through `001D8AB0`", and `001D72F0` is the pass-list one |
| C-S41 | `boot-singleton-01f7f598-accesses.tsv` has 22 ctor rows at `+0xB08`…`+0xD08` | APP:1046-1048, 1061-1062 call those spans "unobserved" before 2026-09-18 (instrument scope differs; TSV not cited) |

#### 3.2.2 World tick, field frame and force-fight mode

| id | stale or banner text (quote+cite) | answered or contradicted by (quote+cite, dated) |
|---|---|---|
| C-S42 | "three unread gates that skip the tick entirely" (TICK:59) | EX-6 "ANSWERED 2026-09-12 (FABLE)" (TICK:920); C-TICK:198-200 struck "stale" 2026-09-22 |
| C-S43 | "**those gates are unread** and this contract does not claim what they test" (C-TICK:151-152) | C-TICK:198-212 (struck/answered 2026-09-22) — §10 left unstruck |
| C-S44 | "whether ordinary callbacks change the mask during a pass is not established (`EX-9`)" (TICK:93-94) | "ANSWERED 2026-09-18 (FABLE)" (TICK:956) |
| C-S45 | "\| What the unread callees do \| **not established** \| — \| UNKNOWN \|" (TICK:978) | EX-3 "ANSWERED 2026-09-12 (FABLE)" (TICK:865) |
| C-S46 | "Bits 1 / 3 / 24 setters and clearers; bit 16 has none" (TICK:977) | "**Bit 16 answered 2026-09-12 (FABLE)**" (TICK:941) |
| C-S47 | "the widget constructor reads it for exactly that reason" (TICK:762) | getter has "12 call sites in 12 bodies" (C-TICK:222, CLOSED 2026-09-23) |
| C-S48 | `02089340` row "6 script-driven" (TICK:430) | §2.5 bit 6 "**a treasure is being opened**" (TICK:336; FZ-1 2026-09-11, TICK:772) |
| C-S49 | "The `02098E10` cell is the shared stop-registry context" (TICK:1272-1273) | "actor-manager slot array at `02098E10`" (TICK:63); C-STOP:217 |
| C-S50 | `001EC690` "~~`01F832C4` flag read~~" corrected (TICK:487) | struck with dated correction 2026-10-01; TICK:1103 agrees — fine |
| C-S51 | `0051E800`/`0051E840` "~~set `+0x128` `=1`~~" (TICK:466) | corrected 2026-10-01 and TICK:1213-1214 agree |
| C-S52 | `00392710` struck (TICK:706) | corrected 2026-09-28 — fine |
| C-S53 | "~~12 / 15 / 16 / 17 / 19~~" (TICK:870-871) | corrected 2026-09-21 (TICK:877-883) — fine |
| C-S54 | "`0x18`" latch and "`0x0B`/`0x18` … what each opens on screen is still the router page's open item" (TICK:244-245) | EX-2 "ANSWERED 2026-09-12 (FABLE)" (TICK:840) |
| C-S55 | "**Correction to the static read**: the `267310` gate is inverted — `test eax; je` *skips* the slot calls." (C-TICK:185-186) | TICK:103/TICK:565 already state skip when byte == 0; the correction names no page claim it overturns |
| C-S56 | "Which actor managers slots 3 and 4 hold is not established here." (C-TICK:108) | TICK:183-184 "sub-steps 1–15 exist for the cutscene managers (slots 1–4)" (2026-09-11) — partial answer |
| C-S57 | "(its meaning is not named on this page)" re `00265680` (C-TICK:316) | TICK:930-933 decodes `00265680` (EX-6, 2026-09-12) |
| C-S58 | "the null predicate the same page names" / "the null predicate `00253B90`" (TICK:217, TICK:947) | FORCE:60-63: `00253B90` is the force-fight `flag == 0` predicate (FORCE AUDITED); TICK never names force fight |
| C-S59 | main loop `0022A770` (STOP:49) | TICK:54 `0022A770` is the field frame; main loop is `0022B8C0` (TICK:55) |
| C-S60 | `last_reviewed: 2026-09-10` (TICK:16), `last_pass: 2026-09-12` (TICK:19) | page carries dated edits to 2026-10-01 (TICK:466, TICK:1091) |
| C-S61 | TICK `status: AUDITED` (TICK:4) | README:63-64 "**DOCUMENTED, tier 1.**" |
| C-S62 | `last_reviewed: 2026-09-02` (FORCE:18) | dated edits 2026-09-11..2026-09-21 (FORCE:13, FORCE:170, FORCE:183) |
| C-S63 | FORCE `status: AUDITED` (FORCE:4) | body banner "**DOCUMENTED.**" (FORCE:32); FORCE is not listed in README (no "force" in README) |
| C-S64 | "\| `BattleUnit_UpdateCombatFrame`, `FUN_0030C010` \| unread \|" (FORCE:117) | "AN-4 ANSWERED 2026-09-12 (FABLE)" (FORCE:183) |
| C-S65 | "\| `00252C80` \| the second writer — 134 B, unread \|" (FORCE:148) | AN-2 answered (propagated 2026-09-11) (FORCE:177-180) |
| C-S66 | "What they are remains open" (FORCE:280) and "`FUN_00252C80` (the second writer, still unread)" (FORCE:271-272) | AN-1 "ANSWERED 2026-09-17" (FORCE:170, FORCE:277); AN-5 (FORCE:272-273) |
| C-S67 | "What those two bytes are is answered in §5" fine; but "`0027768A` … writes `0208F570`, the shared mode-state field this page's §5 documents" (FORCE:295) | FORCE §5 (FORCE:165-199) never mentions `0208F570` |
| C-S68 | "presentation `00308130` calls `00253B90`" (FORCE:301) | FORCE:330 lists `BattleUnit_ComputePartyBattleStance` (00308130) under Gameplay |
| C-S69 | "*Not read:* the identity of the `0208E6A4` handle" (FORCE:198) | TICK:330 "arms the one-shot at `0208E6A8` with a handle at `0208E6A4`; its caller `00306B10` … registers `00306560` for a unit's handle"; MODE:400 (owner registration) |
| C-S70 | "`00253B90` gate the paths and are **not read**" (NBR:160) | FORCE:60 whole 12-byte body read (2026-09-02) |
| C-S71 | SWE2-EC7-18/19 sections dated "2026-05-15" (TICK:1699, TICK:1707) | predate the page's own `last_reviewed: 2026-09-10` and surrounding 2026-09 sections — date anomaly |

#### 3.2.3 Per-frame update gate and system stop registry

| id | stale or banner text (quote + cite) | answered or contradicted by (quote + cite, dated) |
|---|---|---|
| C-S72 | GATE `last_reviewed: 2026-09-11` (GATE:17); `last_pass: 2026-09-13` (GATE:21) | dated edits to 2026-09-30: "re-read 2026-09-30, SWE2-CONTRACT" (GATE:416); 2026-09-25 sections (GATE:409-415, 510) |
| C-S73 | C-GATE `last_reviewed: 2026-09-11` (C-GATE:17) | edits to 2026-10-01 ("(OPUS, 2026-10-01)", C-GATE:418, 1790) |
| C-S74 | STOP `last_reviewed: 2026-09-12` (STOP:10); no `readiness:` field (STOP:1-17) | edits to 2026-10-01 ("(OPUS, 2026-10-01)", STOP:818) |
| C-S75 | README: STOP "**PARTIAL, tier 1.**" (README:14) | STOP front matter "status: AUDITED" (STOP:4) |
| C-S76 | README: "seven per-actor stop sets (movement, script execution, animation rate, …) … switches audio groups, character culling, UI and input words" (README:16-18) | "*(a label this row should not have kept - corrected 2026-09-19, FABLE: **the value is an opacity, not a rate.**…*" (STOP:203); A29 pair "not a UI pair but the **pad-vibration pause and resume**" (STOP:299, answered 2026-09-17) |
| C-S77 | README lists no entry for the Per-Frame-Update-Gate page or C-GATE (README:11-40, grep) | GATE exists with status AUDITED (GATE:4) |
| C-S78 | GATE §10: "Both now have one, and neither is answered." (GATE:279) | "**DZ-2 ANSWERED 2026-09-11**" (GATE:247); DZ-1 answered by "***ANSWERED 2026-09-17 (FABLE): the node is the target-line object…" (GATE:225) |
| C-S79 | GATE: "**The route it must take is visible one address away.**… it names where to look next." (GATE:289-300) | "**Closed 2026-09-11 (OPUS-CONTRA-GATEWORD…)** The registry route does not reach the word" (GATE:308-309) |
| C-S80 | GATE: "**No name is proposed for the node type.**" (GATE:207) | UQ-25 answered 2026-09-17: "the node is the target-line object" (GATE:225) |
| C-S81 | GATE: "**Which field uses which is not established.**" (GATE:185) | UQ-27 "ANSWERED 2026-09-17 (FABLE): no field is in thousandths of a degree" (GATE:252) |
| C-S82 | GATE: "the head of `DT-1`'s list of 112" (GATE:160-161) | UQ-29 "ANSWERED BY CITATION 2026-09-17 … of the 139 residual functions **131 are cited**" (GATE:256) |
| C-S83 | GATE: "Whether it is retired, reserved, or handled elsewhere is **not established**." (GATE:79-80); C-GATE:155-156 repeats it | UQ-26 "NO ADMISSIBLE SOURCE — reviewed and signed 2026-09-16" (GATE:227); C-GATE:284 "closed 2026-09-22" |
| C-S84 | GATE duplicated bullet "**Script_VM_Native_Bridge — CLIENT and SERVICE (15 edges).**" (GATE:419 and GATE:421) | — (duplicate) |
| C-S85 | C-GATE duplicated paragraph "The check that would matter needs a modified word…" (C-GATE:272-275 and 277-280); C-GATE:273 says "§9 says nothing in the image writes the word" | the claim is in §10 (C-GATE:171-178) |
| C-S86 | C-GATE §14: "~~What `0x0010` was for~~" etc., all closed 2026-09-22 (C-GATE:284-311) | — (consistent) |
| C-S87 | C-GATE: "the 3,862 are where it will not" (C-GATE:1335-1336) | "**The residue is at most 3,079 bytes in 191 spans**, not 3,862." (C-GATE:1288, "CORRECTED SAME DAY") |
| C-S88 | STOP: "a **UI** bit pair `0035B4B0(5)` / `0035B510(0xFF)` on A bit 29" (STOP:185) | "*A bit 29*, … not a UI pair but the **pad-vibration pause and resume**" (STOP:299, ANSWERED 2026-09-17); C-STOP:282-283 "an **owner in that layer, not UI**" |
| C-S89 | STOP: "requester bitsets whose consumers are not read here" (STOP:186-187) | SM-3 "***ANSWERED 2026-09-17 (FABLE): every listed consumer is named…" (STOP:299) |
| C-S90 | STOP set-5 "animation"/"rate" labels: column header "5 animation" (STOP:106); "animation set 5" (STOP:143); "the apply's rate-1.0 animation path" (STOP:155); "the set-5 animation-rate machinery" (STOP:219); "rate arm, 0.0" / "rate arm, 1.0" (STOP:226-227); "animation hook" (STOP:230) | "corrected 2026-09-19, FABLE: **the value is an opacity, not a rate.**" (STOP:203); "no reader uses it as a simulation rate" (STOP:213-214); struck row STOP:333 |
| C-S91 | STOP: "## SWE2-EC7-18 update (2026-05-15)" (STOP:535) | dated four months before the page was authored, "Authored by FABLE, 2026-09-12" (STOP:27) |
| C-S92 | STOP labels render-record functions as registry bodies: "`00477B10` (889 B) is the stop-registry row accessor - `cl*64` row into `02CA6CA0`" (STOP:545); "`00423B10` … is the registry's record enumerator" (STOP:541) | `02CA6CA0` is "the **packed channel table**" for add-motion (STOP:457, 294); a parallel correction for `0051CC30` "is not a system-stop body" (STOP:561, 2026-09-19) |
| C-S93 | STOP duplicated `0035C750` paragraph (STOP:794 and STOP:798); duplicated PlatformOnlineAchievements bullet (STOP:450 and STOP:453) | — (duplicate) |
| C-S94 | STOP: "the id dispatch at `00225E44`–`00225E5F` is not tabulated here" (STOP:84); C-STOP:285-286 "the page does not tabulate the cancel's id dispatch either" | EXP-191 tabulates the `00225EB0` dispatch "(`0`→`2DDC30`/`182DA0`, `0xC`→`182D60`, `0xD`→clears recB bit41 then `182D40`, `0xF`→`182D40`)" (C-STOP:213-214), for the sweep, not the cancel |
| C-S95 | STOP manager count "~~1 or 3 managers by record A bit 30~~" (STOP:61) | corrected in place 2026-09-12 (STOP:61-63); C-STOP SS-7 agrees (C-STOP:131-134) — resolved, no unstruck repeat found |
| C-S96 | C-STOP: "the world tick and field frame remains uncontracted and this document does not claim it" (C-STOP:34-35); "**Uncontracted** \| the world tick and field frame" (C-STOP:148) | C-TICK exists: `Battle-Frame/CONTRACT-world-simulation-tick.md`, `method: address-resolution verification 2026-09-22`, `last_reviewed: 2026-09-29` (C-TICK:12, 20) |
| C-S97 | C-STOP `crossref_clean: false` (C-STOP:26); C-GATE `crossref_clean: false` (C-GATE:22) | — (banner) |
| C-S98 | C-GATE: "Two of the seven — `_5380` … and `_8FA0` … are passed to no handler at all" struck (C-GATE:473-476); GATE:476 struck | corrected 2026-09-18 (C-GATE:478) and 2026-09-25 (GATE:562-570) — struck in both places |
| C-S99 | GATE §8 evidence row "| bit `0x0010` is unused | no `test` with that mask anywhere in the function |" (GATE:263) | widened image-wide by UQ-26 (GATE:236-239) — consistent, scope stale |

#### 3.2.4 Battle runtime mode ladder, diagnostics log, duplicated names, all-ones convention

| id | stale or banner text (quote+cite) | answered or contradicted by (quote+cite, dated) |
|---|---|---|
| C-S100 | MODE:35 "**PARTIAL.** The ladder, its inputs and its persistence are read at tier 1." | MODE:5 "status: AUDITED … status line brought up to date 2026-09-18 (FABLE)" |
| C-S101 | MODE:18 `last_reviewed: 2026-09-12`, MODE:21 `last_pass: 2026-09-02` | dated edits MODE:357 (2026-09-14), MODE:427 (2026-09-19), MODE:731/740 (2026-09-25) |
| C-S102 | MODE:153-154 "**Bits 0 and 1 have no script verbs at all** — the complementary evidence that they are engine-internal, driven by UI and combat" | MODE:289-290 "**The two unnamed bits have script verbs after all**" (2026-09-12); MODE:545-546 "**ANSWERED 2026-09-12:** both have verbs" |
| C-S103 | MODE:506-507 "**All four bits are live, but from different places.** Bit 0 is UI, bit 1 is combat/audio" | MODE:110-111 "corrected 2026-09-12, §2c"; MODE:185-187 "(Diagram and sentence corrected 2026-09-12, OPUS-CONTRA-LADDER-LABELS…)" |
| C-S104 | MODE:665-669 "a script outranks authored area data which outranks combat which outranks UI … **O-4 stays open**" | MODE:515-517 "**ANSWERED 2026-09-12 (FABLE):** … **O-4.**" |
| C-S105 | MODE:543-544 "which of entry 3's readers (`0031B950`, `BattleSlotMap_ResolveMappedBattleSlot`, five more) an event script relies on is not read" | C-MODE:386-387 "**ANSWERED 2026-09-22 (SWE2-CONTRACT) — the reader is the party-read-in state machine `0037B4D0`**" |
| C-S106 | MODE:305 "the battle-menu builder, the target cursor — is asking *"is the party riding a chocobo?"*" (as callers of `00303EC0`) | MODE:204 "`FUN_00313DB0` — tests `== 2` **inline**, without the wrapper" |
| C-S107 | MODE:1004-1019 and MODE:1021-1036 — the same `00303F00`/`00304060` section twice | — (duplicate block) |
| C-S108 | MODE:1059 "SWE2-EC7-19 update (2026-05-15)"; DUP:421 same | dates earlier than both pages' own creation-era dates (2026-09-xx) |
| C-S109 | MODE:1083-1085 "`00254B50` — the mode-ladder body proper" ; MODE:1369 "`0035D6B0`/`0035D8D0`/`0035D980`/`0035DA80` ladder quartet" | MODE:1089 "`00254B50` (263 B) is the body … `ecx & 0x7FFF` is the request id" (a UI request executor); C-MODE:469 "`00254B50 ← 00253C50/00254B40/002E09A0`" |
| C-S110 | MODE:232 "`WorldTransitionSnapshot_RestorePersistencePairForActor` (`005843E0`)" | MODE:588 / MODE:962 "`WorldTransitionSnapshot_RestorePersistencePairForActiveSlot` (005843E0)" |
| C-S111 | C-MODE:6 `readiness: CONTRACT READY` | C-MODE:263-264 "Live capture: still absent, and that is the gate this subsystem fails." |
| C-S112 | C-MODE:521 "| any execution of this operation, isolated or live | **none**; §13 | none | UNKNOWN |" | C-MODE:266-269 "**Executed 2026-09-12** … **55 comparisons, 0 mismatches**"; C-MODE:343 executed 2026-09-26 |
| C-S113 | C-MODE:579 "**The four setters are still not driven**" | C-MODE:343-349 "**The setters, the reset, the getters and the save round trip are executed since (2026-09-26 …)**" |
| C-S114 | C-MODE:117 "`003148F0` — whose result is used as the row index and whose body is **not read here**"; C-MODE:241 "/* the active field index; body not read */" | C-MODE:334-336 (2026-09-18) "**The negative-index clamp is in `003148F0`** … `00314903 cmovs eax, ecx`"; HUBS:293 "(`003148F0`, 27 B) reads **one** field — the persistent payload's dword `+0x1044`" |
| C-S115 | C-MODE:162 "/* the fourth slot - the guest's */"; C-MODE:171 "loses the ride timer, the guest slot and the event" | MODE:322 "**Roster slot 3 is the mount.**" (§2c, 2026-09-12); C-MODE:478 "**ANSWERED 2026-09-15 (OPUS) — it does nothing to the guest slot**" |
| C-S116 | C-MODE:17 `last_reviewed: 2026-09-12`, C-MODE:22 `crossref_clean: false` | dated edits C-MODE:82 (2026-09-26), C-MODE:386 (2026-09-22), C-MODE:642 (2026-09-18) |
| C-S117 | C-MODE:625 and C-MODE:629 — identical "Script_VM_Native_Bridge — CLIENT and SERVICE (48 edges)" bullets | — (duplicate) |
| C-S118 | C-MODE:34-38 says the two stale MODE statements are "routed rather than repeated" (`OPUS-CONTRA-LADDER-LABELS`) | MODE:506-507 still carries "Bit 0 is UI, bit 1 is combat/audio" unstruck |
| C-S119 | C-MODE:502 "*Not claimed:* what `[record + 0x284]` is." | outside 00, not audited: `17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md:209` "+0x284  u32   objectFlags" |
| C-S120 | (outside 00, cited by MODE:310/536) `11-Party/Battle-State-Block/the-battle-state-block-field-map.md:120` "**the mode flags** — bit 0 UI, bit 1 combat / audio" | MODE:518-521 "**ANSWERED 2026-09-12:** bit 0 the summon … bit 1 the chocobo" |
| C-S121 | LOG:17 `last_reviewed: 2026-09-08` | LOG:25 "promoted: 2026-10-01"; edits LOG:112, LOG:177, LOG:191 (2026-09-30) |
| C-S122 | LOG:28/30 title and filename "level-gate" | LOG:31 "**there is no level gate** (§9, 2026-09-13)" (kept deliberately) |
| C-S123 | LOG:176 "**What the channel id means**, or its range." ; LOG:201 "what the other channel ids mean stays open" | LOG:177 "**Answered functionally 2026-09-30 (SWE2-CONTRACT):** channel **4** is the debugger-break channel"; LOG:191-193 RC-9 answered 2026-09-30 |
| C-S124 | LOG:342-345 "**Not claimed.** Which class the sink is … What `02EBA3D0` holds. Whether any caller of `005CDAA0` is itself gated" | LOG:347-349 annotation; LOG:201 (2026-09-18); LOG:78 (2026-09-21); LOG:354 RC-10 answered 2026-09-30 |
| C-S125 | DUP:20 `last_reviewed: 2026-09-03` | DUP:264 pass 2026-09-13; DUP:373 2026-09-14 |
| C-S126 | DUP:83 "the thunk is identifiable without ambiguity" | DUP:86 "**Not without ambiguity — the rule misses the one chain §2 counts (2026-09-13, §9).**" |
| C-S127 | DUP:107 "~~while their thunk has some~~" (struck) | DUP:111 "**Corrected 2026-09-13 (§9): the 30 is right; the clause holds for 13 of them.**" — consistent |
| C-S128 | ONES:19 `last_reviewed: 2026-09-03` | ONES:145 reconciled 2026-09-30 |
| C-S129 | ONES:371 "What `+0xB8`/`+0xB9` and `+0x412` *hold* is still unread" | ONES:145 "*(Reconciled 2026-09-30 (FABLE …): that item is UQ-218, ANSWERED 2026-09-30 … so this half is no longer open.)*" (for `+0xB8`/`+0xB9`) |
| C-S130 | ONES:71 "adjacent handle pair `+0x695`, `+0x696` \| 1 \| released \| `16-UI`" | ONES:139-140 "`+0x695` is `presentationSlot1` and `+0x696` `presentationSlot2`" (2026-09-13); ONES:237 "`0030688B  mov byte ptr [rbx + 0x696], al   ; hand the handle across`" |
| C-S131 | README:13-68 lists no Battle-Runtime-Mode, Diagnostics-Logging, DUP or ONES page | front matter of all five pages: AUDITED |
| C-S132 | APP:894 "a 0x4050-byte frame under `_chkstk` (`00808F10`)" | LOG:165 "`00808F10` \| `_alloca_probe`" (same function, two names; MODE:683 also `_alloca_probe`) |

#### 3.2.5 Encoded-id space, class registry, query record, basis helpers, ABI recovery

| id | stale or banner text (quote+cite) | answered or contradicted by (quote+cite, dated) |
|---|---|---|
| C-S133 | EID front matter "independent acceptance pending" (EID:4) | "SECTION-05 is accepted by a non-author review … `verdict:ACCEPT`" (CLS:50-53, 2026-09-30 citing 2026-09-29) |
| C-S134 | C-EID "independent acceptance pending" (C-EID:14, C-EID:26-27) | CLS:50-55 (2026-09-29/30); C-EID's own OV-3 "NOT A QUESTION 2026-09-29" (C-EID:317) |
| C-S135 | QREC `status: PARTIAL`, "formal peer acceptance pending" (QREC:4, QREC:12) | "the same review accepts the query-record page (OV-9)" (CLS:54-55) |
| C-S136 | EID OV-5 open: "shipped-state reachability of unusual count/high-pointer/fourth-key-range cases, and formal independent acceptance" (EID:608-609) | "**CLOSED 2026-09-23 (SWE2-CONTRACT): both named anomalies are unreachable on shipped data**" (C-EID:250-251); acceptance CLS:50-55 |
| C-S137 | QREC "Shipped reachability of that fourth interval is not proven by this fixture." (QREC:179-180); OV-8 open (QREC:196) | C-EID:252-261 (2026-09-23): "ids ≥ `0x8200` can never validate on shipped data" |
| C-S138 | EID 02EBF008: "what those two do is unread, so the table stays unnamed (FY-7)" (EID:444) | "**Slot 0 named 2026-09-12 (FABLE):** the **movie fade schedule**" (EID:645-649) |
| C-S139 | EID 02EBF020 Potion/Elixir row retained in table text (EID:441, retracted inline 2026-09-12) | same line, "retracted 2026-09-12, FABLE" |
| C-S140 | CLS §5c: "a correspondence across two numbering schemes and is **not** an identity: no code was read that converts one into the other" (CLS:194-195) | "**`class = (id >> 12) + 5`**" (CLS:487, 2026-09-13); EID:98-101 (2026-09-11) |
| C-S141 | CLS §3 "Four documents … none of them could see the others' numbers" / §3 omits id bases (CLS:31-33, CLS:497-499) | CLS:490-492 id-base table (2026-09-13) |
| C-S142 | CLS "Only the `us` pack was decoded; other language packs are not checked" (CLS:376, CLS:540) | "the other eight language copies carry byte-identical authored tables" (EID:71; EID:659-660, 2026-09-11) |
| C-S143 | CLS owner_layer "CodeDomain — shared; no PrimaryOwner" (CLS:5) | "`00322C50` itself is Gameplay-owned" (CLS:211) |
| C-S144 | BASIS "**Cited by no document in this database.**" / "**Nothing in the database cites either address**" (BASIS:31, BASIS:113) | VTIDX:1409-1410 lists `0062DDE0`/`0062DFB0` as `PWorldMatrixFlyController` vtable slots 7 and 8 (undated row) |
| C-S145 | BASIS last_reviewed 2026-09-03 (BASIS:19) | dated sections 2026-09-14 … 2026-09-20 (BASIS:158-185) |
| C-S146 | EID last_reviewed 2026-09-22 (EID:19), audit last_pass 2026-09-12 (EID:47) | dated edits 2026-09-25 (EID:181, EID:187) and 2026-09-29 (EID:607) |
| C-S147 | CLS last_reviewed 2026-09-22 (CLS:19) | 2026-09-30 sections (CLS:50, CLS:58, CLS:225, CLS:327) |
| C-S148 | QREC last_reviewed 2026-09-22 (QREC:11) | falsification 2026-09-29 (QREC:203) |
| C-S149 | C-EID audit `last_pass: 2026-09-30` vs `date: 2026-09-21` (C-EID:17, C-EID:21) | internal |
| C-S150 | ABI "the 562 functions below are still in it" (ABI:38); audit "562 functions … analysed" (ABI:16) | "the frontier now holds **342**" (ABI:88, 2026-09-17) |
| C-S151 | ABI UQ-1 example "`002465F0` is the known case" (ABI:123) | "**`002465F0` IS NOT IN THE DATASET.**" (ABI:172) |
| C-S152 | EID "two snapshots"/census figures 76/14/14 vs 75/14/12 | "a drift the page already records" (EID:749-750) |
| C-S153 | README of 00 does not list any of the six pages (README:11-68) | pages exist in folder |

#### 3.2.6 Shared transform workbench (EE/VU0 register bank, save/restore, primitives)

| id | stale or banner text (quote+cite) | answered or contradicted by (quote+cite, dated) |
|---|---|---|
| C-S154 | WB:4 "status: AUDITED" | WB:485 "`DOCUMENTED`, one falsification pass."; README:50 "**DOCUMENTED, tier 1, one falsification pass.**" |
| C-S155 | WB:18 "last_reviewed: 2026-09-02" | dated edits to WB:105 (2026-09-26), WB:279 (2026-09-08), WB:315 (2026-09-12) |
| C-S156 | WB:40-41 "The ledger mirror is pending." | not answered on the page |
| C-S157 | WB:217 "row array (grouping beyond matrix 0 unproven, BQ-16)"; WB:480-481 "left open (BQ-16)"; WB:528-529 "Offered as a lead for `BQ-16`" | WB:304 "**BQ-16 ANSWERED**" (ticked 2026-09-13) |
| C-S158 | WB:563 "Whether anything ever does is `BQ-19`'s question, not answered here." | EEVU:271 "***ANSWERED 2026-09-18 (FABLE) — the pools carry no jobs, so the bank has exactly one user thread.**" |
| C-S159 | WB:186 "the only initializer" / WB:291 "It is the only thing that clears the area" | C-WB:247 shows it run from the rig frame `003E00C0` and `003DFFE0` (2026-09-29); not a boot-only initializer |
| C-S160 | EEVU:4 "status: DOCUMENTED" | README:45 "**PARTIAL, tier 1.**" |
| C-S161 | EEVU:12 "last_reviewed: 2026-09-14" | dated edits EEVU:225 (09-18), EEVU:261-262 (09-27/28), EEVU:370 (09-29) |
| C-S162 | SAVE:17 "last_reviewed: 2026-09-08" | edits SAVE:86 (2026-09-28), SAVE:269 (2026-09-27), SAVE:287 (2026-09-28) |
| C-S163 | SAVE:260 "what it selects is not established" | SAVE:292 "***ANSWERED 2026-09-17 (FABLE)***" (UQ-42) |
| C-S164 | SAVE:294 "the row's byte 1 (UQ-42) stays open" | SAVE:292 (UQ-42 answered same date) |
| C-S165 | SAVE:319 "what any of it is for | **not established** … UNKNOWN" | SAVE:294 "***ANSWERED 2026-09-17 (FABLE): colour arithmetic in the PS2 seven-bit convention***" |
| C-S166 | SAVE:320 "any runtime observation | **none exists**" | SAVE:298 UQ-45 "**SUPERSEDED** (2026-09-14 …)" |
| C-S167 | SAVE:46 quotes WB "**nothing restores it**" | WB:279 "**CORRECTED 2026-09-08**" |
| C-S168 | C-SAVE:28 "249 functions write one shared area and nothing restores it" | WB:279-285 (2026-09-08) |
| C-S169 | C-SAVE:17 "last_reviewed: 2026-09-11"; C-SAVE:6 "BEHAVIORALLY UNDERSTOOD" | C-SAVE:71, 83, 234 (2026-09-28 edits); C-SAVE:260 "**0 mismatches**" differential |
| C-S170 | C-SAVE:192 / C-SAVE:386 (struck) "no relationship to the workbench" | C-SAVE:192-195 "*Resolved 2026-09-23*" |
| C-S171 | C-WB:84-85 "*That grouping is `BQ-16` and this contract does not close it.*" | C-WB:178 "**CLOSED 2026-09-23**" |
| C-S172 | C-WB:192 "Whether any pair of borrowers can overlap in time (§10)." | EEVU:271 (2026-09-18) one user thread |
| C-S173 | C-PRIM:113-115 "`022D91A0` has 67 writers … `022D8F90` has 47 and 59" | C-PRIM:365 "**Replaced 2026-09-21 (SWE2-CONTRACT) with a defined instrument**" |
| C-S174 | PRIM:345-347 "**who consumes them is not**" | C-PRIM:269-280 "**Answered 2026-09-21 (SWE2-CONTRACT): yes — pervasively, but by the workbench family**" |
| C-S175 | PRIM:357-358 "What the live blocks … are … their meaning is not." | PRIM:224 "**Answered 2026-09-14 (FABLE, `BQ-16`)**"; C-PRIM:288 |
| C-S176 | PRIM:361-363 "That `00397910` is only a matrix multiply." | C-PRIM:302 "**Answered 2026-09-20 by a full line-by-line read: yes.**" |
| C-S177 | PRIM:17 "last_reviewed: 2026-09-08" | edits PRIM:174 (09-21), PRIM:604 (10-01), PRIM:1538 (09-30) |
| C-S178 | PRIM:805 "## SWE2-EC7-19 update (2026-05-15)" | date precedes every other dated line in the group (earliest otherwise 2026-09-02) |
| C-S179 | PRIM:1586/1594 and PRIM:1590/1598 duplicate `00276430`/`003F74F0` paragraphs; PRIM:553/557 two different "Script_VM_Native_Bridge" paragraphs; C-SAVE:487/488 duplicates; SAVE:303/327 two "## 9" headings | — |
| C-S180 | C-PRIM:11 "last_reviewed: 2026-09-17" | C-PRIM:295 "*(corrected 2026-10-01, OPUS …)*" |
| C-S181 | README:41-42 "a 660-byte buffer at `022D9198` … thirteen objects rather than one" | WB:439 "### CORRECTED: 62 objects, not 13" (2026-09-02); EEVU:113 |

#### 3.2.7 Object model (RTTI and the vtable method index)

| id | stale or banner text | answered or contradicted by |
|---|---|---|
| C-S182 | `last_reviewed: 2026-09-02` / `last_pass: 2026-09-02` (RTTI:22, 25) | dated edits to 2026-09-22: "**CONFIRMED 2026-09-22 (FABLE)**" (RTTI:190), "(FABLE, 2026-09-22)" (RTTI:248, 259) |
| C-S183 | `last_reviewed: 2026-09-02` / `last_pass: 2026-09-02` (VTIDX:19, 22) | "2026-09-28, applied by FABLE" (VTIDX:145); "SUPERSEDED 2026-09-26" (VTIDX:154) |
| C-S184 | "**Still open:** which *game* subsystem calls that narrow interface … **AS-1a.**" (RTTI:157-159) | "~~Which *game* subsystem calls Phyre's physics interface.~~ **ANSWERED as far as it can be**" (RTTI:367-368; §6 dated 2026-09-02, RTTI:464) |
| C-S185 | "~~**that reading is a lead, not a finding.**~~ … **Still open on the narrower point:** *battle* voice specifically" (RTTI:190, 200-201) | "**ANSWERED 2026-09-22 (FABLE): battle voice specifically**" (RTTI:382-383) |
| C-S186 | "**Still open:** whether Phyre's reflection glue (the descriptor instances) describes exactly these RTTI classes." (RTTI:462, narrowing dated 2026-09-14, RTTI:409) | "**GLUE HALF ANSWERED 2026-09-22 (FABLE)**" (RTTI:410) |
| C-S187 | "191 apart and not explained by these three. **AS-8.**" (RTTI:490-491) | "**AS-8 closed**" (RTTI:587) — itself contested, see C.1 |
| C-S188 | "- [x] Replace `vtable_map.py`'s `demangle()` … **AS-9.**" (RTTI:376-378) ticked with no answer; "**AS-9** tracks replacing the demangler" (RTTI:589-590) | "correcting the demangler does not move it" (RTTI:712-713); "**AS-9a is closed.**" (RTTI:892) — whether AS-9 itself was done is not stated |
| C-S189 | "Those are the real dispatch tables" (RTTI:670-671); "two of the largest are now documented" (RTTI:691) | "**Correction to section 8.** … **The largest of them is not a dispatch table at all**" (RTTI:706-708, undated) |
| C-S190 | RTTI §6 reads the three AS-7 qwords as slots "past the true end of three vtables" (RTTI:484-487) | §14: "**they are inline ASCII strings, not pointers**" in "Phyre's field-descriptor tables" (RTTI:888, 917) |
| C-S191 | "`BattleFormula_EvaluateTargetPreview` (`003859FF`)" / "`BattleFormula_ResolveTargetResult` (`003863D0`)" (RTTI:401-402) | function entries are `00385680` / `00385F60` (RTTI:683, 1002, 1009) — names attached to interior call sites |
| C-S192 | RTTI section numbering jumps §9 → §12 (RTTI:693, 710) | — (no §10/§11) |
| C-S193 | Links `members/rtti-class-vtables.tsv`, `members/phyre-registrar-classes.tsv` (RTTI:414, 438) | files live in `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/members/`; `Object-Model/members/` holds only the zero-at-load file |
| C-S194 | "**4,265 of the 4,275 sit at exactly one slot; 10 occupy two slots of the same class** — multiple inheritance, where a class has more than one vtable." (VTIDX:106-107); "multiple inheritance, 10 cases" (VTIDX:236) | "*Answered on the page 2026-09-14 (FABLE)…: neither — all ten are two virtual slots of the same single vtable*" and "The sentence … above is corrected by this." (VTIDX:157-158, 176-177) — still unstruck at VTIDX:106-107 and VTIDX:236 |
| C-S195 | BA-2 "**Nothing here has had its body read.**" (VTIDX:153) | "five families have been read so far" (VTIDX:2529-2530); ~250 bodies read in SWE2-EC7 updates dated 2026-09-19..21 (e.g. VTIDX:3365-5219); "SUPERSEDED 2026-09-26" (VTIDX:154) |
| C-S196 | "Following them would move essentially nothing out of the 9.9 %" (VTIDX:2611); "**3,395 functions holding 748 KB are reached by none of the three static routes**" (VTIDX:2588) and the `BattleMenu_…` example (VTIDX:2602) | "## 14. RETRACTION" — 351 fn / 1.0 % (VTIDX:2614, 2658); `002778C0` "is address-taken" (VTIDX:2629-2631) — only the table row VTIDX:2575 is struck |
| C-S197 | §14 "**88 KB**" residue (VTIDX:2675) | §14a: "§14's *"88 KB"* is at most about **64 KB**" (VTIDX:2747-2748; FABLE measured 2026-09-16, OPUS 2026-09-17, VTIDX:2700) |
| C-S198 | BA-1 "The 2,611 folded addresses' owners" (VTIDX:143) | "for the true owner of the 2,179 FOLDED addresses, 2026-09-28" (VTIDX:145) with INHERITANCE 320 / ONE-TEMPLATE-FAMILY 73 / STUB 39 answered (VTIDX:149) — 2,611 is reused unqualified at VTIDX:80, 135, 234, 2528 |
| C-S199 | `0068AF90` "`+0x70`/`+0x74`=1.0f" (VTIDX:3900) | its interior anchor "(the `+0x24` = 1.0f store)" (VTIDX:3900) names a field the line does not list |
| C-S200 | duplicate bullet "**Script_VM_Native_Bridge — CLIENT (1 edge).**" (VTIDX:2859) | repeated verbatim at VTIDX:2862 |
| C-S201 | "`FieldData_GetActiveFieldRecordBit15` (00313F60), `FieldData_GetActiveFieldRecordBit15` (00377C20)" (VTIDX:2861) | one name on two addresses — the DUP page's subject; unresolved here |
| C-S202 | README lists VTIDX (README:32-35) but **not** RTTI | RTTI is `status: AUDITED` (RTTI:4) |
| C-S203 | README: "Never deleted, hence no stated object size." (README:31) | APP:129, APP:361 (Falsification pass 1 - 2026-09-02, APP:340) |

#### 3.2.8 Shared-state accessors and the ownership boundary

| id | stale or banner text (quote+cite) | answered or contradicted by (quote+cite, dated) |
|---|---|---|
| C-S204 | HUBS key table: "`00362850` … not read" (HUBS:209) | TICK:893 "**`00362850` is the audio listener update:**" (TICK §7 EX-3) |
| C-S205 | HUBS key table: "`00233780` `SpawnKeep_RotatePersistenceBanksForAreaTransition` … not read" (HUBS:210) | NBR:445 "`SpawnKeep_RotatePersistenceBanksForAreaTransition` is the worked example, read in full" (2026-09-14) |
| C-S206 | HUBS key table: "— \| `SaveImage_GetPersistentPayloadBase` \| — \| — \| not read" (HUBS:212) | HUBS:331 "**U-5 ANSWERED 2026-09-12 (FABLE):** `002EF2B0` is …"; HUBS:606-612 (2026-09-18) |
| C-S207 | "The 49 callers of hub 2 include 21 with no owner tag … identifying them is **U-3**." (HUBS:418-419) | HUBS:297-298 "**U-3 ANSWERED 2026-09-12 (FABLE)**" |
| C-S208 | "recorded as **U-4** rather than dressed up as a runtime claim" (HUBS:416) | HUBS:325 U-4 "(closed — the register row is WITHDRAWN.)"; bounded 2026-09-22 (HUBS:327) |
| C-S209 | HUBS `last_reviewed: 2026-09-02` (HUBS:18) | dated edits to 2026-09-12/13/14/17/18/19/20/22/26 and "re-read 2026-09-30" (HUBS:948) |
| C-S210 | HUBS front matter `status: AUDITED` (HUBS:4) | README:59 "**DOCUMENTED, tier 1.**" |
| C-S211 | HUBS has two "## 9." headings ("## 9. Related" HUBS:421, "## 9. Falsification pass 2026-09-02" HUBS:430); HUBS:49 "Corrected 2026-09-02 (§9)" | structural only |
| C-S212 | NBR: "`0022AF50` sets to **3** and `0022B000` sets to **5** (§3 and §4)" (NBR:243-244) | NBR §3 is the audio chain (NBR:69) and §4 the class validator (NBR:108); no section of NBR describes those mode bodies |
| C-S213 | NBR `last_reviewed: 2026-09-14` (NBR:12) | dated edits 2026-09-15, 09-17 (NBR:326-332), 09-21 (NBR:84), 09-28 (NBR:178, 236) |
| C-S214 | NBR not listed in README "Systems in this category" (no README line names `the-shared-neighbours-pass-22-keeps-finding.md`) | NBR front matter AUDITED (NBR:4) |
| C-S215 | NBR §10.4 "the 922 denominator no longer exists" (NBR:432-433) | headline still states "130 of pass 22's 922" (NBR:24) — historical by NBR:433 |
| C-S216 | OWN `last_reviewed: 2026-09-02` (OWN:19); `last_pass_state:` is a sha (OWN:23) | dated edits through 2026-09-30 (OWN:537) |
| C-S217 | OWN body "### Status `DOCUMENTED`, one falsification pass." (OWN:488-490); README:37 "DOCUMENTED" | front matter `status: AUDITED` (OWN:4) |
| C-S218 | OWN "SWE2-EC7-18 update (2026-05-15)" (OWN:687) | date earlier than every other dated section of the page (2026-09-xx) |
| C-S219 | `003B8670` "has no document" (struck, OWN:304-308) | OWN:308 "**BQ-12 ANSWERED 2026-09-12 (FABLE)**" — correctly struck |
| C-S220 | Ownership of `002BAF80`: HUBS:316 "Input — `002B7B80`, `002BAF80` (the two 4.8 KB dispatchers)" | NBR:366-367 "`Presentation` `002BAF80`"; HUBS:883-886 Presentation |
| C-S221 | OWN "is a 660-byte buffer … written by **215 functions**" (README:41-42) | OWN:159-160 "the "660-byte buffer" is three separate 64-byte row blocks plus several unrelated slots" (2026-09-02) |

#### 3.2.9 Developer tuning console: dispatcher, tunables, second table, event slot, names

| id | stale or banner text (quote+cite) | answered or contradicted by (quote+cite, dated) |
|---|---|---|
| C-S222 | C-CON:297 "**Empty.** … nothing here has been observed running." | C-CON:139 "*(2026-09-25, FABLE, …, on OPUS block 315, which executed every id …)*" |
| C-S223 | C-CON:305-308 Unresolved 1 "Whether the 111 codes are area codes" and 2 "Why `dst0104` appears at two ids" | CON2:75-83 "**Answered 2026-09-30 (SWE2-CONTRACT): they are map-pack names** … fields 230 and 232 both load `dst0104.mpk`" |
| C-S224 | C-CON:311 Unresolved 4 "The eight-entry uniform array the console cannot reach" | TUNES:564 "**What the eight entries at `+190` are** — **eight shadow-map matrices**"; TUNES:568 UQ-24 "**cascades**" (2026-09-16) |
| C-S225 | C-CON:19 `last_reviewed: 2026-09-21` | dated edits at C-CON:77 (2026-09-25), 87 (2026-09-30), 139 (2026-09-25), 166 (2026-09-26) |
| C-S226 | C-CON:8 `implements:` lists four pages and omits EVSLOT | EVSLOT is in the same folder (EVSLOT:9 `owner_layer: CodeDomain:DeveloperConsole`) |
| C-S227 | CON282:4 `status: DOCUMENTED` | CON282:501 "**Status stays `PARTIAL`.**" (2026-09-03 pass; never updated) |
| C-S228 | CON282:18 `last_reviewed: 2026-09-03`, `last_pass: 2026-09-03` | edits dated 2026-09-29/30 (CON282:113, 153, 94); C-CON pass 1 2026-09-29 corrected CON282's counts (CON282:113) |
| C-S229 | CON282:32 "the biggest function in the executable that no document has cited" | the page and C-CON now cite it (C-CON:52) |
| C-S230 | CON282:54 "**Fifty-six of the numbered commands do nothing at all.**" | CMDNAMES:396-398 "38 of them still draw a live value, 12 are labelled buttons with the action removed, 6 draw blank." (2026-09-03) |
| C-S231 | CON282:345 "97 addresses, none named. This is the open question" | CON282:346 pointer; CON282:250 "**ANSWERED 2026-09-27 (OPUS)**" |
| C-S232 | CON282:274 "Which code serves rows 1–11 was not traced." | CON282:275 "*Now traced as far as the image allows (2026-09-30 …)*" |
| C-S233 | CON282:502-503 "this pass did not trace its caller" | CON282:504 "*Answered since (2026-09-30 pointer …)*" |
| C-S234 | TUNES:18 `last_reviewed: 2026-09-03` | edits to 2026-10-01 (TUNES:589, 691, 1229) |
| C-S235 | TUNES:169 "`.data`, uninitialised" | TUNES:65 "**Corrected 2026-09-03 …** The block is a **C++ static object**" |
| C-S236 | TUNES:471-472 "**This does not identify `01F82D20`.** … §7 leaves it open." | TUNES:607 "**Answered 2026-09-14 (FABLE): it is the `GameSettingConfig` singleton pointer**" |
| C-S237 | TUNES:522-524 "nothing here establishes *how* it is opened, and this document does not claim a route to it." | CON282:261-262 "**Answered 2026-09-13 (FABLE), statically:**" (Config screen route) |
| C-S238 | TUNES:574-575 "whether the five unfilled elements are dead capacity … is not settled." | TUNES:585 RC-8 "**ANSWERED 2026-09-30 …** elements 3–7 are built but never counted in." |
| C-S239 | TUNES:667-669 "The integer-form accesses … are still unexplained." | TUNES:670 "*Narrowed 2026-09-30 …*" and RC-7 ANSWERED (684) |
| C-S240 | TUNES:779-780 "The difference is not reconciled." | TUNES:780 pointer (2026-09-30) and TUNES:1082-1084 (2026-09-12) |
| C-S241 | TUNES:1093-1096 "Left unverified and said so." | TUNES:1097 "*Verified 2026-09-30 (SWE2-CONTRACT): disjoint.*" |
| C-S242 | CON2:19 `last_reviewed: 2026-09-03` | sections dated 2026-09-30 (CON2:75, 126, 217-283) |
| C-S243 | CON2:72-73 "**What the codes name is not established here.**" | CON2:75 "**Answered 2026-09-30**" |
| C-S244 | CON2:149-150 asm comment "the console arm writes it"; 155 "the glyph-record builder copies it"; 162-163 "**The console writes a byte on one object; a render-record builder copies it**" (kept unstruck) | CON2:126-136 "**Corrected 2026-09-30** … `001C977B` is not a console arm … `0018F316` is not a glyph-record builder" |
| C-S245 | CON2:205-207 "**What this document does not claim:** …" | CON2:208 "*All six are answered since (2026-09-30 …)*" |
| C-S246 | EVSLOT file name `the-event-slot-panel-and-its-dead-feeder.md` | EVSLOT:4 "earlier "dead feeder" verdict retracted" (2026-09-25); title EVSLOT:25 "live feeder" |
| C-S247 | EVSLOT:88 "`01F832C4` | dword | cleared by the pusher each push" (only writer listed) | EVSLOT:302 "`01F832C4` has one more writer than §2 lists: `001EC690` increments it" |
| C-S248 | EVSLOT:340-341 "Section 6's open items stay open." (2026-09-29) | §6 answers dated 2026-09-30 (EVSLOT:180, 219, 230) |
| C-S249 | CMDNAMES:19 `last_reviewed: 2026-09-03` | CMDNAMES:419 "**Resolved 2026-09-18 (FABLE)**" |
| C-S250 | CMDNAMES:416-417 "**Raised, not resolved**" | CMDNAMES:419 resolved 2026-09-18 |
| C-S251 | CMDNAMES:31 "**GENERATED — do not hand-edit.**" | the hand-added paragraph CMDNAMES:419 |
| C-S252 | README:11-63 "## Systems in this category" lists no Developer-Tuning-Console page | the folder has 16 pages (C-CON:30-31) |

#### 3.2.10 Developer tuning console: the arm catalogue (work division and slices A-I)

| id | stale or banner text | answered or contradicted by |
|---|---|---|
| C-S253 | ARMDIV:290 "**96 of 282 ids catalogued; 186 remain.**" | ARMDIV:456 "**The table is closed.** Nine slices, five sessions, every action id catalogued." |
| C-S254 | ARMDIV:276-277 claims table: H "**offered, awaiting reply**", I "claimed" | ARMDIV:454 "## H delivered — 282 of 282"; ARM-H, ARM-I exist |
| C-S255 | ARMDIV:294 "Slices A and B read `GN158` and **stay that way.**" | ARM-A:12, ARM-B:12 `parent_tag: GN162` ("CARRIED TO GN162 2026-09-21", ARM-A:13) |
| C-S256 | ARMDIV:14 `last_reviewed: 2026-09-13` | dated body edits 2026-09-14 (ARMDIV:540), 2026-09-19 (ARMDIV:578-612) |
| C-S257 | ARMDIV:98 "**102 of 102 stepping arms have this shape.**" (History) | ARMDIV:44 "**but only 55 have that shape.** The other **47 are signed pairs**" (re-derived 2026-09-13) |
| C-S258 | ARMDIV:185-186 "zero-filled tail of `.data`, built at run time." / ARM-C:205-206 "It is in the zero-filled tail of `.data`, so it holds no value in the file and is built at run time." / ARM-B:153 "the array is in `.data` BSS, so it holds no value in the file." | TUNES:65-68 "**Corrected 2026-09-03: "uninitialised, built at run time, no file image" was wrong.** The block is a **C++ static object**" |
| C-S259 | Slices A–I `last_reviewed: 2026-09-03` (e.g. ARM-A:19) | dated body answers up to 2026-09-26 (ARM-A:304; ARM-D:298; ARM-G:191; ARM-I:317) |
| C-S260 | ARM-C:19, ARM-D:18, ARM-E:18, ARM-F:19, ARM-G:19, ARM-H:19, ARM-I:19 `parent_tag: GN159` | same front matter `parent_tag: GN162` (e.g. ARM-C:12) |
| C-S261 | ARM-B:61 "Who calls it is still untraced." | ARM-B:191-197 "**Answered 2026-09-14 (FABLE)**" |
| C-S262 | ARM-B:118-119 "slices C–I have not been read" | ARM-B:121 "**Resolved by slice C, 2026-09-03.**" |
| C-S263 | ARM-C:60 "**No target in this slice is identified by name** — see §8" | ARM-C:215-219 (ANSWERED 2026-09-25: all 36 named); §8 is the call chain |
| C-S264 | ARM-C:235/239 garbled struck UQ-12 heading ("~~…its `+0xCC4`/`+0xCC8`/`+0xCCC`~~" … "fields are.") | ARM-C:241 ANSWERED 2026-09-17 |
| C-S265 | ARM-D:153-156 "ids 140–293 are unread" | ARM-D:319-335 (UQ-16 answered 2026-09-25/26) |
| C-S266 | ARM-E:290-291 "the `0x0E` is a channel or key selector, not decoded" | ARM-E:427-429 / ARMDIV:475 (`0x38/4 = 14`, property 14) |
| C-S267 | ARM-E:328-334, ARM-E:348 consumer of the 21 Map floats open | CON282:250 ANSWERED 2026-09-27 (cbuffer) |
| C-S268 | ARM-F:256-257 "**No field in this slice was traced to a reader.**" | ARM-F:260 ANSWERED 2026-09-25 |
| C-S269 | ARM-G:121 "ids 236–293 are unread" | ARM-H / ARM-I delivered (ARMDIV:454-456) |
| C-S270 | ARM-I:97-98 "Slice H (ids 236–267) is unread" | ARM-I:100-106 "Tested by slice H §8" |
| C-S271 | ARM-I:316-317 UQ-21 checkbox open wording | "*Answered 2026-09-26 (OPUS)*" same line |
| C-S272 | CMDNAMES:111 id 28 field `02CB8130` (generated table) | CMDNAMES:419 "**Resolved 2026-09-18 (FABLE)** … id 28 does not own it"; ARM-A:117-142 |
| C-S273 | CMDNAMES:410-417 "**Raised, not resolved**" | CMDNAMES:419 same page, 2026-09-18 |
| C-S274 | ARM-A:304 UQ-7 premise "far outside the contiguous run" | "DISSOLVED in the register 2026-09-26" (same line) |
| C-S275 | ARM-D:128 "Flagged 2026-09-08, unresolved." | still unresolved (no later dated line) — listed in G.1 |
| C-S276 | ARMDIV:20 `crossref_clean: true` | slices all `crossref_clean: false` (e.g. ARM-A:25); C.1 items above |

