# OV-21: original count publication and direct callback boundary

Method A. This package verifies original instruction order and a closed local
call graph; it does not execute FF12 machine code or launch the game.

## Result

Acquisition `0051FBB0` increments page `+14` at `0051FC71`, then bank total
`+58` at `0051FCB2`. On its successful local normal return, both writes occur
in that order. Earlier failure returns remain separate.

Release `0051FCF0`, admitted by total != 0, decrements the page via `0051FD5E`
before decrementing the total at `0051FE0C`. The earlier zero-total refusal
does not write either count. The admission is != 0, not a positivity or
valid-index guarantee. Negative, duplicate and stale inputs are not proven safe.

With valid coherent entry counts and no interference, the source arithmetic is:

| Operation | At entry (total / sum of pages) | After page write | After total write |
| --- | --- | --- | --- |
| Acquire last free slot | 319 / 319 | 319 / 320 | 320 / 320 |
| Release from full bank | 320 / 320 | 320 / 319 | 319 / 319 |

These are conditional calculations, not captured events. Equality between the
page sum and bank total is not maintained at every original instruction. The
previous conditional occupancy lemma needs a coherent operation boundary or
an explicitly identified stopped phase.

The complete direct callees between these writes are:

- acquisition: `003AB7F0`;
- release: `0051F880`, `003AB7F0`, `0020E620`;
- page unlink: `003AB7F0`;
- pointer reader `003AB7F0`: `0036B130`;
- `0036B130` and `0020E620`: no calls.

All these local bodies and return/branch paths are checked against the original
image. There is no callback or indirect dispatch in this graph. Pointer/base
readers have no nonstack memory writes; their saved-register writes are private
frame writes, requiring valid frames disjoint from the bank/tables. Page unlink
updates metadata; it is reached when the released page count is zero, and its
QWORD `+14` clear covers that already-zero count and page cursor `+18`.

`0020E620` is an arena-relative subtraction: ECX minus DWORD `[01F83530]`,
returned through EAX. It is not RNG or an allocation. This static code does not
establish the actual arena-base value in a loaded save.

The graph excludes a direct callback explanation through these particular
callees under ordinary valid execution. It does not prove thread ownership,
absence of asynchronous interference, natural caller reachability, completed
initialization, atomicity or lifetime across a transition.

## Evidence and reproduction

EXE SHA256:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
New capture contains release 308 bytes, pointer reader 99 bytes and arena helper
9 bytes. Acquisition, page unlink and handle-reader bytes are retained from
the earlier bank and name-binding packages, with manifests/provenance pinned
in `lineage.json`. They are not counted as new captures or executions.

`capture.py` uses the reviewed shared access-role adapter in the actual path.
`prove.py` checks new and retained prerequisites, exact original bytes, closed
local CFG and callee sets, count-store dominance on successful normal returns,
memory access roles and reader effects. `result-01.json` / `proof-01.*` are
current. Four actual CLI refusals cover failed new capture, changed retained
capture receipt, missing source and coherent page-count store-offset mutation.
The retained-input hash gate is correctly expected to reject before the status
gate. No empty or incomplete run is PASS.

The legacy name-binding capture receipt lacks terminal/exception fields. Its
source bytes are independently checked against the pinned EXE by this producer;
the old receipt is not promoted to native/live proof or credited as another run.

Use the project's existing Python with `run.py proof-new prove.py
result-new.json`. All outputs refuse overwrite. Raw stdout/stderr, interpreter
and driver identities, dependency hashes and case inputs remain available.
An early patch with a placeholder context was refused, changed no source and
launched no test. Only the completed applied source was executed.

## Consumer and observation implications

OPUS's bank contract and FABLE's owner/lifetime explanation should qualify
count/list consistency by operation phase after independent agreement. A
sampler reading individual fields asynchronously cannot assume an atomic tuple.
A one-count mismatch at an interior point alone does not establish persistent
corruption or natural exhaustion. A future observation must bind bank identity,
entry/return or stopped transition and timing of the relevant reads.

Remaining obligations are all-writer preservation, real caller/thread and
scheduling relationships, initialization/resource binding, owner/key cardinality
and natural exhaustion/reuse. The local callback explanation is narrowed;
actual concurrent interference remains unproved. No whole OV-21 closure or L3
parity is asserted.

No PC control, game, native harness, instruments, save/config/reference bytes
or peer processes/files were changed. All our producer/control processes are
terminal. Independent acceptance and canonical consumption are separate from
producer validity. The full L1+L2 goal stays ACTIVE; menu allowance remains
spent and its extension unapproved.
