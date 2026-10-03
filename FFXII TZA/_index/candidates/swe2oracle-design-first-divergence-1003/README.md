# Design note: first-divergence records for parity and bounded DB probes (SWE2-ORACLE, 2026-10-03)

Answers the user's request (relayed by FABLE) for a design of section 5, "Reconstruction / parity: first-divergence
summaries", of `Database/Tools/work/FABLE/FFXII_PROJECT_IMPROVEMENT_ADDENDUM_2026-10-03.md`. **Priority P2**
(addendum section 16): it must not delay database completion. Per section 17, this note **extends the existing parity
machinery rather than adding a system**, and it implements nothing in the dashboard. It also carries one worked
example on a real sealed suite, `first_divergence_probe.py` (output `first_divergence_probe.out`, record
`first-divergence.tsv`, `FAILS 0`).

## 1. What already exists, and what this extends (SWE2-ORACLE)

| existing piece | what it already does | what first divergence adds |
|---|---|---|
| `Reconstruction/Tests/Differential/diff_*.py` (45 pilots) + `Reconstruction/PARITY-STANDARD.md` §5 | run the original under Unicorn and the reconstruction driver on one script, compare an **ordered stream of output lines** and print `N comparisons, M mismatches` | the index and kind of the **first** mismatching line, and whether earlier states were compared at all |
| `gfz-scripts/parity_status.py` → `_index/PARITY-STATUS.md` | reads each pilot's `PARITY` declaration with `ast`; with `--run`, executes each pilot and parses its counts; declared and measured columns kept apart | one more parsed line per pilot (§5) and one generated TSV (§6) |
| sealed Unicorn suites `_experiments/evidence/*/check.py` + `result.json` | isolated original-code runs, each with a receipt | the reference side of a DB probe (§8) |
| `gfz-scripts/execution_coverage.py` + `execcov/` shim (`b742fa6c9`) | wraps `Uc` without editing a suite; per-run executed-entry records; a run counts only if its receipt reproduces | the same wrapping technique records a state sequence (§3) |
| `gfz-scripts/seal.py` + `_experiments/evidence/receipts/store/` | write-once receipts; `publishable()` gate (committed drivers, exact case ids) | carries both compared runs and the comparison (§4) |
| ASTRA live captures (EXP records, `@runtime`) | observed values from the running game | a live reference sequence at observation points (§3.3) |

## 2. The record schema (SWE2-ORACLE)

One row per compared pair: a reference run and a candidate run of one package on one case. Fields are the addendum's,
plus two that make "first" checkable.

| field | content |
|---|---|
| `record` | stable id: `<package>:<case>:<candidate>` |
| `package` | the reconstruction package / subsystem (PARITY `subsystem`) |
| `expected_contract` | the owning CONTRACT path (PARITY `contract`), or `none` |
| `reference_result` | the reference run: original under Unicorn, a live capture, or a second sealed run; **receipt run id** |
| `reconstruction_result` | the candidate run: reconstruction driver, mutant, other arm; **receipt run id** |
| `compared_from` | **the earliest observation point both sides recorded** (e.g. `event 0 (entry)`, `observation point 0`, `final state only`) |
| `first_divergent_step` | index + both sides' values at the first differing observation point, or `NONE over N`, or **`UNKNOWN (earlier states were not compared)`** |
| `divergence_class` | one of the addendum's list: initialization, input interpretation, field/type/layout, branch condition, RNG, ordering, lifetime, resource binding, script/native bridge, state transition, downstream consequence, presentation-only, unknown |
| `likely_ownership` | contract, implementation, instrument or integration (§7) |
| `late_visible_mismatch` | what a final-state compare would show, kept beside the first divergence and never in its place |
| `evidence` | the receipts, the comparator's receipt, the pilot or suite path |
| `status` | `NO DIVERGENCE`, `FIRST DIVERGENCE ESTABLISHED`, `LATE MISMATCH ONLY`, `CONTROL FAILED`, `UNRUN` |

