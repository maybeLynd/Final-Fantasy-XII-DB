# Original resolved script-variable store (67)

Method B: verified shipping0026D530's full call-free194-byte leaf and original
24-byte/six-target table, in initialized disposable Unicorn guests. Exact EXE
SHA25673461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8.
Entry/branches/table targets/RET graph closes over the supplied original body.
Source-derived bound, not a claimed .pdata function extent. No stubs, calls,
original POPV/normal caller execution, native CPU or game automation.

ABI RCX points to supplied48-byte result record. +10 is destination base,
+18 packed descriptor, +1C signed element index, +20 supplied dword. Width
is bits28..31. Stack/return sentinel, guard memory and MXCSR1F80 initialized.
Shared reviewed adapter is compiled directly from pinned source and invoked
for each decoded memory operand; raw Capstone access flags are not substituted.
Provider files and limits retained. Actual effects/order, not return value alone,
are checked. Full RET/stack advancement, record/code/table/stack unchanged and
only expected guarded destination writes required for every case.

| Width | Original write policy for supplied dword | Element stride |
|---|---|---:|
| 0 / u8 | signed-input clamp0..255, byte store | 1 |
| 1 / s8 | signed-input clamp−128..127, byte store | 1 |
| 2 / u16 | signed-input clamp0..65535, word store | 2 |
| 3 / s16 | signed-input clamp**−32767..+32768**, low-word store | 2 |
| 4 / s32 | raw dword bits | 4 |
| 5 / f32 | raw dword bits; no arithmetic/conversion in this leaf | 4 |

Thus u8 input−1 writes00 and256 writesFF, refuting narrowing/wrap. Width3 is
not the usual signed16 bounds: original MOV EAX,FFFF8001 at26D5C7 and
MOV R9D,8000 at26D5D4 yield−32768→word8001 and+32768/+32769→word8000.
The signed16 view of those word bits is a representation prediction, not an
executed PUSHV read. Intent of unusual limits is UNKNOWN; do not fix the original
binary or silently normalize the policy in a reconstruction.

Original22 cases retained. First reducer assumed conventional signed16 bounds
and FAILED before any result; old checker/failure preserved. Three additive
original width3 boundaries−32767/−32766/+32769 used the unchanged AST-selected
runner, without replaying22. Its first setup omitted struct, failed during record
initialization before original execution/result; old helper/failure retained and
dependency supplied. Corrected actual raw-default checks all25 observations.

Controls: private CMOVG->CMOVL at26D577 makes width0 input256 write00 instead
of originalFF, explicit non-shipping intervention. Original width5 copies NaN
payload7FC00000 as four bytes (no float operation). Width6 reaches original JA/
RET with zero writes, positive width5 write observer retained. Width3 index−1
writes base−2 inside the disposable guard: scaling alone, no new index clamp here.
A supplied lower28-bit change leaves width0 effect unchanged, not proof of a
valid descriptor/caller in gameplay. Narrow-wrap, standard-s16, no-write-detector
and clamp-opcode checker faults must reject. Never accept an incomplete/zero run.

The verified closed source graph has NO call/free/release. It stores resolved
values, contradicting canonical verb page's phrase “0026D530 releases the block.”
Required OPUS/FABLE/DATA consumers: represent exact per-width write policy,
preserve width3 asymmetric input bounds/word bits, correct release wording,
propagate affected native store contracts/prose/tests without changing original
bytes. Existing canonical storage classes/kind conversions are separate: this
does not execute00267E60 or its coercion/notification/callback effects.

Limits: injected already-resolved ABI/state; no initialized native bank values,
caller-guaranteed input/index range, normal reachability/scheduling/lifetime,
global malformed or alias safety. No hardware/MXCSR flag parity claim; emulator
and provider identities explicit. No game/PC control/save/config/reference/peer
writes. S19 allowance spent/unapproved extension persists. Independent acceptance
and canonical incorporation pending; fullL1+L2 NOT_MET.

Reproduce capture.py retained default (no recapture), check.py and the fault flags
in regression-controls.json. Do not rerun extra-s16-boundary.py on a published
package: it intentionally refuses replacing its existing additive raw evidence.
