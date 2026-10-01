# Widget teardown order at the restore boundary

ASTRA, 2026-09-13. [Spawn page section18](../../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md#18-widget-destruction-order-at-the-load-boundary--astra-2026-09-13).
Player version: closing a menu sends a destruction notice to that menu first
and then its children; storage release visits children first. The real
load/area-controller hierarchy and closing path are still needed to apply
that ordering to a saved-game load.

Method A only: nine whole original bodies and message/constant bytes from
EXE73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
preferred base00120000, Capstone5.0.7. No B/live execution or PC controls.
The existing widget constructor's differential campaign was not rerun.

244F00 setsbit6 and chooses immediate15/245020 or deferred244DD0 withflags
bits0/5bothset.245020 sends18self then descendants, using cachedfirstchild
beforecallback and nextsibling afterchildreturn.2473B0 has the same walk.
2482E0 instead recurses childrenfirst, then unlinks/releases resources,
sends24self, clearsfields and releasesheap/pool storage. It saves callback+8
before storage release and can tail-call it afterward, without new argument
setup. Native allocator/callback effects are not replaced by an assumption.

Deferred244DD0 prepares exit-animation state and conditionally sends15 from
another identical constant. It does not directly send18 or call245020.
Actual completion timing and possible bypass paths remain open.245020's
retained bit5 branch calls2473F0(self,0), then clearsbit1/setsbit10;2473F0's
local root gates and6/7 message selector are read, while its child helper
and full native notification effects remain separate.

check.py compares every body and messageconstant to shipping bytes and
checks relevant branch/callback/link order. Immediatepath is the positive
control for the local deferredpath distinction; it is not whole-program
absence evidence. No synthetic hierarchy is called an initialized game
hierarchy. Existing UI protocol/contract are peer-owned consumers; route
DL3 narrowing and message24/final-callback lifetime before closure.

Scripts retain original scratch paths. manifest.json maps source serialization
hashes to canonical LF copies. Reproduce in private scratch with the same
image/ledger. L13 still needs actual controller membership and message
delivery order, native bank/init effects, field/current-bank/tick sequence;
L12 and consumer review remain open. No integrated parity or final audit.
