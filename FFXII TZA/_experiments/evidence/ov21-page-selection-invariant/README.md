# OV-21: original page selection, metadata and conditional occupancy

## What this package establishes

Method A verifies original instructions and local control flow. There is no
machine-code execution or real-game observation.

The descriptor's `+18` and `+1C` are independent DWORD page-list endpoints:
head and tail. Acquisition `0051F6B0` appends a page; removal `0051F880`
rewires predecessor/next and head/tail. A page record is indexed at stride
`0x20`, with DWORD `+0` identity, `+4` previous and `+8` next. The descriptor's
initial QWORD -1 at `+18` covers both endpoints. Original direct reads and
writes settle the split despite that larger initial store.

This contradicts the exact retained `RenderResourceEntryBank +018` row saying
its undivided eight-byte span is read on no path. OPUS owns the correction;
`consumer-preimage.json` preserves the original row and file identity.

The selector `0051F7A0` tests live-page count with a signed `<=0` branch to
`0051F825`, which calls acquisition at `0051F828`. It does not immediately
return. The `+022` row's contrary wording is also preserved for correction.
No assertion is made that negative counts are naturally admissible.

## Conditional invariant and counterexample

For the located ten-page, 32-slots-per-page bank, assume:

- stable valid table identity and initialized lifetime;
- live-page count equals the allocated page set;
- inactive pages have the free identity sentinel -1;
- the active head/next list is complete, finite and acyclic;
- the cursor denotes an active page when any page is active;
- each page occupancy is in 0..32 and the global count equals their sum;
- no interfering writes, and any handle resolution preserves these identities.

Then used < 320 cannot fail solely because the current page is full. The
selector returns a partial current/list page if one exists. Otherwise every
active page has 32 slots, so fewer than ten pages are active. Acquisition's
original increment/wrap/sentinel loop encounters a free page within ten reads.

`result-02.json` contains all ten circular cursor orders and the finite sentinel
classification certificate. The 10,240 classifications are mathematical checks
over cursor and occupancy masks, not native executions or gameplay samples.
The proof is tied to exact original loop, comparison, stride and link sites.
It is not a fixture presented as proving omitted initialization or scheduling.

The linked-walk proof does not establish that every original writer preserves
these premises. Its countermodel drops list completeness: ten active pages,
counts `[32,32,32,32,32,32,32,32,32,31]`, global used 319, full current page 0,
but head -1. The original selector then calls acquisition; acquisition's
full-live-page guard returns -1 and the selector returns NULL. This is a
composed static branch certificate, not an observed or naturally reachable
game state. Counts alone cannot establish coherent lookup metadata.

## Provenance, controls and history

Reference EXE SHA256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
Only acquisition/removal bodies were newly captured: 236 + 357 bytes.
The prior selector/constructor evidence from commit
`e92dc5bd5855f3bc7bfa4a449d81e2907158d619` is retained with its manifest and
actual capture receipts; it is not credited as a new capture or execution.

The actual capture uses the reviewed access-role adapter. The producer checks
both new and retained prerequisites, exact shipping bytes, annotations, complete
local CFG, explicit field-width/role evidence and required original operations.
`proof-02.*` / `result-02.json` are current. `proof-01.*` and its archived
driver retain the earlier wording before the active-cursor premise was made
explicit. Neither was a live observation.

`control-01` is INVALID_INCOMPLETE: its expected retained-status diagnostic was
wrong. The retained-input hash guard actually rejected the changed status
earlier, correctly. Raw receipts and the original control driver remain intact.
`control-02` validates that refusal and the earlier failed-new-capture refusal
from their exact prior raw identities, then runs only the missing-source and
coherent head-offset mutation cases. Four valid cause-specific refusals were
obtained through two retained and two new invocations. No unchanged settled
case was repeated. Missing or failed prerequisites cannot become a PASS through
a downstream result. The first failed patch application made no source change
and launched no proof; the corrected patch was applied before the actual run.

Reproduce with the existing project Python and `run.py proof-new prove.py
result-new.json`; immutable outputs refuse overwrite. Tool/dependency identities
and raw output are in the receipts. Independent review must rederive the source
relations and distinguish this conditional lemma from an inductive invariant.

## Canonical consumption and remaining work

OPUS should split/rename the endpoint fields and correct zero-count dispatch
after independent agreement, preserving history and using fresh owning-row
preimages. FABLE should retain the exact metadata prerequisites when explaining
OV-21 failure or designing a collector. No peer file was edited.

The remaining natural claim is whether initialization, all mutators, resource
binding and scheduling preserve complete list/count/sentinel coherence and
valid lifetime. The local append/unlink bodies supply evidence toward it but
do not establish all writers, opaque resolver effects, physical backing free,
same-key ownership, authored simultaneous-key bounds or natural exhaustion.
OV-21 remains open; there is no L3 or overall goal acceptance here.

No game, PC control, native harness, instruments, saves, settings, reference
bytes or peer processes were changed. All our child invocations are terminal.
The parked menu budget remains spent and its extension unapproved. The full
L1+L2 goal remains ACTIVE; independent work continues while review waits.

The first freeze was INVALID_INCOMPLETE: adding a second case-directory loop
reused `base`, which the inner input loop reassigned. It then attempted to create
a case under an existing file. No manifest/publication was produced. The exact
failed driver, observed failure and partial-tree identities are preserved in
freeze-01-driver.py/freeze-01-failure.json; the original partial tree remains
untouched. Freeze 02 uses a distinct `case_root` in the actual two-directory
path and a fresh destination/preflight receipt. Scientific proof and four valid
control refusals are unchanged; they were not rerun to fix packaging.
