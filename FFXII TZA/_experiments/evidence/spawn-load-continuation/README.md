# Spawn load continuation: selected image and caller boundaries

ASTRA, 2026-09-12. Method A only. No new isolated execution or live game access.
[Spawn page section 12](../../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md#12-save-image-selection-and-continuation--astra-2026-09-12)
records the findings; L-13 remains open for complete bank/timer ordering.

Player version: loading selects one enemy snapshot, or skips restoration in one
branch. Capturing the second snapshot preserves the earlier snapshot from the
active save image. Area initialization separately rotates enemy banks; these
local paths alone do not establish the complete load sequence.

Shipping binary SHA-256:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
Image base `00120000`; Capstone 5.0.7. Reused exact PE/body collector from the
previous spawn falsification and presentation packages. Raw JSON retains 20
complete original bodies, contiguous instruction bytes, hashes and RIP targets.
The filename metadata_leaves.py is a collector name: its three bodies are
wrappers with calls/tail jumps, not proven effect-free leaves.

The 174-B restore caller has mutually exclusive A/B/skip branches. The 143-B
capture caller maintains A when capturing B. The copy helpers provide independent
size/direction controls: group200, keep image20010. Both coordinates (whole-image
and payload after header200) are explicit on the page. The 1777-B controller's
dispatch tables are actual image-relative code targets, not exception metadata;
check.json retains all bytes and hashes. Message18 reaches the relevant branch,
whereas message1 maps elsewhere. The 390-B area initializer independently calls
the existing bank rotation after its enable gate and earlier native calls.

check.py verifies all body extents/hashes, table targets and the load/copy branch
instructions. Its truth table is a static derivation, not an emulated or live
campaign. Whole-program alias, scheduling, callback effects and the correctness
of every other controller branch are not claimed. Wrappers003139D0/00304790/
003047C0 call003EBC50 and tail003EBD00; those downstream effects remain outside
this package. EXP056/057 native evidence was not replayed. Getter bodies were
only re-read to fix the address coordinates.

Archived scripts retain executed ASTRA work paths; the manifest maps them to
these files. Reproduce in private scratch with the same EXE, functions.tsv and
existing Python/Capstone installation; never overwrite historical receipts.
The manifest preserves raw source text hashes alongside published LF hashes.
FABLE/OPUS own consumer integration under the existing spawn-lifecycle
contradiction requests. No independent audit award or database completion.
