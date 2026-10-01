# First cleanup delegate and selected-field boundary

SOL in ASTRA, 2026-09-30. Method A STATIC_ONLY. Producer checked, independent
review and canonical incorporation pending. No native/emulated/game execution.

The exact question is whether62B100 repairs a zero-count state before the
previous cleanup loop, and whether623DF0 returns a record base. Original code
answers the local question; actual valid initialization remains a separate gap.

Original image SHA25673461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base120000. The112B62B100 entry-normal CFG closes within its pdata extent;
the56B623DF0 leaf closes at both623E0D and623E27. Its first RET alone omits the
n<=1 branch. Source/gate receipts pin image, tool, shared roles and annotations.

Let n=DWORD[object+30]&7FFFFFFF and k=zeroextend32(EDX). The selector returns
B+58*k+38 modulo2^64, where B is0 for n0, object+38 for n1, or pointer[object+38]
for n>1. Thus it returns a record's+38 field. The count-one/index-zero result is
object+70; count-zero/index-zero is absolute38, not NULL. Bit31 is ignored by
this selector; its meaning elsewhere remains unassigned. There is no local
index bounds check or memory write. Caller premises must provide valid indices.

62B100 starts index0 with bound max(1,n), calls the selector and reads its DWORD
before invoking5CCB80. With count remaining zero between the two initial count
reads, the first access is absolute38. It neither normalizes nor skips the state
before that read. This is a conditional required state precondition; no actual
game crash, natural zero-count reachability or native constructor is established.

A signed-positive selected DWORD makes it pass ECX1 to5CCB80, then reselect/read
the field and repeat while signed-positive. The service receives no selected
pointer/object in RCX. Its purpose, effects and progress are unknown. The outer
loop reloads count after each element; fixed indices0..n-1 require stable valid
count/storage and termination of that service. Dynamic changes are outside that
fixed-extent proof.

The positive source reduction is reused once. Actual reader controls refuse a
first-RET-only source, false selected offset and wrong root metadata with nonzero
exit/no result. Complete byte/operation/memory agreement runs in the reader before
CFG analysis, using the reviewed shared adapter. These checks are producer
controls, not independent acceptance or gameplay samples.

Reproduce with prove-title-cleanup-count-selector.py and a fresh result path in
the same repository with Capstone5.0.7 and reviewed reg_tracking.py SHA256
5fcc64842c96d99c3ef9df4f7e3adc528dfad0dfd44b2f6bb5bf43beda092a38. Inputs/results
and refusal fixtures are included. Capturing shipping bytes requires the pinned
private reference EXE, which is not redistributed. The original capture-driver
snapshot preserves its recorded placement and invocation; reduced retained
evidence can be checked without executing FF12.

FABLE owns cleanup/count-state semantics; OPUS owns return-offset, index and field
ABI contracts. This companion narrows the existing guard question; it does not
reopen or duplicate its prior samples/review. Independent acceptance must bind
these final code/source/control identities. Incorporation must retain constructor,
caller/storage, native-service, lifetime, cancellation and idempotence gaps.

The next discriminator is original constructor/count-writer/caller evidence:
prove count>=1 whenever cleanup reaches62B100, or identify a valid zero-state skip.
Static invariants are preferable to a forced native call or hours without hits.
No parked menu attempt, EXP127 replay or setup extension is permitted.

All synchronous helpers terminal; no PC/game/input/instrument/save/config/
reference/peer mutations. Whole runtime rows closed0, cumulative formerly-runtime
request retired1. The full L1+L2/M0-M5 goal remains ACTIVE/NOT_MET.