**The rule the schema enforces:** `first_divergent_step` may name a step only when `compared_from` is at or before
it, and every observation point between them compared equal. A row with `compared_from = final state only` must say
`UNKNOWN` (worked example row F0). That is the addendum's "do not treat a late visible mismatch as the first
divergence" requirement, made mechanical.

## 3. How a harness captures comparable state sequences (SWE2-ORACLE)

A first divergence is only as early as the earliest state both sides recorded. There are three comparison situations.
They need different sequences.

### 3.1 Same binary, different input or bytes: the event trace

The case for two runs of a sealed suite, mutants, and two arms of one routine. Both sides execute the same image, so
an instruction-level trace aligns. Wrap `Uc` exactly as the execcov shim does (no suite edit) and record, in order:
`X rip` per instruction (`UC_HOOK_CODE`), and `W rip addr size bytes` per write (`UC_HOOK_MEM_WRITE`). The bytes are
read back when the next instruction starts, so 16-byte SIMD stores carry real values. Add `R` for reads of a watched
address. A range read hook fires on the access *start*, so the watch must span `site-15..site`; the first probe run
missed a 16-byte load covering `01CCFE03` because of this. The first differing event is the first divergence at
instruction granularity. Cost here: 9,374 events for one 624-word twist. The whole probe, about 45 runs, takes about 6 s.

### 3.2 Reconstruction against original: observation points

A reconstruction is native code, so **no instruction stream is shared**. Comparison happens at **observation
points**: contract-level states both sides can emit in the same order, such as each write to a contract field, each
element of an output array, each returned value, each state word after a step. The pilots already do this: every
`V`/`S`/`W` line of `diff_rng_generators.py` is an observation point, and its stream is compared in order. Two
requirements turn that into first divergence:
- **Granularity is declared.** A pilot that compares only after the whole call has `compared_from = final state`, and
  its divergences are `UNKNOWN`. A pilot that emits per-step states can name a first step.
- **Intermediate observation points are emitted by both sides.** The reconstruction driver prints the same
  `<kind> <value>` line at the same contract step the Unicorn side records (a write hook on the contract's field
  range). A pilot that adds a per-step stream raises its own resolution, and nothing else changes.

The worked example's row A0 shows why this is the right level. The shipped twist's scalar and SIMD arms are two
implementations of one contract, the closest available analog of a reconstruction. Their instruction streams part at
event 4 (the feature gate, by design), yet their 625-point observation streams are **identical**. An
instruction-level comparison would report a false divergence. The observation level reports parity.

### 3.3 Live against isolated: ASTRA captures as the reference

An ASTRA live capture (field values at a breakpoint, a write watch, a per-frame dump) is a reference sequence at
observation points chosen by the capture. The isolated run or reconstruction is compared against it at the same
points. `compared_from` is the first captured point. A live capture that records only the end state gives `UNKNOWN`
for any earlier divergence. The live run's environment (map, frame, inputs) has to be matched by the isolated
fixture before a difference is a divergence. Otherwise ownership is **instrument** (§7). This needs `@runtime` and
is ASTRA's to run. The design adds only the record shape.

## 4. Sealing: how the existing receipts carry it (SWE2-ORACLE)

No new mechanism; `seal.py` as it stands:
- **Each side is a run with a receipt.** The reference and candidate sequences are each the `result` of a sealed run.
  Drivers are committed (the `publishable()` gate). Cases are the case ids, and inputs are the fixture or case files.
  A sequence file is just a larger result. Seal flat `{case_id: {...}}` maps, which `seal._case_ids` accepts.
- **The comparison is a third receipt.** Driver = the comparator (here `first_divergence_probe.py`). Inputs = the two
  side results, by sha256. Result = the first-divergence rows. A row is evidence only when all three receipts pass
  `publishable()`. A row whose side receipt is missing reports `UNRUN`, never `NO DIVERGENCE`.
- **Reproduction before comparison.** Re-run the reference first, and compare only if its sealed receipt reproduces,
  the execution_coverage rule. A reference that does not reproduce makes every downstream row an instrument problem.
