# Root retention and the resource-ready message

ASTRA, 2026-09-13. [Spawn page section20](../../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md#20-root-retention-and-resource-ready-delivery--astra-2026-09-13).
Player version: a UI parent passes down the setting that lets a menu keep its
storage after a closing notice. Resource completion supplies the message that
attaches the load menu, but equal request counts do not prove valid content.

Method A only,13 new and8 reused whole bodies, exact shipping EXE
73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base00120000, Capstone5.0.7. No B/live execution or PC control.

2445D0 message1 sets rootflags0/1/5 and copies its descriptor selector; other
messages return0 locally.248220 propagates5 through2418E0/2463F0.245020's
post-notification bit5 choice therefore has a concrete producer in this
attachment chain, conditional on later callbacks preserving it.247490 gates
not just its own notification but its entire descendant recursion; unchanged
or disabled intermediate nodes prune the subtree.

249580 allocates one of12 zeroed 0x20-byte batch records at2090790 and stores
the owner pointer.582790 calls it with the load widget, requests resources,
and finishes with249410. Seal setsbatchbit1; equal requested/completed16-bit
counts dispatch16 to the owner's handler when mode+4 iszero, then clearactive
bit0. Member adapter2495C0 first signextendsECX to its record pointer, invokes
its materializer if present, incrementsbatchcompleted, conditionallydispatches,
then releasesmemberbit0. Native materializers249660/249670 remain unread here.

2494F0 is the alternate explicit completion entry. Allthree local completion
paths testsealed/equalcounts, notactivebit0, so clearingactive alone is no
one-shot guarantee. Customcallback paths do not clearbatchactive;2495C0's
customcallback site does not prepare RCX=batch, unlike the two direct batch
entries. Do not invent one uniform callback ABI or equate count equality with
successful resources. No actual allocation pressure, callback mutation or
request scheduling was executed in this package.

check.py verifies all21 bodies againstshippingbytes and local call/write/branch
controls, including rootflaginheritance, the skipped recursivebranch, owner
construction and notification-before-release order. Priorrawtables establish
that16 enters the load handler's known attach path; they are linked through
the earlier hierarchy package rather than copied again.

Manifest records source serialization and canonical LF hashes. Reproduction
uses retained scratch paths in a private directory with the same reference.
Independent UI/resource/type propagation remains with FABLE/OPUS. Actual load
restore order, later retained-widget reclamation, callback/materialization
effects, initialization/lifetime and L12/L13 remain open. Full L1/L2 and final
reviews are not complete; no reconstruction phase or integrated parity.
