# Phyre texture admission, physical copy and pointer-key insertion

Method A STATIC_ONLY, producer checked; independent review and canonical use
pending. The original executable is SHA256
73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base120000. No shipping function, native/emulated harness or game was executed.

Question: which representation and effects connect 62C360 / 62EB90 to the
identified Texture2DD3D11Element async object? Does that entry settle the drain's
pendingCount+38? Competing explanations were direct updater/counter execution
versus storage admission with scheduling/counter changes elsewhere.

New source-linked facts: with object+B4 bit10000 clear, 62C360 copies exactly
200 bytes, source R8+0..C7 to object+C0..187, as twelve sequential16-byte
load/store pairs then one8-byte pair. It does not stage the whole input before
writing; no general overlapping-buffer guarantee follows. Its unsigned element
index guard returns3 on failure, and a null element resource returns15h.

The embedded element+40 data receives the texture pointer at+8 and index at+10.
Raw RTTI/slot0 binds D54348 to621FF0, which loads those fields and tails622010.
The adjacent qword at table+8 is another RTTI locator, not a second inferred
function slot. Original622010 invokes graphics-context vslot180 at most12 times
under ABI-preserving normal returns, and on the later single-element arm calls
584730 and nulls selected element+28. Native effects and actual dispatch remain
open. Existing independently accepted OPUS constructor and T5 argument facts are
corroboration/premises, not new discoveries or experiments here:
513baa66d (ptexture2dd3d11) and773c08600 (d3d11-element-release), accepted in
SWE2-AUDIT-SEM reviews. We did not rerun those reviewers' controls/censuses.

62EB90 passes context+38*zeroextend32(bank), a result local and the saved pointer
to199DB0. That original entry compares/copies the pointer as a node key. With a
valid finite ordered-tree/sentinel invariant it performs keyed insertion,
including an existing-key refusal, rather than FIFO callback-pair append. Its
two insertion branches request28-byte nodes via allocator vslot10, link through
16D840, increment container+28 and write result+8=1. The non-insertion arm writes
result+8=0. A115-state finite event abstraction checks insertion order across
all original normal branches; it is an invariant proof, not115 executed tests.
The complete16D720 and16D840 helpers have no calls. Thus this local closure never
directly invokes the async object as callback; opaque allocator effects remain
excluded. It does not establish the scheduler's actual execution/consumption.

Container+28 is not the texture-element+38 wait field under the ordinary
distinct-allocation premise. The complete writer closure for element+38 stays
OPEN. The physical wrapper loads its R9D from byte[entryRSP+18]; that is not the
incomingR9D.199DB0 locally overwrites/tests its own key/direction values. The
empty-root arm may still carry incomingR9 to its opaque allocator call, so this
does not prove an unused fourth-argument ABI or an uninitialized-state defect.

Reproduce the two reductions with the existing analysis Python and fresh outputs:

    python <packet>/prove-texture-async-admission-boundary.py <fresh.json>
    python <packet>/prove-texture-queue-tree-boundary.py <another-fresh.json>

Readers require the shared reviewed access-role adapter and re-decode all
shipping source bytes before their CFG/dataflow checks. The actual capture path
uses it, with memory-store, LEA and RMW controls. Raw code hashes, unwind roots,
helper padding, physical RTTI and source/result/driver pins are retained.
The ten final actual CLI refusal controls reuse the two completed positives;
they are synthetic source mutations, not native/live observations. Four earlier
admission refusals are reused by receipt, two repaired/new cases are run in02.
The malformed original ModRM mutation failed its intended gate check; it is
preserved in01 and supplies no PASS.02 fixes the fixture to a consistent XMM
source-register change and reaches the original-body pin. No producer semantic
conclusion relied on the failed mutation. The first admission result's phrase
"626C-style naming is not used" is a stray editorial phrase with no evidence
claim; read its following exact62C360 proposition. That original result remains
immutable. This README is the additive qualification, not a changed sample.

Open: natural initialized object/container identities, allocator/interface
success and side effects, real caller/thread/timing, full counter writers,
queue consumption/removal, cancellation/drain, lifetime/reuse, and meaning of
the200-byte physical tail. The ordinary title17ECC0 object is not assigned this
Phyre class merely because its cleanup reaches similar code. Constructors and
fixtures do not establish live initialization, nor do source pins imply semantic
acceptance. WholeOV29/other runtime rows and the full L1+L2 goal remain open.

Consumers: OPUS owns exact layout/ABI/container versus element-count facts;
FABLE owns scheduling/lifetime prose. Existing accepted field facts are reused,
and only these new extents, local insert/refuse/order and limits need review.
Next cheapest discriminator: original consumer/removal binding and complete
element+38 writer dataflow, then a bounded original-code effect if static proof
cannot discriminate. Actual process observation is reserved for unproved natural
identity/order premises. No interactive setup is justified by these sources.

Cleanup: only file reads and bounded synchronous analysis. All known children
terminated. No PC controls, game, instrumentation, saves/config/reference binary
or unrelated process writes. EXP127 stays invalid; parked menu budget remains
spent/unapproved. Existing byte-preserving *-text policy was applied before the
manifest so raw CRLF inputs cannot silently change during Git publication.