- **Cumulative reuse** follows the existing `case_sources` rule. A divergence row never counts an inherited case as a
  new comparison.

## 5. What a pilot prints, so the existing generator can parse it (SWE2-ORACLE)

One optional line beside the existing `N comparisons, M mismatches`, per case or once per pilot:

```
FIRST-DIVERGENCE: case=<id> compared_from=<point> step=<index|NONE|UNKNOWN> class=<class> ref=<value> cand=<value>
```

`parity_status.py --run` already parses each pilot's output. It would parse this line too, under the same rule as
today: **an unparseable or absent line is `UNPARSED` or `UNRUN`, never `NONE`**. A pilot that prints nothing keeps
its current row unchanged.

## 6. Where it surfaces: a generated TSV as a dashboard generation input (SWE2-ORACLE)

- **`_index/FIRST-DIVERGENCE.tsv`**, generated by `parity_status.py --run`, next to `PARITY-STATUS.md`, never
  hand-edited. Columns are the §2 schema. Same generator, same run, same freshness rule as the page it sits beside.
- **Dashboard:** the TSV becomes one more *generation input* of the existing atomic dashboard build, with its input
  fingerprint (generator sha, pilot shas, receipt run ids) checked like every derived snapshot. A stale TSV shows
  STALE, never last-known rows as current. The view answers the addendum's question 11 ("where is the first
  divergence?"): per package, the earliest established divergence, or `UNKNOWN` with the granularity that limited it.
- `check_parity_current.py` already diffs `PARITY-STATUS.md` against its generator. The same check covers the TSV.
  No new gate.

## 7. The correction loop: routing by ownership (SWE2-ORACLE)

Ownership is decided by **triangulating** reference, candidate and contract at the first divergent point, never by
the candidate alone:

| finding at the first divergence | likely ownership | routed to | via |
|---|---|---|---|
| the **reference** (original or live) disagrees with what the **contract** states, and the candidate follows the contract | **contract** → fix the DB | the CONTRACT owner / page owner; the register row | a `contradiction` task (TEAM.md) with the divergence row as counter-evidence; correction gate 4a on publish |
| the candidate disagrees with both reference and contract | **implementation** → fix the reconstruction | the pilot / package owner under `Reconstruction/` | a request carrying the row, the case and the receipts |
| the reference run does not reproduce its receipt, a control fails (the D0 determinism control, a mutant not localized, a missed watch), or the live and isolated environments differ | **instrument** → fix the evidence harness | the harness owner (SWE2-ORACLE for sealed Unicorn suites and the execcov tools, ASTRA for live captures) | a request to the harness owner; the row stays `CONTROL FAILED` |
| each unit matches at its own observation points, but the composed run diverges at a seam (an argument, a shared field, an ordering between units) | **integration** → fix the cross-system composition | the INTEGRATION-dimension owner (PARITY-STANDARD §3) | a request naming both units' receipts and the seam's observation point |

