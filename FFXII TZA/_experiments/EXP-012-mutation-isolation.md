---
experiment: EXP-012
title: Isolated mutation cases and honest incomplete verdicts
status: COMPLETE
contract: none - validation instrument, source isolation and campaign verdicts
tool: Reconstruction/Tests/mutation_test.py
method: B - isolated original-code execution
live_game: false
date_designed: 2026-09-10
date_run: 2026-09-10
---

# EXP-012 — mutation isolation repaired; group campaign fails

## Question and verified failure

The old mutation runner wrote into shared production sources. A failed build continued to the
next case without restoring that file; its outer cleanup could also normalize original bytes.
Zero-tested and timed-out campaigns could return success. These defects were verified by reading
the tool; the unsafe version was not executed against production during this experiment.

H1: a noncompiling C mutant can contaminate a later header case. H2: fresh captured dependencies
per case prevent that contamination, including on interruption. Separately, an empty, partial or
invalid campaign must remain distinguishable from a complete campaign with behavioral kills.

## Method and controls

Each baseline/mutant now compiles in a new private directory containing its captured source,
header, driver and local harness dependencies. Production files are only read. Cleanup checks the
resolved temporary directory before recursive removal. Build outputs and compiler scripts are
private; durable build, input-hash, harness and verdict receipts survive cleanup. A timeout owns
and terminates the spawned process tree. Unrecognized output or an instrument error is INVALID,
not a behavioral kill. NO_BUILD and byte-identical executables are reported separately and do not
count as valid comparisons. A selected subset cannot earn a full-campaign pass.

Seven regression controls passed, including an actual MSVC compilation failure, an interrupted
mutant, exact CRLF preservation across a C-to-header transition, empty/partial/invalid verdicts,
and termination of a sleeping process and its descendant. The final run took 2.524 seconds.
Six group-comparator controls also passed. See
[regression-controls.json](evidence/EXP-012-mutation-isolation/regression-controls.json).

An earlier timeout test only checked eventual exit; its 31.6-second duration showed that this was
too weak to prove termination. The test now enforces elapsed time and checks the descendant PID.
Windows process-tree controls ran outside the restricted sandbox so permission denial could not
masquerade as successful cleanup. A group identity-rejection test emitted a ResourceWarning for
an unclosed read handle; it still rejected the wrong executable. This is retained in the log.

The original complete campaign temporarily placed cases under its evidence directory. Database
scanners encountered access-denied paths while those cases were active. All cases were removed;
the final tool places temporary cases under the system temporary directory by default, outside
canonical evidence. Durable receipts remain at the explicitly requested output path.

## Complete generated campaign and affected rerun

Reference executable SHA256:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
The group pilot uses the isolated original-code comparator from EXP-011, including four explicit
ret stubs. The mechanically generated manifest contains 87 sites: 73 C and 14 header mutations.
All 87 ran after a matching baseline. Production input bytes remained identical, and every
baseline/case temporary directory was removed.

The preserved [complete campaign](evidence/EXP-012-mutation-isolation/group-campaign/campaign.json)
reports **FAIL_INCOMPLETE: 64 kills, 13 survivors, 9 byte-identical executables, 1 invalid comparison,
0 noncompiling mutants, and 0 timeouts**. The matching instrument snapshot is
[mutation_test-full-campaign.py](evidence/EXP-012-mutation-isolation/mutation_test-full-campaign.py),
SHA256 `cfefcd3b53ebd2e27c2c387077c0be7c74e9ec44a1484df490e847be9a9b045c`.
Its bytes were recovered by reversing the subsequent index-selection edit and verified against
the original receipt hash. Original inputs, generated candidates and raw results remain intact.

The invalid case was generated index 72: `return 1` changed to `return 2`. The comparator's output
schema incorrectly restricted candidate returns to 0/1. A structurally valid signed 32-bit return
must be accepted for comparison; the unequal value is a behavioral mismatch. The parser and its
regression control now enforce that distinction.

The [affected rerun](evidence/EXP-012-mutation-isolation/return-control/campaign.json) compiled
the **same source and same executable SHA256** as the earlier invalid case and detected a mismatch.
It selected only index 72, correctly reported INCOMPLETE and returned native exit code 3, recorded
in [the process receipt](evidence/EXP-012-mutation-isolation/return-control-process.json).
The original 87-case receipt is not overwritten: this is an affected-case correction, not a second
full campaign. Together the observations yield 65 detected mutants, 13 survivors and 9 identical
executables. They do not earn a mutation pass. The earlier
[one-case limit control](evidence/EXP-012-mutation-isolation/limited-control/campaign.json) also
remains INCOMPLETE despite killing its selected mutant.

## Remaining detection gaps

These survivors refer to the captured C source, not future line numbers. Different executable
bytes are not proof of semantic inequivalence; none is dismissed as equivalent by judgment.

| Generated index | Captured source change |
|---|---|
| 3 | line 14: 0 → 1 |
| 6 | line 23: 0 → 1 |
| 18 | line 42: 1 → 2 |
| 20 | line 57: 0 → 1 |
| 25 | line 63: 0 → 1 |
| 34 | line 81: 0 → 1 |
| 37 | line 85: 0 → 1 |
| 47 | line 100: 2 → 3 |
| 50 | line 101: 8 → 9 |
| 51 | line 101: 0 → 1 |
| 64 | line 126: 0 → 1 |
| 66 | line 126: >= → > |
| 69 | line 136: 1 → 2 |

## Result and scope

This repairs the demonstrated source-isolation and verdict defects and exposes a concrete group
test gap. It does not change production group semantics, certify the other eight pilots, prove
live callback effects or establish integrated parity. Binary identity is checked before the
campaign; actual build and harness receipts bind candidate inputs to the observed executable.
Final instrument snapshots are retained beside the run inputs. A final sealed parity milestone
still needs its required complete campaign. Next work is a bounded analysis of these 13 surviving
sites and discriminating original-code cases, preserving the generated manifest and old results.
