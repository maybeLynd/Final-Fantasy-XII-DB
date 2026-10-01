# Repaired progress deltas use the named prior generation

**Scoped ACCEPT** at exact original repository source `17d6cdc2915b22b1743cdd2e2c6acc2fcdf6f5e2`, Method A. Independent cases came from the existing `9e84de6209f585650fb242f3a40f3ed8dc3643cd` histories/inputs, not OPUS's D6/D7 tests. No new generation was built and none of the prior files was overwritten.

Competing explanations: the progress selector still skips a newer verified generation without a progress view, or it now uses only the one generation selected for all deltas. The exact old Stores are copied byte-for-byte from the immutable capsule and tied to its member hashes. Original `Store.open_generation` verifies each admitted history entry. Actual original verification CLI status/result is checked against the **CURRENT** manifest, before selector execution. The missing-progress case has two such CURRENT CLI receipts (one per loop iteration); these do not independently verify the older generation or count as additional selector experiments. Its older entry's proof is the distinct original `open_generation` call.

| Retained input | Original repaired observation |
|---|---|
| Empty history | Both prior values None; no change block; measure says no prior |
| Latest verified generation has progress30/100 | Both prior identities name that generation; synthetic40/100 gives +10 accepted/0 scope/+10pp in both calculations |
| Older verified progress20/100, newer verified generation has no progress view | Prior progress None; change expression None; measure no prior; delta_basis names the **newer** generation |

The capture executes original `prior_generation`, repaired `prior_progress`, `annotate_deltas` and the **exact AST-selected change expression** from the original `requirements.measure` return dictionary. Its `change(...)` arm executes for the aligned case; its None arm for the other two. This is not a full `measure` invocation, adapter or `_build`. Original `_build` argument flow is statically bound: `prior_generation(st)` once, `prior_progress(pman,pdir)`, then `annotate_deltas(views,pdir,pman)`. The selector repair and named-basis consistency are supported at that boundary; actual end-to-end builder/deployment/browser behavior remains separately unverified.

Source/Git blobs, current preimages, loaded module paths, interpreter/driver identity, admitted parent manifests/inputs and unchanged copied Stores are retained. The raw capture has no exception and exits0. The read-only reducer checks completeness, actual required verifier exit/text, source and Store identity plus the cases; missing case and failed prerequisite with otherwise-good output refuse. No producer suite or old external audit is credited as our execution. Those are producer checks, not independent acceptance of ASTRA's evidence.

OPUS owns canonical repaired-source incorporation; the required nonauthor review of this evidence is separate. Preserve the earlier counterexample at its original source, the actual day-boundary versus immediate-prior wording debt assigned to DATA, and the wider My Progress/dashboard acceptance gaps. No real accepted database counts, terminal audits, loaded module/PID, rendered navigation, full migration or full L1+L2 completion follows. PC/browser/game control remains off; no server restart/build/save/config/reference changes. Menu allowance stays spent and its extension unapproved.

Player view: if the previous report lacks progress data, the dashboard must show “no prior” instead of silently reaching further back while naming the newer report. The repaired functions now do that on the retained test histories.
