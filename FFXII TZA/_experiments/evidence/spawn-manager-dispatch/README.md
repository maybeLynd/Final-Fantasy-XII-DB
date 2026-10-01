# Manager queue and resource-completion admission

ASTRA, 2026-09-13. [Spawn page section14](../../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md#14-queued-teardown-and-resource-completion-enter-area-initialization--astra-2026-09-13).
Player version: queued area work can initialize actors, clear the party roster,
then unload managers. Requests added during a pass can run now, wait, or be
cleared by the operation in progress. Resource completion is a separate route.

Method A retains ten whole catalog extents from the verified shipping EXE,
SHA-256 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
preferred base 00120000, Capstone 5.0.7, and the ledger hash in each collector.
The previously read 1,689-byte 002628B0 is reused from arena-selector-static;
check.json records its source and body hashes. All retained instruction bytes
are checked directly against the original image. 0032F850's catalog extent
ends with the out-of-range branch's call to 00809728; that failure path is
not executed or treated as a proved runtime return here.

Method B executes only the original 179-byte 0025BFB0 with Unicorn 2.1.4.
Injected Windows x64 ABI, queue dword and distinctive nonzero roster bytes.
0026CE60 and 002628B0 are explicitly controlled providers; neither native body
executes. Trap sentinels occupy provider entries but hooks return before them.
The controlled providers return an unrelated RAX value, testing that the
wrapper reloads its global. Their optional queue changes are interventions,
not ordinary gameplay or evidence of native initialization/unload effects.

Two feasibility controls first distinguished empty from bit-0 work and proved
the roster is cleared between initialization and unload. The unchanged probe
then completed twelve cases: low masks, high-bit preservation and five queue
changes at callback boundaries. Every case has a complete return, intact
stack/nonvolatile registers/code and no invalid memory access. The checker
replays all non-stack reads/writes and each callback's observed boundary state,
and checks exact callback arguments/order plus the final mask and roster.
Across the twelve cases plus two retained feasibility controls it reconciles
53 reads and 55 writes. Private corrupted-publication and swapped-order
controls are rejected. No older mutation or experiment is replaced.

The default sandbox first could not import the existing Unicorn package;
that attempt stopped before a test and was not a pass. A scoped approved
offline run used the existing library. No game, PC-control session, save,
live hook, native callback execution or new laboratory was involved.

Scripts retain the actual ASTRA scratch paths. manifest.json maps their
executed serialization hashes to canonical LF copies. Reproduce in private
scratch with the same EXE/ledger/Python libraries, preserving these receipts.
No claim of live load reachability, initialized manager state, full native
callback effects or integrated parity. L-13 remains open for pending-bit-0
release, save-controller connection and intervening bank/timer behavior.
FABLE/OPUS own the affected party/world-tick/save/type/contract propagation.
