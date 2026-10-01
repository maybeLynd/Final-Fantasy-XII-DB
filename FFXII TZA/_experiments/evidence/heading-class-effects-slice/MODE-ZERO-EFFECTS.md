# CON-172: a source-derived effect slice, not class-stability closure

Method A only. All addresses are shipping-image VAs, image base `0x120000`,
EXE SHA256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
No instruction was executed as a native FF12 experiment in this package. Python
ran read-only capture/decoding/checking. Catalogue-only/no-unwind extents retain
`UNPROVED_CATALOGUE_ONLY`; a complete straight-line snippet is not silently
promoted into an image-wide absence or lifetime proof.

The question remains whether `002E45E0` can change the current actor's kind before
the frame driver's later delta gate. The original caller's class gate and the
963-byte intervening body do not themselves settle that. Three competing models
remain: preservation under established initialized layout/ABI conditions; a native
write that changes it; or unproved aliases/delegated effects preventing closure.

## Caller discriminator and mode-zero path

`002E4964 xor edx,edx`, `002E4966 mov rcx,rsi`, `002E4969 call 0026C120`
supplies mode **zero**. The relevant class-3 arm is `0026C244`, not modes 2/3/4.
It writes the new mode into the active steering subrecord's `+0x28`, saving the
previous mode. If subrecord `+0x65` is nonzero it calls `002EBE50(actor,0,0)` and
`002E8EE0(actor)`; it then calls `002E6300(actor,ctx,old_mode)`.

`002EBE50` with zero clears context `+0xB4/+0x224`, writes subrecord `+0x63`,
then invokes `002EC3F0` and `002E8EE0`. Consequently an open teardown gate can
reach `002E8EE0` twice; no idempotence, scheduling or visible effect follows just
from that source fact. `002E6300` has a conditional **JS tail** into `00265510`,
which reads the class gate and active subrecord `+0x64`. No CALL-count argument
may erase the tail. The supplied old mode determines whether it is selected.

`002EC3F0` stages one of six head-look paths based on profile flags. Their existing
FABLE/EC7 mechanism is consumed through the canonical staged-look page. This
package does not re-execute those helpers or award their complete native closure.

## Object-state writes: exact sequence, conditional region identity

`002E8EE0` resolves the secondary-context word id through bank `022C6F28` with
stride `0x740`, refusing `-1` and zero occupancy. It reaches `003E6BD0` then
`003E6BC0`; each adds `0x580` to the render-record pointer and tail-jumps to
`003E3440` or `003E33E0`, respectively. It also ORs render `+0x290` with `0x800`.

For the flags word at `F`, the original setters read the word **twice**. Let `d0`
and `d1` be those sequential reads, not an assumed atomic snapshot:

* `003E33E0`: `(((uint32(uint16(DX)) << 23) ^ d0) & 0x00800000) ^ d1`, then OR 2.
* `003E3440`: `(((uint32(EDX) << 24) ^ d0) & 0x01000000) ^ d1`, then OR 4.

Only if `d0 == d1` may these be reduced to replacing bit 23/24 with the input low
bit and raising dirty bit 1/2. Neither reduction proves concurrency/atomicity.
The canonical look-command page already describes the stable-input staged roles;
staging is not application by the later controller or player-visible presentation.

For example, the bit-23 store can overlap actor byte `+3` if `F == actor+1`.
That is a conditional address calculation, **not an observed initialized alias**.
Proved aligned/disjoint actor/render allocation would exclude it. Operand
displacement alone supplies neither that proof nor a real counterexample.

## Position path and why it is not a local memcpy

The two `0026AFE0` caller sites pass EBX as stack argument five. The parent zeroes
EBX earlier, but this slice has not proved its preservation through every intervening
native/delegated call; the nonzero branch is not universally pruned.

On its class-3 zero-argument arm, `0026AFE0` calls `002E5DF0`, a wrapper that
calls `002E5C90` with argument five zero. `002E5C90` writes context XYZ, optionally
adds attachment offsets, calls existing predicate `00267260`, passes a stack-local
four-lane candidate to `003DB1B0`, and conditionally copies placed XYZ back via
`003DAE00`. Its cold code **after the first RET** remains part of the validated
340-byte extent. It then calls `002E6000`. Existing predicate replay is not repeated.

`003DB1B0` calls **the placement solver** `00380D30(body+0x30,candidate)` and
returns whether signed body word `+0x82` is nonnegative. A null body returns 1
without that call; this is source branch behavior, not success of an actual placement.
The solver resolves a field/cell, applies the blocked-cell mask, conditionally copies
four candidate lanes, obtains ground height, and calls `003808A0`. Its six original
CALL sites remain explicit. It is not a vector-copy stub and its omitted native
callees are not proven by a composed fixture. The existing movement-body page
describes this mechanism; no duplicate cell-solver experiment is claimed.

