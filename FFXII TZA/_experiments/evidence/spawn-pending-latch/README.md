# Pending latch release and map-bind order

ASTRA, 2026-09-13. [Spawn page section15](../../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md#15-map-setup-releases-the-pending-latch--astra-2026-09-13).
Player version: map setup prepares pictures, placement and navigation before
releasing the hold on actor initialization. Other resource bits can still
delay that initialization. This is a bounded part of the loading sequence.

Method A only: ten complete catalog extents, direct byte comparison against
shipping EXE SHA-256
73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
preferred base00120000, Capstone5.0.7 and per-body/ledger hashes retained.
No new isolated original-code or live execution, and no PC-control session.

00332130 clears pending bit0 and finalizes only old-nonzero/new-zero masks.
00378120 tail-calls it for manager0 after map/navigation setup. 003775D0's
bit3 bind branch calls that setup before clearingbit3 and setting its ready
word. Additional script/state callers use managers1..3; their ordinary
triggers and unread native callees are not established by local call order.
The old-mask0/1/3 distinctions in the page are original-branch readings,
not a new synthetic or live test set.

0025D4D0 clears manager+10bit1, not resourcependingbit0. 0032ED80 zeroes the
whole mask during cleanup without calling the finalizer. Its catalog extent
ends at the range-failure call; failure/helper effects were not executed.
0032F6F0 was a path-string helper, a rejected adjacent lead retained here.
Source checks distinguish the actual latch and init edges from that helper.

check.json preserves selected reference-export rows and the export hash.
Known indexed reset0032F0FF is found; known RIP-base release00332130 is
absent. That blind-spot control prevents an exhaustive-writer claim from
this export. No negative result is promoted to whole-program absence.

Scripts retain actual scratch paths. manifest.json maps executed source
serialization hashes to canonical LF copies. Reproduce with the exact
image/ledger and existing Python/Capstone in private scratch, preserving
these receipts. L-13 still needs save-controller/resource-request linkage
and native field-ID/current-bank/tick preparation. L-12 and peer consumer
review stay open. No full roundtrip, integrated parity or final audit.
