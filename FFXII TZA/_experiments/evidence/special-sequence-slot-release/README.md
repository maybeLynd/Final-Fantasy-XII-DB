# Prepared slot release and special-sequence ownership

Shipping EXE73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8;
Method A exact original source/CFG/caller order. No original machine-code
execution, forced calls, game session or natural stale-owner observation.

For a player: this asks what the code guarantees when a prepared cinematic
slot is released. A slot being freed and the whole cinematic sequence ending
are separate outcomes. This is a code finding, not a reproduced gameplay bug.

Complete functions:30C970224B (slotrelease),30657087B (global release),
31B7E042B (ownerresolver). Actual shared reviewed access-role adapter is called
and checked in the capture path. Source, annotation, tool and checked terminal
capture status must all agree before proof.

With a valid poolslot0..31 and track+18 nonzero, the caller resolves handle+20
using31B7E0, copies RAX straight into RCX and calls306570. There is no NULL
check on that transfer.31B7E0 returns0 when02089340bit4 is clear or lookup3588B0
returnsNULL. Its tail263E30 native effects are not established by a stub.

306570 allows the resource query when requested unit isNULL, global owner is
NULL, OR they are equal. A nonnull foreign unit is rejected only when global
owner is also nonnull. Predicate2671F0(3) must return0 for the LOCAL clear:
flags022C2158 low2 bits cleared, QWORD022C215C cleared (kind AND adjacent
stateDWORD022C2160), QWORDowner022C2168 cleared, then238A60 and tail332190(3).
A nonzero predicate returns without these LOCAL stores. This does not prove
that the predicate/transitive callees themselves never touch those globals.

After306570 returns normally,30C970 proceeds directly to slotreset regardless
of its branch. There is no success-result test: low5slotflags clear, action1C
becomesFFFF, links clear, handles reset, trackstates10/14/18 and owner20 clear.
A failed owner resolution can therefore be forwarded as a wildcard request;
and a skipped global-clear path is not a skipped slot reset. Neither result
proves naturally reached invalid handles or pool reuse while a sequence lives.

Twelve branch-partition countermodels are mathematical labels, not tests of
nativecallees or gameplay. The actual producer controls are three CLI runs:
failed capture, missing source and a coherent same-size RCX=RAX -> RCX=RBX
mutation. Each must refuse for the named cause with no result. Original-source
positive and primarybyte comparison prevent self-consistent fixtures from
becoming proof of FF12 behavior.

Premises: validslot/links/privateframe, ordinaryx64ABI, normal external returns,
and slot/global memory noninterference for the stated observations. Resource
release/calleepredicate effects, object reuse/handle lifetime/scheduling and
natural combined-state reachability remain open. No atomicity, portableruntime
pointer, integratedparity or wholeOV21/42 closure follows.

Canonical consumers: OPUS qualify ownership/cleanup contracts; FABLE qualify
mode/command seam global-release summaries and preserve natural-lifetime gaps.
Independent SPEC acceptance is pending. Existing UQ109/112 and localguard
facts are reused, not a new census or independent audit claimed as ours.

Reproduce prove.py from repo root with a fresh result name. Negative cases
retain actual raw stdout/stderr/receipts and differing inputs; unchanged files
are hash-bound references to the base input set in input-identities.json.
Reproduce controls in a disposable copy of baseinputs/positive evidence,
omitting generated controls and control-result/status outputs. Never alter
published inputs. All own children terminal; no PC/game/save/config/reference
or peer process changes, so no state restoration intervention was needed.
