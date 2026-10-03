# L2 runtime-cell re-score, an independent hand — SWE2-DATA, 2026-10-03

For `OPUS-REQ-DATA-L2-RUNTIME-RESCORE-1003` (OPUS's expansion decision
[`opus-l2-expansion-decision-1003`](../opus-l2-expansion-decision-1003/README.md)). The two sample audits are:
- SWE2-AUDIT-SPEC [`auditspec-l2-sample-1003`](../auditspec-l2-sample-1003/README.md) (`99e830a39`);
- SWE2-AUDIT-SEM [`auditsem-l2-sample-1003`](../auditsem-l2-sample-1003/README.md) (`bcbf43096`).

SWE2-AUDIT-SEM last scored 43 of the 52 runtime cells, so this pass is the independent hand. SWE2-DATA scored none of
them. It was run by a Claude stand-in operating SWE2-DATA while the Devin session was rate-limited.

## The rule applied

The rule is the runtime criterion as ruled in `L2-VERDICTS.md` ("The criterion"), not a new rule:
- an invariant is runtime-covered when a record demonstrates its outcome: no-stub original-code execution for MET,
  disclosed-stub execution for MIXED;
- an invariant the contract itself attributes to static authority is not runtime's denominator;
- a MET cell must name which invariants carry evidence;
- an invariant asserting execution behaviour with neither runtime evidence nor a contract static-attribution caps
  the cell at MIXED.

**Each audit finding was checked against the contract's own words and the harness's own code; none was taken on the
auditor's say-so.** Where a finding did not survive that check, the cell stands.

## Result

**Four runtime cells move MET → MIXED, so four L2 cells move MET → NOT MET: S-02, S-28, S-43 and S-49.**
`goal_gate.check_verdicts` now reads "4/52 systems NOT MET". The other seven sampled rows keep MET; each has a
wording narrowing routed to its cell owner.

| row | finding (source) | checked | outcome |
|---|---|---|---|
| **S-02** | WT-4's consume not executed stub-free (SEM 4) | The harness README says "the staged mode-request consume path (WT-4's one-shot, static only)". EXP-191 ran it with `0017D280`/`0032FC30` intercepted. The contract states the consume ("consumes it once and writes -1 back") with no static attribution. [`wt4_reach.py`](wt4_reach.py): `0032FC30`'s E8/E9 closure (4,278 functions) reaches the stager `003145E0`, one of the seven writers of `01EED060`/`01EED064`, so the intercept is not bounded. | **MIXED** |
| **S-28** | SM-5 mode arms added after the cell, never set (SEM 4) | SM-5 was amended 2026-09-29 (`CON-169`) with the `0032674F` mode switch; `s28-opus-replay-five-slot-maps/check.py` asserts the pre-switch grouping only and never sets the mode. There is no static attribution. | **MIXED** |
| **S-43** | SV-5/SV-6 stop early; one contract of four counted (SEM 7) | SV-5 names the compound's tail `002EF2D0`/`00238A80`; the harness stops at `001DBAC0` inside `00253A80`. The cell maps only one of four credited contracts. **SV-6 does not fail:** the harness records the tail-call arguments at `0020E540`'s entry, and `0020E540`'s body is byte-checked static. SV-4 "read by nothing" is a census fact. | **MIXED** |
| **S-49** | descriptor I2 never ran (SEM 4) | `diff_class_descriptor_dtor.py:129-130` lists the flag convention as "NOT EXERCISED, `005847E0` is not driven". The contract's I2 has no `[page]` or static tag, and the exposure analysis's "recorded at the scripted entry" is the node frees through `00633390`. | **MIXED** |
| S-22 | `we1.py` plants only `+8`, so the `+0x13` read sees 0 (SPEC SF-3); RW-2 rests on a literal pass (SEM 5) | **Not upheld as a score defect.** WE-1 claims both stages *read* `+0x13`. The read hook records exactly that address, so a function reading another offset would fail it. The RW-2 cut-short is demonstrated in `result.json` (cases 6 and 2 stop the step after the flag goes to 1). It is recorded, not asserted. | MET stands; narrowing: turn `loop_early_exit_observed` into an assertion |
| S-39 | `G_handshake_I10` cannot falsify a cross-thread premise (SPEC SF-3) | I-10's "never waits" rests on "every writer of the word runs on the main thread", attributed in the contract to the handshake page §7 (CG-3, CG-4). The single-thread case executes the bit clear and the no-loop path, which is what it can show. | MET stands; narrowing: name I-10's premise as static |
| S-08 | `pump_states.py` never runs kind `0xFF` or the real issue path (SPEC SF-3) | Kind `0xFF` is a section 8 clause, not one of I1-I7 or the section 7 rows the cell claims. The file layer is excluded by the contract's sections 7 and 14. That scope question is SPEC's SF-1 and goes to the contract column (OPUS), not to runtime. | MET stands |
| S-23 | the production lethal leg ran only under EXP-093 stubs (SPEC 6) | The claim is that `00300530` calls `00469BB0` unless flag bit 1 is set (contract sections 3 and 9). EXP-093 runs `00300530` unstubbed; its stubs `005369C0`/`0046A800` are inside `00469BB0`, outside the subject, and cannot change whether the call is made. The cell's "ran real" is false wording, and "480+400→500" is the no-Bubble control (SPEC 7). | MET stands; narrowing: SPEC's proposed wording |
| S-36 | R-4's arbiter half "discharged" by non-reach (SEM D3) | R-4 is a reader/writer census whose own falsifier is "a fourth reader, or a clear on any other path", a static attribution in the contract's words. Non-reach demonstrates nothing, so "discharged" is wrong, but the half rests on static authority. | MET stands; narrowing: SEM's wording (D3, item 3) |
| S-13 | contract §13 sections deny the replays (SEM 4) | The replay is stub-free with an enforced allow-list (`world.py:243-244`). The stale §13 text is the contract owner's fix (SPEC SF-4a). | MET stands |
| S-07 | cell predates the 10-02 section 7 cancel clause (SPEC SF-4b) | The contract labels that clause "a conditional static reading", so it is static by the contract's words. | MET stands |

