# Summon selector producer does not enforce the Esper band

Player version: summon mode chooses a fourth-slot definition from a saved byte.
The script-facing setter and the mapping step do not check that this byte names
one of the thirteen Espers. This is a code finding, not an observed bad summon.

Question: can the original selector API/map arm establish the type27..39
precondition required by309230's Dismiss table branch? H1 was a local band
guard; H2 was low-byte storage plus FF empty conversion. **H2 is supported.**

Method A, verified shipping EXE
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
Original59B50FFB0,14B3139C0,15B3137E0 and1253B3266C0 are captured/redecoded
through the actual shared reviewed access-role adapter. The1253B body is
closed by its actual local CFG, not by taking its first15B .pdata fragment
as a whole-function size. No process state, machine-code or gameplay execution.

50FFB0 calls267E10 twice on the same VM stack object. It preserves the first
EAX in EDI, then passes its low byte DIL (zeroextended) to3139C0. That setter
storesCL at battle-state5AD4. It then forwards the second popped EAX, preserved
in EBX, in fullECX32 to313550. Neither the bridge nor the byte setter adds a
27..39 guard. The two-pop order is an observation of original code; argument
names and the Pop/coercion's full behavior are not inferred here.

3137E0 reads5AD4 as a zeroextended byte. Under the mode1 arm's stated entry
preconditions,3269D2 obtains the summoner index and3269DA obtains that byte.
The four-iteration loop propagates it to slot3 of maps1,2,4 at state offsets
5A60,5A72,5A96; byteFF instead becomes wordFFFF. No27..39 test intervenes.
Other first-four slots preserve the summoner index or becomeFFFF.

The map claim ends at326A34 **before the shared actor/application tail**.
Prerequisites: normal original callees, x64 nonvolatile ABI/private valid
frame, a valid same battle-state block, writable maps and no intervening
alias/foreign/callee writes. The complete function CFG records callee
boundaries; it does not prove their effects or return-time map stability.

result-02.json contains the exact pins, graphs, three store identities,
all256 mathematical byte cases and ten illustrative raw-integer mappings.
The byte enumeration is a finite source calculation, not256 native tests,
captured startup values, or proof all inputs occur in authored programs.
The13-member authored summon table is existing evidence, not a new census.

Reproduction, from repository root using the existing analysis venv:
`prove.py FRESH_OUTPUT --src PACKAGE_DIRECTORY`. Source files, original EXE,
checked capture receipts/driver and shared dependency hashes are prerequisites.
Actual producer positive plus three actual CLI refusals are retained:
failedcapture; missing source; coherent same-count/length DIL->AL mutation
that would select the second pop instead. The original byte identity check
rejects the latter even though its disassembly annotations remain coherent.
Failures must have exact diagnostics, no result and complete case cardinality.

The first actual CLI wrote a relative output filename at the repository root;
the control correctly refused its missing package positive before running any
negative cases. That invocation is INVALID for package delivery. Its exact
driver/output and source/controller preimages remain retained. The producer
now resolves relative outputs against its package directory. Corrected proof02
and control02 are the valid package receipts; no unchanged failed retry.

Downstream required change: qualify OPUS/FABLE's pending presentation-domain
work so mode1/mapping alone cannot prove an Esper-band initialized stats
record. Native-domain proof is complete only at this local scope.
**Still open:** authored arguments, other/bulk saved-state writers, actual
ApplyUnitDefinition/party-read initialization and lifetime, natural Dismiss
acceptance->execution, and the type seen by309230 at its actual invocation.
No automatic broad OV42/21 closure or independent acceptance.

Cleanup: every own helper is finite/terminal; no PC/game/instrumentation,
saves/configuration/reference binaries or peer processes were changed.
