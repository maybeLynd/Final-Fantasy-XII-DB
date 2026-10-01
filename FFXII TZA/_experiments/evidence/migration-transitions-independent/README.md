# Transition admission: REJECT; write campaign incomplete

The actual immutable transition CLI admits malformed review links: truthy dictionary
commit, a non-SHA string commit and a dictionary record each produce a planned REPAIR.
An author-owned self-review produces planned INCORPORATE to a different owner. A list
author raises TypeError and aborts the plan rather than returning a malformed-field row.
Valid reject/accept, no-owner acceptance and missing/conflicting/string/missing-commit
controls establish the intended branches. Original in-memory apply/schema accepts the
emitted malformed tasks; no malformed task was applied to the production board.

Cause: commit truthiness and author membership are checked; commit/record representation
and reviewer-versus-author independence are not. OPUS owns cause/consumer repair and
re-review. This is actual CLI dry-run admission plus original-function in-memory effects,
not proof of applied malformed queue rows or false completed database packages.

The original full apply campaign is **INCOMPLETE**. One actual supported-writer REJECT
control created exactly one author repair. The next valid ACCEPT exceeded the20s caller
deadline; a private incorporation row/journal appeared afterward. That later write cannot
replace the lost caller receipt or establish nested process cleanup. Remaining write,
racing/idempotence and failed-writer-prefix controls did not execute and remain open.
No complete apply run, broad M2/A14/A16 or host cancellation acceptance is awarded.

Learning: unmodified Windows team.py uses one Local mutex name across board paths, so
copied fixture code is not independent of that kernel namespace. This is a possible
contention mechanism, not the proven timeout cause. subprocess.run only retained the
parent failure; exact nested-child tracking was missing. CIM was unavailable and psutil
was absent; no unverified process was killed, lock reaped or guard changed. Before another
write campaign, add owned descendant handles/cleanup and one bounded feasibility control;
do not retry the unchanged campaign or lengthen a deadline without detection controls.

Changed method: read-only CLI and in-memory original functions answer admission without
more contended writes. All fixtures are explicitly labelled and validated under the
unchanged identity/schema rules. They are disposable tests specifically authorized by
the existing request, not a new production board/bootstrap. Original source and partial
run remain immutable; no peer, game, save/config/reference or controller changes.
The active full L1+L2 goal continues; missing required write/host evidence remains open.