`003DAE00` null-tests its source and copies three dwords from source `+0x30/+0x34/
+0x38` to the supplied destination in order. Here the destination is the caller's
stack candidate under a valid ABI frame. No arbitrary overlap-safe copy or valid
source lifetime is inferred.

`002E6000` requires actor, secondary context, non-`-1` first dword and class 3;
secondary `+0x14F` bit 0 suppresses the render write. Otherwise it obtains
`00263910(actor)` (secondary `+0x140`, plus positive zero, then `+0x144` in that
instruction order), adds that to context Y, and calls `003EC3D0(id,X,Y,Z,flag)`.
Do not collapse the float operations into real-number algebra or claim new bit-exact
floating-point execution.

## Render commit and the remaining native dispatch

`003EC3D0` validates signed word id/occupied render row, then applies its own
position and attachment gates. Position equality uses `ucomiss` with explicit JP
branches; unordered input takes the change arm. Depending on the gates it may
zero or update render `+0x140..+0x14C`, clear `+0x284` bit 9, and set other flags.

At `003EC4AF` it reads global **`02B3EC90`**, ORs that with stack argument five,
and skips the commit arm only when the result is zero. Thus argument five zero
alone does **not** establish that the downstream commit is absent. Even equal
position lanes can reach this gate. On the commit arm it ORs `+0x304` with
`0x4000`, zeros `+0x23C`, optionally calls `004288B0(row,-1)`, and tail-jumps
`003B3CA0(row+0x288,30)` when that handle is not `-1`.

The checked `004288B0` snippet raises `+0x290` bit 10; the `-1` arm raises
`+0x284` bit 17 and clears byte `+0x40A`. These existing canonical facts are
corroborated, not new project acceptance.

`003B3CA0` is **not established as audio**. It checks the generation-keyed 64-slot
table at `02EBD480`, requires its slot `+0x10` pointer, saves global context
`02F97340/02F97348`, calls the existing global publisher `0024ED80`, invokes
`003A9490(30)`, and restores the saved context/publisher on normal return.
The publisher's existing EC7/canonical work is consumed, not duplicated. This
normal-return sequence is not exception-safe restoration proof.

`003A9490` walks owners through context `+8`, owner links `+8`, and node chains
at owner `+0x118`/node `+0x30` for owner types `0x67/0x6B/0x71/0x72` at its
`+0x108` object `+0x44`. It calls `0043EE70(node,owner,30)` for each selected node.
It is a real linked-list operation, not an observed scheduling event or an
initialized list/lifetime guarantee.

The 49-byte `0043EE70` snippet is a **tail dispatcher**, not a harmless leaf:

| node byte | native tail |
|---|---|
| `0x67` | `0045FD00` |
| `0x6B` | `00529D40` |
| `0x71` | `0052A8A0` |
| `0x72` | `0052B5D0` |

Other byte values return. These four targets have not been effect-proved by this
slice. This is the concrete next offline discriminator. No genuine initialized
call path, universal class preservation or class-change counterexample is claimed.

## Initialization evidence and remaining obligations

Original `00266AD0` arms can plant context at record `+0x120` and secondary
context at `+0x350`. Under the selected valid arm, non-wrapping live storage and
unchanged binding, direct context scalar stores cannot overlap header byte `+3`.
This is a conditional layout fact. EXP-107 already executed the original binder
against isolated fixtures, including all eight arms; this package does not rerun
or count those external executions as its own. This slice did not capture its
jump-table data again, so arm-to-sequence selection is consumed from that evidence.

Original `00262F90` shows why record-relative initialization is not sufficient as
a universal invariant: after its state checks and `002E4A40`, it copies another
record's `+0xC0/+0xB8` pointers into this record and calls `002681E0` twice.
No global reachability, exclusivity, lifetime or current live binding is established.

Still OPEN: four commit-dispatch tail effects; other relevant steering/native paths;
EBX preservation where fifth-argument pruning depends on it; initialized render/body/
context region identity and stability; native global-publisher delegated effects;
actual scheduling/normal reachability if a claim eventually requires it. Offline
preparation is sufficient for the next four-tail read; no live allowance is consumed.

Canonical incorporation belongs to OPUS/FABLE. This is a narrowed static dependency
map and retained evidence, not independent acceptance or whole L1+L2 completion.
