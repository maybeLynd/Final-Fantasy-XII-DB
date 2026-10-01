---
experiment: EXP-014
title: Two missing group image boundaries and the remaining survivor scope
status: COMPLETE
contract: ../05-Spawn-Encounter-Lifecycle/CONTRACT-group-completion-and-respawn.md
tool: evidence/EXP-014-group-survivor-scope/probe.py
method: B - isolated original-code execution
live_game: false
date_designed: 2026-09-10
date_run: 2026-09-10
---

# EXP-014 — exact bkei and flag boundaries detect two survivors

## Question and source evidence

EXP-012 retained 13 different-binary survivors. Two change the image adapter's requested read
width: generated index 47 asks for three bytes for the two-byte bkei, and index 69 asks for two
bytes to access a one-byte flag. The original loads a word at `00263D30` and returns at `00263D37`;
its flag update at `00306FE0` is `or byte ptr [rdi+rcx*8+0x10],1`, after re-reading the group id
at `00306FD1`. Spare bytes in the old images conceal both excessive-width requests.

Prediction: with the required native operand exactly at its image boundary, the unmutated probe
will match original code, and the oversized request will fail its image lookup and diverge.
Moving only the other operand to its boundary should leave that mutant matching: a cross-control
against attributing every difference to either new fixture indiscriminately.

## Controlled experiment

The [probe](evidence/EXP-014-group-survivor-scope/probe.py) constructs two fresh images. Both
contain group 1 with memberMask 2, deadMask 0, arm bit 1, bkei 1 selecting slot 1, and unit bit 47
initially set. The bkei fixture ends its record immediately after the two-byte word and keeps a
full ledger entry. The flag fixture keeps spare record bytes and ends its ledger immediately
after the flag. Both leave every required original operand mapped. These are synthetic image
boundaries, not claims about live allocation sizes.

The original instructions execute in Unicorn 2.1.4 with the four EXP-011 ret stubs. Identity must
match SHA256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
Each call must reach its return sentinel and stack boundary. The baseline and both exact captured
generated mutants are compiled in fresh private directories; all copies are removed afterward.
No production semantics or game state are changed.

The six [observed comparisons](evidence/EXP-014-group-survivor-scope/boundary-run/receipt.json):

| Candidate | Bkei boundary | Flag boundary |
|---|---|---|
| Unmutated | exact match | exact match |
| Index 47, need 2 → 3 | return 0 versus original 1; bytes differ | exact match |
| Index 69, need 1 → 2 | exact match | return still 1, but bytes and callback-visible memory differ |

Every original call completed with four ordered callbacks, dispatch `(unit,0x2005,0)`, and flag 1.
Thus the second defect is invisible to a return-only oracle. Both cross-controls matched.
Source, compiler/driver hashes, commands, raw output and exact post images are retained.

## Durable suite change and affected validation

The existing group comparator now plants both inputs: a dedicated bkei region ending at +0xF8,
and group 63's flag at the end of its region. Its seven padding bytes are omitted from the image;
group 64 remains a separate exact-qword-boundary region, preserving the earlier control.
Five dedicated units are now required, so accepted `--units` is 5..128. The default 48-unit run
contains 102 calls. Original-code-required accesses remain mapped; omitted padding is outside
the comparison image, not evidence that the native program lacks padding.

The [extended suite](evidence/EXP-014-group-survivor-scope/extended-suite-control/campaign.json)
matched on the unmutated baseline: 102 calls, 22 completions, zero callback/return/memory mismatches.
Only affected generated indices 47 and 69 were rerun; both were detected. The runner correctly
reported INCOMPLETE and native exit 3 for a two-of-87 subset. Six instrument regression controls
passed. Production inputs stayed byte-identical during the run and all temporary cases were
removed. This adds two detections to the historical evidence; it is not a new full campaign or
a mutation pass. Eleven of the original 13 survivors remain unresolved under the campaign rules.

## Scope of the other eleven survivors

The preserved original baseline was also rerun with a read hook. All 100 invocation records
exactly reproduced the historical records. Its 863 data reads fit within the exact captured image
regions; another 492 reads were within the private stack. No read lay outside those two sets.
The nonempty data/stack counts control the recorder. Full reads, decoded original instructions
and finite arm-predicate controls are in
[survivor-observations.json](evidence/EXP-014-group-survivor-scope/survivor-observations.json).
This is original-code access evidence; it is not branch coverage of the C adapter.

| Index | Captured mutation and distinguishing boundary |
|---|---|
| 3 | `GroupImage_At` missing-region return 0 → pointer 1. Adapter failure behavior is not exercised by the valid original data accesses; a malformed image is a separate instrument test. |
| 6 | `load_q` missing-region fallback 0 → 1. Same untested adapter failure boundary. |
| 18 | `load_b` missing-region sentinel -1 → -2. Both are negative; no native unmapped-read equivalence is established. |
| 20 | Map null guard compares 1 instead of 0. Supplied maps have neither address; null fallback may conceal a crossed guard. Native lane lookup explicitly tests null at `002360D0..002360D3`. |
| 25 | Count guard `<0` → `<1`. A zero count is rejected later for every nonnegative bkei as well: byte count load/decrement/compare at `002360D9..002360E0`. This boundary does not distinguish the returned lane. |
| 34 | Unit null guard compares 1 instead of 0. The null case still returns 0 through the image adapter's missing-pointer fallback; output equality does not prove identical internal reads. |
| 37 | +0x698 pointer null guard compares 1 instead of 0. A null pointer can then encounter the image adapter's negative kind fallback and still return 0; address 1 is not a supplied record. |
| 50 | High-byte shift 8 → 9. Every nonzero high byte produces an index above 255 in both expressions; native count is a byte, so both are rejected. High byte zero gives the same index. This is a bounded range argument, not byte-identical executable evidence. |
| 51 | Missing bkei fallback 0 → 1. No missing bkei operand occurs in the captured native read domain; original unmapped-read behavior is not a successful fallback contract. |
| 64, 66 | `arm>=0` → `arm>=1` / `arm>0`, before `arm&1`. All possible adapter returns (-1 and bytes 0..255) have the same combined predicate; 257 finite controls are retained. The original tests bit 0 directly at `00306FB6`. |

These explanations do **not** reclassify different executables as EQUIVALENT, alter the generated
manifest, or erase surviving results. The instrument's established exemption remains identical
executable bytes only. A broader adapter-failure contract or independent helper test would need
its own scope and must not be promoted as original-game parity. Native callback effects,
live initialization and scheduling remain outside this experiment. The two demonstrated gaps
are repaired; further input padding changes would not distinguish the remaining hypotheses.
