# Native relation cache: conditional invariant and exact removal effects

Producer-valid Method A; independent review and canonical consumption pending.
No original machine instructions, emulator, live game or gameplay were run.

## What the player would know

The game keeps small records linking a recipient, an acting character and a
target. Ending a relationship removes its active marker and updates a linked
list. The code contains two removal paths, but a correctly formed live record
cannot satisfy both on the same notification. A broken record can; the remover
does not protect its counters against a second removal. This is a conditional
implementation fact, not evidence that normal play creates broken records.
Natural summoner KO / Esper behavior remains a separate open question.

## Question and method

EXP091 patched 00512F30 to RET. Its dispatch/notification samples therefore do
not prove this native handler's effects. Are those effects opaque callbacks, or
a closed local cache operation? Can its two syntactic removal sites both run
on one coherent matched-kind2 notification?

Method A is sufficient: retain verified shipping bytes, qualify the entry/CFG
and every normal transfer/write, derive the equality gates and exhaust their
equality patterns. A native harness is unnecessary for the named CMP/JE/JNE
conditions and byte decrement. Process observations would be needed for actual
binding, initialization/reuse and normal scheduling, which this package does
not answer. An RT label is not a reason to open the game.

## Identity and starting evidence

Authorized EXE SHA256
73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
image base 00120000. Capstone 5.0.7. Actual capture adapter reg_tracking.py
5fcc64842c96d99c3ef9df4f7e3adc528dfad0dfd44b2f6bb5bf43beda092a38;
byte-role validator 7c4ea9f6e3a937ea65a2863c92fe4abfd1b2bf08ad1e481c0cd1393c5b7a5f13.
The qualified capture path really invokes the reviewed adapter and its store,
LEA/address and read-modify-write controls; this is not merely an optional path.

* source-native-event-boundary-01.json: SHA e954c611838d373bafde92d6b4118fb22695ee0b26a6fbf3d6476907f5a04215;
  00512F30..00513144, 532 bytes / 161 instructions / seven chained unwind fragments.
  Original range bytes SHA 0c7b71f3a5dda00683960be0d765dc6271bc5e06b98c3ab024f5cb643c0869ae.
* source-relation-remove-leaf-01.json: SHA 974aec9544ed4837a248d4c4f669435c6bbd24e232beb4906cef3037d64f911a;
  entry-reachable 00512CD0..00512D72, 162 bytes / 47 instructions.
  Original bytes SHA 197fdb36ea18ad0920eb3c31b0ca3cb2d09e93ba850f53bf4765ab4218886abf.
  No covering .pdata row. A bounded direct-successor/RET worklist, absence of
  calls and the next known entry 00512D80 qualify the leaf. No root is invented.
* source-ko-notify-01.json retains the original 00313B30 notification body,
  410 bytes SHA ae38b605a33a5e7bf053f2482cf02f9d9e89625bad67651bf586dedd1c2ef4c1.
  It provides packet context, not execution or natural reachability.

The source qualifiers and current producer have actual terminal0 receipts;
raw bytes, memory roles, CFG, statuses and stderr/stdout are retained.

## Original effects and representation

The notification record is 16 bytes: kind at +0; Boolean flag at +1
(00313C3D TEST / 00313C40 SETE / 00313C59 store); recipient UID at +4;
actor UID at +8; target UID at +C (00313C6E/76/7E). Source-pointer equality
sets kind1 or kind2 (00313C50/5E/63). These are source facts, not a live identity.

00512F30 copies receiver RCX to R11 and packet RDX to RDI. Kind1 and kind3 use
inline DWORDs +0/+4/+8 and flag-byte operations at +F. The kind2 arm uses
32 fixed 16-byte slots at 02CA81F0, an allocation cursor at 02CA83F0 and linked
owner indices. Node +0/+4/+8 hold recipient/actor/target; +C is the own index,
+D previous, +E next, +F low-nibble occupancy/kind. The inline owner block has
head +C, tail +D, count +E. Existing DATA embeddedBlock0650 access/layout census
is prior credit; it is not an ASTRA recensus or a proof of every field meaning.

The complete handler has 26 persistent write sites; the remover has 11.
Its only native transfers are call 00513005 and tail 00513022 to 00512CD0.
There is no imported callback or heap-free in this bounded two-body closure.
Valid disjoint receiver, packet, stack and pool objects remain required.

00512CD0 splices previous/next and owner head/tail; ANDs node+F with F0;
unconditionally decrements owner+E and byte 02EBA481. It does not check
occupancy or prevent byte underflow (0 becomes FF). It does not clear the
removed row's DWORD IDs or link bytes. A slot becoming inactive is not heap
deallocation. Allocation increments that counter and updates 02EBA480 with an
unsigned maximum at that point; outside writers and whole-program monotonicity
are not proved. Self-slot indices must already be initialized consistently.

