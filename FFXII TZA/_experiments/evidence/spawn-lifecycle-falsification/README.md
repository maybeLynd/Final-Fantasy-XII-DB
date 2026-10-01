# Spawn lifecycle independent falsification

ASTRA, 2026-09-12. Methods A and B; no live game access. The subsystem page is
[REOPENED, section 11](../../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md#11-independent-falsification--astra-2026-09-12).
This package does not complete the database or its required final reviews.

Player version: normal spawn rules survived several checks, but large modded
attempt settings can skip choosing a position and accept old coordinates.
A rejected candidate can leave a distance result behind. The save restore helper
copies only one enemy-state bank although the serializer writes two.

## Identity and retained evidence

Shipping EXE SHA-256:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
Preferred base `00120000`; Capstone 5.0.7; Unicorn 2.1.4.
`primary.json` and `callees.json` contain 14 complete contiguous bodies, bytes,
hashes and resolved RIP references. They prove local mechanics, not live state.

`probe.py` retains the executed instrument. It follows the existing
`cap_policy_probe.py` PE extraction, isolated mapping, ABI checks and trace method.
`feasibility.json` retains the initial empty/one-slot controls. `execution.json`
retains all 40 complete cases, initial writes, provider calls/interventions,
native read/write order, final snapshots, visits and ABI/code checks. Six shipping
bodies execute: 00234DA0, 00235720, 0031E620, 003A1960, 003273B0 and 00239020.
`check.py` independently checks the outcome table and replays 609 reads/117 writes.
Its removed-publication private mutation must fail. `static_check.py` checks exact
body integrity, the local AREA/point CFG and serializer/restorer reference controls.

## Limits and failed methods

Slot lookup, focus handle, field permission, actor positions, actor lookup, clock,
active count and candidate service are controlled providers, not native executions.
The cookie boundary preserves RAX but performs no cookie check. Trap sentinels
at stub entries are harness scaffolding and are not executed. Injected state,
masked FP exceptions and disjoint mapped pointers are explicit preconditions.
The automatic selector's candidate is a stub; AREA output non-publication is
separate complete-body method A evidence. No native initialization, gameplay
reachability, live scheduling, terrain effects or death consequences are claimed.

The first dependency collector included an unverified function key (00327380)
and failed before emitting JSON. That guessed entry and an unused guessed entry
were removed; only ledger-backed complete bodies are in the result. No partial
collector result is counted. The normal sandbox could not import the existing
Unicorn library; a scoped offline execution request granted access. The first
larger probe failed at a stub boundary because zero-filled stub pages allowed
decoder lookahead beyond the page. This incomplete run is not a pass. Adding
trap sentinels corrected the harness; the complete rerun is the retained execution.
No original instructions were patched and no game was launched or attached.

The first feasibility instrument predated only the trap-sentinel/incomplete-run
logging additions. Its two cases had returned and effects were inspected before
the larger run. The corresponding two cases also complete in execution.json.
The final instrument is archived; no claim is made that the pre-edit source hash
was captured. Historical experiments and mutation campaigns were not rerun.

## Reproduction and publication identities

The archived scripts retain the exact executed workspace paths. Their sources
were `Database/Tools/work/ASTRA/spawn-lifecycle-*.json`, and outputs went only to
ASTRA scratch. Reproduction requires the same executable, function ledger and
existing Python/Capstone/Unicorn environment. Use the manifest's source path
mapping in a private scratch copy; never overwrite these historical receipts.
Run the two feasibility cases before the full probe, then the independent check
and static check. Raw source JSON hashes inside check outputs refer to that
recorded workspace serialization. The manifest records both those source hashes
and the published LF hashes; normalization changes no JSON value or instruction.

FABLE/OPUS integration remains pending. L-12 asks for ordinary initialized AREA
output context; L-13 asks how caller 005843E0 and the load sequence rebuild/select
bank and timer state. The local original-code result settles neither question.
