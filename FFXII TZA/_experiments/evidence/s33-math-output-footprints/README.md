# S33: native math output bounds compose into the history record

SOL in ASTRA; Method A STATIC_ONLY. Producer proof complete; independent
acceptance and OPUS/FABLE consumption pending. No native instruction execution,
FF12 process, simulated input or new matrix/R7 sample.

The prior history packet left the other math-callee outputs open. Could one
write the visual's phase, occupied flags, links or history counters despite the
bounded explicit copy loop? Retained bytes plus bounded native output/argument
analysis settle that conditional question. Gameplay would not prove all output
sites; foreign modules and natural scheduling remain distinct boundaries.

## Identity and reused evidence

Shipping image SHA-256:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`,
preferred base `0x120000`. `source-01.json` retains thirteen new bounded helper
spans. Capture actually uses the reviewed `reg_tracking.op_kind` policy and
its store, LEA and read/modify/write controls. The proof revalidates annotations
and compares every helper and caller byte against the exact hashed image.

The immutable `matrix-buffer-alias` packet supplies original `00202B70` and
`00217060` bytes. Its source/manifests are retained and checked. This proof
re-annotates those bytes through the shared adapter, producing
`retained-matrix-reannotation-01.json`; old records remain unchanged. Its known
vector snapshot, matrix overlap and wrapper-staging findings are reused, with
their private-frame/alias limits. No old arithmetic or overlap campaign rerun.

Caller and conditional counter-domain evidence come from history packet commit
`a02735a448712ad00bed799bafed0ec663bfd3e0`. The parent manifest, source, result,
actual producer, terminal exit/exception and stdout/stderr are retained and
checked. Parent success is a required producer prerequisite; its independent
semantic acceptance remains pending and is not inferred from integrity.

## Native output regions

| Native body / composition | Caller-owned output bound |
|---|---:|
| `00202B10`, `00203080`, retained `00202B70/00217060` | 16 B |
| `00202DE0` through `00216660` | 16 B, including the zero fallback |
| `00270CF0` and its copy branches | 16 B |
| `00270B40` | 16 B |
| `00270A10` through `00270B40` | 16 B; intermediate matrix is private scratch |
| `00203170`, `00270720` | 64 B |
| `00202E90` through tail `00217790` | 64 B |
| `00202F00` through tail `00217880` | 64 B |

The two rotation wrappers restore their own stack frames and **tail-jump** to
the native rotation cores. Wrapper size alone would miss those stores. Both
tails are included and closed; their writes stay within the same matrix.

`00270B40` has indexed quaternion stores. The original float comparisons select
an integer in `0..2`; the original table at `009159D8` is the three signed
DWORDs `(1,2,0)`, bytes `010000000200000000000000`. Two applications select the
other component indices, keeping all indexed output stores within the first
12 bytes; W is at +12. Three finite index cases check the permutation. This is
an address bound, not a reconstructed floating-point result.

The normalized write records preserve all 63 relevant direct store sites.
They distinguish caller outputs from private stack spills. Receiver aliases,
index transfers, tail edges and eighteen actual caller destination assignments
are bound to original instructions. Fifteen native bodies close locally,
including the two retained matrix bodies; 38 transfer assertions are proof
checks, not executed FF12 tests.

## Actual caller composition and its premises

The manager calls `003FC170(visual+0x20,visual)`. For each of four history
channels H, this body passes record destinations to the vec4 addition at H and
quaternion interpolation at H+0x10. Each is 16 bytes. Its other vector,
quaternion and matrix destinations are in valid private stack storage. Combine
those effects with the earlier explicit copy/counter bound for counters in
`0..6`: the composed record writes end at visual `+0x254`, below phase `+0x260`,
flags `+0x272` and links `+0x278/+0x280`.

This theorem requires valid record/argument memory, private frames disjoint
from the record and their own source arguments, ordinary nonvolatile-register
ABI, normal returns, no outside interference and the imported math/cookie
contracts described below. It closes the previously omitted **native output
width** dependency. It does not observe an initialized game object, certify
all process writes or prove the next invocation's timing.

Vector/matrix overlap can affect values even while writes remain within the
declared destination region. The retained wrapper stages its leaf result before
copying it to the caller output; its RAX residue is private stack storage,
not a stable returned caller pointer. No global alias-safety or bit-exact
trajectory claim follows. The actual caller uses the filled destination.

## Explicit foreign boundary

The shipping import declarations identify math thunks for `atan2f`, `cosf`,
`sinf`, `sqrtf`, `acosf`, and direct `_isnan`/`_finite` imports from
`api-ms-win-crt-math-l1-1-0.dll`. The retained `library-boundary-01.json` is a
read-only feasibility note with original thunk/data bytes and declarations;
it is not a loaded-module capture or a separately credited experiment. The
decisive quaternion index table is reread from the exact image by the proof.

The normal math contract does not modify FF12 records, and the cookie check
returns normally on its valid-cookie path. These are **declared boundary
premises**, not effects established by a stub or by this packet's native tests.
No loaded DLL identity or effects were observed. If those contracts or ABI fail,
the wider composition does not apply. Preserve that limit instead of treating
import names as empirical execution.

## Actual invocation and failure controls

`proof-01.status.json` reports terminal exit 0, no exception and checked driver
identity; the raw stdout/stderr and result are immutable. Before downstream
results, the actual path requires successful capture, nonempty source, retained
member identity and the parent's successful terminal proof status. It validates
shared roles, closes helper/tail CFGs, bounds stores, verifies exact image bytes
and checks the original index table.

Five actual proof-CLI controls require that valid positive and refuse:

- failed capture status;
- missing source;
- zero source bodies;
- missing required history-proof status;
- a same-count original-code change: one ADDSS becomes MULSS with matching
  updated disassembly, memory roles and body hash.

The last control passes the decode/role and footprint checks but fails exact
shipping-byte identity. Every control has its specific diagnostic, terminal
nonzero exit, empty stdout and no result. Inherited input hashes and changed or
missing members make the controls reproducible without duplicating unchanged
files in the publication. Missing status and valid empty output are distinct.

Run `prove.py` from the repository root with a fresh output file and `--src`
pointing to the packet. The exact reference image, declared Python/Capstone
dependencies, included helpers and pinned repository adapter are required.
The derived reannotation also requires a fresh output directory. Never overwrite
published inputs/results. Capture retains its original owned-parent invocation
and was not repeated during sealing.

## Required consumers and remaining questions

OPUS: after independent agreement, add exact native output widths, tail
composition, caller destinations and required record/stack/library premises to
the existing visual-history contract. FABLE: refine the native history effects
while keeping natural initialization, real cadence, presentation and lifetime
gaps explicit. Existing consumer tasks own incorporation; no peer page edited.

Natural drop -> visual creation -> possible zero handle -> actual pool tick ->
consequence remains unobserved. A sample release on update 51 remains a fixture
observation. The malformed INT32_MAX history counter from the earlier packet
remains outside the initialized range and is not a reported game crash. A wider
manager guarantee still needs valid finite links, updater/foreign normal effects,
noninterference and actual invocation/ownership where the claim requires them.

All bounded helpers terminated. No game, PC control, instrument, service,
save/configuration/reference mutation or peer-process change. The parked menu
budget remains spent and its extension unapproved. Goal ACTIVE/NOT_MET;
independent review and full L1+L2 completion remain outstanding.
