# Suspended-action copy origin

Task ASTRA-SUSPEND-RESTORE-COPY-ORIGIN-1001. Consumers: OPUS command contract,
FABLE action ownership, and ORACLE's original EXP-091 producer.

Question: does original 30EDA0 restore 0x4F0 bytes at unit+730 or unit+6B0?
The published EXP-091 summary, its check.py comment, and CONTRACT-commit-action
row use +730. The actual first store uses [rcx-80] after advancing rcx by 80.
Hypotheses: cursor is the start address; or store displacement cancels the
advance and restores the earlier action block. A complete finite-loop footprint
distinguishes them. Also identify whether +714 and +B88 are copied and whether
the bitmap release retains the incoming source pointer after +B88 is overwritten.

Method A is sufficient: certified original instructions, reviewed memory roles,
finite constant-count copy-loop symbolic address calculation, complete tail,
and checked source prerequisites. No harness or live run is required to decide
the local copy origin. Source and destination must be valid disjoint buffers;
natural allocator placement, aliasing, scheduling and lifetime remain separate.

Reuse the reviewed capture/annotation/CFG helpers. Capture only the three
bounded original bodies (30EDA0 restore, 30EFF0 snapshot, 30DFA0 allocation).
Controls: actual source positive, failed upstream capture, missing source,
coherently reannotated first-store displacement mutation rejected against EXE.
Check every interval, loop counter and tail; no empty/partial result can pass.
Acceptance is exact interval coverage and original-pointer carrier, not a green
script alone. Stop on changed image/dependency/decoding/incomplete prerequisites.

No process control, native execution or save/config/reference changes. Finite
Python children exit normally. Preserve published EXP-091 as history and route
an additive correction plus the minimal producer regression to its owner;
do not edit peer files or rerun the 85-case campaign to inflate coverage.
