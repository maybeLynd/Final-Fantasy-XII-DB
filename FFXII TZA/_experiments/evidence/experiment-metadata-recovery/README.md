# EXP-037..074 metadata recovery

ASTRA, 2026-09-12. This repairs `OPUS-NOTICE-EXPERIMENT-FRONTMATTER` using the
historical records, their retained primary receipts and current contract scopes.
It adds no experiment, live observation, contract or readiness promotion.

All 38 original Markdown bodies remain byte-for-byte intact after a new flat
frontmatter prefix. [recovery.json](recovery.json) records each original body hash,
prefix extent, metadata, historical manifest hash and the contract inventory at
review. All 290 files sealed by those historical manifests still match. Failed
setups, mutations, prior pause statements and later correction history are retained.
The dates in the prefixes refer to the historical work; recovery is dated separately.

The evidence classes are four preparations (037/038/042/045), one generated native
instrument control (039), one retained-capture assessment (041), one tool verdict
reproduction (044), and 31 isolated original-code records. **None of these 38 records
reports a live FF12 run.** The native fixture in 039 ran its own generated code.
`COMPLETE` describes a bounded package; it does not mean native dependencies,
ordinary gameplay, integrated parity or the full database are complete.

## Contract links and their limits

Each linked record has an explicit `contract_coverage` field. These links describe
useful evidence for a component, caller or constraint; they do not imply the whole
contract was executed. Owner review and contract-side integration remain pending.

| Records | Existing contract | Specific coverage |
|---|---|---|
| 040, 047 | commit-action | Optional cancellation's local effects; reset boundaries on attacker-mask lifetime. Commit itself is not executed. |
| 041 | game-setting-config | Retained EXP-001 pointer expressions and documentation correction. Missing old identity receipts and E8 failures remain. |
| 043, 046 | battle-target-buffer | Original append and reset. Reset's imported memset is a controlled fill. |
| 048, 049 | field-runtime-pass | Its original 003588B0 resolver dependency. No field pass or native registry initialization. |
| 056 | gameplay-generators | The documented MT seed caller's arithmetic and tail argument. The MT seeder is omitted. |
| 057 | save-image-buffers | Original active getter and distinct active/staging identities in the checksum segment. Whole-buffer operations are not executed. |
| 060 | hp-write-and-lethal-transition | Caller-side HP arguments and flag translation. HP setters are stubs; no HP or death effect. |
| 064 | inventory-class-storage | Caller-side inventory arguments after reservation. Native deduction is omitted. |
| 068, 069 | widget-object | Factory arguments and descriptor/payload snapshots at call entry. Factory, copying, ownership and widget effects are omitted. |

The other records name an exact `none - ...` reason. That means **no matching current
contract**, not exclusion from the database or permission to close a question.
In particular, the procedural RNG in 070/071 is explicitly outside the LCG/MT
contract, and 072..074 run different facing/math entries from those listed by
facing-and-steering. Focus publication, loot selection/retirement, numeric copy-out,
MP writers/cost/consumption, runtime-header acceptance and router dispatch retain
their semantic pages and evidence. A nearby category alone does not provide a link.

## Reader checks and outstanding work

[check.py](check.py) is read-only. It checks every retained body and historical
manifest, both existing metadata parsers, and every selected tool/contract path.
[metadata-check.json](metadata-check.json) retains its output. The one-time prefix
writer is preserved as [recover.py](recover.py); it refuses already-prefixed inputs
and is not a routine maintenance command.

[consumer-checks.json](consumer-checks.json) retains five private reader controls
and both read-only canonical scans. Controls distinguish a prepared record, an
uncited planted record, a dead contract path and an executed record under an empty
section. [consumer_controls.py](consumer_controls.py) is the exact control runner.
No fixture was planted in the canonical database.

Both canonical scans return 1, preserved as findings rather than changed to pass.
All 13 new links await citations; the existing EXP-079 citation gap also remains.
There are 17 older records without a contract field and the pre-existing binding
profile backlink mismatch. These require separate bounded recovery work.

The runtime reader's two new `UNDERSTATED` flags are **false positives**: its denial
regex matches “changes **none** of the 520 bytes” in battle-target-buffer and a
line beginning “none of them survives” in gameplay-generators. Both refer to
behavior or test composition, not absence of evidence. Their raw output is kept
and routed to OPUS in `ASTRA-REQ-OPUS-METADATA-CONSUMPTION`; do not delete
accurate contract prose to silence them.

This recovery restores discoverability. It does not independently repeat the
historical semantic campaigns, resolve their live gaps or substitute for the
required final reviews.

## Publication line-ending correction

The metadata package was committed as `671e6ce`. An additional pre-publication
comparison failed at EXP-056: its raw working body included CRLF, while its
existing Git blob used LF. The next PowerShell command still invoked publication
despite that failed check. This was a command-sequencing error, not a passing gate.

[publication-normalization.json](publication-normalization.json) records the
failure and the subsequent complete comparison: **all 38 committed bodies equal
their prior Git bodies exactly**, and the working bodies differ from those only
by existing line endings. The original raw hashes remain in recovery.json.
The integrity reader now reports raw-byte equality separately and verifies the
original Git text representation across LF/CRLF checkouts. It locates the actual
prefix terminator instead of assuming its byte length survives text conversion.
The original reader, outputs and manifest remain in commit `671e6ce`; the follow-up
does not rewrite that history or rerun a historical FF12 experiment.

[In-memory controls](newline-controls.json) exercise the corrected reader on LF and
CRLF versions of each record and reject an actual body-text mutation in every
record. [Source](newline_controls.py). No canonical body is rewritten by these controls.
