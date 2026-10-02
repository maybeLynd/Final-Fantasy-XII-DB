# Render-slot self-index, cursor and publication preconditions

Method A answers the next rig-caller question from original initialization and
allocation code. A successful local slot allocation establishes a self-index
under explicit cursor/native-state premises. A live-count cap alone does not
establish those premises or guarantee termination of the next-free scan.

For the player: adding a visible character involves writing its slot index,
marking that slot active, then counting it in the pool. Those are separate steps.
Reconstruction must keep that bookkeeping coherent when creating and releasing
characters. No gameplay bug, hang or actual transient observation is asserted.

## Question, competing explanations and method

H1: livecount<160 alone bounds every access and establishes a healthy owner.
H2: starting cursor bounds, stable occupancy and lifecycle/metadata coherence are
additional requirements; ID, flags and count have separate publication boundaries.

The source directly distinguishes these propositions, so no original-code harness
or game session is required. Native fill/resource effects, natural scheduling and
actual lifetime are different questions. The accepted pool count is reused; it
is not re-censused or counted as a new result. Existing attributed +0 writes were
preparation, not complete alias/bulk-fill/all-writer proof.

Reference EXE SHA256:
73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8.
Complete shipping bodies: 41F730..41FBE8 (1208 bytes), 420480..420851 (977),
4269A0..426C85 (741), 4279B0..427AF9 (329), total3255 bytes.

## Exact initialization and allocation boundaries

41F730 requests a zero-fill of740h bytes and directly writes WORD0=FFFF.
4269A0 calls this per-record clear160 times at740h stride. It then stores QWORD0
at tail48808, jointly seeding DWORD cursor48808 and DWORD livecount4880C.
These are source calls/stores; the package does not sample initialized live state
or infer absence of opaque callee effects from a missing direct write.

After name lookup4278E0 returnsFFFF, allocator4279B0 checks signed livecount<160.
It loads starting cursor with MOVSXD at4279FA and forms
record=base+cursor*740h. There is no independent cursor-domain comparison before
passing that pointer to the clear41F730. Given cursor0..159, a valid pool/private
frame and normal clear return, its WORD[record]=SI store at427A4D writes the
physical row index exactly.

The allocator then calls420480(record,...). That body first ORs record284 with
2010F9h before any call in the body. Under normal return the allocator raises
record290 bit0, increments livecount at427A7F, chooses the next cursor and returns
the record. The self-index store precedes the active-flag boundary, which precedes
the count increment. This does not prove atomicity, natural observation of an
intermediate phase or absence of reentrancy/interference. The metadata body's
supplied direct writes do not clear0 or284; indirect effects remain separate.

The factory can forward owner0 to rig68, and4215A0 can forward it to rig6C. These
original stores help establish a freshly allocated self-index under the premises;
they do not certify that an arbitrary later caller still has a valid active owner.

## Conditional circular-scan invariant and falsifiers

For a starting cursor0..159, each scan iteration increments byone and wraps160
to0. Every index stays0..159; a complete cycle visits all160 exactly once.
Given stable readable flags and at leastone zero284, the scan terminates within
160 visits. No count cap alone proves that a zero284 exists.

Two fixed-width source countermodels distinguish the missing premises:

- livecount0 passes the count cap even with starting cursor-1 or160; its first
  clear pointer is outside the declared160-row domain. No actual fault or invalid
  natural cursor is observed.
- livecount0 with all160 flags nonzero after metadata enters the next-free scan
  after incrementing count to1. Under stable flags, the mathematical loop cycles
  without a zero. This is not an executed hang or a claim that shipping code can
  naturally reach the inconsistent snapshot.

The160 cycle calculations are mathematical controls, not160 machine-code or
live-game tests. Complete all-writer/list/count/occupancy coherence and native
caller/lifecycle guarantees remain open.

## Instrument validation and the retained failure

The actual capture uses the shared reviewed access-role adapter. Current producer
checks original identity/bytes, four complete local CFGs, exact original field
operations/widths/roles, nonvolatile carriers, publication dominance, the initial
cursor-check boundary and the fixed160 representation/cycle invariant.
Five actual disposable CLI refusals test failed capture, failed required
inspection despite an existing apparent output, incomplete wrapper, missing
source and a coherent self-index-store register mutation. They check the actual
producer invocation with prerequisite gates before output, not helper existence.

The first feasibility script was unfortunately named inspect.py. Capstone's
stdlib inspect import loaded it recursively; it wrote an apparent inspection
output and printed success, but the outer process exited1. That output is
INVALID_PRODUCER_INVOCATION, preserved with raw receipts and an explicit
disposition. No consumer or semantic claim relied on it. The corrected actual
path inspect-slot-source.py guards against that local filename before dependencies.
Inspect02 is a valid four-body source feasibility run. A separate actual shadow
CLI regression reproduces the input condition and requires nonzero/diagnostic/no
result plus the checked positive. Producer01 and the five refusal controls are
valid; producer checks are distinct from independent project acceptance.

## Consumers, limits and cleanup

OPUS/FABLE should qualify slot/self-index/cursor and rig caller contracts with
these input domains and publication boundaries. Keep successful local allocation
separate from universal safe later use, lifetime, ownership/reuse and natural
scheduling. The new package does not repeat the accepted160-slot capacity result.

No original machine code was executed; no emulator, stubs, live process, native
call or observation was involved. Native fill/resource/opaque effects, actual
all-writer coherence and scheduling remain open. Binary, driver, input, result
and receipts are preserved; published inputs remain immutable. No PC/game/native
harness/instrument/save/config/reference/peer file or process changed. All own
scientific children are terminal. EXP127 stays invalid, K14 closed, and the parked
menu allowance spent/unapproved. Independent review/canonical consumption remain
required; no wholeOV row or fullL1+L2 completion is claimed.
