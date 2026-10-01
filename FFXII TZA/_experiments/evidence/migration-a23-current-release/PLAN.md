# A23 deployed release verification, current-generation slice

Question: does the *currently served* dashboard and its portable export satisfy
the release record's deployed-source, matching-generation and independent-
receipt claims? Competing explanations: current server/generation/export are
coherent and version-bound; the release document describes an older version;
or deployed module identity/export membership is unavailable, leaving A23
unmeasured rather than accepted.

This is an independent read-only A23 slice under
`FRONTIER-REQ-ASTRA-WORKFLOW-INDEPENDENT-VERIFY`. Source record is
`_index/workflow/RELEASE-DASHBOARD-2026-09-29.md` (marked DELIVERED, NOT
ACCEPTED); its historical generation and PID are not current proof. Initial
HTTP feasibility at 2026-09-29T18:42Z returned generation
`g20260929T183844Z-d50c67`, empty problems, `reader_stale=false`, and
PARTIAL progress/VBF/executable/evidence/fleet. Preserve this raw response
separately; no acceptance inferred from it.

Method: read-only actual HTTP `/api/status`, root and view endpoints; inspect
the current generation manifest and export mechanism, exact current source
identities and any matching ZIP. Verify ZIP bytes/membership with the current
checker if available, using its actual process exit. Cross-check independent
receipts and release requirements. Positive control: a manifest-declared
served view resolves, matching its status and declared hash. Failure control:
an absent/mismatched required view or export cannot be PASS. Do not mutate
deployed store, server, controller, peer files or live game. If loaded module
PID/version or current export is inaccessible, keep that component
UNMEASURED and report the exact requirement; do not invent whole-host proof.

Stop after a specific A23 verdict or blocker. A23 acceptance needs more than
this HTTP slice: launcher/restart, test/deployment identities, matching export,
independent receipts and final owner acceptance must all be supported.