`divergence_class` (§2) is a **first guess from the symptom**: the kind of the first differing event (control flow →
branch condition, write target → field/type/layout, value at the same target → state transition). In the worked
example it is right for the jump mutants but describes symptoms elsewhere. `m-simd-ecx` is an initialization defect
(a loop counter's start value) that first shows as a write to the wrong cell. The class is refined by whoever takes
the routed task, and recorded back into the row.

## 8. A bounded DB-probe use available now, before reconstruction is authorized (SWE2-ORACLE)

All of this runs on existing sealed suites with no reconstruction code. Each answers a database-quality question:
- **Determinism of a sealed suite:** the same case twice must give `NO DIVERGENCE` over the full event sequence. A
  divergence means the receipt depends on something unsealed (uninitialised fixture memory, time, ordering). That is
  an instrument finding against the suite.
- **Mutation sensitivity with localization:** the suite's own mutants as candidates. Today a suite reports a mutant
  "killed" from a final-state mismatch. First divergence additionally shows that the harness *sees the defect where it
  happens*. A first divergence earlier than the patched instruction's first execution would expose a harness defect.
- **Alternative-path parity:** two arms of one routine (feature gates, mode switches) compared at observation points.
  This is a static-plus-isolated check of a contract's "both paths agree" claim.
- **Live against isolated (ASTRA):** where a live capture exists, compare the isolated fixture at the captured points.
  The first mismatch is either a contract fact or a fixture (instrument) defect.

## 9. Worked example: mt-twist-simd-exec (EXP-111), the shipped MT19937 twist `00866B90` (SWE2-ORACLE)

`first_divergence_probe.py` imports the suite's own `check.py` (`run_twist`, `MUTS`, `build_states`) and swaps in a
recording `Uc`. It never edits the suite. The sealed `result.json` md5 `5f2c5917…` is identical before and after
(checked). Input state `rand`, the suite's own. Output: `first_divergence_probe.out`, rows in `first-divergence.tsv`.
`FAILS 0`.

| rows | comparison | result |
|---|---|---|
| D0 | baseline twice | `NO DIVERGENCE` over 9,374 events and 625 observation points: the determinism control holds |
| m-gate … m-sc1-shr (20) | each suite mutant against shipped bytes | **all 20 localize.** The first divergence is never before the first execution of the patched instruction (or the first read of the patched constant). It is often within a few events: `m-sc2-m` executes the patch at event 3,427 and diverges at 3,429 (scalar2's first write to `s[227]`). `m-tail-mti` diverges at 9,363, right after the patched store at 9,362. |
| m-gate | gate `jl`→`jge` on the scalar input | first divergence at event 4 (branch condition). **No observation-point divergence**: the SIMD arm runs and produces the same state. The suite kills it only through the stack region it checks as a canary. This is a real divergence with no contract-level consequence, which a final-state-only parity view would miss or misclass. |
| m-sc1-loop / m-sc2-loop | loop bound → never | first divergence is the branch at 3,416 and 9,358. Each mutant executes its patched jump first at events 25 and 3,432, where both sides still branch the same way until the bound matters. "First divergence" is the first *differing* step, not the first execution of the defect. |
| A0 | scalar arm against SIMD arm | instruction streams part at event 4 (by design); **observation streams equal over 625 points**: contract-level parity, and why §3.2 compares observation points |
| F0 | `m-sc2-m` compared on the final state only, as the sealed suite does | `UNKNOWN (earlier states were not compared)`; late visible mismatch `final s[227]` |

The probe's first run failed one control, `m-simd-hi`. That was an instrument defect, the range read hook described in
§3.1. It was fixed in the probe and the reason is commented in the code. That is the loop of §7 applied to the
example's own instrument.

## 10. Limits (SWE2-ORACLE)

- **Design only.** Nothing in `parity_status.py`, the pilots, `PARITY-STATUS.md` or the dashboard is changed. §5 and
  §6 are the smallest changes that would implement it when the work is scheduled. It is P2 and waits behind database
  completion.
- **The worked example is a DB probe, not reconstruction parity.** The candidates are mutants and the other arm, not
  reconstruction code. Its "implementation" ownership is known by construction.
- **Instruction-level traces only align within one binary.** Reconstruction parity needs observation points, and its
  first divergence is only as fine as the points both sides emit.
- **The class column is a symptom-level first guess** (§7), not a diagnosis.
- Event traces are large: about 9k events for one 624-word twist. Long-running suites
  (gambit-walk-exec, more than 25 min under the coverage shim) would record observation points only, never full traces.
- Run the probe with system Python 3.14 (unicorn 2.1.4). The analysis venv's unicorn 2.1.0 rejects the SIMD arm.

## 11. Re-run (SWE2-ORACLE)

```
python "Database/FFXII TZA/_index/candidates/swe2oracle-design-first-divergence-1003/first_divergence_probe.py"
```

About 6 s. Ends `FAILS 0` and rewrites `first-divergence.tsv`.
