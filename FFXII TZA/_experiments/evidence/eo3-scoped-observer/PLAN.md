# EO3: scoped observer preparation

Question: for a primary map `.efb` raw-path request, what full heap pointer P
reaches the producer, what low32 value enters the completed queue record, and
what pointer Q reaches the issuer? Competing cases: P is preserved; upper bits
are discarded without sign fill; low32 bit31 produces a sign-filled Q; or the
selected route never produces a fully observable request. The historical EO3
crash cause remains a separate question.

Consumers: FABLE resource-request-queue semantics and OPUS request layout/ABI.
Existing exact reference and preflight establish narrowing, sign extension and
the corrected observation sites. Existing captures do not establish actual P.
Method A is sufficient for validating frame anchors and projecting retained
native contexts. Synthetic controls validate recorder decisions. A fresh live
observation is required for actual allocation/caller/scheduling; none occurs here.

Use the existing owned-event capture and full-context audit. The scoped addition
needs RDI/R10/RBX/RAX and stopped-event stack/path/slot reads; the old public hit
record lacks those registers. Correlate producer frame/return, completed builder
frame/return, and slot plus request ID. Do not use next-hit ordering as identity.
At0032E84D, RDI still holds the full pointer: mov EDX,EDI and mov ECX,FF do not
write it. One stopped context there supplies both original P and staged low32;
the additional0032E846 breakpoint demanded by current FABLE prose is unnecessary.
The exact-byte/static register-effect check is retained in staging.json.

Future state: exact reference executable SHA73461d0..., fresh clean designated
test process, backed-up modern Stepping000, visible Stepping baseline; retained
EXP026 Right1s then W1s reached Eastgate. That historical route is not fresh
proof that the gated primary requester at00377F82 executes. Verify its caller
return00377F87 and actual PS2Data/efb path; do not merge the auxiliary mode caller.
Use a no-trigger baseline and one complete normal request as delivery control.

Budgets: at most10s,8 producer events,32KiB of context/read payload,128 source
path bytes per selected event. Stop on the first complete isolated request.
Zero cases, missing state, ambiguous/reused identity, read failure, overflow or
incomplete chains cannot pass. Preserve raw successful and failed read receipts.

Stop escalation: P!=sign_extend(low32(P)) at the producer is a useful allocation
observation but cannot yet prove issuance or consequence. Do not deliberately
resume that selected call to seek a crash. A pending-event safe-close/abort path
must be qualified before deployment; the existing candidate's ordinary
resume-then-cleanup path is insufficient for this case. Pure controls do not
qualify this operating-system action. No fallback consequence breakpoint is
commissioned. New user stop/takeover halts automation without automatic restart.

Acceptance of live semantics additionally needs exact mapped module/tool identity,
actual trigger, no missing required events, before/after normal responsiveness,
fatal-dialog check, verified detach/handles and original save/config restoration.
The native FP context-transparency counterexample remains; narrowed context flags
are not a demonstrated fix. EXP127 remains INVALID_POST_TRACE with unknown cause.
No live launcher or automatic activation is provided by this preparation package.

Player version: this prepares a way to follow one area file through loading and
detect whether its memory address loses bits. It does not claim a new game run,
nor that a loading crash has been explained. PC control remains off.
