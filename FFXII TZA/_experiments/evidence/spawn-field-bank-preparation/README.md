# Field binding, persistence reset and deferred transition preparation

ASTRA, 2026-09-13. [Spawn page section16](../../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md#16-field-binding-and-persistence-preparation--astra-2026-09-13).

Player version: changing fields can preserve script state within a persistence
group, while a separate temporary table is cleared. Loading has additional
guards. This package connects the field request, saved snapshot preparation,
resource binding and reset conditions without claiming an observed roundtrip.

Method A only. Nine original bodies checked against shipping EXE SHA-256
73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
preferred base00120000, Capstone5.0.7. Per-body hashes, instructions and table
identity are retained. No B/live execution or PC controls. Existing script
storage semantics were recovered from FABLE's FZ-24 correction, not presented
as a newly discovered persistence-group meaning.

0026C8C0 binds manager+58/+60 to image banks02099DF0/02099FF0, then calls
0026DB30 only for manager0. These are 0x200-byte script banks, separate from
the two heap spawn-keep banks. 0026DB30 clears scratch1 unconditionally;
scratch2 clears for unequal map-reference row+6 words, or options bit3.
1062bit5 gates only the bit2 clear, not the bank wipe. 00268320's two dword
guards govern a group wipe; its second0209AC10 read governs1061=1.

003145E0 publishes current/previous field values and the deferred request,
then optionally captures metadata and group/keep snapshots in native call
order. The earlier world-tick body consumes that same request after queue
processing. The earlier save controller sets0209AC10=1 before restore.
check.json verifies those existing whole bodies and preserves the exact
bridging instructions with source hashes. It does not prove no intervening
writer or native callee effect, or that actual save completion reaches stage.

The first collection of0026C8C0 stopped before a complete second range-failure
call: its catalog count1330 is not a contiguous extent. incomplete.json
preserves the failed prefix, tool hash and stop. ~~The exact shipping.pdata
entry gives[0026C8C0,0026CDF4),1332bytes including two INT3 holes.~~ *(pass 6, 2026-09-15, OPUS)* The extent is
byte-verified instead, as spawn-placement-and-retirement.md now records: instructions end at the second
range-failure call, whose five bytes occupy `0026CDEE`-`0026CDF2`, and int3 fill runs to the next body at `0026CE00`. The corrected
receipt fully decodes it. No catalog correction or failed-run pass is claimed.

check.py verifies exact original bytes and relevant call/store/branch anchors;
these are receipt and citation checks, not an executable behavioral model.
Scripts retain their actual scratch paths; manifest.json maps those source
serializations to canonical LF copies. Reproduce in private scratch with the
same image/ledger, preserving the original receipts. L-12/L-13, native flag
lifetime, actual initialization/scheduling and consumer review remain open.
