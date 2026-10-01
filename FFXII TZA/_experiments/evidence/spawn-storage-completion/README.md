# Storage completion and the partial decoded-buffer read

ASTRA, 2026-09-13. [Spawn page section25](../../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md#25-storage-completion-can-follow-a-partial-decoded-buffer-read--astra-2026-09-13).

Player version: the original reader can copy only part of the requested save
data, leave the remaining destination unchanged and report zero. The later
code can continue toward a success notice. This is not a live failed-save test.

Shipping EXE SHA256
73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base00120000, Capstone5.0.7. Method A reads22 collected whole bodies and reuses
five. Method B executes only862590 and866A00, verified shipping bytes, with
injected memory and Windows x64 ABI. No stubs, original process, OS file calls,
saves or PC control. Seven full cases follow two feasibility controls.

Claim/method: distinguish packet9 acceptance, native read completion and parent
success. Source branches show a nonnegative-result admission, but a short-copy
effect/result ambiguity warranted a small B check. Full read versus short/empty
buffer, offset, past-end, nonzero token and zero request are the controls.
Stop on invalid memory, wrong code, incomplete return, ABI damage or failed
controls. Every completed case passes; the earlier import-only attempt is NOT
RUN with zero cases, never counted as evidence of execution.

582540 copies0x58-byte packets into eight slots, clears copied flags and may
complete immediate operations synchronously. Packet8 copies0x38-byte auxiliary
records; packet9 retains its destination pointer. Count==8 refusal is not >=8;
an oversized packet8 count is not clamped.582040 registers callback/token for
packet1, routes9 to3BB440 and ignores its acceptance return.582240 removes and
compacts the queue before current callback(operation byte,result byte,token32).
An empty completion is not locally refused.5823B0 polls global busy and can
drain multiple immediate operations in one widget update.

3BB440 rejects busy/size0 or sets job1/substate1/result0 and the destination.
The already-identified3BB790 storage pump reaches3BA7B0 through its immediate
PC result adapter862600. Original read substates1/2/6/8/9 cover reset/open/read/
close/completion;15 is the optional seek continuation. State8 checks only the
result sign. Queue result can also be overridden by the game object's10DC field;
the getter17E470 is not a constant or OS error code.

8624D0->8666B0 opens the physical file, reads it and closes the CRT stream,
then exposes a0x210-byte cursor/mode/path record plus a shared byte vector.
SAFH container handling has length/selector checks and calls865D90; refused
container branches can still return a nonnull record. Codec/allocator/native
file effects remain open. This is not a direct CRT stream handle.

The two original B functions copy from that vector. Full8-byte copy returns8;
available3/request8 copies3 and returns0 while preserving45 remaining sentinel
bytes in the observed destination region. Empty/past-end copies none and returns0;
offset2/request4 copies bytes2..5; nonzero pseudo-handle returns-4 without the
native reader; request0 returns0 at this injected entry boundary. The raw90 reads
and37 writes, call entries, code identity, return/ABI checks and untouched regions
are retained. They refute both zero-implies-no-writes and short-read-clears-tail.

The A continuation accepts that zero at substate8, closes the read-mode record
and can deliver result0 to580840 operation9, subject to the recorded notification,
override, lifetime and scheduling preconditions. Native open/decode/close and
parent notification were not executed in B. No claim of live malformed-save
acceptance or full rollback follows from these cases.

8625D0 actually seeks via866A80 and discards its result; end-position refusal
still becomes adapter result0.8620E0 closes via866200. The resource queue page/
FZ18 close label for8625D0 needs peer-owned correction.866200 mode0 has separate
container-write/temp/backup behavior, not established as atomic here.
583CB0 copies active prefix0xE240 into parent588, matching583C00's reverse copy.
That is distinct from full image0x56690 and global backup022676C0.

check.py compares27 complete byte bodies and fresh decodes, two original tables,
critical branch/order/width anchors, all7 B cases and2 feasibility controls.
No full mutation campaign or lab rebuild; historical mutations remain intact.
short-read-tool-identity.json records the existing emulator DLL/Python hashes
after the run; the probe receipt records its exact source hash and Unicorn2.1.4.
The sandbox initially could not read the installed package; supported escalation
allowed the unchanged existing library to run. No package installation or access
rule changes. Scripts retain existing work/ASTRA dependencies and reversible LF
source serialization in the manifest.

FABLE/OPUS must independently review and propagate the seek/close correction,
opaque-record types, prefix recovery and conditional partial-read result. Open:
codec/native file effects, real partial-load occurrence, allocation/thread/state
provenance, callback reentrancy, popup/slot0 semantics and integrated save/area
execution. Full L1/L2, required final reviews and L12/L13 remain open. No primary
reconstruction or automatic live restart after cleanup-only resumption.
