# Equal numeric cache key retains the existing payload — conditional source proof

Exact FF12 image73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8.
Method A STATIC_ONLY; SOL in ASTRA producer. Independent SPEC review and FABLE
semantic/OPUS structural consumption pending. This is a new insertion/hit
discriminator after preprocessing4554a365, not another archive census or live run.

001D6A20 forwards its caller's 32-bit numeric key unchanged to0020B680. It
does not recompute a key from a filename. Given a valid finite unsigned-key
ordered tree and an existing equal numeric key,0020B680 takes its hit branch:
it sends the incoming *buffer pointer to0020B0F0, then passes the existing
record's data pointer and length to0020C300. The miss branch's new payload
assignment is not reached. The key comparison has no filename tie-breaker.
The ordered-tree argument applies to all unsigned32 keys under that invariant;
it does not establish the natural tree's initialization or key population.

0020B0F0 calls statically declared _msize, subtracts its return frommanager+10
using LOCK XADD, then tailcalls statically declared free. Static PE imports
are not proof of loaded CRT targets or native allocator effects. Valid distinct
incoming allocation and ordinary ABI/normal returns are explicit premises.
Aliasing the incoming buffer with the retained payload is outside this proof.

0020C300 keeps the supplied existing pointer and length in nonvolatile registers,
and supplies them to00217A60 after a16-byte allocation. The allocation-null path
returns0. This closes the original call argument/dataflow; actual constructor
effects or durable lifetime do not follow from those arguments. Existing mode
and requested mode are distinct stack arguments; counter, reference and tag/mode
changes are possible. Reuse does not mean absence of side effects.

Five complete local CFGs and63 original operation assertions are tied to exact
body/source hashes, checked upstream exit/terminal/stdout/stderr and actual
reviewed store/LEA/RMW adapter invocation. Four real CLI controls must refuse
upstream failure, coherent truncated body, coherent changed key MOV and false
release import. No original instructions were executed; assertions are source
checks, not63 native tests. The tree proof is inductive, not an absence sample.

The actual invocation wrapper initially rejected --out before launching the
reducer. That failed command/preimage is retained, no result was accepted, and
REMAINDER now forwards the real argument tokens. Positive02 validates that
concrete path. No hidden missing-result success or reset of failed evidence.

Unresolved: all actual insertion callers/key domains, natural same-key
different-file collisions, cache membership/eviction/reachability, native
constructor/allocator/loaded CRT effects and lifetime, malformed state safety,
runtime-built kind-FF paths, and whole OV33 E2. The six missing indexed rows
are not proved cache hits. Source-only insertion semantics narrow that question;
they do not establish the archive namespace or natural issue path.

Replay into a fresh owned folder using the retained reducer and input/control
hashes. Control deltas inherit pinned baseline inputs, with all changed inputs,
full stdout/stderr and receipts preserved. Never write into published results.
No game/PC/instrument/save/config/reference/peer process was changed. Finite
helpers terminate. Goal ACTIVE/NOT_MET; parked menu allowance remains spent and
unapproved, EXP127 invalid, K14 independently closed. Next: establish specific
original insertion caller/key source domains before a bounded namespace proof.