## Invariant, discriminator and result

Creation on a miss requires flag0 and recipient UID != target UID
(00512F94/98 and 00512F9D/A0). For a matched kind2 row, the handler first
removes when flag1 and node.target == packet.target (00512FF1/FF5/FFA/FFD,
call 00513005). It next tail-removes when packet.recipient == packet.target
(0051300D/10, tail 00513022). Otherwise it stores packet.target to node+8 at
00513027, including after the first removal; that can change an inactive row.

Under packet.recipient == node.recipient, matched actor identity and the live
invariant node.target != node.recipient, both removal tests cannot be true:
they would require node.target == packet.target == node.recipient. When no
removal happens, the new target remains different from recipient. The exact
leaf preserves R11/RDI and relevant packet/target values; that preservation
is checked from this code, not assumed because these are volatile registers.

The reducer exhausts all 203 equality partitions of six uint32 identities and
flag0/1. Twenty partitions/flags satisfy the coherent matched-state premises;
zero double-removal or surviving-live-invariant counterexamples. A deliberately
broken premise (all six IDs equal, flag1) reaches both sites. The equality
domain is exhaustive for these conditions, not 406 native/game samples.

## Controls and failed prerequisites

Current producer prove-native-relation-invariant.py SHA
769766d329f7f472f1d5eeba91ef29c6434b68ff7acab2a725cc63d61d147930;
result-native-relation-invariant-02.json is current. Four explicitly synthetic
source-record controls are refused by their intended detector:
reversed matching-target branch (coherent double-remove counterexample),
ignored creation inequality (creation counterexample), changed remover
DWORD+8 write (value-preservation footprint), and new owner+714 store
(complete handler write envelope). They are not native byte mutations.

Actual current CLI receives the labelled failed qualification receipt:
terminal exit1 / exceptionnull, specific upstream rejection and no output.
check-native-relation-prerequisite.py SHA
82876fb44b7dfc20d7f8494f2cac5e76216956239e5a22a23a6222874e94a95a
checks that invocation and a matching successful current producer. A failed
wrapper exit alone does not count as this control.

The first notify qualification assumed one physical row and failed; retained
preimage/receipt precede the seven-fragment CHAININFO correction. Original proof
v1/result01 lacked an asserted complete handler write envelope. Preserve them
as history; current result02 adds that assertion and its concrete control.
No old published result was edited and no unchanged settled sample was repeated.

## Limits and affected consumers

This is a conditional original-source proof, not live defaults, cache binding,
lifetime/reuse, all callers, all packet kinds, all outside writes, corrupted-list
termination, all malformed-pointer safety or integration/parity. A linked-list
cycle can invalidate normal-return assumptions. The double-remove witness is
not proof that natural play reaches that malformed state. No whole UQ147 or
OV-row closure; natural summoner KO / Esper113, real scheduling and presentation
remain open. No new complete formerly-runtime row is credited before acceptance.
This package removes the need for live observation of this local handler's
opaque-callback/effect and coherent double-removal questions only.

SPEC must independently inspect qualified bytes, equality abstraction,
assumptions, effects and concrete controls. OPUS owns cache type/ABI/contract
preconditions and EXP091 stub-limit wording. FABLE owns semantic UQ147 framing.
Do not rename a field or erase a runtime dependency merely from physical access.
Returned target-fixup and boundary-correction reviews are separately ACCEPT
(342644f78 and 76143cef7); ORACLE's resolver repair 78271194d is separate Method B
producer evidence, not ASTRA execution or automatic independent acceptance.

## Reproduction and cleanup

Use the repository venv with Capstone5.0.7 and the pinned adapter/validator.
Copy the frozen package's producer/input files to a fresh child of existing
Database/Tools/work/ASTRA/runtime-residue-method-retriage, preserving filenames;
its parent supplies validate-title-source-annotations.py. Current producer to
a fresh result name reproduces the proof without the game or recapture. The
qualification scripts additionally need the authorized EXE and the actual
ov42-gauge-callback-binding/capture-index-path.py; dependency copies/hashes are
included for review. Never overwrite the retained result/status files. Re-run
the failed-prerequisite invocation only with fresh receipt tags/output names,
or inspect its preserved actual receipts. No general runtime platform is needed.

No game launched, PC control, attach, memory/native write, emulator, save/config
or reference write. Finite CLI children/shells exited; no runtime/publisher lease
is part of the science. Only our handles/processes may be closed; no peer process
or dirty file was reset. Published inputs/results remain immutable.
