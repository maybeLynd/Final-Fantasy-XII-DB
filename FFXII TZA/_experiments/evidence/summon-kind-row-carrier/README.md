# Special-sequence kind and action-row carrier

Method A, shipping EXE73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8.
No native/harness/game execution. Producer validity, independent acceptance and
canonical consumption are separate.

For a player: an ordinary Summon has an Esper value in its action row. This
check asks whether the later presentation step necessarily uses that same row.
It does not report a reproduced gameplay bug.

The existing canonical mode page already identifies kind1 with actions262..274,
and existing authored data identifies their Esper selectors27..39. That table
census is not new work. Original kind data is corroborated here only to connect
the code paths; one retained us table supplies the countermodel inputs.

`30CBE0` builds a row from queued record WORD+1C, forwards it to`30CE10`, and
`306BD0` classifies its row index into global`022C215C`. The initializer guards
re-entry using owner`022C2168`. That is an owner comparison, not row equality.

The complete normal code of`304850` runs from304850 through RET305041; its
catalog2088bytes also contains52bytes of switch data and2bytes of padding.
The13 switch destinations are derived from the original CMP12 guard. This
caller reads current action WORD`unit+714`, builds the row inR15 and passes it
at304F4D to306760 when row flags+0C bit30 is set. R15 reaching that call comes
from its current-row construction or null path; restored savedR15 paths do not
reach the call. This caller has no explicit RIP read of kind or owner. This
negative is local source scope, not a claim about transitive callee invariants.

`306760` retains incomingRDX inRDI, dispatches on kind, and kind1's arm reads
incoming row BYTE+26 intoCL and storesCL to battle-state5AD4. This is proved
at the store under normal external-call/ABI/noninterference premises, not the
full sequence's lifetime or subsequent effects.

The mathematical countermodel uses prior queued row262 (kind1, selector27)
and current row275 (Dismiss, bit30, selector0). Both are valid retained table
rows and their local bit/value conditions are compatible. It is NOT executed
original code or a naturally reached state. Upstream action scheduling,
ownership, registry stability and row-identity invariants may exclude it.

Result: kind1 by itself cannot establish27..39 for an arbitrary later incoming
row. The remaining discriminator is the original pending-to-current action
lifecycle: prove same row and relevant state remain paired through preparation,
commit and presentation, or identify the exact permitted replacement/abort.
No local countermodel proves that this happens in normal FF12. Actual resulting
battle-stats type, otherwriters/save restores, ownership and wholeOV42 remain
open. No live-absence probe or forced-call sample is warranted by this result.

Reproduce the producer from repo root using this directory's prove.py with a
fresh output name. It validates retained manifests/bytes, current shippingEXE,
reviewed access annotations and actual checked capture exits before deriving
complete caller CFG/dataflow and conditional countermodel. Control01 executes
three actual CLI refusals: failed prerequisite, missing source and coherent
same-size current-row R15->R14 mutation; each refuses specifically without a
result. These are producer checks, not additional original/game experiments.

Each frozen negative case records complete input identities. Unchanged case
inputs reference identically hashed base files; only differing inputs and actual
stdout/stderr/receipts are duplicated. To reproduce controls, make a disposable
copy of base inputs plus positive result/receipts, omit generated controls and
control-result/control-status outputs, and run original control.py there. Never
edit the published copy. Absolute recorded command paths describe original run.
All capture/CLI children terminal. No save/config/reference/peer process or PC
control changes; no restoration operation was needed.
