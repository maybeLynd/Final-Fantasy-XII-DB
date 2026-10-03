# Suspended action restores the live action block

ASTRA-SUSPEND-RESTORE-COPY-ORIGIN-1001. Method A, STATIC_ONLY.
Producer validated; independent acceptance and canonical incorporation pending.

## Exact question and result

Original 30EDA0 restores **0x4F0 bytes to unit+0x6B0**, covering the half-open
interval `[unit+0x6B0, unit+0xBA0)`. EXP-091, its check.py comment and
CONTRACT-commit-action incorrectly describe unit+0x730 as the copy origin.
The +0x80 adjustment advances the loop cursor; the first destination store
at 30EDC7 uses `[rcx-0x80]`, cancelling that advance. Every source and
destination interval is accounted for in result-01.json: nine groups of
eight 16-byte copies, followed by seven 16-byte tail copies, 79 in total.
These are statically calculated intervals, not 79 native tests.

The original paired snapshot 30EFF0 copies that same unit interval to its
allocated slot. Restoration therefore includes the phase at +6B4, current
action ID at +714 (saved offset64), and pointer at +B88 (saved offset4D8).
The prepared-slot bytes +694/+695/+696 lie outside this copied interval.

Restore loads the incoming source from +B88 into R8 before copying. That
register is not rewritten before the slot comparison at 30EE5D, even though
the copy overwrites the unit's +B88 with saved content. Slot release uses
the incoming source, not a reload of the overwritten field. An exact match
among eight 4F0-byte slots clears that slot's bitmap bit; no match still
returns1. The saved +B88 value is not automatically null, unique ownership,
or evidence of nesting/reuse safety.

## Evidence and reproducibility

Shipping EXE SHA256:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
source-01.json retains complete original bodies 30EDA0..30EE9A (250 bytes),
30EFF0..30F121 (305 bytes), 30DFA0..30E010 (112 bytes). Annotation validation
uses the reviewed access-role adapter in the actual capture path, including
store, address-only LEA and read-modify-write controls. Complete local CFGs,
checked capture status and original byte comparisons precede address reduction.

run.py preserves actual terminal/exit/exception status and raw stdout/stderr
for capture, proof and controls. There is one valid positive producer run and
three actual CLI refusals: failed required capture, missing source, and a
same-length first-store displacement mutation coherently reannotated/rehashed
but rejected against original bytes. These control evidence integrity; they
are not altered native FF12 executions. No incomplete or zero-case run passes.

To reproduce, copy the immutable base packet into a disposable directory
inside this repository, remove generated result/control outputs from the
copy only, then run `run.py proof-new prove.py result-new.json`. Negative
case inputs use exact hash-bound inherited base files plus retained overlays,
explicit removed files and raw refusal receipts. Never edit the frozen packet.

## Consumer correction and producer cause

correction.json binds exact read-only preimages of the three affected records.
The old EXP-091 `canc-cpyhit` predicate checks entry and bitmap release, not
destination boundaries. Its 85 cases and 10 mutations remain ORACLE's historical
work and are not new evidence credited here. Required owner follow-through:

- ORACLE adds a bounded original 30EDA0 case with a patterned disjoint source,
  poisoned destination and canaries at unit+6AF / unit+BA0. Check all 4F0 bytes,
  including +714 and +B88, and distinguish the incoming R8 release pointer from
  copied field contents. Preserve old runs and mutations; no full campaign
  repeat is necessary solely for this new local check.
- OPUS and FABLE add the corrected copy domain and restore-pointer contract
  to their owned consumers, preserving the old prose as corrected history.

## Limits and cleanup

Address/order proof only: no native or emulated original execution, live
observation, natural reachability, allocator lifetime, scheduler or integrated
parity claim. Source and destination are assumed mapped, valid and disjoint;
general overlap safety is unproved. Snapshot's native allocator/memset must
return normally; tags or stubs do not establish their effects. Slot reuse,
natural ownership and concurrent writes remain open where required.

All bounded Python children terminated; no PC control, FF12 process, services,
instrumentation, saves, configuration, reference binaries or peer work changed.
