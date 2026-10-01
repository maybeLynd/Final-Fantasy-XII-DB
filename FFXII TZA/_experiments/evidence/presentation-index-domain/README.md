# Original special-sequence selector: exact table precondition

QUESTION: does `00309230` validate the thirteen-type table domain, and what
does the original instruction order establish outside that domain? Method A,
STATIC_ONLY. OPUS consumes exact type/ABI/selector preconditions; FABLE consumes
the remaining OV42/OV21 admission model. Natural reachability remains open.

The full 199-byte original body and `00306BD0` prefix through the actual
`00306C56` request call match EXE
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
Reviewed shared access-role adapter is actually used and independently
re-decoded; store/LEA/RMW capture controls passed. The retained eight direct
caller prefixes are identity-checked inputs, not a new census or complete
indirect-call/caller-value proof. Original constants and their previously
canonical progression are corroborated, not newly discovered/tested data.

## Established source behavior

`003092C0` compares the full entry RDX (saved RBX) with **zero-extended ECX**.
Null global context or null first `0020E600` return selects comparison value0.
Otherwise the function rereads context and calls `0020E600` again, computing
`(low32(second return) + u16(context+8)*0x113) modulo2^32`. The first and second
returns/context reads are not assumed identical. Equal comparison therefore
requires RBX's upper32 bits zero; this is original-code arithmetic, not an
observed runtime pointer or loaded-address guarantee.

Unequal comparison returns zero-extended `WORD[entryRDX+0x24]`, domain0..65535
under an accessible-read premise. It does not consult or validate the type band.
Equal comparison reads a type byte through `entryRCX+0x698`, then executes
`MOVZX EAX,byte; SUB EAX,0x1B; CDQE; MOV EAX,[RSP+RAX*4+0x20]`.
There is **no local type bound guard**. Address stays within the thirteen
initialized DWORDs iff type27..39. Their values42..78 step3 were already known.

Exhaustive algebraic partition of all256 byte inputs, relative to post-prologue
RSP (offsets hexadecimal):

| Type byte | Read offset | Original-frame provenance |
|---|---|---|
| 0..26 | -4C..1C | Outside table, preceding frame/callee-controlled bytes |
| 27..39 | 20..50 | The initialized table |
| 40 | 54 | Gap with no local initializer |
| 41..42 | 58..5C | Low/high words of stored stack cookie |
| 43..44 | 60..64 | Low/high words of saved entry RDI |
| 45..46 | 68..6C | Low/high words of caller return address |
| 47..48 | 70..74 | Low/high words of saved entry RBX |
| 49..255 | 78..3B0 | Caller bytes beyond the local frame |

These are predicted addresses/provenance under ordinary ABI/private frame and
noninterference, **not observed values, executed bad inputs or faults**. No
universal claim that preceding/caller bytes are uninitialized. The stack-cookie
check follows both branches; under normal return it checks the cookie, not the
selector's type validity. Foreign/native callee effects are a stated premise.

The new original caller prefix sets manager3, calls `00309230` at`00306C4D`,
then passes returned EAX as EDX to `0032FC30` at`00306C56` without an intervening
index check. This is a source transfer, not normal gameplay reaching it. The
prefix is not a complete caller CFG. `0032FC30` requests a manager resource
set; no reward/damage/pixel consequence is established.

## Controls and reproduction

`result-01.json` is the successful producer proof: one full CFG,56 source pins,
256 algebraic address cases, three declared external call sites. These are
static deductions, not native/live experiment counts. Terminal capture01 and
proof01 receipts preserve driver/interpreter hashes, argv, exit and streams.
`proof-controls-02/result.json` and `control-03.*` retain four actual proof CLI
refusals: failed capture, missing source, zero bodies, coherent same-size/count
`SUB EAX,1B -> SUB EAX,1A` mutation rejected against shipping bytes. Every
refusal requires its exact diagnostic, empty stdout and absent result, with
the original positive proof required. No invalid/zero-case run is a PASS.

`control-01.*` / `proof-controls-01/` are **INVALID incomplete**: the verdict
and exit were indented inside the loop and only the first case ran. Original
controller preimage is retained. A failed shell edit parsed no Python statements;
the mistaken control02 retry only refused the already-existing output directory.
Neither adds semantic/control credit. The producer fix moves finalization after
the loop; four-case gate remains required. Only the affected controller was
rerun; original source/proof inputs remain unchanged.

From repository root use project Python with
`prove.py FRESH_OUTPUT_JSON --src PUBLISHED_PACKET_DIRECTORY`.
Published `dependencies/` resolves the same reviewed adapter/CFG; original EXE
is still hash-checked. Original capture/retained discovery drivers preserve how
inputs were obtained, but the proof consumes immutable source rather than
recapturing the eight callers. A reviewer should use fresh output/control space,
never overwrite these records. Producer validity is not independent acceptance.

## Limits and next discriminator

The required next fact is the **natural equal-branch type/context admission**,
or a source invariant proving it. This packet cannot supply initialized actor
type, stable context/resolver returns, pointer relocation/lifetime, interference,
or any naturally produced out-of-band value. It does not close whole OV42/21,
establish rejection/leak/crash, or duplicate shipped action-table census. The
unequal WORD branch must retain its separate authored-value/producer bounds.
Next inspect actual caller/type initialization or named peer-consumer evidence;
do not rerun these settled256 cases or start gameplay solely for a historical
RT label. Menu allowance remains spent and its extension unapproved.

No game/PC/control/instrument/save/config/reference/peer-process changes. All
our finite capture/proof/control helpers terminated; restoration is vacuous
because no runtime state was touched. Goal ACTIVE/NOT_MET. Independent SPEC
review and OPUS/FABLE qualified incorporation still required.
