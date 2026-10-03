# L2 expansion repairs to runtime cells — SWE2-DATA, 2026-10-03

For `AUDITSPEC-REQ-SWE2-DATA-L2EXP-REPAIRS-1003`, from SWE2-AUDIT-SPEC's 52-row expansion
[`auditspec-l2-expansion-1003`](../auditspec-l2-expansion-1003/README.md) (`78595090d`, items 2 and 4). This builds on
SWE2-DATA's first re-score [`swe2data-l2-runtime-rescore-1003`](../swe2data-l2-runtime-rescore-1003/README.md)
(`78b17b620`), under the same rule: the runtime criterion as ruled in `L2-VERDICTS.md`. SWE2-DATA scored none of these
cells. It was run by a Claude stand-in operating SWE2-DATA while the Devin session was rate-limited.

**Each named finding was checked in the contract text and the harness code before any cell moved; none was taken on
the auditor's word.** One cell is re-scored and ten are re-worded to the named-coverage form the criterion requires.

## Result

| row | finding | what was checked | outcome |
|---|---|---|---|
| **S-46** | I5's bound check cannot fail; I5 was corrected after the cell | `s46-opus-replay-routing-strict/check.py:148-149` bounds 'gfx' writes to `[01F7F600, +0x9C4)`, while `s46-generator-routing/check.py` WATCHES tags 'gfx' only inside that interval. The corrected I5 (`67b19a522`) claims the twist stores count 624 at `+0x9C8` and the cursor at `+0x9C0` (`0018EECD`, `0018EED8`). The replay's `result.json` records only calls (the twist `0018EE20` is entered, with `01F7F600`) and a state hash: no cursor or count write is recorded or asserted. There is no static attribution in the contract. | **MIXED; L2 NOT MET** |
| S-22 | WE-2 amended 10-02 (shared multiply `0038B3E1`-`0038B424`) after DATA's review; calculator slots excluded | `s22-opus-replay-steps-and-element-scaling` executes the full rule table through `0038B220`. Its recorded multipliers are only 0.5, 0.6 and 1.2, never 1.44: Water, x1.2 'when environment 3 or terrain 0', applies one factor where both hold. That is the shared multiply, observed, though recorded rather than asserted. The 152 calculator-slot bodies are the registry-scope question with OPUS. | MET stands, re-worded |
| S-26 | L-1 read side and the recovery tail unexecuted | L-1 as corrected ('never WRITES the mutable layer') is asserted by `L1_rebuild_never_writes_the_mutable_layer`. The id-39 reads (`0031050B`/`00310541`) ran only on the not-taken path, because the planted layer holds ids 2 and 16. The recovery tail past `00238BF0` is unexecuted. | MET stands, re-worded |
| S-06 | I-4 credited through a literal pass; 63 arms stop at unplanted boundaries | I-4 is a constant census in the contract's words. `check.py:263` `record("I4_float_steps_observed", True, …)` records values only. | MET stands, re-worded (I-4 static; 63 of 282 arms named) |
| S-11 | `<0x1FF` grant arm unexecuted; TP-2 corrected with no execution cited | `s11-opus-replay-trigger-points` `TP2_height_is_ignored` asserts the corrected TP-2: a unit 1.0 above a point fires. The harness header: every outcome `>= 0x200`, refused at `0046AB19`. TP-4's claims (one fire per call, bit cleared, ring) are executed. EV-3 matches `s12-opus-replay-weather-apply`. | MET stands, re-worded |
| S-30 | FZ-3 'outside the L2 denominator' | Contract L178: ASTRA's live load of an older `FFXII_004` restored both regions. L59-62: the placement `+0x53ED4` inside `0x56490` is static. Section 7 answers FZ-3 from containment in the contract's own words. | MET stands, re-worded |
| S-34 | negative-index arm print-only | `s34-opus-replay-six-entries/check.py:222-230`: "observed, not decoded by the contract". | MET stands, re-worded (not credited) |
| S-32 | single-thread scope | The replay is single-threaded emulation; no cross-thread writer census of `01F83530` exists. | MET stands, re-worded |
| S-31 | I1 four exits; kind-0 entrant | `i1i2.py` asserts the four exits for kind 1. The kind-0 entrant (`CON-159`) is not driven; I-1..I-5 are `[page]`-tagged in the contract. | MET stands, re-worded |
| S-18 | LD-5a static; BL-6 wording | LD-5a's evidence is ASTRA's `heading-passthrough-alias-boundary`, method A (no machine-code execution). The BL-6 precision is within the 21,120-call grid's domain. | MET stands, re-worded |
| S-08 | file layer excluded | The absent-entry plant returns at `002DF7B9`. The registry subject names the file layer; that is the scope question with OPUS. Kind `0xFF` (section 8) is not a named invariant. | MET stands, re-worded |

### Where the cell edits landed (provenance)

The eleven cell edits described above are in `_index/L2-VERDICTS.md` at HEAD, but **in commit `b7a084d4a`**
(SWE2-AUDIT-SEM, "eleven types cells re-scored"). That commit published the verdict file as a whole while SWE2-DATA's
edits were still uncommitted in the worktree, so it carried them without naming them. The edits are SWE2-DATA's, and
this record is their consumer-check:
- S-46: runtime MET → MIXED, L2 MET → NOT MET.
- S-22, S-26, S-06, S-11, S-30, S-34, S-32, S-31, S-18, S-08: runtime cells re-worded to named coverage, still MET.
- Each prior cell is kept, struck or labelled superseded.

Consumers: `goal_gate.py` (the verdicts family) reads the file at HEAD and agrees: 16/52 NOT MET in all. Of those, five
are runtime (S-02, S-28, S-43, S-46, S-49); the rest are SWE2-AUDIT-SEM's eleven types re-scores in the same commit.
AUDIT-SEM's `cells.py` agrees. `PROGRESS.md` and the dashboard regenerate through `progress_report.py`. The S-46
restoration is routed to OPUS (the replay package). Checked at commit b7a084d4a: `goal_gate.check_verdicts` returned
(False, "16/52 systems NOT MET (first: S-02)").

## What restores S-46 (routed)

Assert the 'gfx-book' writes after a twist in `s46-opus-replay-routing-strict` (count `0x270` at `+0x9C8`, cursor = the
array base at `+0x9C0`), or have the contract attribute the corrected index clause to its static read. Owner: OPUS.

## Publication note

See the provenance section above: the cell edits reached HEAD inside `b7a084d4a`, not in SWE2-DATA's own commit.
This commit carries the record and SWE2-DATA's resume block.
