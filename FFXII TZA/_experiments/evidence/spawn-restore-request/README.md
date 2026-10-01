# Restore-specific field request and controller flag bridge

ASTRA, 2026-09-13. [Spawn page section17](../../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md#17-the-restore-request-and-its-controller-bridge--astra-2026-09-13).

Player version: loading has a route that requests the saved field again. The
load controller sets a request flag that the area controller reads before
resetting small script tables and requesting the field. The exact ordering
of their completion messages versus snapshot restoration remains unproved.

Method A only: thirteen original bodies, exact whole-body bytes and hashes,
shipping EXE73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
preferred base00120000, Capstone5.0.7. No B/live run or PC-control session.
The header-validator predicate was already established by EXP058; its body
here corroborates the callers' branch meaning, without replaying that test.

00314530 directly requeues payload1044, sets1062bit5 and105C and requests
manager teardown1,2,3,0. The five-byte00267C90 thunk reaches it. Three native
callers all call00268320 before that thunk.00280140's message18 path chooses
this route when its pointed-to flags+8bit9 is set. Its message1 initialization
points that storage at*(0209AC30)+3F8, so flags+8 is the context's+400.

00285E60 sets that context+400bits9/10. Reused00582860 message12/subtype16
sets its ownC4bit4 and calls00285E60; its message18 has the known
209AC10=1/5843E0 restore path. Exact table bytes and relevant instructions
from the existing whole controller receipt are retained in check.json.
This is the shared native flag bridge, not proof of actual message ordering,
pointer stability, successful initialized load or all intervening effects.

00314440 is the other route: a pending nonnegative field request makes it
return0 without staging; otherwise it calls003145E0 and admits further
teardown only after successful staging.00355940 returns the209AC10 dword
through the VM helper;00355E80 tail-calls its setter with0. Shipping dispatch
records prove call IDs05BE/05BF. The decompiled Trial-script uses are leads
for FABLE to validate against authored bytecode and scheduling, not a new
claim that this flag is Trial-owned or that every load takes those scripts.

check.py verifies source integrity, cited branches and stores, the controller
bridge and two raw dispatch records. Cached rawcalls/RIP exports supply
positive leads only; whole original bodies verify each cited edge. No
exhaustive-writer/caller claim follows from a cache. Script labels still come
from the existing catalog. manifest.json preserves exact source serialization
hashes and canonical LF mapping; reproduce in private scratch with the same
image and ledger. L-12/L-13 and peer consumer review remain open.