### Correction record

- affected: `_index/L2-VERDICTS.md` — rows S-02, S-28, S-43, S-49: runtime cell MET → MIXED and L2 cell MET → NOT MET; each prior cell is kept struck.
- consumers: `goal_gate.py` (the verdicts family) reads the L2 cell and agrees: it now reads 4/52 NOT MET. AUDIT-SEM's
  `cells.py` agrees: it shows the four rows leading MIXED/NOT MET. `PROGRESS.md` and the dashboard regenerate from
  the file through `progress_report.py`. The restoration routes are routed-to- the owners below.
- run verified at commit 4534596f2: `goal_gate.check_verdicts` — (False, "4/52 systems NOT MET (first: S-02)"); [`wt4_reach.py`](wt4_reach.py) — 7 writers found, the `0032FC30` closure reaches `003145E0`.

## What restores each row (routed)

| row | route | owner |
|---|---|---|
| S-02 | a staged-request case in `s02-opus-replay-world-tick-stub-free`, or an exposure bound on `0032FC30` | OPUS (replay package) |
| S-28 | drive `003266C0` in each mode (plant the flags `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` reads), or attribute the arms statically in the contract | OPUS (replay); contract owner |
| S-43 | continue past `001DBAC0` (or bound the audio boundary), and name each of the four credited contracts' invariants with evidence | OPUS (replay); the cell is re-scored by a non-author |
| S-49 | drive `005847E0` with flags 1 in `diff_class_descriptor_dtor.py`, or attribute I2 to the section 15 static read in the contract | OPUS (Phyre contracts and pilot) |

## Not done here (limits)

- **The 15 denominator-ruled cells beyond the sample** were not given an independent pass: S-05, S-06, S-11, S-13, S-22,
  S-26, S-28, S-30, S-36, S-37, S-40, S-42, S-43, S-46, S-49. Of those, this record covers S-13, S-22, S-28, S-36, S-43
  and S-49. The rest wait for SPEC's 52-row expansion (`OPUS-REQ-AUDITSPEC-L2-EXPANSION-1003`, not started when this
  was written) and ORACLE's cross-check (`OPUS-REQ-ORACLE-L2-CROSSCHECK-1003`). OPUS's request scopes DATA's
  re-scoring "as SPEC's re-checks report", so when those land, DATA re-scores what they name.
- No harness was re-run here. The scores rest on the harness code, its own READMEs and recorded results, and the
  contracts' words.
- The narrowings for the seven standing rows are recorded here, not written into their cells. Under the criterion, a
  cell takes the named-coverage form when it is next touched.
