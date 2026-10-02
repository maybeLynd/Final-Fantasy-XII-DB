# A cancellation can attempt an end notification without RET

Question: does an end-notification attempt certify that the target executed RET?
H1 says only normal RET posts. H2 says the native cancel path can remove a
nonzero-state request and invoke the same end-notification helper. Method A is
sufficient: exact original native carriers and complete recycler control flow,
composed with retained, published original removal/post bytes. No game or native
harness is required. Successful receipt delivery and natural interleaving remain
separate questions.

`00352980` passes its popped channel and mode 4 to `003DB420`. `00353660` passes
first-pop + 1 as the lower channel bound and resolves the second pop to an actor,
then uses the same mode 4. Both tail into `003DB6E0`; that scheduler's effects are
outside this packet.

Mode 4 normalises the internal state filter to zero. The recycler scans channels
downward from `actor+88 - 1` to `max(0, signed input)`, gated by its initial
active-bit snapshot. It selects the first nonzero entry state. States 1 and 2
therefore qualify alongside state 3. It calls removal **once per selected
channel**, then decrements the channel; it does not clear every entry from that
channel in this invocation.

For a valid head entry with mode-3 notification descriptor and a valid non-8000
requester, retained `003DB2A0` invokes `003DC0D0` independently of the incoming
entry run state. The scoped mode-4 cancellation path can attempt the end
notification without calling the target's bytecode interpreter. This refutes
an unconditional “only RET produces this completion attempt” specification. It
does not prove that an authored scene cancels such a request or that the
notification was admitted, delivered or consumed.

The recycler returns EAX 1 on all normal paths, including NULL actor, empty
range and no selected entry. Reverse reaching-definition checks establish the
three return definitions; a constant somewhere in the body is insufficient.
Its return does not certify removal or notification success.

Scope requires stable, valid, disjoint actor/entry/frame storage and normal ABI
and returns. The exact no-opaque-helper composition uses entry flags 0/1. Larger
flags cross `00263050`; its effects are not established here. Natural
cancellation, same-key re-entry, ownership/reuse and frame timing remain open.

Extent lesson: the first `.pdata` entry for `003DB420` covers only 28 bytes.
Branches leave that fragment. The complete local body is 304 bytes, with the
removal at `003DB506` and NULL return at `003DB545`. The producer requires the
complete original range; a focused control passes the truncated fragment to
the actual CFG checker and requires refusal.

`capture.py` uses the reviewed shared access-role adapter on its actual path.
`prove.py` requires successful current capture and retained parent receipts,
original image/byte/role identity and complete control flow. `control.py` checks
four real disposable CLI refusals and six labelled static source/CFG mutations.
The initial Python syntax failure produced no semantic output; its driver and
receipts remain immutable. It was corrected before any valid result, and the
drafted return reasoning was strengthened to the actual reverse-definition
proof. These are producer checks; SPEC independent acceptance and FABLE/OPUS
canonical incorporation remain required.

All children finish; no PC/game/native/emulator session, save/configuration,
reference binary or peer file was changed.
