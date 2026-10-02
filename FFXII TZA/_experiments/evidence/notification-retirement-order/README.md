# Completion notification precedes request-entry reclamation

Question: does a finishing request make its own slot free before posting an end
notification? H1 says early reclamation protects a full same-actor pool. H2 says
notification allocation happens first. Method A is sufficient: eight complete
retained shipping bodies, exact EXE/body identities, local CFG and memory roles.
No game, native harness or emulator is used. Earlier SECTION12 exhausted
different-actor experiments are retained context, not rerun or counted here.

The original head-entry removal calls the link-unhook at `003DB346`, which clears
entry state and adjusts entry/neighbour links. With valid, disjoint actor/pool
storage it does not put the slot on the actor's free list. Eligible end
notification is attempted at `003DB37D` → `003DC122`. Re-insertion into the free
list occurs later at `003DB3F0`, followed by head publication at `003DB3F9`.
All normal local paths after the post pass that later head store.

The notification descriptor selects function **0**. An empty function table
therefore refuses with allocation result 3 before the capacity check. With
function 0 admitted, a free head of FF returns 2 without helper calls or own
object writes. A non-FF head reaches insertion helpers; this packet does not
establish their success or effects.

For a valid head mode-3 entry resolving its requester to the **same actor**, a
full free list and flags byte 0/1, the notification fails before the finished
entry becomes allocatable. Those flags skip the separate reference helper. The
removal's final EAX is the original entry flags' low bit, independent of the
notification result: conditional flags 1 returns 1 despite the lost notification.
This is a bounded source implication, not proof that play reaches such a state.
Flags ≥2 additionally invoke `00263050`, whose effects remain outside this proof.

An observer must identify requester, free head and allocation call origin at the
attempt. Spare capacity observed **after** removal does not establish capacity
at notification time. Shipped full-pool reachability, actor lifetime/reuse,
concurrent mutation and cancel/re-entry scheduling remain open.

Reproduce from the repository venv with `prove.py` and a fresh result name.
`capture.py` actually imports and uses the reviewed shared access-role adapter,
including memory-store, LEA and read-modify-write controls. `control.py` has three
actual failed/missing-prerequisite CLI refusals and five labelled static source
countermodels. These are producer checks, not independent project acceptance.

The first producer stopped before semantic output because its expected LEA was
transcribed incorrectly. The original driver/failed receipt remain immutable in
history. The corrected assertion and focused wrong-LEA regression are retained.
All tools are finite and read-only outside this owned evidence workspace; no
game, PC-control, saves, settings, reference binaries or peer work were changed.

FABLE consumes the order and observer qualification on the actor-request page;
OPUS consumes the pool/post/return contract; SPEC independently reviews exact
source identity, valid-layout premises, invocation checks and conclusions.
